"""Entrypoint for demo displaying flow usage."""

import argparse
import asyncio
from pathlib import Path
from typing import Any

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.gopro_base import GoProBase
from open_gopro.models.constants.settings import SettingId, VideoResolution
from open_gopro.models.constants.statuses import StatusId
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging

console = Console()


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: GoProBase | None = None
    tasks: list[asyncio.Task] = []

    def handle_setting_updates(update: dict[SettingId, Any]) -> None:
        for setting, value in update.items():
            console.print(f"Setting value update: {setting} = {value}")

    def handle_status_updates(update: dict[StatusId, Any]) -> None:
        for status, value in update.items():
            console.print(f"Status update: {status} = {value}")

    def handle_setting_capability_updates(update: dict[SettingId, list]) -> None:
        for setting, value in update.items():
            console.print(f"Setting capability update: {setting} = {value}")

    try:
        # TODO
        async with WirelessGoPro(args.identifier) as gopro:
            setting_value_flow = (await gopro.ble_command.register_for_all_settings()).unwrap()
            setting_capability_flow = (await gopro.ble_command.register_for_all_capabilities()).unwrap()
            status_value_flow = (await gopro.ble_command.register_for_all_statuses()).unwrap()
            tasks.append(asyncio.create_task(setting_value_flow.collect(handle_setting_updates)))
            tasks.append(asyncio.create_task(status_value_flow.collect(handle_status_updates)))
            tasks.append(asyncio.create_task(setting_capability_flow.collect(handle_setting_capability_updates)))

            # Wait until resolution is set to 4k
            await setting_value_flow.first(lambda s: s.get(SettingId.VIDEO_RESOLUTION) == VideoResolution.NUM_1080)
            console.print("Exiting...")

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    finally:
        if gopro:
            await gopro.close()
        # Ensure tasks are properly cancelled and awaited
        for task in tasks:
            if not task.done():
                task.cancel()
        # Wait for all tasks to complete their cancellation
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


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
