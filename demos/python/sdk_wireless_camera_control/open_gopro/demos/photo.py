# photo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Entrypoint for taking a picture demo."""

import argparse
from pathlib import Path

from rich.console import Console

from open_gopro import WirelessGoPro, WiredGoPro, Params, constants
from open_gopro.util import setup_logging, add_cli_args_and_parse

console = Console()  # rich consoler printer


def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    with WiredGoPro(args.identifier) if args.wired else WirelessGoPro(
        args.identifier, wifi_interface=args.wifi_interface
    ) as gopro:
        if args.wired:
            gopro.http_command.wired_usb_control(control=Params.Toggle.ENABLE)
        # Configure settings to prepare for photo
        gopro.http_setting.video_performance_mode.set(Params.PerformanceMode.MAX_PERFORMANCE)
        gopro.http_setting.max_lens_mode.set(Params.MaxLensMode.DEFAULT)
        gopro.http_setting.camera_ux_mode.set(Params.CameraUxMode.PRO)
        gopro.http_command.set_turbo_mode(mode=Params.Toggle.DISABLE)
        assert gopro.http_command.load_preset_group(group=Params.PresetGroup.PHOTO).is_ok

        # Get the media list before
        media_set_before = set(x["n"] for x in gopro.http_command.get_media_list().flatten)
        # Take a photo
        console.print("Capturing a photo...")
        assert gopro.http_command.set_shutter(shutter=Params.Toggle.ENABLE).is_ok

        # Wait for encoding to start
        while not gopro.http_command.get_camera_state()[constants.StatusId.ENCODING]:
            continue
        # Wait for encoding to stop
        while gopro.http_command.get_camera_state()[constants.StatusId.ENCODING]:
            continue

        # Get the media list after
        media_set_after = set(x["n"] for x in gopro.http_command.get_media_list().flatten)
        # The photo (is most likely) the difference between the two sets
        photo = media_set_after.difference(media_set_before).pop()
        # Download the photo
        console.print("Downloading the photo...")
        gopro.http_command.download_file(camera_file=photo, local_file=args.output)
        console.print(f"Success!! :smiley: File has been downloaded to {args.output}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera, take a photo, then download it.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Where to write the photo to. If not set, write to 'photo.jpg'",
        default=Path("photo.jpg"),
    )
    parser.add_argument(
        "--wired",
        action="store_true",
        help="Set to use wired (USB) instead of wireless (BLE / WIFI) interface",
    )

    return add_cli_args_and_parse(parser)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
