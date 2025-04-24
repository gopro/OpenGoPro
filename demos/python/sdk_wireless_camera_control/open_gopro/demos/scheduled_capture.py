# scheduled_capture.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Apr 22 17:06:25 UTC 2025

"""Entrypoint for demonstrating a 15 second scheduled capture video 1 minute in the future."""

import argparse
import asyncio
import logging
from datetime import timedelta

from rich.console import Console

from open_gopro import WirelessGoPro, constants, proto
from open_gopro.gopro_base import GoProBase
from open_gopro.logger import set_stream_logging_level, setup_logging
from open_gopro.models.general import ScheduledCapture
from open_gopro.util import add_cli_args_and_parse, get_current_dst_aware_time

console = Console()


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: GoProBase | None = None

    try:
        async with WirelessGoPro(args.identifier, enable_wifi=False) as gopro:
            assert gopro
            set_stream_logging_level(logging.WARNING)

            console.print("Entering Video Mode")
            assert (await gopro.ble_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_VIDEO)).ok

            now, tz_offset, is_dst = get_current_dst_aware_time()
            console.print(f"Setting the camera's datetime to {now}")
            assert (await gopro.ble_command.set_date_time_tz_dst(date_time=now, tz_offset=tz_offset, is_dst=is_dst)).ok

            console.print("Getting the current scheduled capture value, just for demonstration.")
            current_scheduled_capture = await gopro.ble_setting.scheduled_capture.get_value()
            assert current_scheduled_capture.ok
            console.print(f"Current scheduled capture is: {current_scheduled_capture.data}")

            # Set the video duration
            console.print("Setting the video encoding duration to 15 seconds.")
            assert (await gopro.ble_setting.video_duration.set(constants.settings.VideoDuration.NUM_15_SECONDS)).ok

            # Configure scheduled capture for one minute in the future
            capture_time = now + timedelta(minutes=1)
            console.print(f"Scheduling a scheduled capture at {capture_time}")
            assert (
                await gopro.ble_setting.scheduled_capture.set(ScheduledCapture.from_datetime(capture_time, True))
            ).ok
            console.print("Scheduled capture is configured successfully :smiley:")
            console.print("Exiting...")

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE and configure a 15 second scheduled capture video for 1 minute in the future"
    )

    return add_cli_args_and_parse(parser, wifi=False)


if __name__ == "__main__":
    asyncio.run(main(parse_arguments()))
