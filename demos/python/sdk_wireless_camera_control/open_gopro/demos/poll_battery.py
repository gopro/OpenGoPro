"""Example to poll the battery (with no WiFi connection)"""

import sys
import time
import logging
import argparse
from pathlib import Path
from typing import Tuple

from rich import traceback
from rich.logging import RichHandler
from rich.console import Console

from open_gopro import GoPro

logger = logging.getLogger(__name__)
traceback.install()  # Enable exception tracebacks in rich logger
console = Console()  # rich consoler printer


def main() -> None:
    """Main function."""
    identifier, log_location = parse_arguments()
    setup_logging(log_location)

    try:
        with GoPro(identifier, enable_wifi=False) as gopro:
            # Now we only want errors and above since we're going to be doing a lot of printing below
            for handler in logger.handlers:
                if isinstance(handler, RichHandler):
                    handler.setLevel(logging.ERROR)

            # Ensure that wifi is not enabled. Not needed but left for instructive purposes
            assert not gopro.ble_status.ap_state.get_value().flatten

            samples = []
            with console.status("[bold green]Polling the battery until it dies..."):
                for x in range(1000):
                    battery_percentage = gopro.ble_status.int_batt_per.get_value().flatten
                    battery_bars = gopro.ble_status.batt_level.get_value().flatten
                    samples.append((x, time.asctime(), battery_percentage, battery_bars))
                    console.print(
                        f"sample {samples[-1][0]} @ time {samples[-1][1]} Percentage: {samples[-1][2]}, Bars: {samples[-1][3]}"
                    )
                    time.sleep(5)

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


def parse_arguments() -> Tuple[str, Path]:
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
    args = parser.parse_args()

    return args.identifier, args.log


if __name__ == "__main__":
    main()
