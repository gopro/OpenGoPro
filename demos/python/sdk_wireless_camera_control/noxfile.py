"""Nox sessions."""

from pathlib import Path
from typing import Any

import nox
from nox_poetry import session

nox.options.sessions = "format", "lint", "tests", "docstrings", "docs", "safety"


@session(python=["3.9"])
def format(session) -> None:
    """Run black code formatter."""
    session.install("black")
    session.run("black", "--check", "open_gopro", "tests", "noxfile.py", "docs/conf.py")


@session(python=["3.8", "3.9", "3.10"])
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


@session(python=["3.8", "3.9", "3.10"])
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


@session(python=["3.9"])
def docstrings(session) -> None:
    """Validate docstrings."""
    session.install("darglint")
    session.run("darglint", "open_gopro")


@session(python=["3.9"])
def docs(session) -> None:
    """Build the documentation."""
    session.install(".")
    session.install(
        "sphinx",
        "sphinx-autodoc-typehints",
        "sphinx-rtd-theme",
        "sphinxcontrib-napoleon",
    )
    session.run("sphinx-build", "docs", "docs/build")


@session(python=["3.8", "3.9", "3.10"])
def safety(session) -> None:
    """Scan dependencies for insecure packages."""
    session.install("safety")
    session.run(
        "safety",
        "check",
        f"--file={Path(session.virtualenv.location) / 'tmp' / 'requirements.txt'}",
        "--full-report",
    )
