==============
Cakemix :cake:
==============

|license| |tests| |codecov| |style wemake| |Gitpod ready to code| |chat|

English | Português_

Cakemix is a tool for creating code template generators like :code:`create-react-app` and :code:`npm init`. Avoiding you to waste time organizing a project.

Features :sparkles:
===================

Install :floppy_disk:
========================

Cakemix uses PyOxidizer_ to generate the executables. You can see how to install it below:

Windows
-------

Cakemix can be installed on Windows through Chocolatey_:

.. code-block:: python

   choco install cakemix

You can also get the executable_.

MacOS and Linux
-------------

Cakemix can be installed on MacOS or Linux via Homebrew_:

.. code-block:: python

   brew install cakemix

You can also get the executable for MacOS_ and Linux_.

Python
------

You can also install Cakemix on any machine with Python 3.6.1+ via pip:

.. code-block:: python

   pip install cakemix-python

Quickstart :rocket:
======================

This is just a basic tutorial to show what Cakemix is capable of. For something more complete, see the documentation_.

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

Contributors :busts_in_silhouette:
====================================

This project was created and is maintained by @vadolasi.

If you wish to become a contributor, see the `Contribution Guidelines`_.

License :scroll:
================

`GNU General Public License v3.0 (GPL-3)`_

Author :bust_in_silhouette:
===========================

.. links

.. _Português: ./locales/pt-br/README.rst
.. _PyOxidizer: https://pyoxidizer.readthedocs.io/en/stable/
.. _Chocolatey: https://chocolatey.org/
.. _executable: https://google.com/
.. _Homebrew: https://brew.sh/
.. _MacOS: https://google.com/
.. _Linux: https://google.com/
.. _documentation: https://google.com/
.. _`Contribution Guidelines`: CONTRIBUTING.rst
.. _`GNU General Public License v3.0 (GPL-3)`: https://choosealicense.com/licenses/gpl-3.0/

.. imagens

.. |license| image:: https://img.shields.io/github/license/vadolasi/cakemix?label=licen%C3%A7a
   :alt: This project uses the GPL-3 license
   :target: https://choosealicense.com/licenses/gpl-3.0/

.. |tests| image:: https://img.shields.io/github/workflow/status/vadolasi/cakemix/Python%20package?label=testes&logo=Github
   :alt: Tests status
   :target: https://github.com/vadolasi/cakemix/actions?query=workflow%3A%22Python+package%22

.. |codecov| image:: https://codecov.io/gh/vadolasi/cakemix/branch/master/graphs/badge.svg?branch=master
   :alt: Code corverage status

.. |style wemake| image:: https://img.shields.io/badge/estilo-wemake-black
   :alt: Python Wemake styleguide
   :target: https://wemake-python-stylegui.de/

.. |Gitpod ready to code| image:: https://img.shields.io/badge/Gitpod-pronto--para--codificar-blue?logo=gitpod
   :alt: Open in Gitpod.io
   :target: https://gitpod.io/#https://github.com/vadolasi/cakemix/

.. |chat| image:: https://img.shields.io/discord/773328172065488916?logo=Discord
   :alt: Cakemix Community on Discord
   :target: https://discord.com/channels/773328172065488916/
