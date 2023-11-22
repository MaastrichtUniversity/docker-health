#!/usr/bin/env bash
set -e

SECURITY_AUTHUSER=ehrbase-user
SECURITY_AUTHPASSWORD=SuperSecretPassword
BASE_URL=http://localhost:8080/ehrbase 

DIR="ehrbase-v0.31.0"
# Check if the directory exists
if [ -d "$DIR" ]; then
    # Directory exists, so remove it
    echo "Directory $DIR already exists. Removing..."
    sudo rm -r "$DIR/.pgdata"
    rm -rf "$DIR"
    
fi

# Starting a local ehrbase
git clone --depth 1 -b v0.31.0 https://github.com/ehrbase/ehrbase ehrbase-v0.31.0
cd ehrbase-v0.31.0
docker compose up -d
cd - 
echo "### sleep 30s for composition to start ### \n"
sleep 30

# 1. Upload/Post OPT to ehr REST end point. Note: web_templates upload/post not suported on ecsis end point
echo "### upload/post OPT ### \n"
response=$(curl -u $SECURITY_AUTHUSER:$SECURITY_AUTHPASSWORD -v \
-X POST -H "Content-Type: application/xml" \
-d @./data/templates/vital_signs.opt \
$BASE_URL/rest/openehr/v1/definition/template/adl1.4 2>&1)

http_status=$(echo "$response" | grep -oP "(?<=HTTP/1.1 )\d+" | tail -1)

# Check the status code
if [ "$http_status" == "204" ]; then
    # Extract ETag if status is 204
    etag=$(echo "$response" | grep "ETag:" | awk '{print $2}' | tr -d '"')
    echo "Template file vital_signs.opt has been uploaded. ETag: $etag"
elif [ "$http_status" == "409" ]; then
    echo "HTTP 409 Conflict, template already on ehrbase"
    exit 1
else
    echo "Error: HTTP status $http_status"
    exit 1
fi

# 2. Generate ehrID on ECIS end point

# We have a name associated to the ehrid

SUBJECT_ID=patient001
SUBJECT_NAMESPACE=datahub
echo "### using patient name: ${SUBJECT_ID} on namespace: ${SUBJECT_NAMESPACE} ### \n"

response=$(curl -u $SECURITY_AUTHUSER:$SECURITY_AUTHPASSWORD  \
-X 'POST' -H 'accept: */*' \
"${BASE_URL}/rest/ecis/v1/ehr?subjectId=${SUBJECT_ID}&subjectNamespace=${SUBJECT_NAMESPACE}" 2>&1)


json_response=$(echo "$response" | sed -n '/^{/,$p')

EHR_ID=$(echo $json_response | jq -r '.ehrId')
queryable=$(echo $json_response | jq -r '.ehrStatus.queryable')
modifiable=$(echo $json_response | jq -r '.ehrStatus.modifiable')

# Check if ehrId is not null or empty
if [ -z "$EHR_ID" ]; then
    echo "Change subject ID, it is likely already existing"
else
    # Output values
    echo "EHR ID: $EHR_ID"
    echo "Queryable: $queryable"
    echo "Modifiable: $modifiable"
fi

#EHR ID: 5005f67a-d184-4060-91b6-8c36e817cb3c
#Queryable: false
#Modifiable: false

#3. lets make ehrid modifiable and queriable (optional?)

echo "### making ehr queriable and findable ###\n"""
#EHR_ID=5005f67a-d184-4060-91b6-8c36e817cb3c
response=$(curl  -u $SECURITY_AUTHUSER:$SECURITY_AUTHPASSWORD \
   -X 'PUT' \
  "${BASE_URL}/rest/ecis/v1/ehr/${EHR_ID}/status" \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
"subjectId": "patient004",
"subjectNamespace": "datahub",
"queryable": true,
"modifiable": true
}' 2>&1)

#echo $response

json_response=$(echo "$response" | sed -n 's/.*{/{/p')
echo "$json_reponse"


# 4. Export vital signs template (OPT) as webTemplate:
# Note vital signs templateId is extracted from OPT
#  <template_id>
#    <value>Vital signs</value>
#  </template_id>
echo "### Getting webtemplate from OPT template ### \n"
curl -u $SECURITY_AUTHUSER:$SECURITY_AUTHPASSWORD \
  -H 'accept: application/json' \
  "${BASE_URL}/rest/ecis/v1/template/Vital%20signs" | jq '.' > ./data/templates/vital_signs.webtemplate

echo "### vital signal webtemplate ### \n"
head -30 ./data/templates/vital_signs.webtemplate

#5. Get template example (composition) in flat format with random data

# some formats are not supported
echo "### Getting multiple formats into data/templates folder ### \n"
FORMATS=("FLAT" "STRUCTURED" "XML" "JSON")
for format in "${FORMATS[@]}"; do
    # Make the curl request and save the output to a file
    curl -v -u $SECURITY_AUTHUSER:$SECURITY_AUTHPASSWORD \
    -H 'accept: application/json' \
    -o "./data/compositions/vital_signs.${format,,}" \
    "${BASE_URL}/rest/ecis/v1/template/Vital%20signs/example?FORMAT=${format}"

done

# 6. Simplify flat composition example (only work with temperature)
echo "###  Simplify flat composition example (only work with temperature) ### \n"

{
    echo "{"
grep -E 'category|context|body_temperature|vital_signs2/language\|code|vital_signs2/language\|terminology|territory|composer' \
./data/compositions/vital_signs.flat 
echo "}"
} > ./data/compositions/temperature.flat

echo "### looking into temperature flat composition ###\n"
head -30  ./data/compositions/temperature.flat

echo "### setting temperature with correct values 37c ###\n"
# replace multiple "vital_signs2/body_temperature/any_event:0/temperature|magnitude" with 
# 37.0c intead of random value 50c
sed -E 's/("vital_signs2\/body_temperature\/any_event:[0-9]+\/temperature\|magnitude" : )[0-9]+\.[0-9]+/\137.0/' ./data/compositions/temperature.flat > ./data/compositions/modified_temperature.flat
# The generated flat composition file can be pushed to REST

# Submit composition and get its identification and URL
echo "### submit composition get composition identifier ###\n"
curl -v -X 'POST' \
  -u $SECURITY_AUTHUSER:$SECURITY_AUTHPASSWORD \
  "${BASE_URL}/rest/ecis/v1/composition?format=FLAT&templateId=Vital%20signs&ehrId=${EHR_ID}" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @./data/compositions/modified_temperature.flat

sleep 30 
cd ehrbase-v0.31.0
docker compose down
cd - 
echo "That's it , maybe comment the docker compose down to see the composition url ?!"