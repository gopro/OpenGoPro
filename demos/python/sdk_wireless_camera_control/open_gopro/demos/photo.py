# photo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Entrypoint for taking a picture demo."""

import sys
import logging
import argparse
from pathlib import Path
from typing import Tuple, Optional

from rich.console import Console

from open_gopro import GoPro, Params
from open_gopro.util import setup_logging

logger = logging.getLogger(__name__)
console = Console()  # rich consoler printer


def main(
    identifier: Optional[str], log_location: Path, output_location: Path, wifi_interface: Optional[str]
) -> int:
    """Main program functionality

    Args:
        identifier (Optional[str]): device to connect to
        log_location (Path): file to write detailed log
        output_location (Path): name of photo file
        wifi_interface (Optional[str]): wifi interface (or None to auto detect)

    Returns:
        int: program return code
    """
    global logger
    logger = setup_logging(logger, log_location)

    def exception_cb(exception: Exception) -> None:
        logger.error(f"IN MAIN ==> {exception}")

    gopro: Optional[GoPro] = None
    return_code = 0
    try:
        with GoPro(identifier, wifi_interface=wifi_interface, exception_cb=exception_cb) as gopro:
            # Configure settings to prepare for photo
            if gopro.is_encoding:
                gopro.ble_command.set_shutter(Params.Shutter.OFF)
            gopro.ble_setting.video_performance_mode.set(Params.PerformanceMode.MAX_PERFORMANCE)
            gopro.ble_setting.max_lens_mode.set(Params.MaxLensMode.DEFAULT)
            gopro.ble_command.set_turbo_mode(False)
            assert gopro.ble_command.load_preset(Params.Preset.PHOTO).is_ok

            # Get the media list before
            media_set_before = set(x["n"] for x in gopro.wifi_command.get_media_list().flatten)
            # Take a photo
            console.print("Capturing a photo...")
            assert gopro.ble_command.set_shutter(Params.Shutter.ON).is_ok

            # Get the media list after
            media_set_after = set(x["n"] for x in gopro.wifi_command.get_media_list().flatten)
            # The photo (is most likely) the difference between the two sets
            photo = media_set_after.difference(media_set_before).pop()
            # Download the photo
            console.print("Downloading the photo...")
            gopro.wifi_command.download_file(camera_file=photo, local_file=output_location)
            console.print(f"Success!! :smiley: File has been downloaded to {output_location}")

    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")

    if gopro is not None:
        gopro.close()
    console.print("Exiting...")
    return return_code


def parse_arguments() -> Tuple[str, Path, Path, Optional[str]]:
    """Parse command line arguments

    Returns:
        Tuple[str, Path, Path, Optional[str]]: (identifier, path to save log, path to store photo, wifi interface)
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
    parser.add_argument(
        "-w",
        "--wifi_interface",
        type=str,
        help="System Wifi Interface. If not set, first discovered interface will be used.",
        default=None,
    )
    args = parser.parse_args()

    return args.identifier, args.log, args.output, args.wifi_interface


def entrypoint() -> None:
    """Entrypoint for setup.py"""
    sys.exit(main(*parse_arguments()))


if __name__ == "__main__":
    entrypoint()
