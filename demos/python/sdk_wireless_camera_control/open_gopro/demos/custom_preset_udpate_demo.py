# photo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Entrypoint for taking a picture demo."""

import argparse
import asyncio
from pathlib import Path

from rich.console import Console

from open_gopro import WiredGoPro, WirelessGoPro, proto
from open_gopro.gopro_base import GoProBase
from open_gopro.logger import setup_logging
from open_gopro.util import add_cli_args_and_parse

console = Console()


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)
    gopro: GoProBase | None = None

    try:
        async with (
            WiredGoPro(args.identifier)  # type: ignore
            if args.wired
            else WirelessGoPro(args.identifier, wifi_interface=args.wifi_interface)
        ) as gopro:
            assert gopro
            ble_last_file = (await gopro.ble_command.get_last_captured_media()).data
            http_last_file = (await gopro.http_command.get_last_captured_media()).data
            assert ble_last_file.media.folder == http_last_file.folder
            assert ble_last_file.media.file == http_last_file.file

            presets = (await gopro.ble_command.get_preset_status()).data
            custom_preset_id: int | None = None
            for group in presets.preset_group_array:
                for preset in group.preset_array:
                    if preset.user_defined:
                        custom_preset_id = preset.id
            if not custom_preset_id:
                raise RuntimeError("Could not find a custom preset.")
            # Ensure we can load it
            assert (await gopro.ble_command.load_preset(preset=custom_preset_id)).ok
            # Now try to update it
            assert (
                await gopro.ble_command.custom_preset_update(
                    icon_id=proto.EnumPresetTitle.PRESET_TITLE_BIKE,
                    title="custom title",
                )
            ).ok
            input("press enter to continue")
            assert (
                await gopro.ble_command.custom_preset_update(
                    icon_id=proto.EnumPresetTitle.PRESET_TITLE_MOTOR,
                    title=proto.EnumPresetTitle.PRESET_TITLE_MOTOR,
                )
            ).ok
            print("cheese")

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
