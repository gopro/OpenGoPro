# connect_wifi.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:44 PM

"""Connect to the Wifi AP of a GoPro camera."""

import sys
import time
import logging
import argparse
from pathlib import Path
from typing import Optional, Tuple

from rich.console import Console

from open_gopro import GoPro
from open_gopro.util import setup_logging, set_logging_level

logger = logging.getLogger(__name__)
console = Console()  # rich consoler printer


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera's Wifi Access Point.")
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. \
            If not used, first discovered GoPro will be connected to",
        default=None,
    )
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        help="Location to store detailed log",
        default="gopro_wifi.log",
    )
    parser.add_argument(
        "-w",
        "--wifi_interface",
        type=str,
        help="System Wifi Interface. If not set, first discovered interface will be used.",
        default=None,
    )
    parser.add_argument(
        "-p",
        "--password",
        action="store_true",
        help="set to read sudo password from stdin",
    )

    args = parser.parse_args()
    args.password = sys.stdin.readline() if args.password else None
    return args


def main(args: argparse.Namespace) -> int:
    global logger
    logger = setup_logging(logger, args.log)

    gopro: Optional[GoPro] = None
    return_code = 0
    try:
        with GoPro(args.identifier, wifi_interface=args.wifi_interface, wifi_password=args.password, enable_wifi=False) as gopro:
            # Now we only want errors
            set_logging_level(logger, logging.ERROR)

            gopro.wifi_command.set_keep_alive()

            console.print("\n\n🎆🎇✨ Success!! Wifi AP is connected 📡\n")
            console.print("Send commands as per https://gopro.github.io/OpenGoPro/http")
            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
    if gopro is not None:
        gopro.close()
    console.print("Exiting...")
    return return_code


if __name__ == "__main__":
    main(parse_arguments())
