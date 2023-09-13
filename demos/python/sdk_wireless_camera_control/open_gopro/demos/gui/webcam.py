# usb.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 18 00:18:13 UTC 2022

"""USB webcam demo"""

import argparse
import asyncio
from typing import Final

from rich.console import Console

from open_gopro import Params, WiredGoPro, WirelessGoPro
from open_gopro.constants import WebcamError, WebcamStatus
from open_gopro.demos.gui.components.util import display_video_blocking
from open_gopro.gopro_base import GoProBase
from open_gopro.logger import setup_logging
from open_gopro.util import add_cli_args_and_parse

console = Console()

STREAM_URL: Final[str] = r"udp://0.0.0.0:8554"


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
                return False
            if response.status in statuses:
                # We found the desired status
                return True

    # Wait for either status or timeout
    try:
        return await asyncio.wait_for(poll_for_status(), timeout)
    except TimeoutError:
        return False


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)
    gopro: GoProBase | None = None

    try:
        async with (
            WirelessGoPro(args.identifier, wifi_interface=args.wifi_interface)  # type: ignore
            if args.wireless
            else WiredGoPro(args.identifier)
        ) as gopro:
            assert gopro
            await gopro.http_command.wired_usb_control(control=Params.Toggle.DISABLE)

            await gopro.http_command.set_shutter(shutter=Params.Toggle.DISABLE)
            if (await gopro.http_command.webcam_status()).data.status not in {
                WebcamStatus.OFF,
                WebcamStatus.IDLE,
            }:
                console.print("[blue]Webcam is currently on. Turning if off.")
                assert (await gopro.http_command.webcam_stop()).ok
                await wait_for_webcam_status(gopro, {WebcamStatus.OFF})

            console.print("[blue]Starting webcam...")
            await gopro.http_command.webcam_start()
            await wait_for_webcam_status(gopro, {WebcamStatus.HIGH_POWER_PREVIEW})

            # Start player
            display_video_blocking(STREAM_URL, printer=console.print)  # blocks until user exists viewer
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


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Setup and view a GoPro webcam.")
    parser.add_argument(
        "--wireless",
        action="store_true",
        help="Set to use wireless (BLE / WIFI) instead of wired (USB)) interface",
    )
    return add_cli_args_and_parse(parser)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
