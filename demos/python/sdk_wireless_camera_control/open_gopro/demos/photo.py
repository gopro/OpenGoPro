# photo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Entrypoint for taking a picture demo."""

import argparse
from pathlib import Path
from typing import Optional

from rich.console import Console

from open_gopro import GoPro, Params
from open_gopro.util import setup_logging, add_cli_args_and_parse

console = Console()  # rich consoler printer


def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    def exception_cb(exception: Exception) -> None:  # pylint: disable=unused-variable
        logger.error(f"IN MAIN ==> {exception}")

    gopro: Optional[GoPro] = None
    try:
        with GoPro(args.identifier, wifi_interface=args.wifi_interface, exception_cb=exception_cb) as gopro:
            # Configure settings to prepare for photo
            if gopro.is_encoding:
                gopro.ble_command.set_shutter(Params.Toggle.DISABLE)
            gopro.ble_setting.video_performance_mode.set(Params.PerformanceMode.MAX_PERFORMANCE)
            gopro.ble_setting.max_lens_mode.set(Params.MaxLensMode.DEFAULT)
            gopro.ble_setting.camera_ux_mode.set(Params.CameraUxMode.PRO)
            gopro.ble_command.set_turbo_mode(False)
            assert gopro.ble_command.load_preset_group(Params.PresetGroup.PHOTO).is_ok

            # Get the media list before
            media_set_before = set(x["n"] for x in gopro.wifi_command.get_media_list().flatten)
            # Take a photo
            console.print("Capturing a photo...")
            assert gopro.ble_command.set_shutter(Params.Toggle.ENABLE).is_ok

            # Get the media list after
            media_set_after = set(x["n"] for x in gopro.wifi_command.get_media_list().flatten)
            # The photo (is most likely) the difference between the two sets
            photo = media_set_after.difference(media_set_before).pop()
            # Download the photo
            console.print("Downloading the photo...")
            gopro.wifi_command.download_file(camera_file=photo, local_file=args.output)
            console.print(f"Success!! :smiley: File has been downloaded to {args.output}")

    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")

    if gopro:
        gopro.close()
    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera, take a photo, then download it.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Where to write the photo to. If not set, write to 'photo.jpg'",
        default=Path("photo.jpg"),
    )
    return add_cli_args_and_parse(parser)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
