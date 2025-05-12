# util.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:50 PM

"""Miscellaneous utilities for the GoPro package."""

from __future__ import annotations

import argparse
import asyncio
import enum
import logging
import subprocess
import sys
from dataclasses import is_dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar

import pytz
from construct import Container
from pydantic import BaseModel
from typing_extensions import TypeIs
from tzlocal import get_localzone

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


util_logger = logging.getLogger(__name__)


class Singleton:
    """To be subclassed to create a singleton class."""

    _instances: dict[type[Singleton], Singleton] = {}

    def __new__(cls, *_: Any) -> Any:  # noqa https://github.com/PyCQA/pydocstyle/issues/515
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls)
        return cls._instances[cls]


def map_keys(obj: Any, key: str, func: Callable) -> None:
    """Map all matching keys (deeply searched) using the input function

    Args:
        obj (Any): object to modify in place
        key (str): key to search for to modify
        func (Callable): mapping function
    """
    if isinstance(obj, dict):
        for k in obj.keys():
            if k == key:
                obj[k] = func(obj[k])
            else:
                map_keys(obj[k], key, func)
    elif isinstance(obj, list):
        for i in obj:
            map_keys(i, key, func)
    else:
        # neither a dict nor a list, do nothing
        pass


def scrub(obj: Any, bad_keys: list | None = None, bad_values: list | None = None) -> None:
    """Recursively scrub a collection (dict / list) of bad keys and / or bad values

    Args:
        obj (Any): collection to scrub
        bad_keys (list | None): Keys to remove. Defaults to None.
        bad_values (list | None): Values to remove. Defaults to None.

    Raises:
        ValueError: Missing bad keys / values
    """
    bad_keys = bad_keys or []
    bad_values = bad_values or []
    if not (bad_values or bad_keys):
        raise ValueError("Must pass either / or bad_keys or bad_values")

    def recurse(obj: Any) -> None:
        if isinstance(obj, dict):
            for key, value in {**obj}.items():
                if key in bad_keys or value in bad_values:
                    del obj[key]
                else:
                    recurse(obj[key])
        elif isinstance(obj, list):
            for i, value in enumerate(list(obj)):
                if value in bad_values:
                    del obj[i]
                else:
                    recurse(obj[i])
        else:
            # neither a dict nor a list, do nothing
            pass

    recurse(obj)


def pretty_print(obj: Any, stringify_all: bool = True, should_quote: bool = True) -> str:
    """Recursively iterate through object and turn elements into strings

    Args:
        obj (Any): object to recurse through
        stringify_all (bool): At the end of each recursion, should the element be turned into a string?
            For example, should an int be turned into a str? Defaults to True.
        should_quote (bool): Should each element be surrounded in quotes?. Defaults to True.

    Returns:
        str: pretty-printed string
    """
    output = ""
    nest_level = 0

    def sanitize(e: Any) -> str:
        """Get the value part and replace any underscored with spaces

        Args:
            e (Any): argument to sanitize

        Returns:
            str: sanitized string
        """
        value_part = str(e).lower().split(".")[1]
        value_part = value_part.replace("_", " ").title()
        return value_part

    def stringify(elem: Any) -> Any:
        """Get the string value of an element if it is not a number (int, float, etc.)

        Args:
            elem (Any): element to potentially stringify

        Returns:
            Any: string representation or original object
        """

        def quote(elem: Any) -> Any:
            return f'"{elem}"' if should_quote else elem

        ret: str
        if isinstance(elem, (bytes, bytearray)):
            ret = quote(elem.hex(":"))
        if isinstance(elem, enum.Enum) and isinstance(elem, int):
            ret = quote(str(elem) if not stringify_all else sanitize(elem))
        if isinstance(elem, (bool, int, float)):
            ret = quote(elem) if stringify_all else elem  # type: ignore
        ret = str(elem)
        return quote(ret)

    def recurse(elem: Any) -> None:
        """Recursion function

        Args:
            elem (Any): current element to work on
        """
        nonlocal output
        nonlocal nest_level
        indent_size = 4
        # Convert to dict if possible
        if isinstance(elem, BaseModel):
            elem = dict(elem)
            scrub(elem, bad_values=[None])
        if isinstance(elem, dict):
            # nested dictionary
            nest_level += 1
            output += "{"
            for k, v in elem.items():
                output += f"\n{' ' * (indent_size * nest_level)}"
                # Add key
                recurse(k)
                output += " : "
                # Add value
                if isinstance(v, (dict, list, BaseModel)):
                    recurse(v)
                else:
                    output += stringify(v)
                output += ","

            nest_level -= 1
            output += f"\n{' '* (indent_size * nest_level)}}}"

        elif isinstance(elem, list):
            # nested list
            nest_level += 1
            output += f"[\n{' '* (indent_size * nest_level)}"
            if len(elem):
                for item in elem[:-1]:
                    recurse(item)
                    output += ", "
                recurse(elem[-1])
            nest_level -= 1
            output += f"\n{' '* (indent_size * nest_level)}]"

        else:
            output += stringify(elem)

    recurse(obj)
    return output


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
    response = (
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # type: ignore
        .stdout.read()
        .decode(errors="ignore")
    )
    util_logger.debug(f"Receive response --> {response}")

    return response


