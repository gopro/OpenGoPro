# scanner.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Mar 25 16:44:35 UTC 2025

"""Demo to retrieve and parse information from non-connected GoPros"""

import argparse
import asyncio
import enum
import sys
from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

from bleak import BleakScanner
from rich.console import Console

from open_gopro.domain.exceptions import FailedToFindDevice
from open_gopro.gopro_wired import WiredGoPro
from open_gopro.models import AdvData, GoProAdvData
from open_gopro.network.wifi.mdns_scanner import find_first_ip_addr
from open_gopro.util import add_cli_args_and_parse, ainput

console = Console()


class NetworkType(enum.Enum):
    """Scan Response Network type"""

    BLE = enum.auto()
    WIFI_AP = enum.auto()
    DNS = enum.auto()


T = TypeVar("T")


@dataclass(frozen=True)
class ScanResponse(ABC, Generic[T]):
    """Base class for scan responses"""

    data: T
    network: NetworkType


@dataclass(frozen=True)
class BleScanResponse(ScanResponse[GoProAdvData]):
    """A BLE advertisement / scan response"""

    data: GoProAdvData
    network: NetworkType = NetworkType.BLE


@dataclass(frozen=True)
class WifiApScanResponse(ScanResponse[str]):
    """An SSID discovered by scanning via WiFi"""

    data: str
    network: NetworkType = NetworkType.WIFI_AP


@dataclass(frozen=True)
class DnsScanResponse(ScanResponse[str]):
    """ "A DNS entry discovered by scanning mDNS"""

    data: str
    network: NetworkType = NetworkType.DNS


def process_scan_response(scan_response: ScanResponse) -> None:
    """Log the scan response

    Args:
        scan_response (ScanResponse): scan response to process
    """
    match (scan_response):
        case BleScanResponse():
            console.print(f"{scan_response.network.name} ==> {scan_response.data.serial_number}")
        case WifiApScanResponse() | DnsScanResponse():
            console.print(f"{scan_response.network.name} ==> {scan_response.data}")


async def scan_ble() -> None:
    """Scan BLE Advertisements / scan responses and combine them to find GoPros"""
    unique_adv_data: set[GoProAdvData] = set()

    async with BleakScanner(service_uuids=["0000fea6-0000-1000-8000-00805f9b34fb"]) as scanner:
        while True:
            adv_data = AdvData()
            async for _, data in scanner.advertisement_data():
                adv_data.update(data)
                if adv_data.local_name:  # Once we've received the scan response...
                    break

            if (gopro_adv_data := GoProAdvData.fromAdvData(adv_data)) not in unique_adv_data:
                process_scan_response(BleScanResponse(gopro_adv_data))
            unique_adv_data.add(gopro_adv_data)


async def scan_wifi_ap() -> None:
    """Scan for GoPro XXXX WiFi SSIDs"""
    raise NotImplementedError


async def scan_dns() -> None:
    """Scan for MDNS entries that match the GoPro service name"""
    unique_responses: set[str] = set()

    while True:
        try:
            response = await find_first_ip_addr(WiredGoPro._MDNS_SERVICE_NAME, 10)
            serial = response.name.split(".")[0]
            if serial not in unique_responses:
                process_scan_response(DnsScanResponse(serial))
            unique_responses.add(serial)
        except FailedToFindDevice:
            continue


async def wait_for_exit() -> None:
    """Exit on enter"""
    await ainput("Press enter to exit\n")
    console.print("Exiting...")
    sys.exit()


async def main(_: argparse.Namespace) -> None:
    await asyncio.gather(
        scan_ble(),
        # scan_wifi_ap(args.password, args.interface),
        scan_dns(),
        wait_for_exit(),
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan for GoPro's via BLE and mDNS.")

    return add_cli_args_and_parse(parser, bluetooth=False)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
