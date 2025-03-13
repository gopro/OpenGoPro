# conftest.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 27 22:11:09 UTC 2025

from pathlib import Path

import pytest

@pytest.fixture(scope="module")
def sealed_class_as_text() -> str:
    return (Path("tests") / "vectors" / "sealed_class.kt").read_text()


@pytest.fixture(scope="module")
def sealed_class_negative_as_text() -> str:
    return (Path("tests") / "vectors" / "sealed_class_negative.kt").read_text()

@pytest.fixture(scope="module")
def data_class_as_text() -> str:
    return (Path("tests") / "vectors" / "data_class.kt").read_text()


@pytest.fixture(scope="module")
def data_class_negative_as_text() -> str:
    return (Path("tests") / "vectors" / "data_class_negative.kt").read_text()


@pytest.fixture(scope="module")
def file_as_text() -> str:
    return (Path("tests") / "vectors" / "file.kt").read_text()


@pytest.fixture(scope="module")
def config_as_path() -> Path:
    return Path("tests") / "vectors" / "config.toml"
