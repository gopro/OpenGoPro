# util.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:50 PM

"""Miscellaneous utilities for the GoPro package."""

import sys
import queue
import logging
import subprocess
from pathlib import Path
from typing import Dict, Type, Any, List, Optional, Union

from rich.logging import RichHandler
from rich import traceback

util_logger = logging.getLogger(__name__)


def setup_logging(logger: Any, output: Path, modules: Dict[str, int] = None) -> Any:
    """Configure open gopro modules for logging

    The application's logger is passed in, modified, and then returned

    Args:
        logger (Any): input logger that will be modified and then returned
        output (Path): Path of log file for file stream handler
        modules (Dict[str, int], optional): Optional override of modules / levels.

    Returns:
        Any: updated logger that the application can use for logging
    """
    modules = modules or {
        "open_gopro.gopro": logging.DEBUG,
        "open_gopro.api.builders": logging.DEBUG,
        "open_gopro.communication_client": logging.DEBUG,
        "open_gopro.ble.adapters.bleak_wrapper": logging.DEBUG,
        "open_gopro.wifi.adapters.wireless": logging.DEBUG,
        "open_gopro.responses": logging.DEBUG,
        "open_gopro.util": logging.DEBUG,
        "bleak": logging.DEBUG,
    }

    # Logging to file with millisecond timing
    fh = logging.FileHandler(output, mode="w")
    file_formatter = logging.Formatter(
        fmt="%(threadName)13s:%(asctime)s.%(msecs)03d %(filename)-26s %(lineno)4s %(levelname)-8s | %(message)s",
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
    for module, level in modules.items():
        l = logging.getLogger(module)
        l.setLevel(level)
        l.addHandler(fh)
        l.addHandler(sh)

    traceback.install()  # Enable exception tracebacks in rich logger

    return logger


def set_logging_level(logger: Any, level: int) -> None:
    """Change the global logging level

    Args:
        logger (Any): logger to update
        level (int): level to set
    """
    for handler in logger.handlers:
        if isinstance(handler, RichHandler):
            handler.setLevel(level)


def launch_vlc(location: Optional[Path]) -> None:
    """Launch VLC

    Args:
        location (Optional[Path]): path to VLC. If None, it will be automatically discovered
    """
    # This is a fairly lazy way to find VLC. We'll call it best effort.
    potential_vlc_locations: List[Union[Path, str]] = []
    command = "echo Invalid Platform"
    if "linux" in sys.platform.lower():
        potential_vlc_locations = [r'"/snap/bin/vlc"']
        command = 'su $(id -un 1000) -c "{} udp://@:8554 > /dev/null 2>&1 &"'
    elif "darwin" in sys.platform.lower():
        potential_vlc_locations = [r'"/Applications/VLC.app/Contents/MacOS/VLC"']
        command = "{} udp://@:8554 > /dev/null 2>&1 &"
    elif "win" in sys.platform.lower():
        potential_vlc_locations = [
            r'"/c/Program Files/VideoLAN/VLC/vlc.exe"',
            r'"/c/Program Files (x86)/VideoLAN/VLC/vlc.exe"',
            r'"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"',
            r'"C:\Program Files\VideoLAN\VLC\vlc.exe"',
        ]
        command = "{} udp://@:8554 &"

    potential_vlc_locations = potential_vlc_locations if location is None else [location]
    for vlc in potential_vlc_locations:
        response = cmd(command.format(vlc)).lower()

        if (
            " not " not in response
            and " no " not in response
            and " cannot " not in response
            and " unexpected " not in response
        ):
            util_logger.info("VLC launched")
            return

    util_logger.error("Failed to find VLC")


def scrub(obj: Any, bad_key: str) -> None:
    """Recursively scrub a dict or list to remove a given key in place.

    Args:
        obj (Any): dict or list to operate on. If neither, it will return immediately.
        bad_key (str): key to remove
    """
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            if key == bad_key:
                del obj[key]
            else:
                scrub(obj[key], bad_key)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] == bad_key:
                del obj[i]
            else:
                scrub(obj[i], bad_key)
    else:
        # neither a dict nor a list, do nothing
        pass


def cmd(command: str) -> str:
    """Send a command to the shell and return the result.

    Args:
        command (str): command to send

    Returns:
        str: response returned from shell
    """
    util_logger.debug(f"Send cmd --> {command}")
    # Note: Ignoring unicode characters in SSIDs to prevent intermittent UnicodeDecodeErrors from occurring
    # while trying to connect to SSID when *any* AP is nearby that has unicode characters in the name
    response = (
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # type: ignore
        .stdout.read()
        .decode(errors="ignore")
    )
    util_logger.debug(f"Receive response --> {response}")

    return response


class Singleton:
    """To be subclassed to create a singleton class."""

    _instances: Dict[Type["Singleton"], Type["Singleton"]] = {}

    # pylint: disable=missing-return-doc, missing-return-type-doc
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        """Check for existing instance."""
        if cls not in cls._instances:
            # https://github.com/python/mypy/issues/6061
            cls._instances[cls] = object.__new__(cls, *args, **kwargs)  # type: ignore
        return cls._instances[cls]


class SnapshotQueue(queue.Queue):
    """A subclass of the default queue module to safely take a snapshot of the queue

    This is so we can access the elements (in a thread safe manner) without dequeuing them.
    """

    def snapshot(self) -> List[Any]:
        """Acquire the mutex, then return the queue's elements as a list.

        Returns:
            List[Any]: List of queue elements
        """
        with self.mutex:
            return list(self.queue)
