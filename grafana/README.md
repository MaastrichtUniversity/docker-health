# How to run Grafana and Prometheus to monitor performance

## Deploy Grafana

Grafana is the interface that can visualise (similar to Kibana of ELK) the queries and uses Prometheus as source

```
# Make sure minikube is running
./dh.sh setup

# Apply the manifest
kubectl apply -f grafana/grafana.yaml

```

Grafana interface should now be available on http://grafana.local.dh.unimaas.nl

The username/password is admin/admin. It will prompt you to change it, but you can skip this step.

## Install Prometheus with Helm

Prometheus monitors, collects the metrics and stores them over time which then Grafana can use for visualization

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack -n performance --create-namespace
```
