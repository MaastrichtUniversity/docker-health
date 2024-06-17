#!/usr/bin/env bash

set -e

. ./lib-hdp.sh
. ./.env

ARGS="$@ "
if [[ ${ARGS} = *"-vv "* ]]; then
   export LOGTRESHOLD=$DBG
   ARGS="${ARGS/-vv /}"
elif [[ ${ARGS} = *"--verbose "* ]] || [[ ${ARGS} = *"-v "* ]]; then
   export LOGTRESHOLD=$INF
   ARGS="${ARGS/--verbose /}"
   ARGS="${ARGS/-v /}"
fi

# set RIT_ENV if not set already
env_selector

# Set the prefix for the project
COMPOSE_PROJECT_NAME="dev-hdp"
export COMPOSE_PROJECT_NAME

# specify externals for this project
externals="externals/dh-hdp-demodata https://github.com/MaastrichtUniversity/dh-hdp-demodata.git
externals/dh-hdp-templates https://github.com/um-datahub/dh-hdp-templates.git
externals/zib-templates https://github.com/um-datahub/zib-templates.git
externals/dh-hdp-transform-rest https://github.com/MaastrichtUniversity/dh-hdp-transform-rest.git
externals/dh-hdp-notebooks https://github.com/MaastrichtUniversity/dh-hdp-notebooks.git
externals/dh-hdp-etl https://github.com/MaastrichtUniversity/dh-hdp-etl.git"


# do the required action in case of externals or exec
if [[ $1 == "externals" ]]; then
    action=${ARGS/$1/}
    run_repo_action ${action} "${externals}"
    exit 0
fi

if [[ $1 == "demo-data" ]]; then
    echo -e "\nGenerate a synthetic dataset"
    docker compose build demo-data
    docker compose up demo-data

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "transform-demo" ]]; then
    docker build -t "${HDP_DEMO_TEMPLATES_IMAGE_NAME}" ./externals/dh-hdp-templates/
    echo -e "\nStart Spring boot Rest API"
    docker compose build transform-rest-demo proxy filebeat
    docker compose up -d transform-rest-demo proxy filebeat

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "data-exploration" ]]; then
    echo -e "\nExplore synthea dataset"
    docker compose build data-exploration proxy
    docker compose up -d data-exploration proxy

    echo -e "\nExit rit.sh"
    exit 0
fi


if [[ $1 == "demo" ]]; then
    docker build -t "${HDP_DEMO_TEMPLATES_IMAGE_NAME}" ./externals/dh-hdp-templates/
    echo -e "Update permissions of the folder filebeat/logs/ehrdb/"
    mkdir -p ./filebeat/logs/ehrdb && chmod -R 777 ./filebeat/logs/ehrdb
    echo -e "\nStart EHRbase Rest API"
    docker compose build ehrbase proxy filebeat
    docker compose up -d ehrbase proxy filebeat
    until docker compose logs --tail 100 ehrbase 2>&1 | grep -q "Started EhrBase in";
    do
    echo -e "Waiting for EhrBase"
      sleep 10
    done
    echo -e "\nStart Spring boot Rest API"
    docker compose build transform-rest-demo
    docker compose up -d transform-rest-demo
    sleep 3
    echo -e "\nRunning etl-demo"
    docker compose build etl-demo
    docker compose up -d etl-demo
    sleep 15
    echo -e "\nPrint logs for etl-demo"
    docker compose logs etl-demo

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "zib" ]]; then
    docker build -t "${HDP_ZIB_TEMPLATES_IMAGE_NAME}" ./externals/zib-templates/
    echo -e "Update permissions of the folder filebeat/logs/ehrdb/"
    mkdir -p ./filebeat/logs/ehrdb && chmod -R 777 ./filebeat/logs/ehrdb
    echo -e "\nStart EHRbase Rest API"
    docker compose build ehrbase proxy filebeat
    docker compose up -d ehrbase proxy filebeat
    until docker compose logs --tail 100 ehrbase 2>&1 | grep -q "Started EhrBase in";
    do
    echo -e "Waiting for EhrBase"
      sleep 10
    done
    echo -e "\nStart Spring boot Rest API"
    docker compose build transform-rest-zib
    docker compose up -d transform-rest-zib
    sleep 3
    echo -e "\nRunning etl-zib"
    docker compose build etl-zib
    docker compose up -d etl-zib
    sleep 15
    echo -e "\nPrint logs for etl-zib"
    docker compose logs etl-zib

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "demo-zib" ]]; then
    docker build -t "${HDP_ZIB_TEMPLATES_IMAGE_NAME}" ./externals/zib-templates/
    echo -e "Update permissions of the folder filebeat/logs/ehrdb/"
    mkdir -p ./filebeat/logs/ehrdb && chmod -R 777 ./filebeat/logs/ehrdb

    echo -e "\nExplore synthea dataset"
    docker compose build proxy demo-sprint-6
    docker compose up -d proxy demo-sprint-6

    echo -e "\nStart EHRbase Rest API"
    docker compose build ehrbase
    docker compose up -d ehrbase
    until docker compose logs --tail 100 ehrbase 2>&1 | grep -q "Started EhrBase in";
    do
    echo -e "Waiting for EhrBase"
      sleep 10
    done

    echo -e "\nStart Sprint boot Rest API"
    docker compose build transform-rest-zib
    docker compose up -d transform-rest-zib

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "backend" ]]; then
    docker compose up -d ehrbase proxy filebeat
    until docker compose logs --tail 100 ehrbase 2>&1 | grep -q "Started EhrBase in";
    do
      echo -e "Waiting for EhrBase"
      sleep 10
    done

    echo -e "\nEHRbase up and running, exiting rit.sh"
    exit 0
fi

docker compose $ARGS