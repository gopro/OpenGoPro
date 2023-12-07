# ble_query_register_resolution_value_updates.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:00 PM

import sys
import enum
import asyncio
import argparse
from typing import Optional

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GOPRO_BASE_UUID, connect_ble, Response

from tutorial_modules import logger


# Note that this may change based on the Open GoPro version!
class Resolution(enum.Enum):
    RES_4K = 1
    RES_2_7K = 4
    RES_2_7K_4_3 = 6
    RES_1080 = 9
    RES_4K_4_3 = 18
    RES_5K = 24


resolution: Resolution


async def main(identifier: Optional[str]) -> None:
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    # UUIDs to write to and receive responses from
    SETTINGS_REQ_UUID = GOPRO_BASE_UUID.format("0074")
    SETTINGS_RSP_UUID = GOPRO_BASE_UUID.format("0075")
    QUERY_REQ_UUID = GOPRO_BASE_UUID.format("0076")
    QUERY_RSP_UUID = GOPRO_BASE_UUID.format("0077")

    RESOLUTION_ID = 2

    client: BleakClient
    response = Response()

    def notification_handler(characteristic: BleakGATTCharacteristic, data: bytes) -> None:
        logger.info(f'Received response at handle {characteristic.handle}: {data.hex(":")}')

        response.accumulate(data)

        # Notify the writer if we have received the entire response
        if response.is_received:
            response.parse()

            # If this is query response, it must contain a resolution value
            if client.services.characteristics[characteristic.handle].uuid == QUERY_RSP_UUID:
                global resolution
                resolution = Resolution(response.data[RESOLUTION_ID][0])
            # If this is a setting response, it will just show the status
            elif client.services.characteristics[characteristic.handle].uuid == SETTINGS_RSP_UUID:
                logger.info("Command sent successfully")
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")

            # Notify writer that the procedure is complete
            event.set()

    client = await connect_ble(notification_handler, identifier)

    # Register for updates when resolution value changes
    logger.info("Registering for resolution updates")
    event.clear()
    await client.write_gatt_char(QUERY_REQ_UUID, bytearray([0x02, 0x52, RESOLUTION_ID]), response=True)
    await event.wait()  # Wait to receive the notification response
    logger.info("Successfully registered for resolution value updates.")
    logger.info(f"Resolution is currently {resolution}")

    # Write to command request BleUUID to change the video resolution (either to 1080 or 2.7K)
    new_resolution = Resolution.RES_2_7K if resolution is Resolution.RES_1080 else Resolution.RES_1080
    logger.info(f"Changing the resolution to {new_resolution}...")
    event.clear()
    await client.write_gatt_char(
        SETTINGS_REQ_UUID, bytearray([0x03, 0x02, 0x01, new_resolution.value]), response=True
    )
    await event.wait()  # Wait to receive the notification response
    logger.info("Successfully changed the resolution")

    # Let's verify we got the update
    while resolution is not new_resolution:
        event.clear()
        await event.wait()
    logger.info(f"Resolution is now {resolution}")

    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, register for updates to the resolution, receive the current resolution, modify the resolution, and confirm receipt of the change notification."
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
