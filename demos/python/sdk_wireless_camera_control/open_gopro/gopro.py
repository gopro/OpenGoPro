# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations
import time
import enum
import queue
import logging
import traceback
import threading
from queue import Queue
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Final, Optional, Callable, Pattern, TypeVar

import wrapt
import requests

import open_gopro.exceptions as GpException
from open_gopro.exceptions import ExceptionHandler
from open_gopro.ble import BleUUID
from open_gopro.ble.adapters import BleakWrapperController
from open_gopro.wifi.adapters import Wireless
from open_gopro.util import SnapshotQueue, Logger
from open_gopro.responses import GoProResp, ResponseType
from open_gopro.constants import CmdId, GoProUUIDs, StatusId, QueryCmdId, ProducerType
from open_gopro.api import (
    WirelessApi,
    WiredApi,
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    Params,
)
from open_gopro.interface import GoProWirelessInterface, GoProWiredInterface, JsonParser

logger = logging.getLogger(__name__)

KEEP_ALIVE_INTERVAL: Final = 28
WRITE_TIMEOUT: Final = 5
GET_TIMEOUT: Final = 5
HTTP_GET_RETRIES: Final = 5

# TODO Replace this with Self once mypy implements it
GoPro = TypeVar("GoPro", bound="GoProBase")


class Interface(enum.Enum):
    """Enum to identify wireless interface"""

    WIFI = enum.auto()
    BLE = enum.auto()


def ensure_opened(interface: Interface) -> Callable:
    """Raise exception if relevant interface is not currently opened

    Args:
        interface (Interface): wireless interface to verify

    Returns:
        Callable: Direct pass-through of callable after verification
    """

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: WirelessGoPro, args: Any, kwargs: Any) -> Callable:
        if interface is Interface.BLE and not instance.is_ble_connected:
            raise GpException.GoProNotOpened("BLE not connected")
        if interface is Interface.WIFI and not (
            hasattr(instance, "is_wifi_connected") and instance.is_wifi_connected
        ):
            raise GpException.GoProNotOpened("Wifi not connected")
        return wrapped(*args, **kwargs)

    return wrapper


@wrapt.decorator
def acquire_ready_lock(wrapped: Callable, instance: WirelessGoPro, args: Any, kwargs: Any) -> Any:
    """Call method after acquiring ready lock.

    Release lock when done

    Args:
        wrapped (Callable): method to call
        instance (WirelessGoPro): instance that owns the method
        args (Any): positional arguments
        kwargs (Any): keyword arguments

    Returns:
        Any: result of method
    """
    if instance._maintain_ble:
        logger.trace(f"{wrapped.__name__} acquiring lock")  # type: ignore
        with instance._ready:
            logger.trace(f"{wrapped.__name__} has the lock")  # type: ignore
            ret = wrapped(*args, **kwargs)
    else:
        ret = wrapped(*args, **kwargs)
    if instance._maintain_ble:
        logger.trace(f"{wrapped.__name__} released the lock")  # type: ignore
    return ret


class GoProBase(ABC):
    """The base class for communicating with all GoPro Clients"""

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
    @abstractmethod
    def identifier(self) -> str:
        """Unique identifier for the connected GoPro Client

        Returns:
            str: identifier
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def version(self) -> str:
        """The Open GoPro API version of the GoPro Client

        Only Version 2.0 is currently supported.

        Returns:
            str: string version
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


