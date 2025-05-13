# usb.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 18 00:18:13 UTC 2022

"""USB / wireless webcam demo"""

import argparse
import asyncio
import sys

from rich.console import Console

from open_gopro import WiredGoPro, WirelessGoPro
from open_gopro.demos.gui.video_display import BufferlessVideoCapture
from open_gopro.gopro_base import GoProBase
from open_gopro.models.constants import (
    Toggle,
    WebcamError,
    WebcamProtocol,
    WebcamStatus,
)
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging

console = Console()


def get_stream_url(protocol: WebcamProtocol | None, gopro: GoProBase) -> str:
    """Get the stream URL for the given protocol using the gopros IP address if needed

    Args:
        protocol (WebcamProtocol | None): protocol to use. If None, TS will be used
        gopro (GoProBase): GoPro to use for the base IP address

    Returns:
        str: stream URL
    """
    match protocol:
        case WebcamProtocol.RTSP:
            return f"rtsp://{gopro.ip_address}:554/live"
        case WebcamProtocol.TS | None:
            return r"udp://0.0.0.0:8554"


async def wait_for_webcam_status(gopro: GoProBase, statuses: set[WebcamStatus], timeout: int = 10) -> bool:
    """Wait for specified webcam status(es) for a given timeout

    Args:
        gopro (GoProBase): gopro to communicate with
        statuses (set[WebcamStatus]): statuses to wait for
        timeout (int): timeout in seconds. Defaults to 10.

    Returns:
        bool: True if status was received before timing out, False if timed out or received error
    """

    async def poll_for_status() -> bool:
        # Poll until status is received
        while True:
            response = (await gopro.http_command.webcam_status()).data
            if response.error != WebcamError.SUCCESS:
                # Something bad happened
                console.print(f"[yellow]Received webcam error: {response.error}")
                return False
            if response.status in statuses:
                # We found the desired status
                return True

    # Wait for either status or timeout
    try:
        return await asyncio.wait_for(poll_for_status(), timeout)
    except TimeoutError:
        return False


# TODO handle COHN


async def main(args: argparse.Namespace) -> int:
    logger = setup_logging(__name__, args.log)
    gopro: GoProBase | None = None

    try:
        wireless_interfaces: set[WirelessGoPro.Interface] = set()
        # if args.cohn:
        #     wireless_interfaces = wireless_interfaces.union({WirelessGoPro.Interface.BLE, WirelessGoPro.Interface.COHN})
        # elif args.wifi:
        if args.wifi:
            wireless_interfaces = wireless_interfaces.union(
                {WirelessGoPro.Interface.BLE, WirelessGoPro.Interface.WIFI_AP}
            )
        async with (
            WirelessGoPro(
                args.identifier,
                host_wifi_interface=args.wifi_interface,
                interfaces=wireless_interfaces,
            )
            if wireless_interfaces
            else WiredGoPro(args.identifier)
        ) as gopro:
            assert gopro
            await gopro.http_command.wired_usb_control(control=Toggle.DISABLE)

            await gopro.http_command.set_shutter(shutter=Toggle.DISABLE)
            if (await gopro.http_command.webcam_status()).data.status not in {
                WebcamStatus.OFF,
                WebcamStatus.IDLE,
            }:
                console.print("[blue]Webcam is currently on. Turning if off.")
                assert (await gopro.http_command.webcam_stop()).ok
                await wait_for_webcam_status(gopro, {WebcamStatus.OFF})

            console.print("[blue]Starting webcam...")
            if (
                status := (await gopro.http_command.webcam_start(protocol=args.protocol)).data.error
            ) != WebcamError.SUCCESS:
                console.print(f"[red]Couldn't start webcam: {status}")
                return -1
            await wait_for_webcam_status(gopro, {WebcamStatus.HIGH_POWER_PREVIEW})

            # await ainput("Press enter to stop webcam and exit...")

            # Start player (blocks until user exists viewer)
            BufferlessVideoCapture(
                source=get_stream_url(args.protocol, gopro),
                protocol=BufferlessVideoCapture.Protocol(args.protocol.name),
                printer=console.print,
            ).display_blocking()
            console.print("[blue]Stopping webcam...")
            assert (await gopro.http_command.webcam_stop()).ok
            await wait_for_webcam_status(gopro, {WebcamStatus.OFF, WebcamStatus.IDLE})
            assert (await gopro.http_command.webcam_exit()).ok
            await wait_for_webcam_status(gopro, {WebcamStatus.OFF})
            console.print("Exiting...")

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()

    return 0


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Setup and view a GoPro webcam using TS protocol.")
    protocol = parser.add_argument_group(
        "protocol",
        "Mutually exclusive Protocol option if not default wired USB.",
    )
    group = protocol.add_mutually_exclusive_group()
    group.add_argument(
        "--wifi",
        action="store_true",
        help="Set to use wireless (BLE / WIFI AP) instead of wired (USB)) interface",
    )
    parser.add_argument(
        "--protocol",
        type=str,
        choices=["RTSP", "TS"],
        default=None,
        help="Streaming protocol to use. If not configured, default camera option will be used (normally RTSP)",
    )
    # group.add_argument(
    #     "--cohn",
    #     action="store_true",
    #     help="Communicate via COHN. Assumes COHN is already provisioned",
    # )
    args = add_cli_args_and_parse(parser)
    # Convert protocol string to enum if it is set
    match args.protocol:
        case "RTSP":
            args.protocol = WebcamProtocol.RTSP
        case "TS":
            args.protocol = WebcamProtocol.TS
        case None:
            pass
    return args


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    sys.exit(asyncio.run(main(parse_arguments())))


if __name__ == "__main__":
    entrypoint()
