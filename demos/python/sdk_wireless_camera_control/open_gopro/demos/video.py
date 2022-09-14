# video.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:46 PM

"""Entrypoint for taking a video demo."""

import time
import argparse
from pathlib import Path
from typing import Optional

from rich.console import Console

from open_gopro import GoPro, Params
from open_gopro.util import setup_logging, add_cli_args_and_parse

console = Console()  # rich consoler printer


def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)
    gopro: Optional[GoPro] = None

    with GoPro(args.identifier, wifi_interface=args.wifi_interface, sudo_password=args.password) as gopro:
        # Configure settings to prepare for video
        if gopro.is_encoding:
            gopro.ble_command.set_shutter(Params.Toggle.DISABLE)
        gopro.ble_setting.video_performance_mode.set(Params.PerformanceMode.MAX_PERFORMANCE)
        gopro.ble_setting.max_lens_mode.set(Params.MaxLensMode.DEFAULT)
        gopro.ble_setting.camera_ux_mode.set(Params.CameraUxMode.PRO)
        gopro.ble_command.set_turbo_mode(False)
        assert gopro.ble_command.load_preset_group(Params.PresetGroup.VIDEO).is_ok

        # Get the media list before
        media_set_before = set(x["n"] for x in gopro.wifi_command.get_media_list().flatten)
        # Take a video
        console.print("Capturing a video...")
        assert gopro.ble_command.set_shutter(Params.Toggle.ENABLE).is_ok
        time.sleep(args.record_time)
        assert gopro.ble_command.set_shutter(Params.Toggle.DISABLE).is_ok

        # Get the media list after
        media_set_after = set(x["n"] for x in gopro.wifi_command.get_media_list().flatten)
        # The video (is most likely) the difference between the two sets
        video = media_set_after.difference(media_set_before).pop()
        # Download the video
        console.print("Downloading the video...")
        gopro.wifi_command.download_file(camera_file=video, local_file=args.output)
        console.print(f"Success!! :smiley: File has been downloaded to {args.output}")

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
    return add_cli_args_and_parse(parser)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
