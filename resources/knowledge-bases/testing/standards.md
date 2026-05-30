# Testing Standards

## Methodology: TDD

Follow Test-Driven Development:

1. **Red** — Write a failing test that defines the expected behavior
2. **Green** — Write the minimum code to make the test pass
3. **Refactor** — Clean up the code while keeping tests green

Never write production code without a failing test first.

## Test Structure: BDD

All tests follow Behavior-Driven Development structure:

```
Given: [initial state or preconditions]
When:  [action or event]
Then:  [expected outcome]
```

- Use descriptive labels for each block
- Use `And` to break down complex setups or assertions
- Test names describe behavior: "should [expected outcome] when [condition]"

## Test Types

| Type | Scope | Dependencies | Speed |
|------|-------|-------------|-------|
| Unit | Single function/class | None (or mocks for external) | Fast (<100ms) |
| Integration | Multiple components | Real services (Testcontainers) | Medium (<10s) |
| End-to-End | Full system | Deployed environment | Slow (<60s) |

### Test Pyramid

- **Many** unit tests — fast feedback, cover edge cases and logic branches
- **Some** integration tests — verify components work together with real dependencies
- **Few** end-to-end tests — validate critical user journeys only

Invest most effort in integration tests — they catch the bugs that matter most (real services, real data, real interactions) while remaining fast enough to run on every PR.

## Negative Testing

Never skip negative scenarios. Every feature must test:

- Invalid inputs (null, empty, malformed, boundary values)
- Error conditions (service unavailable, timeout, permission denied)
- Edge cases (empty collections, max values, concurrent access)
- Unauthorized access attempts

For every happy path test, write at least one negative test.

## Mocking Rules

Avoid mocking unless absolutely necessary. Prefer real implementations.

### When mocking is acceptable

- External third-party services (payment gateways, email providers)
- Simulating failure scenarios difficult to reproduce (network timeouts, disk full)
- Services with side effects in tests (sending real emails, charging cards)

### When mocking is NOT acceptable

- Internal services and repositories — use real implementations
- Databases — use Testcontainers
- Message queues — use Testcontainers
- Caches — use embedded or Testcontainers
- Framework classes — use test utilities provided by the framework

### Why

Mocks test the contract you *think* exists, not the one that *actually* exists. Real implementations catch integration bugs that mocks hide.

## Integration Testing

### Testcontainers

Use Testcontainers for all tests requiring external infrastructure:

- Databases (PostgreSQL, MySQL, MongoDB)
- Message brokers (Kafka, RabbitMQ)
- Caches (Redis)
- Search engines (Elasticsearch)
- Any service available as a Docker image

**Rules:**

- Share containers across tests in the same suite for performance
- Guarantee isolation via transaction rollback or explicit cleanup
- Use the same version as production
- Configure via dynamic properties (not hardcoded ports)

### API Testing

- Test real HTTP calls against a running application
- Validate response status, headers, and body
- Test error responses (4xx, 5xx) with correct error format
- Test pagination, filtering, and sorting

## Test Isolation

- Each test must be independent — execution order must not matter
- No shared mutable state between tests
- Clean up after each test (transaction rollback, explicit delete)
- Shared infrastructure (containers) is allowed if state doesn't leak
- Design tests to run in parallel — avoid global state, use unique test data, and isolate resources per test to optimize feedback loop

## Test Data

- Create test data within the test (Given block) — not in shared fixtures
- Use builders or factories for complex objects
- Never rely on pre-existing data in the database
- Use realistic but deterministic data (not random)

## Coverage Expectations

| Layer | Target |
|-------|--------|
| Business logic (services) | >80% |
| API endpoints (controllers) | Happy path + all error cases |
| Data access (repositories) | Custom queries only |
| Configuration | Don't test |
| DTOs / value objects | Don't test |

## What NOT to Test

- Framework behavior (DI works, annotations are processed)
- Getters, setters, constructors with no logic
- Trivial delegation (service just calls repository and returns)
- Third-party library internals
- Generated code (mappers, builders)

## Naming Conventions

- Test class: `<ClassUnderTest>Test` or `<ClassUnderTest>Spec`
- Test method: `"should <expected behavior> when <condition>"`
- Feature files: `<feature-name>.feature` in a `features/` directory
- Test location: mirrors main source structure

## Data-Driven Tests

Use parameterized/data-driven tests for:

- Input validation (multiple valid/invalid inputs)
- Boundary conditions (min, max, edge values)
- Multiple scenarios with same structure but different data

Avoid duplicating test logic — extract to parameterized tests with a data table.
