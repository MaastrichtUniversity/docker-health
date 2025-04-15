# Docker Health - Local Development with Minikube

This directory contains Kubernetes manifests for deploying Docker Health services to a local Minikube environment. This setup allows developers to test the complete stack without requiring external resources.

# Prerequisites

### These services need to be installed on your machine
 - docker
 - kubectl or use this alias in your bashrc `alias kubectl="minikube kubectl --"`
 - minikube

## Quick Start

I've tried to keep the process as easy as it was with dh.sh script

### 1. Setup the Kubernetes cluster and folders

```bash
./dh.sh setup
```
This will start minikube with all needed addons, pull down the external repos, add log folders to filebeat and set hostnames in /etc/hosts with the minikube ip.

### 2. Pull default docker images from Dockerhub

```bash
./dh.sh pull
```

### 3. Build the docker images from externals

```bash
./dh.sh build
```

#### 3a The script supports build with custom tag, but not needed for local development, see next example

```bash
./dh.sh build transform-rest 2.0.0
```

### 4. Apply Kubernetes manifests with local overlay

```bash
./dh.sh apply
```

### 5. Show status of all pods

```bash
./dh.sh status
```

### 6. For a UI overview of the Minikube kubernetes stack and pods with logs checkout Headlamp

https://headlamp.dev/

Or you can enable the default dashboard with

```bash
minikube dashboard
```

## Manual steps

Follow these manual steps to deploy the Docker Health stack in your local Minikube manually:

### 1. Start Minikube

```bash
minikube start --cpus 4 --memory 8192 --disk-size=30g --driver=docker
```

### 2. Enable the Ingress Controller

```bash
minikube addons enable ingress
```

### 3. Set up Local DNS Entries

Add the local hostname entries to your `/etc/hosts` file:

```bash
./localhost.sh
```


### 4. Point to Minikube's Docker Daemon && set docker build vars

```bash
eval $(minikube -p minukube docker-env)
export ENV_TAG=latest
export MAVEN_VERSION=3.9.5
```

### 4a. Pull external images into Minikube's Docker daemon

Some components use external images from Docker Hub. Pull them into Minikube's Docker daemon:

```bash
# Pull external images
./pull-external-images.sh
```

### 5. Build Docker Images

```bash
# From project root
docker buildx bake
```

### 6. Deploy to Minikube

```bash
kubectl create namespace dh-health
```

```bash
kubectl apply -k deploy/overlays/local
```

## Configuration Details

The local overlay applies the following customizations:

1. Sets empty registry host (using images built directly in Minikube)
2. Sets `imagePullPolicy: Never` to use locally built images

## Development Workflow

### Rebuilding and Updating Services

After making code changes:

```bash
# Ensure you're using Minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild specific service or all services
docker-compose build [service_name]

# Restart the deployment to pick up new image
kubectl rollout restart deployment [service_name] -n dh-health
```

### Accessing Services

Once deployed, you can access the services at their local dns name

### Viewing Logs

```bash
# View logs for a specific deployment
kubectl logs -l app=transform-rest -n dh-health
```

### Troubleshooting

#### Images Not Found
If you see `ImagePullBackOff` errors, ensure you've built the images with Minikube's Docker daemon:

```bash
eval $(minikube docker-env)
docker-compose build
kubectl rollout restart deployment -n dh-health
```

#### Storage Issues
For persistent storage issues:

```bash
# Ensure storage provisioner is enabled
minikube addons enable storage-provisioner

# Check PVC status
kubectl get pvc -n dh-health
```

#### Ingress Not Working
Check if the ingress controller is properly installed:

```bash
kubectl get pods -n ingress-nginx
```


### Troubleshooting MacOS specifically

Kubernetes on MacOS is less straight forward unfortunately. While trying to run Kubernetes, you may run into the following issues:

1. Errors while trying to run `minikube start`. This seems to be due to Minikube defaulting to the `None` driver on MacOS, which is not supported on Darwin(OS)/arm64. This can be fixed by specifying the driver for Minikube to use:

