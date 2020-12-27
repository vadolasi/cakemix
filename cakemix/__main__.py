"""Run the Cakemix."""

import importlib
import sys
from typing import Any

if sys.version_info.minor >= 8:
    module_name = 'importlib.metadata'
else:
    module_name = 'importlib_metadata'

importlib_metadata: Any = importlib.import_module(module_name)

cakemix = list(
    filter(
        lambda entry_point: entry_point.name == 'cakemix',
        importlib_metadata.entry_points()['console_scripts'],
    ),
)[0]

cakemix.load()()
