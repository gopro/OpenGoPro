# cohn.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Oct 24 19:08:07 UTC 2023

"""Entrypoint for configuring and demonstrating Camera On the Home Network (COHN)."""

from __future__ import annotations

import argparse
import logging
import asyncio
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from open_gopro import WirelessGoPro, constants
from open_gopro.gopro_base import GoProBase
from open_gopro.gopro_wired import WiredGoPro
from open_gopro.logger import setup_logging
from open_gopro.models.general import CohnInfo
from open_gopro.util import add_cli_args_and_parse

console = Console()

logger: logging.Logger


@dataclass
class GoPro:
    serial: str
    name: str
    gopro: WirelessGoPro | None = None
    cohn: CohnInfo | None = None


def wrapped_console_print(target: GoPro, message: str) -> None:
    console.print(f"{target.name} ==> {message}")


async def take_photo(gopro: GoProBase) -> None:
    await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)
    await asyncio.sleep(2)
    await gopro.http_command.set_shutter(shutter=constants.Toggle.DISABLE)


async def multi_record_via_cohn(targets: list[GoPro]) -> None:
    gopro: WirelessGoPro | None = None
    try:
        # Ensure COHN is provisioned
        for target in targets:
            # Start with just BLE connected in order to provision COHN
            async with WirelessGoPro(target=target.serial, interfaces={WirelessGoPro.Interface.BLE}) as gopro:
                if await gopro.cohn.is_configured:
                    console.print("COHN is already configured :smiley:")
                else:
                    await gopro.access_point.connect("dabugdabug", "pleasedontguessme")
                    await gopro.cohn.configure(force_reprovision=True)

        gopros = [WirelessGoPro(target=target.serial, interfaces={WirelessGoPro.Interface.COHN}) for target in targets]
        async with asyncio.TaskGroup() as tg:
            for gopro in gopros:
                await gopro.open()
                tg.create_task(take_photo(gopro), name=gopro.identifier)

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))
        if gopro:
            await gopro.close()


async def multi_record_via_usb(targets: list[GoPro]) -> None:
    async with asyncio.TaskGroup() as tg:
        for gopro in [WiredGoPro(target.serial) for target in targets]:
            await gopro.open()
            tg.create_task(take_photo(gopro), name=gopro.identifier)


async def main(args: argparse.Namespace) -> None:
    global logger
    logger = setup_logging(__name__, args.log)

    targets = [
        GoPro("0711", "Hero12Left"),
        GoPro("0702", "Hero12Right"),
        # GoPro("0053", "Hero13"),
    ]
    # await multi_record_via_cohn(targets)
    await multi_record_via_usb(targets)


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
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
