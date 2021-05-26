# util.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Miscellaneous utilities for the GoPro package."""

import sys
import queue
import logging
import subprocess
from pathlib import Path
from typing import Dict, Type, Any, List, Optional, Union

logger = logging.getLogger(__name__)


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
            logger.info("VLC launched")
            return

    logger.error("Failed to find VLC")


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
    logger.debug(f"Send cmd --> {command}")
    # Note: Ignoring unicode characters in SSIDs to prevent intermittent UnicodeDecodeErrors from occurring
    # while trying to connect to SSID when *any* AP is nearby that has unicode characters in the name
    response = (
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # type: ignore
        .stdout.read()
        .decode(errors="ignore")
    )
    logger.debug(f"Receive response --> {response}")

    return response


class Singleton:
    """To be subclassed to create a singleton class."""

    _instances: Dict[Type["Singleton"], Type["Singleton"]] = {}

    # pylint: disable=missing-return-doc, missing-return-type-doc
    def __new__(cls, *args, **kwargs):  # type: ignore
        """Check for existing instance."""
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls, *args, **kwargs)
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
