# Health Data Platform

## Project Overview

This project builds a federated network of Clinical Data Repositories (CDRs) using the [EHRbase](https://ehrbase.org/about-ehrbase/), an open-source electronic health record (EHR) backend.
It follows the [openEHR standard](https://specifications.openehr.org/) to support interoperable sharing and querying of clinical data across multiple systems.
Templates are based on the Dutch Healthcare Information Building Blocks ([ZIBs](https://zibs.nl/wiki/HCIM_Mainpage)), ensuring consistent and structured health information.

Each node in the federated network represents a Dutch health organization. The currently supported nodes are:

- **MUMC**: Maastricht University Medical Center (hospital)
- **ZIO**: Zorg in Ontwikkeling (general practitioners)
- **ENVIDA**: Envida healthcare organization
- (**TEST**: Separate node used for testing)

The implementation relies on the following services:

- [dh-hdp-zib-templates](https://github.com/um-datahub/dh-hdp-zib-templates/tree/2024.1): OpenEHR templates matching the ZIBs
- [dh-hdp-transform-rest](https://github.com/MaastrichtUniversity/dh-hdp-transform-rest/tree/2024.1): REST API for data class transformation into openEHR compositions
- [dh-hdp-etl](https://github.com/MaastrichtUniversity/dh-hdp-etl/tree/2024.1): ETL workflow for loading data into a CDR
- [dh-hdp-federation-api](https://github.com/MaastrichtUniversity/dh-hdp-federation-api/tree/2024.1): Federation service for querying across multiple CDRs
- [dh-hdp-etl-utils](https://github.com/MaastrichtUniversity/dh-hdp-etl-utils): A package to share ETL utils classes and functions between different code bases
- [dh-hdp-portal](https://github.com/MaastrichtUniversity/dh-hdp-portal/tree/2024.1): Node User Interface service
- [dh-hdp-notebooks](https://github.com/MaastrichtUniversity/dh-hdp-notebooks/tree/2024.1): Jupyter notebooks for data exploration

## Pre-requisites

### Install the following services on your local machine

- docker
- kubectl
- minikube

> ### Encryption between filebeat and elk [UNUSED ATM!]
>
> CA certificates need to be manually stored in folder `filebeat/certs`.
> The present files are used for development-purposes.
> Right now, we're not using encryption, but we've kept these configurations in case we decide to enable them in the future, hence the commented configurations, for example:
>
> In `docker-compose.yml` :
>
> ```
> #   - ./filebeat/certs:/etc/certs:ro
> ```
>
> In `filebeat/filebeat.yml` :
>
> ```
> #  ssl.certificate_authorities: ["/etc/certs/ca.crt"]
> #  ssl.certificate: "/etc/certs/filebeat.dh.local.crt"
> #  ssl.key: "/etc/certs/filebeat.dh.local.key"
> ```
>
> and others.
>
> If encryption needs to be restored, uncomment the configurations and see `2025.1-ssl` branch of `docker-common`.

## Quick start installation with Minikube

The services are deployed to a local Minikube environment using Kubernetes manifests.

Check out `deploy/README.md` for more information.

1. Setup the Kubernetes cluster and folders

```bash
./dh.sh setup
```

This will start minikube with all needed addons, pull down the external repos, add log folders to filebeat and set hostnames in /etc/hosts with the minikube ip.

2. Pull default docker images from Dockerhub

```bash
./dh.sh pull
```

3. Build the docker images from externals

```bash
./dh.sh build
```

3a. The script supports build with custom tag, but not needed for local development, see next example

```bash
./dh.sh build transform-rest 2.0.0
```

4. Apply Kubernetes manifests with local overlay

```bash
./dh.sh apply
```

5. Show status of all pods

```bash
./dh.sh status
```

### 6. For a UI overview of the Minikube kubernetes stack and pods with logs checkout Headlamp or Freelens

- Headlamp: https://headlamp.dev/

https://github.com/freelensapp/freelens

Or you can enable the default dashboard with

## Manual steps

Follow these manual steps to deploy the stack in your local Minikube manually:

1. Start Minikube

```bash
minikube start --cpus 4 --memory 8192 --disk-size=30g --driver=docker
```

2. Enable the Ingress Controller

```bash
minikube addons enable ingress
```

3. Set up Local DNS Entries

Add the local hostname entries to your `/etc/hosts` file:

```bash
./localhost.sh
```

4. Point to Minikube's Docker Daemon && set docker build vars

```bash
eval $(minikube -p minukube docker-env)
export ENV_TAG=latest
export MAVEN_VERSION=3.9.5
```

4a. Pull external images into Minikube's Docker daemon

Some components use external images from Docker Hub. Pull them into Minikube's Docker daemon:

```bash
# Pull external images
./pull-external-images.sh
```

5. Build Docker Images

```bash
# From project root
docker buildx bake
```

6. Deploy to Minikube

```bash
kubectl create namespace dh-health
```

```bash
kubectl apply -k deploy/overlays/local
```

**Note: Configuration Details**

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

### Running tests

To run tests on single node:

```bash
# Clean up exsisting overlay
kubectl delete -k deploy/overlays/local

# Run the test job
kubectl apply -k deploy/overlays/test-single-node

# Manually clean up the containers
kubectl delete -k deploy/overlays/test-single-node
```

To run tests on federation:

#TODO

### Viewing Logs

```bash
# View logs for a specific deployment
kubectl logs -l app=transform-rest -n dh-health
```

#### Log files

Some log files are still saved in a volumeclaim inside the kubernetes cluster.
You can access them from the terminal:

```bash
minikube ssh
cd /usr/share/logs
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

#### Troubleshooting MacOS specifically

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
