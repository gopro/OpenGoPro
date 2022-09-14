# connect_wifi.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:44 PM

"""Connect to the Wifi AP of a GoPro camera."""

import logging
import argparse
from typing import Optional

from rich.console import Console

from open_gopro import GoPro
from open_gopro.util import setup_logging, set_stream_logging_level, add_cli_args_and_parse

console = Console()  # rich consoler printer


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera's Wifi Access Point.")
    return add_cli_args_and_parse(parser)


def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)
    gopro: Optional[GoPro] = None

    with GoPro(args.identifier, wifi_interface=args.wifi_interface, sudo_password=args.password) as gopro:
        # Now we only want errors
        set_stream_logging_level(logging.ERROR)

        gopro.wifi_command.set_keep_alive()

        console.print("\n\n🎆🎇✨ Success!! Wifi AP is connected 📡\n")
        console.print("Send commands as per https://gopro.github.io/OpenGoPro/http")

        input("\nPress enter to disconnect Wifi and exit...")
        console.print("Exiting...")

    if gopro:
        gopro.close()


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
