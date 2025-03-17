# Kubernetes Deployment for Docker Health Project

This project contains Kubernetes manifests for deploying various services defined in the Docker Compose configuration. The services include:

- **Transform REST**: A service that handles transformation requests.
- **Federation API**: A service that provides a federated API.
- **Filebeat**: A service for shipping logs to a central location.
- **Jupyter ZIB**: A Jupyter notebook service for data analysis and visualization.
- **Redis**: A caching service for fast data retrieval.

## Node-Specific Components

The Docker Health platform includes several node-specific components that represent different healthcare organizations:

- **MUMC Node**: Maastricht University Medical Center components
- **ZIO Node**: Zorg in Ontwikkeling components
- **Envida Node**: Envida healthcare organization components
- **Test Node**: Components for testing and development

Each node includes:
- EHRBase: OpenEHR clinical data repository
- EHR Database: PostgreSQL database for EHRBase
- ETL: Data extraction and transformation service
- OpenEHR Tool: Browser for OpenEHR data
- Portal: User interface for healthcare providers

### Accessing Node Portals

Once deployed, you can access the portals at:
- MUMC Portal: http://portal.mumc.{ENV}.dh.unimaas.nl
- ZIO Portal: http://portal.zio.{ENV}.dh.unimaas.nl
- Envida Portal: http://portal.envida.{ENV}.dh.unimaas.nl

## Directory Structure

- **base/**: Contains base Kubernetes resources for all environments
  - **namespace.yaml**: Defines the dh-health namespace
  - **kustomization.yaml**: Main kustomization file that references all resources
  - **common/**: Common resources shared across services
  - **transform-rest/**, **federation-api/**, etc.: Service-specific manifests
- **overlays/**: Environment-specific configurations
  - **tst/**: Development test environment customizations
  - **acc/**: Acceptance environment customizations
  - **prod/**: Production environment customizations
- **secrets/**: Contains guidelines for managing sensitive information
- **env_files/**: Environment variable files referenced by ConfigMap generators

## Architecture

- All services are deployed in the `dh-health` namespace
- Services are exposed via Nginx Ingress controller
- ConfigMaps are generated from environment files in the `env_files` directory
- Each service has its own deployment, service, and ingress resources
- Environment-specific configurations are maintained through Kustomize overlays
- Internal hostnames are formated `servicename.namespace` example "Redis server" hostname = redis.dh-health

## Environment Selection

In Kubernetes, environments are managed through Kustomize overlays:
- To deploy to a specific environment:
  ```bash
  kubectl apply -k deploy/overlays/tst    # For development environment
  kubectl apply -k deploy/overlays/prod   # For production environment
  ```

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
See for example `/deploy/base/redis`

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