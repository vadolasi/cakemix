"""Run the Cakemix."""

try:
    from importlib import metadata
except ModuleNotFoundError:
    import importlib_metadata as metadata  # type: ignore

cakemix = list(
    filter(
        lambda entry_point: entry_point.name == 'cakemix',
        metadata.entry_points()['console_scripts'],
    ),
)[0]

cakemix.load()()
