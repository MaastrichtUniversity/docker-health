# test-deployment

## Prep

- Make sure that the secret operator is working and can sync with the vault
- See **SOP** for reference <https://mumc.atlassian.net/wiki/spaces/RITDEV/pages/1275494402/Kubernetes+Vault+Secrets+Operator>
- Create the namespace `kubectl create ns dh-health`

### Run the demo-data job first

```bash
kubectl apply -k deploy/overlays/tst/demo-data
```

Now you should be able to apply the whole stack with:

```bash
kubectl apply -k deploy/overlays/tst
```

# Warning

Do not use `kubectl delete -k deploy/overlays/tst`

- this will delete the whole namespace & secret operator
- Instead use:
  
```bash
kubectl delete jobs --all -n dh-health
```

```bash
kubectl delete deploy --all -n dh-health
```
