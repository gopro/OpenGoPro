# log_battery.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:45 PM

"""Example to continuously read the battery (with no Wifi connection)"""

import csv
import time
import logging
import argparse
import threading
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Literal

from rich.console import Console

from open_gopro import WirelessGoPro
from open_gopro.constants import StatusId
from open_gopro.util import setup_logging, set_stream_logging_level, add_cli_args_and_parse

console = Console()  # rich consoler printer

BarsType = Literal[0, 1, 2, 3]


@dataclass
class Sample:
    """Simple class to store battery samples"""

    index: int
    percentage: int
    bars: BarsType

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


def process_battery_notifications(
    gopro: WirelessGoPro, initial_bars: BarsType, initial_percentage: int
) -> None:
    """Separate thread to continuously check for and store battery notifications.

    If the CLI parameter was set to poll, this isn't used.

    Args:
        gopro (WirelessGoPro): instance to get updates from
        initial_bars (BarsType): Initial bars level when notifications were enabled
        initial_percentage (int): Initial percentage when notifications were enabled
    """
    last_percentage = initial_percentage
    last_bars = initial_bars

    # Block until we receive an update
    while notification := gopro.get_notification():
        # Update data points if they have changed
        last_percentage = (
            notification.data[StatusId.INT_BATT_PER]
            if StatusId.INT_BATT_PER in notification.data
            else last_percentage
        )
        last_bars = (
            notification.data[StatusId.BATT_LEVEL] if StatusId.BATT_LEVEL in notification.data else last_bars
        )
        # Append and print sample
        global SAMPLE_INDEX
        SAMPLES.append(Sample(index=SAMPLE_INDEX, percentage=last_percentage, bars=last_bars))
        console.print(str(SAMPLES[-1]))
        SAMPLE_INDEX += 1


def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)
    global SAMPLE_INDEX

    gopro: Optional[WirelessGoPro] = None
    try:
        with WirelessGoPro(args.identifier, enable_wifi=False) as gopro:
            set_stream_logging_level(logging.ERROR)

            if args.poll:
                with console.status("[bold green]Polling the battery until it dies..."):
                    while True:
                        SAMPLES.append(
                            Sample(
                                index=SAMPLE_INDEX,
                                percentage=gopro.ble_status.int_batt_per.get_value().flatten,
                                bars=gopro.ble_status.batt_level.get_value().flatten,
                            )
                        )
                        console.print(str(SAMPLES[-1]))
                        SAMPLE_INDEX += 1
                        time.sleep(args.poll)
            # Otherwise set up notifications
            else:
                console.print("Configuring battery notifications...")
                # Enable notifications of the relevant battery statuses. Also store initial values.
                bars = gopro.ble_status.batt_level.register_value_update().flatten
                percentage = gopro.ble_status.int_batt_per.register_value_update().flatten
                # Start a thread to handle asynchronous battery level notifications
                threading.Thread(
                    target=process_battery_notifications, args=(gopro, bars, percentage), daemon=True
                ).start()
                with console.status("[bold green]Receiving battery notifications until it dies..."):
                    # Sleep forever, allowing notification handler thread to deal with battery level notifications
                    while True:
                        time.sleep(1)

    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
    if len(SAMPLES) > 0:
        csv_location = Path(args.log.parent) / "battery_results.csv"
        dump_results_as_csv(csv_location)
    if gopro:
        gopro.close()
    console.print("Exiting...")


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
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
