"""Adapter for Claude Code — generates .mcp.json, .claude/settings.json, .claude-skills/, and CLAUDE.md."""

import json
import shutil
from pathlib import Path

from common_ai.adapters.base import BaseAdapter
from common_ai.output import print_header, print_tree, print_file_content, print_summary, print_next_steps

MCP_IMAGE = "ghcr.io/jlmonteiro/common-knowledge-base-mcp:latest"


class ClaudeAdapter(BaseAdapter):
    def _mcp_json(self) -> dict:
        return {
            "mcpServers": {
                "common-knowledge-base-mcp": {
                    "command": "docker",
                    "args": ["run", "-i", "--rm", MCP_IMAGE],
                }
            }
        }

    def _settings_json(self) -> dict:
        return {
            "allowedTools": ["common-knowledge-base-mcp:*"]
        }

    def _build_claude_md(self, name: str, kbs: list[Path]) -> str:
        kb_list = "\n".join(f"- **{kb.name}** — {kb.name} conventions and standards" for kb in kbs)
        return f"""# {name}

## Role

You are a senior developer specializing in [YOUR DOMAIN HERE].
You help the team write clean, tested, production-ready code following established conventions.

## Expertise

- [List your agent's areas of expertise]
- [e.g., Java/Spring Boot development]
- [e.g., REST API design]

## Knowledge Bases

Use the MCP server to search these knowledge bases before answering.
Only use the following scopes (pass them in the `scopes` parameter):

{kb_list}

**Important:** Do NOT search scopes outside this list.

## Principles

1. **Convention over configuration** — follow the knowledge bases, don't reinvent
2. **Test-driven** — write tests before or alongside implementation
3. **Security by default** — validate inputs, use parameterized queries, handle errors
4. **Minimal and correct** — solve what was asked, don't over-engineer
"""

    def preview(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> None:
        print_header("🔍 Dry Run — Claude Code")
        tree: dict[str, list[str]] = {}

        if kbs:
            print_header("🔌 MCP Configuration", level=2)
            print_file_content(".mcp.json", None, content=json.dumps(self._mcp_json(), indent=2))
            tree.setdefault(".", []).append(".mcp.json")

            print_header("🔒 Tool Permissions", level=2)
            print_file_content(".claude/settings.json", None, content=json.dumps(self._settings_json(), indent=2))
            tree.setdefault(".claude", []).append("settings.json")

        if skills:
            for skill_dir in skills:
                dest = f".claude-skills/{skill_dir.name}"
                tree.setdefault(dest, []).append("SKILL.md")

        if kbs:
            content = self._build_claude_md(name, kbs)
            print_header("📝 Agent Prompt", level=2)
            print_file_content("CLAUDE.md", None, content=content)
            tree.setdefault(".", []).append("CLAUDE.md")

        print_header("🗂️  Target Structure", level=2)
        print_tree(target, tree)
        print_summary(len(skills), len(kbs), dry_run=True)

    def install(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> None:
        target.mkdir(parents=True, exist_ok=True)

        # .mcp.json at project root
        mcp_file = target / ".mcp.json"
        mcp_file.write_text(json.dumps(self._mcp_json(), indent=2) + "\n")

        # .claude/settings.json
        claude_dir = target / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)
        settings_file = claude_dir / "settings.json"
        settings_file.write_text(json.dumps(self._settings_json(), indent=2) + "\n")

        # Skills to .claude-skills/<name>/
        for skill_dir in skills:
            dest = target / ".claude-skills" / skill_dir.name
            if dest.exists():
                shutil.rmtree(dest)
            dest.mkdir(parents=True, exist_ok=True)
            for f in skill_dir.iterdir():
                if f.is_file():
                    shutil.copy2(f, dest / f.name)

        # CLAUDE.md at root
        if kbs:
            claude_md = target / "CLAUDE.md"
            claude_md.write_text(self._build_claude_md(name, kbs) + "\n")

        print_summary(len(skills), len(kbs), dry_run=False)
        print_next_steps(name, [
            f"Customize your agent prompt: {target / 'CLAUDE.md'}",
            f"MCP config: {mcp_file}",
            f"Skills: {target / '.claude-skills'}/",
        ])
