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
externals="externals/dh-hdp-zib-templates https://github.com/um-datahub/dh-hdp-zib-templates.git
externals/dh-hdp-transform-rest https://github.com/MaastrichtUniversity/dh-hdp-transform-rest.git
externals/dh-hdp-etl https://github.com/MaastrichtUniversity/dh-hdp-etl.git
externals/dh-hdp-federation-api https://github.com/MaastrichtUniversity/dh-hdp-federation-api.git
externals/dh-hdp-notebooks https://github.com/MaastrichtUniversity/dh-hdp-notebooks.git
externals/dh-hdp-node-ui https://github.com/MaastrichtUniversity/dh-hdp-node-ui.git"


# Create docker network dev-hdp_hdp-dh-mumc-net if it does not exists
if [ ! $(docker network ls --filter name=dev-hdp_hdp-dh-mumc-net --format="true") ]; then
  echo "Creating network dev-hdp_hdp-dh-mumc-net"
  docker network create dev-hdp_hdp-dh-mumc-net --subnet "172.32.1.0/24" --label "com.docker.compose.project"="dev-hdp" --label "com.docker.compose.network"="hdp-dh-mumc-net"
fi

# Create docker network dev-hdp_hdp-dh-zio-net if it does not exists
if [ ! $(docker network ls --filter name=dev-hdp_hdp-dh-zio-net --format="true") ]; then
  echo "Creating network dev-hdp_hdp-dh-zio-net"
  docker network create dev-hdp_hdp-dh-zio-net --subnet "172.33.1.0/24" --label "com.docker.compose.project"="dev-hdp" --label "com.docker.compose.network"="hdp-dh-zio-net"
fi

# Create docker network dev-hdp_hdp-dh-envida-net if it does not exists
if [ ! $(docker network ls --filter name=dev-hdp_hdp-dh-envida-net --format="true") ]; then
  echo "Creating network dev-hdp_hdp-dh-envida-net"
  docker network create dev-hdp_hdp-dh-envida-net --subnet "172.34.1.0/24" --label "com.docker.compose.project"="dev-hdp" --label "com.docker.compose.network"="hdp-dh-envida-net"
fi

# Create docker network dev-hdp_hdp-dh-test-net if it does not exists
if [ ! $(docker network ls --filter name=dev-hdp_hdp-dh-test-net --format="true") ]; then
  echo "Creating network dev-hdp_hdp-dh-test-net"
  docker network create dev-hdp_hdp-dh-test-net --subnet "172.31.1.0/24" --label "com.docker.compose.project"="dev-hdp" --label "com.docker.compose.network"="hdp-dh-test-net"
fi


is_local(){
    if [[ $RIT_ENV == "local" ]]; then
      return 0;
    fi
    return 1;
}

setup_requirements(){
    echo -e "Update permissions of the ehrbase and ehrdb filebeat/logs/$1"
    mkdir -p ./filebeat/logs/$1/ehrdb && chmod -R 777 ./filebeat/logs/$1/ehrdb
    mkdir -p ./filebeat/logs/$1/ehrbase && chmod -R 777 ./filebeat/logs/$1/ehrbase
}

dev_setup_requirements(){
    if is_local; then
      setup_requirements $1
    fi
}

check_argument(){
  # Check if the second argument is empty or not "zio"/"mumc"/"envida"
  if [[ -z "$1" || ( "$1" != "mumc" && "$1" != "zio" && "$1" != "envida" ) ]]; then
    echo "Error: The second argument must be either 'mumc', 'zio' or 'envida'"
    exit 1
  fi
}

build_and_up_common_services() {
    echo "Building common services: proxy, filebeat, transform-rest"
    docker compose build proxy filebeat transform-rest

    echo "Starting common services"
    docker compose up -d proxy filebeat transform-rest
}

# do the required action in case of externals or exec
if [[ $1 == "externals" ]]; then
    action=${ARGS/$1/}
    run_repo_action ${action} "${externals}"
    exit 0
fi

if [[ $1 == "setup" ]]; then
    setup_requirements "mumc"
    setup_requirements "zio"
    setup_requirements "envida"
    setup_requirements "test"

    echo -e "\nExit dh.sh"
    exit 0
fi

if [[ $1 == "transform" ]]; then
    echo -e "\nStart Spring boot Rest API"
    if is_local; then docker compose build transform-rest filebeat; fi
    docker compose up -d transform-rest

    echo -e "\nExit dh.sh"
    exit 0
fi

