# Health Data Platform

Setting-up a core clinical data repository to store data from different formats using [openEHR specifications](https://specifications.openehr.org/) and [EHRbase API](https://ehrbase.org/about-ehrbase/).

This service is based on repositories:
- [dh-hdp-demodata](https://github.com/MaastrichtUniversity/dh-hdp-demodata): Simulation of hospital data
- [dh-hdp-templates](https://github.com/MaastrichtUniversity/dh-hdp-templates): Custom-made openEHR templates
- [dh-hdp-etl](https://github.com/MaastrichtUniversity/dh-hdp-etl): ETL Python script
- [dh-hdp-transform-rest](https://github.com/MaastrichtUniversity/dh-hdp-transform-rest): Java REST API for data class transformation into openEHR compositions
- [dh-hdp-notebooks](https://github.com/MaastrichtUniversity/dh-hdp-notebooks): Jupyter notebooks for an initial data exploration

# Add this virtual host entry in your /etc/hosts file
```
127.0.0.1 ehrbase.local.dh.unimaas.nl
127.0.0.1 jupyter.local.dh.unimaas.nl
127.0.0.1 transform.local.dh.unimaas.nl
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
open browser and go to [jupyter.local.dh.unimaas.nl](http://jupyter.local.dh.unimaas.nl)

## Start the EHRbase backend

EHRbase provides a standard-based backend for interoperable clinical applications, implementing the latest version of the openEHR Reference Model and the Archetype Definition Language (AQL).

```
./rit.sh backend
```

Go to your browser and try this:
```
http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
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
