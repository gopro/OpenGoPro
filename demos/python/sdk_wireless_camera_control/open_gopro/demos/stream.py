# stream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:46 PM

"""Entrypoint for taking a picture."""

import time
import logging
import argparse
import threading
from pathlib import Path
from typing import Optional

from rich.console import Console

from open_gopro import GoPro, Params
from open_gopro.util import launch_vlc, setup_logging, add_cli_args_and_parse

logger = logging.getLogger(__name__)
console = Console()  # rich consoler printer


def main(args: argparse.Namespace) -> None:
    global logger
    logger = setup_logging(logger, args.log)

    gopro: Optional[GoPro] = None
    try:
        with GoPro(args.identifier, wifi_interface=args.wifi_interface, sudo_password=args.password) as gopro:
            # Turn off the shutter if we are currently encoding
            if gopro.is_encoding:
                gopro.ble_command.set_shutter(Params.Shutter.OFF)

            gopro.ble_command.set_turbo_mode(False)

            console.print("Starting the preview stream...")
            assert gopro.wifi_command.stop_preview_stream().is_ok
            assert gopro.wifi_command.start_preview_stream().is_ok

            console.print("Launching VLC...")
            threading.Thread(target=launch_vlc, args=(args.vlc_location,), daemon=True).start()

            console.print("Success!! :smiley: Stream has been enabled. VLC is viewing it at udp://@:8554")
            console.print("Send keyboard interrupt to exit.")

            while True:
                time.sleep(0.2)

    except KeyboardInterrupt:
        console.print("Received keyboard interrupt. Shutting down...")
    if gopro:
        gopro.close()
    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, enable the preview stream, then open VLC to view it."
    )
    parser.add_argument(
        "-v",
        "--vlc",
        type=Path,
        help="VLC location. If not set, the location will attempt to be automatically discovered.",
        default=None,
    )
    return add_cli_args_and_parse(parser)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
