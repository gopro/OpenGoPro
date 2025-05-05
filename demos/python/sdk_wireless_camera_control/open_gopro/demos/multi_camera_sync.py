# cohn.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Oct 24 19:08:07 UTC 2023

"""Entrypoint for configuring and demonstrating Camera On the Home Network (COHN)."""

from __future__ import annotations

import argparse
import asyncio
import multiprocessing as mp
from dataclasses import dataclass
from pathlib import Path
from threading import Event

from open_gopro import WirelessGoPro, constants
from open_gopro.gopro_wired import WiredGoPro
from open_gopro.logger import setup_logging
from open_gopro.models.general import CohnInfo
from open_gopro.util import add_cli_args_and_parse


@dataclass
class GoPro:
    """GoPro Target information"""

    serial: str
    name: str
    gopro: WirelessGoPro | None = None
    cohn: CohnInfo | None = None


def multi_record_via_usb(target: GoPro, record_event: Event, ready_event: Event) -> None:
    """_summary_

    Args:
        target (GoPro): _description_
        record_event (Event): _description_
        ready_event (Event): _description_
    """
    setup_logging(__name__, Path(f"{target.serial}.log"))

    async def _execute() -> None:
        async with WiredGoPro(target.serial) as gopro:
            ready_event.set()
            record_event.wait()
            await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)

    asyncio.run(_execute())


def multi_record_via_cohn(target: GoPro, record_event: Event, ready_event: Event) -> None:
    """_summary_

    Args:
        target (GoPro): _description_
        record_event (Event): _description_
        ready_event (Event): _description_
    """
    logger = setup_logging(__name__, Path(f"{target.serial}.log"))

    async def _execute() -> None:
        try:
            # Start with just BLE connected in order to provision COHN
            async with WirelessGoPro(target=target.serial, interfaces={WirelessGoPro.Interface.BLE}) as gopro:
                if await gopro.cohn.is_configured:
                    print("COHN is already configured :)")
                else:
                    await gopro.access_point.connect("dabugdabug", "pleasedontguessme")
                    await gopro.cohn.configure(force_reprovision=True)
            # # Now use COHN
            async with WirelessGoPro(target=target.serial, interfaces={WirelessGoPro.Interface.COHN}) as gopro:
                ready_event.set()
                record_event.wait()
                await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)

        except Exception as e:  # pylint: disable = broad-except
            logger.error(repr(e))
            if gopro:
                await gopro.close()

    asyncio.run(_execute())


def main(_: argparse.Namespace) -> None:
    gopro_targets = [
        GoPro("0711", "Hero12Left"),
        GoPro("0702", "Hero12Right"),
        # GoPro("0053", "Hero13"),
    ]
    record_event = mp.Event()
    ready_events = [mp.Event() for _ in gopro_targets]
    processes = [
        mp.Process(
            # target=multi_record_via_usb,
            target=multi_record_via_cohn,
            args=(gopro_target, record_event, event),
        )
        for event, gopro_target in zip(ready_events, gopro_targets)
    ]
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
