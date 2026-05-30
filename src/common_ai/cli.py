import click


@click.group()
def main():
    """Common AI Resources - multi-tool adapter CLI."""


@main.command()
@click.option("--target", type=click.Choice(["kiro", "claude-code", "gemini"]), required=True)
@click.option("--agent", help="Agent name to generate (all if omitted)")
def generate(target, agent):
    """Generate tool-specific configs from canonical definitions."""
    click.echo(f"Generating for {target}" + (f" (agent: {agent})" if agent else ""))


@main.command()
@click.option("--target", type=click.Choice(["kiro", "claude-code", "gemini"]), required=True)
def install(target):
    """Install generated configs to target tool's location."""
    click.echo(f"Installing to {target}")


if __name__ == "__main__":
    main()
