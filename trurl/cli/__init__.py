import click

from .. import __version__


@click.group()
def main() -> None:
    pass


@main.command()
def version() -> None:
    """Outputs the installed version of trurl."""
    print(f"trurl=={__version__}")
