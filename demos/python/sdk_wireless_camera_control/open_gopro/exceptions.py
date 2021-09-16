# exceptions.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Exceptions that pertain to Gopro-level functionality."""


class GoProError(Exception):
    """Base class for other GoPro-level exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(f"GoPro Error: {message}")


class ResponseParseError(GoProError):
    """The scan failed without finding a device."""

    def __init__(self, identifier: str, data: bytearray) -> None:
        super().__init__(f"Failed to parse {data.hex(':')} from {identifier}")


class InvalidOpenGoProVersion(GoProError):
    """Attempt to access an invalid Open GoPro API version"""

    def __init__(self, version: str) -> None:
        super().__init__(f"{version} is not a valid Open GoPro API version.")


class InvalidConfiguration(GoProError):
    """Something was attempted that is not possible for the current configuration."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Invalid configuration: {message}")


class GoProNotInitialized(GoProError):
    """A command was attempted without waiting for the GoPro instance to initialize."""

    def __init__(self) -> None:
        super().__init__("GoPro has not been initialized yet")


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
        super().__init__(
            f"{connection} connection failed to establish after {retries} retries with timeout {timeout}"
        )


class ConnectionTerminated(GoProError):
    """A connection that was previously established has termianted."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Connection terminated: {message}")


class ResponseTimeout(GoProError):
    """A response has timed out."""

    def __init__(self, timeout: float) -> None:
        super().__init__(f"Response timeout occurred of {timeout} seconds")
