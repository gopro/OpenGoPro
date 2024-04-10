# ble_query_poll_resolution_value.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:00 PM

import sys
import enum
import asyncio
import argparse

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GoProUuid, connect_ble, TlvResponse

from tutorial_modules import logger


# Note these may change based on the Open GoPro version!
class Resolution(enum.Enum):
    """Common Resolution Values"""

    RES_4K = 1
    RES_2_7K = 4
    RES_2_7K_4_3 = 6
    RES_1440 = 7
    RES_1080 = 9
    RES_4K_4_3 = 18
    RES_5K = 24


class QueryResponse(TlvResponse):
    """A TLV Response to a Query Operation.

    Args:
        uuid (GoProUuid): _description_
    """

    def __init__(self, uuid: GoProUuid) -> None:
        """Constructor"""
        super().__init__(uuid)
        self.data: dict[int, bytes] = {}

    def parse(self) -> None:
        """Perform common TLV parsing. Then also parse all Query elements into the data property"""
        super().parse()
        buf = bytearray(self.payload)
        while len(buf) > 0:
            # Get ID and Length of query parameter
            param_id = buf[0]
            param_len = buf[1]
            buf = buf[2:]
            # Get the value
            value = buf[:param_len]
            # Store in dict for later access
            self.data[param_id] = bytes(value)

            # Advance the buffer
            buf = buf[param_len:]


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
            # Reset per-uuid response
            responses_by_uuid[uuid] = QueryResponse(uuid)

    client = await connect_ble(notification_handler, identifier)

    # Write to query BleUUID to poll the current resolution
    logger.info("Getting the current resolution")
    request = bytes([0x02, 0x12, RESOLUTION_ID])
    logger.debug(f"Writing to {query_request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(query_request_uuid.value, request, response=True)
    # Wait to receive the notification response
    response = await received_responses.get()
    response.parse()
    resolution = Resolution(response.data[RESOLUTION_ID][0])
    logger.info(f"Resolution is currently {resolution}")

    # Write to command request BleUUID to change the video resolution (either to 1080 or 2.7K)
    target_resolution = Resolution.RES_2_7K if resolution is Resolution.RES_1080 else Resolution.RES_1080
    logger.info(f"Changing the resolution to {target_resolution}...")
    request = bytes([0x03, 0x02, 0x01, target_resolution.value])
    logger.debug(f"Writing to {setting_request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(setting_request_uuid.value, request, response=True)
    # Wait to receive the notification response
    response = await received_responses.get()
    response.parse()
    # Ensure the setting was successful
    assert response.status == 0x00

    # Now let's poll again until we see the update occur
    while resolution is not target_resolution:
        logger.info("Polling the resolution to see if it has changed...")
        request = bytes([0x02, 0x12, RESOLUTION_ID])
        logger.debug(f"Writing to {query_request_uuid}: {request.hex(':')}")
        await client.write_gatt_char(query_request_uuid.value, request, response=True)
        response = await received_responses.get()  # Wait to receive the notification response
        response.parse()
        resolution = Resolution(response.data[RESOLUTION_ID][0])
        logger.info(f"Resolution is currently {resolution}")

    logger.info("Resolution has changed as expected. Exiting...")

    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, get the current resolution, modify the resolution, and confirm the change was successful."
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
