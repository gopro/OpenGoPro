# demo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Demonstration of using the GoPro package."""

import time
import logging
import argparse
import threading
from pathlib import Path
from typing import Tuple, Optional

from rich.console import Console

from open_gopro import GoPro
from open_gopro.constants import QueryCmdId
from open_gopro.util import launch_vlc, setup_logging, set_logging_level

logger = logging.getLogger(__name__)
console = Console()  # rich consoler printer


def process_async_events(gopro: GoPro) -> None:
    """Separate thread to continuously get and print asynchronous events from the GoPro instance.

    Args:
        gopro (GoPro): instance to get updates from
    """
    while True:
        # Block until we receive one
        update = gopro.get_update()

        # Print pushed updates (they're either setting capability or setting / status value updates)
        description = "capabilities are" if update.cmd is QueryCmdId.SETTING_CAPABILITY_PUSH else "value is"
        for item in update:
            console.print(f"{item} {description} now: {update[item]}")


def main() -> int:
    """Main demo functionality

    Returns:
        int: error code
    """
    identifier, log_location, vlc_location = parse_arguments()
    global logger
    logger = setup_logging(logger, log_location)

    gopro: Optional[GoPro] = None
    return_code = 0
    try:
        with GoPro(identifier) as gopro:
            # Dump services to CSV
            gopro._ble.services_as_csv()

            # Start a thread to handle asynchronous notifications
            threading.Thread(target=process_async_events, args=(gopro,), daemon=True).start()

            # Now we only want errors and above since we're going to be doing a lot of printing below
            set_logging_level(logger, logging.ERROR)

            with console.status("[bold green]Ensuring the shutter is off..."):
                if gopro.is_encoding:
                    assert gopro.ble_command.set_shutter(gopro.params.Shutter.OFF).is_ok

            with console.status("[bold green]Ensuring turbo mode is off..."):
                assert gopro.ble_command.set_turbo_mode(False).is_ok

            with console.status("[bold green]Getting all statuses via BLE..."):
                for status, value in gopro.ble_command.get_camera_statuses().items():
                    console.print(f"{status} : {value}")

            with console.status("[bold green]Getting settings and statuses via Wifi..."):
                for item, value in gopro.wifi_command.get_camera_state().items():
                    console.print(f"{item} : {value}")

            with console.status("[bold green]Getting Open GoPro info..."):
                assert gopro.keep_alive()
                assert gopro.ble_command.set_third_party_client_info().is_ok
                version = gopro.ble_command.get_open_gopro_api_version()
                assert version.is_ok
                console.print(f"Version is {version['major']}.{version['minor']}")

            with console.status("[bold green]Setting Cinematic preset..."):
                assert gopro.ble_command.load_preset(gopro.params.Preset.CINEMATIC).is_ok

            with console.status("[bold green]Getting some individual values via BLE..."):
                resolution = gopro.ble_setting.resolution.get_value().flatten
                console.print(f"Current resolution is {resolution}")
                fov = gopro.ble_setting.video_field_of_view.get_value().flatten
                console.print(f"Current video FOV is {fov}")
                encoding = gopro.ble_status.encoding_active.get_value().flatten
                console.print(f"Current encoding status is {encoding}")

            with console.status("[bold green]Getting some capabilities via BLE..."):
                resolution_caps = gopro.ble_setting.resolution.get_capabilities_values().flatten
                console.print(f"Current resolution capabilities are: {resolution_caps}")
                fov_caps = gopro.ble_setting.video_field_of_view.get_capabilities_values().flatten
                console.print(f"Current video FOV capabilities are: {fov_caps}")

            with console.status("[bold green]Registering for push notifications..."):
                assert gopro.ble_setting.resolution.set(gopro.params.Resolution.RES_1080).is_ok
                fps_caps_update = gopro.ble_setting.fps.register_value_update().flatten
                console.print(f"New fps capabilities are: {fps_caps_update}")
                assert gopro.ble_setting.resolution.register_value_update().is_ok
                assert gopro.ble_setting.resolution.register_capability_update().is_ok
                assert gopro.ble_setting.fps.register_capability_update().is_ok
                assert gopro.ble_setting.video_field_of_view.register_value_update().is_ok
                assert gopro.ble_setting.video_field_of_view.register_capability_update().is_ok
                assert gopro.ble_status.encoding_active.register_value_update().is_ok

            with console.status("[bold green]Taking a photo..."):
                assert gopro.ble_command.load_preset(gopro.params.Preset.PHOTO).is_ok
                assert gopro.ble_command.set_shutter(gopro.params.Shutter.ON).is_ok

            with console.status("[bold green]Taking a video..."):
                assert gopro.ble_command.load_preset(gopro.params.Preset.CINEMATIC).is_ok
                assert gopro.ble_command.set_shutter(gopro.params.Shutter.ON).is_ok
                time.sleep(2)  # Take a 2 second video
                assert gopro.ble_command.set_shutter(gopro.params.Shutter.OFF).is_ok

            with console.status("[bold green]Testing some capability pushes"):
                assert gopro.ble_setting.resolution.set(gopro.params.Resolution.RES_1080).is_ok
                assert gopro.ble_setting.fps.set(gopro.params.FPS.FPS_30).is_ok
                assert gopro.ble_setting.fps.set(gopro.params.FPS.FPS_240).is_ok
                assert gopro.ble_setting.resolution.get_capabilities_values().is_ok
                assert gopro.ble_setting.video_field_of_view.set(gopro.params.VideoFOV.LINEAR).is_ok
                assert gopro.ble_setting.video_field_of_view.set(gopro.params.VideoFOV.NARROW).is_ok
                assert gopro.ble_setting.video_field_of_view.set(gopro.params.VideoFOV.WIDE).is_ok
                # We expect this to fail as it is not valid with the current resolution
                assert not gopro.ble_setting.video_field_of_view.set(gopro.params.VideoFOV.MAX_SUPERVIEW).is_ok
                # Cycle through resolutions. This will cause other settings (and their capabilities) to update
                for resolution in resolution_caps:
                    assert gopro.ble_setting.resolution.set(resolution).is_ok

            with console.status("[bold green]Get media list and download some media..."):
                assert gopro.wifi_command.set_preset(gopro.params.Preset.PHOTO).is_ok
                media_list = gopro.wifi_command.get_media_list()["media"][0]["fs"]
                # Find a picture and download it
                picture = ""
                for file in [x["n"] for x in media_list]:
                    if file.lower().endswith(".jpg"):
                        picture = file
                        gopro.wifi_command.download_file(camera_file=picture)
                        break
                # Find a video and download it
                video = ""
                for file in [x["n"] for x in media_list]:
                    if file.lower().endswith(".mp4"):
                        video = file
                        gopro.wifi_command.download_file(camera_file=video)
                        break

            with console.status("[bold green]Getting media information..."):
                assert gopro.wifi_command.get_media_info(video).is_ok
                assert gopro.wifi_command.get_media_info(picture).is_ok
                gopro.wifi_command.get_gpmf_data(camera_file=picture)
                gopro.wifi_command.get_screennail(camera_file=video)
                gopro.wifi_command.get_telemetry(camera_file=video)
                gopro.wifi_command.get_thumbnail(camera_file=picture)
                assert gopro.wifi_command.get_preset_status().is_ok

            with console.status("[bold green]Cycling through resolutions via Wifi..."):
                assert gopro.wifi_command.set_preset(gopro.params.Preset.CINEMATIC).is_ok
                for resolution in gopro.params.Resolution:
                    assert gopro.wifi_setting.resolution.set(resolution).is_ok

            with console.status("[bold green]Starting the preview stream..."):
                gopro.wifi_command.stop_preview_stream()
                gopro.wifi_command.start_preview_stream()

            console.print("Preview stream is enabled. View with a UDP server at udp://@:8554.")
            console.print("Send keyboard interrupt to exit.")

            threading.Thread(target=launch_vlc, args=(vlc_location,), daemon=True).start()

            while True:
                time.sleep(0.2)

    except Exception as e:  # pylint: disable=broad-except
        logger.error(repr(e))
        return_code = 1
    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
    finally:
        if gopro is not None:
            gopro.close()
        console.print("Exiting...")
        return return_code  # pylint: disable=lost-exception


def parse_arguments() -> Tuple[str, Path, Path]:
    """Parse command line arguments

    Returns:
        Tuple[str, Path, Path]: (identifier, path to save log, path to VLC)
    """
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE and Wifi and do some things."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. \
            If not used, first discovered GoPro will be connected to",
        default=None,
    )
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        help="Location to store detailed log",
        default="gopro_demo.log",
    )
    parser.add_argument(
        "-v",
        "--vlc",
        type=Path,
        help="VLC location. If not set, the location will attempt to be automatically discovered.",
        default=None,
    )
    args = parser.parse_args()

    return args.identifier, args.log, args.vlc


if __name__ == "__main__":
    main()
