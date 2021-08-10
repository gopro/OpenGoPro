# poll_battery.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Jul 30 21:36:24 UTC 2021

"""Example to continuously read the battery (with no WiFi connection)"""

import sys
import csv
import time
import logging
import argparse
import threading
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Tuple, Literal, List

from rich import traceback
from rich.logging import RichHandler
from rich.console import Console

from open_gopro import GoPro
from open_gopro.constants import StatusId

logger = logging.getLogger(__name__)
traceback.install()  # Enable exception tracebacks in rich logger
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

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return f"Index {self.index} @ time {self.time.strftime('%H:%M:%S')} --> bars: {self.bars}, percentage: {self.percentage}"

sample_index = 0
samples: List[Sample] = []

def dump_results_as_csv(location: Path) -> None:
    """Write all of the samples to a csv file

    Args:
        location (Path): File to write to
    """
    console.print(f"Dumping results as CSV to {location}")
    with open(location, mode="w") as f:
        w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(["index", "time", "percentage", "bars"])
        initial_time = samples[0].time
        for s in samples:
            w.writerow([s.index, (s.time - initial_time).seconds, s.percentage, s.bars])


def process_battery_notifications(gopro: GoPro, initial_bars: BarsType, initial_percentage: int) -> None:
    """Separate thread to continuously check for and store battery notifications.

    If the CLI parameter was set to poll, this isn't used.

    Args:
        gopro (GoPro): instance to get updates from
        initial_bars (BarsType): Initial bars level when notifications were enabled
        initial_percentage (int): Initial percentage when notifications were enabled
    """
    global sample_index
    global samples
    last_percentage = initial_percentage
    last_bars = initial_bars

    while True:
        # Block until we receive an update
        notification = gopro.get_update()
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
        samples.append(Sample(index=sample_index, percentage=last_percentage, bars=last_bars))
        console.print(str(samples[-1]))
        sample_index += 1


def main() -> None:
    """Main function."""
    identifier, log_location, poll = parse_arguments()
    setup_logging(log_location)

    global sample_index
    global samples

    try:
        with GoPro(identifier, enable_wifi=False) as gopro:
            # Now we only want errors and above since we're going to be doing a lot of printing below
            for handler in logger.handlers:
                if isinstance(handler, RichHandler):
                    handler.setLevel(logging.ERROR)

            # Ensure that wifi is not enabled. Not needed but left for instructive purposes
            assert not gopro.ble_status.ap_state.get_value().flatten

            # Setup notifications if we are not polling
            if poll is None:
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
            # Otherwise, poll
            else:
                with console.status("[bold green]Polling the battery until it dies..."):
                    while True:
                        samples.append(
                            Sample(
                                index=sample_index,
                                percentage=gopro.ble_status.int_batt_per.get_value().flatten,
                                bars=gopro.ble_status.batt_level.get_value().flatten,
                            )
                        )
                        console.print(str(samples[-1]))
                        sample_index += 1
                        time.sleep(poll)

    except Exception as e:  # pylint: disable=broad-except
        logger.error(repr(e))
        sys.exit(-1)
    except KeyboardInterrupt:
        logger.warning("Received keyboard interrupt. Shutting down...")
    finally:
        if len(samples) > 0:
            csv_location = Path(log_location.parent) / 'battery_results.csv'
            dump_results_as_csv(csv_location)
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


def parse_arguments() -> Tuple[str, Path, Optional[int]]:
    """Parse command line arguments

    Returns:
        Tuple[str, Path, Path]: (identifier, path to save log, path to VLC)
    """
    parser = argparse.ArgumentParser(
        description="Connect to the GoPro via BLE only and continuously read the battery (either by polling or notifications)."
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
        default="log_battery.log",
    )
    parser.add_argument(
        "-p",
        "--poll",
        type=int,
        help="Set to poll the battery at a given interval. If not set, battery level will be notified instead. Defaults to notifications.",
        default=None,
    )
    args = parser.parse_args()

    return args.identifier, args.log, args.poll


if __name__ == "__main__":
    main()
