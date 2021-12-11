# wifi_enable_and_connect.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:01 PM

import asyncio
import logging
import argparse

from tutorial_modules import GOPRO_BASE_UUID, enable_wifi
try:
    from open_gopro.wifi_controller import Wireless
except:
    from open_gopro.wifi.adapters.wireless import Wireless

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


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
    if wifi.connect(ssid, password, timeout=30):
        logger.info("Wifi Connected!")


async def main(identifier):
    await connect_wifi(identifier)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE, get WiFi info, enable WiFi and connect."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to",
        default=None,
    )
    args = parser.parse_args()

    asyncio.run(main(args.identifier))
