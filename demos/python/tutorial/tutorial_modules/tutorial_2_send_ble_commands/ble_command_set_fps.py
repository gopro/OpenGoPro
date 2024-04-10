# ble_command_set_fps.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:58 PM

import sys
import asyncio
import argparse

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import connect_ble, logger, GoProUuid


async def main(identifier: str | None) -> None:
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    request_uuid = GoProUuid.SETTINGS_REQ_UUID
    response_uuid = GoProUuid.SETTINGS_RSP_UUID

    client: BleakClient

    async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid)
        logger.info(f'Received response at {uuid}: {data.hex(":")}')

        # If this is the correct handle and the status is success, the command was a success
        if uuid is response_uuid and data[2] == 0x00:
            logger.info("Command sent successfully")
        # Anything else is unexpected. This shouldn't happen
        else:
            logger.error("Unexpected response")

        # Notify the writer
        event.set()

    client = await connect_ble(notification_handler, identifier)

    # Write to command request BleUUID to change the fps to 240
    logger.info("Setting the fps to 240")
    request = bytes([0x03, 0x03, 0x01, 0x00])
    logger.debug(f"Writing to {request_uuid}: {request.hex(':')}")
    event.clear()
    await client.write_gatt_char(request_uuid.value, request, response=True)
    await event.wait()  # Wait to receive the notification response
    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera, then attempt to change the fps to 240.")
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to",
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
