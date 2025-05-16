# Health Data Platform

## Project Overview

This project builds a federated network of Clinical Data Repositories (CDRs) using
the [EHRbase](https://ehrbase.org/about-ehrbase/), an open-source electronic health record (EHR) backend.
It follows the [openEHR standard](https://specifications.openehr.org/) to support interoperable sharing and querying of
clinical data across multiple systems.
Templates are based on the Dutch Healthcare Information Building Blocks ([ZIBs](https://zibs.nl/wiki/HCIM_Mainpage)),
ensuring consistent and structured health information.

Each node in the federated network represents a Dutch health organization. The currently supported nodes are:

- **MUMC**: Maastricht University Medical Center (hospital)
- **ZIO**: Zorg in Ontwikkeling (general practitioners)
- **ENVIDA**: Envida healthcare organization
- (**TEST**: Separate node used for testing)

The implementation relies on the following repositories:

- [dh-hdp-zib-templates](https://github.com/um-datahub/dh-hdp-zib-templates/tree/2024.1): OpenEHR templates matching the
  ZIBs
- [dh-hdp-etl](https://github.com/MaastrichtUniversity/dh-hdp-etl/tree/2024.1): ETL workflow for loading data into a CDR
- [dh-hdp-etl-utils](https://github.com/MaastrichtUniversity/dh-hdp-etl-utils): A package to share ETL utils classes and
  functions between different code bases
- [dh-hdp-transform-rest](https://github.com/MaastrichtUniversity/dh-hdp-transform-rest/tree/2024.1): REST api for data
  class transformation into openEHR compositions
- [dh-hdp-federation-api](https://github.com/MaastrichtUniversity/dh-hdp-federation-api/tree/2024.1): REST api service
  for querying across a federation of CDRs
- [dh-hdp-portal](https://github.com/MaastrichtUniversity/dh-hdp-portal/tree/2024.1): Node User Interface service
- [dh-hdp-notebooks](https://github.com/MaastrichtUniversity/dh-hdp-notebooks/tree/2024.1): Jupyter notebooks for data
  exploration

## Pre-requisites

### Install the following tools on your local machine

- docker
- kubectl
- minikube

> ### Encryption between filebeat and elk [UNUSED ATM!]
>
> CA certificates need to be manually stored in folder `filebeat/certs`.
> The present files are used for development-purposes.
>
> Right now, we're not using encryption, but we've kept these configurations in case we decide to enable them in the
> future, hence the commented configurations, for example:
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

## Quick start installation of the HDP local env

Deployment of the services to a Minikube environment using Kubernetes manifests.

Check out [deploy/README.md](https://github.com/MaastrichtUniversity/docker-health/tree/2024.1/deploy#kubernetes-deployment)
for more information on the Kubernetes architecture and deployed services.

1. Setup the Kubernetes cluster and folders

```bash
./dh.sh setup
```

This will start Minikube with all needed addons, pull down the external repos, add log folders to the Minikube machine
and set hostnames in /etc/hosts with the Minikube ip.

2. Pull default docker images from Dockerhub

```bash
./dh.sh pull
```

3. Build the docker images from externals

```bash
./dh.sh build
```

Note: Build with a custom tag is supported (not needed for local development).

```bash
./dh.sh build transform-rest 2.0.0
```

4. Apply Kubernetes manifests on the `local` overlay

```bash
./dh.sh apply
```

5. Show status of all pods

```bash
./dh.sh status
```

For a UI overview of the Minikube kubernetes stack and pods with logs checkout one of the following dashboard:

- Headlamp: https://headlamp.dev/

- Freelens: https://github.com/freelensapp/freelens

- Enable the default dashboard with `minikube dashboard`

## Development Workflow

### dh.sh functionalities

Checkout existing functionality in the dh.sh. For examples:

```bash
./dh.sh setup               Setup Kubernetes environment
./dh.sh start               Start Kubernetes environment
./dh.sh build               Build all Docker images
./dh.sh apply               Apply Kubernetes manifests with local overlay
./dh.sh apply tst           Apply Kubernetes manifests with tst overlay
./dh.sh delete              Delete Kubernetes manifests with local overlay
./dh.sh delete tst          Delete Kubernetes manifests with tst overlay
./dh.sh status              Print the pods status
./dh.sh status -w           Print and follow the pods status
./dh.sh rollout             Rollout a restart of all the deployments
./dh.sh rollout jupyter-zib Rollout a restart of the jupyter-zib deployment
./dh.sh up test-node        Apply Kubernetes manifests with local overlay & the label test-node
./dh.sh up others           Apply Kubernetes manifests with local overlay & without the labels test-node
./dh.sh down test-node      Delete Kubernetes manifests with local overlay & the label test-node
./dh.sh down others         Delete Kubernetes manifests with local overlay & without the labels test-node
```

### Rebuilding and Updating Services

After making code changes:

```bash
# Ensure you're using Minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild specific service or all services
docker-compose build [service_name]

# Restart the deployment to pick up new image
./dh.sh rollout [service_name]
```

### Accessing Services

Once deployed, you can access the services at their local dns name.

### Running tests

Pre-requirement: Clean up existing overlays.

To run tests on single node:

```bash
# 1. Run the test job
./dh.sh apply test-single-node

# 2. Check the logs of test-single-node pod to see the result

# 3. Manually clean up the containers
./dh.sh delete test-single-node
```

To run tests on federation:

```bash
# 1. Run the test job
./dh.sh apply test-federation

# 2. Check the logs of test-federation pod to see the result

# 3. Manually clean up the containers
./dh.sh delete test-federation
```

### Viewing Logs

To view logs for a specific deployment, checkout a Kubernetes dashboard or run the following command:

```bash
kubectl logs -l app=transform-rest -n dh-health
```

#### Log files

Some log files are still saved in a volumeclaim inside the kubernetes cluster.
You can access them from the terminal:

```bash
minikube ssh
cd /usr/share/logs
```

### Stop minikube

```bash
minikube stop
```

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
./pull-external-images.sh
```

5. Build Docker Images

```bash
docker buildx bake
```

6. Deploy to Minikube

```bash
kubectl create namespace dh-health
```

```bash
kubectl apply -k deploy/overlays/local
```
