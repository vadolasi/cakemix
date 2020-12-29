"""Define the "run" command."""

import click
from rich import box
from rich.console import Console
from rich.table import Table

from cakemix.database import Cakemix, Database


@click.command('list')
def list_cakemixes():
    """List the cakemixes."""
    console = Console()

    table = Table(
        show_header=True, header_style='bold green', box=box.HORIZONTALS,
    )
    table.add_column('Name')
    table.add_column('Description')
    table.add_column('Author')

    with Database() as database:
        for cakemix_object in database.query(Cakemix).all():
            table.add_row(
                cakemix_object.name, cakemix_object.description, cakemix_object.author,
            )

    console.print(table)
