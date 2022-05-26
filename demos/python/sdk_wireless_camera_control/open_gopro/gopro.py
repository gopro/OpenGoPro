# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations
import time
import enum
import queue
import logging
import threading
from queue import Queue
from pathlib import Path
from typing import Any, Dict, Final, Optional, Callable, Union, Generic, Pattern

import wrapt
import requests

from open_gopro.exceptions import (
    GoProNotInitialized,
    InvalidOpenGoProVersion,
    ResponseTimeout,
    InvalidConfiguration,
    ConnectionTerminated,
)
from open_gopro.ble import BleUUID, BleDevice
from open_gopro.ble.adapters import BleakWrapperController
from open_gopro.wifi.adapters import Wireless
from open_gopro.util import SnapshotQueue, build_log_rx_str
from open_gopro.responses import GoProResp
from open_gopro.constants import CmdId, GoProUUIDs, StatusId, QueryCmdId, ProducerType
from open_gopro.api import Api, BleCommands, BleSettings, BleStatuses, WifiCommands, WifiSettings, Params
from open_gopro.communication_client import GoProBle, GoProWifi

logger = logging.getLogger(__name__)

KEEP_ALIVE_INTERVAL: Final = 60
WRITE_TIMEOUT: Final = 5
GET_TIMEOUT: Final = 5
HTTP_GET_RETRIES: Final = 5

ExceptionHandler = Callable[[Exception], None]


class Interface(enum.Enum):
    """Enum to identify wireless interface"""

    WIFI = enum.auto()
    BLE = enum.auto()


def ensure_initialized(interface: Interface) -> Callable:
    """Raise exception if relevant interface is not currently initialized

    Args:
        interface (Interface): wireless interface to verify

    Returns:
        Callable: Direct pass-through of callable after verification
    """

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: GoPro, args: Any, kwargs: Any) -> Any:
        if interface is Interface.BLE and not instance.is_ble_connected:
            raise GoProNotInitialized("BLE not connected")
        if interface is Interface.WIFI and not instance.is_wifi_connected:
            raise GoProNotInitialized("Wifi not connected")
        return wrapped(*args, **kwargs)

    return wrapper


