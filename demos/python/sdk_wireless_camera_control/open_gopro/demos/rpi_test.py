"""RPI BLE Testing"""

import asyncio
from pathlib import Path

from rich.console import Console

from open_gopro import WirelessGoPro, constants
from open_gopro.logger import setup_logging

console = Console()


async def main() -> None:
    logger = setup_logging(__name__, Path("rpi_test.log"))

    gopro: WirelessGoPro | None = None

    try:
        async with WirelessGoPro(enable_wifi=False) as gopro:
            assert gopro
            await gopro.ble_command.set_shutter(shutter=constants.Toggle.ENABLE)

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()

if __name__ == "__main__":
    asyncio.run(main())
