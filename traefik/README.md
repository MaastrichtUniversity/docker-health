# Traefik/Gateway-api in minikube

# How to install Helm

https://helm.sh/docs/intro/install

## For Ubuntu

### Via APT

```
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

### Via Snap

```
sudo snap install helm --classic
```

### Verify installation

```
helm version
```

# How to install Traefik

https://doc.traefik.io/traefik/getting-started/install-traefik/#use-the-helm-chart

Make sure your minikube cluster is running

```
./dh.sh setup

cd traefik

# Install Gateway API
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.5.1/standard-install.yaml

# Install traefik
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik --namespace traefik --create-namespace --values values.yaml

# In your browser go to
http://traefik.dashboard.local.dh.unimaas.nl/dashboard/
```

# Troubleshooting

Clean-up

```
helm uninstall traefik -n traefik
kubectl delete ns traefik
```

Update the configuration

```
helm upgrade traefik traefik/traefik --namespace traefik --values values.yaml
kubectl rollout restart deploy/traefik -n traefik
```

### Port conflict between Ingress vs Traefik

If you see the following error when setting up, either disable Ingress addon or remove Traefik service

```
0/1 nodes are available: 1 node(s) didn't have free ports for the requested pod ports. preemption: 0/1 nodes are available: 1 No preemption victims found for incoming pod.
```
