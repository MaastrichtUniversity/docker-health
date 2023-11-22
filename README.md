# Docker-health

Main repository for the HDP project.
The current services:
- EHRbase
- ETL-demo

# Add this virtual host entry in your /etc/hosts file
```
127.0.0.1	ehrbase.local.dh.unimaas.nl
127.0.0.1	jupyter.local.dh.unimaas.nl
127.0.0.1	javarest.local.dh.unimaas.nl
```

Go to your browser and try this:
```
http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
```
Update the credentials in `./ehrbase/.env.ehrbase`

# Run the stack

## Clone the external repositories

```
./rit.sh externals clone
./rit.sh externals checkout develop
```

## Create the synthetic dataset

```
./rit.sh data
```

## Start the data  exploration Jupyter notebook

```
./rit.sh data-exploration
```
open browser and goto [jupyter.local.dh.unimaas.nl](jupyter.local.dh.unimaas.nl)

## Start the EHRbase backend

```
./rit.sh backend
```


## Run ETL demo

**WIP**

```
./rit.sh demo
```

# Run the java rest synthea demo

```
docker compose build java-rest-demo
docker compose up java-rest-demo
```

Swagger interface is now at http://localhost:8081/swagger-ui/index.html
or http://javarest.local.dh.unimaas.nl/swagger-ui/index.html

## diagnosis
```
curl -X 'POST' \
  'http://localhost:8081/diagnosis-demo' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "startTime": "2011-10-18T20:29:31Z",
  "endTime": "2010-10-18T20:29:31Z",
  "dateClinicallyRecognised": "2017-10-18T20:29:31Z",
  "diagnosisValue": "Anemia (disorder)",
  "diagnosisSNOMEDCode": "271737000"
}'
```

## patient
```
curl -X 'POST' \
  'http://localhost:8081/patient' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
    "startTime": "2011-10-18T20:29:31Z",
    "sexAssignedAtBirth": "Male",
    "dateOfBirth": "2000-10-18T20:29:31Z",
    "dateOfDeath": "2000-10-18T20:29:31Z"
}'

```


## vital_signs

Minimum
```
curl -X 'POST' \
  'http://localhost:8081/vital_signs' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
    "startTime": "2011-10-18T20:29:31Z"
}'
```

Extended
```
curl -X 'POST' \
  'http://localhost:8081/vital_signs' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "startTime": "2011-10-18T20:29:31Z",
  "bodyHeightObservation": {
    "pointInTime": [
      {
        "bodyHeightMagnitude": 185,
        "bodyHeightUnits": "cm",
        "timeValue": "1999-12-18T04:05:06Z"
      },
      {
        "bodyHeightMagnitude": 173,
        "bodyHeightUnits": "cm",
        "timeValue": "2023-12-18T01:02:03Z"
      }	
    ]
  }
}'
```

Will return a valid composition


## Kill the whole stack

```
./rit.sh down
```


# Specified command-lines
```
docker exec -it hdp-etl-demo-1 bash
```

```
python ETL.py --help
Usage: ETL.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get-all-ehr-id      Get all EHR ID on a specific openEHR instance
  list-all-templates  Print all template available on the server
  run                 Runs all ETL from default hard coded values
```
