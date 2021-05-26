# stream.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Entrypoint for taking a picture."""

import sys
import time
import logging
import argparse
import threading
from pathlib import Path
from typing import Tuple

from rich import traceback
from rich.logging import RichHandler
from rich.console import Console

from open_gopro import GoPro, params
from open_gopro.util import launch_vlc

logger = logging.getLogger(__name__)
traceback.install()  # Enable exception tracebacks in rich logger
console = Console()  # rich consoler printer


def main() -> None:
    """Main function."""
    identifier, log_location, vlc_location = parse_arguments()
    setup_logging(log_location)

    try:
        spinner = console.status("[bold green]Connecting...")
        spinner.start()
        with GoPro(identifier) as gopro:
            assert gopro.ble_command.set_shutter(params.Shutter.OFF).is_ok
            assert gopro.ble_command.set_turbo_mode(False).is_ok
            spinner.stop()

            with console.status("[bold green]Starting the preview stream..."):
                assert gopro.wifi_command.stop_preview_stream().is_ok
                assert gopro.wifi_command.start_preview_stream().is_ok

            with console.status("[bold green]Launching VLC..."):
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
        sys.exit(-1)
    except KeyboardInterrupt:
        console.print("Received keyboard interrupt. Shutting down...")
    finally:
        console.print("Exiting...")
        sys.exit(0)


def setup_logging(log_location: Path) -> None:
    """Configure logging to file and Rich console logging

    Args:
        log_location (Path): location to configure for the file handler
    """
    # Logging to file with
    fh = logging.FileHandler(f"{log_location}", mode="w")
    file_formatter = logging.Formatter(
        fmt="%(threadName)13s: %(name)30s:%(lineno)5d %(asctime)s.%(msecs)03d %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    fh.setFormatter(file_formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Use Rich for colorful console logging
    sh = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
    stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
    sh.setFormatter(stream_formatter)
    sh.setLevel(logging.WARNING)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    # Enable / disable logging in modules
    for (module, level) in [
        ("open_gopro.gopro", logging.DEBUG),
        ("open_gopro.ble_commands", logging.DEBUG),
        ("open_gopro.ble_controller", logging.DEBUG),
        ("open_gopro.wifi_commands", logging.DEBUG),
        ("open_gopro.wifi_controller", logging.DEBUG),
        ("open_gopro.responses", logging.DEBUG),
        ("open_gopro.util", logging.DEBUG),
        ("bleak", logging.DEBUG),
        ("bleak.backends.bluezdbus.client", logging.DEBUG),
        ("bleak.backends.corebluetooth.client", logging.DEBUG),
        ("bleak.backends.dotnet.client", logging.DEBUG),
    ]:
        log = logging.getLogger(module)
        log.setLevel(level)
        log.addHandler(fh)
        log.addHandler(sh)


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
