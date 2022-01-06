# wifi_enable_and_connect.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:01 PM

import sys
import time
import asyncio
import logging
import argparse
from typing import Optional, Tuple

from bleak import BleakClient
from open_gopro.wifi.adapters import Wireless

from tutorial_modules import enable_wifi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


async def connect_wifi(identifier: str = None) -> Tuple[Wireless, BleakClient]:
    """Connect to a GoPro's WiFi AP

    Connect to a GoPro via BLE, find its WiFi AP SSID and password, enable its WiFI AP, then connect via WiFi

    Args:
        identifier (str, optional): Last 4 digits of GoPro serial number. Defaults to None.
    """

    ssid, password, client = await enable_wifi(identifier)

    # Now use the Open GoPro Python module to connect to the WiFi
    wifi = Wireless()
    logger.info("Connecting to GoPro WiFi AP")
    if wifi.connect(ssid, password):
        logger.info("Wifi Connected!")

    return wifi, client


async def main(identifier: Optional[str], timeout: Optional[int]) -> None:
    wifi, ble = await connect_wifi(identifier)

    if not timeout:
        logger.info("Maintaining WiFi Connection indefinitely. Send keyboard interrupt to exit.")
        while True:
            time.sleep(2)
    else:
        logger.info(f"Maintaining WiFi connection for {timeout} seconds")
        time.sleep(timeout)

    wifi.disconnect()
    await ble.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE, get WiFi info, enable WiFi and connect. \
            Send keyboard interrupt to exit."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. \
            If not used, first discovered GoPro will be connected to",
        default=None,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="time in seconds to maintain connection before disconnecting. If not set, will maintain connection indefinitely",
        default=None,
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(args.identifier, args.timeout))
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        sys.exit(-1)
    else:
        sys.exit(0)
