"""Define the "remove" command."""

import os
from pathlib import Path

import click

from cakemix.database import Cakemix, Database
from cakemix.output import Task, exit_with_error


def delete_cakemix(database: Database, cakemix_name: str):
    """[summary].

    Args:
        database (Database): [description]
        cakemix_name (str): [description]
    """
    cakemix = database.query(Cakemix).filter(Cakemix.name == cakemix_name)

    if cakemix:
        cakemix.delete()
        database.save()
        os.remove(
            Path.home() / '.cakemix' / 'cakemixes' / f'{cakemix_name}.zip',
        )
    else:
        exit_with_error(f'Cakemix \"{cakemix_name}\" not found')


@click.command('remove')
@click.argument('cakemix_name')
def remove(cakemix_name: str):
    """Remove a cakemix.

    Args:
        cakemix_name (str): [description]
    """
    with Database() as database:
        with Task('Deleting cakemix...', f'Cakemix \"{cakemix_name}\" deleted'):
            delete_cakemix(database, cakemix_name)
