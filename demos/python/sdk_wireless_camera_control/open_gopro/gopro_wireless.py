# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations
import time
import queue
import logging
import threading
from pathlib import Path
from queue import Queue
from typing import Any, Final, Optional, Pattern

import wrapt

import open_gopro.exceptions as GpException
from open_gopro.gopro_base import GoProBase, MessageMethodType, GoProMessageInterface
from open_gopro.ble import BleUUID
from open_gopro.ble.adapters import BleakWrapperController
from open_gopro.wifi.adapters import Wireless
from open_gopro.util import SnapshotQueue, Logger
from open_gopro.responses import GoProResp, ResponseType, JsonParser
from open_gopro.constants import GoProUUIDs, StatusId, QueryCmdId, ProducerType
from open_gopro.api import (
    WirelessApi,
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    Params,
)
from open_gopro.interface import GoProWirelessInterface, MessageRules

logger = logging.getLogger(__name__)

KEEP_ALIVE_INTERVAL: Final = 28
WRITE_TIMEOUT: Final = 5
GET_TIMEOUT: Final = 5
HTTP_GET_RETRIES: Final = 5


@wrapt.decorator
def enforce_message_rules(
    wrapped: MessageMethodType, instance: WirelessGoPro, args: Any, kwargs: Any
) -> GoProResp:
    """Wrap the input message method, applying any message rules (MessageRules)

    Args:
        wrapped (MessageMethodType): Method that will be wrapped
        instance (WirelessGoPro): owner of method
        args (Any): positional arguments
        kwargs (Any): keyword arguments

    Returns:
        GoProResp: forward response of message method
    """
    rules: list[MessageRules] = kwargs.pop("rules", [])

    # Acquire ready lock unless we are initializing or this is a Set Shutter Off command
    have_lock = False
    if instance._should_maintain_state and instance.is_open and not MessageRules.FASTPASS in rules:
        logger.trace(f"{wrapped.__name__} acquiring lock")  # type: ignore
        instance._ready.acquire()
        logger.trace(f"{wrapped.__name__} has the lock")  # type: ignore
        have_lock = True
        response = wrapped(*args, **kwargs)
    else:  # Either we're not maintaining state, we're not opened yet, or this is a fastpass message
        response = wrapped(*args, **kwargs)

    # Release the lock if we acquired it
    if instance._should_maintain_state:
        if have_lock:
            instance._ready.release()
            logger.trace(f"{wrapped.__name__} released the lock")  # type: ignore
        if response.is_ok:
            # Is there any special handling required after receiving the response?
            if MessageRules.WAIT_FOR_ENCODING_START in rules:
                logger.trace("Waiting to receive encoding started.")  # type: ignore
                instance._encoding_started.wait()
    return response


