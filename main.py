from tempfile import TemporaryDirectory
from pathlib import Path
from jinja2 import Template

import typer
from git import Repo

app = typer.Typer()


def list_paths(root_tree, path=Path(".")):
    for blob in root_tree.blobs:
        yield path / blob.name
    for tree in root_tree.trees:
        yield from list_paths(tree, path / tree.name)


def main(cakemix_path: str, output_path: str):
    with TemporaryDirectory() as tempdir:
        repo = Repo.clone_from(cakemix_path, tempdir)

        commit = repo.head.commit

        for path in list_paths(commit.tree):
            file = Path(tempdir, path)

            try:
                text = file.read_text()

                template: Template = Template(text)
                data = template.render({ "a": "b" })

                result = Path(output_path, path)

                result.parent.mkdir(parents=True, exist_ok=True)
                result.write_text(data)

            except:
                continue


if __name__ == "__main__":
    typer.run(main)
