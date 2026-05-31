# :material-upload: Push

Pushes changes with all pre-merge checks. If on main, delegates to create-pr skill.

!!! tip "Triggers"
    - "push" / "push changes" / "ready to merge" / "prepare for PR"

!!! success "Expected Outcomes"
    - Lint, tests, changelog, version, rebase, Docker build all verified
    - Branch pushed with tracking
    - Suggests opening a PR

## Example

!!! example "Scenario: Pushing a feature branch"

    **Step 0:** Branch `feature/add-kbs`, remote `origin`, no tracking.

    **Step 1 — Checks:**

    | Check | Result |
    |-------|--------|
    | 🌿 Branch | ✅ Not on main |
    | 📂 Committed | ✅ Clean |
    | 🧹 Lint | ✅ `ruff check src/` passes |
    | 🧪 Tests | ✅ 22 passed |
    | 📋 Changelog | ✅ `[0.3.0]` section exists |
    | 🏷️ Version | ✅ 0.3.0 (MINOR for features) |
    | 🔄 Rebase | ✅ Up to date with main |
    | 🐳 Docker | ✅ Builds (tagged 0.3.0 + latest) |

    **Step 2:** `git push -u origin feature/add-kbs`

    **Step 3:** "All checks passed. Ready to open a PR? Run 'create pr'."

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/git/push/SKILL.md)
