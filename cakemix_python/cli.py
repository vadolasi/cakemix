"""Run the CLI."""
import click


@click.group()
def cli():
    """Init the CLI."""


@cli.command()
def add():
    """Add a cakemix."""


@cli.command()
def remove():
    """Remove a cakemix."""


@cli.command()
def run():
    """Run a cakemix."""
