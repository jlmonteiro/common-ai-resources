# Gradle Conventions

## Language

Always use Kotlin DSL (`build.gradle.kts`) — never Groovy DSL.

## Project Structure

```
project-root/
├── build.gradle.kts              # Root build script
├── settings.gradle.kts           # Project settings and modules
├── gradle.properties             # Project properties and version
├── gradle/
│   ├── libs.versions.toml        # Version catalog
│   └── wrapper/                  # Gradle wrapper files
├── buildSrc/                     # Shared build logic and conventions
│   └── build.gradle.kts
└── modules/
    ├── service-a/
    │   └── build.gradle.kts
    ├── service-b/
    │   └── build.gradle.kts
    └── deployment/
        └── build.gradle.kts
```

## Module Types

| Type | Purpose | Produces |
|------|---------|----------|
| Implementation | Business logic, application code | Deployable artifacts (JAR, Docker image) |
| Deployment | Helm charts, infrastructure config | Packaged charts |

## Version Catalog (libs.versions.toml)

All dependency versions are centralized in the version catalog:

```toml
[versions]
spring-boot = "3.5.4"
spock = "2.4-M4"
docker-plugin = "9.4.0"

[libraries]
spring-boot-starter = { group = "org.springframework.boot", name = "spring-boot-starter", version.ref = "spring-boot" }
spring-boot-starter-web = { group = "org.springframework.boot", name = "spring-boot-starter-web", version.ref = "spring-boot" }
spock-core = { group = "org.spockframework", name = "spock-core", version.ref = "spock" }

[bundles]
spring = ["spring-boot-starter", "spring-boot-starter-web"]

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
docker = { id = "com.bmuschko.docker-remote-api", version.ref = "docker-plugin" }
```

Usage in build scripts:

```kotlin
plugins {
    alias(libs.plugins.spring.boot)
}

dependencies {
    implementation(libs.bundles.spring)
    testImplementation(libs.spock.core)
}
```

## Settings Configuration

```kotlin
// settings.gradle.kts
rootProject.name = "project-name"
include("modules:service-a")
include("modules:service-b")
include("modules:deployment")
```

## Task Organization

- Group tasks logically: `docker`, `helm`, `package`, `publish`, `versioning`
- Always add meaningful `description`
- Use proper task dependencies (`dependsOn`)
- Use task configuration avoidance (register over create)

```kotlin
tasks.register("package") {
    group = "package"
    description = "packages the deliverable artifacts"
    dependsOn("buildDockerImage")
}
```

## Standards

- Use version catalog for all dependencies — no inline versions
- Use `alias()` for plugins and libraries
- Environment variables for credentials — never hardcode
- Enable Gradle daemon, parallel builds, and build cache
- All modules inherit version from root `gradle.properties`
