# Set the prefix for the project
COMPOSE_PROJECT_NAME="hdp"
export COMPOSE_PROJECT_NAME

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
    sleep 5
    echo "Print logs for etl-demo"
    docker compose logs etl-demo

    echo "Exit rit.sh"
    exit 0
fi
