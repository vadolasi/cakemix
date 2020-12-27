"""Controls the output."""

import logging
import sys
from typing import Any, Callable

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


def run_task(
    running_message: str,
    success_message: str,
    task_function: Callable,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """[summary].

    Args:
        running_message (str): [description]
        success_message (str): [description]
        task_function (Callable): [description]
        args (tuple): [description]
        kwargs (dict): [description]

    Returns:
        Any: [description]
    """
    with console.status(running_message):
        task_result = task_function(*args, **kwargs)

    if task_result[0]:
        exit_with_error(task_result[0])
    else:
        log.info(success_message, extra={'markup': True})

    if len(task_result) > 1:
        return task_result[1]
