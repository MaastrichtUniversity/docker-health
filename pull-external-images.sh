#!/bin/bash

set -e

# Make sure we're using Minikube's Docker daemon
if ! docker info 2>/dev/null | grep -q "minikube"; then
  echo "Error: Not connected to Minikube's Docker daemon!"
  echo "Please run: eval \$(minikube docker-env)"
  exit 1
fi

echo "Pulling external images into Minikube's Docker daemon..."

# Redis
echo "Pulling Redis image..."
docker pull redis:latest

# EHRBase images
echo "Pulling EHRBase image..."
docker pull ehrbase/ehrbase:2.6.0

# EHRBase Postgres image
echo "Pulling EHRBase Postgres image..."
docker pull ehrbase/ehrbase-v2-postgres:16.2

# OpenEHRTool image
echo "Pulling OpenEHRTool image..."
docker pull surfercrs4/openehrtool:latest

# BusyBox for ETL initContainer
echo "Pulling busybox:1.28..."
docker pull  busybox:1.28

echo "All external images have been pulled into Minikube's Docker daemon."