import click

from ..prototyping import prototyping


@click.group()
def main() -> None:
    pass


main.add_command(prototyping)
