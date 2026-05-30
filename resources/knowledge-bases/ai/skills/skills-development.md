# Skills Development Guidelines

## What Are Skills?

Skills are structured instruction sets that follow a "Discovery vs Activation" pattern:

- Discovered at startup (agent reads name and description only)
- Activated on-demand when the user's prompt matches the skill's intent
- Save tokens by loading full instructions only when needed
- Follow an open standard compatible with multiple AI tools

## Skill Anatomy

A skill is a directory containing a `SKILL.md` file with YAML frontmatter:

    skill-name/
    └── SKILL.md

### SKILL.md Format

    ---
    name: "skill-name"
    description: "What this skill does. Use when user says X, Y, or Z."
    ---

    # Instructions

    ## Step 1: Preparation
    [What to read or check first]

    ## Step 2: Execution
    [The actual work with code examples]

    ## Step 3: Validation
    [Verify the result]

### Required Components

**YAML Frontmatter:**

- `name` — Skill identifier (kebab-case)
- `description` — Functional intent + trigger phrases (machine-facing)

**Markdown Body:**

- Step-by-step instructions
- Code examples and templates
- Validation/verification criteria

## When to Use Skills

| Use Skills When | Use Context Files When | Use Knowledge Bases When |
|----------------|----------------------|--------------------------|
| Complex multi-step workflows | Core rules needed every interaction | Large reference documentation |
| Large library of guides | Agent identity and personality | API references, specs |
| Token optimization needed | Small, always-relevant instructions | Fact-based lookups |
| Selective activation desired | Coding standards for every response | Searchable on-demand |

## Core Architecture & Execution Model

### The Agent Constitution

An agent needs a Constitution, not just a system prompt. It needs clear boundaries, precise trigger conditions, and a strict separation between hard rules and flexible execution guidelines.

Every task must be mapped against an upfront blueprint before a single artifact is modified. The agent operates under a Requirements-Design-Plan (RDP) trifecta.

### Hard Rules vs Behavioral Guidelines

**Hard Rules (Non-negotiable):**

- Never execute a destructive tool command (recursive file deletion, force-pushes) without explicit user confirmation
- Never hallucinate API parameters or schema definitions — if an endpoint or property is undocumented, use a discovery tool first or ask
- Never proceed with implementation without a clear architectural path

**Behavioral Guidelines (Default but adaptive):**

- When analyzing an open-ended problem, default to providing three distinct technical approaches ranked by implementation speed, complexity, and performance trade-offs
- When presenting critical choices, include a "Do Nothing / Retain Existing" option to counter action-bias

### The THINK vs DO Protocol

When faced with ambiguity, enter a THINK state:

1. Generate an internal draft
2. Analyze edge cases
3. Establish a plan

Do not freeze or block waiting for user input on minor implementation details. If the path is architecturally clear, immediately pivot to DO and surface the completed action.

## Skill Discovery & Execution

### Frontmatter Trigger Rules

The `description` field of a skill is machine-facing, not human-facing. It must contain the explicit functional intent plus specific semantic trigger phrases.

**Bad:**

    description: "Helps write pull request summaries."

**Good:**

    description: "Generate a structured git pull request description. Trigger when the user requests a PR review, asks to stage changes for a code review, or runs the slash command /review-pr."

### Description Quality Criteria

- State the functional outcome (what it produces)
- List 2-3 trigger phrases the user might say
- Mention the slash command if applicable
- Be specific about scope — what it does NOT do

### Context Isolation

For heavy, multi-file investigations, log analysis, or lengthy code refactoring tasks, isolate execution. Run the skill in a forked context to prevent intermediate reasoning from polluting the main conversation history.

## Communication & Tool Integration

### Pre-Tool Brevity Rule

Enforce absolute brevity immediately before firing a tool or invoking an MCP server. Write a maximum of one sentence stating exactly what you are about to look up or execute.

**Bad:**

    "I see you want to look at the logs. I am going to search through the
    application logs to see if I can find any instances of a NullPointerException
    that might be causing this crash..."

**Good:**

    "Searching application logs for 'NullPointerException'."

### Anti-Bias Protocol

When presenting a critical architectural or design choice:

1. Propose a list of ranked alternatives
2. At least one option must always be "Do Nothing", "Defer Strategy", or "Retain Existing Architecture"
3. Detail the hidden risks of moving forward too quickly

This counters natural AI sycophancy and action-bias.

## Technical Artifact Production

### Primitive Types & Slim Signatures

When defining custom skill wrappers, native functions, or MCP tool exports:

- Minimize input parameters
- Use primitive types (`string`, `integer`, `boolean`) over deeply nested objects
- This ensures the LLM's function-calling mechanism maps parameters accurately

### Snake Case in Function Schema

Even if the underlying runtime uses camelCase or PascalCase, define tool names and JSON Schema parameters in `snake_case`. Modern LLMs are disproportionately trained on Python function signatures, making tool-calling significantly more reliable with snake_case keys.

## Skill Structure Best Practices

### One Skill = One Workflow

Do not combine unrelated procedures in a single skill.

**Bad:** `deployment-and-testing-and-monitoring`

**Good:** Separate skills for each concern

### Step Structure

Structure instructions clearly with numbered steps:

1. **Preparation** — what to read or check first
2. **Execution** — the actual work
3. **Validation** — verify the result

Include code examples and checklists within each step.

### Activation Testing

Verify the skill activates with expected prompts:

    User: "update the changelog with the new feature"
    Agent: [Should activate update-changelog skill]

If the skill doesn't activate, improve the description with more trigger keywords.

## Complete Example

A real-world skill for updating a changelog:

    ---
    name: "update-changelog"
    description: "Update CHANGELOG.md with new entries following Keep a Changelog format.
    Use when user says 'update changelog', 'add to changelog', 'log this change',
    or after completing a feature/fix."
    ---

    # Update Changelog

    ## Step 1: Read Current Changelog

    Read `CHANGELOG.md` to understand the current state and existing entries
    under `[Unreleased]`.

    ## Step 2: Determine Category

    Classify the change:
    - **Added** — New features
    - **Changed** — Modifications to existing functionality
    - **Fixed** — Bug fixes
    - **Removed** — Features removed

    ## Step 3: Write the Entry

    - Use imperative mood: "Add", "Fix", "Change"
    - One entry per logical change
    - Write from the user's perspective

    ## Step 4: Insert Under [Unreleased]

    Add the entry under the appropriate category heading.

    ## Step 5: Verify

    - Entry is under `[Unreleased]`
    - Correct category
    - No duplicates
    - Valid markdown

**Why this works:**

- Description contains functional intent ("Update CHANGELOG.md")
- Description lists trigger phrases ("update changelog", "log this change")
- Steps are numbered and focused
- Each step has clear success criteria
- The skill is scoped to one workflow
