---
name: "create-migration"
description: "Create a database migration following naming conventions and expand-contract pattern. Use when user says 'create migration', 'add migration', 'modify schema', 'add table', 'add column', or 'database change'."
---

# Create Migration

## Prerequisites

Search the following knowledge bases:
- **databases** — naming conventions, migration workflow, expand-contract pattern
- **testing** — test migrations against real DB (Testcontainers)

## Step 1: Gather Context

Ask the user:

1. "What change do you need?" (add table, add column, modify column, remove column, add index)
2. "Which table/entity is affected?"
3. "Is this a breaking change?" (rename, remove, type change)

## Step 2: Determine Strategy

**Non-breaking changes (single migration):**
- Add new table
- Add nullable column
- Add column with default value
- Add index

**Breaking changes (expand-contract — multiple migrations):**
- Rename column → add new, migrate data, drop old
- Remove column → verify no consumers, then drop
- Change type → add new column, migrate, drop old

Present the strategy:

> "This is a breaking change (renaming `user_name` to `username`). I'll use expand-contract:
> 1. Migration V003: Add `username` column
> 2. Migration V004: Backfill data from `user_name`
> 3. Migration V005: Drop `user_name` (after all consumers updated)
>
> OK?"

## Step 3: Create Migration File

File naming: `V<number>__<description>.sql`

```sql
-- V003__add_username_column.sql

ALTER TABLE users ADD COLUMN username VARCHAR(50);
```

Apply conventions from databases KB:
- Table names: plural, snake_case
- Column names: singular, snake_case
- Index names: `idx_<table>_<columns>`
- Constraint names: `uq_`, `chk_`, `fk_` prefixes

## Step 4: Create Rollback

Every migration must have a rollback strategy:

```sql
-- Rollback for V003
ALTER TABLE users DROP COLUMN username;
```

## Step 5: Create Test

Write a test that:
1. Applies the migration against a Testcontainers database
2. Verifies the schema change is correct
3. Verifies existing data is not corrupted
4. Verifies rollback works

## Step 6: Present Summary

```
✓ Migration created:

Files:
  - migrations/V003__add_username_column.sql
  - migrations/V003__add_username_column_rollback.sql
  - tests/.../MigrationV003Spec

Strategy: Non-breaking (single migration)
Rollback: Tested ✅

Next steps:
  - Review migration SQL
  - Run against staging with production data copy
  - Update application code to use new column
```
