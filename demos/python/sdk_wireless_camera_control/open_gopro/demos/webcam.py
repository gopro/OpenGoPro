# usb.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 18 00:18:13 UTC 2022

"""Usb demo"""

import argparse
from typing import Final
from pathlib import Path
import multiprocessing as mp
from multiprocessing.synchronize import Event

from rich.console import Console
import cv2 as cv

from open_gopro import WiredGoPro, Params
from open_gopro.util import setup_logging

console = Console()  # rich consoler printer

started_event = mp.Event()

STREAM_URL: Final[str] = r"udp://0.0.0.0:8554"


def view_webcam(event: Event) -> None:
    """Multiprocessing target to view webcam

    Args:
        event (Event): Event to set once stream is ready for viewing
    """
    vid = cv.VideoCapture(STREAM_URL + "?overrun_nonfatal=1&fifo_size=50000000", cv.CAP_FFMPEG)
    event.set()

    while True:
        ret, frame = vid.read()
        if ret:
            cv.imshow("frame", frame)
        cv.waitKey(1)  # Show for 1 millisecond


def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    with WiredGoPro(args.identifier) as gopro:
        # Start webcam
        gopro.usb_command.wired_usb_control(Params.Toggle.DISABLE)
        gopro.usb_command.webcam_start()

        # Start player
        logger.info("Starting Viewer")
        mp.Process(target=view_webcam, daemon=True, args=(started_event,)).start()
        started_event.wait()
        logger.info("Player started.")

        # Wait for input to exit
        input("Press enter to exit.")
        gopro.usb_command.webcam_stop()
        gopro.usb_command.webcam_exit()
        # Process is a daemon so no need to stop it

    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Setup and view a GoPro webcam.")
    parser.add_argument(
        "identifier",
        type=str,
        help="Last 3 digits of GoPro serial number, which is the last 3 digits of the default camera SSID.",
    )
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        help="Location to store detailed log",
        default="gopro_demo.log",
    )
    return parser.parse_args()


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
