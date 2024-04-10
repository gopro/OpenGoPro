# ble_command_set_shutter.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:58 PM

from __future__ import annotations
import sys
import enum
import asyncio
import argparse
from typing import Callable, TypeVar

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from tutorial_modules import GOPRO_BASE_UUID, connect_ble, logger


T = TypeVar("T")


class GoProUuid(str, enum.Enum):
    """UUIDs to write to and receive responses from"""

    COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
    COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
    SETTINGS_REQ_UUID = GOPRO_BASE_UUID.format("0074")
    SETTINGS_RSP_UUID = GOPRO_BASE_UUID.format("0075")
    CONTROL_QUERY_SERVICE_UUID = "0000fea6-0000-1000-8000-00805f9b34fb"
    INTERNAL_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
    QUERY_REQ_UUID = GOPRO_BASE_UUID.format("0076")
    QUERY_RSP_UUID = GOPRO_BASE_UUID.format("0077")
    WIFI_AP_SSID_UUID = GOPRO_BASE_UUID.format("0002")
    WIFI_AP_PASSWORD_UUID = GOPRO_BASE_UUID.format("0003")
    NETWORK_MANAGEMENT_REQ_UUID = GOPRO_BASE_UUID.format("0091")
    NETWORK_MANAGEMENT_RSP_UUID = GOPRO_BASE_UUID.format("0092")

    @classmethod
    def dict_by_uuid(cls, value_creator: Callable[[GoProUuid], T]) -> dict[GoProUuid, T]:
        """Build a dict where the keys are each UUID defined here and the values are built from the input value_creator.

        Args:
            value_creator (Callable[[GoProUuid], T]): callable to create the values from each UUID

        Returns:
            dict[GoProUuid, T]: uuid-to-value mapping.
        """
        return {uuid: value_creator(uuid) for uuid in cls}


async def main(identifier: str | None) -> None:
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()
    request_uuid = GoProUuid.COMMAND_REQ_UUID
    response_uuid = GoProUuid.COMMAND_RSP_UUID

    client: BleakClient

    async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
        uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid)
        logger.info(f'Received response at {uuid}: {data.hex(":")}')

        # If this is the correct handle and the status is success, the command was a success
        if uuid is response_uuid and data[2] == 0x00:
            logger.info("Command sent successfully")
        # Anything else is unexpected. This shouldn't happen
        else:
            logger.error("Unexpected response")

        # Notify the writer
        event.set()

    client = await connect_ble(notification_handler, identifier)

    # Write to command request BleUUID to turn the shutter on
    logger.info("Setting the shutter on")
    event.clear()
    request = bytes([3, 1, 1, 1])
    logger.debug(f"Writing to {request_uuid}: {request.hex(':')}")
    await client.write_gatt_char(request_uuid.value, request, response=True)
    await event.wait()  # Wait to receive the notification response

    await asyncio.sleep(2)  # If we're recording, let's wait 2 seconds (i.e. take a 2 second video)
    # Write to command request BleUUID to turn the shutter off
    logger.info("Setting the shutter off")
    request = bytes([3, 1, 1, 0])
    logger.debug(f"Writing to {request_uuid}: {request.hex(':')}")
    event.clear()
    await client.write_gatt_char(request_uuid.value, request, response=True)
    await event.wait()  # Wait to receive the notification response
    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, set the shutter on, wait 2 seconds, then set the shutter off."
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
