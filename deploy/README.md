# Kubernetes Deployment

This repository includes Kubernetes manifests for deploying the federated network of CDRs.

## Folder Structure

```
deploy/
├── base                         # Contains base Kubernetes resources for all environments
│   ├── common                   # Common resources shared across services
│   ├──federation-rest           # federation-rest service
│   ├──transform-rest            # transform-rest service
│   ├── jupyter-zib              # jupyter-zib service
│   ├── openehr-nodes            # All existing openEHR node services
└── overlays                     # Environment-specific configurations
    ├── local                    # Local development environment
    ├── tst                      # Development test environment customizations
    ├── acc                      # Acceptance environment customizations
    ├── prod                     # Production environment customizations
    ├── test-federation          # Specific environment for running the federation tests
    └── test-single-node         # Specific environment for running the single-node tests
```

## Services

### Currently supported environments

- **local**
- **tst**
- <s>**acc**</s>
- <s>**prod**</s>
- **test-single-node**: Run a subset of the base
- **test-federation**: Run a subset of the base

### Currently supported nodes in the network

- **mumc**
- **zio**
- **envida**
- (**test**: Used for running single-node tests)

#### Each node includes the following components

- **ehrbase**: open-source openEHR backend
    - Hosts available at: http://ehrbase.{NODENAME}.{ENV}.dh.unimaas.nl
- **ehrdb**: PostgreSQL database linked to EHRBase
- **etl-zib**: Data extraction, transformation and loading service
    - Hosts available at: http://etl.{NODENAME}.{ENV}.dh.unimaas.nl
- **openehrtool**: Development tool for openEHR
    - Hosts available at: http://openehrtool.{NODENAME}.{ENV}.dh.unimaas.nl
- **portal**: User Interface of the federated network
    - Hosts available at: http://portal.{NODENAME}.{ENV}.dh.unimaas.nl

### Additional deployed services

- **transform-rest**: Performs transformation of data to openEHR composition via a REST api
    - Host available at: http://transform.{ENV}.dh.unimaas.nl
- **federation-rest**: Provides a federation REST api for querying data of multiple nodes
    - Host available at: http://federation.{ENV}.dh.unimaas.nl
- <s>**filebeat**: A service used for shipping logs to a central location</s>
- **jupyter-zib**: Jupyter notebook for data analysis and visualization
    - Host available at: http://jupyter.{ENV}.dh.unimaas.nl

### Notes on Kubernetes configurations

- All services are deployed in the `dh-health` namespace
- This setup uses the Minikube Docker daemon to avoid pushing images to a registry
- Services are exposed through Nginx Ingress controller with domain patterns:
  Each service has its own ingress configuration in its respective directory.
    - Ensure that your Kubernetes cluster has the Nginx Ingress Controller installed

- Each service has its own kustomization, deployment, service, ingress, etc. resources
- PersistentVolumeClaims require appropriate StorageClass configurations in your cluster
- Environment-specific configurations are maintained through Kustomize overlays
    - Sensitive information should be stored using a secretGenerator in each overlay
- Environment variables are configured via ConfigMap generators
- Internal hostnames are formated `servicename.namespace` example "Envida ehrbase server" hostname =
  envida-ehrbase.dh-health
- The `local` overlay applies the following customizations:
    - Sets empty registry host (using images built directly in Minikube)
    - Sets `imagePullPolicy: Never` to ensure Kubernetes uses locally built images
- To deploy a specific environment:
  ```bash
  kubectl apply -k deploy/overlays/tst    # For development
  kubectl apply -k deploy/overlays/prod   # For production
  ```

## Instructions for new code integration

### Adding a new template

Follow instructions
in [dh-hdp-etl/README.md](https://github.com/MaastrichtUniversity/dh-hdp-etl/tree/2024.1?tab=readme-ov-file#how-to-add-a-new-zib-template-in-the-codebase)

### Adding/Updating a Kubernetes resources

1. Update the base resources in `base/` directory
2. Create or update environment-specific patches in one of the `overlays/`
3. Update the appropriate `kustomization.yaml` file to include new resources

### Adding a new node

1. In `base/openehr-nodes`,
    1. Add a complete new node folder
       (After copy/pasting, make sure the name of the new node is updated in every file)
    2. Add the new resource folder name to `base/openehr-nodes/kustomization.yaml`
2. In the `kustomization.yaml` file of `overlay/local`, `tst`, etc.,
    1. If required, add the new resources
    2. Add new ingress patches
    3. Add new secretGenerators
3. Add new container environment variables to `base/federation-rest/deployment.yaml` and
   `overlay/test-federation/job.yaml`
4. Add the new local hosts to `localhost.sh`
5. In `dh-hdp-etl-utils`
    1. Add the new node name to `dhhdpetlutils/core/enums.py`
    2. Update the new version number in `pyproject.toml` and release a new tag
    3. Update the package version in the `requirements.txt` file in both `dh-hdp-etl` and `dh-hdp-federation-api`
6. Add a new demo-data folder in `data`
   1. Remember to update the new configuration in `base/openehr-nodes/{nodename}/etl-config/config.yaml`
7. In `dh-hdp-federation-api`
    1. Add a new `list` item into `SuccessQueryModel` in `src/response_models.py`
    2. Add a new `NodeCredentialsSettings` item into `CredentialsSettings` in `src/settings.py`
    3. In `test_federation_rest.py`
        1. Add new variable lists containing the expected results from the newly created demo-data
        2. Add new `TestClient` and `TestBtgClient` test classes,
