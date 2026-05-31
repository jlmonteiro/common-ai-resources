---
name: "create-helm-chart"
description: "Scaffold a Helm chart following conventions. Includes templates, values, helpers, NOTES.txt, and probes. Use when user says 'create helm chart', 'add helm chart', 'scaffold chart', or 'create deployment'."
---

# Create Helm Chart

## Prerequisites

Search the following knowledge bases:
- **helm** — chart structure, values, helpers, NOTES.txt, probes, ConfigMaps/Secrets
- **k8s** — resource limits, security context, network policies, labels
- **docker** — image naming and tagging conventions

## Step 1: Gather Context

Ask the user:

1. "What is the application name?"
2. "What port does it expose?"
3. "Does it need a database or other dependencies?" (for service dependencies in values)
4. "Does it need ingress?" (Yes/No)

## Step 2: Create Chart Structure

```
deployment/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml (if requested)
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── networkpolicy.yaml
│   └── NOTES.txt
└── tests/
    └── deployment_test.yaml
```

## Step 3: Generate Files

### Chart.yaml
- apiVersion v2, type application
- version and appVersion set

### values.yaml
- Follow camelCase, max 3 nesting levels
- Include: replicaCount, image, service, resources, probes, ingress
- Environment variables mapped with defaults
- Document all values with `## @param` comments

### _helpers.tpl
- fullname, labels, selectorLabels, serviceAccountName

### deployment.yaml
- Standard labels (app.kubernetes.io/*)
- Security context (non-root, drop all capabilities, read-only fs)
- Resource requests and limits
- Liveness, readiness, startup probes
- envFrom for ConfigMap and Secret injection
- Topology spread constraints

### NOTES.txt
- Emoji-rich with resources, ingress URLs, validation commands, known issues

### networkpolicy.yaml
- Default deny ingress/egress
- Allow only required paths

## Step 4: Validate

```bash
helm lint ./deployment
helm template my-release ./deployment --debug
```

## Step 5: Present Summary

```
✓ Helm chart created: deployment/

Files: Chart.yaml, values.yaml, 7 templates, 1 test
Features: probes, security context, network policy, NOTES.txt

Next steps:
  - Review values.yaml defaults
  - Run: helm install --dry-run my-release ./deployment
  - Add to CI pipeline
```
