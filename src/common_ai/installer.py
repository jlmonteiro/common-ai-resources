from pathlib import Path

import click

from common_ai.adapters import get_adapter
from common_ai.registry import Registry


class Installer:
    def __init__(self, tool: str, name: str, target: str, skills: list[str], kbs: list[str], force: bool = False):
        self.adapter = get_adapter(tool)
        self.name = name
        self.target = Path(target).expanduser()
        self.force = force
        self.registry = Registry()
        self.selected_skills = self._resolve_skills(skills)
        self.selected_kbs = self._resolve_kbs(kbs)

    def _resolve_skills(self, skills: list[str]) -> list[Path]:
        if not skills or "all" in skills:
            return self.registry.all_skills()
        resolved = []
        for name in skills:
            found = self.registry.find_skills(name)
            if not found:
                click.echo(f"  ⚠️  Skill not found: {name}", err=True)
            resolved.extend(found)
        return resolved

    def _resolve_kbs(self, kbs: list[str]) -> list[Path]:
        if not kbs or "all" in kbs:
            return self.registry.all_kbs()
        resolved = []
        for name in kbs:
            found = self.registry.find_kbs(name)
            if not found:
                click.echo(f"  ⚠️  Knowledge base not found: {name}", err=True)
            resolved.extend(found)
        return resolved

    def dry_run(self):
        self.adapter.preview(self.name, self.target, self.selected_skills, self.selected_kbs)

    def execute(self):
        self.adapter.install(self.name, self.target, self.selected_skills, self.selected_kbs, self.force)
