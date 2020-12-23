"""Run the CLI."""

from pathlib import Path

import click
import toml


@click.group()
def cli():
    """Init the CLI."""


@cli.command()
@click.argument('src')
@click.argument('dst')
def add(src: Path, dst: Path):  # noqa: WPS210
    """Add a cakemix.

    Args:
        src (Path): Cakemix location.
        dst (Path): Output dir.
    """
    src = Path(src)
    dst = Path(dst)

    settings_path = src / '.cakemixsrc/settings.toml'
    arguments_path = src / '.cakemixsrc/arguments.toml'

    with settings_path.open() as settings_file:
        click.echo(toml.loads(settings_file.read()))

    with arguments_path.open() as arguments_file:
        click.echo(toml.loads(arguments_file.read()))

    click.echo(dst)


@cli.command()
def remove():
    """Remove a cakemix."""


@cli.command()
def run():
    """Run a cakemix."""