T = TypeVar("T")


class SnapshotQueue(asyncio.Queue, Generic[T]):
    """A subclass of the default queue module to safely take a snapshot of the queue

    This is so we can access the elements (in a thread safe manner) without dequeuing them.
    """

    def __init__(self, maxsize: int = 0) -> None:
        self._lock = asyncio.Lock()
        super().__init__(maxsize)

    async def get(self) -> T:
        """Wrapper for passing generic type through to subclass

        Returns:
            T: type of this Snapshot queue
        """
        return await super().get()

    async def peek_front(self) -> T | None:
        """Get the first element without dequeueing it

        Returns:
            T | None: First element of None if the queue is empty
        """
        async with self._lock:
            return None if self.empty() else self._queue[0]  # type: ignore


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
        argparse.Namespace: modified argument parser
    """
    # Common args
    parser.add_argument(
        "--log",
        type=Path,
        help="Location to store detailed log. Defaults to gopro_demo.log",
        default="gopro_demo.log",
    )

    if bluetooth:
        parser.add_argument(
            "--identifier",
            type=str,
            help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. \
                If not used, first discovered GoPro will be connected to",
            default=None,
        )

    if wifi:
        parser.add_argument(
            "--wifi_interface",
            type=str,
            help="System Wifi Interface. If not set, first discovered interface will be used.",
            default=None,
        )
        parser.add_argument(
            "--password",
            action="store_true",
            help="Set to read sudo password from stdin. If not set, you will be prompted for password if needed",
        )

    parser.epilog = "Note that a minimal log is written to stdout. An extremely detailed log is written to the path set by the --log argument."
    args = parser.parse_args()
    if wifi:
        args.password = sys.stdin.readline() if args.password else None

    return args


async def ainput(string: str, printer: Callable | None = None) -> str:
    """Async version of input

    Raises:
        ValueError: Can not access default sys.stdout.write

    Args:
        string (str): prompt string
        printer (Callable | None): Printer used to display prompt. Defaults to None in which case sys.stdout.write
            will attempt to be used.

    Returns:
        str: Input read from console
    """
    if not printer:
        try:
            printer = sys.stdout.write
        except AttributeError as e:
            raise ValueError("No printer was passed and default standard out writer does not exist.") from e
    await asyncio.get_event_loop().run_in_executor(None, lambda s=string: printer(s + " "))  # type: ignore
    return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)


def get_current_dst_aware_time() -> tuple[datetime, int, bool]:
    """Get the current time, utc offset in minutes, and daylight savings time

    Returns:
        tuple[datetime, int, bool]: [time, utc_offset in minutes, is_dst?]
    """
    tz = pytz.timezone(get_localzone().key)  # type: ignore
    now = tz.localize(datetime.now(), is_dst=None)
    try:
        is_dst = now.tzinfo._dst.seconds != 0  # type: ignore
        offset = (now.utcoffset().total_seconds() - now.tzinfo._dst.seconds) / 60  # type: ignore
    except AttributeError:
        is_dst = False
        offset = now.utcoffset().total_seconds() / 60  # type: ignore
    if is_dst:
        offset += 60
    return (now, int(offset), is_dst)


def deeply_update_dict(d: dict, u: dict) -> dict:
    """Recursively update a dict

    Args:
        d (dict): original dict
        u (dict): dict to apply updates from

    Returns:
        dict: updated original dict
    """
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deeply_update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def to_dict(container: Container) -> dict:
    """Convert a parsed construct container to a dict, removing any internal Construct fields

    This is needed because annoyingly all construct's contain an "_io" field.
    See https://github.com/construct/construct/issues/1055

    Args:
        container (Container): container to convert

    Returns:
        dict: converted dict with any construct internal properties removed
    """
    d = dict(container)
    d.pop("_io", None)
    return d


def is_dataclass_instance(obj: Any) -> TypeIs[DataclassInstance | type[DataclassInstance]] | bool:
    """Check if a given object is a dataclass instance

    Args:
        obj (Any): object to analyze

    Returns:
        TypeIs[DataclassInstance | type[DataclassInstance]] | bool: TypeIs from analysis
    """
    return is_dataclass(obj) and not isinstance(obj, type)
