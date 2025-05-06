# photo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Entrypoint for taking a picture demo."""

import argparse
import asyncio
from pathlib import Path

from rich.console import Console

from open_gopro import WiredGoPro, WirelessGoPro
from open_gopro.gopro_base import GoProBase
from open_gopro.models import constants, proto
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging

console = Console()


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: GoProBase | None = None

    try:
        async with (
            WiredGoPro(args.identifier)
            if args.wired
            else WirelessGoPro(args.identifier, host_wifi_interface=args.wifi_interface)
        ) as gopro:
            assert gopro
            assert (await gopro.http_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_PHOTO)).ok

            # Get the media list before
            media_set_before = set((await gopro.http_command.get_media_list()).data.files)

            # Take a photo
            assert (await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)).ok

            # Get the media list after
            media_set_after = set((await gopro.http_command.get_media_list()).data.files)
            # The video (is most likely) the difference between the two sets
            photo = media_set_after.difference(media_set_before).pop()

            # Download the photo
            console.print(f"Downloading {photo.filename}...")
            await gopro.http_command.download_file(camera_file=photo.filename, local_file=args.output)
            console.print(f"Success!! :smiley: File has been downloaded to {Path(args.output).absolute()}")

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()


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
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
