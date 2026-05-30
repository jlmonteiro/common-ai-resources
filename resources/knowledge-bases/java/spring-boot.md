# Spring Boot Conventions

## Project Structure

```
src/main/java/com.example.project/
├── Application.java              # Main class
├── config/                       # @Configuration classes
├── controller/                   # @RestController
├── service/                      # @Service (business logic)
├── repository/                   # @Repository (data access)
├── model/
│   ├── entity/                   # JPA entities
│   └── dto/                      # Records (request/response)
├── exception/                    # Custom exceptions + global handler
└── util/                         # Utility classes
```

## Dependency Injection

Always use constructor injection — never field injection. Use Lombok `@RequiredArgsConstructor` with final fields:

```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
}
```

## Lombok

Use Lombok to reduce boilerplate:

- `@RequiredArgsConstructor` — constructor injection (final fields)
- `@Slf4j` — logger declaration
- `@Builder` — builder pattern for complex objects
- `@Data` — only for JPA entities (not DTOs — use records instead)

Never use `@AllArgsConstructor` or `@NoArgsConstructor` without justification.

## REST Controllers

- Use `@RestController` with `@RequestMapping("/api/v1/<resource>")`
- Return `ResponseEntity<T>` for explicit HTTP status control
- Use records for request/response DTOs
- Validate input with `@Valid` and Bean Validation annotations
- Controllers handle HTTP concerns only — delegate to services

## DTO Mapping

Use MapStruct for entity-to-DTO conversions — never manual mapping in services:

```java
@Mapper(componentModel = "spring")
public interface UserMapper {
    UserResponse toResponse(User entity);
    User toEntity(CreateUserRequest request);
}
```

- Annotate mappers with `@Mapper(componentModel = "spring")` for DI
- One mapper per domain aggregate
- Keep mapping logic in the mapper — not in services or controllers

## Validation

Prefer annotation-based validation (Bean Validation / Jakarta Validation) over manual checks:

```java
public record CreateUserRequest(
    @NotBlank @Size(min = 3, max = 50) String username,
    @NotBlank @Email String email,
    @NotNull @Min(18) Integer age
) {}
```

- Use `@Valid` on controller parameters to trigger validation
- Use standard annotations (`@NotBlank`, `@Email`, `@Size`, `@Min`, `@Max`, `@Pattern`)
- Create custom constraint annotations for complex business rules
- Never validate manually in services what can be expressed as annotations

## Exception Handling

Use a global exception handler with `ProblemDetail` (RFC 7807) for all error responses:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setTitle("Resource Not Found");
        return problem;
    }
}
```

- Always use `ProblemDetail` (Spring 6+) — never custom error response classes
- Set `title`, `status`, and `detail` at minimum
- Add `instance` and custom properties when useful for debugging

## Configuration

- Use `application.yml` over `application.properties`
- Profile-specific config: `application-{profile}.yml`
- Use `@ConfigurationProperties` for typed config (not `@Value`)
- Never hardcode secrets — use environment variables or secret managers

### Environment Variable Mapping

Map all configurable values to environment variables with sensible defaults. This makes the application container-friendly (12-Factor App):

```yaml
server:
  port: ${SERVER_PORT:8080}

spring:
  datasource:
    url: ${DB_URL:jdbc:postgresql://localhost:5432/mydb}
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:}

app:
  cache:
    ttl: ${CACHE_TTL:300}
  feature:
    enabled: ${FEATURE_ENABLED:false}
```

**Rules:**

- Every value that differs between environments must be an env var
- Always provide a default that works for local development
- Secrets (passwords, tokens) must have empty defaults — never commit real values
- Use uppercase with underscores for env var names

## Logging

- Use `@Slf4j` (Lombok) for logger declaration
- Use structured logging with key-value pairs
- Log levels: ERROR (failures), WARN (recoverable), INFO (business events), DEBUG (development)
- Never log sensitive data (passwords, tokens, PII)
- Use MDC to enrich logs with contextual information (request ID, user ID, tenant)
- Include correlation IDs for distributed tracing

```java
MDC.put("requestId", requestId);
MDC.put("userId", userId);
try {
    log.info("Processing order orderId={}", orderId);
} finally {
    MDC.clear();
}
```

## Transaction Management

- Use `@Transactional` at service layer — never at controller or repository
- Default to `readOnly = true` for queries
- Keep transactions short — no external calls inside transactions
- Specify rollback rules explicitly

## Health Checks

- Always include Spring Boot Actuator
- Expose `/actuator/health` for liveness/readiness
- Add custom health indicators for critical dependencies
- Configure in `application.yml`:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, info, metrics
  endpoint:
    health:
      show-details: when-authorized
```

## Common Pitfalls

- Don't use `@Autowired` on fields — use constructor injection
- Don't put business logic in controllers
- Don't expose JPA entities in API responses
- Don't catch exceptions in controllers — use `@RestControllerAdvice`
- Don't use `@Transactional` on private methods (won't work with proxies)
- Don't call `@Transactional` methods from within the same class (proxy bypass)
