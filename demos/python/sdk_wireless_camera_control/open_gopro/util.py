# util.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:50 PM

"""Miscellaneous utilities for the GoPro package."""

from __future__ import annotations
import sys
import enum
import json
import queue
import logging
import argparse
import subprocess
from pathlib import Path
import http.client as http_client
from typing import Dict, Type, Any, List, Optional, Union, Final, Tuple

from rich.logging import RichHandler
from rich import traceback

util_logger = logging.getLogger(__name__)

# From https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
def addLoggingLevel(levelName: str, levelNum: int) -> None:
    """Comprehensively adds a new logging level to the `logging` module and the currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example:
    --------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    Args:
        levelName (str): name of level (i.e. TRACE)
        levelNum (int): integer level of new logging level
    """
    methodName = levelName.lower()

    def logForLevel(self: Any, message: str, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message: str, *args: Any, **kwargs: Any) -> None:
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def setup_logging(
    logger: Any,
    output: Optional[Path] = None,
    modules: Optional[Dict[str, int]] = None,
    handlers: Optional[Tuple[logging.Handler]] = None,
) -> logging.Logger:
    """Configure open gopro modules for logging

    The application's logger is passed in, modified, and then returned

    Args:
        logger (Any): input logger that will be modified and then returned
        output (Path, Optional): Path of log file for file stream handler. If not set, will not log to file.
        modules (Dict[str, int], Optional): Optional override of modules / levels. Will be merged into default
            modules.
        handlers (Tuple[logging.Handler], Optional): additional logging handlers to append to standard handlers

    Returns:
        Any: updated logger that the application can use for logging
    """
    default_modules = {
        "open_gopro.gopro": logging.DEBUG,
        "open_gopro.api.builders": logging.DEBUG,
        "open_gopro.api.wifi_commands": logging.DEBUG,
        "open_gopro.api.ble_commands": logging.DEBUG,
        "open_gopro.communication_client": logging.DEBUG,
        "open_gopro.ble.adapters.bleak_wrapper": logging.INFO,
        "open_gopro.ble.client": logging.DEBUG,
        "open_gopro.wifi.adapters.wireless": logging.DEBUG,
        "open_gopro.responses": logging.DEBUG,
        "open_gopro.util": logging.DEBUG,
        "bleak": logging.WARNING,
        "urllib3": logging.WARNING,
        "http.client": logging.WARNING,
    }

    logging_modules = {**default_modules, **modules} if modules else default_modules

    # monkey-patch a `print` global into the http.client module; all calls to
    # print() in that module will then use our logger's debug method
    http_client.HTTPConnection.debuglevel = 1
    http_client.print = lambda *args: logging.getLogger("http.client").debug(" ".join(args))  # type: ignore

    addLoggingLevel("TRACE", logging.DEBUG - 5)

    if output:
        # Logging to file with millisecond timing
        fh = logging.FileHandler(output, mode="w")
        file_formatter = logging.Formatter(
            fmt="%(threadName)13s:%(asctime)s.%(msecs)03d %(filename)-40s %(lineno)4s %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S",
        )
        fh.setFormatter(file_formatter)
        fh.setLevel(logging.TRACE)  # type: ignore # pylint: disable=no-member
        logger.addHandler(fh)
    else:
        fh = None

    # Use Rich for colorful console logging
    sh = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
    stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
    sh.setFormatter(stream_formatter)
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)
    logger.setLevel(logging.TRACE)  # type: ignore # pylint: disable=no-member

    # Add any additioinal logger
    if handlers:
        for handler in handlers:
            logger.addHandler(handler)

    # Enable / disable logging in modules
    for module, level in logging_modules.items():
        l = logging.getLogger(module)
        l.setLevel(level)
        if fh:
            l.addHandler(fh)
        l.addHandler(sh)
        if handlers:
            for handler in handlers:
                l.addHandler(handler)

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


ARROW_HEAD_COUNT: Final = 8
ARROW_TAIL_COUNT: Final = 14


def build_log_tx_str(stringable: Any) -> str:
    """Build a string with Tx arrows

    Args:
        stringable (Any): stringable object to surround with arrows

    Returns:
        str: string surrounded by Tx arrows
    """
    arrow = f"{'<'*ARROW_HEAD_COUNT}{'-'*ARROW_TAIL_COUNT}"
    return f"\n\n{arrow}\n\t{stringable}\n{arrow}\n"


