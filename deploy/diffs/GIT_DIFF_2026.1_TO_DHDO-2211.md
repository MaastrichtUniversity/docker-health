# Git Diff: 2026.1 → DHDO-2211
## deploy/overlays/local

**Generated:** 2026-07-23  
**Branch:** `DHDO-2211` vs `2026.1`

---

## Summary

This diff shows significant refactoring of the Kubernetes deployment overlays, primarily focused on:

1. **Namespace restructuring** - Moving from a single `dh-health` namespace to node-specific namespaces
2. **Secret naming consolidation** - Removing node prefixes from secret names
3. **Gateway/Route namespace cleanup** - Removing explicit namespace declarations
4. **Service discovery reorganization** - Moving to shared-components with name suffixes
5. **New directory structure** - Creating dedicated `jupyter`, `config`, `service-discovery` overlays
6. **Test federation restructure** - Complete redesign of the test-federation overlay

---

## File Structure Changes

### Deleted Files

- `deploy/overlays/local/jupyter-zib-config/kustomization.yaml`
- `deploy/overlays/local/shared/components/kustomization.yaml`
- `deploy/overlays/local/shared/kustomization.yaml`
- `deploy/overlays/local/test-federation/job-reader-role.yaml`
- `deploy/overlays/local/test-federation/job.yaml`

### Renamed/Moved Files

| From | To |
|------|-----|
| `jupyter-zib-config/jupyter-zib-gateway.yaml` | `jupyter/jupyter-zib-gateway.yaml` |
| `shared/components/service-discovery/` | `shared-components/service-discovery/` |
| `shared/components/data-encryption-secret/` | `shared-components/data-encryption-secret/` |
| `shared/components/federation-secret/` | `shared-components/federation-secret/` |
| `shared/components/terminology-server-proxy-secret/` | `shared-components/terminology-server-proxy-secret/` |
| `test-federation/job-reader-role.yaml` | `test-federation/job/job-reader-role.yaml` |
| `test-federation/job.yaml` | `test-federation/job/job.yaml` |

### New Files

#### Jupyter Overlay
- `jupyter/kustomization.yaml`
- `jupyter/namespace.yaml`

#### Node Config (per node: envida, mumc, vitala, zio)
- `node-{NODE}/config/kustomization.yaml`
- `node-{NODE}/config/namespace.yaml`
- `node-{NODE}/config/services-list-role-binding.yaml`
- `node-{NODE}/service-discovery/kustomization.yaml`
- `node-{NODE}/etl-config_secrets/kustomization.yaml`

#### Shared Components
- `shared-components/kustomization.yaml`
- `shared-components/service-discovery/services-list-role.yaml`

#### Test Federation
- `test-federation/job/namespace.yaml`
- `test-federation/job/kustomization.yaml`
- `test-federation/job/job.yaml`
- `test-federation/job/services-list-role-binding.yaml`
- `test-federation/nodes/kustomization.yaml`
- `test-federation/nodes/envida/kustomization.yaml`
- `test-federation/nodes/mumc/kustomization.yaml`
- `test-federation/nodes/vitala/kustomization.yaml`
- `test-federation/nodes/zio/kustomization.yaml`

---

## Key Changes by Category

### 1. Namespace Changes

**Before:** All resources used `namespace: dh-health`

**After:** Node-specific namespaces:
- `dh-health-envida`
- `dh-health-mumc`
- `dh-health-vitala`
- `dh-health-zio`
- `dh-health-jupyter`
- `dh-health-test`
- `dh-health-test-federation`

**Example (node-envida/kustomization.yaml):**
```yaml
namespace: dh-health-envida
```

### 2. Secret Naming Changes

Secrets are now **without node prefixes**, with `namePrefix` used in kustomizations to avoid collisions:

| Old Name | New Name |
|----------|----------|
| `envida-ehrbase-creds` | `ehrbase-creds` |
| `envida-portal-creds` | `portal-creds` |
| `envida-federation-key` | `federation-key` |
| `mumc-ehrbase-creds` | `ehrbase-creds` |
| `zio-federation-key` | `federation-key` |

**Example (node-envida/etl-config_secrets/kustomization.yaml):**
```yaml
namePrefix: envida-
resources:
  - ../../../../base/openehr-nodes/envida/etl-zib/etl-config
components:
  - ../components/secrets
```

### 3. Gateway/HTTPRoute Changes

**Removed:** Explicit `namespace: dh-health` declarations  
**Changed:** Backend service names from `{node}-{service}` to just `{service}`

**Example (node-envida/components/ehrbase-gateway/ehrbase-gateway.yaml):**
```yaml
# Before
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: envida-ehrbase-gateway
  namespace: dh-health  # REMOVED

# After
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: envida-ehrbase-gateway
  # namespace removed

spec:
  # ...
  backendRefs:
    - name: envida-ehrbase  # CHANGED TO: ehrbase
      port: 8080
```

