# :material-source-pull: Create PR

Creates a pull request. If on main, moves commits to a new branch first.

!!! tip "Triggers"
    - "create PR" / "open PR" / "create pull request"
    - "send for review" / "create merge request"

!!! success "Expected Outcomes"
    - Commits on a feature branch (not main)
    - PR created with conventional commit title and description template
    - PR URL displayed

## Example

!!! example "Scenario: Working on main with 7 commits"

    **Step 0:** On `main` with unpushed commits → moves to Step 1.

    **Step 1 — Move Off Main:**

    Agent analyzes commits:
    ```
    feat: initial project scaffold
    feat: add MCP server
    docs: add documentation
    feat: add git knowledge bases
    ```

    > "Primary type: feat. Suggested branch: `feature/initial-project-setup`. OK?"

    User: "Yes"

    Creates branch, resets main to origin.

    **Step 2:** Runs all pre-push checks (lint, tests, changelog, version).

    **Step 3:** `git push -u origin feature/initial-project-setup`

    **Step 4 — Create PR:**

    ```
    Title: feat: initial project setup

    ## Summary
    Initial project scaffold with MCP server, knowledge bases, and documentation.

    ## Changes
    - Python CLI with generate/install commands
    - MCP knowledge base server (Docker, semantic search)
    - Git, Docker, SDD knowledge bases
    - MkDocs Material documentation

    ## Testing
    - inv lint passes
    - inv build succeeds
    - mkdocs build --strict passes
    ```

    Opens: `gh pr create --title "..." --body "..." --base main`

    Result: `https://github.com/user/repo/pull/1`

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/git/create-pr/SKILL.md)
