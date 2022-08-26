# ble_connect.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:56 PM

import re
import enum
import sys
import asyncio
import argparse
from typing import Dict, Any, List, Callable, Optional

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice as BleakDevice

from tutorial_modules import logger


def exception_handler(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception {str(loop)}: {msg}")
    logger.critical("This is unexpected and unrecoverable.")


async def connect_ble(
    notification_handler: Callable[[int, bytes], None],
    identifier: Optional[str] = None,
) -> BleakClient:
    """Connect to a GoPro, then pair, and enable notifications

    If identifier is None, the first discovered GoPro will be connected to.

    Retry 10 times

    Args:
        notification_handler (Callable[[int, bytes], None]): callback when notification is received
        identifier (str, optional): Last 4 digits of GoPro serial number. Defaults to None.

    Raises:
        Exception: couldn't establish connection after retrying 10 times

    Returns:
        BleakClient: connected client
    """

    asyncio.get_event_loop().set_exception_handler(exception_handler)

    gopro_address: Optional[BleakDevice] = None
    client: Optional[BleakClient] = None

    RETRIES = 10
    for retry in range(1, RETRIES):
        try:
            # If we haven't yet found a ZGoPro
            if gopro_address is None:
                # Map of discovered devices indexed by name
                devices: Dict[str, BleakDevice] = {}

                def _scan_callback(device: BleakDevice, _: Any) -> None:
                    if device.name:
                        devices[device.name] = device
                        logger.info(f"\tDiscovered: {device}")

                # Now get list of advertisements that contain device name
                await BleakScanner().discover(detection_callback=_scan_callback)
                # Now look for our matching device
                token = re.compile(r"GoPro [A-Z0-9]{4}" if identifier is None else f"GoPro {identifier}")
                if not (matched_devices := [device for name, device in devices.items() if token.match(name)]):
                    raise Exception("Failed to find a GoPro")

                logger.info(f"Found {len(matched_devices)} matching devices.")
                # Connect to first matching Bluetooth device
                gopro_address = matched_devices[0]
            # We already found the device and are trying to connect
            else:
                logger.info(f"Establishing BLE connection to {gopro_address}...")
                client = BleakClient(gopro_address)
                await client.connect(timeout=15)
                logger.info("BLE Connected!")

                # Try to pair (on some OS's this will expectedly fail)
                logger.info("Attempting to pair...")
                try:
                    await client.pair()
                except NotImplementedError:
                    # This is expected on Mac
                    pass
                logger.info("Pairing complete!")

                # Enable notifications on all notifiable characteristics
                logger.info("Enabling notifications...")
                for service in client.services:
                    for char in service.characteristics:
                        if "notify" in char.properties:
                            logger.info(f"Enabling notification on char {char.uuid}")
                            await client.start_notify(char, notification_handler)  # type: ignore
                logger.info("Done enabling notifications")

            assert client
            return client
        except Exception as e:
            logger.error(f"Connection establishment failed: {e}")
            logger.warning(f"Retrying #{retry}")

    raise Exception(f"Couldn't establish BLE connection after {RETRIES} retries")


async def main(identifier: Optional[str]) -> None:
    def dummy_notification_handler(*_: Any) -> None:
        ...

    client = await connect_ble(dummy_notification_handler, identifier)
    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera, pair, then enable notifications.")
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. \
            If not used, first discovered GoPro will be connected to",
        default=None,
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(args.identifier))
    except Exception as e:
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
