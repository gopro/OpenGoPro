# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations
import enum
import logging
import traceback
import threading
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Final, Callable, TypeVar, Generic, Optional

import wrapt
import requests

from open_gopro.interface import JsonParser
import open_gopro.exceptions as GpException
from open_gopro.api import (
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    WiredApi,
    WirelessApi,
)
from open_gopro.responses import GoProResp

logger = logging.getLogger(__name__)

WRITE_TIMEOUT: Final = 5
GET_TIMEOUT: Final = 5
HTTP_GET_RETRIES: Final = 5

# TODO Replace this with Self once mypy implements it
GoPro = TypeVar("GoPro", bound="GoProBase")
ApiType = TypeVar("ApiType", WiredApi, WirelessApi)
MessageMethodType = Callable[[Any, bool], GoProResp]


class GoProMessageInterface(enum.Enum):
    """Enum to identify wireless interface"""

    HTTP = enum.auto()
    BLE = enum.auto()


@wrapt.decorator
def catch_thread_exception(
    wrapped: Callable, instance: GoProBase, args: Any, kwargs: Any
) -> Optional[Callable]:
    """Catch any exceptions from this method and pass them to the exception handler identifier by thread name

    Args:
        wrapped (Callable): method that this is wrapping
        instance (GoProBase): instance owner of method
        args (Any): positional args
        kwargs (Any): keyword args

    Returns:
        Optional[Callable]: forwarded return of wrapped method or None if exception occurs
    """
    try:
        return wrapped(*args, **kwargs)
    except Exception as e:  # pylint: disable=broad-except
        instance._handle_exception(threading.current_thread().name, {"exception": e})
        return None


def ensure_opened(interface: tuple[GoProMessageInterface]) -> Callable:
    """Raise exception if relevant interface is not currently opened

    Args:
        interface (Interface): wireless interface to verify

    Returns:
        Callable: Direct pass-through of callable after verification
    """

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: GoProBase, args: Any, kwargs: Any) -> Callable:
        if GoProMessageInterface.BLE in interface and not instance.is_ble_connected:
            raise GpException.GoProNotOpened("BLE not connected")
        if GoProMessageInterface.HTTP in interface and not instance.is_http_connected:
            raise GpException.GoProNotOpened("HTTP interface not connected")
        return wrapped(*args, **kwargs)

    return wrapper


