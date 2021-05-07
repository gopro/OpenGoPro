# ble_command_set_shutter.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:46 AM

import bleak
import time
import asyncio
import logging
import argparse
from binascii import hexlify

from bleak import BleakClient

from tutorial_modules import GOPRO_BASE_UUID, connect_ble

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def parse_arguments() -> str:
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, set the shutter, wait 2 seconds, then set the shutter off."
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


async def main():
    identifier = parse_arguments()

    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    # UUIDs to write to and receive responses from
    COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
    COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
    response_uuid = COMMAND_RSP_UUID

    client: BleakClient

    def notification_handler(handle: int, data: bytes) -> None:
        logger.info(f'Received response at {handle=}: {hexlify(data, ":")}')

        # If this is the correct handle and the status is success, the command was a success
        if client.services.characteristics[handle].uuid == response_uuid and data[2] == 0x00:
            logger.info("Command sent successfully")
        # Anything else is unexpected. This shouldn't happen
        else:
            logger.error("Unexpected response")

        # Notify the writer
        event.set()

    client = await connect_ble(notification_handler, identifier)

    # Write to command request UUID to turn the shutter on
    logger.info("Setting the shutter on")
    event.clear()
    await client.write_gatt_char(COMMAND_REQ_UUID, bytearray([3, 1, 1, 1]))
    await event.wait()  # Wait to receive the notification response

    time.sleep(2)  # If we're recording, let's wait 2 seconds (i.e. take a 2 second video)
    # Write to command request UUID to turn the shutter off
    logger.info("Setting the shutter off")
    event.clear()
    await client.write_gatt_char(COMMAND_REQ_UUID, bytearray([3, 1, 1, 0]))
    await event.wait()  # Wait to receive the notification response


if __name__ == "__main__":
    asyncio.run(main())
