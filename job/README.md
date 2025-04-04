# How to run the integration tests

```
kubectl apply -k job/test-node
```


# How to check the tests logs

```
kubectl logs -f -l app=test-etl-zib-job -n dh-health
```

Need to ask for the logs after 1 minute/the init, other you get this error:
```
Error from server (BadRequest): container "test-etl-zib-job" in pod "test-etl-zib-job-k6swp" is waiting to start: PodInitializing
```

# How to stop the pods

```
kubectl delete -k job/test-node
```