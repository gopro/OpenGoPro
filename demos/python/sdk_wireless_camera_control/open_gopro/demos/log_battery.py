# log_battery.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Example to continuously read the battery (with no Wifi connection)"""

import argparse
import asyncio
import csv
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.models.constants import StatusId
from open_gopro.util import add_cli_args_and_parse, ainput
from open_gopro.util.logger import set_stream_logging_level, setup_logging

console = Console()

last_percentage = 0
last_bars = 0


@dataclass
class Sample:
    """Simple class to store battery samples"""

    index: int
    percentage: int
    bars: int

    def __post_init__(self) -> None:
        self.time = datetime.now()

    def __str__(self) -> str:
        return f"Index {self.index} @ time {self.time.strftime('%H:%M:%S')} --> bars: {self.bars}, percentage: {self.percentage}"


SAMPLE_INDEX = 0
SAMPLES: list[Sample] = []


def dump_results_as_csv(location: Path) -> None:
    """Write all of the samples to a csv file

    Args:
        location (Path): File to write to
    """
    console.print(f"Dumping results as CSV to {location}")
    with open(location, mode="w") as f:
        w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(["index", "time", "percentage", "bars"])
        initial_time = SAMPLES[0].time
        for s in SAMPLES:
            w.writerow([s.index, (s.time - initial_time).seconds, s.percentage, s.bars])


async def process_status(
    update: Literal[StatusId.INTERNAL_BATTERY_BARS, StatusId.INTERNAL_BATTERY_PERCENTAGE],
    value: int,
) -> None:
    """TODO

    Args:
        update (Literal[StatusId.INTERNAL_BATTERY_BARS, StatusId.INTERNAL_BATTERY_PERCENTAGE]): _description_
        value (int): _description_
    """
    global last_percentage
    global last_bars

    match update:
        case StatusId.INTERNAL_BATTERY_PERCENTAGE:
            last_percentage = value
        case StatusId.INTERNAL_BATTERY_BARS:
            last_bars = value

    # Append and print sample
    global SAMPLE_INDEX
    SAMPLES.append(Sample(index=SAMPLE_INDEX, percentage=last_percentage, bars=last_bars))
    console.print(str(SAMPLES[-1]))
    SAMPLE_INDEX += 1


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: WirelessGoPro | None = None
    try:
        async with WirelessGoPro(args.identifier, interfaces={WirelessGoPro.Interface.BLE}) as gopro:
            set_stream_logging_level(logging.ERROR)

            async def process_percentage() -> None:
                async for percentage in (
                    (await gopro.ble_status.internal_battery_percentage.get_value_observable()).unwrap().observe()
                ):
                    await process_status(StatusId.INTERNAL_BATTERY_PERCENTAGE, percentage)

            async def process_bars() -> None:
                async for bars in (
                    (await gopro.ble_status.internal_battery_bars.get_value_observable()).unwrap().observe()
                ):
                    await process_status(StatusId.INTERNAL_BATTERY_BARS, bars)

            await asyncio.wait(
                [
                    asyncio.create_task(process_percentage()),
                    asyncio.create_task(process_bars()),
                    asyncio.create_task(ainput("Press enter to stop exit...")),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )
            console.print("Exiting...")

    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
    if SAMPLES:
        csv_location = Path(args.log.parent) / "battery_results.csv"
        dump_results_as_csv(csv_location)
    if gopro:
        await gopro.close()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to the GoPro via BLE only and track the battery status.")
    return add_cli_args_and_parse(parser, wifi=False)


def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
