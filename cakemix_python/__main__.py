"""Run the Cakemix."""

from importlib.metadata import entry_points

cakemix = list(
    filter(
        lambda entry_point: entry_point.name == 'cakemix',
        entry_points()['console_scripts'],
    ),
)[0]

cakemix.load()()
