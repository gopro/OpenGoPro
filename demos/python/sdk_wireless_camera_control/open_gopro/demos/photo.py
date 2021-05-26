# photo.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Entrypoint for taking a picture."""

import sys
import logging
import argparse
from pathlib import Path
from typing import Tuple

from rich import traceback
from rich.logging import RichHandler
from rich.console import Console

from open_gopro import GoPro, params

logger = logging.getLogger(__name__)
traceback.install()  # Enable exception tracebacks in rich logger
console = Console()  # rich consoler printer


def main() -> None:
    """Main function."""
    identifier, log_location, output_location = parse_arguments()
    setup_logging(log_location)

    try:
        spinner = console.status("[bold green]Connecting...")
        spinner.start()
        with GoPro(identifier) as gopro:
            assert gopro.ble_command.set_shutter(params.Shutter.OFF).is_ok
            assert gopro.ble_command.set_turbo_mode(False).is_ok
            spinner.stop()

            with console.status("[bold green]Capturing a photo..."):
                # Get the media list before
                media_set_before = set(x["n"] for x in gopro.wifi_command.get_media_list()["media"][0]["fs"])
                # Take a photo
                assert gopro.ble_command.load_preset(params.Preset.PHOTO).is_ok
                assert gopro.ble_command.set_shutter(params.Shutter.ON).is_ok

            with console.status("[bold green]Downloading the photo..."):
                # Get the media list after
                media_set_after = set(x["n"] for x in gopro.wifi_command.get_media_list()["media"][0]["fs"])
                # The photo (is most likely) the difference between the two dicts as sets
                photo = media_set_after.difference(media_set_before).pop()
                # Download the photo
                gopro.wifi_command.download_file(camera_file=photo, local_file=output_location)

            console.print(
                f"Success!! :smiley: File has been downloaded to {output_location}", style="bold green"
            )

    except Exception as e:  # pylint: disable=broad-except
        logger.error(repr(e))
        sys.exit(-1)
    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
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
        Tuple[str, Path, Path]: (identifier, path to save log, path to store photo)
    """
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera, take a photo, then download it.")
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
        default=Path("photo.log"),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Where to write the photo to. If not set, write to 'photo.jpg'",
        default=Path("photo.jpg"),
    )
    args = parser.parse_args()

    return args.identifier, args.log, args.output


if __name__ == "__main__":
    main()
