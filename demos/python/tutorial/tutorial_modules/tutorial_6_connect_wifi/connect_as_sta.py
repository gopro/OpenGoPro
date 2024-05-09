# connect_sta.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:49 UTC 2024

import sys
import asyncio
import argparse
from typing import Generator, Final

from bleak import BleakClient
from tutorial_modules import GoProUuid, connect_ble, proto, logger, ResponseManager


def yield_fragmented_packets(payload: bytes) -> Generator[bytes, None, None]:
    """Generate fragmented packets from a monolithic payload to accommodate the max BLE packet size of 20 bytes.

    Args:
        payload (bytes): input payload to fragment

    Raises:
        ValueError: Input payload is too large.

    Yields:
        Generator[bytes, None, None]: fragmented packets.
    """
    length = len(payload)

    CONTINUATION_HEADER: Final = bytearray([0x80])
    MAX_PACKET_SIZE: Final = 20
    is_first_packet = True

    # Build initial length header
    if length < (2**13 - 1):
        header = bytearray((length | 0x2000).to_bytes(2, "big", signed=False))
    elif length < (2**16 - 1):
        header = bytearray((length | 0x6400).to_bytes(2, "big", signed=False))
    else:
        raise ValueError(f"Data length {length} is too big for this protocol.")

    byte_index = 0
    while bytes_remaining := length - byte_index:
        # If this is the first packet, use the appropriate header. Else use the continuation header
        if is_first_packet:
            packet = bytearray(header)
            is_first_packet = False
        else:
            packet = bytearray(CONTINUATION_HEADER)
        # Build the current packet
        packet_size = min(MAX_PACKET_SIZE - len(packet), bytes_remaining)
        packet.extend(bytearray(payload[byte_index : byte_index + packet_size]))
        yield bytes(packet)
        # Increment byte_index for continued processing
        byte_index += packet_size


async def fragment_and_write_gatt_char(client: BleakClient, char_specifier: str, data: bytes) -> None:
    """Fragment the data into BLE packets and send each packet via GATT write.

    Args:
        client (BleakClient): Bleak client to perform GATT Writes with
        char_specifier (str): BLE characteristic to write to
        data (bytes): data to fragment and write.
    """
    for packet in yield_fragmented_packets(data):
        await client.write_gatt_char(char_specifier, packet, response=True)


async def scan_for_networks(manager: ResponseManager) -> int:
    """Scan for WiFi networks

    Args:
        manager (ResponseManager): manager used to perform the operation

    Raises:
        RuntimeError: Received unexpected response.

    Returns:
        int: Scan ID to use to retrieve scan results
    """
    logger.info(msg="Scanning for available Wifi Networks")

    start_scan_request = bytearray(
        [
            0x02,  # Feature ID
            0x02,  # Action ID
            *proto.RequestStartScan().SerializePartialToString(),
        ]
    )
    start_scan_request.insert(0, len(start_scan_request))

    # Send the scan request
    logger.debug(f"Writing: {start_scan_request.hex(':')}")
    await manager.client.write_gatt_char(GoProUuid.NETWORK_MANAGEMENT_REQ_UUID.value, start_scan_request, response=True)
    while response := await manager.get_next_response_as_protobuf():
        if response.feature_id != 0x02:
            raise RuntimeError("Only expect to receive Feature ID 0x02 responses after scan request")
        if response.action_id == 0x82:  # Initial Scan Response
            manager.assert_generic_protobuf_success(response.data)
        elif response.action_id == 0x0B:  # Scan Notifications
            scan_notification: proto.NotifStartScanning = response.data  # type: ignore
            logger.info(f"Received scan notification: {scan_notification}")
            if scan_notification.scanning_state == proto.EnumScanning.SCANNING_SUCCESS:
                return scan_notification.scan_id
        else:
            raise RuntimeError("Only expect to receive Action ID 0x02 or 0x0B responses after scan request")
    raise RuntimeError("Loop should not exit without return")


