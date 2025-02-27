from pathlib import Path

import pytest


@pytest.fixture
def enum_as_text() -> str:
    return (Path("tests") / "vectors" / "enum.kt").read_text()


@pytest.fixture
def sealed_class_as_text() -> str:
    return (Path("tests") / "vectors" / "sealed_class.kt").read_text()

@pytest.fixture
def file_as_text() -> str:
    return (Path("tests") / "vectors" / "file.kt").read_text()