class GoProBase(ABC, Generic[ApiType]):
    """The base class for communicating with all GoPro Clients"""

    def __init__(self, **kwargs: Any) -> None:
        self._should_maintain_state = kwargs.get("maintain_state", True)
        self._exception_cb = kwargs.get("exception_cb", None)
        self._internal_state = GoProBase._InternalState.ENCODING | GoProBase._InternalState.SYSTEM_BUSY

    def _handle_exception(self, source: Any, context: dict[str, Any]) -> None:
        """Gather exceptions from module threads and send through callback if registered.

        Note that this function signature matches asyncio's exception callback requirement.

        Args:
            source (Any): Where did the exception come from?
            context (Dict): Access exception via context["exception"]
        """
        # context["message"] will always be there; but context["exception"] may not
        if exception := context.get("exception", False):
            logger.error(f"Received exception {exception} from {source}")
            logger.error(traceback.format_exc())
            if self._exception_cb:
                self._exception_cb(exception)
        else:
            logger.error(f"Caught unknown message: {context['message']} from {source}")

    class _InternalState(enum.IntFlag):
        """State used to manage whether the GoPro instance is ready or not."""

        READY = 0
        ENCODING = 1 << 0
        SYSTEM_BUSY = 1 << 1

    def __enter__(self: GoPro) -> GoPro:
        self.open()
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    @abstractmethod
    def open(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect to the GoPro Client and prepare it for communication

        Args:
            timeout (int): time before considering connection a failure. Defaults to 10.
            retries (int): number of connection retries. Defaults to 5.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Gracefully close the GoPro Client connection"""
        raise NotImplementedError

    @property
    def is_encoding(self) -> bool:
        """Is the camera currently encoding?

        Raises:
            InvalidConfiguration: if maintain_state is False, there is no way to know the GoPro's state

        Returns:
            bool: True if yes, False if no
        """
        if not self._should_maintain_state:
            raise GpException.InvalidConfiguration("Not maintaining BLE state so encoding is not applicable")
        return bool(self._internal_state & GoProBase._InternalState.ENCODING)

    @property
    def is_busy(self) -> bool:
        """Is the camera currently performing a task that prevents it from accepting commands?

        Raises:
            InvalidConfiguration: if maintain_state is False, there is no way to know the GoPro's state

        Returns:
            bool: True if yes, False if no
        """
        if not self._should_maintain_state:
            raise GpException.InvalidConfiguration("Not maintaining BLE state so busy is not applicable")
        return bool(self._internal_state & GoProBase._InternalState.SYSTEM_BUSY)

    @property
    @abstractmethod
    def _api(self) -> ApiType:
        """Unique identifier for the connected GoPro Client

        Returns:
            str: identifier
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def identifier(self) -> str:
        """Unique identifier for the connected GoPro Client

        Returns:
            str: identifier
        """
        raise NotImplementedError

    @property
    def version(self) -> str:
        """The API version that the connected camera supports

        Only 2.0 is currently supported

        Returns:
            str: supported version
        """
        return self._api.version

    @property
    @abstractmethod
    def _base_url(self) -> str:
        """Build the base endpoint for USB commands

        Returns:
            str: base endpoint with URL from serial number
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def http_command(self) -> HttpCommands:
        """Used to access the Wifi commands

        Returns:
            HttpCommands: the commands
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def http_setting(self) -> HttpSettings:
        """Used to access the Wifi settings

        Returns:
            HttpSettings: the settings
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def ble_command(self) -> BleCommands:
        """Used to call the BLE commands

        Returns:
            BleCommands: the commands
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def ble_setting(self) -> BleSettings:
        """Used to access the BLE settings

        Returns:
            BleSettings: the settings
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def ble_status(self) -> BleStatuses:
        """Used to access the BLE statuses

        Returns:
            BleStatuses: the statuses
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Is this client ready for communication?

        Returns:
            bool: True if yes, False if no
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_ble_connected(self) -> bool:
        """Are we connected via BLE to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_http_connected(self) -> bool:
        """Are we connected via HTTP to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        raise NotImplementedError

    @staticmethod
    def _ensure_opened(interface: tuple[GoProMessageInterface]) -> Callable:
        """Raise exception if relevant interface is not currently opened

        Args:
            interface (Interface): wireless interface to verify

        Returns:
            Callable: Direct pass-through of callable after verification
        """
        return ensure_opened(interface)

    @staticmethod
    def _catch_thread_exception(*args: Any, **kwargs: Any) -> Optional[Callable]:
        """Catch any exceptions from this method and pass them to the exception handler identifier by thread name

        Args:
            args (Any): positional args
            kwargs (Any): keyword args

        Returns:
            Optional[Callable]: forwarded return of wrapped method or None if exception occurs
        """
        return catch_thread_exception(*args, **kwargs)

    @ensure_opened((GoProMessageInterface.HTTP,))
    def _get(self, url: str, parser: Optional[JsonParser] = None) -> GoProResp:
        """Send an HTTP GET request to an Open GoPro endpoint.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.wifi_command and self.wifi_status)

        Args:
            url (str): endpoint URL
            parser (Optional[JsonParser]): Optional parser to further parse received JSON dict. Defaults to
                None.

        Raises:
            ResponseTimeout: Response was not received in GET_TIMEOUT seconds

        Returns:
            GoProResp: response
        """
        url = self._base_url + url
        logger.debug(f"Sending:  {url}")

        response: Optional[GoProResp] = None
        for _ in range(HTTP_GET_RETRIES):
            try:
                request = requests.get(url, timeout=GET_TIMEOUT)
                request.raise_for_status()
                response = GoProResp._from_http_response(parser, request)
                break
            except requests.exceptions.HTTPError as e:
                # The camera responded with an error. Break since we successfully sent the command and attempt
                # to continue
                logger.warning(e)
                response = GoProResp._from_http_response(parser, e.response)
                break
            except requests.exceptions.ConnectionError as e:
                logger.warning(repr(e))
            except Exception as e:  # pylint: disable=broad-except
                logger.critical(f"Unexpected error: {repr(e)}")
            else:
                pass
            logger.warning("Retrying to send the command...")
        else:
            raise GpException.ResponseTimeout(HTTP_GET_RETRIES)

        assert response is not None
        return response

    @ensure_opened((GoProMessageInterface.HTTP,))
    def _stream_to_file(self, url: str, file: Path) -> GoProResp:
        """Send an HTTP GET request to an Open GoPro endpoint to download a binary file.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.wifi_command and self.wifi_status)

        Args:
            url (str): endpoint URL
            file (Path): location where file should be downloaded to

        Returns:
            GoProResp: location of file that was written
        """
        assert self.is_http_connected

        url = self._base_url + url
        logger.debug(f"Sending: {url}")
        with requests.get(url, stream=True, timeout=GET_TIMEOUT) as request:
            request.raise_for_status()
            with open(file, "wb") as f:
                logger.debug(f"receiving stream to {file}...")
                for chunk in request.iter_content(chunk_size=8192):
                    f.write(chunk)

        return GoProResp._from_stream_response(request)
