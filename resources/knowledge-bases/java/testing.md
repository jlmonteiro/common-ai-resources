# Java Testing Standards

## Framework

- **Test framework**: Spock (Groovy) with Given-When-Then structure
- **Mocking**: Mockito via `@MockitoBean` / `@MockitoSpyBean` (Spring context-aware)
- **Containers**: Testcontainers for databases, queues, and external services
- **REST testing**: MockMvc for controller tests

## Test Structure

### Class Annotations

Every test class must have `@Title` and `@Narrative`:

```groovy
@Title("User Service")
@Narrative("Handles user creation, retrieval, and validation")
class UserServiceSpec extends Specification {
}
```

### Block Structure

- Indent block content one level from the label
- Use descriptive block labels (not just `given:`, but `given: "a valid user request"`)
- Keep blocks small — use `and:` to break down complex setups or assertions

```groovy
def "should create user and send welcome email"() {
    given: "a valid registration request"
        def request = new CreateUserRequest(name: "John", email: "john@test.com")

    and: "email service is available"
        emailService.send(_, _) >> true

    when: "user is created"
        def result = userService.create(request)

    then: "user is persisted"
        result.id != null
        userRepository.count() == 1

    and: "welcome email is sent"
        1 * emailService.send("john@test.com", _)
}
```

### Data-Driven Tests

Use `where:` blocks for parameterized tests:

```groovy
def "should validate email format: #email"() {
    expect:
        validator.isValid(email) == expected

    where:
        email                | expected
        "user@example.com"   | true
        "invalid"            | false
        ""                   | false
        null                 | false
}
```

## Test Slices

Use the narrowest test slice possible:

| Annotation | Use for | Loads |
|-----------|---------|-------|
| `@WebMvcTest(Controller)` | Controller tests | Web layer only |
| `@DataJpaTest` | Repository tests | JPA + embedded DB |
| `@SpringBootTest` | Integration tests | Full context |

Never use `@SpringBootTest` when a slice is sufficient.

## Mocking Rules

### Prefer Real Beans

Only mock external dependencies (payment gateways, email services, third-party APIs). Use real beans for internal services and repositories.

Mocks are also acceptable to simulate negative or edge case scenarios that are difficult to reproduce with real beans (timeouts, network failures, corrupted data).

```groovy
@SpringBootTest
class OrderServiceSpec extends Specification {
    @Autowired
    OrderService orderService          // Real

    @Autowired
    OrderRepository orderRepository    // Real

    @MockitoBean
    PaymentGateway paymentGateway      // Mock (external)
}
```

### Use Spring-Managed Mocks

- Always use `@MockitoBean` / `@MockitoSpyBean` — never `Mock()` or `Mockito.mock()`
- Spring annotations properly replace beans in the application context
- Manual mocks bypass Spring proxies and AOP

### Don't Mock What You Don't Own

Never mock framework classes (`HttpServletRequest`, `EntityManager`, etc.). Use test utilities instead (`MockMvc`, `TestEntityManager`).

## Test Isolation

- Each test must be independent — one test must never be affected by another
- Use `cleanup:` block or `@Transactional` for data cleanup
- Never use `@Shared` for mutable objects
- Tests must pass in any order
- Shared containers (Testcontainers) are allowed for performance, provided tests don't leak state — use transaction rollback or explicit cleanup to guarantee isolation

## Naming

- Test class: `<ClassUnderTest>Spec` (e.g., `UserServiceSpec`)
- Test method: `"should <expected behavior> when <condition>"`
- Location: `src/test/groovy/` mirroring main package structure

## What NOT to Test

- Don't test Spring framework itself (autowiring works, annotations exist)
- Don't test getters/setters
- Don't test trivial delegation (service just calls repository)
- Don't test third-party library behavior

## Testcontainers

Use for integration tests requiring real infrastructure:

```groovy
@SpringBootTest
@Testcontainers
class DatabaseSpec extends Specification {

    @Container
    @Shared
    static PostgreSQLContainer postgres = new PostgreSQLContainer("postgres:15-alpine")

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl)
        registry.add("spring.datasource.username", postgres::getUsername)
        registry.add("spring.datasource.password", postgres::getPassword)
    }
}
```

## Coverage Expectations

- Business logic (services): high coverage (>80%)
- Controllers: test happy path + error cases
- Repositories: test custom queries only (Spring Data handles the rest)
- Configuration: don't test
