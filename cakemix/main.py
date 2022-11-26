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
    os.chdir("../")

    with TemporaryDirectory() as tempdir:
        Repo.clone_from(cakemix_path, tempdir)

        answers = {}

        cakemix_config = yaml.safe_load(Path(tempdir, "config.yaml").read_text())
        cakemix_args_file_text = Path(tempdir, "args.yaml.j2").read_text()

        for document in cakemix_args_file_text.split("---"):
            inputs = []

            cakemix_args = yaml.safe_load(Template(document).render(cakemix=answers))

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

        for _, dirs, filenames in os.walk(str(Path(tempdir, main_path))):
            Path(output_path).mkdir(parents=True, exist_ok=True)

            for directory in dirs:
                Path(output_path, directory).mkdir(parents=True, exist_ok=True)

            for path in filenames:
                file = Path(tempdir, main_path, path)

                try:
                    text = file.read_text()

                    template: Template = Template(text)
                    data = template.render(cakemix=answers)

                    result = Path(output_path, path)
                    result.write_text(data)

                except:
                    result = Path(output_path, path)

                    result.write_bytes(file.read_bytes())


def run():
    typer.run(main)