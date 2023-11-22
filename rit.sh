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
    echo "Generate a synthetic dataset"
    docker compose build demo-data
    docker compose up demo-data

    echo "Exit rit.sh"
    exit 0
fi

if [[ $1 == "java" ]]; then
    echo "Start Sprint boot Rest API"
    docker compose build java-rest-demo
    docker compose up -d proxy java-rest-demo

    echo "Exit rit.sh"
    exit 0
fi

if [[ $1 == "data-exploration" ]]; then
    echo "Explore synthea dataset"
    docker compose build data-exploration
    docker compose up -d proxy data-exploration

    echo "Exit rit.sh"
    exit 0
fi


if [[ $1 == "demo" ]]; then
    docker compose build
    docker compose up -d ehrbase proxy
    until docker logs --tail 30 hdp-ehrbase-1 2>&1 | grep -q "Started EhrBase in";
    do
      echo "Waiting for EhrBase"
      sleep 10
    done

    echo "Running etl-demo"
    docker compose up -d etl-demo
    # sleep 5
    # echo "Print logs for etl-demo"
    # docker compose logs etl-demo

    echo "Exit rit.sh"
    exit 0
fi

if [[ $1 == "backend" ]]; then
    docker compose up -d ehrbase proxy
    until docker logs --tail 30 hdp-ehrbase-1 2>&1 | grep -q "Started EhrBase in";
    do
      echo "Waiting for EhrBase"
      sleep 10
    done

    echo "EHRbase up and running, exiting rit.sh"
    exit 0
fi

docker compose $ARGS