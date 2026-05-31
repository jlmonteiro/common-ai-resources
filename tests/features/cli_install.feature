Feature: CLI Install Command
  As a developer
  I want to install skills and knowledge bases for different AI tools
  So that I can use shared resources across Kiro, Claude, and Gemini

  Scenario: Kiro dry run shows agent JSON and tree
    Given a target directory
    When I run install with tool "kiro" name "test-agent" skills "git/commit" kbs "git" and dry-run
    Then the output contains "Dry Run — Kiro CLI"
    And the output contains "test-agent-agent.json"
    And the output contains "prompt.md"
    And the output contains "skills/git/commit"
    And the output contains "knowledge-bases/git"
    And no files are written

  Scenario: Kiro install creates all expected files
    Given a target directory
    When I run install with tool "kiro" name "test-agent" skills "git/commit" kbs "git"
    Then the file "prompt.md" exists in target
    And the file "skills/git/commit/SKILL.md" exists in target
    And the file "knowledge-bases/git/commit-messages.md" exists in target
    And the agent JSON exists at parent with name "test-agent"

  Scenario: Claude install creates correct layout
    Given a target directory
    When I run install with tool "claude" name "my-dev" skills "git/commit" kbs "git"
    Then the file ".mcp.json" exists in target
    And the file ".claude/settings.json" exists in target
    And the file ".claude-skills/commit/SKILL.md" exists in target
    And the file "CLAUDE.md" exists in target

  Scenario: Gemini install creates correct layout
    Given a target directory
    When I run install with tool "gemini" name "my-dev" skills "git/commit" kbs "git"
    Then the file ".gemini/settings.json" exists in target
    And the file ".gemini/skills/commit/SKILL.md" exists in target
    And the file "GEMINI.md" exists in target

  Scenario: Install all resources when none specified
    Given a target directory
    When I run install with tool "kiro" name "all-agent" and no filters
    Then skills directory contains more than 1 skill
    And knowledge-bases directory contains more than 1 scope

  Scenario: Kiro agent JSON contains correct structure
    Given a target directory
    When I run install with tool "kiro" name "java-dev" skills "git/commit" and kbs "git,java"
    Then the agent JSON has name "java-dev"
    And the agent JSON has a skill resource
    And the agent JSON has 2 knowledge base resources

  Scenario: Claude MCP config has no volume mount
    Given a target directory
    When I run install with tool "claude" name "dev" skills "git/commit" kbs "git"
    Then the file ".mcp.json" contains "ghcr.io/jlmonteiro/common-knowledge-base-mcp:latest"
    And the file ".mcp.json" does not contain "-v"

  Scenario: Gemini settings has no volume mount
    Given a target directory
    When I run install with tool "gemini" name "dev" skills "git/commit" kbs "git"
    Then the file ".gemini/settings.json" contains "ghcr.io/jlmonteiro/common-knowledge-base-mcp:latest"
    And the file ".gemini/settings.json" does not contain "-v"

  Scenario: Prompt restricts scopes for Claude
    Given a target directory
    When I run install with tool "claude" name "dev" skills "git/commit" kbs "git"
    Then the file "CLAUDE.md" contains "Do NOT search scopes outside this list"
    And the file "CLAUDE.md" contains "**git**"

  Scenario: Registry finds skills by category/name
    Given the registry
    When I search for skill "git/commit"
    Then exactly 1 skill is found

  Scenario: Registry finds knowledge base by scope
    Given the registry
    When I search for kb "docker"
    Then exactly 1 kb is found

  Scenario: Claude dry run shows MCP config and tree
    Given a target directory
    When I run install with tool "claude" name "dev" skills "git/commit" kbs "git" and dry-run
    Then the output contains "Dry Run — Claude Code"
    And the output contains ".mcp.json"
    And the output contains ".claude/settings.json"
    And the output contains "CLAUDE.md"
    And the output contains ".claude-skills/commit"
    And no files are written

  Scenario: Gemini dry run shows settings and tree
    Given a target directory
    When I run install with tool "gemini" name "dev" skills "git/commit" kbs "git" and dry-run
    Then the output contains "Dry Run — Gemini CLI"
    And the output contains ".gemini/settings.json"
    And the output contains "GEMINI.md"
    And the output contains ".gemini/skills/commit"
    And no files are written

  Scenario: Gemini install writes skills to correct path
    Given a target directory
    When I run install with tool "gemini" name "dev" skills "git/commit" kbs "git"
    Then the file ".gemini/skills/commit/SKILL.md" exists in target
    And the file "GEMINI.md" contains "Do NOT search scopes outside this list"

  Scenario: Claude install writes skills to correct path
    Given a target directory
    When I run install with tool "claude" name "dev" skills "git/commit" kbs "git"
    Then the file ".claude-skills/commit/SKILL.md" exists in target
    And the file "CLAUDE.md" contains "Do NOT search scopes outside this list"

  Scenario: Kiro install prints next steps
    Given a target directory
    When I run install with tool "kiro" name "my-agent" skills "git/commit" kbs "git" and capture output
    Then the output contains "What's Next"
    And the output contains "prompt.md"
