# Helm Chart Conventions

## Chart Structure

```
my-chart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── _helpers.tpl   # Template helpers
├── tests/             # Unit tests
└── charts/            # Dependencies
```

## Chart.yaml

```yaml
apiVersion: v2
name: my-app
description: Brief description of the chart
type: application
version: 1.0.15
appVersion: "1.0.15"
```

**Rules:**

- `version` and `appVersion` are required
- Both follow SemVer
- Use `-SNAPSHOT` suffix for development versions

## values.yaml Standards

Group related values. Always provide sensible defaults:

```yaml
replicaCount: 2

image:
  repository: ghcr.io/namespace/my-app
  tag: ""  # Defaults to appVersion
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

Document values with comments:

```yaml
## @param replicaCount Number of pod replicas
replicaCount: 2
```

## Template Helpers

Every chart must define standard helpers in `_helpers.tpl`:

```yaml
{{- define "my-app.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "my-app.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "my-app.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "my-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.name }}
{{- .Values.serviceAccount.name }}
{{- else }}
{{- include "my-app.fullname" . }}
{{- end }}
{{- end }}
```

## NOTES.txt

The `templates/NOTES.txt` file is displayed after `helm install/upgrade`. It must provide actionable information for the operator to validate the deployment.

### Requirements

- Use emoji icons for visual scanning
- List all critical resources with their access paths
- Include validation commands the operator can run immediately
- Include known issues or warnings when applicable

### Template

```
{{- $fullName := include "my-app.fullname" . -}}

🚀 {{ .Chart.Name }} v{{ .Chart.AppVersion }} deployed successfully!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Resources:
   • Deployment:  {{ $fullName }}
   • Service:     {{ $fullName }}:{{ .Values.service.port }}
   • Namespace:   {{ .Release.Namespace }}

{{- if .Values.ingress.enabled }}

🌐 Ingress:
{{- range .Values.ingress.hosts }}
   • http{{ if $.Values.ingress.tls }}s{{ end }}://{{ .host }}{{ (first .paths).path }}
{{- end }}
{{- end }}

{{- if eq .Values.service.type "NodePort" }}

🔌 NodePort Access:
   export NODE_PORT=$(kubectl get svc {{ $fullName }} -n {{ .Release.Namespace }} -o jsonpath='{.spec.ports[0].nodePort}')
   export NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}')
   echo http://$NODE_IP:$NODE_PORT
{{- end }}

✅ Validation:
   kubectl get pods -l app.kubernetes.io/instance={{ .Release.Name }} -n {{ .Release.Namespace }}
   kubectl logs -l app.kubernetes.io/instance={{ .Release.Name }} -n {{ .Release.Namespace }} --tail=50

{{- if .Values.healthCheck }}
🏥 Health Check:
   kubectl exec -it deploy/{{ $fullName }} -n {{ .Release.Namespace }} -- curl -s localhost:{{ .Values.service.port }}/health
{{- end }}

{{- if .Values.notes.warnings }}
⚠️  Known Issues:
{{- range .Values.notes.warnings }}
   • {{ . }}
{{- end }}
{{- end }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Rules

- Always show deployment name, namespace, and service port
- Always include validation commands (get pods, logs)
- Show ingress URLs when ingress is enabled
- Show NodePort access commands when service type is NodePort
- Show health check command when health endpoint exists
- Keep it scannable — operators read this in a terminal after deploy

## Standards

- Use Kubernetes standard labels (`app.kubernetes.io/*`)
- Use conditionals for optional resources (`{{- if .Values.ingress.enabled }}`)
- Use `secretKeyRef` for sensitive data — never plain text in values
- Always define resource requests and limits
- Use `toYaml` with `nindent` for nested structures
- Truncate names to 63 characters (Kubernetes limit)

### Values Naming

- Use camelCase for all value keys
- Maximum 3 levels of nesting
- Group by concern (image, service, ingress, resources, probes)

```yaml
# ✅ Good
replicaCount: 2
image:
  repository: my-app
  tag: "1.0.0"

# ❌ Bad — too deep, inconsistent casing
app_config:
  server:
    http:
      connection:
        timeout: 30
```

### Probes

Every container must define liveness and readiness probes:

```yaml
livenessProbe:
  httpGet:
    path: /health/liveness
    port: {{ .Values.service.port }}
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health/readiness
    port: {{ .Values.service.port }}
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3

startupProbe:
  httpGet:
    path: /health/startup
    port: {{ .Values.service.port }}
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 30
```

**Rules:**

- Liveness: "is the process alive?" — restart if not
- Readiness: "can it serve traffic?" — remove from load balancer if not
- Startup: use for slow-starting apps — prevents liveness from killing during init

### ConfigMaps vs Secrets

| Use ConfigMap for | Use Secret for |
|-------------------|---------------|
| Application config (ports, feature flags) | Passwords, tokens, API keys |
| Non-sensitive environment variables | TLS certificates |
| Configuration files (nginx.conf, app.yaml) | Connection strings with credentials |

**Rule:** If the value would be a problem in a git log or terminal output, it's a Secret.

### Environment Injection

Use `envFrom` to inject entire ConfigMaps/Secrets. Use individual `env` only for overrides or computed values:

```yaml
envFrom:
  - configMapRef:
      name: {{ include "my-app.fullname" . }}-config
  - secretRef:
      name: {{ include "my-app.fullname" . }}-secrets

env:
  - name: POD_NAME
    valueFrom:
      fieldRef:
        fieldPath: metadata.name
```

## Validation

Before publishing any chart:

```bash
helm lint ./my-chart                          # Syntax check
helm lint ./my-chart --values values-prod.yaml # With production values
helm template my-release ./my-chart --debug   # Render templates
helm install my-release ./my-chart --dry-run  # Simulate install
```

## Dependencies

```yaml
# Chart.yaml
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.example.com/"
    condition: postgresql.enabled
```

```bash
helm dependency update ./my-chart  # Download dependencies
```

**Rules:**

- Pin dependency versions exactly
- Pin all Docker image tags in values.yaml — never use `latest` in production
- Use `condition` to make dependencies optional
- Run `helm dependency update` after any change to Chart.yaml dependencies
