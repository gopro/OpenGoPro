"""Nox sessions."""

from pathlib import Path
from typing import Any

import nox
from nox_poetry import session

PYTHON_VERSIONS = ["3.8"]

package = "open_gopro"
nox.options.sessions = "format", "lint", "tests", "docstrings", "docs", "safety"
locations = "open_gopro", "tests", "noxfile.py", "docs/conf.py"


@session(python=PYTHON_VERSIONS)
def format(session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=PYTHON_VERSIONS)
def lint(session) -> None:
    """Lint using flake8."""
    session.install(".")
    session.install(
        "pylint",
        "mypy",
        "types-requests",
        "construct-typing",
    )
    session.run("mypy", "open_gopro")
    session.run("pylint", "open_gopro")


@session(python=PYTHON_VERSIONS)
def tests(session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install(
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "pytest-mock",
        "pytest-html",
        "coverage[toml]",
        "requests-mock",
    )
    session.run("pytest", "tests/unit", "--cov-fail-under=70")


@session(python=PYTHON_VERSIONS)
def docstrings(session) -> None:
    """Validate docstrings."""
    session.install("darglint")
    session.run("darglint", "open_gopro")


@session(python=PYTHON_VERSIONS)
def docs(session) -> None:
    """Build the documentation."""
    session.install(".")
    session.install(
        "sphinx",
        "sphinx-autodoc-typehints",
        "sphinx-rtd-theme",
        "sphinxcontrib-napoleon",
    )
    session.run("sphinx-build", "docs", "docs/_build")


@session(python=PYTHON_VERSIONS)
def safety(session) -> None:
    """Scan dependencies for insecure packages."""
    session.install("safety")
    session.run(
        "safety",
        "check",
        f"--file={Path(session.virtualenv.location) / 'tmp' / 'requirements.txt'}",
        "--full-report",
    )
