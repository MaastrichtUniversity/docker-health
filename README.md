# Health Data Platform

Setting-up a core clinical data repository to store data from different formats using [openEHR specifications](https://specifications.openehr.org/) and the [EHRbase API](https://ehrbase.org/about-ehrbase/).
EHRbase provides a standard-based backend for interoperable clinical applications, implementing the latest version of the openEHR Reference Model and the Archetype Definition Language (AQL).

This service is based on repositories:

- [dh-hdp-zib-templates](https://github.com/um-datahub/dh-hdp-zib-templates/tree/2024.1): Custom-made openEHR templates matching the Dutch ZIBs
- [dh-hdp-etl](https://github.com/MaastrichtUniversity/dh-hdp-etl/tree/2024.1): ETL Python script
- [dh-hdp-transform-rest](https://github.com/MaastrichtUniversity/dh-hdp-transform-rest/tree/2024.1): Java REST API for data class transformation into openEHR compositions
- [dh-hdp-notebooks](https://github.com/MaastrichtUniversity/dh-hdp-notebooks/tree/2024.1): Jupyter notebooks for an initial data exploration

Aditional proof of concept level repositiory:

- [dh-hdp-federation-api](https://github.com/MaastrichtUniversity/dh-hdp-federation-api/tree/2024.1): Proof of concept Federation service
- [dh-hdp-node-ui](https://github.com/MaastrichtUniversity/dh-hdp-node-ui/tree/2024.1): Proof of concept Node User Interface service

## Requirements

### Encryption between filebeat and elk

CA certificates need to be manually stored in folder `filebeat/certs`.
The present files are used for development-purposes.

### Add these virtual host entries in your /etc/hosts file

```
127.0.0.1 test.ehrbase.local.dh.unimaas.nl
127.0.0.1 test.openehrtool.local.dh.unimaas.nl

127.0.0.1 transform.local.dh.unimaas.nl
127.0.0.1 jupyter.local.dh.unimaas.nl
```

### Template variables

For each new template, add its `template_id` and semantic version (`sem_ver`) as variables into
`env_files/zib-templates.env`).

Variables `api_route` and `filename` can be auto-generated by running the bash script `./env_files/append_template_variables.sh`
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

### Start the EHRbase backend

Start the default test backend:
```
./dh.sh backend
```

Open your browser and try [http://test.ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html](http://test.ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html) with the following credentials:

```
SECURITY_AUTHUSER=user0
SECURITY_AUTHPASSWORD=foobar0
```
Credentials can be updated in `.env`.

For a specific node, e.g mumc:
```
./dh.sh backend mumc
```

### Run the ETL

Extract data from csv files, transform the data into valid openEHR compositions by using a REST API and load the compositions into EHRbase.

Start the default test node:
```
./dh.sh etl
```

For a specific node, e.g mumc:
```
./dh.sh etl mumc
```

Recreate the ETL stack:

```
./dh.sh up -d --force-recreate test-ehrdb test-ehrbase test-etl-zib
```

### Run the tests

Start the dev environment for a single node and execute all the tests

```
./dh.sh test single-node
```

- Execute all the tests

```
./dh.sh run --rm --entrypoint pytest test-etl-zib --verbose --verbosity=5
```

- Execute a specific class test

```
./dh.sh run --rm --entrypoint pytest test-etl-zib --verbose --verbosity=5 tests/test_burgerlijke_staat.py::TestBurgerlijkeStaat2017
```

- Execute a single test

```
./dh.sh run --rm --entrypoint pytest test-etl-zib --verbose --verbosity=5 tests/test_all_zib_pipelines.py::TestAllZibPipelines::test_number_of_templates
```

### Kill the whole stack

```
./dh.sh down
```

### Start openehr-Tools [for DEV environment only]

Tool for interacting with the EHRbase server with a basic dashboard integrated.

```
./dh.sh openehrtool
```

Open your browser and try [http://test.openehrtool.local.dh.unimaas.nl](http://test.openehrtool.local.dh.unimaas.nl)

For a specific node, e.g mumc:
```
./dh.sh openehrtool mumc
```

### Start the Jupyter notebook for data exploration and live demo

```
./dh.sh jupyter
```

Open your browser and try [http://jupyter.local.dh.unimaas.nl](http://jupyter.local.dh.unimaas.nl) using the following token:

```
SERVER_APP_TOKEN=aa3ca297f81ed69a3fcab71ff886d5cf3207be09960f6de7
```

### POC Federated EHRBase nodes

#### Add these virtual host entries in your /etc/hosts file

```
127.0.0.1 mumc.ehrbase.local.dh.unimaas.nl
127.0.0.1 mumc.openehrtool.local.dh.unimaas.nl
127.0.0.1 mumc-ui.local.dh.unimaas.nl
127.0.0.1 zio.ehrbase.local.dh.unimaas.nl
127.0.0.1 zio.openehrtool.local.dh.unimaas.nl
127.0.0.1 zio-ui.local.dh.unimaas.nl
127.0.0.1 federation.local.dh.unimaas.nl
```

#### Run the federation

Up each node, load data and start the federation API:

```
./dh.sh federation
```

To run the federation service API integration test:
```
./dh.sh test federation
```

User Interfaces available at [mumc-ui.local.dh.unimaas.nl](mumc-ui.local.dh.unimaas.nl) & [zio-ui.local.dh.unimaas.nl](zio-ui.local.dh.unimaas.nl)

(To run the node UI on each node: `./dh.sh node-ui mumc; ./dh.sh node-ui zio`)


(Optional)
To run openEHR tool on each node:

```
./dh.sh openehrtool mumc; ./dh.sh openehrtool zio
```