if [[ $1 == "federation" ]]; then
    dev_setup_requirements "mumc"
    dev_setup_requirements "zio"
    dev_setup_requirements "envida"

    echo -e "\nStart FastAPI"
    if is_local; then docker compose build federation-api filebeat; fi
    docker compose up -d federation-api

    echo -e "\nExit dh.sh"
    exit 0
fi

run_etl_zib(){
    dev_setup_requirements $1
    if is_local; then build_and_up_common_services; fi
    docker compose build $1-etl-zib
    echo -e "\nRunning $1-etl-zib"
    docker compose up -d $1-etl-zib
    # Add a safe guard against infinite loop during a CI execution
    SAFE_GUARD=0
    until docker compose logs --tail 15 $1-etl-zib 2>&1 | grep -q "Print all EHR ids available on the server";
    do
      if [[ $SAFE_GUARD -eq 15  ]]; then
        echo -e "STOP waiting for $1-etl-zib"
        break
      fi
      ((SAFE_GUARD++))
      echo -e "Waiting for $1-etl-zib"
      sleep 5
    done

    if [[ $SAFE_GUARD -ne 15  ]]; then
      echo -e "\nPrint logs for $1-etl-zib"
      docker compose logs $1-etl-zib
      echo -e "\nExit dh.sh"
      exit 0
    else
      echo -e "\nFailed to run $1-etl-zib"
      exit 1
    fi
}

if [[ $1 == "etl" ]]; then
    if [[ -z "$2" ]]; then
        run_etl_zib "test"
    else
        check_argument "$2"
        run_etl_zib "$2"
    fi
fi

run_backend(){
    dev_setup_requirements $1
    docker compose up -d $1-ehrbase
    until docker container inspect --format "{{json .State.Health.Status }}" dev-hdp-$1-ehrbase-1 2>&1 | grep -q "healthy";
    do
      echo -e "Waiting for EHRbase ($1 node)"
      sleep 10
    done
    echo -e "\nEHRbase ($1 node) up and running"
}

if [[ $1 == "backend" ]]; then
    if [[ -z "$2" ]]; then
        run_backend "test"
    else
        check_argument "$2"
        run_backend "$2"
    fi

    echo -e "\nExit dh.sh"
    exit 0
fi

if [[ $1 == "jupyter" ]]; then
    dev_setup_requirements "mumc"
    dev_setup_requirements "zio"
    dev_setup_requirements "envida"

    echo -e "\nExplore zib dataset"
    if is_local; then docker compose build jupyter-zib transform-rest; fi
    docker compose up -d jupyter-zib

    echo -e "\nExit dh.sh"
    exit 0
fi

run_openehrtool(){
    docker compose up -d $1-openehrtool
    echo -e "\nOpenEHRtool on $1 node up and running"
}

if [[ $1 == "openehrtool" ]]; then
    if [[ -z "$2" ]]; then
      run_openehrtool "test"
    else
      check_argument "$2"
      run_openehrtool "$2"
    fi

    echo -e "\nExit dh.sh"
    exit 0
fi

run_node-ui(){
    docker compose build federation-api $1-node-ui
    docker compose up -d $1-node-ui
    echo -e "\nNode userinterface on $1 node up and running"
}

if [[ $1 == "node-ui" ]]; then
    if [[ -z "$2" ]]; then
       echo -e "Missing node name"
       exit 1
    else
      check_argument "$2"
      run_node-ui "$2"
    fi

    echo -e "\nExit dh.sh"
    exit 0
fi



run_single_node_tests(){
    dev_setup_requirements "test"
    if is_local; then build_and_up_common_services; fi

    echo -e "\nStart single node tests on test-etl-zib"
    docker compose build test-etl-zib
    docker compose run --rm --entrypoint pytest test-etl-zib --verbose --verbosity=5
#    docker compose run --rm --entrypoint pytest test-etl-zib -s
#    docker compose run --rm --entrypoint pytest test-etl-zib -o log_cli=true --log-cli-level=INFO
}

run_federation_tests(){
    dev_setup_requirements "mumc"
    dev_setup_requirements "zio"
    dev_setup_requirements "envida"
    if is_local; then build_and_up_common_services; fi
    echo -e "\nStart federation tests"
    docker compose run --build --rm --entrypoint pytest federation-api -s --verbose --verbosity=5
}

if [[ $1 == "test" ]]; then
    if [[ $2 == "single-node" ]]; then
        run_single_node_tests
    elif [[ $2 == "federation" ]]; then
        run_federation_tests
    fi

    if [ $? -eq 0 ]; then
      echo -e "\nExit dh.sh"
      exit 0
    else
      echo -e "\nFailed to run $2 tests"
      exit 1
    fi
fi


docker compose $ARGS
