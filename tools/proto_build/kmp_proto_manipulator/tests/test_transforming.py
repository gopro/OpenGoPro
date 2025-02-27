import pytest

from kmp_proto_manipulator.entities.config import Config
from kmp_proto_manipulator.parsers.config import ConfigParser

@pytest.fixture(scope="module")
def config(config_as_path) -> Config:
    return ConfigParser.parse_config(config_as_path)

class TestTransforming:
    def test_object_in_config_is_transformed(self):

    def test_object_not_in_config_is_not_transformed(self): ...
