# :material-database-edit: Create Migration

Creates database migrations following expand-contract pattern with rollback and test verification.

!!! tip "Triggers"
    - "create migration" / "add migration" / "modify schema"
    - "add table" / "add column" / "database change"

!!! success "Expected Outcomes"
    - Migration file with proper naming (`V<N>__<description>.sql`)
    - Rollback script
    - Test verifying migration against Testcontainers
    - Expand-contract strategy for breaking changes

## Example

!!! example "Scenario: Rename column (breaking change)"

    **Step 1:** "What change?" → Rename `user_name` to `username` in `users` table.

    **Step 2:** Agent detects breaking change, proposes expand-contract:

    > "This is a breaking change. I'll use 3 migrations:
    > 1. V003: Add `username` column (nullable)
    > 2. V004: Backfill data from `user_name` to `username`
    > 3. V005: Drop `user_name` (after all consumers updated)
    >
    > OK?"

    User: "Yes"

    **Step 3:** Creates migration files:

    ```sql
    -- V003__add_username_column.sql
    ALTER TABLE users ADD COLUMN username VARCHAR(50);

    -- V004__backfill_username.sql
    UPDATE users SET username = user_name WHERE username IS NULL;
    ALTER TABLE users ALTER COLUMN username SET NOT NULL;

    -- V005__drop_user_name_column.sql
    ALTER TABLE users DROP COLUMN user_name;
    ```

    **Step 4:** Rollback for each:

    ```sql
    -- Rollback V003
    ALTER TABLE users DROP COLUMN username;
    ```

    **Step 5:** Test applies all migrations against Testcontainers PostgreSQL, verifies data integrity, tests rollback.

    Agent: "V005 should only be applied after confirming all consumers use `username`. I've marked it as pending."

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/database/create-migration/SKILL.md)
