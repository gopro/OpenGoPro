# livestream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Example to start and view a livestream"""

import argparse
import asyncio

from rich.console import Console

from open_gopro import Params, WirelessGoPro
from open_gopro.constants import WebcamError, WebcamStatus
from open_gopro.logger import setup_logging
from open_gopro.util import add_cli_args_and_parse, ainput

console = Console()


async def wait_for_webcam_status(gopro: WirelessGoPro, status: WebcamStatus, timeout: int = 10) -> bool:
    """Wait for a specified webcam status for a given timeout

    Args:
        gopro (WirelessGoPro): gopro to communicate with
        status (WebcamStatus): status to wait for
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
            if response.status == status:
                # We found the desired status
                return True

    # Wait for either status or timeout
    try:
        return await asyncio.wait_for(poll_for_status(), timeout)
    except TimeoutError:
        return False


async def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)

    async with WirelessGoPro(args.identifier) as gopro:
        await gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)
        if (await gopro.http_command.webcam_status()).data.status != WebcamStatus.OFF:
            console.print("[blue]Webcam is currently on. Turning if off.")
            assert (await gopro.http_command.webcam_stop()).ok
            await wait_for_webcam_status(gopro, WebcamStatus.OFF)

        console.print("[blue]Starting webcam...")
        await gopro.http_command.webcam_start()
        await wait_for_webcam_status(gopro, WebcamStatus.HIGH_POWER_PREVIEW)

        await ainput("Press enter to exit.", console.print)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to the GoPro via BLE and Wifi, start and view wireless webcam."
    )
    return add_cli_args_and_parse(parser)


def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
