# test_transforming.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 27 22:11:09 UTC 2025

import pytest

from kmp_proto_manipulator.entities.config import Config
from kmp_proto_manipulator.parsers.config import ConfigParser
from kmp_proto_manipulator.parsers.kotlin_transformer import KotlinTransformer


@pytest.fixture(scope="function")
def transformer(config_as_path) -> KotlinTransformer:
    return KotlinTransformer(ConfigParser.parse_config(config_as_path))


def test_sealed_class_in_config_is_transformed(transformer: KotlinTransformer, sealed_class_as_text: str):
    transformed = transformer.transform(sealed_class_as_text)
    assert "internal sealed class" not in transformed
    assert "public sealed class" in transformed


def test_sealed_class_not_in_config_is_not_transformed(
    transformer: KotlinTransformer, sealed_class_negative_as_text: str
):
    transformed = transformer.transform(sealed_class_negative_as_text)
    assert "internal sealed class" in transformed
    assert "public sealed class" not in transformed


def test_data_class_in_config_is_transformed(transformer: KotlinTransformer, data_class_as_text: str):
    transformed = transformer.transform(data_class_as_text)
    assert "internal data class" not in transformed
    assert "public data class" in transformed


def test_data_class_not_in_config_is_not_transformed(transformer: KotlinTransformer, data_class_negative_as_text: str):
    transformed = transformer.transform(data_class_negative_as_text)
    assert "internal data class" in transformed
    assert "public data class" not in transformed
