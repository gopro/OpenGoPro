"""Nox sessions."""

import tempfile
from typing import Any

import nox
from nox_poetry import session


package = "open_gopro"
nox.options.sessions = "lint", "types", "tests", "docs", "format"
locations = "open_gopro", "tests", "noxfile.py", "docs/conf.py"


@session(python=["3.8"])
def format(session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=["3.8"])
def lint(session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@session(python=["3.8"])
def types(session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@session(python=["3.8"])
def tests(session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install(
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "pytest-mock",
        "coverage[toml]",
        "requests-mock"
    )
    session.run("pytest", "tests/unit_tests")


@session(python=["3.8"])
def docs(session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")


@session(python=["3.8"])
def coverage(session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@session(python=["3.8"])
def safety(session) -> None:
    """Scan dependencies for insecure packages."""
    session.install("safety")
    session.run("safety", "check", f"--file={requirements.name}", "--full-report")
