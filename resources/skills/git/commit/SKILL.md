---
name: "commit"
description: "Commit changes with pre-commit sanity checks. Use when user says 'commit', 'save changes', 'commit this', or 'stage and commit'."
---

# Commit Changes

## Prerequisites

Before executing any step, search the **git/** knowledge bases for applicable guidelines, rules, and templates. Key references:

- **git/commit-messages** — message format, types, version impact
- **git/branching** — branch naming, workflow rules
- **git/pre-commit-hooks** — automated vs manual checks
- **git/best-practices** — commit hygiene, security

## Step 0: Detect Existing Hooks

Check if the project has a `.pre-commit-config.yaml` file.

**If it exists:** read it to identify which checks are already automated. Skip those checks in the steps below — don't duplicate what pre-commit already enforces.

Common hooks that eliminate manual checks:

- `detect-private-key` → skip secrets scan (Step 1.1)
- `conventional-pre-commit` → skip message format validation (Step 1.2)
- `no-commit-to-branch` → skip branch check (Step 1.4)
- `ruff-check` → skip lint (Step 2.1)

**If it does NOT exist:** suggest configuring pre-commit hooks. Refer to the **git/pre-commit-hooks** knowledge base for implementation examples. Ask the user:

> "This project has no pre-commit hooks configured. Would you like me to set them up? This automates secrets detection, lint, commit message validation, and branch protection."

- If **accepted**: create `.pre-commit-config.yaml` using the appropriate example from the KB, run `pre-commit install`, then re-run Step 0.
- If **rejected**: proceed with manual AI-driven checks in the steps below.

## Step 1: Mandatory Checks

Run these checks before every commit. Block the commit if any fail.

### 1.1 No Secrets in Staged Files

Scan staged files for patterns that indicate secrets:

- `.env` files
- API keys, tokens, passwords in plain text
- Private keys (`.pem`, `.key`)
- Hardcoded credentials

If found, unstage the file and alert the user.

### 1.2 Commit Message Format

Validate the commit message follows Conventional Commits. Refer to the **git/commit-messages** knowledge base for the full specification.

Check:
- Has a valid type (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `style`, `ci`, `build`, `revert`)
- Subject is imperative mood, lowercase, no period, max 72 chars
- Breaking changes use `!` or `BREAKING CHANGE:` footer

### 1.3 Changelog Updated

If the commit type is `feat`, `fix`, or `perf`, verify that `CHANGELOG.md` has a corresponding entry under `[Unreleased]`. If not, invoke the **update-changelog** skill first.

### 1.4 Branch Check

Verify the current branch is NOT `main` (unless the user explicitly confirmed direct commit). Refer to the **git/branching** knowledge base for workflow rules.

## Step 2: Recommended Checks

Run these when possible. Warn but don't block if they fail.

### 2.1 Lint Passes

Run `inv lint` and report any issues. Suggest fixes but allow the user to proceed.

### 2.2 Tests Pass

Run `inv test` if tests exist for the changed code. Report failures.

### 2.3 Untracked Files

Check for untracked files that might have been forgotten. List them and ask if any should be staged.

### 2.4 Scope Matches Changes

If the commit message includes a scope, verify the changed files are related to that scope. Warn if there's a mismatch.

## Step 3: Execute Commit

Once all mandatory checks pass:

1. Stage files (specific files, not `git add .`)
2. Compose commit message following conventional commits format
3. Execute `git commit`
4. Report the commit hash and summary

## Step 4: Post-Commit

- Suggest `git push` if the branch has a remote
- If this was a release-worthy change, remind about `inv release`
