# Docker-health

Main repository for the HDP project.
The current services:
- EHRbase
- ETL-demo

# Add this virtual host entry in your /etc/hosts file
```
127.0.0.1	ehrbase.local.dh.unimaas.nl
```

Go to your browser and try this:
```
http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
```
Update the credentials in `./ehrbase/.env.ehrbase`

# Run the stack
```
./rit.sh demo
```

# Run the java rest synthea demo

```
docker compose build java-rest-demo
docker compose up java-rest-demo
```

Swagger interface is now at http://localhost:8081/swagger-ui/index.html


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
  "diagnosisSNOMEDCode": "271737000",
  "genderSNOMEDCode": "248153007",
  "genderValue": "Male"
}'
```

Will return a valid composition
