from abc import ABC, abstractmethod
from pathlib import Path


class BaseAdapter(ABC):
    @abstractmethod
    def preview(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> None:
        """Print dry-run preview of what would be installed."""

    @abstractmethod
    def install(self, name: str, target: Path, skills: list[Path], kbs: list[Path]) -> None:
        """Install resources to target directory."""
