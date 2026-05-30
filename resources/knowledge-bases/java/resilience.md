# Resilience Standards

## Library

Resilience4j with Spring Boot integration. Use annotation-based configuration.

## Circuit Breakers

### When to Use

- External HTTP calls (third-party APIs, other microservices)
- Database connections under high load
- Any dependency that can become unresponsive

### When NOT to Use

- Internal method calls within the same service
- Fast-failing validations
- Operations that should always be attempted (fire-and-forget)

### Default Configuration

```yaml
resilience4j:
  circuitbreaker:
    configs:
      default:
        sliding-window-type: COUNT_BASED
        sliding-window-size: 10
        minimum-number-of-calls: 5
        failure-rate-threshold: 50
        slow-call-duration-threshold: 5s
        wait-duration-in-open-state: 60s
        permitted-number-of-calls-in-half-open-state: 3
        automatic-transition-from-open-to-half-open-enabled: true
        record-exceptions:
          - java.net.ConnectException
          - java.net.SocketTimeoutException
          - org.springframework.web.client.HttpServerErrorException
        ignore-exceptions:
          - com.example.exception.ValidationException
          - com.example.exception.ResourceNotFoundException
```

### Usage

```java
@CircuitBreaker(name = "externalApi", fallbackMethod = "fallback")
public Response callExternalApi(Request request) {
    return restClient.post(request);
}

private Response fallback(Request request, Exception ex) {
    return Response.defaultResponse();
}
```

## Retries

### When to Use

- Transient network failures
- Temporary service unavailability
- Database connection timeouts

### When NOT to Use

- Validation errors (4xx responses)
- Business logic failures
- Non-idempotent operations without idempotency keys

### Default Configuration

```yaml
resilience4j:
  retry:
    configs:
      default:
        max-attempts: 3
        wait-duration: 1s
        enable-exponential-backoff: true
        exponential-backoff-multiplier: 2
        retry-exceptions:
          - java.net.ConnectException
          - java.net.SocketTimeoutException
          - org.springframework.web.client.ResourceAccessException
        ignore-exceptions:
          - com.example.exception.ValidationException
          - com.example.exception.ResourceNotFoundException
```

### Usage

```java
@Retry(name = "externalApi", fallbackMethod = "fallback")
public Response callWithRetry(Request request) {
    return restClient.post(request);
}
```

## Rules

- Always define a fallback method for circuit breakers
- Always use exponential backoff with jitter for retries
- Never retry non-idempotent operations
- Record only infrastructure exceptions — ignore business exceptions
- Configure per-instance overrides for different SLA requirements
- Combine circuit breaker + retry: retry wraps circuit breaker (retry first, then circuit breaker trips)
- All resilience config goes in `application.yml` — not hardcoded in annotations
