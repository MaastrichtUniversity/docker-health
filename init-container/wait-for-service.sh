#!/bin/sh
URL=$1
NAME=$2
N_ATTEMPTS=${3:-20}
SLEEP=${4:-10}

for i in $(seq 1 $N_ATTEMPTS); do
  echo "Waiting for $NAME..."
  if wget -qO- "$URL" | grep -q UP; then
    echo "$NAME is healthy!"
    exit 0
  fi
  sleep $SLEEP
done

echo "$NAME failed health check after $N_ATTEMPTS attempts"
exit 1