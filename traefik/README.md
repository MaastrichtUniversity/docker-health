# Traefik/Gateway-api in minikube

# How to install Helm

https://helm.sh/docs/intro/install


```
sudo apt-get install helm
# or
sudo snap install helm --classic
```

# How to install Traefik

https://doc.traefik.io/traefik/getting-started/install-traefik/#use-the-helm-chart

Make sure your minikube cluster is running

```
./dh.sh setup

cd traefik

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
