import importlib.resources
from pathlib import Path


def _find_resources_dir() -> Path:
    """Find the resources directory, whether running from source or installed."""
    # When installed as a package, 'resources' is a top-level package in the wheel
    try:
        return Path(str(importlib.resources.files("resources")))
    except (ModuleNotFoundError, TypeError):
        pass
    # Fallback: running from source tree
    return Path(__file__).parent.parent.parent / "resources"


RESOURCES_DIR = _find_resources_dir()


class Registry:
    def __init__(self, resources_dir: Path = RESOURCES_DIR):
        self.resources_dir = resources_dir

    def all_skills(self) -> list[Path]:
        skills_dir = self.resources_dir / "skills"
        return sorted(p.parent for p in skills_dir.rglob("SKILL.md"))

    def find_skills(self, name: str) -> list[Path]:
        """Find skills by 'category/name' or just 'name'."""
        parts = name.split("/")
        return [s for s in self.all_skills() if s.name == parts[-1] and (len(parts) == 1 or s.parent.name == parts[0])]

    def all_kbs(self) -> list[Path]:
        kb_dir = self.resources_dir / "knowledge-bases"
        return sorted(d for d in kb_dir.iterdir() if d.is_dir())

    def find_kbs(self, name: str) -> list[Path]:
        kb_dir = self.resources_dir / "knowledge-bases"
        target = kb_dir / name
        return [target] if target.is_dir() else []
