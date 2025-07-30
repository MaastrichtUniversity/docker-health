[![Development Status](https://img.shields.io/badge/Development%20Status-Alpha-red)](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha)


**⚠️ ALPHA - Under Active Development and Quality Assurance ⚠️**

This project is currently in its alpha stage. It is actively being developed, and we are in the process of conducting thorough quality assurance testing. Therefore, expect potential instability and incomplete features.

-----------

![openFHIR logo](https://open-fhir.com/images/openFIHR-logo-color-dark-horizontal-1.svg)

openFHIR is an engine that implements [FHIR Connect specification](https://sevkohler.github.io/FHIRconnect-spec/build/site/FHIRconnect/v1.0.0/index.html) and facilitates bidirectional mappings between openEHR and FHIR.
It is an open source edition of the commercial offering available at https://open-fhir.com

## [Documentation](https://open-fhir.com/documentation/index.html)
## [Sandbox](https://sandbox.open-fhir.com/)

## Build
### With docker and docker-compose

Build the docker image
```
docker-compose build
```

Run all services
```
docker-compose up
```

### Build with Maven
Build the jar
```
mvn clean package
```

Setup postgres (skip if postgres is locally configured)
```
docker-compose up db
```

Run using
```
java -jar target/*.jar
```

When it's running browse to Swagger UI --> http://localhost:8080/swagger-ui/index.html
