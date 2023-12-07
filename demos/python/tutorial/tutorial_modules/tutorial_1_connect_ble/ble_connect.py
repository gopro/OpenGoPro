# ble_connect.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:56 PM

import re
import sys
import asyncio
import argparse
from typing import Dict, Any, List, Optional

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice as BleakDevice

from tutorial_modules import logger, noti_handler_T


def exception_handler(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    """Catch exceptions from non-main thread

    Args:
        loop (asyncio.AbstractEventLoop): loop to catch exceptions in
        context (Dict[str, Any]): exception context
    """
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception {str(loop)}: {msg}")
    logger.critical("This is unexpected and unrecoverable.")


async def connect_ble(notification_handler: noti_handler_T, identifier: Optional[str] = None) -> BleakClient:
    """Connect to a GoPro, then pair, and enable notifications

    If identifier is None, the first discovered GoPro will be connected to.

    Retry 10 times

    Args:
        notification_handler (noti_handler_T): callback when notification is received
        identifier (str, optional): Last 4 digits of GoPro serial number. Defaults to None.

    Raises:
        Exception: couldn't establish connection after retrying 10 times

    Returns:
        BleakClient: connected client
    """

    asyncio.get_event_loop().set_exception_handler(exception_handler)

    RETRIES = 10
    for retry in range(RETRIES):
        try:
            # Map of discovered devices indexed by name
            devices: Dict[str, BleakDevice] = {}

            # Scan for devices
            logger.info("Scanning for bluetooth devices...")

            # Scan callback to also catch nonconnectable scan responses
            # pylint: disable=cell-var-from-loop
            def _scan_callback(device: BleakDevice, _: Any) -> None:
                # Add to the dict if not unknown
                if device.name and device.name != "Unknown":
                    devices[device.name] = device

            # Scan until we find devices
            matched_devices: List[BleakDevice] = []
            while len(matched_devices) == 0:
                # Now get list of connectable advertisements
                for device in await BleakScanner.discover(timeout=5, detection_callback=_scan_callback):
                    if device.name != "Unknown" and device.name is not None:
                        devices[device.name] = device
                # Log every device we discovered
                for d in devices:
                    logger.info(f"\tDiscovered: {d}")
                # Now look for our matching device(s)
                token = re.compile(r"GoPro [A-Z0-9]{4}" if identifier is None else f"GoPro {identifier}")
                matched_devices = [device for name, device in devices.items() if token.match(name)]
                logger.info(f"Found {len(matched_devices)} matching devices.")

            # Connect to first matching Bluetooth device
            device = matched_devices[0]

            logger.info(f"Establishing BLE connection to {device}...")
            client = BleakClient(device)
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
                        await client.start_notify(char, notification_handler)
            logger.info("Done enabling notifications")

            return client
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error(f"Connection establishment failed: {exc}")
            logger.warning(f"Retrying #{retry}")

    raise RuntimeError(f"Couldn't establish BLE connection after {RETRIES} retries")


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
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
