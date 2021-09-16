# connect_wifi.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:44 PM

"""Connect to the Wifi AP of a GoPro camera."""

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


def parse_arguments() -> Tuple[Optional[str], Path]:
    """Parse the command line arguments

    Returns:
        Tuple[Optional[str], Path]: (identifier, log location)
    """
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
    args = parser.parse_args()

    return (args.identifier, args.log)


def main() -> int:
    """Main functionality

    Returns:
        int: program return code
    """
    (identifier, log_location) = parse_arguments()
    global logger
    logger = setup_logging(logger, log_location)

    gopro: Optional[GoPro] = None
    return_code = 0
    try:
        with GoPro(identifier) as _:
            # Now we only want errors
            set_logging_level(logger, logging.ERROR)

            console.print("\n\n🎆🎇✨ Success!! Wifi AP is connected 📡\n")
            console.print("Send commands as per https://gopro.github.io/OpenGoPro/wifi")
            while True:
                time.sleep(1)

    except Exception as e:  # pylint: disable=broad-except
        logger.error(repr(e))
        return_code = 1
    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
    finally:
        if gopro is not None:
            gopro.close()
        console.print("Exiting...")
        return return_code  # pylint: disable=lost-exception


if __name__ == "__main__":
    main()
