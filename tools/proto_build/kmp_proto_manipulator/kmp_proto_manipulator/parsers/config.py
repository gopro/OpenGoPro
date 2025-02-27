# config.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 27 22:11:09 UTC 2025

"""Config Parser."""

import tomllib
from pathlib import Path

from kmp_proto_manipulator.entities.config import Config


class ConfigParser:
    """Config Parser.

    This has no context-aware data so can be used like a singleton via class methods.
    """

    @classmethod
    def parse_config(cls, config_toml: Path) -> Config:
        """Parse a config TOML file into a Config object.

        Args:
            config_toml (Path): input TOML file

        Returns:
            Config: parsed config object
        """
        return Config(**tomllib.loads(config_toml.read_text()))
