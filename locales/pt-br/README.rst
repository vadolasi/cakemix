==============
Cakemix :cake:
==============

|licença| |testes| |codecov| |estilo wemake| |Gitpod pronto para codificar| |chat|

English_ | Português

Cakemix é uma ferramenta para criar geradores de templates de código como :code:`create-react-app` e :code:`npm init`. Evitando que você perca tempo organizando um projeto.

Features :sparkles:
===================

Instalação :floppy_disk:
========================

Cakemix utiliza PyOxidizer_ para gerar os executáveis. Você pode ver como instala-lo abaixo:

Windows
-------

O Cakemix pode ser instalado no Windows através do Chocolatey_:

.. code-block:: python

   choco install cakemix

Você também pode obter o exécutavel_.

MacOS e Linux
-------------

O Cakemix pode ser instalado no MacOS ou Linux através do Homebrew_:

.. code-block:: python

   brew install cakemix

Você também pode obter o executável para MacOS_ e Linux_.

Python
------

Você também pode instalar o Cakemix em qualquer máquina com Python 3.6.1+  através do pip:

.. code-block:: python

   pip install cakemix-python

Começo rápido :rocket:
======================

Esta é apenas um tutorial básico para mostrar o que o Cakemix é capaz de fazer. Para algo mais completo, veja a documentação_.

.. code-block:: python

   # cakemix_project/versions/python2.py

   def main():
       print "Executando Python 2"
       print "{{ message }}"

.. code-block:: python

   # cakemix_project/versions/python3.py

   def main():
       print("Executando Python 3")
       print("{{ message }}")

.. code-block:: python

   # cakemix_project/main.py

   from python{{ python_version }} import main

   if __name__ == "__main__":
       main()

.. code-block:: yaml

   # cakemix_project/.cakemixsrc/structure.yaml

   - {{ project_name }} @contents=["self", "versions"]:
       - python{{ python_version }}.py
       - {{ project_name }}.py @content="main.py"

Contribuidores :busts_in_silhouette:
====================================

Este projeto foi criado e é mantido por @vadolasi.

Se você deseja se torna um contribuidor, veja o `Guia de Contribuição`_.

Licença :scroll:
================

`GNU General Public License v3.0 (GPL-3)`_

Autor :bust_in_silhouette:
==========================

.. links

.. _English: ../../README.rst
.. _PyOxidizer: https://pyoxidizer.readthedocs.io/en/stable/
.. _Chocolatey: https://chocolatey.org/
.. _exécutavel: https://google.com/
.. _Homebrew: https://brew.sh/
.. _MacOS: https://google.com/
.. _Linux: https://google.com/
.. _documentação: https://google.com/
.. _`Guia de Contribuição`: CONTRIBUTING.rst
.. _`GNU General Public License v3.0 (GPL-3)`: https://choosealicense.com/licenses/gpl-3.0/

.. imagens

.. |licença| image:: https://img.shields.io/github/license/vadolasi/cakemix?label=licen%C3%A7a
   :alt: Este projeto utiliza a licença GPL-3
   :target: https://choosealicense.com/licenses/gpl-3.0/

.. |testes| image:: https://img.shields.io/github/workflow/status/vadolasi/cakemix/Python%20package?label=testes&logo=Github
   :alt: Status dos testes
   :target: https://github.com/vadolasi/cakemix/actions?query=workflow%3A%22Python+package%22

.. |codecov| image:: https://codecov.io/gh/vadolasi/cakemix/branch/master/graphs/badge.svg?branch=master
   :alt: Status do code corverage

.. |estilo wemake| image:: https://img.shields.io/badge/estilo-wemake-black
   :alt: Guia de estilo Wemake para Python
   :target: https://wemake-python-stylegui.de/

.. |Gitpod pronto para codificar| image:: https://img.shields.io/badge/Gitpod-pronto--para--codificar-blue?logo=gitpod
   :alt: Abrir em Gitpod.io
   :target: https://gitpod.io/#https://github.com/vadolasi/cakemix/

.. |chat| image:: https://img.shields.io/discord/773328172065488916?logo=Discord
   :alt: Comunidade do Cakemix no Discord
   :target: https://discord.com/channels/773328172065488916/
