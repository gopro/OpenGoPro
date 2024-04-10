# set_turbo_mode.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:49 UTC 2024

from __future__ import annotations
import sys
import asyncio
import argparse
from dataclasses import dataclass
from typing import TypeAlias, cast

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from google.protobuf.message import Message as ProtobufMessage

from tutorial_modules import logger, proto
from tutorial_modules import GoProUuid, connect_ble, Response, QueryResponse, TlvResponse, ProtobufResponse, Resolution

RESOLUTION_ID = 2


@dataclass(frozen=True)
class ProtobufId:
    """Protobuf feature / action identifier pair."""

    feature_id: int
    action_id: int


# From https://gopro.github.io/OpenGoPro/ble/protocol/id_tables.html#protobuf-ids
# TODO automatically generate this and fill out all messages.
ProtobufIdToMessage: dict[ProtobufId, type[ProtobufMessage] | None] = {
    ProtobufId(0x02, 0x02): None,
    ProtobufId(0x02, 0x04): None,
    ProtobufId(0x02, 0x05): None,
    ProtobufId(0x02, 0x0B): proto.NotifStartScanning,
    ProtobufId(0x02, 0x0C): proto.NotifProvisioningState,
    ProtobufId(0x02, 0x82): proto.ResponseStartScanning,
    ProtobufId(0x02, 0x83): proto.ResponseGetApEntries,
    ProtobufId(0x02, 0x84): proto.ResponseConnect,
    ProtobufId(0x02, 0x85): proto.ResponseConnectNew,
    ProtobufId(0xF1, 0x64): None,
    ProtobufId(0xF1, 0x65): None,
    ProtobufId(0xF1, 0x66): None,
    ProtobufId(0xF1, 0x67): None,
    ProtobufId(0xF1, 0x69): None,
    ProtobufId(0xF1, 0x6B): None,
    ProtobufId(0xF1, 0x79): None,
    ProtobufId(0xF1, 0xE4): None,
    ProtobufId(0xF1, 0xE5): None,
    ProtobufId(0xF1, 0xE6): proto.ResponseGeneric,
    ProtobufId(0xF1, 0xE7): proto.ResponseGeneric,
    ProtobufId(0xF1, 0xE9): None,
    ProtobufId(0xF1, 0xEB): proto.ResponseGeneric,
    ProtobufId(0xF1, 0xF9): None,
    ProtobufId(0xF5, 0x6D): None,
    ProtobufId(0xF5, 0x6E): None,
    ProtobufId(0xF5, 0x6F): None,
    ProtobufId(0xF5, 0x72): None,
    ProtobufId(0xF5, 0x74): None,
    ProtobufId(0xF5, 0xED): None,
    ProtobufId(0xF5, 0xEE): proto.ResponseCOHNCert,
    ProtobufId(0xF5, 0xEF): proto.ResponseGeneric,
    ProtobufId(0xF5, 0xEF): proto.NotifyCOHNStatus,
    ProtobufId(0xF5, 0xF2): None,
    ProtobufId(0xF5, 0xF3): None,
    ProtobufId(0xF5, 0xF4): None,
    ProtobufId(0xF5, 0xF5): None,
}

ConcreteResponse: TypeAlias = ProtobufResponse | QueryResponse | TlvResponse


