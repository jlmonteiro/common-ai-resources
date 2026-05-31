# :material-shield-refresh: Resilience

Standards for fault tolerance patterns and graceful degradation.

<div class="grid cards" markdown>

- :material-electric-switch:{ .lg .middle } **Circuit Breaker**

    ---

    States (closed/open/half-open), when to use, fallback.

- :material-refresh:{ .lg .middle } **Retry**

    ---

    Exponential backoff with jitter, idempotency, transient errors only.

- :material-timer-outline:{ .lg .middle } **Timeout**

    ---

    Budget allocation, per-hop limits, deadline propagation.

- :material-wall:{ .lg .middle } **Bulkhead**

    ---

    Resource isolation, connection pools, backpressure.

- :material-backup-restore:{ .lg .middle } **Fallback**

    ---

    Cached response, default value, queued for later.

</div>

## Source

| File | Description |
|------|-------------|
| [`standards.md`](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/knowledge-bases/resilience/standards.md) | Full resilience standards |
