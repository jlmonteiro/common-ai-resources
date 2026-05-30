# Caching Standards

## Libraries

| Type | Library | Use when |
|------|---------|----------|
| Local cache | Caffeine | Single instance, low latency, small dataset |
| Distributed cache | Redis | Multi-instance, shared state, large dataset |

## When to Cache

- Data read frequently, changes infrequently (reference data, catalogs, profiles)
- Expensive computations or database queries
- External API responses with stable data

## When NOT to Cache

- Real-time data that must be current
- Frequently mutated data (high write-to-read ratio)
- Security-sensitive data (tokens, credentials)
- Large objects that would exhaust memory

## Annotations

Use Spring Cache annotations — never manual cache get/put:

| Annotation | Purpose |
|-----------|---------|
| `@Cacheable` | Cache the result, return cached on subsequent calls |
| `@CachePut` | Always execute, update cache with result |
| `@CacheEvict` | Remove entry from cache |
| `@CacheConfig` | Class-level cache defaults |

```java
@Service
@CacheConfig(cacheNames = "users")
public class UserService {

    @Cacheable(key = "#id")
    public User findById(Long id) {
        return userRepository.findById(id).orElseThrow();
    }

    @CachePut(key = "#user.id")
    public User update(User user) {
        return userRepository.save(user);
    }

    @CacheEvict(key = "#id")
    public void delete(Long id) {
        userRepository.deleteById(id);
    }
}
```

## Configuration

### Caffeine (Local)

```yaml
spring:
  cache:
    type: caffeine
    caffeine:
      spec: maximumSize=1000,expireAfterWrite=300s
```

### Redis (Distributed)

```yaml
spring:
  cache:
    type: redis
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      timeout: ${REDIS_TIMEOUT:2000}
```

## Rules

- Always define TTL — never cache indefinitely
- Always define max size for local caches
- Use meaningful cache names (not generic "cache1")
- Evict on write operations — stale data is worse than a cache miss
- Monitor cache hit/miss ratios via metrics
- Handle cache failures gracefully — cache down should not break the application
