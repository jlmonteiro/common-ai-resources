# Gradle Version Management

## Single Source of Truth

Version is stored in `gradle.properties`:

```properties
version=1.0.15-SNAPSHOT
```

All modules inherit from root. Never define version in individual module build scripts.

## Version Format

```
MAJOR.MINOR.PATCH[-SNAPSHOT]
```

- `SNAPSHOT` suffix indicates development (not released)
- Release versions have no suffix

## Development Cycle

```
1.0.15-SNAPSHOT  →  1.0.15  →  1.0.16-SNAPSHOT
   (develop)       (release)    (next iteration)
```

1. **Development**: Work with `-SNAPSHOT` version
2. **Release**: Remove `-SNAPSHOT` suffix, tag, publish
3. **Post-release**: Increment patch, add `-SNAPSHOT`

## Rules

- Never deploy SNAPSHOT versions to production
- Release versions are immutable once published
- All modules in a multi-module project share the same version
