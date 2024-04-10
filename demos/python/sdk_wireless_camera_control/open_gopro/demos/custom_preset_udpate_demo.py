# custom_preset_udpate_demo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Mar 28 20:25:41 UTC 2024

"""Simple demo to modify a currently accessible custom preset's title and icon."""

import asyncio
from pathlib import Path

from rich.console import Console

from open_gopro import WiredGoPro, proto
from open_gopro.logger import setup_logging

console = Console()


async def main() -> None:
    logger = setup_logging(__name__, Path("custom_preset.log"))
    gopro: WiredGoPro | None = None

    try:
        async with WiredGoPro() as gopro:
            presets = (await gopro.http_command.get_preset_status()).data
            custom_preset_id: int | None = None
            for group in presets["presetGroupArray"]:
                for preset in group["presetArray"]:
                    if preset["userDefined"]:
                        custom_preset_id = preset["id"]
            if not custom_preset_id:
                raise RuntimeError("Could not find a custom preset.")
            # Ensure we can load it
            assert (await gopro.http_command.load_preset(preset=custom_preset_id)).ok
            # Now try to update it
            assert (
                await gopro.http_command.update_custom_preset(
                    icon_id=proto.EnumPresetIcon.PRESET_ICON_SNOW,
                    title_id=proto.EnumPresetTitle.PRESET_TITLE_SNOW,
                )
            ).ok
            input("press enter to continue")
            assert (
                await gopro.http_command.update_custom_preset(
                    icon_id=proto.EnumPresetIcon.PRESET_ICON_MOTOR,
                    title_id=proto.EnumPresetTitle.PRESET_TITLE_MOTOR,
                )
            ).ok
            input("press enter to continue")
            assert (
                await gopro.http_command.update_custom_preset(
                    custom_name="Custom Name",
                    icon_id=proto.EnumPresetIcon.PRESET_ICON_BIKE,
                    title_id=proto.EnumPresetTitle.PRESET_TITLE_USER_DEFINED_CUSTOM_NAME,
                )
            ).ok

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()


if __name__ == "__main__":
    asyncio.run(main())
