# livestream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Example to start and view a livestream"""

import time
import argparse
from typing import Optional

from rich.console import Console

from open_gopro import WirelessGoPro, Params, constants
from open_gopro.util import setup_logging, add_cli_args_and_parse, display_video_blocking

console = Console()  # rich consoler printer


def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)

    with WirelessGoPro(args.identifier, enable_wifi=False) as gopro:
        gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)
        gopro.ble_command.register_livestream_status(register=[Params.RegisterLiveStream.STATUS])

        console.print(f"Connecting to {args.ssid}...")
        gopro.ble_command.scan_wifi_networks()
        # Wait to receive scanning success
        scan_id: Optional[int] = None
        while update := gopro.get_notification():
            if (
                update == constants.ActionId.NOTIF_START_SCAN
                and update["scanning_state"] == Params.ScanState.SUCCESS
            ):
                scan_id = update["scan_id"]
                break
        # Get scan results and see if we need to provision
        assert scan_id
        for entry in gopro.ble_command.get_ap_entries(scan_id=scan_id)["entries"]:
            if entry["ssid"] == args.ssid:
                if not entry["scan_entry_flags"] & Params.ScanEntry.CONFIGURED:
                    gopro.ble_command.request_wifi_connect(ssid=args.ssid, password=args.password)
                    # Wait to receive provisioning done notification
                    while update := gopro.get_notification():
                        if (
                            update == constants.ActionId.NOTIF_PROVIS_STATE
                            and update["provisioning_state"] == Params.ProvisioningState.SUCCESS_NEW_AP
                        ):
                            break
                break

        # Start livestream
        console.print("Configuring livestream...")
        gopro.ble_command.set_livestream_mode(
            url=args.url,
            window_size=args.resolution,
            cert=bytes(),
            minimum_bitrate=args.min_bit,
            maximum_bitrate=args.max_bit,
            starting_bitrate=args.start_bit,
            lens=args.fov,
        )
        # Wait to receive livestream started status
        console.print("Waiting for livestream to be ready...")
        while update := gopro.get_notification():
            if (
                update == constants.ActionId.LIVESTREAM_STATUS_NOTIF
                and update["live_stream_status"] == Params.LiveStreamStatus.READY
            ):
                break
        console.print("Starting livestream")
        time.sleep(2)
        assert gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE).is_ok

        console.print("Displaying the video...")
        display_video_blocking(args.url)

        assert gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)
        gopro.ble_command.release_network()


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
        "--resolution",
        help="Resolution.",
        choices=[x.value for x in Params.WindowSize],
        default=Params.WindowSize.SIZE_480.value,
    )
    parser.add_argument(
        "--fov",
        help="Field of View.",
        choices=[x.value for x in Params.LensType],
        default=Params.LensType.WIDE.value,
    )
    return add_cli_args_and_parse(parser, wifi=False)


def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
