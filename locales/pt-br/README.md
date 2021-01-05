# Cakemix :cake:

[![This project uses the GPL-3 license](https://img.shields.io/github/license/vadolasi/cakemix?label=licen%C3%A7a)](https://choosealicense.com/licenses/gpl-3.0/)
[![Tests status](https://img.shields.io/github/workflow/status/vadolasi/cakemix/Python%20package?label=tests&logo=Github)](https://github.com/vadolasi/cakemix/actions?query=workflow%3A%22Python+package%22)
[![Code coverage status](https://codecov.io/gh/vadolasi/cakemix/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/vadolasi/cakemix/branch/master/graphs/badge.svg?branch=master)
[![Python Wemake styleguide](https://img.shields.io/badge/style-wemake-black)](https://wemake-python-stylegui.de/)
[![Gitpod ready to code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/vadolasi/cakemix/)
[![Cakemix's Discord server](https://img.shields.io/discord/773328172065488916?logo=Discord)](https://discord.com/channels/773328172065488916/)

[English](../../README.md) | Português

Cakemix é uma ferramenta para criar geradores de templates de código como `create-react-app` e `npm init`. Evitando que você perca tempo organizando um projeto.

## Features :sparkles:

## Install :floppy_disk:

Cakemix utiliza [PyOxidizer](https://pyoxidizer.readthedocs.io/en/stable/) para gerar os executáveis. Você pode ver como instala-lo abaixo:

### Windows

O Cakemix pode ser instalado no Windows através do [Chocolatey](https://chocolatey.org/):

``` bash
choco install cakemix
```

Você também pode obter o [executable](https://google.com/).

### MacOS and Linux

O Cakemix pode ser instalado no MacOS ou Linux através do [Homebrew](https://brew.sh/index_pt-br):

``` bash
brew install cakemix
```

Você também pode obter o executável para [MacOS](https://google.com/) e [Linux](https://google.com/).

### Python

Você também pode instalar o Cakemix em qualquer máquina com Python 3.6.1+  através do pip:

``` bash
pip install cakemix-python
```

## Quickstart :rocket:

Esta é apenas um tutorial básico para mostrar o que o Cakemix é capaz de fazer. Para algo mais completo, veja a [documentação](https://cakemix.tk/pt/docs/começo-rápido/visão-geral).

``` text
# cakemix_project/versions/python2.py

def main():
    print "Executando Python 2"
    print "{{ message }}"
```

``` text
# cakemix_project/versions/python3.py

def main():
    print("Executando Python 3")
    print("{{ message }}")
```

``` texr
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

Este projeto foi criado e é mantido por [Vitor Daniel](https://github.com/vadolasi/).

Se você deseja se torna um contribuidor, veja o [Guia de Contribuição](CONTRIBUTING.md).

## License :scroll:

[GNU General Public License v3.0 (GPL-3)](https://choosealicense.com/licenses/gpl-3.0/)
