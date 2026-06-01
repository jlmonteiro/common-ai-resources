"""Adapter for Kiro CLI — installs skills, knowledge bases, agent.json, and prompt.md."""

import json
import shutil
from pathlib import Path

import click

from common_ai.adapters.base import BaseAdapter
from common_ai.output import print_header, print_tree, print_file_content, print_summary, print_next_steps, build_prompt

SKILLS_SUBDIR = "skills"
KB_SUBDIR = "knowledge-bases"


class KiroAdapter(BaseAdapter):
    def _agent_json(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> dict:
        resources = [f"file://{target / 'prompt.md'}"]
        if skills:
            resources.append(f"skill://{target / SKILLS_SUBDIR}/**/SKILL.md")
        for kb_dir in kbs:
            resources.append({
                "type": "knowledgeBase",
                "name": kb_dir.name.replace("-", " ").title(),
                "description": f"{kb_dir.name} conventions and standards. Use when working with {kb_dir.name}-related tasks.",
                "source": f"file://{target / KB_SUBDIR / kb_dir.name}",
                "indexType": "best",
                "include": ["**/*.md"],
            })
        return {
            "name": name,
            "resources": resources,
            "tools": ["read", "write", "knowledge", "shell", "use_subagent"],
            "allowedTools": ["read", "knowledge"],
            "toolsSettings": {
                "shell": {
                    "autoAllowReadonly": True,
                    "allowedCommands": [
                        "git *",
                        "find *",
                        "ls *",
                        "grep *",
                        "cat *",
                        "gh *",
                        "./gradlew *",
                        "npm *",
                        "npx *",
                        "docker *",
                        "docker-compose *",
                    ],
                },
                "write": {"allowedPaths": ["."]},
                "knowledge": {"autoAllow": True},
                "use_subagent": {"trustedAgents": [name]},
            },
        }

    def _prompt_md(self, name: str, kbs: list[Path]) -> str:
        return build_prompt(
            name, kbs,
            "The following knowledge bases contain project conventions and decisions. Always search them before answering:",
        )

    def preview(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> None:
        print_header("🔍 Dry Run — Kiro CLI")
        tree: dict[str, list[str]] = {}

        agent_config = self._agent_json(name, target, skills, kbs)
        agent_file = f"{name}-agent.json"
        print_header("🤖 Agent Configuration", level=2)
        print_file_content(agent_file, None, content=json.dumps(agent_config, indent=2))
        tree.setdefault(".", []).append(agent_file)

        print_header("📝 Agent Prompt", level=2)
        print_file_content("prompt.md", None, content=self._prompt_md(name, kbs))
        tree.setdefault(".", []).append("prompt.md")

        if skills:
            for skill_dir in skills:
                dest = target / SKILLS_SUBDIR / skill_dir.parent.name / skill_dir.name
                tree.setdefault(str(dest.relative_to(target)), []).append("SKILL.md")

        if kbs:
            for kb_dir in kbs:
                dest = target / KB_SUBDIR / kb_dir.name
                files = sorted(kb_dir.rglob("*.md"))
                file_names = [str(f.relative_to(kb_dir)) for f in files]
                tree.setdefault(str(dest.relative_to(target)), []).extend(file_names)

        print_header("🗂️  Target Structure", level=2)
        print_tree(target, tree)
        print_summary(len(skills), len(kbs), dry_run=True)

    def install(self, name: str, target: Path, skills: list[Path], kbs: list[Path], force: bool = False) -> None:
        if target.exists() and not force:
            click.echo(f"  ❌ Target already exists: {target}\n     Use --force to overwrite.", err=True)
            raise SystemExit(1)
        target.mkdir(parents=True, exist_ok=True)
        installed_skills = 0
        installed_kbs = 0

        for skill_dir in skills:
            dest = target / SKILLS_SUBDIR / skill_dir.parent.name / skill_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            for f in skill_dir.iterdir():
                if f.is_file():
                    shutil.copy2(f, dest / f.name)
            installed_skills += 1

        for kb_dir in kbs:
            dest = target / KB_SUBDIR / kb_dir.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(kb_dir, dest)
            installed_kbs += 1

        # Write prompt.md
        prompt_file = target / "prompt.md"
        prompt_file.write_text(self._prompt_md(name, kbs))

        # Write agent.json next to the resources dir
        agent_config = self._agent_json(name, target, skills, kbs)
        agent_file = target.parent / f"{name}-agent.json"
        agent_file.write_text(json.dumps(agent_config, indent=2) + "\n")

        print_summary(installed_skills, installed_kbs, dry_run=False)
        print_next_steps([
            f"Customize your agent prompt: {target / 'prompt.md'}",
            f"Agent config: {agent_file}",
            "Review 'tools', 'allowedTools', and 'toolsSettings' in the agent JSON and adjust to your needs",
            "Add a 'description' field to the agent JSON to describe your agent's purpose",
        ])

    def update(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> None:
        if not target.exists():
            click.echo(f"  ❌ Target does not exist: {target}\n     Use 'install' first.", err=True)
            raise SystemExit(1)

        updated_skills = 0
        updated_kbs = 0

        # Replace skills
        skills_dir = target / SKILLS_SUBDIR
        if skills_dir.exists():
            shutil.rmtree(skills_dir)
        for skill_dir in skills:
            dest = target / SKILLS_SUBDIR / skill_dir.parent.name / skill_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            for f in skill_dir.iterdir():
                if f.is_file():
                    shutil.copy2(f, dest / f.name)
            updated_skills += 1

        # Replace knowledge bases
        kbs_dir = target / KB_SUBDIR
        if kbs_dir.exists():
            shutil.rmtree(kbs_dir)
        for kb_dir in kbs:
            dest = target / KB_SUBDIR / kb_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copytree(kb_dir, dest, dirs_exist_ok=True)
            updated_kbs += 1

        # Merge agent.json — preserve user customizations
        agent_file = target.parent / f"{name}-agent.json"
        if agent_file.exists():
            existing = json.loads(agent_file.read_text())
        else:
            existing = {"name": name}

        # Build new resources list
        new_config = self._agent_json(name, target, skills, kbs)
        new_resources = new_config["resources"]

        # Preserve user-added resources not managed by us
        managed_sources = {r["source"] for r in new_resources if isinstance(r, dict)}
        managed_strings = set(r for r in new_resources if isinstance(r, str))
        user_resources = []
        for r in existing.get("resources", []):
            if isinstance(r, dict) and r.get("source") not in managed_sources:
                user_resources.append(r)
            elif isinstance(r, str) and r not in managed_strings:
                user_resources.append(r)
        existing["resources"] = new_resources + user_resources

        agent_file.write_text(json.dumps(existing, indent=2) + "\n")

        print_summary(updated_skills, updated_kbs, dry_run=False)
        print_next_steps([
            "Skills and knowledge bases updated to latest version",
            f"Agent config merged: {agent_file}",
            "Your prompt.md, tools, and description were preserved",
        ])
