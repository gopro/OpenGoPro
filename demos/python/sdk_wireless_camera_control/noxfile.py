# noxfile.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Feb  4 21:36:17 UTC 2022

"""Nox sessions."""

import nox
from nox_poetry import session

# Don't run docs by default since it needs graphviz.
nox.options.sessions = "format", "lint", "tests", "docstrings"

SUPPORTED_VERSIONS = [
    "3.9",
    "3.10",
    "3.11",
]


@session(python=SUPPORTED_VERSIONS[-1])
def format(session) -> None:
    """Run black code formatter."""
    session.install("black")
    session.run("black", "--check", "open_gopro", "tests", "noxfile.py", "docs/conf.py")


# Mypy is changing too much between versions. Let's only lint on the latest version
@session(python=SUPPORTED_VERSIONS[-1])
def lint(session) -> None:
    """Lint using pylint and check types with mypy."""
    session.install(".[gui]")
    session.install(
        "pylint",
        "mypy",
        "construct-typing",
        "mypy-protobuf",
        "types-requests",
        "types-attrs",
        "types-pytz",
        "types-tzlocal",
    )
    session.run("mypy", "open_gopro")
    session.run("pylint", "--no-docstring-rgx=__|main|parse_arguments|entrypoint", "open_gopro")


@session(python=SUPPORTED_VERSIONS)
def tests(session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install(
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "pytest-timeout",
        "pytest-mock",
        "pytest-html",
        "coverage[toml]",
        "requests-mock",
    )
    session.run("pytest", "tests", "--cov-fail-under=65")


@session(python=SUPPORTED_VERSIONS[-1])
def docstrings(session) -> None:
    """Validate docstrings."""
    session.install("darglint")
    session.install("pydocstyle[toml]")
    session.run("pydocstyle", "open_gopro")
    session.run("darglint", "open_gopro")


@session(python=SUPPORTED_VERSIONS[-1])
def docs(session) -> None:
    """Build the documentation."""
    session.install(".")
    session.install(
        "sphinx",
        "sphinx-autodoc-typehints",
        "sphinx-rtd-theme",
        "sphinxcontrib-napoleon",
        "autodoc-pydantic",
        "darglint",
    )
    session.run("sphinx-build", "-W", "docs", "docs/build")
    # Clean up for Jekyll consumption
    session.run("rm", "-rf", "docs/build/.doctrees", "/docs/build/_sources", "/docs/build/_static/fonts", external=True)
