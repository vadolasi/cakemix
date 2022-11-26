import os
from tempfile import TemporaryDirectory
from pathlib import Path
from jinja2 import Template

import inquirer
import typer
import yaml
from git import Repo

app = typer.Typer()


@app.command()
def main(cakemix_path: str, output_path: Path = "."):
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
                        inputs.append(inquirer.Text(name=arg["name"], message=arg["message"], default=arg.get("default", None)))
                    case "list":
                        inputs.append(inquirer.List(name=arg["name"], message=arg["message"], choices=arg["choices"], default=arg.get("default", None)))
                    case "confirm":
                        inputs.append(inquirer.Confirm(name=arg["name"], message=arg["message"], default=arg.get("default", None)))
                    case "password":
                        inputs.append(inquirer.Password(name=arg["name"], message=arg["message"], default=arg.get("default", None)))
                    case "path":
                        inputs.append(inquirer.Path(name=arg["name"], message=arg["message"], default=arg.get("default", None)))
                    case "editor":
                        inputs.append(inquirer.Editor(name=arg["name"], message=arg["message"], default=arg.get("default", None)))
                    case "checkbox":
                        inputs.append(inquirer.Checkbox(name=arg["name"], message=arg["message"], choices=arg["choices"], default=arg.get("default", None)))
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

                    path_result = Template(path).render(cakemix=answers)

                    result = Path(output_path, path_result)
                    result.write_text(data)

                except:
                    path_result = Template(path).render(cakemix=answers)

                    result = Path(output_path, path_result)

                    result.write_bytes(file.read_bytes())

        files_actions_file = Path(tempdir, "files.yaml.j2")

        if files_actions_file.exists():
            files_actions = yaml.safe_load(Template(files_actions_file.read_text()).render(cakemix=answers))

            for action in files_actions:
                match action["command"]:
                    case "copy":
                        Path(
                            output_path,
                            Template(action["to"]).render(cakemix=answers)
                        ).write_bytes(
                            Path(
                                output_path,
                                Template(action["from"]).render(cakemix=answers)
                            ).read_bytes()
                        )
                    case "move":
                        Path(
                            output_path,
                            Template(action["to"]).render(cakemix=answers)
                        ).write_bytes(
                            Path(
                                output_path,
                                Template(action["from"]).render(cakemix=answers)
                            ).read_bytes()
                        )
                        Path(
                            output_path,
                            Template(action["from"]).render(cakemix=answers)
                        ).unlink()
                    case "delete":
                        Path(
                            output_path,
                            Template(action["path"]).render(cakemix=answers)
                        ).unlink()


if __name__ == "__main__":
    app()
