# usb.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 18 00:18:13 UTC 2022

"""Usb demo"""

import argparse
from typing import Final
from pathlib import Path

from rich.console import Console

from open_gopro import WiredGoPro, Params
from open_gopro.util import setup_logging, display_video_blocking

console = Console()  # rich consoler printer

STREAM_URL: Final[str] = r"udp://0.0.0.0:8554"


def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    with WiredGoPro(args.identifier) as gopro:
        # Start webcam
        gopro.http_command.wired_usb_control(control=Params.Toggle.DISABLE)
        gopro.http_command.webcam_start()

        # Start player
        display_video_blocking(STREAM_URL)  # blocks until user exists viewer
        gopro.http_command.webcam_stop()
        gopro.http_command.webcam_exit()

    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Setup and view a GoPro webcam.")
    parser.add_argument(
        "identifier",
        type=str,
        help="Last 3 digits of GoPro serial number, which is the last 3 digits of the default camera SSID.",
    )
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        help="Location to store detailed log",
        default="gopro_demo.log",
    )
    return parser.parse_args()


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
