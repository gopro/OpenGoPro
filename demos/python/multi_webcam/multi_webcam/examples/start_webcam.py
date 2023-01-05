# start_webcam.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 11 20:03:39 UTC 2022

import sys
import logging
import argparse
from typing import Final

from multi_webcam.webcam import Webcam

logging.basicConfig(level=logging.DEBUG)

DEFAULT_PORT: Final = 8554


def main(args: argparse.Namespace):
    try:
        webcam = Webcam(serial=args.serial)  # 11
        webcam.start(args.port, args.resolution, args.fov)
        input("Press enter to exit...")
        webcam.disable()
    except Exception as e:
        logging.error(e)
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enable and start the webcam.")
    parser.add_argument("serial", type=str, help="Last 3 digits of camera serial number.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help=f"Port to use. If not set, port will not be specified to camera.",
        default=None,
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        help=f"Resolution to use. If set, fov must also be set.",
        default=None,
    )
    parser.add_argument(
        "-f",
        "--fov",
        type=int,
        help=f"FOV to use. If set, resolution must also be set",
        default=None,
    )
    return parser.parse_args()


def entrypoint():
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
