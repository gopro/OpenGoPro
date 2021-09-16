# stream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:46 PM

"""Entrypoint for taking a picture."""

import time
import logging
import argparse
import threading
from pathlib import Path
from typing import Tuple, Optional

from rich.console import Console

from open_gopro import GoPro
from open_gopro.util import launch_vlc, setup_logging

logger = logging.getLogger(__name__)
console = Console()  # rich consoler printer


def main() -> int:
    """Main functionality

    Returns:
        int: program return code
    """
    identifier, log_location, vlc_location = parse_arguments()
    global logger
    logger = setup_logging(logger, log_location)

    gopro: Optional[GoPro] = None
    return_code = 0
    try:
        with GoPro(identifier) as gopro:
            # Turn off the shutter if we are currently encoding
            if gopro.is_encoding:
                assert gopro.ble_command.set_shutter(gopro.params.Shutter.OFF)

            assert gopro.ble_command.set_turbo_mode(False).is_ok

            console.print("Starting the preview stream...")
            assert gopro.wifi_command.stop_preview_stream().is_ok
            assert gopro.wifi_command.start_preview_stream().is_ok

            console.print("Launching VLC...")
            threading.Thread(target=launch_vlc, args=(vlc_location,), daemon=True).start()

            console.print(
                "Success!! :smiley: Stream has been enabled. VLC is viewing it at udp://@:8554",
                style="bold green",
            )
            console.print("Send keyboard interrupt to exit.")

            while True:
                time.sleep(0.2)

    except Exception as e:  # pylint: disable=broad-except
        logger.error(repr(e))
        return_code = 1
    except KeyboardInterrupt:
        console.print("Received keyboard interrupt. Shutting down...")
    finally:
        if gopro is not None:
            gopro.close()
        console.print("Exiting...")
        return return_code  # pylint: disable=lost-exception


def parse_arguments() -> Tuple[str, Path, Path]:
    """Parse command line arguments

    Returns:
        Tuple[str, Path, Path]: (identifier, path to save log, path to VLC)
    """
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, enable the preview stream, then open VLC to view it."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If \
            not used, first discovered GoPro will be connected to",
        default=None,
    )
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        help="Location to store detailed log",
        default=Path("stream.log"),
    )
    parser.add_argument(
        "-v",
        "--vlc",
        type=Path,
        help="VLC location. If not set, the location will attempt to be automatically discovered.",
        default=None,
    )
    args = parser.parse_args()

    return args.identifier, args.log, args.vlc


if __name__ == "__main__":
    main()
