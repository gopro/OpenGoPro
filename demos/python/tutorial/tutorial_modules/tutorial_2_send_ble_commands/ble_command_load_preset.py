# ble_command_load_preset.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:51 UTC 2021

import asyncio
import logging
import argparse
from binascii import hexlify

from bleak import BleakClient

from tutorial_modules import GOPRO_BASE_UUID, connect_ble

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


async def main(identifier):
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

    # Write to command request UUID to load the cinematic preset
    logger.info("Loading the cinematic preset...")
    event.clear()
    await client.write_gatt_char(COMMAND_REQ_UUID, bytearray([0x06, 0x40, 0x04, 0x00, 0x00, 0x00, 0x02]))
    await event.wait()  # Wait to receive the notification response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, then change the preset to Cinematic."
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
