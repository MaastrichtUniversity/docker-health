# How to run Grafana and Prometheus to monitor performance

## Deploy Grafana

Grafana is the interface that can visualize (similar to Kibana of ELK) the queries and uses Prometheus as source

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

helm install monitoring prometheus-community/kube-prometheus-stack -n performance
```

If you want to verify that Prometheus is working or test your queries straight in Prometheus , forward the port

`kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n performance`

Now you can access Prometheus on http://localhost:9090/query

## Create dashboard in Grafana manually

### Configure the connetion between Grafana and Prometheus

1. Add Prometheus as a data source http://grafana.local.dh.unimaas.nl/connections/datasources/new
2. Configure server URL http://monitoring-kube-prometheus-prometheus:9090
3. Save and test the connection

### Create a panel

1. http://grafana.local.dh.unimaas.nl/dashboards
2. Create new dashboard -> Edit -> Panel -> Configure visualization
3. Here you define your metrics and queries . Select Prometheus as a data source. Then either build a query by selecting some metrics in "Builder" or use "Code" where you can enter a PromQL query
4. Query - CPU per pod over time

```
sum by (pod) (rate(container_cpu_usage_seconds_total{namespace="dh-health"}[5m]))
```

5. Query - memory usage per pod

```
sum by (pod) (
  container_memory_working_set_bytes{namespace="dh-health"}
)
```

6. Save and you should now be able to see some graphs!

### Alternative option

You can also import a pre-made dashboard, for example, https://grafana.com/grafana/dashboards/10219-dash/ by downloading the JSON file and importing in Dashboards -> New -> Import. However, you still might need to configure/edit the queries to make it work
