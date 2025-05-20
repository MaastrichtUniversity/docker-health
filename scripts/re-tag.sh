#!/bin/bash

######################
####  docker-bake.hcl
######################

cp docker-bake.hcl docker-bake.hcl.bak

# dh-hdp-transform-rest 
cd externals/dh-hdp-transform-rest
TRANSFORM_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i s/transform-rest:\${ENV_TAG}/transform-rest:${TRANSFORM_BRANCH}/ docker-bake.hcl

# dh-hdp-federation-api
cd externals/dh-hdp-federation-api
FEDERATION_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i s/federation-rest:\${ENV_TAG}/federation-rest:${FEDERATION_BRANCH}/ docker-bake.hcl
sed -i s/federation-test:\${ENV_TAG}/federation-test:${FEDERATION_BRANCH}/ docker-bake.hcl

# dh-hdp-notebooks
cd externals/dh-hdp-notebooks
NOTEBOOKS_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i s/jupyter-zib:\${ENV_TAG}/jupyter-zib:${NOTEBOOKS_BRANCH}/ docker-bake.hcl

# dh-hdp-etl
cd externals/dh-hdp-etl
ETL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i s/etl-zib-test:\${ENV_TAG}/etl-zib-test:${ETL_BRANCH}/ docker-bake.hcl
sed -i s/etl-zib-rest:\${ENV_TAG}/etl-zib-rest:${ETL_BRANCH}/ docker-bake.hcl
sed -i s/etl-zib-pipeline:\${ENV_TAG}/etl-zib-pipeline:${ETL_BRANCH}/ docker-bake.hcl

# dh-hdp-portal
cd externals/dh-hdp-portal
PORTAL_TAG=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i s/portal:\${ENV_TAG}/portal:${PORTAL_TAG}/ docker-bake.hcl