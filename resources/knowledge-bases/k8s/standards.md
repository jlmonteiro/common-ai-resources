# Kubernetes Standards

> **Note:** For Helm chart templating, values, and packaging conventions, see the **helm** knowledge base. This KB covers runtime Kubernetes concerns: resource management, scaling, security, and operational practices.

## Resource Dimensioning

### Requests and Limits

Every container must define both requests and limits:

| Resource | Request (guaranteed) | Limit (maximum) |
|----------|---------------------|-----------------|
| CPU | What the app needs under normal load | 2-3x request (allow burst) |
| Memory | Steady-state usage (measured, not guessed) | Request + headroom for spikes (no OOMKill) |

**Rules:**

- Never deploy without resource requests — causes scheduling chaos
- Never set memory limit equal to request — leaves no room for GC spikes or transient load
- Measure actual usage in staging before setting production values
- CPU limits are optional for non-latency-sensitive workloads (throttling vs bursting trade-off)

### Right-Sizing Process

1. Deploy with generous limits and monitoring
2. Observe actual usage over 7+ days (include peak traffic)
3. Set request = p95 usage, limit = observed max + 20% headroom
4. Review quarterly or after significant changes

## Scaling

### Horizontal Pod Autoscaler (HPA)

- Scale on CPU and/or custom metrics (request rate, queue depth)
- Set `minReplicas` ≥ 2 for high-availability services
- Set `maxReplicas` based on infrastructure capacity and cost budget
- Use `stabilizationWindowSeconds` to prevent flapping

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

### Vertical Pod Autoscaler (VPA)

- Use in `recommend` mode to inform right-sizing — not in auto mode for production
- Never combine VPA (auto) with HPA on the same metric

### Pod Disruption Budgets (PDB)

Required for all services with `replicas > 1`:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
spec:
  minAvailable: 1    # or maxUnavailable: 1
  selector:
    matchLabels:
      app: my-service
```

**Rules:**
- Ensures at least one pod remains during voluntary disruptions (node drain, upgrades)
- Use `minAvailable` for critical services
- Use `maxUnavailable` for batch/worker services

## Security

### Pod Security

- Run as non-root user (match Dockerfile convention)
- Drop all capabilities, add only what's needed
- Read-only root filesystem where possible
- No privilege escalation

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
```

### Network Policies

- Default deny all ingress and egress
- Explicitly allow only required communication paths
- Isolate namespaces — services in namespace A cannot reach namespace B unless explicitly allowed

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### Secrets

- Use Kubernetes Secrets (or external secrets operator) — never ConfigMaps for sensitive data
- Enable encryption at rest for etcd
- Limit secret access via RBAC to specific service accounts
- Rotate secrets without pod restart (use mounted volumes, not env vars for rotatable secrets)

## Namespaces

### Strategy

| Pattern | Use when |
|---------|----------|
| Per-environment | `dev`, `staging`, `production` |
| Per-team | `team-payments`, `team-users` |
| Per-application | `order-service`, `notification-service` |

**Rules:**
- Never deploy to `default` namespace
- Apply ResourceQuotas per namespace to prevent noisy neighbors
- Apply LimitRanges to enforce minimum/maximum per container

### Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
```

## Configuration

### ConfigMaps

- Use for non-sensitive application configuration
- Mount as files for large configs, use env vars for simple key-value
- Version config changes by updating the ConfigMap name or annotation (triggers pod restart)

### Environment Variables

- Map all configurable values to env vars with sensible defaults
- Use `envFrom` for bulk injection (see Helm KB)
- Use `fieldRef` for pod metadata (pod name, namespace, node)

### Immutable Infrastructure

- Never `kubectl exec` to modify running containers
- Never `kubectl edit` deployments in production
- All changes go through git → CI/CD → deploy
- Treat pods as cattle, not pets

## Resilience

### Pod Topology

- Use `topologySpreadConstraints` to distribute pods across nodes/zones
- Use pod anti-affinity for critical services (don't co-locate all replicas)

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: my-service
```

### Graceful Shutdown

- Set `terminationGracePeriodSeconds` to match application drain time
- Handle SIGTERM in the application (stop accepting new requests, finish in-flight)
- Use `preStop` hook if the app needs extra time before SIGTERM

```yaml
lifecycle:
  preStop:
    exec:
      command: ["sh", "-c", "sleep 5"]
terminationGracePeriodSeconds: 30
```

### Startup Dependencies

- Don't rely on pod startup order — design for eventual availability
- Use readiness probes to signal when ready (see Helm KB for probe conventions)
- Use init containers for one-time setup (DB migration, config fetch)

## Labels and Annotations

### Required Labels

Every resource must have:

```yaml
labels:
  app.kubernetes.io/name: my-service
  app.kubernetes.io/version: "1.2.3"
  app.kubernetes.io/component: api
  app.kubernetes.io/part-of: my-platform
  app.kubernetes.io/managed-by: helm
```

### Annotations

Use for operational metadata:

- `description` — what this resource does
- `owner` — team responsible
- `documentation` — link to runbook or docs

### Observability Annotations

For Prometheus/Alloy scraping and log/trace collection:

```yaml
annotations:
  # Metrics scraping
  prometheus.io/scrape: "true"
  prometheus.io/port: "8080"
  prometheus.io/path: "/actuator/prometheus"

  # Log collection
  logs.grafana.com/collect: "true"
  logs.grafana.com/format: "json"

  # Tracing
  traces.grafana.com/collect: "true"
  traces.grafana.com/port: "4317"
  traces.grafana.com/protocol: "grpc"
```

**Rules:**
- Always enable metrics scraping for services exposing a metrics endpoint
- Set log format annotation to match your logging configuration (json/text)
- Enable trace collection for services instrumented with OpenTelemetry
- Disable collection explicitly for noisy sidecar containers
