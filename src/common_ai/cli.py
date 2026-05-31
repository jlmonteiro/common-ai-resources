import click

from common_ai.installer import Installer


@click.group()
def main():
    """Common AI Resources - multi-tool adapter CLI."""


@main.command()
@click.option("--tool", type=click.Choice(["kiro", "claude", "gemini"]), required=True, help="Target AI tool.")
@click.option("--name", required=True, help="Agent name.")
@click.option("--target", type=click.Path(), required=True, help="Installation directory.")
@click.option("--skills", multiple=True, help="Skills to install (category/name or 'all').")
@click.option("--knowledge-bases", "kbs", multiple=True, help="Knowledge bases to install (scope or 'all').")
@click.option("--dry-run", is_flag=True, help="Preview what would be installed without writing files.")
def install(tool, name, target, skills, kbs, dry_run):
    """Install skills and knowledge bases to target tool's location."""
    installer = Installer(tool=tool, name=name, target=target, skills=list(skills), kbs=list(kbs))
    if dry_run:
        installer.dry_run()
    else:
        installer.execute()


if __name__ == "__main__":
    main()