class WiredGoPro(GoProBase, GoProWiredInterface):
    """The top-level USB interface to a Wired GoPro device.

    Args:
        serial (str): (at least) last 3 digits of GoPro Serial number
    """

    _BASE_IP: Final[str] = "172.2{}.1{}{}.51"
    _BASE_ENDPOINT: Final[str] = "http://{ip}:8080/"

    def __init__(self, serial: str) -> None:
        GoProWiredInterface.__init__(self)
        self._serial = serial
        # We currently only support version 2.0
        self._api = WiredApi(self)
        self._open = False

    def open(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect to the Wired GoPro Client and prepare it for communication

        Args:
            timeout (int): time before considering connection a failure. Defaults to 10.
            retries (int): number of connection retries. Defaults to 5.

        Raises:
            InvalidOpenGoProVersion: the GoPro camera does not support the correct Open GoPro API version
        """
        # TODO use timeout / retries for automatic IP discovery via mDNS
        # Find and configure API version
        version = self.http_command.get_open_gopro_api_version().flatten
        version_str = f"{version.major}.{version.minor}"
        if version_str != "2.0":
            raise GpException.InvalidOpenGoProVersion(version)
        logger.info(f"Using Open GoPro API version {version_str}")
        self._open = True

    def close(self) -> None:
        """Gracefully close the GoPro Client connection"""

    @property
    def identifier(self) -> str:
        """Unique identifier for the connected GoPro Client

        Returns:
            str: identifier
        """
        return self._serial

    @property
    def version(self) -> str:
        """The Open GoPro API version of the GoPro Client

        Only Version 2.0 is currently supported.

        Returns:
            str: string version
        """
        return self._api.version

    @property
    def http_command(self) -> HttpCommands:
        """Used to access the USB commands

        Returns:
            HttpCommands: the commands
        """
        return self._api.http_command

    @property
    def http_setting(self) -> HttpSettings:
        """Used to access the USB settings

        Returns:
            HttpSettings: the settings
        """
        return self._api.http_setting

    @property
    def ble_command(self) -> BleCommands:
        """Used to call the BLE commands

        Raises:
            NotImplementedError: Not valid for WiredGoPro
        """
        raise NotImplementedError

    @property
    def ble_setting(self) -> BleSettings:
        """Used to access the BLE settings

        Raises:
            NotImplementedError: Not valid for WiredGoPro
        """
        raise NotImplementedError

    @property
    def ble_status(self) -> BleStatuses:
        """Used to access the BLE statuses

        Raises:
            NotImplementedError: Not valid for WiredGoPro
        """
        raise NotImplementedError

    @property
    def is_open(self) -> bool:
        """Is this client ready for communication?

        Returns:
            bool: True if yes, False if no
        """
        return self._open

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    @property
    def _base_endpoint(self) -> str:
        """Build the base endpoint for USB commands

        Returns:
            str: base endpoint with URL from serial number
        """
        return WiredGoPro._BASE_ENDPOINT.format(ip=WiredGoPro._BASE_IP.format(*self._serial[-3:]))

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
        url = self._base_endpoint + url
        logger.debug(f"Sending:  {url}")

        response: Optional[GoProResp] = None
        for _ in range(HTTP_GET_RETRIES):
            try:
                request = requests.get(url, timeout=GET_TIMEOUT)
                request.raise_for_status()
                response = GoProResp._from_http_response(parser, request)
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
                break
            logger.warning("Retrying to send the command...")
        else:
            raise GpException.ResponseTimeout(HTTP_GET_RETRIES)

        assert response is not None
        return response

    def _stream_to_file(self, url: str, file: Path) -> None:
        """Send an HTTP GET request to an Open GoPro endpoint to download a binary file.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.wifi_command and self.wifi_status)

        Args:
            url (str): endpoint URL
            file (Path): location where file should be downloaded to

        Raises:
            NotImplementedError: TODO
        """
        raise NotImplementedError("TODO. Not sure if we need this for USB.")


class WirelessGoPro(GoProBase, GoProWirelessInterface):
    """The top-level BLE and Wifi interface to a Wireless GoPro device.

    See the `Open GoPro SDK <https://gopro.github.io/OpenGoPro/python_sdk>`_ for complete documentation.

    This will handle, for BLE:

    - discovering target GoPro device
    - establishing the connection
    - discovering GATT characteristics
    - enabling notifications
    - discovering Open GoPro version
    - transferring data

    This will handle, for Wifi:

    - finding SSID and password
    - establishing Wifi connection
    - transferring data

    It will also do some synchronization, etc:

    - ensuring camera is ready / not encoding before transferring data
    - sending keep alive signal periodically

    If no target arg is passed in, the first discovered BLE GoPro device will be connected to.

    It can be used via context manager:

    >>> from open_gopro import WirelessGoPro
    >>> with WirelessGoPro() as gopro:
    >>>     gopro.ble_command.set_shutter(Params.Toggle.ENABLE)

    Or without:

    >>> from open_gopro import WirelessGoPro
    >>> gopro = WirelessGoPro()
    >>> gopro.open()
    >>> gopro.ble_command.set_shutter(Params.Toggle.ENABLE)
    >>> gopro.close()

    Args:
        target (Pattern, Optional): A regex to search for the target GoPro's name. For example, "GoPro 0456").
            Defaults to None (i.e. connect to first discovered GoPro)
        wifi_interface (str, Optional): Set to specify the wifi interface the local machine will use to connect
            to the GoPro. If None (or not set), first discovered interface will be used.
        sudo_password (str, Optional): User password for sudo. If not passed, you will be prompted if a password
            is needed which should only happen on Nix systems.
        enable_wifi (bool): Optionally do not enable Wifi if set to False. Defaults to True.
        exception_cb (ExceptionHandler, Optional): callback to be notified when exception occurs in a thread
            besides main. This is useful if you anticipate unexpected BLE connection drops.
        kwargs (Dict): additional parameters for internal use / testing

    Raises:
        InterfaceConfigFailure: In order to communicate via Wifi, there must be an available
            Wifi Interface. By default during initialization, the Wifi driver will attempt to automatically
            discover such an interface. If it does not find any, it will raise this exception. Note that
            the interface can also be specified manually with the 'wifi_interface' argument.
    """

    _BASE_URL: Final[str] = "http://10.5.5.9:8080/"  #: Hard-coded Open GoPro base URL

    class _InternalState(enum.IntFlag):
        """State used to manage whether the GoPro instance is ready or not."""

        READY = 0
        ENCODING = 1 << 0
        SYSTEM_BUSY = 1 << 1

    def __init__(
        self,
        target: Optional[Pattern] = None,
        wifi_interface: Optional[str] = None,
        sudo_password: Optional[str] = None,
        enable_wifi: bool = True,
        exception_cb: Optional[ExceptionHandler] = None,
        **kwargs: Any,
    ) -> None:
        # Store initialization information
        self._enable_wifi_during_init = enable_wifi
        self._exception_cb = exception_cb
        self._maintain_ble = kwargs.get("maintain_ble", True)
        ble_adapter = kwargs.get("ble_adapter", BleakWrapperController)
        wifi_adapter = kwargs.get("wifi_adapter", Wireless)

        try:
            # Initialize GoPro Communication Client
            GoProWirelessInterface.__init__(
                self,
                ble_controller=ble_adapter(self._handle_exception),
                wifi_controller=wifi_adapter(wifi_interface, password=sudo_password) if enable_wifi else None,
                disconnected_cb=self._disconnect_handler,
                notification_cb=self._notification_handler,
                target=target,
            )
        except GpException.InterfaceConfigFailure as e:
            logger.error(
                "Could not find a suitable Wifi Interface. If there is an available Wifi interface, try passing it manually with the 'wifi_interface' argument."
            )
            raise e

        # We currently only support version 2.0
        self._api = WirelessApi(self)

        # Current accumulating synchronous responses, indexed by GoProUUIDs. This assumes there can only be one active response per BleUUID
        self._active_resp: dict[BleUUID, GoProResp] = {}
        # Responses that we are waiting for.
        self._sync_resp_wait_q: SnapshotQueue = SnapshotQueue()
        # Synchronous response that has been parsed and are ready for their sender to receive as the response.
        self._sync_resp_ready_q: SnapshotQueue = SnapshotQueue()

        # For outputting asynchronously received information
        self._out_q: Queue[GoProResp] = Queue()
        self._listeners: dict[ProducerType, bool] = {}

        # Set up events
        self._ble_disconnect_event = threading.Event()
        self._ble_disconnect_event.set()
        self._encoding_started = threading.Event()
        self._encoding_started.clear()

        # Set up threads
        self._threads_waiting = 0
        # If we are to perform BLE housekeeping
        if self._maintain_ble:
            self._threads_waiting += 2
            # Set up thread to send keep alive
            self._keep_alive_thread = threading.Thread(
                target=self._periodic_keep_alive, name="keep_alive", daemon=True
            )
            # Set up thread to block until camera is ready to receive commands
            self._ready = threading.Lock()
            self._state_condition = threading.Condition()
            self._internal_state = (
                WirelessGoPro._InternalState.ENCODING | WirelessGoPro._InternalState.SYSTEM_BUSY
            )
            self._state_thread = threading.Thread(target=self._maintain_state, name="state", daemon=True)

    @property
    def identifier(self) -> str:
        """Get a unique identifier for this instance.

        The identifier is the last 4 digits of the camera. That is, the same string that is used to
        scan for the camera for BLE.

        If no target has been provided and a camera is not yet found, this will be None

        Raises:
            GoProNotOpened: Client is not opened yet so no identifier is available

        Returns:
            str: last 4 digits if available, else None
        """
        if self._ble.identifier is None:
            raise GpException.GoProNotOpened("Client does not yet have an identifier.")
        return self._ble.identifier

    @property
    def is_ble_connected(self) -> bool:
        """Are we connected via BLE to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        return self._ble.is_connected

    @property
    def is_wifi_connected(self) -> bool:
        """Are we connected via Wifi to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        return self._wifi.is_connected

    @property
    def is_encoding(self) -> bool:
        """Is the camera currently encoding?

        Raises:
            InvalidConfiguration: if maintain_state is False, there is no way to know the GoPro's state

        Returns:
            bool: True if yes, False if no
        """
        if not self._maintain_ble:
            raise GpException.InvalidConfiguration("Not maintaining BLE state so encoding is not applicable")
        return bool(self._internal_state & WirelessGoPro._InternalState.ENCODING)

    @property
    def is_busy(self) -> bool:
        """Is the camera currently performing a task that prevents it from accepting commands?

        Raises:
            InvalidConfiguration: if maintain_state is False, there is no way to know the GoPro's state

        Returns:
            bool: True if yes, False if no
        """
        if not self._maintain_ble:
            raise GpException.InvalidConfiguration("Not maintaining BLE state so busy is not applicable")
        return bool(self._internal_state & WirelessGoPro._InternalState.SYSTEM_BUSY)

    @property
    def version(self) -> str:
        """The API version that the connected camera supports

        Only 2.0 is currently supported

        Returns:
            str: supported version
        """
        return self._api.version

    @property
    def ble_command(self) -> BleCommands:
        """Used to call the BLE commands

        Returns:
            BleCommands: the commands
        """
        return self._api.ble_command

    @property
    def ble_setting(self) -> BleSettings:
        """Used to access the BLE settings

        Returns:
            BleSettings: the settings
        """
        return self._api.ble_setting

    @property
    def ble_status(self) -> BleStatuses:
        """Used to access the BLE statuses

        Returns:
            BleStatuses: the statuses
        """
        return self._api.ble_status

    @property
    def http_command(self) -> HttpCommands:
        """Used to access the Wifi commands

        Returns:
            HttpCommands: the commands
        """
        return self._api.http_command

    @property
    def http_setting(self) -> HttpSettings:
        """Used to access the Wifi settings

        Returns:
            HttpSettings: the settings
        """
        return self._api.http_setting

    def open(self, timeout: int = 10, retries: int = 5) -> None:
        """Perform all initialization commands for ble and wifi

        For BLE: scan and find device, establish connection, discover characteristics, configure queries
        start maintenance, and get Open GoPro version..

        For Wifi: discover SSID and password, enable and connect. Or disable if not using.

        Raises:
            Exception: Any exceptions during opening are propagated through
            InvalidOpenGoProVersion: Only 2.0 is supported

        Args:
            timeout (int): How long to wait for each connection before timing out. Defaults to 10.
            retries (int): How many connection attempts before considering connection failed. Defaults to 5.
        """
        try:
            # Establish BLE connection and start maintenance threads if desired
            self._open_ble(timeout, retries)

            # Find and configure API version
            version = self.ble_command.get_open_gopro_api_version().flatten
            version_str = f"{version.major}.{version.minor}"
            if version_str != "2.0":
                raise GpException.InvalidOpenGoProVersion(version)
            logger.info(f"Using Open GoPro API version {version_str}")

            # Establish Wifi connection if desired
            if self._enable_wifi_during_init:
                self._open_wifi(timeout, retries)
            else:
                # Otherwise, turn off Wifi
                logger.info("Turning off the camera's Wifi radio")
                self.ble_command.enable_wifi_ap(enable=False)
        except Exception as e:
            logger.error(f"Error while opening: {e}")
            self.close()
            raise e

    def close(self) -> None:
        """Safely stop the GoPro instance.

        This will disconnect BLE and WiFI if applicable.

        If not using the context manager, it is mandatory to call this before exiting the program in order to
        prevent reconnection issues because the OS has never disconnected from the previous session.
        """
        self._close_wifi()
        self._close_ble()

    @ensure_opened(Interface.BLE)
    def get_notification(self, timeout: Optional[float] = None) -> Optional[GoProResp]:
        """Get an asynchronous notification that we received from a registered listener.

        If timeout is None, this will block until a notification is received.
        The updates are received via FIFO.

        Args:
            timeout (float, Optional): Time to wait for a notification before returning. Defaults to None (wait forever)

        Returns:
            GoProResp: Received notification if there is one in the queue or None otherwise
        """
        try:
            return self._out_q.get(timeout=timeout)
        except queue.Empty:
            return None

    @ensure_opened(Interface.BLE)
    def keep_alive(self) -> bool:
        """Send a heartbeat to prevent the BLE connection from dropping.

        This is sent automatically by the GoPro instance if its `maintain_ble` argument is not False.

        Returns:
            bool: True if it succeeded,. False otherwise
        """
        return self.ble_setting.led.set(Params.LED.BLE_KEEP_ALIVE).is_ok

    @property
    def is_open(self) -> bool:
        """Is this client ready for communication?

        Returns:
            bool: True if yes, False if no
        """
        return self._threads_waiting == 0

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

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

    def _maintain_state(self) -> None:
        """Thread to keep track of ready / encoding and acquire / release ready lock."""
        try:
            self._ready.acquire()
            have_lock = True
            while self.is_ble_connected:

                with self._state_condition:
                    self._state_condition.wait()

                    if have_lock and not (self.is_busy or self.is_encoding):
                        # If this is the first time, mark that we might now be opened
                        if not self.is_open:
                            self._threads_waiting -= 1
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

            self._threads_waiting += 1
            logger.debug("Maintain state thread exiting...")
        except Exception as e:  # pylint: disable=broad-except
            self._handle_exception(threading.current_thread().name, {"exception": e})

    def _periodic_keep_alive(self) -> None:
        """Thread to periodically send the keep alive message via BLE."""
        try:
            while self.is_ble_connected:
                if not self.is_open:
                    self._threads_waiting -= 1
                try:
                    if self.keep_alive():
                        time.sleep(KEEP_ALIVE_INTERVAL)
                except Exception:  # pylint: disable=broad-except
                    # If the connection disconnects while we were trying to send, there can be any number
                    # of exceptions. This is expected and this thread will exit on the next while check.
                    pass

            self._threads_waiting += 1
            logger.debug("periodic keep alive thread exiting...")
        except Exception as e:  # pylint: disable=broad-except
            self._handle_exception(threading.current_thread().name, {"exception": e})

    def _register_listener(self, producer: ProducerType) -> None:
        """Register a producer to store notifications from.

        The notifications can be accessed via the get_notification() method.

        Args:
            producer (ProducerType): Producer to listen to.
        """
        self._listeners[producer] = True

    def _unregister_listener(self, producer: ProducerType) -> None:
        """Unregister a producer in order to stop listening to its notifications.

        Args:
            producer (ProducerType): Producer to stop listening to.
        """
        if producer in self._listeners:
            del self._listeners[producer]

    def _open_ble(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect the instance to a device via BLE.

        Args:
            timeout (int): Time in seconds before considering establishment failed. Defaults to 10 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 5.
        """
        # Establish connection, pair, etc.
        self._ble.open(timeout, retries)
        # Configure threads if desired
        if self._maintain_ble:
            self._state_thread.start()
            self.ble_status.encoding_active.register_value_update()
            self.ble_status.system_ready.register_value_update()
            self.keep_alive()
            self._keep_alive_thread.start()
        logger.info("BLE is ready!")

    def _update_internal_state(self, response: GoProResp) -> None:
        """Update the internal state based on the received response.

        Update encoding and / or busy status and notify state maintenance thread.

        Args:
            response (GoProResp): received response to parse for state changes
        """
        if self._maintain_ble:
            if (
                response.cmd
                in [
                    QueryCmdId.REG_STATUS_VAL_UPDATE,
                    QueryCmdId.GET_STATUS_VAL,
                    QueryCmdId.STATUS_VAL_PUSH,
                ]
                and StatusId.ENCODING in response.data
            ):
                with self._state_condition:
                    if response[StatusId.ENCODING] is True:
                        self._internal_state |= WirelessGoPro._InternalState.ENCODING
                    else:
                        self._internal_state &= ~WirelessGoPro._InternalState.ENCODING
                    self._state_condition.notify()
            if (
                response.cmd
                in [
                    QueryCmdId.REG_STATUS_VAL_UPDATE,
                    QueryCmdId.GET_STATUS_VAL,
                    QueryCmdId.STATUS_VAL_PUSH,
                ]
                and StatusId.SYSTEM_READY in response.data
            ):
                with self._state_condition:
                    if response[StatusId.SYSTEM_READY] is True:
                        self._internal_state &= ~WirelessGoPro._InternalState.SYSTEM_BUSY
                    else:
                        self._internal_state |= WirelessGoPro._InternalState.SYSTEM_BUSY
                    self._state_condition.notify()

    def _notification_handler(self, handle: int, data: bytearray) -> None:
        """Receive notifications from the BLE controller.

        Args:
            handle (int): Attribute handle that notification was received on.
            data (bytearray): Bytestream that was received.
        """
        # Responses we don't care about. For now, just the BLE-spec defined battery characteristic
        if (uuid := self._ble.gatt_db.handle2uuid(handle)) == GoProUUIDs.BATT_LEVEL:
            return
        logger.debug(f'Received response on BleUUID [{uuid}]: {data.hex(":")}')

        # Add to response dict if not already there
        if uuid not in self._active_resp:
            self._active_resp[uuid] = GoProResp(meta=[uuid])

        self._active_resp[uuid]._accumulate(data)

        if (response := self._active_resp[uuid]).is_received:
            response._parse()

            self._update_internal_state(response)

            # Check if this is the awaited synchronous response (id matches). Note! these have to come in order.
            response_claimed = False
            if not self._sync_resp_wait_q.empty():
                queue_snapshot = self._sync_resp_wait_q.snapshot()
                if queue_snapshot[0] == response.identifier:
                    # Dequeue it and put this on the ready queue
                    self._sync_resp_wait_q.get_nowait()
                    self._sync_resp_ready_q.put_nowait(response)
                    response_claimed = True

            # If this wasn't the awaited synchronous response...
            if not response_claimed:
                logger.info(Logger.build_log_rx_str(response, asynchronous=True))
                # See if there are any registered responses that need to be enqueued for client consumption
                for key in list(response.data.keys()):
                    if (response.cmd, key) not in self._listeners and not response.is_protobuf:
                        del response.data[key]
                # Enqueue the response if there is anything left
                if len(response.data) > 0:
                    self._out_q.put_nowait(response)

            # Clear active response from response dict
            del self._active_resp[uuid]

    def _close_ble(self) -> None:
        """Terminate BLE connection if it is connected"""
        if self.is_ble_connected and self._ble is not None:
            self._ble_disconnect_event.clear()
            self._ble.close()
            self._ble_disconnect_event.wait()

    def _disconnect_handler(self, _: Any) -> None:
        """Disconnect callback from BLE controller

        Raises:
            ConnectionTerminated: We entered this callback in an unexpected state.
        """
        if self._ble_disconnect_event.is_set():
            raise GpException.ConnectionTerminated("BLE connection terminated unexpectedly.")
        self._ble_disconnect_event.set()

    @ensure_opened(Interface.BLE)
    def _send_ble_message(self, uuid: BleUUID, data: bytearray, response_id: ResponseType) -> GoProResp:
        """Write a characteristic and block until its corresponding notification response is received.

        Args:
            uuid (BleUUID): characteristic to write to
            data (bytearray): bytes to write
            response_id (ResponseType): identifier to claim parsed response in notification handler

        Raises:
            ResponseTimeout: did not receive a response before timing out

        Returns:
            GoProResp: received response
        """
        assert self._ble
        # Acquire ready lock unless we are initializing or this is a Set Shutter Off command
        have_lock = False
        if self._maintain_ble and self.is_open and not (data[0] == CmdId.SET_SHUTTER.value and data[-1] == 0):
            logger.trace("_send_ble_message acquiring lock")  # type: ignore
            self._ready.acquire()
            logger.trace("_send_ble_message has lock")  # type: ignore
            have_lock = True

        # Store information on the response we are expecting
        self._sync_resp_wait_q.put(response_id)

        # Fragment data and write it
        for packet in self._fragment(data):
            logger.debug(f"Writing to [{uuid.name}] UUID: {packet.hex(':')}")
            self._ble.write(uuid, packet)

        # Wait to be notified that response was received
        try:
            response: GoProResp = self._sync_resp_ready_q.get(timeout=WRITE_TIMEOUT)
        except queue.Empty as e:
            logger.error(f"Response timeout of {WRITE_TIMEOUT} seconds!")
            raise GpException.ResponseTimeout(WRITE_TIMEOUT) from e

        # Check status
        if not response.is_ok:
            logger.warning(f"Received non-success status: {response.status}")

        if self._maintain_ble:
            # Release the lock if we acquired it
            if have_lock:
                self._ready.release()
                logger.trace("command released the lock")  # type: ignore
            # If this was set shutter on success, we need to wait to be notified that encoding has started
            if response.is_ok and response.cmd is CmdId.SET_SHUTTER and data[-1] == 1:
                logger.trace("Waiting to receive encoding started.")  # type: ignore
                self._encoding_started.wait()

        return response

    @ensure_opened(Interface.BLE)
    @acquire_ready_lock
    def _read_characteristic(self, uuid: BleUUID) -> GoProResp:
        """Read a characteristic's data by GoProUUIDs.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.command, self.setting, self.ble_status)

        Args:
            uuid (BleUUID): characteristic data to read

        Returns:
            GoProResp: response from UUID read
        """
        received_data = self._ble.read(uuid)
        logger.debug(f"Reading from {uuid.name}")
        return GoProResp._from_read_response(uuid, received_data)

    @ensure_opened(Interface.BLE)
    def _open_wifi(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect to a GoPro device via Wifi.

        Args:
            timeout (int): Time before considering establishment failed. Defaults to 15 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 10.

        Raises:
            ConnectFailed: Was not able to establish the Wifi Connection
        """
        logger.info("Discovering Wifi AP info and enabling via BLE")
        password = self.ble_command.get_wifi_password().flatten
        ssid = self.ble_command.get_wifi_ssid().flatten
        for retry in range(1, retries):
            try:
                assert self.ble_command.enable_wifi_ap(enable=True).is_ok
                self._wifi.open(ssid, password, timeout, 1)
                break
            except GpException.ConnectFailed:
                logger.warning(f"Wifi connection failed. Retrying #{retry}")
                # In case camera Wifi is in strange disable, reset it
                assert self.ble_command.enable_wifi_ap(enable=False).is_ok
        else:
            raise GpException.ConnectFailed("Wifi Connection failed", timeout, retries)

    def _close_wifi(self) -> None:
        """Terminate the Wifi connection."""
        if hasattr(self, "_wifi"):  # Corner case where instantiation fails before superclass is initialized
            self._wifi.close()

    @ensure_opened(Interface.WIFI)
    @acquire_ready_lock
    def _get(self, url: str, parser: Optional[JsonParser] = None) -> GoProResp:
        """Send an HTTP GET request to an Open GoPro endpoint.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.wifi_command and self.wifi_status)

        Args:
            url (str): endpoint URL
            parser (Optional[JsonParser]): Optional parser to further parse received JSON dict. Defaults to
                None.

        Raises:
            GoProNotOpened: WiFi is not currently connected
            ResponseTimeout: Response was not received in GET_TIMEOUT seconds

        Returns:
            GoProResp: response
        """
        if not self.is_wifi_connected:
            raise GpException.GoProNotOpened("WiFi is not connected.")

        url = WirelessGoPro._BASE_URL + url
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
            finally:
                logger.warning("Retrying to send the command...")
        else:
            raise GpException.ResponseTimeout(HTTP_GET_RETRIES)

        assert response is not None
        return response

    @ensure_opened(Interface.WIFI)
    @acquire_ready_lock
    def _stream_to_file(self, url: str, file: Path) -> None:
        """Send an HTTP GET request to an Open GoPro endpoint to download a binary file.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.wifi_command and self.wifi_status)

        Args:
            url (str): endpoint URL
            file (Path): location where file should be downloaded to
        """
        assert self.is_wifi_connected

        url = WirelessGoPro._BASE_URL + url
        logger.debug(f"Sending: {url}")
        with requests.get(url, stream=True, timeout=GET_TIMEOUT) as request:
            request.raise_for_status()
            with open(file, "wb") as f:
                logger.debug(f"receiving stream to {file}...")
                for chunk in request.iter_content(chunk_size=8192):
                    f.write(chunk)
