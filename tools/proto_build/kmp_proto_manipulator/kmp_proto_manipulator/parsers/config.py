import tomllib

from pathlib import Path

from kmp_proto_manipulator.entities.config import Config


class ConfigParser:
    @classmethod
    def parse_config(cls, config_toml: Path) -> Config:
        return Config(**tomllib.loads(config_toml.read_text()))