**Backend renaming pattern:**
- `envida-ehrbase` → `ehrbase`
- `mumc-etl-zib-rest` → `etl-zib-rest`
- `vitala-federation-rest` → `federation-rest`
- `zio-terminology-server-proxy` → `terminology-server-proxy`

### 4. Service Discovery Restructuring

**Before:** Single `service-discovery` component in shared/components

**After:** 
- Moved to `shared-components/service-discovery`
- Each node uses `nameSuffix` to avoid ClusterRole name collisions:
  - `services-list-envida`
  - `services-list-mumc`
  - `services-list-vitala`
  - `services-list-zio`

**Example (node-envida/service-discovery/kustomization.yaml):**
```yaml
nameSuffix: -envida
components:
  - ../../shared-components/service-discovery
```

### 5. Main Kustomization Changes

**deploy/overlays/local/kustomization.yaml:**

**Before:**
```yaml
resources:
  - ../../base/jupyter-zib
  - ../../base/openehr-nodes/envida
  - ../../base/openehr-nodes/mumc
  - ../../base/openehr-nodes/vitala
  - ../../base/openehr-nodes/zio

components:
  - jupyter-zib-config
  - node-envida/components
  - node-mumc/components
  - node-vitala/components
  - node-zio/components
```

**After:**
```yaml
resources:
  - jupyter
  - node-envida
  - node-mumc
  - node-vitala
  - node-zio
```

### 6. Test Federation Changes

Complete restructuring with new `nodes/` directory:

**Before:** Flat structure with all nodes listed in main kustomization

**After:** Hierarchical structure:
```
test-federation/
├── nodes/
│   ├── kustomization.yaml
│   ├── envida/kustomization.yaml
│   ├── mumc/kustomization.yaml
│   ├── vitala/kustomization.yaml
│   └── zio/kustomization.yaml
└── job/
    ├── kustomization.yaml
    ├── namespace.yaml
    ├── job.yaml
    ├── job-reader-role.yaml
    └── services-list-role-binding.yaml
```

**Job changes:**
- Updated to query jobs across **all namespaces** (`-A` flag)
- Changed from namespace-specific to cross-namespace job monitoring
- Updated federation URLs to use node-specific namespaces:
  - `http://federation-rest.dh-health-envida:8000`
  - `http://federation-rest.dh-health-mumc:8000`
  - etc.

### 7. RBAC Changes

**services-list Role/Binding:**

**Before:** Role + RoleBinding in `dh-health` namespace

**After:** 
- ClusterRole in `shared-components/service-discovery`
- Per-node ClusterRoleBinding with `nameSuffix`
- Test federation has its own `services-list-binding-federation`

**Example (node-envida/config/services-list-role-binding.yaml):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: services-list-binding-envida
subjects:
- kind: ServiceAccount
  name: default
roleRef:
  kind: ClusterRole
  name: services-list-envida  # Note the suffix
  apiGroup: rbac.authorization.k8s.io
```

---

## Gateway Backend Changes Summary

All gateway HTTPRoutes now point to **non-prefixed** service names:

| Service | Old Backend | New Backend |
|---------|-------------|-------------|
| EHRBase | `{node}-ehrbase` | `ehrbase` |
| ETL ZIB REST | `{node}-etl-zib-rest` | `etl-zib-rest` |
| Transform REST | `{node}-transform-rest` | `transform-rest` |
| Federation REST | `{node}-federation-rest` | `federation-rest` |
| Terminology Proxy | `{node}-terminology-server-proxy` | `terminology-server-proxy` |
| OpenEHRTool | `{node}-openehrtool` | `openehrtool` |
| Portal | `{node}-portal` | `portal` |

---

## New Shared Components Structure

**deploy/overlays/local/shared-components/kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

resources:
  - ../../../base/base-config

components:
  - data-encryption-secret
  - federation-secret
  # service-discovery excluded to avoid name collision
  - terminology-server-proxy-secret

patches:
  - target:
      kind: Deployment
    patch: |
      - op: replace
        path: /spec/template/spec/containers/0/imagePullPolicy
        value: Never

configMapGenerator:
  - name: ehrbase-config-base
    behavior: merge
    literals:
      - ADMIN_API_ACTIVE=true
```

---

## Migration Notes

1. **Secret references** in existing manifests need updating to remove node prefixes
2. **Service names** in gateways/routes are now un-prefixed
3. **Namespace references** should be updated to node-specific namespaces
4. **Test federation job** now queries all namespaces instead of just `dh-health`
5. **ClusterRole names** now have node suffixes to avoid collisions

---

## Statistics

- **Files deleted:** 6
- **Files renamed/moved:** 6
- **Files created:** ~30
- **Nodes affected:** envida, mumc, vitala, zio
- **Namespaces introduced:** 7 (jupyter, envida, mumc, vitala, zio, test, test-federation)
