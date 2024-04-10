# ble_command_get_state.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:59 PM

from __future__ import annotations
import sys
import json
import enum
import asyncio
import argparse
from typing import TypeVar
from dataclasses import dataclass, asdict

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GoProUuid, connect_ble, logger

T = TypeVar("T", bound="Response")


class Response:
    """The base class to encapsulate all BLE Responses

    Args:
        uuid (GoProUuid): UUID that this response was received on.
    """

    def __init__(self, uuid: GoProUuid) -> None:
        """Constructor"""
        self.bytes_remaining = 0
        self.uuid = uuid
        self.raw_bytes = bytearray()

    @classmethod
    def from_received_response(cls: type[T], received_response: Response) -> T:
        """Build a new response from a received response.

        Can be used by subclasses for essentially casting into their derived type.

        Args:
            cls (type[T]): type of response to build
            received_response (Response): received response to build from

        Returns:
            T: built response.
        """
        response = cls(received_response.uuid)
        response.bytes_remaining = 0
        response.raw_bytes = received_response.raw_bytes
        return response

    @property
    def is_received(self) -> bool:
        """Have all of the bytes identified by the length header been received?

        Returns:
            bool: True if received, False otherwise.
        """
        return len(self.raw_bytes) > 0 and self.bytes_remaining == 0

    def accumulate(self, data: bytes) -> None:
        """Accumulate a current packet in to the received response.

        Args:
            data (bytes): bytes to accumulate.
        """
        CONT_MASK = 0b10000000
        HDR_MASK = 0b01100000
        GEN_LEN_MASK = 0b00011111
        EXT_13_BYTE0_MASK = 0b00011111

        class Header(enum.Enum):
            """Header Type Identifiers"""

            GENERAL = 0b00
            EXT_13 = 0b01
            EXT_16 = 0b10
            RESERVED = 0b11

        buf = bytearray(data)
        if buf[0] & CONT_MASK:
            buf.pop(0)
        else:
            # This is a new packet so start with an empty byte array
            self.raw_bytes = bytearray()
            hdr = Header((buf[0] & HDR_MASK) >> 5)
            if hdr is Header.GENERAL:
                self.bytes_remaining = buf[0] & GEN_LEN_MASK
                buf = buf[1:]
            elif hdr is Header.EXT_13:
                self.bytes_remaining = ((buf[0] & EXT_13_BYTE0_MASK) << 8) + buf[1]
                buf = buf[2:]
            elif hdr is Header.EXT_16:
                self.bytes_remaining = (buf[1] << 8) + buf[2]
                buf = buf[3:]

        # Append payload to buffer and update remaining / complete
        self.raw_bytes.extend(buf)
        self.bytes_remaining -= len(buf)
        logger.debug(f"{self.bytes_remaining=}")


class TlvResponse(Response):
    """A Type Length Value TLV Response.

    TLV response all have an ID, status, and payload.
    """

    def __init__(self, uuid: GoProUuid) -> None:
        super().__init__(uuid)
        self.id: int
        self.status: int
        self.payload: bytes

    def parse(self) -> None:
        """Extract the ID, status, and payload"""
        self.id = self.raw_bytes[0]
        self.status = self.raw_bytes[1]
        self.payload = bytes(self.raw_bytes[2:])


@dataclass
class HardwareInfo:
    """The meaningful values from a hardware info response"""

    model_number: int
    model_name: str
    firmware_version: str
    serial_number: str
    ap_ssid: str
    ap_mac_address: str

    def __str__(self) -> str:
        return json.dumps(asdict(self), indent=4)

    @classmethod
    def from_bytes(cls, data: bytes) -> HardwareInfo:
        """Parse and build from a raw hardware info response bytestream

        Args:
            data (bytes): bytestream to parse

        Returns:
            HardwareInfo: Parsed response.
        """
        buf = bytearray(data)
        # Get model number
        model_num_length = buf.pop(0)
        model = int.from_bytes(buf[:model_num_length], "big", signed=False)
        buf = buf[model_num_length:]
        # Get model name
        model_name_length = buf.pop(0)
        model_name = (buf[:model_name_length]).decode()
        buf = buf[model_name_length:]
        # Advance past deprecated bytes
        deprecated_length = buf.pop(0)
        buf = buf[deprecated_length:]
        # Get firmware version
        firmware_length = buf.pop(0)
        firmware = (buf[:firmware_length]).decode()
        buf = buf[firmware_length:]
        # Get serial number
        serial_length = buf.pop(0)
        serial = (buf[:serial_length]).decode()
        buf = buf[serial_length:]
        # Get AP SSID
        ssid_length = buf.pop(0)
        ssid = (buf[:ssid_length]).decode()
        buf = buf[ssid_length:]
        # Get MAC address
        mac_length = buf.pop(0)
        mac = (buf[:mac_length]).decode()
        buf = buf[mac_length:]

        return cls(model, model_name, firmware, serial, ssid, mac)


async def main(identifier: str | None) -> None:
    client: BleakClient
    responses_by_uuid = GoProUuid.dict_by_uuid(TlvResponse)
    received_responses: asyncio.Queue[TlvResponse] = asyncio.Queue()

    request_uuid = GoProUuid.COMMAND_REQ_UUID
    response_uuid = GoProUuid.COMMAND_RSP_UUID

    async def tlv_notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid)
        logger.info(f'Received response at {uuid}: {data.hex(":")}')

        response = responses_by_uuid[uuid]
        response.accumulate(data)

        if response.is_received:
            # If this is the correct handle, enqueue it for processing
            if uuid is response_uuid:
                logger.info("Received the get hardware info response")
                await received_responses.put(response)
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")
            # Reset the per-UUID response
            responses_by_uuid[uuid] = TlvResponse(uuid)

    client = await connect_ble(tlv_notification_handler, identifier)

    # Write to command request BleUUID to get the hardware info
    logger.info("Getting the camera's hardware info...")
    request = bytearray([0x01, 0x3C])
    logger.debug(f"Writing to {request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(request_uuid.value, request, response=True)
    response = await received_responses.get()
    # Parse TLV headers and Payload
    response.parse()
    # Now parse payload into human readable object
    hardware_info = HardwareInfo.from_bytes(response.payload)
    logger.info(f"Parsed hardware info: {hardware_info}")

    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera via BLE, then get its hardware info.")
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
