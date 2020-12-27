"""Define the "add" command."""

import shutil
from pathlib import Path

import click
import toml

from cakemix.database import Cakemix, Database
from cakemix.output import run_task


def read_cakemix_src(database: Database, cakemix_src: Path):
    """[summary].

    Args:
        database (Database): [description]
        cakemix_src (Path): [description]

    Returns:
        Tuple[Any]: Error and cakemix.
    """
    if not Path(cakemix_src / 'structure.yaml').exists():
        return ('File \"structure.yaml\" not found',)

    if not Path(cakemix_src / 'settings.toml').exists():
        return ('File \"settings.toml\" not found',)

    cakemix = database.add(
        database.cakemix_object,
        database,
        structure=Path(cakemix_src / 'structure.yaml').read_text(),
        **toml.loads(Path(cakemix_src / 'settings.toml').read_text()),
    )

    if not Path(cakemix_src / 'arguments.toml').exists():
        return ('File \"arguments.toml\" not found',)

    arguments = toml.loads(Path(cakemix_src / 'arguments.toml').read_text())

    for argument_name, argument_options in arguments.items():
        cakemix.add_argument(name=argument_name, **argument_options)

    return ('', cakemix)


def read_paths(src_dir: Path, cakemix: Cakemix):
    """[summary].

    Args:
        src_dir (Path): [description]
        cakemix (Cakemix): [description]

    Returns:
        Tuple[any]: Error
    """
    src_len = len(str(src_dir)) + 1

    for path in sorted(src_dir.rglob('*')):
        if path.is_dir():
            cakemix.add_path(
                path=str(path)[src_len:], content_type='directory',
            )
        else:
            try:  # noqa: WPS229
                path.read_text()
                cakemix.add_path(
                    path=str(path)[src_len:], content_type='plain_text',
                )
            except UnicodeDecodeError:
                cakemix.add_path(
                    path=str(path)[
                        src_len:
                    ], content_type='not_plain_text',
                )

    return ('',)


def save_cakemix(src_dir: Path, cakemix: Cakemix, database: Database):
    """Save the cakemix in database and in .cakemix/cakemixes dir.

    Args:
        src_dir (Path): [description]
        cakemix (Cakemix): [description]
        database (Database): [description]

    Returns:
        Tuple[Any]: Error
    """
    shutil.make_archive(
        str(Path.home() / '.cakemix' / 'cakemixes' / cakemix.name),
        'zip',
        src_dir,
    )

    database.save()

    return ('',)


@click.command()
@click.argument('src')
def add(src: str):
    """Add a cakemix.

    Args:
        src (str): Cakemix location.
    """
    src_dir = Path(src)
    cakemix_src = src_dir / '.cakemixsrc'

    with Database() as database:
        cakemix = run_task(
            'Reading .cakemixsrc...',
            '.cakemixsrc',
            read_cakemix_src,
            database,
            cakemix_src,
        )

        run_task(
            'Processing files...', 'Files processed', read_paths, src_dir, cakemix,
        )

        run_task(
            'Saving cakemix...',
            'Cakemix saved',
            save_cakemix,
            src_dir,
            cakemix,
            database,
        )
