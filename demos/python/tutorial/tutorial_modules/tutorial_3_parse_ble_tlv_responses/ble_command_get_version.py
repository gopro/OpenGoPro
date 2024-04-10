# ble_command_get_version.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:59 PM

import sys
import asyncio
import argparse

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GoProUuid, connect_ble, logger


async def main(identifier: str | None) -> None:
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    client: BleakClient

    request_uuid = GoProUuid.COMMAND_REQ_UUID
    response_uuid = GoProUuid.COMMAND_RSP_UUID

    async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid)
        logger.info(f'Received response {uuid}: {data.hex(":")}')

        # If this is the correct handle and the status is success, the command was a success
        if uuid is response_uuid:
            # First byte is the length of this response.
            length = data[0]
            # Second byte is the ID
            command_id = data[1]
            # Third byte is the status
            status = data[2]
            # The remainder is the payload
            payload = data[3 : length + 1]
            logger.info(f"Received a response to {command_id=} with {status=}, payload={payload.hex(':')}")

            # Now parse the payload from the response documentation
            major_length = payload[0]
            payload.pop(0)
            major = payload[:major_length]
            payload.pop(major_length)
            minor_length = payload[0]
            payload.pop(0)
            minor = payload[:minor_length]
            logger.info(f"The version is Open GoPro {major[0]}.{minor[0]}")

        # Anything else is unexpected. This shouldn't happen
        else:
            logger.error("Unexpected response")

        # Notify the writer if we have received the entire response
        event.set()

    client = await connect_ble(notification_handler, identifier)

    # Write to command request BleUUID to get the Open GoPro Version
    logger.info("Getting the Open GoPro version...")
    event.clear()
    request = bytes([0x01, 0x51])
    logger.debug(f"Writing to {request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(request_uuid.value, request, response=True)
    await event.wait()  # Wait to receive the notification response
    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera via BLE, then get the Open GoPro version.")
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
