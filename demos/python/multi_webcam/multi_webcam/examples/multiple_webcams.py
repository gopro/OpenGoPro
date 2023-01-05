# multiple_webcams.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 11 20:03:39 UTC 2022

from __future__ import annotations
import json
import logging
import argparse
from pathlib import Path

from multi_webcam import GoProWebcamPlayer

logging.basicConfig(level=logging.DEBUG)


def main(args: argparse.Namespace):
    with open(args.config) as fp:
        config = json.load(fp)

    webcams: list[GoProWebcamPlayer] = []
    # Open webcams
    for serial, params in config.items():
        w = GoProWebcamPlayer(serial, params.get("port"))
        w.open()
        webcams.append(w)
        w.play(params.get("resolution"), params.get("fov"))

    input("Press enter to stop")
    for webcam in webcams:
        webcam.close()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configure, enable and start webcams with players to view them."
    )
    parser.add_argument("config", type=Path, help="Location of config json file.")
    return parser.parse_args()


def entrypoint():
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
