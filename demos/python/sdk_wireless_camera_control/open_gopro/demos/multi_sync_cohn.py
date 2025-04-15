# cohn.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Oct 24 19:08:07 UTC 2023

"""Entrypoint for configuring and demonstrating Camera On the Home Network (COHN)."""

from __future__ import annotations

import argparse
import asyncio
import re
from dataclasses import dataclass
from functools import cached_property
from typing import Pattern

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.logger import setup_logging
from open_gopro.models.general import CohnInfo
from open_gopro.util import add_cli_args_and_parse

console = Console()

CURL_TEMPLATE = r"""curl -v -u 'gopro:{password}' --cacert cohn.crt 'https://{ip_addr}/gopro/camera/state'"""


@dataclass
class GoPro:
    serial: str
    name: str
    gopro: WirelessGoPro | None = None
    cohn: CohnInfo | None = None

    @cached_property
    def target(self) -> Pattern:
        return re.compile(f".*{self.serial}")


def wrapped_console_print(target: GoPro, message: str) -> None:
    console.print(f"{target.name} ==> {message}")


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    targets = [GoPro("0711", "Hero12"), GoPro("0053", "Hero13")]
    gopro: WirelessGoPro | None = None
    # Ensure COHN is provisioned
    for target in targets[-1:]:
        try:
            # Start with just BLE connected in order to provision COHN
            async with WirelessGoPro(
                target.target,
                interfaces={WirelessGoPro.Interface.BLE},
            ) as gopro:
                if not await gopro.is_cohn_provisioned:
                    await gopro.connect_to_access_point("dabugdabug", "pleasedontguessme")
                    target.cohn = await gopro.configure_cohn()

        except Exception as e:  # pylint: disable = broad-except
            logger.error(repr(e))
            if gopro:
                await gopro.close()
    with open("cohn_db.json", "w") as fp:
        cohn_db = {gopro.serial: gopro.cohn for gopro in targets}
        fp.write(CohnCredentialsDb(credentials=cohn_db).model_dump_json(indent=4))  # type: ignore


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
