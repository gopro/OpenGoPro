# cohn.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Oct 24 19:08:07 UTC 2023

"""Entrypoint for configuring and demonstrating Camera On the Home Network (COHN)."""

from __future__ import annotations

import argparse
import asyncio
import datetime
import multiprocessing as mp
from dataclasses import dataclass
from pathlib import Path
from threading import Event

from open_gopro import WirelessGoPro
from open_gopro.gopro_wired import WiredGoPro
from open_gopro.models import constants, proto
from open_gopro.models.general import CohnInfo, ScheduledCapture
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging


@dataclass
class GoPro:
    """GoPro Target information"""

    serial: str
    name: str
    gopro: WirelessGoPro | None = None
    cohn: CohnInfo | None = None


def multi_record_via_usb(  # pylint: disable = unused-argument
    target: GoPro,
    record_event: Event,
    ready_event: Event,
    ssid: str | None,
    password: str | None,
) -> None:
    """Multiprocess target to synchronized record via USB

    Args:
        target (GoPro): gopro to communicate with
        record_event (Event): event to wait on to start recording
        ready_event (Event): event to notify manager that this target is ready
        ssid (str | None): not used
        password (str | None): not used
    """
    setup_logging(__name__, Path(f"{target.serial}.log"))

    async def _execute() -> None:
        async with WiredGoPro(target.serial) as gopro:
            await gopro.http_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_PHOTO)
            ready_event.set()
            record_event.wait()
            await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)

    asyncio.run(_execute())


def multi_record_via_cohn(
    target: GoPro,
    record_event: Event,
    ready_event: Event,
    ssid: str | None,
    password: str | None,
) -> None:
    """Multiprocess target to synchronized record via COHN

    Args:
        target (GoPro): gopro to communicate with
        record_event (Event): event to wait on to start recording
        ready_event (Event): event to notify manager that this target is ready
        ssid (str | None): WiFi SSID to connect to if COHN provisioning is needed
        password (str | None): WiFi password to use if COHN provisioning is needed
    """
    logger = setup_logging(__name__, Path(f"{target.serial}.log"))

    async def _execute() -> None:
        try:
            # Start with just BLE connected in order to provision COHN
            async with WirelessGoPro(target=target.serial, interfaces={WirelessGoPro.Interface.BLE}) as gopro:
                if await gopro.cohn.is_configured:
                    print("COHN is already configured.")
                else:
                    if not (ssid and password):
                        raise ValueError("COHN provisioning is needed but SSID and password were not provided")
                    await gopro.access_point.connect(ssid, password)
                    await gopro.cohn.configure(force_reprovision=True)
            # # Now use COHN
            async with WirelessGoPro(target=target.serial, interfaces={WirelessGoPro.Interface.COHN}) as gopro:
                await gopro.http_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_PHOTO)
                ready_event.set()
                record_event.wait()
                await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)

        except Exception as e:  # pylint: disable = broad-except
            logger.error(repr(e))
            if gopro:
                await gopro.close()

    asyncio.run(_execute())


def multi_record_via_ble(  # pylint: disable = unused-argument
    target: GoPro,
    record_event: Event,
    ready_event: Event,
    ssid: str | None,
    password: str | None,
) -> None:
    """Multiprocess target to synchronized record via BLE

    Args:
        target (GoPro): gopro to communicate with
        record_event (Event): event to wait on to start recording
        ready_event (Event): event to notify manager that this target is ready
        ssid (str | None): not used
        password (str | None): not used
    """
    setup_logging(__name__, Path(f"{target.serial}.log"))

    async def _execute() -> None:
        async with WirelessGoPro(target.serial, interfaces={WirelessGoPro.Interface.BLE}) as gopro:
            await gopro.ble_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_PHOTO)
            ready_event.set()
            record_event.wait()
            await gopro.ble_command.set_shutter(shutter=constants.Toggle.ENABLE)

    asyncio.run(_execute())


def multi_record_via_scheduled_capture(  # pylint: disable = unused-argument
    target: GoPro,
    record_event: Event,
    ready_event: Event,
    ssid: str | None,
    password: str | None,
) -> None:
    """Multiprocess target to synchronized record via Scheduled Capture over BLE

    Args:
        target (GoPro): gopro to communicate with
        record_event (Event): event to wait on to start recording
        ready_event (Event): event to notify manager that this target is ready
        ssid (str | None): not used
        password (str | None): not used
    """
    logger = setup_logging(__name__, Path(f"{target.serial}.log"))

    async def _execute() -> None:
        async with WirelessGoPro(target.serial, interfaces={WirelessGoPro.Interface.BLE}) as gopro:
            await gopro.ble_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_PHOTO)
            camera_now = (await gopro.ble_command.get_date_time_tz_dst()).data.datetime
            capture_time = camera_now + datetime.timedelta(minutes=1)
            logger.info(f"Camera time is {camera_now}. Recording at {capture_time}")
            await gopro.ble_setting.scheduled_capture.set(
                ScheduledCapture(
                    hour=capture_time.hour,
                    minute=capture_time.minute,
                    is_24_hour=True,
                    is_enabled=True,
                )
            )
            ready_event.set()
            record_event.wait()

    asyncio.run(_execute())


def main(args: argparse.Namespace) -> None:
    gopro_targets = [GoPro(serial, f"Device {idx}") for idx, serial in enumerate(args.devices)]
    record_event = mp.Event()
    ready_events = [mp.Event() for _ in gopro_targets]
    match args.interface:
        case "usb":
            target = multi_record_via_usb
        case "cohn":
            target = multi_record_via_cohn
        case "ble":
            target = multi_record_via_ble
        case "scheduled_capture":
            target = multi_record_via_scheduled_capture
    processes = [
        mp.Process(target=target, args=(gopro_target, record_event, event, args.ssid, args.password))
        for event, gopro_target in zip(ready_events, gopro_targets)
    ]
    # This will serialize the initialization of each process. This is fine since we only care about synchronizing the
    # recording after initialization. And I don't trust OS-level BLE to operate correctly receiving simultaneous
    # commands.
    for event, process in zip(ready_events, processes):
        process.start()
        event.wait()
    record_event.set()
    for process in processes:
        process.join()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Provision / connect a camera for COHN. SSID and password must be passed if COHN is not currently provisioned."
    )
    parser.add_argument(
        "interface",
        type=str,
        choices=["usb", "cohn", "ble", "scheduled_capture"],
        help="Interface to communicate with the target devices",
    )
    parser.add_argument(
        "devices",
        type=str,
        nargs="+",
        help="list of devices to communicate with as last 4 digits of device serial number",
    )
    parser.add_argument(
        "--ssid",
        type=str,
        help="WiFi SSID to connect to if not currently provisioned for COHN.",
        default=None,
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Password of WiFi SSID.",
        default=None,
    )
    return add_cli_args_and_parse(parser, wifi=False)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
