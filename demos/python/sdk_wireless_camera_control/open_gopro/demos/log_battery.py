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
from typing import Optional

from rich.console import Console

from open_gopro import WirelessGoPro, types
from open_gopro.constants import StatusId
from open_gopro.logger import set_stream_logging_level, setup_logging
from open_gopro.util import add_cli_args_and_parse, ainput

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


async def process_battery_notifications(update: types.UpdateType, value: int) -> None:
    """Handle asynchronous battery update notifications

    Args:
        update (types.UpdateType): type of update
        value (int): value of update
    """

    global last_percentage
    global last_bars

    if update == StatusId.INT_BATT_PER:
        last_percentage = value
    elif update == StatusId.BATT_LEVEL:
        last_bars = value

    # Append and print sample
    global SAMPLE_INDEX
    SAMPLES.append(Sample(index=SAMPLE_INDEX, percentage=last_percentage, bars=last_bars))
    console.print(str(SAMPLES[-1]))
    SAMPLE_INDEX += 1


async def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    gopro: Optional[WirelessGoPro] = None
    try:
        async with WirelessGoPro(args.identifier, enable_wifi=False) as gopro:
            set_stream_logging_level(logging.ERROR)

            async def log_battery() -> None:
                global SAMPLE_INDEX
                if args.poll:
                    with console.status("[bold green]Polling the battery until it dies..."):
                        while True:
                            SAMPLES.append(
                                Sample(
                                    index=SAMPLE_INDEX,
                                    percentage=(await gopro.ble_status.int_batt_per.get_value()).data,
                                    bars=(await gopro.ble_status.batt_level.get_value()).data,
                                )
                            )
                            console.print(str(SAMPLES[-1]))
                            SAMPLE_INDEX += 1
                            await asyncio.sleep(args.poll)
                else:  # Not polling. Set up notifications
                    global last_bars
                    global last_percentage

                    console.print("Configuring battery notifications...")
                    # Enable notifications of the relevant battery statuses. Also store initial values.
                    last_bars = (
                        await gopro.ble_status.batt_level.register_value_update(process_battery_notifications)
                    ).data
                    last_percentage = (
                        await gopro.ble_status.int_batt_per.register_value_update(process_battery_notifications)
                    ).data
                    # Append initial sample
                    SAMPLES.append(Sample(index=SAMPLE_INDEX, percentage=last_percentage, bars=last_bars))
                    console.print(str(SAMPLES[-1]))
                    console.print("[bold green]Receiving battery notifications until it dies...")

            asyncio.create_task(log_battery())
            await ainput("[purple]Press enter to exit.", console.print)
            console.print("Exiting...")

    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
    if SAMPLES:
        csv_location = Path(args.log.parent) / "battery_results.csv"
        dump_results_as_csv(csv_location)
    if gopro:
        await gopro.close()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to the GoPro via BLE only and continuously read the battery (either by polling or notifications)."
    )
    parser.add_argument(
        "-p",
        "--poll",
        type=int,
        help="Set to poll the battery at a given interval. If not set, battery level will be notified instead. Defaults to notifications.",
        default=None,
    )
    return add_cli_args_and_parse(parser, wifi=False)


def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
