# wifi_enable_and_connect.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:49 AM

import asyncio
import logging
import argparse

from tutorial_modules import GOPRO_BASE_UUID, enable_wifi
from open_gopro.wifi_controller import Wireless

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def parse_arguments() -> str:
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE, get WiFi info, enable WiFi and connect."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro name to scan for. If not used, first discovered GoPro will be connected to",
        default=None,
    )
    args = parser.parse_args()

    return args.identifier


async def connect_wifi(identifier: str = None) -> None:
    """Connect to a GoPro's WiFi AP

    Connect to a GoPro via BLE, find its WiFi AP SSID and password, enable its WiFI AP, then connect via WiFi

    Args:
        identifier (str, optional): Last 4 digits of GoPro serial number. Defaults to None.
    """

    ssid, password = await enable_wifi(identifier)

    # Now use the Open GoPro Python module to connect to the WiFi
    wifi = Wireless()
    logger.info("Connecting to GoPro WiFi AP")
    if wifi.connect(ssid, password):
        logger.info("Wifi Connected!")


async def main():
    identifier = parse_arguments()

    await connect_wifi(identifier)


if __name__ == "__main__":
    asyncio.run(main())
