import asyncio
from pathlib import Path

from open_gopro import WirelessGoPro
from open_gopro.logger import setup_logging


async def main() -> None:
    logger = setup_logging(__name__, Path("demo.log"))

    gopro: WirelessGoPro | None = None
    async with WirelessGoPro(enable_wifi=False) as gopro:
        logger.critical("Set AP Mode on")
        await gopro.ble_command.enable_wifi_ap(enable=True)

        logger.critical("Wait 10 seconds")
        await asyncio.sleep(10)

        logger.critical("Initiate AP scan")
        await gopro.ble_command.scan_wifi_networks()

        logger.critical("Wait 5 minutes before disconnecting")
        await asyncio.sleep(300)

    if gopro:
        await gopro.close()


def entrypoint() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    entrypoint()
