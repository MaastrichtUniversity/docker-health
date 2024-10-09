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
externals="externals/dh-hdp-templates https://github.com/um-datahub/dh-hdp-templates.git
externals/dh-hdp-zib-templates https://github.com/um-datahub/dh-hdp-zib-templates.git
externals/dh-hdp-transform-rest https://github.com/MaastrichtUniversity/dh-hdp-transform-rest.git
externals/dh-hdp-notebooks https://github.com/MaastrichtUniversity/dh-hdp-notebooks.git
externals/dh-hdp-fhir-bridge https://github.com/MaastrichtUniversity/dh-hdp-fhir-bridge.git
externals/dh-hdp-etl https://github.com/MaastrichtUniversity/dh-hdp-etl.git"


is_local(){
    if [[ $RIT_ENV == "local" ]]; then
      return 0;
    fi
    return 1;

}

setup_requirements(){
    echo -e "Build ${HDP_ZIB_TEMPLATES_IMAGE_NAME} image"
    docker build -t "${HDP_ZIB_TEMPLATES_IMAGE_NAME}" ./externals/dh-hdp-zib-templates/

    echo -e "Update permissions of the folder filebeat/logs/ehrdb/"
    mkdir -p ./filebeat/logs/ehrdb && chmod -R 777 ./filebeat/logs/ehrdb
    mkdir -p ./filebeat/logs/ehrbase && chmod -R 777 ./filebeat/logs/ehrbase
}

dev_setup_requirements(){
    if is_local; then
      setup_requirements
    fi
}

# do the required action in case of externals or exec
if [[ $1 == "externals" ]]; then
    action=${ARGS/$1/}
    run_repo_action ${action} "${externals}"
    exit 0
fi

if [[ $1 == "setup" ]]; then
    setup_requirements
    exit 0
fi

if [[ $1 == "transform" ]]; then
    dev_setup_requirements
    echo -e "\nStart Spring boot Rest API"
    if is_local; then docker compose build transform-rest filebeat; fi
    docker compose up -d transform-rest

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "zib" ]]; then
    dev_setup_requirements
    if is_local; then docker compose build filebeat etl-zib transform-rest; fi

    echo -e "\nRunning etl-zib"
    docker compose up -d etl-zib
    until docker compose logs --tail 100 etl-zib 2>&1 | grep -q "Print all EHR ids available on the server";
    do
      echo -e "Waiting for etl-zib"
      sleep 5
    done

    echo -e "\nPrint logs for etl-zib"
    docker compose logs etl-zib

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "jupyter-zib" ]]; then
    dev_setup_requirements
    echo -e "\nExplore zib dataset"
    if is_local; then docker compose build jupyter-zib transform-rest; fi
    docker compose up -d jupyter-zib

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "fhir" ]]; then
    echo -e "\nStart FHIR Bridge"
    docker compose up -d fhir-bridge
    until docker compose logs --tail 100 fhir-bridge 2>&1 | grep -q "Started FhirBridgeApplication in";
    do
      echo -e "Waiting for FhirBridgeApplication"
      sleep 10
    done

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "fhir-etl" ]]; then
    dev_setup_requirements
    echo -e "\nStart FHIR Bridge"
    docker compose up -d fhir-bridge
    until docker compose logs --tail 100 fhir-bridge 2>&1 | grep -q "Started FhirBridgeApplication in";
    do
      echo -e "Waiting for FhirBridgeApplication"
      sleep 10
    done

    echo -e "\nRunning etl-zib"
    if is_local; then docker compose build etl-zib; fi
    docker compose up -d etl-zib
    until docker compose logs --tail 100 etl-zib 2>&1 | grep -q "Print all EHR ids available on the server";
    do
    echo -e "Waiting for etl-zib"
      sleep 5
    done
    echo -e "\nPrint logs for etl-zib"
    docker compose logs etl-zib

    echo -e "\nExit rit.sh"
    exit 0
fi

if [[ $1 == "backend" ]]; then
    dev_setup_requirements
    docker compose up -d ehrbase
    until docker container inspect --format "{{json .State.Health.Status }}" dev-hdp-ehrbase-1 2>&1 | grep -q "healthy";
    do
      echo -e "Waiting for EhrBase"
      sleep 10
    done

    echo -e "\nEHRbase up and running, exiting rit.sh"
    exit 0
fi

if [[ $1 == "test" ]]; then
    dev_setup_requirements
    echo -e "\nStart ETL-ZIB test"
    if is_local; then docker compose build etl-zib transform-rest; fi
    docker compose run --rm --entrypoint pytest etl-zib --verbose --verbosity=5
#    docker compose run --rm --entrypoint pytest etl-zib -s
#    docker compose run --rm --entrypoint pytest etl-zib -o log_cli=true --log-cli-level=INFO

    exit 0
fi


docker compose $ARGS