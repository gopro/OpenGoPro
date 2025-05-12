# cohn.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Oct 24 19:08:07 UTC 2023

"""Entrypoint for configuring and demonstrating Camera On the Home Network (COHN)."""

from __future__ import annotations

import argparse
import asyncio
import textwrap
from pathlib import Path

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging

console = Console()  # rich consoler printer

COHN_CURL_CMD_TEMPLATE = (
    r"""curl --insecure -v -u 'gopro:{password}' --cacert cohn.crt 'https://{ip_addr}/gopro/camera/state'"""
)


def dump_cohn_collateral(gopro: WirelessGoPro) -> None:
    """Print the COHN credentials and write the certificate to a file.

    Args:
        gopro (WirelessGoPro): gopro to retrieve the credentials from
    """
    assert gopro.cohn.credentials
    console.print(
        f"Sample curl command: {COHN_CURL_CMD_TEMPLATE.format(
        password=gopro.cohn.credentials.password,
        ip_addr=gopro.cohn.credentials.ip_address,)}"
    )
    with open("cohn.crt", "w") as f:
        f.write(gopro.cohn.credentials.certificate)


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: WirelessGoPro | None = None
    try:
        # If we weren't explicitly passed an identifier, we will try to find the first camera available
        if identifier := args.identifier:
            console.print(f"Attempting to directly communicate via COHN to GoPro {identifier}")
        else:
            # Start with Wifi Disabled (i.e. don't allow camera in AP mode) and only connect BLE to check COHN status / provision
            async with WirelessGoPro(
                target=args.identifier,
                interfaces={WirelessGoPro.Interface.BLE},
                cohn_db=args.db,
            ) as gopro:
                if await gopro.cohn.is_configured:
                    console.print("COHN is already configured.")
                else:
                    if not args.ssid or not args.password:
                        raise ValueError("COHN needs to be provisioned but you didn't pass SSID or password.")
                    await gopro.access_point.connect(args.ssid, args.password)
                    await gopro.cohn.configure(force_reprovision=True)

                console.print("[blue]COHN is ready for communication. Dropping the BLE connection.")
                dump_cohn_collateral(gopro)

            identifier = gopro.identifier
        # Now create an object with only COHN
        async with WirelessGoPro(
            target=identifier,
            interfaces={WirelessGoPro.Interface.COHN},
            cohn_db=args.db,
        ) as gopro:
            # Prove we can communicate via the COHN HTTP channel without a BLE or Wifi connection
            assert (await gopro.http_command.get_camera_state()).ok
            console.print("Successfully communicated via COHN!!")
            dump_cohn_collateral(gopro)

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
        Open GoPro Camera on the Home Network (COHN) Utility
        ----------------------------------------------------
        This utility is used to configure and demonstrate the Camera On the Home
        Network (COHN) feature of GoPro cameras. COHN allows the camera to be accessed
        over a local network using HTTP, without the need for a direct Wi-Fi or Bluetooth
        connection.

        There are three main modes of operation that are chosen based on the arguments
        passed to this script:

        1. COHN Provisioning: If the camera is not already provisioned for COHN, you can
           provide the SSID (--ssid) and password (--password) of the Wi-Fi network to
           which the camera should connect. The script will then (re)configure the camera
           for COHN using these credentials.

        2. COHN Communication without initial BLE check: If the camera is already
           provisioned for COHN, you can directly communicate with it using the COHN
           HTTP channel. This is done by passing the camera's identifier (--identifier)
           which is the trailing 4 digits of the serial number.

        3. COHN Communication with initial BLE check: If you don't provide an identifier,
           the script will first attempt to find the first available camera using BLE. If
           it finds a camera that is already provisioned for COHN, it will connect to it
           and demonstrate COHN communication. If it finds a camera that is not provisioned
           for COHN, it will return an error message and exit if you didn't pass SSID and
           password. If you pass SSID and password, this is the same as the first mode of
           operation.

        Therefore, the general procedure for a freshly factory-reset camera is:
            1. Use operation mode 1 to provision COHN
            2. Use operation mode 2 to communicate with (only) COHN
        """
        ),
    )
    parser.add_argument(
        "--ssid",
        type=str,
        help="WiFi SSID to connect. Mutually inclusive with --password.",
        default=None,
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Password of WiFi SSID. Mutually inclusive with --ssid.",
        default=None,
    )
    parser.add_argument(
        "--db",
        type=Path,
        help="path to COHN database file. Defaults to cohn_db.json",
        default=Path("cohn_db.json"),
    )
    args = add_cli_args_and_parse(parser, wifi=False)
    if args.ssid and not args.password:
        parser.error("The --ssid argument requires --password to also be set.")
    return args


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
