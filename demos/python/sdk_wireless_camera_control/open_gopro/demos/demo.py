# demo.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Demonstration of using the GoPro package."""

import sys
import time
import logging
import argparse
import threading
from json import dumps
from pathlib import Path
from typing import Tuple

from rich import traceback
from rich.logging import RichHandler
from rich.console import Console

from open_gopro import GoPro, params, QueryCmdId
from open_gopro.util import launch_vlc

logger = logging.getLogger(__name__)
traceback.install()  # Enable exception tracebacks in rich logger
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
            console.print(f"{item} {description} now: {dumps(update[item])}")


def main() -> None:
    """Main function."""
    identifier, log_location, vlc_location = parse_arguments()
    setup_logging(log_location)

    try:
        with GoPro(identifier) as gopro:
            # Dump services to CSV
            gopro.services_as_csv()

            # Start a thread to handle asynchronous notifications
            threading.Thread(target=process_async_events, args=(gopro,), daemon=True).start()

            # Now we only want errors and above since we're going to be doing a lot of printing below
            for handler in logger.handlers:
                if isinstance(handler, RichHandler):
                    handler.setLevel(logging.ERROR)

            with console.status("[bold green]Ensuring the shutter is off..."):
                assert gopro.ble_command.set_shutter(params.Shutter.OFF).is_ok

            with console.status("[bold green]Ensuring turbo mode is off..."):
                assert gopro.ble_command.set_turbo_mode(False).is_ok

            with console.status("[bold green]Getting all statuses via BLE..."):
                for status, value in gopro.ble_command.get_camera_status().items():
                    console.print(f"{status} : {value}")

            with console.status("[bold green]Getting settings and statuses via WiFi..."):
                for item, value in gopro.wifi_command.get_camera_state().items():
                    console.print(f"{item} : {value}")

            with console.status("[bold green]Getting Open GoPro info..."):
                assert gopro.keep_alive()
                assert gopro.ble_command.set_third_party_client_info().is_ok
                version = gopro.ble_command.get_third_party_api_version()
                assert version.is_ok
                console.print(f"Version is {version['major']}.{version['minor']}")

            with console.status("[bold green]Setting Cinematic preset..."):
                assert gopro.ble_command.load_preset(params.Preset.CINEMATIC).is_ok

            with console.status("[bold green]Getting some individual values via BLE..."):
                resolution = gopro.ble_setting.resolution.get_value().flatten
                console.print(f"Current resolution is {resolution}")
                fov = gopro.ble_setting.video_field_of_view.get_value().flatten
                console.print(f"Current video FOV is {fov}")
                encoding = gopro.ble_status.encoding_active.get_value().flatten
                console.print(f"Current encoding status is {encoding}")

            with console.status("[bold green]Getting some capabilities via BLE..."):
                resolution_caps = gopro.ble_setting.resolution.get_capabilities_values().flatten
                console.print(f"Current resolution capabilities are: {dumps(resolution_caps)}")
                fov_caps = gopro.ble_setting.video_field_of_view.get_capabilities_values().flatten
                console.print(f"Current video FOV capabilities are: {dumps(fov_caps)}")

            with console.status("[bold green]Registering for push notifications..."):
                assert gopro.ble_setting.resolution.set(params.Resolution.RES_1080).is_ok
                fps_caps_update = gopro.ble_setting.fps.register_value_update().flatten
                console.print(f"New fps capabilities are: {dumps(fps_caps_update)}")
                assert gopro.ble_setting.resolution.register_value_update().is_ok
                assert gopro.ble_setting.resolution.register_capability_update().is_ok
                assert gopro.ble_setting.fps.register_capability_update().is_ok
                assert gopro.ble_setting.video_field_of_view.register_value_update().is_ok
                assert gopro.ble_setting.video_field_of_view.register_capability_update().is_ok
                assert gopro.ble_status.encoding_active.register_value_update().is_ok

            with console.status("[bold green]Taking a photo..."):
                assert gopro.ble_command.load_preset(params.Preset.PHOTO).is_ok
                assert gopro.ble_command.set_shutter(params.Shutter.ON).is_ok

            with console.status("[bold green]Taking a video..."):
                assert gopro.ble_command.load_preset(params.Preset.CINEMATIC).is_ok
                assert gopro.ble_command.set_shutter(params.Shutter.ON).is_ok
                time.sleep(2)  # Take a 2 second video
                assert gopro.ble_command.set_shutter(params.Shutter.OFF).is_ok

            with console.status("[bold green]Testing some capability pushes"):
                assert gopro.ble_setting.resolution.set(params.Resolution.RES_1080).is_ok
                assert gopro.ble_setting.fps.set(params.FPS.FPS_30).is_ok
                assert gopro.ble_setting.fps.set(params.FPS.FPS_240).is_ok
                assert gopro.ble_setting.resolution.get_capabilities_values().is_ok
                assert gopro.ble_setting.video_field_of_view.set(params.FieldOfView.LINEAR).is_ok
                assert gopro.ble_setting.video_field_of_view.set(params.FieldOfView.NARROW).is_ok
                assert gopro.ble_setting.video_field_of_view.set(params.FieldOfView.WIDE).is_ok
                # We expect this to fail as it is not valid with the current resolution
                assert not gopro.ble_setting.video_field_of_view.set(params.FieldOfView.SUPERVIEW).is_ok
                # Cycle through resolutions. This will cause other settings (and their capabilities) to update
                for resolution in resolution_caps:
                    assert gopro.ble_setting.resolution.set(resolution).is_ok

            with console.status("[bold green]Get media list and download some media..."):
                assert gopro.wifi_command.set_preset(params.Preset.PHOTO).is_ok
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

            with console.status("[bold green]Cycling through resolutions via WiFi..."):
                assert gopro.wifi_command.set_preset(params.Preset.CINEMATIC).is_ok
                assert gopro.wifi_setting.resolution.set(params.Resolution.RES_1080).is_ok
                assert gopro.wifi_setting.resolution.set(params.Resolution.RES_1440).is_ok
                assert gopro.wifi_setting.resolution.set(params.Resolution.RES_2_7k).is_ok
                assert gopro.wifi_setting.resolution.set(params.Resolution.RES_5k).is_ok
                assert gopro.wifi_setting.resolution.set(params.Resolution.RES_1080).is_ok

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
        sys.exit(-1)
    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
    finally:
        console.print("Exiting...")
        sys.exit(0)


