"""Run the CLI."""

from pathlib import Path

import click

from cakemix.commands import add, remove, run


@click.group()
def cli():
    """Init the CLI."""
    cakemix_data_dir = Path.home() / '.cakemix'
    cakemixes_dir = cakemix_data_dir / 'cakemixes'

    if not cakemix_data_dir.exists():
        cakemix_data_dir.mkdir()

    if not cakemixes_dir.exists():
        cakemixes_dir.mkdir()


cli.add_command(add.add)
cli.add_command(remove.remove)
cli.add_command(run.run)
