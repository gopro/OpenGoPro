# usb.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 18 00:18:13 UTC 2022

"""Usb demo"""

import argparse

from rich.console import Console

from open_gopro import WiredGoPro, Params
from open_gopro.util import setup_logging, add_cli_args_and_parse

console = Console()  # rich consoler printer


def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)

    with WiredGoPro(args.identifier) as gopro:
        gopro.usb_command.get_camera_state()

        gopro.usb_command.wired_usb_control(Params.Toggle.DISABLE)
        print(f"Webcam is currently: {gopro.usb_command.webcam_status().flatten}")
        gopro.usb_command.webcam_start()

    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exercise the GoPro's USB interface.")
    return add_cli_args_and_parse(parser, wifi=False)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
