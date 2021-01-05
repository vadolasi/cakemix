"""Doit tasks."""


def task_setup():
    """Setup development environment."""  # noqa: D401
    return {
        'actions': [
            'python -m pip install --upgrade pip setuptools wheel',
            'pip install poetry',
            'poetry install',
            'poetry run pre-commit install',
            'poetry run pre-commit run --all-files',
        ],
    }


def task_auto_format():
    """Auto format files."""
    return {
        'actions': [
            'pyformat --in-place cakemix/**/*.py tests/*.py',
            'autoflake --in-place cakemix/**/*.py tests/*.py',
            'isort cakemix/**/*.py tests/*.py',
            'add-trailing-comma cakemix/**/*.py tests/*.py',
        ],
    }


def task_lint():
    """Lint files and check dependencies."""
    return {
        'actions': [
            'safety check',
            'flakehell lint',
            'mypy .',
        ],
    }


def task_test():
    """Run tests."""
    return {
        'actions': ['pytest'],
    }


def task_codecov():
    """Run codecov."""
    return {
        'actions': ['pytest --cov=cakemix --cov-report=xml'],
    }
