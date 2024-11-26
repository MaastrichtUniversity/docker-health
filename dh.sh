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
externals/dh-hdp-etl https://github.com/MaastrichtUniversity/dh-hdp-etl.git
externals/dh-hdp-federation-api https://github.com/MaastrichtUniversity/dh-hdp-federation-api.git"


is_local(){
    if [[ $RIT_ENV == "local" ]]; then
      return 0;
    fi
    return 1;
}

setup_requirements(){
    echo -e "Update permissions of the ehrbase and ehrdb filebeat/logs"
    mkdir -p ./filebeat/logs/mumc/ehrdb && chmod -R 777 ./filebeat/logs/mumc/ehrdb
    mkdir -p ./filebeat/logs/mumc/ehrbase && chmod -R 777 ./filebeat/logs/mumc/ehrbase
    mkdir -p ./filebeat/logs/gp/ehrdb && chmod -R 777 ./filebeat/logs/gp/ehrdb
    mkdir -p ./filebeat/logs/gp/ehrbase && chmod -R 777 ./filebeat/logs/gp/ehrbase
}

build_and_up_common_services() {
    echo "Building common services: proxy, filebeat, transform-rest"
    docker compose build proxy filebeat transform-rest

    echo "Starting common services"
    docker compose up -d proxy filebeat transform-rest
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

    echo -e "\nExit dh.sh"
    exit 0
fi

if [[ $1 == "federation" ]]; then
    dev_setup_requirements
    echo -e "\nStart FastAPI"
    if is_local; then docker compose build federation-api filebeat; fi
    docker compose up -d federation-api

    echo -e "\nExit dh.sh"
    exit 0
fi

if [[ $1 == "zib" ]]; then
    dev_setup_requirements
    if is_local; then build_and_up_common_services; fi
    if [[ -z "$2" ]]; then
        docker compose -f docker-compose.mumc-node.yml build etl-zib
        echo -e "\nRunning etl-zib"
        docker compose -f docker-compose.mumc-node.yml up -d etl-zib
        # Add a safe guard against infinite loop during a CI execution
        SAFE_GUARD=0
        until docker compose logs --tail 100 etl-zib 2>&1 | grep -q "Print all EHR ids available on the server";
        do
          if [[ $SAFE_GUARD -eq 15  ]]; then
            echo -e "STOP waiting for etl-zib"
            break
          fi
          ((SAFE_GUARD++))
          echo -e "Waiting for etl-zib"
          sleep 5
        done

        if [[ $SAFE_GUARD -ne 15  ]]; then
          echo -e "\nPrint logs for etl-zib"
          docker compose logs etl-zib
          echo -e "\nExit dh.sh"
          exit 0
        else
          echo -e "\nFailed to run etl-zib"
          exit 1
        fi
    else
        docker compose -f docker-compose.gp-node.yml build etl-zib2
          echo -e "\nRunning etl-zib gp node"
        docker compose -f docker-compose.gp-node.yml up -d etl-zib2
        # Add a safe guard against infinite loop during a CI execution
        SAFE_GUARD=0
        until docker compose logs --tail 100 etl-zib2 2>&1 | grep -q "Print all EHR ids available on the server";
        do
          if [[ $SAFE_GUARD -eq 15  ]]; then
            echo -e "STOP waiting for etl-zib2"
            break
          fi
          ((SAFE_GUARD++))
          echo -e "Waiting for etl-zib2"
          sleep 5
        done

        if [[ $SAFE_GUARD -ne 15  ]]; then
          echo -e "\nPrint logs for etl-zib2"
          docker compose logs etl-zib2
          echo -e "\nExit dh.sh"
          exit 0
        else
          echo -e "\nFailed to run etl-zib2"
          exit 1
        fi
    fi    
fi

if [[ $1 == "jupyter-zib" ]]; then
    dev_setup_requirements
    # The ehrbase server needs to be up with its respective .env in the docker compose of jupyter-zib
    echo -e "\nExplore zib dataset"
    if is_local; then docker compose build jupyter-zib transform-rest; fi
    docker compose up -d jupyter-zib

    echo -e "\nExit dh.sh"
    exit 0
fi

#if [[ $1 == "fhir" ]]; then
#    echo -e "\nStart FHIR Bridge"
#    docker compose up -d fhir-bridge
#    until docker compose logs --tail 100 fhir-bridge 2>&1 | grep -q "Started FhirBridgeApplication in";
#    do
#      echo -e "Waiting for FhirBridgeApplication"
#      sleep 10
#    done
#
#    echo -e "\nExit dh.sh"
#    exit 0
#fi


if [[ $1 == "backend" ]]; then
    dev_setup_requirements
    if [[ -z "$2" ]]; then
        docker compose -f docker-compose.mumc-node.yml up -d ehrbase
        until docker container inspect --format "{{json .State.Health.Status }}" dev-hdp-ehrbase-1 2>&1 | grep -q "healthy";
        do
          echo -e "Waiting for EhrBase (first node)"
          sleep 10
        done
        echo -e "\nEHRbase first node up and running, exiting dh.sh"
    else
        docker compose -f docker-compose.gp-node.yml up -d ehrbase2
        until docker container inspect --format "{{json .State.Health.Status }}" dev-hdp-ehrbase2-1 2>&1 | grep -q "healthy";
        do
          echo -e "Waiting for EhrBase2 (GP node)"
          sleep 10
        done

        echo -e "\nEHRbase2 up and running, exiting dh.sh"
    fi

    exit 0
fi


if [[ $1 == "down" ]]; then
    echo -e "Bringing down services from all compose files"

    docker compose -f docker-compose.yml down
    docker compose -f docker-compose.mumc-node.yml down
    docker compose -f docker-compose.second-node.yml down
    
    exit 0
fi

if [[ $1 == "openehrtool" ]]; then
    if [[ -z "$2" ]]; then
        docker compose -f docker-compose.mumc-node.yml up -d openehrtool
        echo -e "\nOpenEHRtool on mumc node up and running, exiting dh.sh"
    else
        docker compose -f docker-compose.gp-node.yml up -d openehrtool2
        echo -e "\nOpenEHRtool on gp node up and running, exiting dh.sh"
    fi

    exit 0
fi

if [[ $1 == "test" ]]; then
    dev_setup_requirements
    echo -e "\nStart ETL-ZIB test"
    if is_local; then build_and_up_common_services; fi
    if [[ -z "$2" ]]; then
        docker compose -f docker-compose.mumc-node.yml build etl-zib
        docker compose -f docker-compose.mumc-node.yml run --rm --entrypoint pytest etl-zib --verbose --verbosity=5
    #    docker compose -f docker-compose.mumc-node.yml run --rm --entrypoint pytest etl-zib -s
    #    docker compose -f docker-compose.mumc-node.yml run --rm --entrypoint pytest etl-zib -o log_cli=true --log-cli-level=INFO
    else
        docker compose -f docker-compose.gp-node.yml build etl-zib2
        docker compose -f docker-compose.gp-node.yml run --rm --entrypoint pytest etl-zib --verbose --verbosity=5
    #    docker compose -f docker-compose.gp-node.yml run --rm --entrypoint pytest etl-zib -s
    #    docker compose -f docker-compose.gp-node.yml run --rm --entrypoint pytest etl-zib -o log_cli=true --log-cli-level=INFO
    fi


    if [ $? -eq 0 ]; then
      echo -e "\nExit dh.sh"
      exit 0
    else
      echo -e "\nFailed to run etl-zib tests"
      exit 1
    fi
fi


docker compose $ARGS