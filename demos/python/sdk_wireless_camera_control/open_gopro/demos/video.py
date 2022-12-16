# video.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:46 PM

"""Entrypoint for taking a video demo."""

import time
import argparse
from pathlib import Path
from typing import Optional, Union

from rich.console import Console

from open_gopro import WirelessGoPro, WiredGoPro, Params
from open_gopro.util import setup_logging, add_cli_args_and_parse

console = Console()  # rich consoler printer


def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)
    gopro: Optional[Union[WirelessGoPro, WiredGoPro]] = None

    try:
        with (
            WiredGoPro(args.identifier)  # type: ignore
            if args.wired
            else WirelessGoPro(args.identifier, wifi_interface=args.wifi_interface)
        ) as gopro:
            assert gopro
            # Configure settings to prepare for video
            if gopro.is_encoding:
                gopro.http_command.set_shutter(shutter=Params.Toggle.DISABLE)
            gopro.http_setting.video_performance_mode.set(Params.PerformanceMode.MAX_PERFORMANCE)
            gopro.http_setting.max_lens_mode.set(Params.MaxLensMode.DEFAULT)
            gopro.http_setting.camera_ux_mode.set(Params.CameraUxMode.PRO)
            gopro.http_command.set_turbo_mode(mode=Params.Toggle.DISABLE)
            assert gopro.http_command.load_preset_group(group=Params.PresetGroup.VIDEO).is_ok

            # Get the media list before
            media_set_before = set(x["n"] for x in gopro.http_command.get_media_list().flatten)
            # Take a video
            console.print("Capturing a video...")
            assert gopro.http_command.set_shutter(shutter=Params.Toggle.ENABLE).is_ok
            time.sleep(args.record_time)
            assert gopro.http_command.set_shutter(shutter=Params.Toggle.DISABLE).is_ok

            # Get the media list after
            media_set_after = set(x["n"] for x in gopro.http_command.get_media_list().flatten)
            # The video (is most likely) the difference between the two sets
            video = media_set_after.difference(media_set_before).pop()
            # Download the video
            console.print("Downloading the video...")
            gopro.http_command.download_file(camera_file=video, local_file=args.output)
            console.print(f"Success!! :smiley: File has been downloaded to {args.output}")
    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        gopro.close()
    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera, take a video, then download it.")
    parser.add_argument(
        "record_time",
        type=float,
        help="How long to record for",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Where to write the video to. If not set, write to 'video.mp4'",
        default=Path("video.mp4"),
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
