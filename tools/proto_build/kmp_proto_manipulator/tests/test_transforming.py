import pytest

from kmp_proto_manipulator.entities.config import Config
from kmp_proto_manipulator.parsers.config import ConfigParser
from kmp_proto_manipulator.parsers.kotlin_transformer import KotlinTransformer


@pytest.fixture(scope="function")
def transformer(config_as_path) -> KotlinTransformer:
    return KotlinTransformer(ConfigParser.parse_config(config_as_path))


def test_object_in_config_is_transformed(transformer: KotlinTransformer, sealed_class_as_text: str):
    transformed = transformer.transform(sealed_class_as_text)
    assert "internal sealed class" not in transformed
    assert "public sealed class" in transformed


def test_object_not_in_config_is_not_transformed(transformer: KotlinTransformer, sealed_class_negative_as_text: str):
    transformed = transformer.transform(sealed_class_negative_as_text)
    assert "internal sealed class" in transformed
    assert "public sealed class" not in transformed
