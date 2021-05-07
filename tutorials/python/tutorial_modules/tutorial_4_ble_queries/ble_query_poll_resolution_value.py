# ble_query_poll_resolution_value.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:48 AM

import enum
import asyncio
import logging
import argparse
from binascii import hexlify

from bleak import BleakClient

from tutorial_modules import GOPRO_BASE_UUID, connect_ble, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Resolution(enum.Enum):
    RES_4K = 1
    RES_2_7K = 4
    RES_2_7K_4_3 = 6
    RES_1440 = 7
    RES_1080 = 9
    RES_4K_4_3 = 18
    RES_5K = 24


def parse_arguments() -> str:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera then get the current resolution.")
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro name to scan for. If not used, first discovered GoPro will be connected to",
        default=None,
    )
    args = parser.parse_args()

    return args.identifier


resolution: Resolution


async def main():
    identifier = parse_arguments()

    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    # UUIDs to write to and receive responses from
    QUERY_REQ_UUID = GOPRO_BASE_UUID.format("0076")
    QUERY_RSP_UUID = GOPRO_BASE_UUID.format("0077")
    SETTINGS_REQ_UUID = GOPRO_BASE_UUID.format("0074")
    SETTINGS_RSP_UUID = GOPRO_BASE_UUID.format("0075")

    RESOLUTION_ID = 2

    client: BleakClient
    response = Response()

    def notification_handler(handle: int, data: bytes) -> None:
        logger.info(f'Received response at {handle=}: {hexlify(data, ":")}')

        response.accumulate(data)

        # Notify the writer if we have received the entire response
        if response.is_received:
            response.parse()

            # If this is query response, it must contain a resolution value
            if client.services.characteristics[handle].uuid == QUERY_RSP_UUID:
                global resolution
                resolution = Resolution(response.data[RESOLUTION_ID][0])
            # If this is a setting response, it will just show the status
            elif client.services.characteristics[handle].uuid == SETTINGS_RSP_UUID:
                logger.info("Command sent successfully")
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")

            # Notify writer that the procedure is complete
            event.set()

    client = await connect_ble(notification_handler, identifier)

    # Write to query UUID to poll the current resolution
    logger.info("Getting the current resolution")
    event.clear()
    await client.write_gatt_char(QUERY_REQ_UUID, bytearray([0x02, 0x12, RESOLUTION_ID]))
    await event.wait()  # Wait to receive the notification response
    logger.info(f"Resolution is currently {resolution}")

    # Write to command request UUID to change the video resolution (either to 1080 or 1440)
    new_resolution = Resolution.RES_1440 if resolution is Resolution.RES_1080 else Resolution.RES_1080
    logger.info(f"Changing the resolution to {new_resolution}...")
    event.clear()
    await client.write_gatt_char(SETTINGS_REQ_UUID, bytearray([0x03, 0x02, 0x01, new_resolution.value]))
    await event.wait()  # Wait to receive the notification response

    # Now let's poll again until we see the update occur
    while resolution is not new_resolution:
        logger.info("Polling the resolution to see if it has changed...")
        event.clear()
        await client.write_gatt_char(QUERY_REQ_UUID, bytearray([0x02, 0x12, RESOLUTION_ID]))
        await event.wait()  # Wait to receive the notification response
        logger.info(f"Resolution is currently {resolution}")


if __name__ == "__main__":
    asyncio.run(main())
