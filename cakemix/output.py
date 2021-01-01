"""Controls the output."""

import logging
import sys
from typing import Any

from rich.console import Console
from rich.logging import RichHandler

console = Console()


FORMAT = '%(message)s'
logging.basicConfig(
    level='NOTSET',
    format=FORMAT,
    datefmt='[%X]',
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger('rich')


def exit_with_error(message: str):
    """Show a error message and finish execution.

    Args:
        message (str): Error message.
    """
    log.error(message, extra={'markup': True})
    sys.exit(1)


class Task(object):
    """Run task while show rich status."""

    def __init__(
        self, running_message: str, success_message: str, *args: Any, **kwargs: Any,
    ):
        """Create the status object.

        Args:
            running_message (str): [description]
            success_message (str): [description]
            args (Any): [description]
            kwargs (Any): [description]
        """
        self.success_message = success_message
        self.status = console.status(running_message, *args, **kwargs)

    def __enter__(self):
        """Start the task."""
        self.status.start()

    def __exit__(self, exception_type, exception_value, traceback):
        """Close the task.

        Args:
            exception_type ([type]): [description]
            exception_value ([type]): [description]
            traceback ([type]): [description]
        """
        if exception_type != SystemExit:
            self.status.stop()
            console.log(self.success_message)
