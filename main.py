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

        inputs = []

        cakemix_config = yaml.safe_load(Path(tempdir, "cakemix.yaml").read_text())
        main_path = cakemix_config["main_dir"]

        for arg in cakemix_config["args"]:
            match arg["type"]:
                case "text":
                    inputs.append(inquirer.Text(name=arg["name"], message=arg["message"]))

        answers = inquirer.prompt(inputs)

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
