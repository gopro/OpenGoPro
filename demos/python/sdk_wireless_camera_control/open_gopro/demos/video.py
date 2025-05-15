# video.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:46 PM

"""Entrypoint for taking a video demo."""

import argparse
import asyncio
from pathlib import Path

from rich.console import Console

from open_gopro import WiredGoPro, WirelessGoPro
from open_gopro.models import constants, proto
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging

console = Console()


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)
    gopro: WirelessGoPro | WiredGoPro | None = None

    try:
        async with (
            WiredGoPro(args.identifier)
            if args.wired
            else WirelessGoPro(args.identifier, host_wifi_interface=args.wifi_interface)
        ) as gopro:
            assert gopro
            assert (await gopro.http_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_VIDEO)).ok

            # Get the media set before
            media_set_before = set((await gopro.http_command.get_media_list()).data.files)
            # Take a video
            console.print("Capturing a video...")
            assert (await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)).ok
            await asyncio.sleep(args.record_time)
            assert (await gopro.http_command.set_shutter(shutter=constants.Toggle.DISABLE)).ok

            # Get the media set after
            media_set_after = set((await gopro.http_command.get_media_list()).data.files)
            # The video (is most likely) the difference between the two sets
            video = media_set_after.difference(media_set_before).pop()

            # Download the video and GPMF
            console.print(f"Downloading {video.filename}...")
            await gopro.http_command.download_file(
                camera_file=video.filename, local_file=args.output.with_suffix(".mp4")
            )
            await gopro.http_command.get_gpmf_data(
                camera_file=video.filename, local_file=args.output.with_suffix(".gpmf")
            )
            console.print(f"Success!! :smiley: File has been downloaded to {args.output}")
    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()
    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera, take a video, then download it.")
    parser.add_argument("-r", "--record_time", type=float, help="How long to record for", default=2.0)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Where to write the video to (not including file type). If not set, write to 'video'",
        default=Path("video"),
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
