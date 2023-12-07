# ble_query_poll_multiple_setting_values.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
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


# Note these may change based on the Open GoPro version!
class Resolution(enum.Enum):
    RES_4K = 1
    RES_2_7K = 4
    RES_2_7K_4_3 = 6
    RES_1440 = 7
    RES_1080 = 9
    RES_4K_4_3 = 18
    RES_5K = 24


# Note these may change based on the Open GoPro version!
class FPS(enum.Enum):
    FPS_240 = 0
    FPS_120 = 1
    FPS_100 = 2
    FPS_60 = 6
    FPS_30 = 8
    FPS_25 = 9
    FPS_24 = 10
    FPS_200 = 13


# Note these may change based on the Open GoPro version!
class VideoFOV(enum.Enum):
    FOV_WIDE = 0
    FOV_NARROW = 2
    FOV_SUPERVIEW = 3
    FOV_LINEAR = 4
    FOV_MAX_SUPERVIEW = 7
    FOV_LINEAR_HORIZON_LEVELING = 8


resolution: Resolution
fps: FPS
video_fov: VideoFOV


async def main(identifier: Optional[str]) -> None:
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    # UUIDs to write to and receive responses from
    QUERY_REQ_UUID = GOPRO_BASE_UUID.format("0076")
    QUERY_RSP_UUID = GOPRO_BASE_UUID.format("0077")
    SETTINGS_REQ_UUID = GOPRO_BASE_UUID.format("0074")
    SETTINGS_RSP_UUID = GOPRO_BASE_UUID.format("0075")

    RESOLUTION_ID = 2
    FPS_ID = 3
    FOV_ID = 121

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
                global fps
                global video_fov
                resolution = Resolution(response.data[RESOLUTION_ID][0])
                fps = FPS(response.data[FPS_ID][0])
                video_fov = VideoFOV(response.data[FOV_ID][0])
            # If this is a setting response, it will just show the status
            elif client.services.characteristics[characteristic.handle].uuid == SETTINGS_RSP_UUID:
                logger.info("Command sent successfully")
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")

            # Notify writer that the procedure is complete
            event.set()

    client = await connect_ble(notification_handler, identifier)

    # Write to query BleUUID to poll the current resolution, fps, and fov
    logger.info("Getting the current resolution, fps, and fov,")
    event.clear()
    await client.write_gatt_char(
        QUERY_REQ_UUID, bytearray([0x04, 0x12, RESOLUTION_ID, FPS_ID, FOV_ID]), response=True
    )
    await event.wait()  # Wait to receive the notification response
    logger.info(f"Resolution is currently {resolution}")
    logger.info(f"Video FOV is currently {video_fov}")
    logger.info(f"FPS is currently {fps}")

    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera then get the current resolution, fps, and fov."
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
