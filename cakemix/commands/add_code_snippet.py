"""Define the "add_code_snippet" command."""

import click
import pyperclip
import questionary
from slugify import slugify

from cakemix.database import CodeSnippet, Database
from cakemix.output import console


@click.command('add_code_snippet')
def add_code_snippet():
    """Add a code snippet."""
    with Database() as database:

        title = questionary.text('Code snippet title').ask()

        code_snippet = database.add(
            CodeSnippet,
            title=title,
            title_slug=slugify(title),
            description=questionary.text('Code snippet description').ask(),
            tags=questionary.text('Code snippet tags').ask(),
        )

        while True:
            code_snippet_text = pyperclip.paste()

            if code_snippet:
                console.print(f'\n{code_snippet}\n')
                if questionary.confirm('Is the above code snippet correct?').ask():
                    code_snippet.code_snippet = code_snippet_text
                    break
            else:
                input(  # noqa: WPS421
                    'Clipboard is empty! Copy the code snippet and press Enter.',
                )

        database.save()
