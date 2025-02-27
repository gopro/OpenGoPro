from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def enum_as_text() -> str:
    return (Path("tests") / "vectors" / "enum.kt").read_text()


@pytest.fixture(scope="module")
def sealed_class_as_text() -> str:
    return (Path("tests") / "vectors" / "sealed_class.kt").read_text()


@pytest.fixture(scope="module")
def sealed_class_negative_as_text() -> str:
    return (Path("tests") / "vectors" / "sealed_class_negative.kt").read_text()


@pytest.fixture(scope="module")
def file_as_text() -> str:
    return (Path("tests") / "vectors" / "file.kt").read_text()


@pytest.fixture(scope="module")
def config_as_path() -> Path:
    return Path("tests") / "vectors" / "config.toml"
