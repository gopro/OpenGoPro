# provision_cohn.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:49 UTC 2024

import sys
import json
import asyncio
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

import pytz
from tzlocal import get_localzone

from tutorial_modules import GoProUuid, connect_ble, proto, connect_to_access_point, ResponseManager, logger


async def set_date_time(manager: ResponseManager) -> None:
    """Get and then set the camera's date, time, timezone, and daylight savings time status

    Args:
        manager (ResponseManager): manager used to perform the operation
    """
    # First find the current time, timezone and is_dst
    tz = pytz.timezone(get_localzone().key)
    now = tz.localize(datetime.now(), is_dst=None)
    try:
        is_dst = now.tzinfo._dst.seconds != 0  # type: ignore
        offset = (now.utcoffset().total_seconds() - now.tzinfo._dst.seconds) / 60  # type: ignore
    except AttributeError:
        is_dst = False
        offset = (now.utcoffset().total_seconds()) / 60  # type: ignore
    if is_dst:
        offset += 60  # Handle daylight savings time
    offset = int(offset)
    logger.info(f"Setting the camera's date and time to {now}:{offset} {is_dst=}")

    # Build the request bytes
    datetime_request = bytearray(
        [
            0x0F,  # Command ID
            10,  # Length of following datetime parameter
            *now.year.to_bytes(2, "big", signed=False),  # uint16 year
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second,
            *offset.to_bytes(2, "big", signed=True),  # int16 offset in minutes
            is_dst,
        ]
    )
    datetime_request.insert(0, len(datetime_request))

    # Send the request
    logger.debug(f"Writing: {datetime_request.hex(':')}")
    await manager.client.write_gatt_char(GoProUuid.COMMAND_REQ_UUID.value, datetime_request, response=True)
    response = await manager.get_next_response_as_tlv()
    assert response.id == 0x0F
    assert response.status == 0x00
    logger.info("Successfully set the date time.")


async def clear_certificate(manager: ResponseManager) -> None:
    """Clear the camera's COHN certificate.

    Args:
        manager (ResponseManager): manager used to perform the operation

    Raises:
        RuntimeError: Received unexpected response
    """
    logger.info("Clearing any preexisting COHN certificate.")

    clear_request = bytearray(
        [
            0xF1,  # Feature ID
            0x66,  # Action ID
            *proto.RequestClearCOHNCert().SerializePartialToString(),
        ]
    )
    clear_request.insert(0, len(clear_request))

    # Send the request
    logger.debug(f"Writing: {clear_request.hex(':')}")
    await manager.client.write_gatt_char(GoProUuid.COMMAND_REQ_UUID.value, clear_request, response=True)
    while response := await manager.get_next_response_as_protobuf():
        if response.feature_id != 0xF1 or response.action_id != 0xE6:
            raise RuntimeError(
                "Only expect to receive Feature ID 0xF1 Action ID 0xE6 responses after clear cert request"
            )
        manager.assert_generic_protobuf_success(response.data)
        logger.info("COHN certificate successfully cleared")
        return
    raise RuntimeError("Loop should not exit without return")


async def create_certificate(manager: ResponseManager) -> None:
    """Instruct the camera to create the COHN certificate.

    Args:
        manager (ResponseManager): manager used to perform the operation

    Raises:
        RuntimeError: Received unexpected response
    """
    logger.info("Creating a new COHN certificate.")

    create_request = bytearray(
        [
            0xF1,  # Feature ID
            0x67,  # Action ID
            *proto.RequestCreateCOHNCert().SerializePartialToString(),
        ]
    )
    create_request.insert(0, len(create_request))

    # Send the request
    logger.debug(f"Writing: {create_request.hex(':')}")
    await manager.client.write_gatt_char(GoProUuid.COMMAND_REQ_UUID.value, create_request, response=True)
    while response := await manager.get_next_response_as_protobuf():
        if response.feature_id != 0xF1 or response.action_id != 0xE7:
            raise RuntimeError(
                "Only expect to receive Feature ID 0xF1 Action ID 0xE7 responses after create cert request"
            )
        manager.assert_generic_protobuf_success(response.data)
        logger.info("COHN certificate successfully created")
        return
    raise RuntimeError("Loop should not exit without return")


@dataclass(frozen=True)
class Credentials:
    """COHN credentials."""

    certificate: str
    username: str
    password: str
    ip_address: str

    def __str__(self) -> str:
        return json.dumps(asdict(self), indent=4)


