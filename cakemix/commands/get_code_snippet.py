"""Define the "get_code_snippet" command."""

import click
import pyperclip

from cakemix.database import CodeSnippet, Database
from cakemix.output import console, exit_with_error


@click.command('get_code_snippet')
@click.argument('title')
def get_code_snippet(title: str):
    """Get a code snippet.

    Args:
        title (str): The code snippet title
    """
    with Database() as database:
        code_snippet = database.query(CodeSnippet).get({'title_slug': title})

        if not code_snippet:
            exit_with_error(f'Code snippet \"{title}\" not found')

        pyperclip.copy(code_snippet.code_snippet)

    console.print('Code snippet copied to clipboard')
