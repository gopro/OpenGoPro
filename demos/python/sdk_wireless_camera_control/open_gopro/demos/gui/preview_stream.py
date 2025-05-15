# preview_stream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Example to start and view a preview stream"""

import argparse
import asyncio

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.demos.gui.video_display import BufferlessVideoCapture
from open_gopro.models import streaming
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging

console = Console()


async def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)

    async with WirelessGoPro(args.identifier) as gopro:
        console.print("Starting preview stream...")
        await gopro.streaming.start_stream(
            streaming.StreamType.PREVIEW,
            streaming.PreviewStreamOptions(port=args.port),
        )

        console.print("Displaying the preview stream...")
        assert gopro.streaming.url
        BufferlessVideoCapture(
            source=gopro.streaming.url,
            protocol=BufferlessVideoCapture.Protocol.TS,
            printer=console.print,
        ).display_blocking()

        console.print("Stopping preview stream...")
        await gopro.streaming.stop_active_stream()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to the GoPro via BLE and Wifi, start a preview stream, then display it with CV2."
    )
    parser.add_argument(
        "--port", type=int, help="Port to use for livestream. Defaults to 8554 if not set", default=8554
    )
    return add_cli_args_and_parse(parser, wifi=False)


def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
