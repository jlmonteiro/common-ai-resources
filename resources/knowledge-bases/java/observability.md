# Observability Standards

## Stack

- **Metrics**: Micrometer + Prometheus (via Spring Actuator)
- **Tracing**: Micrometer Tracing + OpenTelemetry
- **Annotations**: `@Observed` as the primary observability annotation

## Configuration

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, info, metrics, prometheus
  metrics:
    tags:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:dev}
    distribution:
      percentiles-histogram:
        http.server.requests: true
      slo:
        http.server.requests: 100ms, 200ms, 500ms, 1s, 2s
```

## Annotations

### @Observed (Preferred)

Use `@Observed` for all service methods that need observability. It provides both metrics (timer + count) and tracing spans in a single annotation:

```java
@Observed(
    name = "payment.processing",
    contextualName = "process-payment",
    lowCardinalityKeyValues = {"service", "payment"}
)
public Payment processPayment(PaymentRequest request) {
    return paymentRepository.save(mapToEntity(request));
}
```

### @Counted

Use only when you need count without timing:

```java
@Counted(value = "cache.hits")
public User findFromCache(Long id) {
    return cache.get(id);
}
```

### When to Use Which

| Need | Annotation |
|------|-----------|
| Duration + count + tracing | `@Observed` |
| Count only (no timing) | `@Counted` |
| Dynamic tags or complex logic | Programmatic (MeterRegistry) |

## Naming Conventions

- Use dot notation: `<domain>.<action>` (e.g., `payment.processing`, `users.created`)
- Use lowercase
- Tags must be low cardinality — never use user IDs, request IDs, or unbounded values as tags

## Required Observability

Every service must expose:

- RED metrics for all endpoints (Rate, Errors, Duration) — automatic via Actuator
- Custom business metrics for key operations (`@Observed`)
- Health check endpoints (`/actuator/health`)
- Distributed tracing with context propagation across service boundaries

## Tracing

- Use `@Observed` for automatic span creation
- Propagate trace context in async operations (use `TaskDecorator` or manual propagation)
- Add meaningful span attributes for debugging
- Record exceptions on spans

## Setup

Enable `@Observed` annotation support:

```java
@Bean
public ObservedAspect observedAspect(ObservationRegistry registry) {
    return new ObservedAspect(registry);
}
```