class WirelessGoPro(GoProBase[WirelessApi], GoProWirelessInterface):
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
        kwargs (Dict): additional parameters for internal use / testing

    # noqa: DAR401

    Raises:
        InterfaceConfigFailure: In order to communicate via Wifi, there must be an available # noqa: DAR402
            Wifi Interface. By default during initialization, the Wifi driver will attempt to automatically
            discover such an interface. If it does not find any, it will raise this exception. Note that
            the interface can also be specified manually with the 'wifi_interface' argument.
    """

    def __init__(
        self,
        target: Optional[Pattern] = None,
        wifi_interface: Optional[str] = None,
        sudo_password: Optional[str] = None,
        enable_wifi: bool = True,
        **kwargs: Any,
    ) -> None:
        GoProBase.__init__(self, **kwargs)
        # Store initialization information
        self._should_enable_wifi = enable_wifi
        ble_adapter = kwargs.get("ble_adapter", BleakWrapperController)
        wifi_adapter = kwargs.get("wifi_adapter", Wireless)
        # Set up API delegate
        self._wireless_api = WirelessApi(self)

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

        # Current accumulating synchronous responses, indexed by GoProUUIDs. This assumes there can only be one active response per BleUUID
        self._active_resp: dict[BleUUID, GoProResp] = {}
        # Responses that we are waiting for.
        self._sync_resp_wait_q: SnapshotQueue = SnapshotQueue()
        # Synchronous response that has been parsed and are ready for their sender to receive as the response.
        self._sync_resp_ready_q: SnapshotQueue = SnapshotQueue()

        # For outputting asynchronously received information
        self._out_q: Queue[GoProResp] = Queue()
        self._listeners: dict[ProducerType, bool] = {}

        # Set up BLE threading
        self._ble_disconnect_event = threading.Event()
        self._ble_disconnect_event.set()
        self._keep_alive_thread = threading.Thread(
            target=self._periodic_keep_alive, daemon=True, name="keep alive"
        )
        self._open = False

        # If we are to perform BLE housekeeping
        if self._should_maintain_state:
            self._ready: threading.Lock = threading.Lock()
            # Busy / encoding management
            self._state_condition: threading.Condition = threading.Condition()
            self._encoding_started: threading.Event = threading.Event()
            self._encoding_started.clear()
            self._internal_state = GoProBase._InternalState.ENCODING | GoProBase._InternalState.SYSTEM_BUSY
            self._state_thread = threading.Thread(target=self._maintain_state, name="state", daemon=True)
            self._state_thread.start()

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
    def is_http_connected(self) -> bool:
        """Are we connected via HTTP to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        return self._wifi.is_connected

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
            if version_str != self.version:
                raise GpException.InvalidOpenGoProVersion(version)
            logger.info(f"Using Open GoPro API version {version_str}")

            # Establish Wifi connection if desired
            if self._should_enable_wifi:
                self._open_wifi(timeout, retries)
            else:
                # Otherwise, turn off Wifi
                logger.info("Turning off the camera's Wifi radio")
                self.ble_command.enable_wifi_ap(enable=False)
            self._open = True

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
        self._open = False

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
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

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
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
        return self._open

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    @GoProBase._catch_thread_exception
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

    def _set_state_encoding(self, encoding: bool) -> None:
        """Set whether or not the GoPro is currently encoding

        Args:
            encoding (bool): True if encoding
        """
        with self._state_condition:
            if encoding is True:
                self._internal_state |= GoProBase._InternalState.ENCODING
            else:
                self._internal_state &= ~GoProBase._InternalState.ENCODING
            self._state_condition.notify()

    def _set_state_busy(self, busy: bool) -> None:
        """Set whether or not the GoPro is currently busy

        Args:
            busy (bool): True if busy
        """
        with self._state_condition:
            if busy is False:
                self._internal_state &= ~GoProBase._InternalState.SYSTEM_BUSY
            else:
                self._internal_state |= GoProBase._InternalState.SYSTEM_BUSY
            self._state_condition.notify()

    @GoProBase._catch_thread_exception
    def _periodic_keep_alive(self) -> None:
        """Thread to periodically send the keep alive message via BLE."""
        while self.is_ble_connected:
            try:
                if self.keep_alive():
                    time.sleep(KEEP_ALIVE_INTERVAL)
            except Exception:  # pylint: disable=broad-except
                # If the connection disconnects while we were trying to send, there can be any number
                # of exceptions. This is expected and this thread will exit on the next while check.
                pass
        logger.debug("periodic keep alive thread exiting...")

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
        # Start keep alive and state maintenance
        if self._should_maintain_state:
            self.ble_status.encoding_active.register_value_update()
            self.ble_status.system_busy.register_value_update()
            self.keep_alive()
            self._keep_alive_thread.start()
        logger.info("BLE is ready!")

    def _update_internal_state(self, response: GoProResp) -> None:
        """Update the internal state based on the received response.

        Update encoding and / or busy status and notify state maintenance thread.

        Args:
            response (GoProResp): received response to parse for state changes
        """
        if not self._should_maintain_state:
            return
        if response.cmd in [
            QueryCmdId.REG_STATUS_VAL_UPDATE,
            QueryCmdId.GET_STATUS_VAL,
            QueryCmdId.STATUS_VAL_PUSH,
        ]:
            if StatusId.ENCODING in response.data:
                self._set_state_encoding(response[StatusId.ENCODING])
            if StatusId.SYSTEM_BUSY in response.data:
                self._set_state_busy(response[StatusId.SYSTEM_BUSY])

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

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    @enforce_message_rules
    def _send_ble_message(
        self, uuid: BleUUID, data: bytearray, response_id: ResponseType, **_: Any
    ) -> GoProResp:
        """Write a characteristic and block until its corresponding notification response is received.

        Args:
            uuid (BleUUID): characteristic to write to
            data (bytearray): bytes to write
            response_id (ResponseType): identifier to claim parsed response in notification handler
            **_ (Any): not used

        Raises:
            ResponseTimeout: did not receive a response before timing out

        Returns:
            GoProResp: received response
        """
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

        return response

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    @enforce_message_rules
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

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    def _open_wifi(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect to a GoPro device via Wifi.

        Args:
            timeout (int): Time before considering establishment failed. Defaults to 15 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 10.

        Raises:
            ConnectFailed: Was not able to establish the Wifi Connection
        """
        logger.info("Discovering Wifi AP info and enabling via BLE")
        # TODO skip if we're already connected to this SSID
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

    @enforce_message_rules
    def _get(self, url: str, parser: Optional[JsonParser] = None, **kwargs: Any) -> GoProResp:
        return super()._get(url, parser, **kwargs)

    @enforce_message_rules
    def _stream_to_file(self, url: str, file: Path) -> GoProResp:
        return super()._stream_to_file(url, file)

    @property
    def _base_url(self) -> str:
        return "http://10.5.5.9:8080/"

    @property
    def _api(self) -> WirelessApi:
        return self._wireless_api