class ResponseManager:
    """A wrapper around a BleakClient to manage accumulating, parsing, and retrieving responses.

    Before use, the client must be set via the `set_client` method.
    """

    def __init__(self) -> None:
        """Constructor"""

        self._responses_by_uuid = GoProUuid.dict_by_uuid(Response)
        self._q: asyncio.Queue[ConcreteResponse] = asyncio.Queue()
        self._client: BleakClient | None = None

    def set_client(self, client: BleakClient) -> None:
        """Set the client. This is required before use.

        Args:
            client (BleakClient): bleak client to use for this manager instance.
        """
        self._client = client

    @property
    def is_initialized(self) -> bool:
        """Has the client been set yet?

        Returns:
            bool: True if the client is set. False otherwise.
        """
        return self._client is not None

    @property
    def client(self) -> BleakClient:
        """Get the client. This property assumes that the client has already been set

        Raises:
            RuntimeError: Client has not yet been set.

        Returns:
            BleakClient: Client associated with this manager.
        """
        if not self.is_initialized:
            raise RuntimeError("Client has not been set")
        return self._client  # type: ignore

    def decipher_response(self, undeciphered_response: Response) -> ConcreteResponse:
        """Given an undeciphered and unparsed response, decipher its type and parse as much of its payload as is feasible.

        Args:
            undeciphered_response (Response): input response to decipher

        Raises:
            RuntimeError: Found a Protobuf Response that does not have a defined message for its Feature / Action ID

        Returns:
            ConcreteResponse: deciphered and parsed response
        """
        payload = undeciphered_response.raw_bytes
        # Are the first two payload bytes a real Fetaure / Action ID pair?
        response: Response
        if (index := ProtobufId(payload[0], payload[1])) in ProtobufIdToMessage:
            if not (proto_message := ProtobufIdToMessage.get(index)):
                # We've only added protobuf messages for operations used in this tutorial.
                raise RuntimeError(
                    f"{index} is a valid Protobuf identifier but does not currently have a defined message."
                )
            # Now use the protobuf messaged identified by the Feature / Action ID pair to parse the remaining payload
            response = ProtobufResponse.from_received_response(undeciphered_response)
            response.parse(proto_message)
            return response
        # TLV. Should it be parsed as Command or Query?
        if undeciphered_response.uuid is GoProUuid.QUERY_RSP_UUID:
            # It's a TLV query
            response = QueryResponse.from_received_response(undeciphered_response)
        else:
            # It's a TLV command / setting.
            response = TlvResponse.from_received_response(undeciphered_response)
        # Parse the TLV payload (query, command, or setting)
        response.parse()
        return response

    async def notification_handler(self, characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        """Notification handler to use for the bleak client.

        Args:
            characteristic (BleakGATTCharacteristic): characteristic notification was received on
            data (bytearray): byte data of notification.
        """
        uuid = GoProUuid(self.client.services.characteristics[characteristic.handle].uuid)
        logger.debug(f'Received response at {uuid}: {data.hex(":")}')

        response = self._responses_by_uuid[uuid]
        response.accumulate(data)

        # Enqueue if we have received the entire response
        if response.is_received:
            await self._q.put(self.decipher_response(response))
            # Reset the accumulating response
            self._responses_by_uuid[uuid] = Response(uuid)

    @classmethod
    def assert_generic_protobuf_success(cls, response: ProtobufMessage) -> None:
        """Helper method to assert that a ResponseGeneric is successful

        Args:
            response (ProtobufMessage): GenericResponse. This must be of type proto.ResponseGeneric

        Raises:
            TypeError: response is not of type proto.ResponseGeneric
        """
        generic_response = cast(proto.ResponseGeneric, response)
        if (result := int(generic_response.result)) != int(proto.EnumResultGeneric.RESULT_SUCCESS):
            raise TypeError(f"Received non-success status: {str(result)}")

    async def get_next_response(self) -> ConcreteResponse:
        """Get the next received, deciphered, and parsed response from the queue.

        Note! If you know the type of response that you are expecting, use one of the more narrow-typed get methods.

        Returns:
            ConcreteResponse: Dequeued response.
        """
        return await self._q.get()

    # Helper methods to aid with typing. They are the same at run-time.

    async def get_next_response_as_tlv(self) -> TlvResponse:
        """Get the next received, deciphered, and parsed response, casted as a TlvResponse.

        Returns:
            TlvResponse: dequeued response
        """
        return cast(TlvResponse, await self.get_next_response())

    async def get_next_response_as_query(self) -> QueryResponse:
        """Get the next received, deciphered, and parsed response, casted as a QueryResponse.

        Returns:
            QueryResponse: dequeued response
        """
        return cast(QueryResponse, await self.get_next_response())

    async def get_next_response_as_protobuf(self) -> ProtobufResponse:
        """Get the next received, deciphered, and parsed response, casted as a ProtobufResponse.

        Returns:
            ProtobufResponse: dequeued response
        """
        return cast(ProtobufResponse, await self.get_next_response())


async def set_resolution(manager: ResponseManager) -> bool:
    """Set the video resolution to 1080

    Args:
        manager (ResponseManager): manager used to perform the operation

    Returns:
        bool: True if the setting was successfully set. False otherwise.
    """
    logger.info("Setting the video resolution to 1080")
    request = bytes([0x03, 0x02, 0x01, 0x09])
    request_uuid = GoProUuid.SETTINGS_REQ_UUID
    logger.debug(f"Writing to {request_uuid}: {request.hex(':')}")
    await manager.client.write_gatt_char(request_uuid.value, request, response=True)
    tlv_response = await manager.get_next_response_as_tlv()
    logger.info(f"Set resolution status: {tlv_response.status}")
    return tlv_response.status == 0x00


async def set_shutter_off(manager: ResponseManager) -> bool:
    """Set the shutter off.

    Args:
        manager (ResponseManager): manager used to perform the operation

    Returns:
        bool: True if the shutter was successfully set off. False otherwise.
    """
    # Write to command request BleUUID to turn the shutter on
    logger.info("Setting the shutter on")
    request = bytes([3, 1, 1, 0])
    request_uuid = GoProUuid.COMMAND_REQ_UUID
    logger.debug(f"Writing to {request_uuid}: {request.hex(':')}")
    await manager.client.write_gatt_char(request_uuid.value, request, response=True)
    tlv_response = await manager.get_next_response_as_tlv()
    logger.info(f"Set shutter status: {tlv_response.status}")
    return tlv_response.status == 0x00


async def get_resolution(manager: ResponseManager) -> Resolution:
    """Get the current resolution.

    Args:
        manager (ResponseManager): manager used to perform the operation

    Returns:
        Resolution: The current resolution.
    """
    logger.info("Getting the current resolution")
    request = bytes([0x02, 0x12, 0x02])
    request_uuid = GoProUuid.QUERY_REQ_UUID
    logger.debug(f"Writing to {request_uuid}: {request.hex(':')}")
    await manager.client.write_gatt_char(request_uuid.value, request, response=True)
    query_response = await manager.get_next_response_as_query()
    resolution = Resolution(query_response.data[RESOLUTION_ID][0])
    logger.info(f"Received current resolution: {resolution}")
    return resolution


async def set_turbo_mode(manager: ResponseManager) -> bool:
    """Set the turbo mode off.

    Args:
        manager (ResponseManager): manager used to perform the operation

    Returns:
        bool: True if the turbo mode was successfully set off. False otherwise.
    """
    request = bytearray(
        [
            0xF1,  # Feature ID
            0x6B,  # Action ID
            *proto.RequestSetTurboActive(active=False).SerializeToString(),
        ]
    )
    request.insert(0, len(request))
    request_uuid = GoProUuid.COMMAND_REQ_UUID
    # Write to command request UUID to enable turbo mode
    logger.info(f"Writing {request.hex(':')} to {request_uuid}")
    await manager.client.write_gatt_char(request_uuid.value, request, response=True)
    protobuf_response = await manager.get_next_response_as_protobuf()
    generic_response: proto.ResponseGeneric = protobuf_response.data  # type: ignore
    logger.info(f"Set Turbo Mode Status: {generic_response}")
    return generic_response.result == proto.EnumResultGeneric.RESULT_SUCCESS


async def main(identifier: str | None) -> None:
    manager = ResponseManager()

    try:
        manager.set_client(await connect_ble(manager.notification_handler, identifier))
        # TLV Command (Setting)
        await set_resolution(manager)
        # TLV Command
        await get_resolution(manager)
        # TLV Query
        await set_shutter_off(manager)
        # Protobuf
        await set_turbo_mode(manager)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.error(repr(exc))
    finally:
        if manager.is_initialized:
            await manager.client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, perform operations to demonstrate various responses types."
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
