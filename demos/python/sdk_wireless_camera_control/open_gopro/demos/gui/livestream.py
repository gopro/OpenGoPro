# livestream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Example to start and view a livestream"""

import argparse
import asyncio
from typing import Any

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.models import constants, proto
from open_gopro.util import add_cli_args_and_parse, ainput
from open_gopro.util.logger import setup_logging

console = Console()  # rich consoler printer


async def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)

    async with WirelessGoPro(args.identifier, enable_wifi=False) as gopro:
        await gopro.ble_command.set_shutter(shutter=constants.Toggle.DISABLE)
        await gopro.ble_command.register_livestream_status(
            register=[proto.EnumRegisterLiveStreamStatus.REGISTER_LIVE_STREAM_STATUS_STATUS]
        )

        console.print(f"[yellow]Connecting to {args.ssid}...")
        await gopro.access_point.connect(args.ssid, args.password)

        # Start livestream
        livestream_is_ready = asyncio.Event()

        async def wait_for_livestream_start(_: Any, update: proto.NotifyLiveStreamStatus) -> None:
            if update.live_stream_status == proto.EnumLiveStreamStatus.LIVE_STREAM_STATE_READY:
                livestream_is_ready.set()

        console.print("[yellow]Configuring livestream...")
        gopro.register_update(wait_for_livestream_start, constants.ActionId.LIVESTREAM_STATUS_NOTIF)
        await gopro.ble_command.set_livestream_mode(
            url=args.url,
            window_size=args.resolution,
            minimum_bitrate=args.min_bit,
            maximum_bitrate=args.max_bit,
            starting_bitrate=args.start_bit,
            encode=args.encode,
            lens=args.fov,
        )

        # Wait to receive livestream started status
        console.print("[yellow]Waiting for livestream to be ready...\n")
        await livestream_is_ready.wait()

        # TODO Is this still needed?
        await asyncio.sleep(2)

        console.print("[yellow]Starting livestream")
        assert (await gopro.ble_command.set_shutter(shutter=constants.Toggle.ENABLE)).ok

        console.print("[yellow]Livestream is now streaming and should be available for viewing.")
        await ainput("Press enter to stop livestreaming...\n")

        await gopro.ble_command.set_shutter(shutter=constants.Toggle.DISABLE)
        await gopro.ble_command.release_network()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to the GoPro via BLE only, configure then start a Livestream, then display it with CV2."
    )
    parser.add_argument("ssid", type=str, help="WiFi SSID to connect to.")
    parser.add_argument("password", type=str, help="Password of WiFi SSID.")
    parser.add_argument("url", type=str, help="RTMP server URL to stream to.")
    parser.add_argument("--min_bit", type=int, help="Minimum bitrate.", default=1000)
    parser.add_argument("--max_bit", type=int, help="Maximum bitrate.", default=1000)
    parser.add_argument("--start_bit", type=int, help="Starting bitrate.", default=1000)
    parser.add_argument(
        "--resolution", help="Resolution.", choices=list(proto.EnumWindowSize.values()), default=None, type=int
    )
    parser.add_argument("--fov", help="Field of View.", choices=list(proto.EnumLens.values()), default=None, type=int)
    parser.add_argument("--encode", help="Save video to sdcard.", action=argparse.BooleanOptionalAction)
    parser.set_defaults(encode=True)
    return add_cli_args_and_parse(parser, wifi=False)


def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
