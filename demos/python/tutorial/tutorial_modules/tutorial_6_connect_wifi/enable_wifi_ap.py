# wifi_enable.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:01 PM

import sys
import asyncio
import argparse

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GoProUuid, connect_ble, logger


async def enable_wifi(identifier: str | None = None) -> tuple[str, str, BleakClient]:
    """Connect to a GoPro via BLE, find its WiFi AP SSID and password, and enable its WiFI AP

    If identifier is None, the first discovered GoPro will be connected to.

    Args:
        identifier (str, optional): Last 4 digits of GoPro serial number. Defaults to None.

    Returns:
        Tuple[str, str]: ssid, password
    """
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()
    client: BleakClient

    async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid)
        logger.info(f'Received response at {uuid}: {data.hex(":")}')

        # If this is the correct handle and the status is success, the command was a success
        if uuid is GoProUuid.COMMAND_RSP_UUID and data[2] == 0x00:
            logger.info("Command sent successfully")
        # Anything else is unexpected. This shouldn't happen
        else:
            logger.error("Unexpected response")

        # Notify the writer
        event.set()

    client = await connect_ble(notification_handler, identifier)

    # Read from WiFi AP SSID BleUUID
    ssid_uuid = GoProUuid.WIFI_AP_SSID_UUID
    logger.info(f"Reading the WiFi AP SSID at {ssid_uuid}")
    ssid = (await client.read_gatt_char(ssid_uuid.value)).decode()
    logger.info(f"SSID is {ssid}")

    # Read from WiFi AP Password BleUUID
    password_uuid = GoProUuid.WIFI_AP_PASSWORD_UUID
    logger.info(f"Reading the WiFi AP password at {password_uuid}")
    password = (await client.read_gatt_char(password_uuid.value)).decode()
    logger.info(f"Password is {password}")

    # Write to the Command Request BleUUID to enable WiFi
    logger.info("Enabling the WiFi AP")
    event.clear()
    request = bytes([0x03, 0x17, 0x01, 0x01])
    command_request_uuid = GoProUuid.COMMAND_REQ_UUID
    logger.debug(f"Writing to {command_request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(command_request_uuid.value, request, response=True)
    await event.wait()  # Wait to receive the notification response
    logger.info("WiFi AP is enabled")

    return ssid, password, client


async def main(identifier: str | None, timeout: int | None) -> None:
    *_, client = await enable_wifi(identifier)

    if timeout:
        logger.info(f"Maintaining BLE connection for {timeout} seconds")
        await asyncio.sleep(timeout)
    else:
        input("Maintaining BLE Connection indefinitely. Press enter to exit.")

    logger.info("Disconnect from BLE...")
    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE, get its WiFi Access Point (AP) info, and enable its AP."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default \
            camera SSID. If not used, first discovered GoPro will be connected to",
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
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
