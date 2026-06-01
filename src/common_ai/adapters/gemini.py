"""Adapter for Gemini CLI — generates GEMINI.md, .gemini/settings.json, and .gemini/skills/."""

import json
import shutil
from pathlib import Path

import click

from common_ai.adapters.base import BaseAdapter
from common_ai.output import print_header, print_tree, print_file_content, print_summary, print_next_steps, build_prompt

MCP_IMAGE = "ghcr.io/jlmonteiro/common-knowledge-base-mcp:latest"


class GeminiAdapter(BaseAdapter):
    def _settings_json(self) -> dict:
        return {
            "mcpServers": {
                "common-knowledge-base-mcp": {
                    "command": "docker",
                    "args": ["run", "-i", "--rm", MCP_IMAGE],
                }
            }
        }

    def _build_gemini_md(self, name: str, kbs: list[Path]) -> str:
        return build_prompt(
            name, kbs,
            "Use the MCP server to search these knowledge bases before answering.\n"
            "Only use the following scopes (pass them in the `scopes` parameter):\n\n"
            "**Important:** Do NOT search scopes outside this list.",
        )

    def preview(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> None:
        print_header("🔍 Dry Run — Gemini CLI")
        tree: dict[str, list[str]] = {}

        if kbs:
            print_header("🔌 MCP Configuration", level=2)
            print_file_content(".gemini/settings.json", None, content=json.dumps(self._settings_json(), indent=2))
            tree.setdefault(".gemini", []).append("settings.json")

        if skills:
            for skill_dir in skills:
                dest = f".gemini/skills/{skill_dir.name}"
                tree.setdefault(dest, []).append("SKILL.md")

        if kbs:
            content = self._build_gemini_md(name, kbs)
            print_header("📝 Agent Prompt", level=2)
            print_file_content("GEMINI.md", None, content=content)
            tree.setdefault(".", []).append("GEMINI.md")

        print_header("🗂️  Target Structure", level=2)
        print_tree(target, tree)
        print_summary(len(skills), len(kbs), dry_run=True)

    def install(self, name: str, target: Path, skills: list[Path], kbs: list[Path], force: bool = False) -> None:
        if target.exists() and any((target / f).exists() for f in [".gemini/settings.json", "GEMINI.md"]) and not force:
            click.echo(f"  ❌ Target already has Gemini config: {target}\n     Use --force to overwrite.", err=True)
            raise SystemExit(1)
        target.mkdir(parents=True, exist_ok=True)

        # .gemini/settings.json (only if KBs selected)
        gemini_dir = target / ".gemini"
        gemini_dir.mkdir(parents=True, exist_ok=True)
        settings_file = None
        if kbs:
            settings_file = gemini_dir / "settings.json"
            settings_file.write_text(json.dumps(self._settings_json(), indent=2) + "\n")

        # Skills to .gemini/skills/<name>/
        for skill_dir in skills:
            dest = gemini_dir / "skills" / skill_dir.name
            if dest.exists():
                shutil.rmtree(dest)
            dest.mkdir(parents=True, exist_ok=True)
            for f in skill_dir.iterdir():
                if f.is_file():
                    shutil.copy2(f, dest / f.name)

        # GEMINI.md at root
        if kbs:
            gemini_md = target / "GEMINI.md"
            gemini_md.write_text(self._build_gemini_md(name, kbs) + "\n")

        steps = [f"Customize your agent prompt: {target / 'GEMINI.md'}"]
        if settings_file:
            steps.append(f"MCP settings: {settings_file}")
        if skills:
            steps.append(f"Skills: {gemini_dir / 'skills'}/")
        print_summary(len(skills), len(kbs), dry_run=False)
        print_next_steps(steps)

    def update(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> None:
        if not target.exists():
            click.echo(f"  ❌ Target does not exist: {target}\n     Use 'install' first.", err=True)
            raise SystemExit(1)

        # Replace skills
        gemini_dir = target / ".gemini"
        skills_dir = gemini_dir / "skills"
        if skills_dir.exists():
            shutil.rmtree(skills_dir)
        for skill_dir in skills:
            dest = skills_dir / skill_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            for f in skill_dir.iterdir():
                if f.is_file():
                    shutil.copy2(f, dest / f.name)

        print_summary(len(skills), len(kbs), dry_run=False)
        print_next_steps([
            "Skills updated to latest version",
            "KBs are served via MCP — no local update needed",
        ])
