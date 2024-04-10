# ble_query_register_resolution_value_updates.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:00 PM

import sys
import asyncio
import argparse

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GoProUuid, connect_ble, QueryResponse, Resolution

from tutorial_modules import logger


async def main(identifier: str | None) -> None:
    RESOLUTION_ID = 2

    client: BleakClient
    responses_by_uuid = GoProUuid.dict_by_uuid(QueryResponse)
    received_responses: asyncio.Queue[QueryResponse] = asyncio.Queue()

    query_request_uuid = GoProUuid.QUERY_REQ_UUID
    query_response_uuid = GoProUuid.QUERY_RSP_UUID
    setting_request_uuid = GoProUuid.SETTINGS_REQ_UUID
    setting_response_uuid = GoProUuid.SETTINGS_RSP_UUID

    async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid)
        logger.info(f'Received response at {uuid}: {data.hex(":")}')

        response = responses_by_uuid[uuid]
        response.accumulate(data)

        # Notify the writer if we have received the entire response
        if response.is_received:
            # If this is query response, it must contain a resolution value
            if uuid is query_response_uuid:
                logger.info("Received the Resolution Query response")
                await received_responses.put(response)
            # If this is a setting response, it will just show the status
            elif uuid is setting_response_uuid:
                logger.info("Received Set Setting command response.")
                await received_responses.put(response)
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")
            # Reset the per-uuid response
            responses_by_uuid[uuid] = QueryResponse(uuid)

    client = await connect_ble(notification_handler, identifier)

    # Register for updates when resolution value changes
    logger.info("Registering for resolution updates")
    request = bytes([0x02, 0x52, RESOLUTION_ID])
    logger.debug(f"Writing to {query_request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(query_request_uuid.value, request, response=True)
    # Wait to receive the notification response
    response = await received_responses.get()
    response.parse()
    logger.info("Successfully registered for resolution value updates.")
    resolution = Resolution(response.data[RESOLUTION_ID][0])
    logger.info(f"Resolution is currently {resolution}")

    # Write to command request BleUUID to change the video resolution (either to 1080 or 2.7K)
    new_resolution = Resolution.RES_2_7K if resolution is Resolution.RES_1080 else Resolution.RES_1080
    logger.info(f"Changing the resolution to {new_resolution}...")
    request = bytes([0x03, 0x02, 0x01, new_resolution.value])
    logger.debug(f"Writing to {setting_request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(setting_request_uuid.value, request, response=True)
    # Wait to receive the notification response
    response = await received_responses.get()
    response.parse()
    # Ensure the setting was successful
    assert response.status == 0x00

    # Let's verify we got the update
    logger.info("Waiting to receive new resolution")
    while resolution is not new_resolution and (response := await received_responses.get()):
        response.parse()
        resolution = Resolution(response.data[RESOLUTION_ID][0])
        logger.info(f"Resolution is currently {resolution}")

    logger.info("Resolution has changed as expected. Exiting...")

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
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
