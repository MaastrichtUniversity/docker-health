# Define directories to mount
HEALTH_DIR=$(pwd)
DATA_DIR="$HEALTH_DIR/data"

# Define mount paths in Minikube
MINIKUBE_DATA_PATH="/mnt/data"

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
mount_directory "$DATA_DIR" "$MINIKUBE_DATA_PATH" "data"

# Verify ownership after mounting
echo "Verifying directory ownership..."
minikube ssh "ls -la /mnt"

echo
echo "Directories mounted successfully!"
echo
echo "Mount processes are running in the background. To stop them, run:"
echo "kill \$(cat /tmp/minikube-mount-data.pid)"