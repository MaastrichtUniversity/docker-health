# Health Data Platform

Setting-up a core clinical data repository to store data from different formats using [openEHR specifications](https://specifications.openehr.org/) and the [EHRbase API](https://ehrbase.org/about-ehrbase/).
EHRbase provides a standard-based backend for interoperable clinical applications, implementing the latest version of the openEHR Reference Model and the Archetype Definition Language (AQL).

This service is based on repositories:
- [dh-hdp-demodata](https://github.com/MaastrichtUniversity/dh-hdp-demodata): Simulation of hospital data
- [dh-hdp-templates](https://github.com/um-datahub/dh-hdp-templates): Custom-made openEHR templates
- [dh-hdp-etl](https://github.com/MaastrichtUniversity/dh-hdp-etl): ETL Python script
- [dh-hdp-transform-rest](https://github.com/MaastrichtUniversity/dh-hdp-transform-rest): Java REST API for data class transformation into openEHR compositions
- [dh-hdp-notebooks](https://github.com/MaastrichtUniversity/dh-hdp-notebooks): Jupyter notebooks for an initial data exploration

## Requirements

### Encryption between filebeat and elk

CA certificates need to be manually stored in folder `filebeat/certs`

### Add this virtual host entry in your /etc/hosts file
```
127.0.0.1 ehrbase.local.dh.unimaas.nl
127.0.0.1 jupyter.local.dh.unimaas.nl
127.0.0.1 transform.local.dh.unimaas.nl
```

## Run the stack

After up and running the stack, open your browser and try [http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html](http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html) with the following credentials:
```
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
```
Credentials can be updated in `./ehrbase/.env.ehrbase`

### Clone the external repositories

```
./rit.sh externals clone
./rit.sh externals checkout 2024.1
```

### Generate synthetic dataset

Synthetic patient generator using Synthea with n=1000 patients.

```
./rit.sh data
```

### Start the data exploration Jupyter notebook

```
./rit.sh data-exploration
```
Open your browser and try [http://jupyter.local.dh.unimaas.nl](http://jupyter.local.dh.unimaas.nl) using the following token:
```
SERVER_APP_TOKEN=aa3ca297f81ed69a3fcab71ff886d5cf3207be09960f6de7
```

### Start the EHRbase backend

```
./rit.sh backend
```

Go to your browser and try this:
```
http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
```
Update the credentials in `./ehrbase/.env.ehrbase`

### Run the ETL demo

Extract the synthetic data using csv files, Transform the data into valid EHRbase compositions by using a java REST API and Load the compositions into EHRbase.

```
./rit.sh demo
```

### Kill the whole stack

```
./rit.sh down
```
