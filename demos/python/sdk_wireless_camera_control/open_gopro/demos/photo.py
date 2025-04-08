# photo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Entrypoint for taking a picture demo."""

import argparse
import asyncio
from pathlib import Path
from typing import Any

from rich.console import Console

from open_gopro import WiredGoPro, WirelessGoPro, constants, proto
from open_gopro.gopro_base import GoProBase
from open_gopro.logger import setup_logging
from open_gopro.types import UpdateType
from open_gopro.util import add_cli_args_and_parse, ainput

console = Console()


async def status_handler(update: UpdateType, value: Any) -> None:
    console.print(f"Received status ({update}) ==> {value}")


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: GoProBase | None = None

    try:
        async with WirelessGoPro(enable_wifi=False) as gopro:
            assert gopro

            await gopro.ble_command.register_for_all_settings(callback=status_handler)

            await ainput("Press enter to unregister...")
            await gopro.ble_command.unregister_for_all_settings(callback=status_handler)

            await ainput("Press enter to exit...")

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
