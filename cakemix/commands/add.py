"""Define the "add" command."""

import shutil
from pathlib import Path

import click
import toml
from binaryornot.check import is_binary

from cakemix.database import Cakemix, Database
from cakemix.output import Task, exit_with_error


def read_cakemix_src(database: Database, cakemix_src: Path):
    """[summary].

    Args:
        database (Database): [description]
        cakemix_src (Path): [description]

    Returns:
        Tuple[Any]: Error and cakemix.
    """
    if not (cakemix_src / 'structure.yaml').exists():
        exit_with_error('File \"structure.yaml\" not found')

    if not (cakemix_src / 'settings.toml').exists():
        exit_with_error('File \"settings.toml\" not found')

    cakemix = database.add(
        Cakemix,
        database,
        structure=Path(cakemix_src / 'structure.yaml').read_text(),
        **toml.loads(Path(cakemix_src / 'settings.toml').read_text()),
    )

    if not (cakemix_src / 'parameters.toml').exists():
        exit_with_error('File \"parameters.toml\" not found')

    parameters = toml.loads(  # noqa: WPS110
        Path(cakemix_src / 'parameters.toml').read_text(),
    )

    for parameter_name, parameter_options in parameters.items():
        cakemix.add_parameter(name=parameter_name, **parameter_options)

    return cakemix


def read_paths(src_dir: Path, cakemix: Cakemix):
    """[summary].

    Args:
        src_dir (Path): [description]
        cakemix (Cakemix): [description]
    """
    src_len = len(str(src_dir)) + 1

    for path in sorted(src_dir.rglob('*')):
        path_str = str(path)[src_len:]
        if not path_str.startswith('.cakemixsrc'):
            if path.is_dir():
                cakemix.add_path(path=path_str, content_type='directory')
            elif is_binary(str(path)):
                cakemix.add_path(path=path_str, content_type='not_plain_text')
            else:
                cakemix.add_path(path=path_str, content_type='plain_text')


def save_cakemix(src_dir: Path, cakemix: Cakemix, database: Database):
    """Save the cakemix in database and in .cakemix/cakemixes dir.

    Args:
        src_dir (Path): [description]
        cakemix (Cakemix): [description]
        database (Database): [description]
    """
    shutil.make_archive(
        str(Path.home() / '.cakemix' / 'cakemixes' / cakemix.name),
        'zip',
        src_dir,
    )

    database.save()


@click.command('add')
@click.argument('src')
def add(src: str):
    """Add a cakemix.

    Args:
        src (str): Cakemix location.
    """
    src_dir = Path(src)

    if not src_dir.exists():
        exit_with_error(f'directory \"{src_dir}\" not found')
    elif not src_dir.is_dir():
        exit_with_error(f'\"{src_dir}\" is not a directory')

    cakemix_src = src_dir / '.cakemixsrc'

    with Database() as database:
        with Task('Reading cakemix options...', 'Cakemix options read'):
            cakemix = read_cakemix_src(database, cakemix_src)

        with Task('Processing files...', 'Files processed'):
            read_paths(src_dir, cakemix)

        with Task('Saving cakemix...', f'Cakemix \"{cakemix.name}\" saved'):
            save_cakemix(src_dir, cakemix, database)