def setup_logging(log_location: Path) -> None:
    """Configure logging to file and Rich console logging

    Args:
        log_location (Path): location to configure for the file handler
    """
    # Logging to file with
    fh = logging.FileHandler(f"{log_location}", mode="w")
    file_formatter = logging.Formatter(
        fmt="%(threadName)13s: %(name)40s:%(lineno)5d %(asctime)s.%(msecs)03d %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    fh.setFormatter(file_formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Use Rich for colorful console logging
    sh = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
    stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
    sh.setFormatter(stream_formatter)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    # Enable / disable logging in modules
    for (module, level) in [
        ("open_gopro.gopro", logging.DEBUG),
        ("open_gopro.ble_commands", logging.DEBUG),
        ("open_gopro.ble_controller", logging.DEBUG),
        ("open_gopro.wifi_commands", logging.DEBUG),
        ("open_gopro.wifi_controller", logging.DEBUG),
        ("open_gopro.responses", logging.DEBUG),
        ("open_gopro.util", logging.DEBUG),
        ("bleak", logging.DEBUG),
        ("bleak.backends.bluezdbus.client", logging.DEBUG),
        ("bleak.backends.corebluetooth.client", logging.DEBUG),
        ("bleak.backends.dotnet.client", logging.DEBUG),
    ]:
        log = logging.getLogger(module)
        log.setLevel(level)
        log.addHandler(fh)
        log.addHandler(sh)


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
