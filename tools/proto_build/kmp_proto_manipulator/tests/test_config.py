from pathlib import Path

from kmp_proto_manipulator.entities.config import ProtoObjectScope
from kmp_proto_manipulator.parsers.config import ConfigParser


def test_parse_config(config_as_path: Path):
    config = ConfigParser.parse_config(config_as_path)
    assert len(config.root) == 11
    assert config.root["PresetSetting"].scope == ProtoObjectScope.PUBLIC
