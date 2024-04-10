# ble_query_poll_multiple_setting_values.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:00 PM

import sys
import enum
import asyncio
import argparse

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GoProUuid, connect_ble, QueryResponse, logger, Resolution


# Note these may change based on the Open GoPro version!
class FPS(enum.Enum):
    """Common Frames-per-second values"""

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
    """Common Video Field of View values"""

    FOV_WIDE = 0
    FOV_NARROW = 2
    FOV_SUPERVIEW = 3
    FOV_LINEAR = 4
    FOV_MAX_SUPERVIEW = 7
    FOV_LINEAR_HORIZON_LEVELING = 8


async def main(identifier: str | None) -> None:
    RESOLUTION_ID = 2
    FPS_ID = 3
    FOV_ID = 121

    client: BleakClient
    responses_by_uuid = GoProUuid.dict_by_uuid(value_creator=QueryResponse)
    received_responses: asyncio.Queue[QueryResponse] = asyncio.Queue()

    query_request_uuid = GoProUuid.QUERY_REQ_UUID
    query_response_uuid = GoProUuid.QUERY_RSP_UUID

    async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid)
        logger.info(f'Received response at {uuid}: {data.hex(":")}')

        response = responses_by_uuid[uuid]
        response.accumulate(data)

        # Notify the writer if we have received the entire response
        if response.is_received:
            # If this is query response, enqueue it
            if uuid is query_response_uuid:
                logger.info("Received the Query Response")
                await received_responses.put(response)
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")
            # Reset the per-uuuid response
            responses_by_uuid[uuid] = QueryResponse(uuid)

    client = await connect_ble(notification_handler, identifier)

    # Write to query BleUUID to poll the current resolution, fps, and fov
    logger.info("Getting the current resolution, fps, and fov.")
    request = bytes([0x04, 0x12, RESOLUTION_ID, FPS_ID, FOV_ID])
    logger.debug(f"Writing to {query_request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(query_request_uuid.value, request, response=True)
    response = await received_responses.get()  # Wait to receive the notification response
    # Parse Query headers and query items
    response.parse()
    logger.info(f"Resolution is currently {Resolution(response.data[RESOLUTION_ID][0])}")
    logger.info(f"Video FOV is currently {VideoFOV(response.data[FOV_ID][0])}")
    logger.info(f"FPS is currently {FPS(response.data[FPS_ID][0])}")

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
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
