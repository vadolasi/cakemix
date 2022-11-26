import os
from tempfile import TemporaryDirectory
from pathlib import Path
from jinja2 import Template

import inquirer
import typer
import yaml
from git import Repo

app = typer.Typer()


def main(cakemix_path: str, output_path: str):
    with TemporaryDirectory() as tempdir:
        Repo.clone_from(cakemix_path, tempdir)

        answers = {}

        cakemix_config = yaml.safe_load(Path(tempdir, "cakemix.yaml").read_text())
        cakemix_args_file_text = Path(tempdir, "args.yaml.j2").read_text()

        for document in cakemix_args_file_text.split("---"):
            inputs = []

            cakemix_args = yaml.safe_load(Template(document).render(answers))

            if cakemix_args is None:
                continue

            for arg in cakemix_args:
                match arg.get("type", "text"):
                    case "text":
                        inputs.append(inquirer.Text(name=arg["name"], message=arg["message"]))
                    case _:
                        raise NotImplementedError

            answers.update(inquirer.prompt(inputs))

        main_path = cakemix_config["main_dir"]

        for _, _, filenames in os.walk(str(Path(tempdir, main_path))):
            for path in filenames:
                file = Path(tempdir, main_path, path)

                try:
                    text = file.read_text()

                    template: Template = Template(text)
                    data = template.render(answers)

                    result = Path(output_path, path)

                    result.parent.mkdir(parents=True, exist_ok=True)
                    result.write_text(data)

                except:
                    continue


if __name__ == "__main__":
    typer.run(main)
