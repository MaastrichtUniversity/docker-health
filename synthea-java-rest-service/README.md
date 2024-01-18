# Health Data Plateform -- Java REST API

Data class transformation into openEHR compositions is based on a Java REST API, a software development kit provided by EHRbase
https://github.com/ehrbase/openEHR_SDK

Java classes are automatically generated. Functions should be added/updated in `dto` and `transform` folders.
The connection between the ETL python script and the Java class is done by writing a pydantic Basemodel class using the Field option


## Generation of Java classes

- Build the https://github.com/ehrbase/openEHR_SDK repository

- Connect opt templates to `src/main/resources` of the repository

- Modify the command below with the correct paths

```java  -jar generator/target/generator-2.5.0-SNAPSHOT.jar -opt ./diagnosis_demo.opt -out ../docker-health/synthea-java-rest-service/src/main/java -package com.example.restservice```

- Set environment variables for configuration

``` DIAGNOSIS_SEM_VER=0.4.0;EHRBASE_BASE_URL="http://ehrbase.dh.local:8080/ehrbase/";PATIENT_SEM_VER=0.2.0;VITAL_SIGNS_SEM_VER=0.2.0;EHRBASE_USERNAME=user;EHRBASE_PASSWORD=foobar```



## Run the java rest synthea demo

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
        "magnitude": 185,
        "units": "cm",
        "timeValue": "1999-12-18T04:05:06Z"
      },
      {
        "magnitude": 173,
        "units": "cm",
        "timeValue": "2023-12-18T01:02:03Z"
      }	
    ]
  }
}'
```

Will return a valid composition