async def get_scan_results(manager: ResponseManager, scan_id: int) -> list[proto.ResponseGetApEntries.ScanEntry]:
    """Retrieve the results from a completed Wifi Network scan

    Args:
        manager (ResponseManager): manager used to perform the operation
        scan_id (int): identifier returned from completed scan

    Raises:
        RuntimeError: Received unexpected response.

    Returns:
        list[proto.ResponseGetApEntries.ScanEntry]: list of scan entries
    """
    logger.info("Getting the scanned networks.")

    results_request = bytearray(
        [
            0x02,  # Feature ID
            0x03,  # Action ID
            *proto.RequestGetApEntries(start_index=0, max_entries=100, scan_id=scan_id).SerializePartialToString(),
        ]
    )
    results_request.insert(0, len(results_request))

    # Send the request
    logger.debug(f"Writing: {results_request.hex(':')}")
    await manager.client.write_gatt_char(GoProUuid.NETWORK_MANAGEMENT_REQ_UUID.value, results_request, response=True)
    while response := await manager.get_next_response_as_protobuf():
        if response.feature_id != 0x02 or response.action_id != 0x83:
            raise RuntimeError("Only expect to receive Feature ID 0x02 Action ID 0x83 responses after scan request")
        entries_response: proto.ResponseGetApEntries = response.data  # type: ignore
        manager.assert_generic_protobuf_success(entries_response)
        logger.info("Found the following networks:")
        for entry in entries_response.entries:
            logger.info(str(entry))
        return list(entries_response.entries)
    raise RuntimeError("Loop should not exit without return")


async def connect_to_network(
    manager: ResponseManager, entry: proto.ResponseGetApEntries.ScanEntry, password: str
) -> None:
    """Connect to a WiFi network

    Args:
        manager (ResponseManager): manager used to perform the operation
        entry (proto.ResponseGetApEntries.ScanEntry): scan entry that contains network (and its metadata) to connect to
        password (str): password corresponding to network from `entry`

    Raises:
        RuntimeError: Received unexpected response.
    """
    logger.info(f"Connecting to {entry.ssid}")

    if entry.scan_entry_flags & proto.EnumScanEntryFlags.SCAN_FLAG_CONFIGURED:
        connect_request = bytearray(
            [
                0x02,  # Feature ID
                0x04,  # Action ID
                *proto.RequestConnect(ssid=entry.ssid).SerializePartialToString(),
            ]
        )
    else:
        connect_request = bytearray(
            [
                0x02,  # Feature ID
                0x05,  # Action ID
                *proto.RequestConnectNew(ssid=entry.ssid, password=password).SerializePartialToString(),
            ]
        )

    # Send the request
    logger.debug(f"Writing: {connect_request.hex(':')}")
    await fragment_and_write_gatt_char(manager.client, GoProUuid.NETWORK_MANAGEMENT_REQ_UUID.value, connect_request)
    while response := await manager.get_next_response_as_protobuf():
        if response.feature_id != 0x02:
            raise RuntimeError("Only expect to receive Feature ID 0x02 responses after connect request")
        if response.action_id == 0x84:  # RequestConnect Response
            manager.assert_generic_protobuf_success(response.data)
        elif response.action_id == 0x85:  # RequestConnectNew Response
            manager.assert_generic_protobuf_success(response.data)
        elif response.action_id == 0x0C:  # NotifProvisioningState Notifications
            provisioning_notification: proto.NotifProvisioningState = response.data  # type: ignore
            logger.info(f"Received network provisioning status: {provisioning_notification}")
            if provisioning_notification.provisioning_state == proto.EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP:
                return
            if provisioning_notification.provisioning_state != proto.EnumProvisioning.PROVISIONING_STARTED:
                raise RuntimeError(f"Unexpected provisioning state: {provisioning_notification.provisioning_state}")
        else:
            raise RuntimeError("Only expect to receive Action ID 0x84, 0x85, or 0x0C responses after scan request")
    raise RuntimeError("Loop should not exit without return")


async def connect_to_access_point(manager: ResponseManager, ssid: str, password: str) -> None:
    """Top level method to connect to an access point.

    Args:
        manager (ResponseManager): manager used to perform the operation
        ssid (str): SSID of WiFi network to connect to
        password (str): password of WiFi network  to connect to

    Raises:
        RuntimeError: Received unexpected response.
    """
    entries = await get_scan_results(manager, await scan_for_networks(manager))
    try:
        entry = [entry for entry in entries if entry.ssid == ssid][0]
    except IndexError as exc:
        raise RuntimeError(f"Did not find {ssid}") from exc

    await connect_to_network(manager, entry, password)
    logger.info(f"Successfully connected to {ssid}")


async def main(ssid: str, password: str, identifier: str | None) -> None:
    manager = ResponseManager()
    try:
        client = await connect_ble(manager.notification_handler, identifier)
        manager.set_client(client)
        await connect_to_access_point(manager, ssid, password)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.error(repr(exc))
    finally:
        if manager.is_initialized:
            await manager.client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Connect the GoPro to a Wifi network where the GoPro is in Station Mode (STA)."
    )
    parser.add_argument("ssid", type=str, help="SSID of network to connect to")
    parser.add_argument("password", type=str, help="Password of network to connect to")
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to",
        default=None,
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(args.ssid, args.password, args.identifier))
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
