# ble_command_get_version.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:59 PM

import sys
import asyncio
import argparse
from typing import Dict, Optional

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GOPRO_BASE_UUID, connect_ble, logger


async def main(identifier: Optional[str]) -> None:
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    # UUIDs to write to and receive responses from
    COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
    COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
    response_uuid = COMMAND_RSP_UUID

    client: BleakClient

    def notification_handler(characteristic: BleakGATTCharacteristic, data: bytes) -> None:
        logger.info(f'Received response at handle {characteristic.handle}: {data.hex(":")}')

        # If this is the correct handle and the status is success, the command was a success
        if client.services.characteristics[characteristic.handle].uuid == response_uuid:
            # First byte is the length for this command.
            length = data[0]
            # Second byte is the ID
            command_id = data[1]
            # Third byte is the status
            status = data[2]
            index = 3
            params = []
            # Remaining bytes are individual values of (length...length bytes)
            while index <= length:
                param_len = data[index]
                index += 1
                params.append(data[index : index + param_len])
                index += param_len
            major, minor = params

            logger.info(f"Received a response to {command_id=} with {status=}")
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
    await client.write_gatt_char(COMMAND_REQ_UUID, bytearray([0x01, 0x51]), response=True)
    await event.wait()  # Wait to receive the notification response

    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE, then get the Open GoPro version."
    )
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
    except Exception as e:
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
