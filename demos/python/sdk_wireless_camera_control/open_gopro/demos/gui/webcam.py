# usb.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 18 00:18:13 UTC 2022

"""USB / wireless webcam demo"""

import argparse
import asyncio
import logging
import sys

from returns.pipeline import is_successful
from rich.console import Console

from open_gopro import WiredGoPro, WirelessGoPro
from open_gopro.demos.gui.video_display import BufferlessVideoCapture
from open_gopro.gopro_base import GoProBase
from open_gopro.models.streaming import StreamType, WebcamProtocol, WebcamStreamOptions
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import set_stream_logging_level, setup_logging
from open_gopro.util.util import ainput

console = Console()


async def main(args: argparse.Namespace) -> int:
    logger = setup_logging(__name__, args.log)
    gopro: GoProBase | None = None

    try:
        wireless_interfaces: set[WirelessGoPro.Interface] = set()
        if args.wireless:
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
            set_stream_logging_level(logging.WARNING)
            with console.status(f"Starting webcam stream with protocol {args.protocol}..."):
                if not is_successful(
                    result := (
                        await gopro.streaming.start_stream(
                            stream_type=StreamType.WEBCAM,
                            options=WebcamStreamOptions(protocol=args.protocol),
                        )
                    )
                ):
                    console.print(f"[red]Failed to start webcam stream: {result.failure()}")
                    return 1

            url = gopro.streaming.url if args.protocol == WebcamProtocol.RTSP else "udp://@:8554"
            console.print(f"Preview stream started. It can be viewed in VLC at [yellow]{url}")
            console.print(
                "Press Enter to view the preview stream using Python CV2. Once started, it won't be viewable in VLC."
            )
            await ainput("")

            with console.status("Displaying the preview stream..."):
                assert gopro.streaming.url
                BufferlessVideoCapture(
                    source=gopro.streaming.url,
                    protocol=BufferlessVideoCapture.Protocol(args.protocol.name),
                    printer=console.print,
                ).display_blocking()

            with console.status("Stopping preview stream..."):
                await gopro.streaming.stop_active_stream()
        return 0

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))

    if gopro:
        await gopro.close()

    return 0


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Setup and view a GoPro webcam stream.")
    parser.add_argument(
        "--wireless",
        action="store_true",
        help="Set to use wireless (BLE / WIFI AP) instead of wired (USB) interface",
    )
    parser.add_argument(
        "--protocol",
        type=str,
        choices=["RTSP", "TS"],
        default="TS",
        help="Streaming protocol to use. Defaults to TS. RTSP is not supported on all GoPro models.",
    )
    args = add_cli_args_and_parse(parser)
    # Convert protocol string to enum if it is set
    match args.protocol.lower():
        case "rtsp":
            args.protocol = WebcamProtocol.RTSP
        case "ts":
            args.protocol = WebcamProtocol.TS
    return args


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    sys.exit(asyncio.run(main(parse_arguments())))


if __name__ == "__main__":
    entrypoint()
