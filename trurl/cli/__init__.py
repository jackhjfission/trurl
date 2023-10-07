import click

from .. import __version__
from .environment import conda_compare, conda_export, conda_update


@click.group()
def main() -> None:
    pass


@main.command()
def version() -> None:
    """Outputs the installed version of trurl."""
    print(f"trurl=={__version__}")


main.command(conda_export)
main.command(conda_update)
main.command(conda_compare)
