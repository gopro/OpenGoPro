# set_kotlin_proto_scopes.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 27 22:11:09 UTC 2025

"""Script to manipulate proto-generated kotlin files"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from kmp_proto_manipulator.parsers.config import ConfigParser
from kmp_proto_manipulator.parsers.kotlin_transformer import KotlinTransformer

logger: logging.Logger


def parse_arguments() -> argparse.Namespace:  # noqa
    parser = argparse.ArgumentParser(description="Selectively modify the scope of proto-generated kotlin files.")
    parser.add_argument(
        "config",
        type=Path,
        help="Path to proto manipulator config toml file",
    )
    parser.add_argument(
        "dir",
        type=Path,
        help="Path to directory of kotlin files  to manipulate",
    )
    return parser.parse_args()


def main(args: argparse.Namespace) -> int:  # noqa
    input_directory: Path = args.dir
    config_file: Path = args.config

    print("Transforming proto-generated Kotlin files...")

    transformer = KotlinTransformer(
        config=ConfigParser.parse_config(config_file),
    )

    for kt in input_directory.glob(r"*.kt"):
        print(f"Transforming {kt.name}")
        kt.write_text(transformer.transform(kt.read_text()))

    return 0


def entrypoint() -> int:  # noqa
    sys.exit(main(parse_arguments()))


if __name__ == "__main__":
    main(parse_arguments())
