# To create new java classes from opts

Checkout https://github.com/ehrbase/openEHR_SDK

Build the repo 

Copy templates to root of the repository you just checked out

Modify the command below with the correct paths

```java  -jar generator/target/generator-2.5.0-SNAPSHOT.jar -opt ./diagnosis_demo.opt -out ../docker-health/synthea-java-rest-service/src/main/java -package com.example.restservice```

# Set environment variables for configuration

``` DIAGNOSIS_SEM_VER=0.4.0;EHRBASE_BASE_URL="http://ehrbase.dh.local:8080/ehrbase/";PATIENT_SEM_VER=0.2.0;VITAL_SIGNS_SEM_VER=0.2.0;EHRBASE_USERNAME=user;EHRBASE_PASSWORD=foobar```