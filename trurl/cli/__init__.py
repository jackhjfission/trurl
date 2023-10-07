__version__ = "v0.1.2"

import click

from .environment import conda_export, conda_update


@click.group()
def main() -> None:
    pass


@main.command()
def version() -> None:
    """Outputs the installed version of trurl."""
    print(f"trurl=={__version__}")


main.command(conda_export)
main.command(conda_update)
