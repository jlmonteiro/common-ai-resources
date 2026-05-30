# Java Coding Standards

## Java Version

- **Required**: Java 21 (LTS)
- Use modern features: records, pattern matching, sealed classes, text blocks

## Language Conventions

### Prefer Modern Constructs

- Records for DTOs and immutable data carriers
- Pattern matching for instanceof and switch
- Text blocks for multi-line strings (SQL, JSON)
- Sealed classes for restricted type hierarchies
- Streams and Optional over imperative loops and null checks

### Null Safety

- Return empty collections instead of null
- Use `Optional` for potentially absent return values
- Use `Objects.requireNonNull` for constructor validation
- Never use `Optional` as a field type or method parameter

### Immutability

- Prefer final fields
- Use `List.of()`, `Set.of()`, `Map.of()` for immutable collections
- Use records for value objects

### Import Style

- Explicit imports only — no wildcards (`import java.util.*`)
- Always import classes — never use fully qualified names (FQDNs) inline
- FQDNs are acceptable only to resolve ambiguity between same-named classes
- Order: `java.*`, blank line, `javax.*`/`jakarta.*`, blank line, third-party, blank line, project
- Remove unused imports

### Deprecated APIs

Never use deprecated APIs. Treat deprecation warnings as errors.

| Deprecated | Replacement |
|-----------|-------------|
| `new Date()` | `Instant.now()`, `LocalDateTime.now()` |
| `StringBuffer` (single-threaded) | `StringBuilder` |
| `Vector`, `Hashtable` | `ArrayList`, `HashMap` |

## Architecture

### Layered Structure

```
Controller Layer (REST API)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
```

### Rules

- Never expose entities directly in APIs — always use DTOs (records)
- Controllers handle HTTP concerns only — no business logic
- Services contain business logic — no HTTP or persistence concerns
- Repositories handle data access only

## Code Complexity

### Limits

- Method length: target ≤20 lines, max 50 lines
- Cyclomatic complexity: target ≤10, max 15
- Class length: target ≤200 lines, max 500 lines

### Patterns

- Use guard clauses (early returns) over nested conditionals
- Extract complex boolean logic to named methods
- Use Strategy pattern for complex conditional chains
- Single responsibility: one class = one reason to change

## Exception Handling

- Catch specific exceptions — never catch generic `Exception`
- Throw specific exceptions — never throw generic `Exception` or `RuntimeException`
- Never swallow exceptions (empty catch blocks)
- Use try-with-resources for all `AutoCloseable` resources
- Log or rethrow — never both at the same layer

## Performance

- Use appropriate collections (ArrayList for access, HashSet for lookup)
- Don't optimize without profiling — write clear code first
- Avoid premature optimization
