# Kubernetes Deployment

This repository includes Kubernetes manifests for deploying the federated network of CDRs.

## Services

Currently supported nodes in the network:

- **mumc**
- **zio**
- **envida**
- **test**

Each node includes the following components:

- **ehrbase**: open-source openEHR backend
  - Hosts available at: http://ehrbase.{NODENAME}.{ENV}.dh.unimaas.nl
- **ehrdb**: PostgreSQL database linked to EHRBase
- **etl-zib**: Data extraction, transformation and loading service
  - Hosts available at: http://etl.{NODENAME}.{ENV}.dh.unimaas.nl
- **openehrtool**: Development tool for openEHR
  - Hosts available at: http://openehrtool.{NODENAME}.{ENV}.dh.unimaas.nl
- **portal**: User Interface of the federated network
  - Hosts available at: http://portal.{NODENAME}.{ENV}.dh.unimaas.nl

Additional deployed services:

- **transform-rest**: Performs transformation of data to openEHR composition via a REST api
  - Host available at: http://transform.{ENV}.dh.unimaas.nl
- **federation-api**: Provides a federation API for querying data of multiple nodes
  - Host available at: http://federation.{ENV}.dh.unimaas.nl
- **etl-rest**: Permits the loading of data via a REST api
- **filebeat**: A service used for shipping logs to a central location
- **jupyter-zib**: Jupyter notebook for data analysis and visualization
  - Host available at: http://jupyter.{ENV}.dh.unimaas.nl

## Directory Structure

- **base/**: Contains base Kubernetes resources for all environments
  - **namespace.yaml**: Defines the dh-health namespace
  - **kustomization.yaml**: Main kustomization file that references all resources
  - **env_files/**: Environment variable files referenced by ConfigMap generators
  - **common/**: Common resources shared across services
  - **transform-rest/**, **federation-api/**, etc.: Service-specific manifests
- **overlays/**: Environment-specific configurations
  - **local/**: Local development environment
  - **tst/**: Development test environment customizations
  - **acc/**: Acceptance environment customizations
  - **prod/**: Production environment customizations
- (**secrets/**: Contains guidelines for managing sensitive information)

### Notes

- All services are deployed in the `dh-health` namespace
- Services are exposed via Nginx Ingress controller
- ConfigMaps are generated from environment files in the `env_files` directory
- Each service has its own deployment, service, and ingress resources
- Environment-specific configurations are maintained through Kustomize overlays
- Internal hostnames are formated `servicename.namespace` example "Envida ehrbase server" hostname = envida-ehrbase.dh-health
- To deploy to a specific environment:
  ```bash
  kubectl apply -k deploy/overlays/tst    # For development environment
  kubectl apply -k deploy/overlays/prod   # For production environment
  ```

## Instructions for new code integration

### Adding a new template

Follow instructions in [dh-hdp-etl/README.md](https://github.com/MaastrichtUniversity/dh-hdp-etl/tree/2024.1?tab=readme-ov-file#how-to-add-a-new-zib-template-in-the-codebase)

### Adding a new service

TODO

### Adding a new node

TODO

## Usage

### Deploying Services

Use Kustomize to deploy all services:

```bash
# Deploy local environment
kubectl apply -k deploy/overlays/local

# Deploy acceptance environment
kubectl apply -k deploy/overlays/acc

# Deploy production environment
kubectl apply -k deploy/overlays/prod
```

### Managing Secrets

Sensitive information should be stored as Kubernetes Secrets:

```bash
# Create a secret from literal values
kubectl create secret generic my-secret -n dh-health --from-literal=key=value

# Create a secret from files
kubectl create secret generic my-secret -n dh-health --from-file=./path/to/file

# Reference secrets in deployment files
```

### Environment Configuration

The application uses different configurations for different environments:

1. Environment variables are stored in `/deploy/base/env_files/` and loaded via ConfigMap generators

To add or modify environment variables:

1. Update the appropriate file in `/deploy/base/env_files/`
2. Add this as configMap to `/deploy/base/kustomization.yaml`

### Service Configuration

Some services are using specific .env or .conf files. These are handled with the service structure

### Modifying Resources

To add or modify Kubernetes resources:

1. Update the base resources in `base/` directory
2. Create or update environment-specific patches in `overlays/dev/` or `overlays/prod/`
3. Update the appropriate `kustomization.yaml` file to include new resources

## Ingress Configuration

Services are exposed through Nginx Ingress controller with domain patterns:
Each service has its own ingress configuration in its respective directory.

## Notes

- Ensure that your Kubernetes cluster has the Nginx Ingress Controller installed
- PersistentVolumeClaims require appropriate StorageClass configurations in your cluster
- Environment variables are loaded from ConfigMaps generated from files in `env_files/`