async def get_cohn_certificate(manager: ResponseManager) -> str:
    """Get the camera's COHN certificate

    Args:
        manager (ResponseManager): manager used to perform the operation

    Raises:
        RuntimeError: Received unexpected response

    Returns:
        str: certificate in string form.
    """
    logger.info("Getting the current COHN certificate.")

    cert_request = bytearray(
        [
            0xF5,  # Feature ID
            0x6E,  # Action ID
            *proto.RequestCOHNCert().SerializePartialToString(),
        ]
    )
    cert_request.insert(0, len(cert_request))

    # Send the request
    logger.debug(f"Writing: {cert_request.hex(':')}")
    await manager.client.write_gatt_char(GoProUuid.QUERY_REQ_UUID.value, cert_request, response=True)
    while response := await manager.get_next_response_as_protobuf():
        if response.feature_id != 0xF5 or response.action_id != 0xEE:
            raise RuntimeError("Only expect to receive Feature ID 0xF5 Action ID 0xEE responses after get cert request")
        cert_response: proto.ResponseCOHNCert = response.data  # type: ignore
        manager.assert_generic_protobuf_success(cert_response)
        logger.info("COHN certificate successfully retrieved")
        return cert_response.cert
    raise RuntimeError("Loop should not exit without return")


async def get_cohn_status(manager: ResponseManager) -> proto.NotifyCOHNStatus:
    """Get the COHN status until it is provisioned and connected.

    Args:
        manager (ResponseManager): manager used to perform the operation

    Raises:
        RuntimeError: Received unexpected response

    Returns:
        proto.NotifyCOHNStatus: Connected COHN status that includes the credentials.
    """
    logger.info("Checking COHN status until provisioning is complete")

    status_request = bytearray(
        [
            0xF5,  # Feature ID
            0x6F,  # Action ID
            *proto.RequestGetCOHNStatus(register_cohn_status=True).SerializePartialToString(),
        ]
    )
    status_request.insert(0, len(status_request))

    # Send the scan request
    logger.debug(f"Writing: {status_request.hex(':')}")
    await manager.client.write_gatt_char(GoProUuid.QUERY_REQ_UUID.value, status_request, response=True)
    while response := await manager.get_next_response_as_protobuf():
        if response.feature_id != 0xF5 or response.action_id != 0xEF:
            raise RuntimeError(
                "Only expect to receive Feature ID 0xF5, Action ID 0xEF responses after COHN status request"
            )
        cohn_status: proto.NotifyCOHNStatus = response.data  # type: ignore
        logger.info(f"Received COHN Status: {cohn_status}")
        if cohn_status.state == proto.EnumCOHNNetworkState.COHN_STATE_NetworkConnected:
            return cohn_status
    raise RuntimeError("Loop should not exit without return")


async def provision_cohn(manager: ResponseManager) -> Credentials:
    """Helper method to provision COHN.

    Args:
        manager (ResponseManager): manager used to perform the operation

    Returns:
        Credentials: COHN credentials to use for future COHN communication.
    """
    logger.info("Provisioning COHN")
    await clear_certificate(manager)
    await create_certificate(manager)
    certificate = await get_cohn_certificate(manager)
    # Wait for COHN to be provisioned and get the provisioned status
    status = await get_cohn_status(manager)
    logger.info("Successfully provisioned COHN.")
    credentials = Credentials(
        certificate=certificate,
        username=status.username,
        password=status.password,
        ip_address=status.ipaddress,
    )
    logger.info(credentials)
    return credentials


async def main(ssid: str, password: str, identifier: str | None, certificate: Path) -> Credentials | None:
    manager = ResponseManager()
    credentials: Credentials | None = None
    try:
        client = await connect_ble(manager.notification_handler, identifier)
        manager.set_client(client)
        await set_date_time(manager)
        await connect_to_access_point(manager, ssid, password)
        credentials = await provision_cohn(manager)
        with open(certificate, "w") as fp:
            fp.write(credentials.certificate)
            logger.info(f"Certificate written to {certificate.resolve()}")

    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.error(repr(exc))
    finally:
        if manager.is_initialized:
            await manager.client.disconnect()
    return credentials


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision COHN via BLE to be ready for communication.")
    parser.add_argument("ssid", type=str, help="SSID of network to connect to")
    parser.add_argument("password", type=str, help="Password of network to connect to")
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to",
        default=None,
    )
    parser.add_argument(
        "-c",
        "--certificate",
        type=Path,
        help="Path to write retrieved COHN certificate.",
        default=Path("cohn.crt"),
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(args.ssid, args.password, args.identifier, args.certificate))
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
