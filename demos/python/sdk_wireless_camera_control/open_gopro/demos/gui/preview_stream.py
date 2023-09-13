# preview_stream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Example to start and view a preview stream"""

import argparse
import asyncio

from rich.console import Console

from open_gopro import Params, WirelessGoPro
from open_gopro.demos.gui.components.util import display_video_blocking
from open_gopro.logger import setup_logging
from open_gopro.util import add_cli_args_and_parse

console = Console()


async def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)

    async with WirelessGoPro(args.identifier) as gopro:
        await gopro.http_command.set_preview_stream(mode=Params.Toggle.DISABLE)
        await gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)
        assert (await gopro.http_command.set_preview_stream(mode=Params.Toggle.ENABLE)).ok

        console.print("Displaying the preview stream...")
        display_video_blocking(r"udp://127.0.0.1:8554", printer=console.print)

        await gopro.http_command.set_preview_stream(mode=Params.Toggle.DISABLE)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to the GoPro via BLE and Wifi, start a preview stream, then display it with CV2."
    )
    return add_cli_args_and_parse(parser, wifi=False)


def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
