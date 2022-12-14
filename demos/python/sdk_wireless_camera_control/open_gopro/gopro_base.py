# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations
import enum
import logging
import traceback
import threading
from abc import ABC, abstractmethod
from typing import Any, Final, Callable, TypeVar, Generic

import wrapt

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

logger = logging.getLogger(__name__)

WRITE_TIMEOUT: Final = 5
GET_TIMEOUT: Final = 5
HTTP_GET_RETRIES: Final = 5

# TODO Replace this with Self once mypy implements it
GoPro = TypeVar("GoPro", bound="GoProBase")

ApiType = TypeVar("ApiType", WiredApi, WirelessApi)


@wrapt.decorator
def catch_thread_exception(wrapped: Callable, instance: GoProBase, args: Any, kwargs: Any) -> Any:
    try:
        wrapped(*args, **kwargs)
    except Exception as e:  # pylint: disable=broad-except
        instance._handle_exception(threading.current_thread().name, {"exception": e})


class GoProBase(ABC, Generic[ApiType]):
    """The base class for communicating with all GoPro Clients"""

    def __init__(self, **kwargs) -> None:
        self._should_maintain_state = kwargs.get("maintain_state", True)
        self._exception_cb = kwargs.get("exception_cb", None)

        # Busy / encoding management
        self._ready = threading.Lock()
        self._state_condition = threading.Condition()
        self._encoding_started = threading.Event()
        self._encoding_started.clear()

        # If we are to perform BLE housekeeping
        if self._should_maintain_state:
            # Set up thread to block until camera is ready to receive commands
            self._internal_state = GoProBase._InternalState.ENCODING | GoProBase._InternalState.SYSTEM_BUSY
            self._state_thread = threading.Thread(target=self._maintain_state, name="state", daemon=True)
            self._state_thread.start()

    @catch_thread_exception
    def _maintain_state(self) -> None:
        """Thread to keep track of ready / encoding and acquire / release ready lock."""
        logger.trace("Initial acquiring of lock")  # type: ignore
        self._ready.acquire()
        have_lock = True
        while True:
            with self._state_condition:
                self._state_condition.wait()
                if have_lock and not (self.is_busy or self.is_encoding):
                    self._ready.release()
                    have_lock = False
                    logger.trace("Control released lock")  # type: ignore
                elif not have_lock and (self.is_busy or self.is_encoding):
                    logger.trace("Control acquiring lock")  # type: ignore
                    self._ready.acquire()
                    logger.trace("Control has lock")  # type: ignore
                    have_lock = True
                    if self.is_encoding:
                        logger.trace("Control setting encoded started")  # type: ignore
                        self._encoding_started.set()

        # TODO how to stop this?
        logger.debug("Maintain state thread exiting...")

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

    class _Interface(enum.Enum):
        """Enum to identify wireless interface"""

        HTTP = enum.auto()
        BLE = enum.auto()

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
        raise NotImplementedError

    @property
    @abstractmethod
    def is_http_connected(self) -> bool:
        raise NotImplementedError

    @staticmethod
    def ensure_opened(interface: tuple[GoProBase._Interface]) -> Callable:
        """Raise exception if relevant interface is not currently opened

        Args:
            interface (Interface): wireless interface to verify

        Returns:
            Callable: Direct pass-through of callable after verification
        """

        @wrapt.decorator
        def wrapper(wrapped: Callable, instance: GoProBase, args: Any, kwargs: Any) -> Callable:
            if GoProBase._Interface.BLE in interface and not instance.is_ble_connected:
                raise GpException.GoProNotOpened("BLE not connected")
            if GoProBase._Interface.HTTP in interface and not instance.is_http_connected:
                raise GpException.GoProNotOpened("Wifi not connected")
            return wrapped(*args, **kwargs)

        return wrapper

    @staticmethod
    @wrapt.decorator
    def acquire_ready_lock(wrapped: Callable, instance: GoProBase, args: Any, kwargs: Any) -> Any:
        """Call method after acquiring ready lock.

        Release lock when done

        Args:
            wrapped (Callable): method to call
            instance (GoProBase): instance that owns the method
            args (Any): positional arguments
            kwargs (Any): keyword arguments

        Returns:
            Any: result of method
        """
        if instance._should_maintain_state:
            logger.trace(f"{wrapped.__name__} acquiring lock")  # type: ignore
            with instance._ready:
                logger.trace(f"{wrapped.__name__} has the lock")  # type: ignore
                ret = wrapped(*args, **kwargs)
        else:
            ret = wrapped(*args, **kwargs)
        if instance._should_maintain_state:
            logger.trace(f"{wrapped.__name__} released the lock")  # type: ignore
        return ret

    @staticmethod
    def catch_thread_exception(*args, **kwargs) -> Any:
        return catch_thread_exception(*args, **kwargs)
