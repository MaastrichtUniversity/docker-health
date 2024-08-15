# Health Data Platform

Setting-up a core clinical data repository to store data from different formats using [openEHR specifications](https://specifications.openehr.org/) and the [EHRbase API](https://ehrbase.org/about-ehrbase/).
EHRbase provides a standard-based backend for interoperable clinical applications, implementing the latest version of the openEHR Reference Model and the Archetype Definition Language (AQL).

This service is based on repositories:

- [dh-hdp-demodata](https://github.com/MaastrichtUniversity/dh-hdp-demodata/tree/2024.1): Simulation of hospital data
- [dh-hdp-templates](https://github.com/um-datahub/dh-hdp-templates/tree/2024.1): Custom-made openEHR templates
- [zib-templates](https://github.com/um-datahub/zib-templates/tree/2024.1): Custom-made openEHR templates matching the Dutch ZIBs
- [dh-hdp-etl](https://github.com/MaastrichtUniversity/dh-hdp-etl/tree/2024.1): ETL Python script
- [dh-hdp-transform-rest](https://github.com/MaastrichtUniversity/dh-hdp-transform-rest/tree/2024.1): Java REST API for data class transformation into openEHR compositions
- [dh-hdp-fhir-bridge](https://github.com/MaastrichtUniversity/dh-hdp-fhir-bridge/tree/2024.1): Java REST API for converting FHIR messages into openEHR composition and storage into EHRbase
- [dh-hdp-notebooks](https://github.com/MaastrichtUniversity/dh-hdp-notebooks/tree/2024.1): Jupyter notebooks for an initial data exploration

## Requirements

### Encryption between filebeat and elk

CA certificates need to be manually stored in folder `filebeat/certs`.
The present files are used for development-purposes.

### Add these virtual host entries in your /etc/hosts file

```
127.0.0.1 ehrbase.local.dh.unimaas.nl
127.0.0.1 transform.local.dh.unimaas.nl
127.0.0.1 fhir-bridge.local.dh.unimaas.nl
127.0.0.1 jupyter-zib.local.dh.unimaas.nl
127.0.0.1 jupyter-synthea.local.dh.unimaas.nl
127.0.0.1 openehrtool.local.dh.unimaas.nl
```

## Run the stack

### Clone the external repositories

```
./rit.sh externals clone
./rit.sh externals checkout 2024.1
```

### Generate synthetic dataset

Synthetic patient generator using Synthea with n=1000 patients.

```
./rit.sh demo-data
```

### Start the Jupyter notebook for data exploration and live demo

```
./rit.sh jupyter-synthea # or jupyter-zib
```

Open your browser and try [http://jupyter-synthea.local.dh.unimaas.nl](http://jupyter-synthea.local.dh.unimaas.nl) (or [http://jupyter-zib.local.dh.unimaas.nl](http://jupyter-zib.local.dh.unimaas.nl)) using the following token:

```
SERVER_APP_TOKEN=aa3ca297f81ed69a3fcab71ff886d5cf3207be09960f6de7
```

### Start the EHRbase backend

```
./rit.sh backend
```

Open your browser and try [http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html](http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html) with the following credentials:

```
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
```

Credentials can be updated in `./ehrbase/.env.ehrbase`

### Run the ETL

Extract data from csv files, Transform the data into valid openEHR compositions by using a REST API and Load the compositions into EHRbase.

#### ETL workflows specific to demo templates.

```
./rit.sh demo
```

#### ETL workflows specific to ZIB templates.

```
./rit.sh zib
```

### Kill the whole stack

```
./rit.sh down
```

### Start FHIR-bridge

Convert FHIR messages into openEHR compositions and them into EHRbase

Before starting, build the image in dh-hdp-fhir-bridge (check the README file in [dh-hdp-fhir-bridge](https://github.com/um-datahub/dh-hdp-fhir-bridge/tree/2024.1) for the command)

```
./rit.sh fhir
```

Open your browser and try [http://fhir-bridge.local.dh.unimaas.nl/fhir-bridge](http://fhir-bridge.local.dh.unimaas.nl/fhir-bridge).

### Start openehr-Tools [for DEV environment only]

Tool for interacting with the EHRbase server with a basic dashboard integrated.

```
./rit.sh up -d openehrtool
```

Open your browser and try [https://openehrtool.local.dh.unimaas.nl](https://openehrtool.local.dh.unimaas.nl)
