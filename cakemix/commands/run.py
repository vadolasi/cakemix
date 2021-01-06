"""Define the "run" command."""

import argparse
import tempfile
import zipfile
from pathlib import Path

import click
import click_pathlib
import questionary
import yaml
from jinja2 import Template

from cakemix.database import Cakemix, Database, ParameterTable, PathTable
from cakemix.output import Task


def resolve_structure(directory: Path, path_content: list) -> list:
    """Convert content of ".cakemix/structure.yaml" in list of paths.

    Args:
        directory (Path): [description]
        path_content (list): [description]

    Returns:
        list: list of paths
    """
    paths = []

    if path_content:
        for path in path_content:
            if isinstance(path, dict):
                path_root = list(path.keys())[0]
                path_content = list(path.values())[0]
                paths.extend(
                    resolve_structure(
                        directory / path_root, path_content,
                    ),
                )
                continue
            else:
                paths.append(directory / path)
    else:
        paths.append(directory)

    return paths


def refactor_argument(key, value, database, cakemix):  # noqa: WPS110
    """Convert options and flags to parameter name.

    Args:
        key ([type]): [description]
        value ([type]): [description]
        database ([type]): [description]
        cakemix ([type]): [description]

    Returns:
        [type]: [description]
    """
    key = key.replace('--', '')

    if key.startswith('-'):
        argument = database.query(ParameterTable).filter(
            ParameterTable.cakemix == cakemix, ParameterTable.abbreviation == key[1:],
        ).first()

        key = argument.name

    return (key, value)


def ask_questions(arguments: dict, parameters):  # noqa: WPS110
    """[summary].

    Args:
        arguments (dict): [description]
        parameters ([type]): [description]

    Returns:
        [type]: [description]
    """
    for argument, parameter in zip(arguments.items(), parameters):  # noqa: WPS110
        key, value = argument  # noqa: WPS110
        if parameter.only != 'argument' and not value:
            if parameter.input_type == 'text':
                arguments[key] = questionary.text(parameter.ask).ask()
            elif parameter.input_type == 'boolean':
                arguments[key] = questionary.confirm(parameter.ask).ask()

    return arguments


def read_arguments(
    database: Database, cakemix: Cakemix, args: tuple,  # noqa: WPS110
):
    """Read the arguments.

    Args:
        database (Database): [description]
        cakemix (Cakemix): [description]
        args (tuple): [description]

    Returns:
        [type]: [description]
    """
    parameters = database.query(ParameterTable).filter(  # noqa: WPS110
        ParameterTable.cakemix == cakemix,
    )
    parser = argparse.ArgumentParser(
        description=cakemix.description, allow_abbrev=False,
    )

    for parameter in parameters:
        if parameter.only != 'question':
            parameter_names = [parameter.name]

            kwargs = {
                'name_or_flags': parameter.name,
                'help': parameter.help_message,
            }

            if parameter.parameter_type == 'option':
                kwargs['name_or_flags'] = [
                    f'--{parameter_names[0]}', f'-{parameter.abbreviation}',
                ]
                kwargs['action'] = 'store' if bool(
                    parameter.default,
                ) else 'store_false'

            parser.add_argument()

            parser.add_argument(**kwargs)

    return ask_questions(vars(parser.parse_args(args)), parameters)  # noqa: WPS421


def write_files(  # noqa: WPS211
    database: Database,
    cakemix: Cakemix,
    structure_paths: list,
    dst: Path,
    temp_dir: Path,
    arguments: dict,
):
    """[summary].

    Args:
        database (Database): [description]
        cakemix (Cakemix): [description]
        structure_paths (list): [description]
        dst (Path): [description]
        temp_dir (Path): [description]
        arguments (dict): [description]
    """
    paths = database.query(PathTable).filter(PathTable.cakemix == cakemix)

    for path in structure_paths:
        path_object = paths.filter(
            PathTable.cakemix == cakemix, PathTable.path == str(
                path,
            ),
        ).first()

        if path_object.content_type == 'directory':
            (dst / path).mkdir(parents=True, exist_ok=True)
        elif path_object.content_type == 'not_plain_text':
            (dst / path.parent).mkdir(parents=True, exist_ok=True)
            (dst / path).write_bytes((temp_dir / path).read_bytes())
        else:
            (dst / path.parent).mkdir(parents=True, exist_ok=True)
            path_template = Template((temp_dir / path).read_text())
            (dst / path).write_text(path_template.render(**arguments))


@click.command('run')
@click.argument('cakemix_name')
@click.argument('dst', type=click_pathlib.Path())
@click.argument('args', nargs=-1)
def run(cakemix_name: str, dst: Path, args: tuple):  # noqa: WPS210
    """Run a cakemix.

    Args:
        cakemix_name (str): [description]
        dst (Path): [description]
        args (tuple): [description]
    """
    cakemix_content = Path(
        Path.home(), '.cakemix', 'cakemixes', f'{cakemix_name}.zip',
    )

    with Database() as database:
        cakemix = database.query(Cakemix).get({'name_slug': cakemix_name})

        with Task('Reading arguments...', 'Arguments read'):
            arguments = read_arguments(database, cakemix, args)

        with zipfile.ZipFile(cakemix_content, 'r') as zip_ref:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_ref.extractall(temp_dir)

                with Task('Reading structure...', 'Structure read'):
                    structure_paths = resolve_structure(
                        Path('./'),
                        yaml.full_load(
                            Template(cakemix.structure).render(**arguments),
                        ),
                    )

                with Task('Writing files...', 'Files write'):
                    write_files(
                        database,
                        cakemix,
                        structure_paths,
                        dst,
                        Path(temp_dir),
                        arguments,
                    )
