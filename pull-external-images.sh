#!/bin/bash

set -e

# Make sure we're using Minikube's Docker daemon
if ! docker info 2>/dev/null | grep -q "minikube"; then
  echo "Error: Not connected to Minikube's Docker daemon!"
  echo "Please run: eval \$(minikube docker-env)"
  exit 1
fi

echo "Pulling external images into Minikube's Docker daemon..."

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

# Grafana
echo "Pulling Grafana.."
docker pull grafana/grafana:10.2.3

# Loki
echo "Pulling Loki.."
docker pull grafana/loki:2.9.2

# Loki
echo "Pulling Node-Exporter.."
docker pull prom/node-exporter:v1.9.1

echo "All external images have been pulled into Minikube's Docker daemon."
