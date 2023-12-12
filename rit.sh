#!/usr/bin/env bash

set -e

. ./lib-hdp.sh

ARGS="$@ "
if [[ ${ARGS} = *"-vv "* ]]; then
   export LOGTRESHOLD=$DBG
   ARGS="${ARGS/-vv /}"
elif [[ ${ARGS} = *"--verbose "* ]] || [[ ${ARGS} = *"-v "* ]]; then
   export LOGTRESHOLD=$INF
   ARGS="${ARGS/--verbose /}"
   ARGS="${ARGS/-v /}"
fi


# Set the prefix for the project
COMPOSE_PROJECT_NAME="hdp"
export COMPOSE_PROJECT_NAME

# specify externals for this project
externals="externals/dh-demodata https://github.com/MaastrichtUniversity/dh-demodata.git
externals/hdp-models https://github.com/MaastrichtUniversity/hdp-models.git"


# do the required action in case of externals or exec
if [[ $1 == "externals" ]]; then
    action=${ARGS/$1/}
    run_repo_action ${action} "${externals}"
    exit 0
fi

if [[ $1 == "data" ]]; then
    echo -e "\nGenerate a synthetic dataset"
    docker compose build demo-data
    docker compose up demo-data

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "java" ]]; then
    echo -e "\nStart Sprint boot Rest API"
    docker compose build java-rest
    docker compose up -d java-rest proxy

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "data-exploration" ]]; then
    echo -e "\nExplore synthea dataset"
    docker compose build data-exploration
    docker compose up -d proxy data-exploration

    echo -e "\nExit rit.sh"
    exit 0
fi


if [[ $1 == "demo" ]]; then

    echo -e "\nStart EHRbase Rest API"
    docker compose build
    docker compose up -d ehrbase proxy
    until docker logs --tail 100 hdp-ehrbase-1 2>&1 | grep -q "Started EhrBase in";
    do
    echo -e "Waiting for EhrBase"
      sleep 10
    done

    echo -e "\nStart Sprint boot Rest API"
    docker compose build java-rest
    docker compose up -d java-rest

    echo -e "\nRunning etl-demo"
    docker compose up -d etl-demo
    # sleep 5
    echo -e "\nPrint logs for etl-demo"
    docker compose logs etl-demo

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "backend" ]]; then
    docker compose up -d ehrbase proxy
    until docker logs --tail 30 hdp-ehrbase-1 2>&1 | grep -q "Started EhrBase in";
    do
      echo -e "Waiting for EhrBase"
      sleep 10
    done

    echo -e "\nEHRbase up and running, exiting rit.sh"
    exit 0
fi

docker compose $ARGS