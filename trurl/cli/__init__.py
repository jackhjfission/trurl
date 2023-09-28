import click


@click.group()
def main() -> None:
    pass


@main.command()
def initdb() -> None:
    click.echo("Initialized the database")


@main.command()
def dropdb() -> None:
    click.echo("Dropped the database")
