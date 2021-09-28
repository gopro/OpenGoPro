# video.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:46 PM

"""Entrypoint for taking a video demo."""

import time
import logging
import argparse
from pathlib import Path
from typing import Tuple, Optional

from rich.console import Console

from open_gopro import GoPro
from open_gopro.util import setup_logging

logger = logging.getLogger(__name__)
console = Console()  # rich consoler printer


def main() -> int:
    """Main program functionality

    Returns:
        int: program return code
    """
    identifier, log_location, output_location, record_time = parse_arguments()

    global logger
    logger = setup_logging(logger, log_location)

    gopro: Optional[GoPro] = None
    return_code = 0
    try:
        with GoPro(identifier) as gopro:
            # Turn off the shutter if we are currently encoding
            if gopro.is_encoding:
                assert gopro.ble_command.set_shutter(gopro.params.Shutter.OFF).is_ok

            assert gopro.ble_command.set_turbo_mode(False).is_ok

            console.print("Capturing a video...")
            # Get the media list before
            media_set_before = set(x["n"] for x in gopro.wifi_command.get_media_list()["media"][0]["fs"])
            # Take a video
            assert gopro.ble_command.load_preset(gopro.params.Preset.CINEMATIC).is_ok
            assert gopro.ble_command.set_shutter(gopro.params.Shutter.ON).is_ok
            time.sleep(record_time)
            assert gopro.ble_command.set_shutter(gopro.params.Shutter.OFF).is_ok

            console.print("Downloading the video...")
            # Get the media list after
            media_set_after = set(x["n"] for x in gopro.wifi_command.get_media_list()["media"][0]["fs"])
            # The video (is most likely) the difference between the two dicts as sets
            video = media_set_after.difference(media_set_before).pop()
            # Download the video
            gopro.wifi_command.download_file(camera_file=video, local_file=output_location)
            console.print(
                f"Success!! :smiley: File has been downloaded to {output_location}", style="bold green"
            )

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


def parse_arguments() -> Tuple[str, Path, Path, float]:
    """Parse command line arguments

    Returns:
        Tuple[str, Path, Path, float]: (identifier, path to save log, path to store video, record_time)
    """
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera, take a video, then download it.")
    parser.add_argument(
        "record_time",
        type=float,
        help="How long to record for",
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
        default=Path("video.log"),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Where to write the video to. If not set, write to 'video.mp4'",
        default=Path("video.mp4"),
    )
    args = parser.parse_args()

    return args.identifier, args.log, args.output, args.record_time


if __name__ == "__main__":
    main()