@wrapt.decorator
def acquire_ready_lock(wrapped: Callable, instance: GoPro, args: Any, kwargs: Any) -> Any:
    """Call method after acquiring ready lock.

    Release lock when done

    Args:
        wrapped (Callable): method to call
        instance (GoPro): instance that owns the method
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


class GoPro(GoProBle, GoProWifi, Generic[BleDevice]):
    """The top-level BLE and Wifi interface to a GoPro device.

    See `Open GoPro <https://gopro.github.io/OpenGoPro/python_sdk>`_ for complete documentation.

    This will handle for BLE:

    - discovering device
    - establishing connections
    - discovering GATT characteristics
    - enabling notifications
    - discovering Open GoPro version
    - transferring data

    This will handle for Wifi:

    - finding SSID and password
    - establishing Wifi connection
    - transferring data

    It will also do some synchronization, etc:

    - ensuring camera is ready / not encoding before transferring data
    - sending keep alive signal periodically

    If no target arg is passed in, the first discovered GoPro device will be connected to.

    It can be used via context manager:

    >>> with GoPro() as gopro:
    >>>     gopro.ble_command.set_shutter(Params.Shutter.ON)

    Or without:

    >>> gopro = GoPro()
    >>> gopro.open()
    >>> gopro.ble_command.set_shutter(Params.Shutter.ON)
    >>> gopro.close()

    Args:
        target (Optional[Union[Pattern, BleDevice]], optional): Last 4 of camera name / serial number
            (i.e. 0456 for GoPro0456). Defaults to None (i.e. connect to first discovered GoPro)
        wifi_interface (str): Set to specify the wifi interface the local machine will use to connect
            to the GoPro. If None (or not set), first discovered interface will be used.
        enable_wifi (bool): Optionally do not enable Wifi if set to False. Defaults to True.
        exception_cb (ExceptionHandler): callback to be notified when exception occurs in a thread besides main
        kwargs (Dict): additional parameters for internal use / testing
    """

    _base_url = "http://10.5.5.9:8080/"  #: Hard-coded Open GoPro base URL

    class _InternalState(enum.IntFlag):
        """State used to manage whether the GoPro instance is ready or not."""

        READY = 0
        ENCODING = 1 << 0
        SYSTEM_BUSY = 1 << 1

    def __init__(
        self,
        target: Optional[Union[Pattern, BleDevice]] = None,
        wifi_interface: Optional[str] = None,
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

        # Initialize GoPro Communication Client
        GoProBle.__init__(
            self,
            ble_adapter(self._handle_exception),
            self._disconnect_handler,
            self._notification_handler,
            target,
        )
        GoProWifi.__init__(self, wifi_adapter(wifi_interface))

        # We currently only support version 2.0
        self._api = Api(self, self)

        # Current accumulating synchronous responses, indexed by GoProUUIDs. This assumes there can only be one active response per BleUUID
        self._active_resp: Dict[BleUUID, GoProResp] = {}
        # Responses that we are waiting for.
        self._sync_resp_wait_q: SnapshotQueue = SnapshotQueue()
        # Synchronous response that has been parsed and are ready for their sender to receive as the response.
        self._sync_resp_ready_q: SnapshotQueue = SnapshotQueue()

        # For outputting asynchronously received information
        self._out_q: "Queue[GoProResp]" = Queue()
        self._listeners: Dict[ProducerType, bool] = {}

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
            self._internal_state = GoPro._InternalState.ENCODING | GoPro._InternalState.SYSTEM_BUSY
            self._state_thread = threading.Thread(target=self._maintain_state, name="state", daemon=True)

    def __enter__(self) -> "GoPro":
        self.open()
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    @property
    def identifier(self) -> Optional[str]:
        """Get a unique identifier for this instance.

        The identifier is the last 4 digits of the camera. That is, the same string that is used to
        scan for the camera for BLE.

        If no target has been provided and a camera is not yet found, this will be None

        Returns:
            Optional[str]: last 4 digits if available, else None
        """
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
            raise InvalidConfiguration("Not maintaining BLE state so encoding is not applicable")
        return bool(self._internal_state & GoPro._InternalState.ENCODING)

    @property
    def is_busy(self) -> bool:
        """Is the camera currently performing a task that prevents it from accepting commands?

        Raises:
            InvalidConfiguration: if maintain_state is False, there is no way to know the GoPro's state

        Returns:
            bool: True if yes, False if no
        """
        if not self._maintain_ble:
            raise InvalidConfiguration("Not maintaining BLE state so busy is not applicable")
        return bool(self._internal_state & GoPro._InternalState.SYSTEM_BUSY)

    @property
    def version(self) -> float:
        """The API version does the connected camera supports

        Only 2.0 is currently supported

        Returns:
            float: supported version in decimal form
        """
        return float(self._api.version)

    @property
    def ble_command(self) -> BleCommands:
        """Used to call the version-specific BLE commands

        Returns:
            BleCommands: the commands
        """
        return self._api.ble_command

    @property
    def ble_setting(self) -> BleSettings:
        """Used to access the version-specific BLE settings

        Returns:
            BleSettings: the settings
        """
        return self._api.ble_setting

    @property
    def ble_status(self) -> BleStatuses:
        """Used to access the version-specific BLE statuses

        Returns:
            BleStatuses: the statuses
        """
        return self._api.ble_status

    @property
    def wifi_command(self) -> WifiCommands:
        """Used to access the version-specific Wifi commands

        Returns:
            WifiCommands: the commands
        """
        return self._api.wifi_command

    @property
    def wifi_setting(self) -> WifiSettings:
        """Used to access the version-specific Wifi settings

        Returns:
            WifiSettings: the settings
        """
        return self._api.wifi_setting

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
                raise InvalidOpenGoProVersion(version)
            logger.info(f"Using Open GoPro API version {version_str}")

            # Establish Wifi connection if desired
            if self._enable_wifi_during_init:
                self._open_wifi(timeout, retries)
            else:
                # Otherwise, turn off Wifi
                logger.info("Turning off the camera's Wifi radio")
                self.ble_command.enable_wifi_ap(False)
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

    @ensure_initialized(Interface.BLE)
    def get_update(self, timeout: Optional[float] = None) -> GoProResp:
        """Get a notification that we received from a registered listener.

        If timeout is None, this will block until a notification is received.
        The updates are received via FIFO

        Args:
            timeout (float, optional): Time to wait for a notification before returning. Defaults to None (wait forever)

        Returns:
            GoProResp: Received notification
        """
        return self._out_q.get(timeout=timeout)

    @ensure_initialized(Interface.BLE)
    def keep_alive(self) -> bool:
        """Send a heartbeat to prevent the BLE connection from dropping.

        This is sent automatically by the GoPro instance if its `maintain_ble` argument is not False.

        Returns:
            bool: True if it succeeded,. False otherwise
        """
        return self.ble_setting.led.set(Params.LED.BLE_KEEP_ALIVE).is_ok

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    @property
    def _is_ble_initialized(self) -> bool:
        """Are we done

        Returns:
            bool: True if yes, False if no
        """
        return self._threads_waiting == 0

    def _handle_exception(self, source: Any, context: Dict[str, Any]) -> None:
        """Gather exceptions from module threads and send through callback if registered.

        Note that this function signature matches asyncio's exception callback requirement.

        Args:
            source (Any): Where did the exception come from?
            context (Dict): Access exception via context["exception"]
        """
        # context["message"] will always be there; but context["exception"] may not
        if exception := context.get("exception", False):
            logger.error(f"Received exception {exception} from {source}")
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
                        # If this is the first time, mark that we might now be initialized
                        if not self._is_ble_initialized:
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
                if not self._is_ble_initialized:
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

        The notifications can be accessed via the get_update() method.

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
                        self._internal_state |= GoPro._InternalState.ENCODING
                    else:
                        self._internal_state &= ~GoPro._InternalState.ENCODING
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
                        self._internal_state &= ~GoPro._InternalState.SYSTEM_BUSY
                    else:
                        self._internal_state |= GoPro._InternalState.SYSTEM_BUSY
                    self._state_condition.notify()

    # TODO refactor this into smaller methods
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
            self._active_resp[uuid] = GoProResp(self._parser_map, meta=[uuid])

        self._active_resp[uuid]._accumulate(data)

        if self._active_resp[uuid].is_received:
            response = self._active_resp[uuid]
            response._parse()

            self._update_internal_state(response)

            # Check if this is the awaited synchronous response (id matches). Note! these have to come in order.
            response_claimed = False
            if not self._sync_resp_wait_q.empty():
                queue_snapshot = self._sync_resp_wait_q.snapshot()
                if queue_snapshot[0].id is response.id:
                    # Dequeue it and put this on the ready queue
                    self._sync_resp_wait_q.get_nowait()
                    self._sync_resp_ready_q.put_nowait(response)
                    response_claimed = True

            # If this wasn't the awaited synchronous response...
            if not response_claimed:
                logger.info(build_log_rx_str(response, asynchronous=True))
                # See if there are any registered responses that need to be enqueued for client consumption
                for key in list(response.data.keys()):
                    if (response.cmd, key) not in self._listeners:
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
            raise ConnectionTerminated("BLE connection terminated unexpectedly.")
        self._ble_disconnect_event.set()

    # TODO refactor to allow use of lock decorator which will require a state table for commands/  responses
    @ensure_initialized(Interface.BLE)
    def _write_characteristic_receive_notification(self, uuid: BleUUID, data: bytearray) -> GoProResp:
        """Perform a BLE write and wait for a corresponding notification response.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's API delegate (i.e. self)

        Args:
            uuid (BleUUID): BleUUID to write to
            data (bytearray): data to write

        Raises:
            ResponseTimeout: A response was not received in WRITE_TIMEOUT seconds

        Returns:
            GoProResp: parsed notification response data
        """
        assert self._ble
        # Build response stub to be filled out as it is received
        response = GoProResp._from_write_command(self._parser_map, uuid, data)
        # Acquire ready lock unless we are initializing or this is a Set Shutter Off command
        have_lock = False
        if (
            self._maintain_ble
            and self._is_ble_initialized
            and not (response.id is CmdId.SET_SHUTTER and data[-1] == 0)
        ):
            logger.trace(f"{response.id} acquiring lock")  # type: ignore
            self._ready.acquire()
            logger.trace(f"{response.id} has lock")  # type: ignore
            have_lock = True

        # Store information on the response we are expecting
        self._sync_resp_wait_q.put(response)
        # Perform write
        logger.debug(f"Writing to [{uuid.name}] UUID: {data.hex(':')}")
        self._ble.write(uuid, data)
        # Wait to be notified that response was received
        try:
            response = self._sync_resp_ready_q.get(timeout=WRITE_TIMEOUT)
        except queue.Empty as e:
            logger.error(f"Response timeout of {WRITE_TIMEOUT} seconds!")
            raise ResponseTimeout(WRITE_TIMEOUT) from e

        # Check status
        if not response.is_ok:
            logger.warning(f"Received non-success status: {response.status}")

        if self._maintain_ble:
            # Release the lock if we acquired it
            if have_lock:
                self._ready.release()
                logger.trace(f"{response.id} released the lock")  # type: ignore
            # If this was set shutter on, we need to wait to be notified that encoding has started
            if response.cmd is CmdId.SET_SHUTTER and data[-1] == 1:
                self._encoding_started.wait()

        return response

    @ensure_initialized(Interface.BLE)
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
        return GoProResp._from_read_response(self._parser_map, uuid, received_data)

    @ensure_initialized(Interface.BLE)
    def _open_wifi(self, timeout: int = 15, retries: int = 5) -> None:
        """Connect to a GoPro device via Wifi.

        Args:
            timeout (int): Time before considering establishment failed. Defaults to 15 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 5.
        """
        logger.info("Discovering Wifi AP info and enabling via BLE")
        password = self.ble_command.get_wifi_password().flatten
        ssid = self.ble_command.get_wifi_ssid().flatten
        self.ble_command.enable_wifi_ap(True)
        self._wifi.open(ssid, password, timeout, retries)

    def _close_wifi(self) -> None:
        """Terminate the Wifi connection."""
        if hasattr(self, "_wifi"):  # Corner case where instantication fails before superclass is initialized
            self._wifi.close()

    @ensure_initialized(Interface.WIFI)
    @acquire_ready_lock
    def _get(self, url: str) -> GoProResp:
        """Send an HTTP GET request to an Open GoPro endpoint.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.wifi_command and self.wifi_status)

        Args:
            url (str): endpoint URL

        Raises:
            GoProNotInitialized: WiFi is not currently connected
            ResponseTimeout: Response was not received in GET_TIMEOUT seconds

        Returns:
            GoProResp: response
        """
        if not self.is_wifi_connected:
            raise GoProNotInitialized("WiFi is not connected.")

        url = GoPro._base_url + url
        logger.debug(f"Sending:  {url}")

        response: Optional[GoProResp] = None
        for retry in range(HTTP_GET_RETRIES):
            try:
                request = requests.get(url, timeout=GET_TIMEOUT)
                request.raise_for_status()
                response = GoProResp._from_http_response(self._parser_map, request)
                break
            except requests.exceptions.HTTPError as e:
                # The camera responded with an error. Break since we successfully sent the command and attempt
                # to continue
                logger.warning(e)
                response = GoProResp._from_http_response(self._parser_map, e.response)
                break
            except requests.exceptions.ConnectionError as e:
                logger.warning(repr(e))
                logger.warning("Retrying to send the command...")
                if retry == HTTP_GET_RETRIES - 1:
                    raise ResponseTimeout(HTTP_GET_RETRIES) from e

        assert response is not None
        return response

    @ensure_initialized(Interface.WIFI)
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

        url = GoPro._base_url + url
        logger.debug(f"Sending: {url}")
        with requests.get(url, stream=True) as request:
            request.raise_for_status()
            with open(file, "wb") as f:
                logger.debug(f"receiving stream to {file}...")
                for chunk in request.iter_content(chunk_size=8192):
                    f.write(chunk)
