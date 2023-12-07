# ble_command_get_state.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:59 PM

import sys
import json
import enum
import asyncio
import argparse
from binascii import hexlify
from typing import Dict, Optional

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GOPRO_BASE_UUID, connect_ble, logger


class Response:
    def __init__(self) -> None:
        self.bytes_remaining = 0
        self.bytes = bytearray()
        self.data: Dict[int, bytes] = {}
        self.id: int
        self.status: int

    def __str__(self) -> str:
        return json.dumps(self.data, indent=4, default=lambda x: x.hex(":"))

    @property
    def is_received(self) -> bool:
        return len(self.bytes) > 0 and self.bytes_remaining == 0

    def accumulate(self, data: bytes) -> None:
        CONT_MASK = 0b10000000
        HDR_MASK = 0b01100000
        GEN_LEN_MASK = 0b00011111
        EXT_13_BYTE0_MASK = 0b00011111

        class Header(enum.Enum):
            GENERAL = 0b00
            EXT_13 = 0b01
            EXT_16 = 0b10
            RESERVED = 0b11

        buf = bytearray(data)
        if buf[0] & CONT_MASK:
            buf.pop(0)
        else:
            # This is a new packet so start with an empty byte array
            self.bytes = bytearray()
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
        self.bytes.extend(buf)
        self.bytes_remaining -= len(buf)
        logger.info(f"{self.bytes_remaining=}")

    def parse(self) -> None:
        self.id = self.bytes[0]
        self.status = self.bytes[1]
        buf = self.bytes[2:]
        while len(buf) > 0:
            # Get ID and Length
            param_id = buf[0]
            param_len = buf[1]
            buf = buf[2:]
            # Get the value
            value = buf[:param_len]

            # Store in dict for later access
            self.data[param_id] = value

            # Advance the buffer
            buf = buf[param_len:]


async def main(identifier: Optional[str]) -> None:
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    # UUIDs to write to and receive responses from
    QUERY_REQ_UUID = GOPRO_BASE_UUID.format("0076")
    QUERY_RSP_UUID = GOPRO_BASE_UUID.format("0077")
    response_uuid = QUERY_RSP_UUID

    client: BleakClient
    response = Response()

    def notification_handler(characteristic: BleakGATTCharacteristic, data: bytes) -> None:
        logger.info(f'Received response at handle {characteristic.handle}: {data.hex(":")}')

        response.accumulate(data)

        if response.is_received:
            response.parse()

            # If this is the correct handle and the status is success, the command was a success
            if (
                client.services.characteristics[characteristic.handle].uuid == response_uuid
                and response.status == 0
            ):
                logger.info("Successfully received the response")
            # Anything else is unexpected. This shouldn't happen
            else:
                logger.error("Unexpected response")

            # Notify writer that procedure is complete
            event.set()

    client = await connect_ble(notification_handler, identifier)

    # Write to command request BleUUID to put the camera to sleep
    logger.info("Getting the camera's settings...")
    event.clear()
    await client.write_gatt_char(QUERY_REQ_UUID, bytearray([0x01, 0x12]), response=True)
    await event.wait()  # Wait to receive the notification response
    logger.info(f"Received settings\n: {response}")

    # Write to command request BleUUID to put the camera to sleep
    logger.info("Getting the camera's statuses...")
    event.clear()
    await client.write_gatt_char(QUERY_REQ_UUID, bytearray([0x01, 0x13]), response=True)
    await event.wait()  # Wait to receive the notification response
    logger.info(f"Received statuses\n: {response}")

    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE, then get its statuses and settings."
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
