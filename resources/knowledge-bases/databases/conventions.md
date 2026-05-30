# Database Conventions

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | plural, snake_case | `users`, `order_items` |
| Columns | singular, snake_case | `first_name`, `created_at` |
| Primary keys | `id` | `id` |
| Foreign keys | `<singular_table>_id` | `user_id`, `order_id` |
| Indexes | `idx_<table>_<columns>` | `idx_users_email` |
| Unique constraints | `uq_<table>_<columns>` | `uq_users_email` |
| Check constraints | `chk_<table>_<description>` | `chk_orders_positive_amount` |
| Boolean columns | `is_` or `has_` prefix | `is_active`, `has_verified` |

## Migrations

- Use a versioned migration tool (Liquibase, Flyway, Alembic)
- File naming: `V<number>__<description>.sql` (e.g., `V001__create_users_table.sql`)
- Every migration must have a rollback strategy
- Never modify a migration that has been applied to any environment
- Test migrations against a copy of production data when possible

## Schema Changes

Follow the **expand-contract** pattern for backward-compatible changes:

1. **Expand** — add new column/table (old code still works)
2. **Migrate** — backfill data, update application code
3. **Contract** — remove old column/table (after all consumers updated)

**Rules:**

- Never rename or drop a column in a single step
- New columns must be nullable or have a default
- Breaking changes require a major version bump
- Document the migration path in the PR description
