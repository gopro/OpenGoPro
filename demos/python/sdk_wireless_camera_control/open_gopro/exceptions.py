# exceptions.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Exceptions that pertain to Gopro-level functionality."""

from typing import Callable


class GoProError(Exception):
    """Base class for other GoPro-level exceptions."""


class ResponseParseError(GoProError):
    """Error when parsing received data."""

    def __init__(self, identifier: str, data: bytearray, msg: str = "") -> None:
        super().__init__(f"{msg}: Failed to parse {data.hex(':')} from {identifier}")


class InvalidOpenGoProVersion(GoProError):
    """Attempt to access an invalid Open GoPro API version"""

    def __init__(self, version: str) -> None:
        super().__init__(f"{version} is not a valid Open GoPro API version.")


class InvalidConfiguration(GoProError):
    """Something was attempted that is not possible for the current configuration."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid configuration: {message}")


class GoProNotOpened(GoProError):
    """A command was attempted without waiting for the GoPro instance to open."""

    def __init__(self, message: str) -> None:
        super().__init__(f"GoPro is not correctly open: {message}")


class FailedToFindDevice(GoProError):
    """The scan failed without finding a device."""

    def __init__(self) -> None:
        super().__init__("A scan timed out without finding a device")


class ConnectFailed(GoProError):
    """A BLE connection failed to establish

    Args:
        connection (str): type of connection that failed
        retries (int): how many retries were attempted
        timeout (int): the timeout used for each attempt
    """

    def __init__(self, connection: str, timeout: float, retries: int):
        super().__init__(f"{connection} connection failed to establish after {retries} retries with timeout {timeout}")


class ConnectionTerminated(GoProError):
    """A connection that was previously established has terminated."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Connection terminated: {message}")


class ResponseTimeout(GoProError):
    """A response has timed out."""

    def __init__(self, timeout: float) -> None:
        super().__init__(f"Response timeout occurred of {timeout} seconds")


class InterfaceConfigFailure(GoProError):
    """An error has occurred while setting up the communication interface"""


ExceptionHandler = Callable[[Exception], None]
"""Exception handler callback type"""
