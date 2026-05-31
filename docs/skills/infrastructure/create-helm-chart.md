# :material-ship-wheel: Create Helm Chart

Scaffolds a complete Helm chart with security context, probes, network policies, and NOTES.txt.

!!! tip "Triggers"
    - "create helm chart" / "add helm chart" / "scaffold chart" / "create deployment"

!!! success "Expected Outcomes"
    - Full chart: Chart.yaml, values.yaml, templates, tests
    - Security context, probes, network policy included
    - NOTES.txt with emoji, validation commands
    - Validated with `helm lint`

## Example

!!! example "Scenario: Chart for order-service"

    **Step 1:** "App name?" → order-service. "Port?" → 8080. "Database?" → PostgreSQL. "Ingress?" → Yes.

    **Step 2:** Creates full chart structure.

    **Step 3:** Key files generated:

    `values.yaml`:
    ```yaml
    replicaCount: 2
    image:
      repository: ghcr.io/user/order-service
      tag: ""
    service:
      port: 8080
    ingress:
      enabled: true
      hosts:
        - host: orders.example.com
    resources:
      requests:
        cpu: 250m
        memory: 256Mi
      limits:
        cpu: 500m
        memory: 512Mi
    ```

    `NOTES.txt` output after install:
    ```
    🚀 order-service v1.0.0 deployed!

    📋 Resources:
       • Deployment: my-release-order-service
       • Service: my-release-order-service:8080

    🌐 Ingress:
       • https://orders.example.com/

    ✅ Validation:
       kubectl get pods -l app.kubernetes.io/instance=my-release
    ```

    **Step 4:** `helm lint` ✅, `helm template --debug` ✅

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/infrastructure/create-helm-chart/SKILL.md)
