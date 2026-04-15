# dump_gatt.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Sun Feb  9 2026

"""Entrypoint for dumping BLE GATT attribute table to CSV."""

import argparse
import asyncio
from pathlib import Path

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.util import add_cli_args_and_parse
from open_gopro.util.logger import setup_logging

console = Console()


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: WirelessGoPro | None = None

    try:
        async with WirelessGoPro(args.identifier, interfaces={WirelessGoPro.Interface.BLE}) as gopro:
            output_file = args.output
            console.print(f"Dumping GATT attribute table to {output_file.absolute()}...")
            gopro._ble.gatt_db.dump_to_csv(output_file)
            console.print(f"Success!! :smiley: GATT table has been written to {output_file.absolute()}")

    except Exception as e:  # pylint: disable = broad-except
        logger.error(repr(e))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE and dump the GATT attribute table to CSV."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Where to write the CSV file. Defaults to 'gatt_attributes.csv'",
        default=Path("gatt_attributes.csv"),
    )

    return add_cli_args_and_parse(parser)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
