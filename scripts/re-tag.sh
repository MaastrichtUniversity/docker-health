#!/bin/bash

######################
####  docker-bake.hcl
######################

cp docker-bake.hcl docker-bake.hcl.bak

# dh-hdp-transform-rest 
cd externals/dh-hdp-transform-rest
TRANSFORM_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i "s#transform-rest:\${ENV_TAG}#registry.prod.dh.unimaas.nl/docker-health/transform-rest:${TRANSFORM_BRANCH}#" docker-bake.hcl

# dh-hdp-federation-api
cd externals/dh-hdp-federation-api
FEDERATION_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i "s#federation-api:\${ENV_TAG}#registry.prod.dh.unimaas.nl/docker-health/federation-api:${FEDERATION_BRANCH}#" docker-bake.hcl

# dh-hdp-notebooks
cd externals/dh-hdp-notebooks
NOTEBOOKS_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i "s#jupyter-zib:\${ENV_TAG}#registry.prod.dh.unimaas.nl/docker-health/jupyter-zib:${NOTEBOOKS_BRANCH}#" docker-bake.hcl

# dh-hdp-etl
cd externals/dh-hdp-etl
ETL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i "s#etl-zib:\${ENV_TAG}#registry.prod.dh.unimaas.nl/docker-health/etl-zib:${ETL_BRANCH}#" docker-bake.hcl

# dh-hdp-portal
cd externals/dh-hdp-portal
PORTAL_TAG=$(git rev-parse --abbrev-ref HEAD)
cd ../..
sed -i "s#portal:\${ENV_TAG}#registry.prod.dh.unimaas.nl/docker-health/portal:${PORTAL_TAG}#" docker-bake.hcl
