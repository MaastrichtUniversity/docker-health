# Health Data Platform

Setting-up a core clinical data repository to store data from different formats using openEHR specifications.

This service is based on:
- Synthea, a tool to generate synthetic patients
- EHRbase API, a clinical data repository implementing the openEHR Reference Model
- Java REST API, an EHRbase's SDK permitting the transformation of data objects into valid openEHR compositions
- Jupyter notebook for an initial data exploration

The current services:
- EHRbase
- ETL-demo

# Add this virtual host entry in your /etc/hosts file
```
127.0.0.1 ehrbase.local.dh.unimaas.nl
127.0.0.1 jupyter.local.dh.unimaas.nl
127.0.0.1 javarest.local.dh.unimaas.nl
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

## Generate synthetic dataset

Synthetic patient generator using Synthea with n=1000 patients.

```
./rit.sh data
```

## Start the data exploration Jupyter notebook

```
./rit.sh data-exploration
```
open browser and go to [jupyter.local.dh.unimaas.nl](jupyter.local.dh.unimaas.nl)

## Start the EHRbase backend

EHRbase provides a standard-based backend for interoperable clinical applications, implementing the latest version of the openEHR Reference Model and the Archetype Definition Language (AQL).

```
./rit.sh backend
```

## Run the ETL demo

Extract the synthetic data using csv files, Transform the data into valid compositions by using a java-rest API and Load the compositions into the EHRbase.

```
./rit.sh demo
```

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
  run                 Runs all ETL for a single patient.
```
