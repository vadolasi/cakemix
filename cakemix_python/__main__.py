"""Run the Cakemix."""

from importlib.metadata import entry_points

entry_points()['console_scripts'][0].load()
