# Health Data Platform

Setting-up a core clinical data repository to store data from different formats using [openEHR specifications](https://specifications.openehr.org/) and the [EHRbase API](https://ehrbase.org/about-ehrbase/).
EHRbase provides a standard-based backend for interoperable clinical applications, implementing the latest version of the openEHR Reference Model and the Archetype Definition Language (AQL).

This service is based on repositories:

- [dh-hdp-templates](https://github.com/um-datahub/dh-hdp-templates/tree/2024.1): Custom-made openEHR templates
- [dh-hdp-zib-templates](https://github.com/um-datahub/dh-hdp-zib-templates/tree/2024.1): Custom-made openEHR templates matching the Dutch ZIBs
- [dh-hdp-etl](https://github.com/MaastrichtUniversity/dh-hdp-etl/tree/2024.1): ETL Python script
- [dh-hdp-transform-rest](https://github.com/MaastrichtUniversity/dh-hdp-transform-rest/tree/2024.1): Java REST API for data class transformation into openEHR compositions
- [dh-hdp-fhir-bridge](https://github.com/MaastrichtUniversity/dh-hdp-fhir-bridge/tree/2024.1): Java REST API for converting FHIR messages into openEHR composition and storage into EHRbase
- [dh-hdp-notebooks](https://github.com/MaastrichtUniversity/dh-hdp-notebooks/tree/2024.1): Jupyter notebooks for an initial data exploration

Aditional proof of concept level repositiory:

- [dh-hdp-federation-api](https://github.com/MaastrichtUniversity/dh-hdp-federation-api): Proof of concept Federation service

## Requirements

### Encryption between filebeat and elk

CA certificates need to be manually stored in folder `filebeat/certs`.
The present files are used for development-purposes.

### Add these virtual host entries in your /etc/hosts file

```
127.0.0.1 ehrbase.local.dh.unimaas.nl
127.0.0.1 transform.local.dh.unimaas.nl
127.0.0.1 fhir-bridge.local.dh.unimaas.nl
127.0.0.1 jupyter.local.dh.unimaas.nl
127.0.0.1 openehrtool.local.dh.unimaas.nl
```

### Template variables

For each new template, add its `template_id` and semantic version (`sem_ver`) as variables into the corresponding env
file (for the ZIB, use `env_files/etl_zib.env`). `api_route` and `filename` variables can be auto-generated by running
the bash script `./env_files/append_template_variables.sh`
(after adding a new `create_dynamic_template_variables ${template_id}` line).

## Run the stack

### Clone the external repositories

```
./dh.sh externals clone
./dh.sh externals checkout 2024.1
```

### Run the setup requirements

```
./dh.sh setup
```

### Start the Jupyter notebook for data exploration and live demo

```
./dh.sh jupyter-zib
```

Open your browser and try [http://jupyter.local.dh.unimaas.nl](http://jupyter.local.dh.unimaas.nl) using the following token:

```
SERVER_APP_TOKEN=aa3ca297f81ed69a3fcab71ff886d5cf3207be09960f6de7
```

### Start the EHRbase backend

```
./dh.sh backend
```

Open your browser and try [http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html](http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html) with the following credentials:

```
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
```

Credentials can be updated in `./ehrbase/.env.ehrbase`

### Run the ETL

Extract data from csv files, Transform the data into valid openEHR compositions by using a REST API and Load the compositions into EHRbase.

#### ETL workflows specific to ZIB templates.

```
./dh.sh zib
```

### Run the tests

Start the dev environment and execute all the tests

```
./dh.sh test
```

For more specific test execution, add the following line within `test` in `dh.sh`:

- Execute all the tests

```
docker compose -f docker-compose.mumc-node.yml run --entrypoint pytest etl-zib --verbose --verbosity=5
```

- Execute a specific class test

```
docker compose -f docker-compose.mumc-node.yml run --entrypoint pytest etl-zib --verbose --verbosity=5 tests/test_burgerlijke_staat.py::TestBurgerlijkeStaat2017
```

- Execute a single test

```
docker compose -f docker-compose.mumc-node.yml run --entrypoint pytest etl-zib --verbose --verbosity=5 tests/test_all_zib_pipelines.py::TestAllZibPipelines::test_number_of_templates
```

### Recreate the ETL stack

```
./dh.sh up -d --force-recreate ehrdb ehrbase etl-zib
```

### Kill the whole stack

```
./dh.sh down
```

### Start FHIR-bridge

Convert FHIR messages into openEHR compositions and them into EHRbase

Before starting, build the image in dh-hdp-fhir-bridge (check the README file in [dh-hdp-fhir-bridge](https://github.com/MaastrichtUniversity/dh-hdp-fhir-bridge/tree/2024.1) for the command)

```
./dh.sh fhir
```

Open your browser and try [http://fhir-bridge.local.dh.unimaas.nl/fhir-bridge](http://fhir-bridge.local.dh.unimaas.nl/fhir-bridge).

Run the following command to run both fhir-bridge and etl-zib:

```
./dh.sh up -d fhir-bridge && ./dh.sh up -d etl-zib && ./dh.sh logs -f etl-zib fhir-bridge
```

### Start openehr-Tools [for DEV environment only]

Tool for interacting with the EHRbase server with a basic dashboard integrated.

```
./dh.sh up -d openehrtool
```

Open your browser and try [http://openehrtool.local.dh.unimaas.nl](http://openehrtool.local.dh.unimaas.nl)

### POC Federated EHRBase nodes

Add these virtual hosts to your /etc/hosts

```
127.0.0.1 ehrbase2.local.dh.unimaas.nl
127.0.0.1 openehrtool2.local.dh.unimaas.nl
127.0.0.1 federation.local.dh.unimaas.nl
```

Up each node, load data and start the federation API:

```
./dh.sh zib; ./dh.sh zib 2; ./dh.sh federation
```

(Optional)
To run openEHR tool on each node, run:

```
./dh.sh openehrtool; ./dh.sh openehrtool 2
```
