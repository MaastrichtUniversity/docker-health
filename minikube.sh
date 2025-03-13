#!/usr/bin/env bash

set -e

# Check if Minikube is running
if ! minikube status | grep -q "Running"; then
    echo "Minikube is not running. Starting Minikube..."
    minikube start --cpus 4 --memory 8192 --disk-size=30g --driver=docker
fi

# Enable Minikube Ingress
echo "Enable Ingress"
minikube addons enable ingress
minikube addons enable ingress-dns

# Create log folders
echo -e "Create sub folders for filebeat/logs/"
mkdir -p ./outputs/etl-zib
mkdir -p ./filebeat/logs/envida/ehrbase ./filebeat/logs/envida/ehrdb ./filebeat/logs/envida/etl-zib
mkdir -p ./filebeat/logs/zio/ehrbase ./filebeat/logs/zio/ehrdb ./filebeat/logs/zio/etl-zib
mkdir -p ./filebeat/logs/test/ehrbase ./filebeat/logs/test/ehrdb ./filebeat/logs/test/etl-zib
mkdir -p ./filebeat/logs/mumc/ehrbase ./filebeat/logs/mumc/ehrdb ./filebeat/logs/mumc/etl-zib
mkdir -p ./filebeat/logs/federation-api
mkdir -p ./filebeat/logs/transform-rest

# Already creating the log files
touch ./filebeat/logs/envida/ehrdb/postgresql.log
touch ./filebeat/logs/zio/ehrdb/postgresql.log
touch ./filebeat/logs/test/ehrdb/postgresql.log
touch ./filebeat/logs/mumc/ehrdb/postgresql.log
touch ./filebeat/logs/envida/ehrbase/ehrbase.log
touch ./filebeat/logs/zio/ehrbase/ehrbase.log
touch ./filebeat/logs/test/ehrbase/ehrbase.log
touch ./filebeat/logs/mumc/ehrbase/ehrbase.log
touch ./filebeat/logs/test/etl-zib/etl-zib.log
touch ./filebeat/logs/mumc/etl-zib/etl-zib.log
touch ./filebeat/logs/envida/etl-zib/etl-zib.log
touch ./filebeat/logs/zio/etl-zib/etl-zib.log

# Set explicit permissions on these directories
chmod -R 755 ./filebeat
chmod -R 755 ./outputs

# Define directories to mount
HEALTH_DIR=$(pwd)
EXTERNALS_DIR="$HEALTH_DIR/externals"
DATA_DIR="$HEALTH_DIR/data"
LOG_DIR="$HEALTH_DIR/filebeat"
OUTPUT_DIR="$HEALTH_DIR/outputs"

# Define mount paths in Minikube
MINIKUBE_EXTERNALS_PATH="/externals"
MINIKUBE_DATA_PATH="/data"
MINIKUBE_LOG_PATH="/filebeat"
MINIKUBE_OUTPUT_PATH="/outputs"

# Create mount directories in Minikube
echo "Creating mount directories in Minikube..."
minikube ssh "sudo mkdir -p $MINIKUBE_EXTERNALS_PATH $MINIKUBE_DATA_PATH $MINIKUBE_LOG_PATH $MINIKUBE_OUTPUT_PATH"

# Function to mount a directory
mount_directory() {
    local host_dir=$1
    local minikube_path=$2
    local mount_name=$3

    echo "Mounting $mount_name directory..."
    
    # Check if the mount is already active
    if minikube ssh "mount | grep -q '$minikube_path'"; then
        echo "$mount_name is already mounted. Unmounting first..."
        minikube ssh "sudo umount $minikube_path" || true
    fi
    
    # Start the mount in the background
    nohup minikube mount "$host_dir:$minikube_path" > /tmp/minikube-mount-$mount_name.log 2>&1 &
    MOUNT_PID=$!
    
    # Save the PID for later
    echo $MOUNT_PID > /tmp/minikube-mount-$mount_name.pid
    
    # Wait a moment to ensure the mount starts
    sleep 2
    
    # Verify the mount is working
    if minikube ssh "mount | grep -q '$minikube_path'"; then
        echo "$mount_name directory mounted successfully at $minikube_path"
    else
        echo "Failed to mount $mount_name directory. Check /tmp/minikube-mount-$mount_name.log for details."
        exit 1
    fi
}

# Mount the directories
echo "Mounting directories..."
mount_directory "$EXTERNALS_DIR" "$MINIKUBE_EXTERNALS_PATH" "externals"
mount_directory "$DATA_DIR" "$MINIKUBE_DATA_PATH" "data"
mount_directory "$LOG_DIR" "$MINIKUBE_LOG_PATH" "filebeat"
mount_directory "$OUTPUT_DIR" "$MINIKUBE_OUTPUT_PATH" "outputs"

# Verify ownership after mounting
echo "Verifying directory ownership..."
minikube ssh "ls -la /health"

echo
echo "Directories mounted successfully!"
echo
echo "Mount processes are running in the background. To stop them, run:"
echo "kill \$(cat /tmp/minikube-mount-externals.pid) \$(cat /tmp/minikube-mount-data.pid) \$(cat /tmp/minikube-mount-filebeat.pid) \$(cat /tmp/minikube-mount-output.pid)"