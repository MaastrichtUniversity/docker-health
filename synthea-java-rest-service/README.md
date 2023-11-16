# To create new java classes from opts

Checkout https://github.com/ehrbase/openEHR_SDK

Build the repo 

Copy templates to root of the repository you just checked out

Modify the command below with the correct paths

```java  -jar generator/target/generator-2.5.0-SNAPSHOT.jar -opt ./diagnosis_demo.opt -out ../docker-health/synthea-java-rest-service/src/main/java -package com.example.restservice```