def build_log_rx_str(stringable: Any, asynchronous: bool = False) -> str:
    """Build a string with Rx arrows

    Args:
        stringable (Any): stringable object to surround with arrows
        asynchronous (bool): Should the arrows contain ASYNC?. Defaults to False.

    Returns:
        str: string surrounded by Rx arrows
    """
    s = str(stringable).strip("{").strip("}").strip("\n")
    assert ARROW_TAIL_COUNT > 5
    if asynchronous:
        arrow = f"{'-'*(ARROW_TAIL_COUNT//2-3)}ASYNC{'-'*(ARROW_TAIL_COUNT//2-2)}{'>'*ARROW_HEAD_COUNT}"
    else:
        arrow = f"{'-'*ARROW_TAIL_COUNT}{'>'*ARROW_HEAD_COUNT}"
    return f"\n\n{arrow}\n{s}\n{arrow}\n"


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


def pretty_print(obj: Any) -> str:
    """Recursively iterate through object and turn elements into strings as desired for eventual json dumping

    Args:
        obj (Any): object to recurse through

    Returns:
        str: pretty-printed string
    """

    def stringify(elem: Any) -> Union[str, int, float]:
        """Get the string value of an element if it is not a number (int, float, etc.)

        Special case for IntEnum since json refuses to treat these as strings.

        Args:
            elem (Any): element to potentially stringify

        Returns:
            str: string representation
        """
        if isinstance(elem, (bytes, bytearray)):
            return elem.hex(":")
        if isinstance(elem, enum.Enum) and isinstance(elem, int):
            return str(elem)
        if not isinstance(elem, (int, float)):
            return str(elem)
        return elem

    def recurse(elem: Any) -> Any:
        """Recursion function

        Args:
            elem (Any): current element to work on

        Returns:
            Any: element after recursion is done
        """
        if isinstance(elem, dict):
            # nested dictionary
            new_dic = {}
            for k, v in elem.items():
                if isinstance(v, (dict, list)):
                    new_dic[recurse(k)] = recurse(v)
                else:
                    new_dic[recurse(k)] = stringify(v)

            return new_dic

        if isinstance(elem, list):
            # nested list
            return [recurse(t) for t in elem]

        return stringify(elem)

    return json.dumps(recurse(obj), indent=4)


def cmd(command: str) -> str:
    """Send a command to the shell and return the result.

    Args:
        command (str): command to send

    Returns:
        str: response returned from shell
    """
    # We don't want password showing in the log
    if "sudo" in command:
        logged_command = command[: command.find('"') + 1] + "********" + command[command.find(" | sudo") - 1 :]
    else:
        logged_command = command
    util_logger.debug(f"Send cmd --> {logged_command}")
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

    _instances: Dict[Type[Singleton], Singleton] = {}

    def __new__(cls, *_: Any) -> Any:  # noqa https://github.com/PyCQA/pydocstyle/issues/515
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls)
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


def add_cli_args_and_parse(
    parser: argparse.ArgumentParser,
    bluetooth: bool = True,
    wifi: bool = True,
) -> argparse.Namespace:
    """Append common argparse arguments to an argument parser

    WARNING!! This will also parse the arguments (i.e. call parser.parse_args) so ensure to add any additional
    arguments to the parser before passing it to this function.

    Args:
        parser (argparse.ArgumentParser): input parser to modify
        bluetooth (bool): Add bluetooth args?. Defaults to True.
        wifi (bool): Add WiFi args?. Defaults to True.

    Returns:
        argparse.ArgumentParser: modified argument parser
    """
    # Common args
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        help="Location to store detailed log",
        default="gopro_demo.log",
    )

    if bluetooth:
        parser.add_argument(
            "-i",
            "--identifier",
            type=str,
            help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. \
                If not used, first discovered GoPro will be connected to",
            default=None,
        )

    if wifi:
        parser.add_argument(
            "-w",
            "--wifi_interface",
            type=str,
            help="System Wifi Interface. If not set, first discovered interface will be used.",
            default=None,
        )
        parser.add_argument(
            "-p",
            "--password",
            action="store_true",
            help="Set to read sudo password from stdin. If not set, you will be prompted for password if needed",
        )

    args = parser.parse_args()
    if wifi:
        args.password = sys.stdin.readline() if args.password else None

    return args
