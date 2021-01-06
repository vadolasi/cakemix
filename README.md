# Cakemix :cake:

[![This project uses the GPL-3 license](https://img.shields.io/github/license/vadolasi/cakemix?label=licen%C3%A7a)](https://choosealicense.com/licenses/gpl-3.0/)
[![Tests status](https://img.shields.io/github/workflow/status/vadolasi/cakemix/Python%20package?label=tests&logo=Github)](https://github.com/vadolasi/cakemix/actions?query=workflow%3A%22Python+package%22)
[![Site status](https://img.shields.io/netlify/980e9474-f069-467f-958d-9c215ae3de92?logo=netlify)](https://cakemix.tk/pt/)
[![Code coverage status](https://codecov.io/gh/vadolasi/cakemix/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/vadolasi/cakemix/branch/master/graphs/badge.svg?branch=master)
[![Python Wemake styleguide](https://img.shields.io/badge/style-wemake-black)](https://wemake-python-stylegui.de/)
[![Gitpod ready to code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/vadolasi/cakemix/)
[![Cakemix's Discord server](https://img.shields.io/discord/773328172065488916?logo=Discord)](https://discord.com/channels/773328172065488916/)

English | [Português](./locales/pt-br/README.md)

Cakemix is a tool for creating code template generators like `create-react-app` and `npm init`. Avoiding you to waste time organizing a project.

## Features :sparkles:

## Install :floppy_disk:

Cakemix uses [PyOxidizer](https://pyoxidizer.readthedocs.io/en/stable/) to generate the executables. You can see how to install it below:

### Windows

Cakemix can be installed on Windows through [Chocolatey](https://chocolatey.org/):

``` bash
choco install cakemix
```

You can also get the [executable](https://google.com/).

### MacOS and Linux

Cakemix can be installed on MacOS or Linux via [Homebrew](https://brew.sh/):

``` bash
brew install cakemix
```

You can also get the executable for [MacOS](https://google.com/) and [Linux](https://google.com/).

### Python

You can also install Cakemix on any machine with Python 3.6.1+ via pip:

``` bash
pip install cakemix-python
```

## Quickstart :rocket:

This is just a basic tutorial to show what Cakemix is capable of. For something more complete, see the [documentation](https://cakemix.tk/guide/usage.html).

``` text
# cakemix_project/versions/python2.py

def main():
    print "Hello from Python 2"
    print "{{ message }}"
```

``` text
# cakemix_project/versions/python3.py

def main():
    print("Hello from Python 3")
    print("{{ message }}")
```

``` text
# cakemix_project/main.py

from python{{ python_version }} import main

if __name__ == "__main__":
    main()
```

``` text
# cakemix_project/.cakemixsrc/structure.yaml

- {{ project_name }}:
    - python{{ python_version }}.py
    - {{ project_name }}.py
```

## Contributors :busts_in_silhouette:

This project was created and is maintained by [Vitor Daniel](https://github.com/vadolasi/).

If you wish to become a contributor, see the [Contribution Guidelines](CONTRIBUTING.md).

## License :scroll:

[GNU General Public License v3.0 (GPL-3)](https://choosealicense.com/licenses/gpl-3.0/)
