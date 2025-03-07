# Docker Health - Local Development with Minikube

This directory contains Kubernetes manifests for deploying Docker Health services to a local Minikube environment. This setup allows developers to test the complete stack without requiring external resources.

# Prerequisites
 - docker
 - kubectl
 - minikube

## Quick Start

Follow these steps to deploy the Docker Health stack in your local Minikube:

### 1. Start Minikube

```bash
minikube start --cpus 4 --memory 8192 --disk-size=30g --driver=docker
```

### 2. Enable the Ingress Controller

```bash
minikube addons enable ingress
```

### 3. Set up Local DNS Entries

Add the following entries to your `/etc/hosts` file:

```bash
MINIKUBE_IP=$(minikube ip)
echo "$MINIKUBE_IP transform.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP federation.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP jupyter.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
```

### 4. Point to Minikube's Docker Daemon && set RIT_ENV

```bash
eval $(minikube docker-env)
export RIT_ENV=local
```

### 5. Build Docker Images

```bash
# From project root
docker-compose build
```

### 6. Deploy to Minikube

```bash
kubectl apply -k deploy/overlays/local
```

## Configuration Details

The local overlay applies the following customizations:

1. Sets `RIT_ENV` to `local`
2. Uses `latest` tag for all images
3. Sets empty registry host (using images built directly in Minikube)
4. Sets `imagePullPolicy: Never` to use locally built images

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

Once deployed, you can access the services at:
- Transform REST: http://transform.local.dh.unimaas.nl
- Federation API: http://federation.local.dh.unimaas.nl
- Jupyter ZIB: http://jupyter.local.dh.unimaas.nl

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