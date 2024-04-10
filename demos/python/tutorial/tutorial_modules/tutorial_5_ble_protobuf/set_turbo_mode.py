# set_turbo_mode.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:49 UTC 2024

import sys
import asyncio
import argparse

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from google.protobuf.message import Message as ProtobufMessage

from tutorial_modules import logger
from tutorial_modules import GoProUuid, connect_ble, Response, proto


class ProtobufResponse(Response):
    """Accumulate and parse protobuf responses"""

    def __init__(self, uuid: GoProUuid) -> None:
        super().__init__(uuid)
        self.feature_id: int
        self.action_id: int
        self.uuid = uuid
        self.data: ProtobufMessage

    def parse(self, proto_message: type[ProtobufMessage]) -> None:
        """Set the responses data by parsing using the passed in protobuf container

        Args:
            proto_message (type[ProtobufMessage]): protobuf container to use for parsing
        """
        self.feature_id = self.raw_bytes[0]
        self.action_id = self.raw_bytes[1]
        self.data = proto_message.FromString(bytes(self.raw_bytes[2:]))


async def main(identifier: str | None) -> None:
    client: BleakClient
    responses_by_uuid = GoProUuid.dict_by_uuid(ProtobufResponse)
    received_responses: asyncio.Queue[ProtobufResponse] = asyncio.Queue()

    request_uuid = GoProUuid.COMMAND_REQ_UUID
    response_uuid = GoProUuid.COMMAND_RSP_UUID

    async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid)
        logger.info(f"Received response at UUID {uuid}: {data.hex(':')}")

        response = responses_by_uuid[uuid]
        response.accumulate(data)

        # Notify the writer if we have received the entire response
        if response.is_received:
            # The turbo mode response will come on the Command Response characteristic
            if uuid is response_uuid:
                logger.info("Set Turbo Mode response complete received.")
                # Notify writer that the procedure is complete
                await received_responses.put(response)
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")
            # Reset the per-uuid Response
            responses_by_uuid[uuid] = ProtobufResponse(uuid)

    client = await connect_ble(notification_handler, identifier)

    logger.info("Setting Turbo Mode off.")

    # Build raw bytes request from feature / action IDs and serialized protobuf message
    turbo_mode_request = bytearray(
        [
            0xF1,  # Feature ID
            0x6B,  # Action ID
            *proto.RequestSetTurboActive(active=False).SerializeToString(),
        ]
    )
    turbo_mode_request.insert(0, len(turbo_mode_request))

    # Write to command request UUID to enable turbo mode
    logger.info(f"Writing {turbo_mode_request.hex(':')} to {request_uuid}")
    await client.write_gatt_char(request_uuid.value, turbo_mode_request, response=True)

    # Wait to receive the response, then parse it
    response = await received_responses.get()
    response.parse(proto.ResponseGeneric)
    # Deserialize into protobuf message
    assert response.feature_id == 0xF1
    assert response.action_id == 0xEB
    logger.info("Successfully set turbo mode")
    logger.info(response.data)

    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, send Set Turbo Mode and parse the response"
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
