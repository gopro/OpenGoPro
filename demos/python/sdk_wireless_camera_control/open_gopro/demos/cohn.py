# cohn.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Oct 24 19:08:07 UTC 2023

"""Entrypoint for configuring and demonstrating Camera On the Home Network (COHN)."""

from __future__ import annotations

import argparse
import asyncio

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.logger import setup_logging
from open_gopro.util import add_cli_args_and_parse

console = Console()  # rich consoler printer

MDNS_SERVICE = "_gopro-web._tcp.local."

CURL_TEMPLATE = r"""curl -v -u 'gopro:{password}' --cacert cohn.crt 'https://{ip_addr}/gopro/camera/state'"""


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: WirelessGoPro | None = None
    try:
        # Start with Wifi Disabled (i.e. don't allow camera in AP mode).
        async with WirelessGoPro(args.identifier, enable_wifi=False) as gopro:
            if await gopro.is_cohn_provisioned:
                console.print("[yellow]COHN is already provisioned")
            else:
                if not args.ssid or not args.password:
                    raise ValueError("COHN needs to be provisioned but you didn't pass SSID credentials.")
                assert await gopro.connect_to_access_point(args.ssid, args.password)
            assert await gopro.configure_cohn()

            console.print("[blue]COHN is ready for communication. Dropping the BLE connection.")

        # Prove we can communicate via the COHN HTTP channel without a BLE or Wifi connection
        assert (await gopro.http_command.get_camera_state()).ok
        console.print("Successfully communicated via COHN!!")
        console.print(
            f"Sample curl command: {CURL_TEMPLATE.format(password=gopro._cohn.password, ip_addr=gopro._cohn.ip_address)}"  # type: ignore
        )

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()


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