```bash
# minikube needs to be running to check its profiles
minikube start
# check which driver you should use, e.g. docker
minikube profile list
minikube delete; minikube start --driver=docker
```

2. The `sed` command, used in checking for- and deleting duplicates related to specific virtual hosts in `/etc/hosts`, may not initially be recognised on MacOS. Install it manually through Homebrew via [gnu-sed](https://formulae.brew.sh/formula/gnu-sed). Be sure to add a "gnubin" directory to your PATH from your bashrc/zshrc (on newer macs) to allow for use of the 'sed' command instead of their default 'gsed':

```
# allows for use of 'sed' instead of 'gsed'; HOMEBREW_PREFIX is the location of your homebrew (`which brew`)
PATH="$HOMEBREW_PREFIX/opt/gnu-sed/libexec/gnubin:$PATH"
``` 

Restart the terminal for the change to take effect:

```bash
source ~/.zshrc
```


3. Minikube seemingly being starved of resources. This problem in particular could present itself when trying to start the `ehrdb` and `ehrbase` pods, where the pods continuously timeout and restart. Using the following does not work on MacOS:

```bash
minikube start --cpus 4 --memory 8192 --disk-size=30g --driver=docker
```
Instead, specify the allocated resources through the minikube config file with the number of cpus and amount of memory you require. Good practise is to leave some breathing room for your OS, so do not max the amount of cpus and memory based on your specific system specs:
```bash
minikube config set cpus 4 # specify number of cpus you require
minikube config set memory 8192 # specify amount of memory you require
```
These changes take effect after restarting minikube and should persist across sessions.


4. By default, the Minikube ip (through `minikube ip`) will be used and added to the virtual hosts in `/etc/hosts`. However, using the Minikube ip does not work for this purpose on MacOS. Instead, use `127.0.0.1` and add these to `/etc/hosts` manually:
```
# these can replace the minikube ips
127.0.0.1 ehrbase.envida.local.dh.unimaas.nl
127.0.0.1 ehrbase.mumc.local.dh.unimaas.nl
127.0.0.1 ehrbase.test.local.dh.unimaas.nl
127.0.0.1 ehrbase.zio.local.dh.unimaas.nl
127.0.0.1 federation.local.dh.unimaas.nl
127.0.0.1 jupyter.local.dh.unimaas.nl
127.0.0.1 openehrtool.envida.local.dh.unimaas.nl
127.0.0.1 openehrtool.mumc.local.dh.unimaas.nl
127.0.0.1 openehrtool.test.local.dh.unimaas.nl
127.0.0.1 openehrtool.zio.local.dh.unimaas.nl
127.0.0.1 portal.envida.local.dh.unimaas.nl
127.0.0.1 portal.mumc.local.dh.unimaas.nl
127.0.0.1 portal.zio.local.dh.unimaas.nl
127.0.0.1 transform.local.dh.unimaas.nl
```

5. There is an issue regarding the ingress and ingress-dns addons on MacOS. In order to work around this, use `minikube tunnel`. This tunnel creates a route to services deployed with the LoadBalancer type and sets their Ingress to their ClusterIPs. Use a different terminal for this because it has to stay open:
```bash
# in a different terminal; sudo is required
sudo minikube tunnel
```

After all that, the following seems to work:
```bash
minikube start --driver=docker
minikube addons enable ingress
./dh.sh setup
./dh.sh pull
./dh.sh build
# in a different terminal; sudo is required
sudo minikube tunnel
./dh.sh apply
```

## Cleaning Up

To remove all resources created by this overlay:

```bash
kubectl delete -k deploy/overlays/local
```

To stop Minikube:

```bash
minikube stop
```

## Notes

- This setup uses the Minikube Docker daemon to avoid pushing images to a registry
- The `imagePullPolicy: Never` setting ensures Kubernetes uses locally built images
- Environment variables are configured via ConfigMap generators