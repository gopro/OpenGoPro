# gopro_wireless.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to Wireless GoPros."""

from __future__ import annotations

import asyncio
import enum
import logging
import queue
import traceback
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Final

import requests
from tinydb import TinyDB

import open_gopro.features
from open_gopro.api import (
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    WirelessApi,
)
from open_gopro.domain.communicator_interface import (
    BleMessage,
    GoProBle,
    GoProWirelessInterface,
    HttpMessage,
    Message,
    MessageRules,
)
from open_gopro.domain.exceptions import (
    ConnectFailed,
    ConnectionTerminated,
    GoProNotOpened,
    InterfaceConfigFailure,
    InvalidOpenGoProVersion,
    ResponseTimeout,
)

# These are imported this way for monkeypatching in pytest
from open_gopro.domain.gopro_observable import GoProObservable
from open_gopro.gopro_base import (
    GoProBase,
    GoProMessageInterface,
    enforce_message_rules,
)
from open_gopro.models import GoProResp
from open_gopro.models.constants import ActionId, GoProUUID, StatusId
from open_gopro.models.constants.settings import SettingId
from open_gopro.models.types import ResponseType, UpdateCb, UpdateType
from open_gopro.network.ble import BleakWrapperController, BleUUID
from open_gopro.network.ble.controller import BLEController
from open_gopro.network.wifi import WifiCli
from open_gopro.network.wifi.controller import WifiController
from open_gopro.network.wifi.requests_session import create_less_strict_requests_session
from open_gopro.parsers.response import BleRespBuilder
from open_gopro.util import SnapshotQueue, get_current_dst_aware_time, pretty_print
from open_gopro.util.logger import Logger

logger = logging.getLogger(__name__)


class _ReadyLock:
    """Camera ready state lock manager"""

    class _LockOwner(enum.Enum):
        """Current owner of the communication lock"""

        RULE_ENFORCER = enum.auto()
        STATE_MANAGER = enum.auto()

    def __init__(self) -> None:
        self.lock = asyncio.Lock()
        self.owner: _ReadyLock._LockOwner | None = None

    async def __aenter__(self) -> _ReadyLock:
        """Acquire lock with clear ownership tracking"""
        await self.lock.acquire()
        return self

    async def __aexit__(self, exc_type: BaseException, exc_val: Any, exc_tb: TracebackType) -> None:
        """Release lock and clear ownership"""
        if self.lock.locked():
            self.lock.release()
            self.owner = None

    async def acquire(self, owner: _LockOwner) -> None:
        """Acquire lock with specified owner

        Args:
            owner (_LockOwner): Owner attempting to acquire lock
        """
        logger.trace(f"{owner.name} acquiring lock")  # type: ignore
        await self.lock.acquire()
        self.owner = owner
        logger.trace(f"{owner.name} acquired lock")  # type: ignore

    def release(self) -> None:
        """Release lock if locked"""
        if self.lock.locked():
            logger.trace(f"{self.owner.name} releasing lock")  # type: ignore
            self.lock.release()
            self.owner = None


class WirelessGoPro(GoProBase[WirelessApi], GoProWirelessInterface):
    """The top-level BLE and Wifi interface to a Wireless GoPro device.

    See the `Open GoPro SDK <https://gopro.github.io/OpenGoPro/python_sdk>`_ for complete documentation.

    This will handle, for BLE:

    - discovering target GoPro device
    - establishing the connection
    - discovering GATT characteristics
    - enabling notifications
    - discovering Open GoPro version
    - setting the date, time, timezone, and DST
    - transferring data

    This will handle, for Wifi:

    - finding SSID and password
    - establishing Wifi connection
    - transferring data

    This will handle, for COHN:
    - connecting to Access Point and provisioning COHN
    - maintaining the COHN credential database
    - appending COHN headers to HTTP requests

    It will also do some state management, etc:

    - ensuring camera is ready / not encoding before transferring data
    - sending keep alive signal periodically
    - tracking COHN state

    If no target arg is passed in, the first discovered BLE GoPro device will be connected to.

    It can be used via context manager:

    >>> async with WirelessGoPro() as gopro:
    >>>     # Send some messages now

    Or without:

    >>> gopro = WirelessGoPro()
    >>> await gopro.open()
    >>> # Send some messages now

    Attributes:
        WRITE_TIMEOUT (Final[int]): BLE Write Timeout in seconds. Not configurable.

    Args:
        target (str | None): The trailing digits of the target GoPro's serial number to search for.
            Defaults to None which will connect to the first discovered GoPro.
        host_wifi_interface (str | None): used to specify the wifi interface the local machine will use to connect
            to the GoPro. Defaults to None in which case the first discovered interface will be used. This is only
            needed if you have multiple wifi interfaces on your machine.
        host_sudo_password (str | None): User password for sudo. Defaults to None in which case you will
            be prompted if a password is needed which should only happen on Nix systems. This is only needed for
            Nix systems where the user does not have passwordless sudo access to the wifi interface.
        cohn_db (Path): Path to COHN Database. Defaults to Path("cohn_db.json").
        interfaces (set[WirelessGoPro.Interface] | None): Wireless interfaces for which to attempt to
            establish communication channels. Defaults to None in which case both BLE and WiFi will be used.
        **kwargs (Any): additional parameters for internal use / testing

    Raises:
        ValueError: Invalid combination of arguments.
        InterfaceConfigFailure: In order to communicate via Wifi, there must be an available
            Wifi Interface. By default during initialization, the Wifi driver will attempt to automatically
            discover such an interface. If it does not find any, it will raise this exception. Note that
            the interface can also be specified manually with the 'wifi_interface' argument.
    """

    WRITE_TIMEOUT: Final[int] = 5

    class Interface(enum.Enum):
        """GoPro Wireless Interface selection"""

        BLE = enum.auto()  #: Bluetooth Low Energy
        WIFI_AP = enum.auto()  #: Wifi Access Point
        COHN = enum.auto()  #: Camera on the Home Network (WIFI_STA mode).

    def __init__(
        self,
        target: str | None = None,
        host_wifi_interface: str | None = None,
        host_sudo_password: str | None = None,
        cohn_db: Path = Path("cohn_db.json"),
        interfaces: set[WirelessGoPro.Interface] | None = None,
        **kwargs: Any,
    ) -> None:
        GoProBase.__init__(self, **kwargs)
        # Store initialization information
        interfaces = interfaces or {WirelessGoPro.Interface.BLE, WirelessGoPro.Interface.WIFI_AP}
        self._should_enable_wifi = WirelessGoPro.Interface.WIFI_AP in interfaces
        self._should_enable_ble = WirelessGoPro.Interface.BLE in interfaces
        self._should_enable_cohn = WirelessGoPro.Interface.COHN in interfaces
        self._cohn_db_path = cohn_db
        self._cohn_credentials = kwargs.get("cohn_credentials")
        self._is_cohn_configured = False

        # Valid parameter selections
        if self._should_enable_wifi and self._should_enable_cohn:
            raise ValueError("Can not have simultaneous COHN and Wifi Access Point connections")
        if self._should_enable_wifi and not self._should_enable_ble:
            raise ValueError("Can not have Wifi Access Point connection without BLE")

        self._identifier = target

        ble_adapter: type[BLEController] = kwargs.get("ble_adapter", BleakWrapperController)
        wifi_adapter: type[WifiController] = kwargs.get("wifi_adapter", WifiCli)
        # Set up API delegate
        self._wireless_api = WirelessApi(self)
        self._keep_alive_interval: int = kwargs.get("keep_alive_interval", 3)

        try:
            # Initialize GoPro Communication Client
            GoProWirelessInterface.__init__(
                self,
                ble_controller=ble_adapter(self._handle_exception),
                wifi_controller=wifi_adapter(host_wifi_interface, password=host_sudo_password),
                disconnected_cb=self._disconnect_handler,
                notification_cb=self._notification_handler,
                target=target,
            )
        except InterfaceConfigFailure as e:
            logger.error(
                "Could not find a suitable Wifi Interface. If there is an available Wifi interface, try passing it manually with the 'wifi_interface' argument."
            )
            raise e

        # Feature delegates
        self._cohn: open_gopro.features.CohnFeature
        self._access_point: open_gopro.features.AccessPointFeature
        self._streaming: open_gopro.features.StreamFeature

        # Builders for currently accumulating synchronous responses, indexed by GoProUUID. This assumes there
        # can only be one active response per BleUUID
        self._active_builders: dict[BleUUID, BleRespBuilder] = {}
        # Responses that we are waiting for.
        self._sync_resp_wait_q: SnapshotQueue[ResponseType] = SnapshotQueue()
        # Synchronous response that has been parsed and are ready for their sender to receive as the response.
        self._sync_resp_ready_q: SnapshotQueue[GoProResp] = SnapshotQueue()

        self._listeners: dict[UpdateType | GoProBle._CompositeRegisterType, set[UpdateCb]] = defaultdict(set)

        # To be set up when opening in async context
        self._loop: asyncio.AbstractEventLoop
        self._open = False
        self._is_ble_connected = False
        self._ble_disconnect_event: asyncio.Event

        if self._should_maintain_state:
            self._status_tasks: list[asyncio.Task] = []
            self._state_acquire_lock_tasks: list[asyncio.Task] = []
            self._ready_lock: _ReadyLock
            self._keep_alive_task: asyncio.Task
            self._encoding: bool
            self._busy: bool
            self._encoding_started: asyncio.Event

    @property
    def cohn(self) -> open_gopro.features.CohnFeature:
        """The COHN feature abstraction

        Raises:
            GoProNotOpened: Feature is not yet available because GoPro has not yet been opened

        Returns:
            open_gopro.features.CohnFeature: COHN Feature
        """
        try:
            return self._cohn
        except AttributeError as e:
            raise GoProNotOpened("") from e

    @property
    def access_point(self) -> open_gopro.features.AccessPointFeature:
        """The Access Point (AP) feature abstraction

        Raises:
            GoProNotOpened: Feature is not yet available because GoPro has not yet been opened

        Returns:
            open_gopro.features.AccessPointFeature: AP Feature
        """
        try:
            return self._access_point
        except AttributeError as e:
            raise GoProNotOpened("") from e

    @property
    def streaming(self) -> open_gopro.features.StreamFeature:
        """The Streaming feature abstraction

        Raises:
            GoProNotOpened: Feature is not yet available because GoPro has not yet been opened

        Returns:
            open_gopro.features.StreamFeature: Streaming Feature
        """
        try:
            return self._streaming
        except AttributeError as e:
            raise GoProNotOpened("") from e

    @property
    def identifier(self) -> str:
        """Get a unique identifier for this instance.

        The identifier is the last 4 digits of the camera. That is, the same string that is used to
        scan for the camera for BLE.

        Raises:
            GoProNotOpened: Client is not opened yet so no identifier is available

        Returns:
            str: last 4 digits if available, else None
        """
        if not self._identifier:
            raise GoProNotOpened("Identifier not yet set")
        return self._identifier

    @property
    def is_ble_connected(self) -> bool:
        """Are we connected via BLE to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        # We can't rely on the BLE Client since it can be connected but not ready
        return self._is_ble_connected

    @property
    def is_http_connected(self) -> bool:
        """Are we connected via HTTP to the GoPro device?

        That is, are we connected to the camera's access point or via COHN?

        Returns:
            bool: True if yes, False if no
        """
        return self._is_cohn_configured or self._wifi.is_connected

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

    async def open(self, timeout: int = 15, retries: int = 5) -> None:
        """Perform all initialization commands for ble and wifi

        For BLE: scan and find device, establish connection, discover characteristics, configure queries
        start maintenance, and get Open GoPro version..

        For Wifi: discover SSID and password, enable and connect. Or disable if not using.

        Raises:
            Exception: Any exceptions during opening are propagated through
            InvalidOpenGoProVersion: Only 2.0 is supported
            InterfaceConfigFailure: Requested connection(s) failed to establish

        Args:
            timeout (int): How long to wait for each connection before timing out. Defaults to 10.
            retries (int): How many connection attempts before considering connection failed. Defaults to 5.
        """
        # Set up concurrency
        self._loop = asyncio.get_running_loop()
        self._ble_disconnect_event = asyncio.Event()
        self._cohn = open_gopro.features.CohnFeature(
            cohn_db=TinyDB(self._cohn_db_path, indent=4),
            gopro=self,
            loop=self._loop,
            cohn_credentials=self._cohn_credentials,
        )
        self._access_point = open_gopro.features.AccessPointFeature(self, self._loop)
        self._streaming = open_gopro.features.StreamFeature(self, self._loop)

        # If we are to perform BLE housekeeping
        if self._should_maintain_state:
            self._ready_lock = _ReadyLock()
            self._keep_alive_task = asyncio.create_task(self._periodic_keep_alive())
            self._encoding = True
            self._busy = True
            self._encoding_started = asyncio.Event()

        RETRIES = 5
        for retry in range(RETRIES):
            try:
                if self._should_enable_ble:
                    await self._open_ble(timeout, retries)

                    # TODO need to handle sending these if BLE does not exist
                    await self.ble_command.set_third_party_client_info()
                    # Set current dst-aware time. Don't assert on success since some old cameras don't support this command.
                    dt, tz_offset, is_dst = get_current_dst_aware_time()
                    await self.ble_command.set_date_time_tz_dst(date_time=dt, tz_offset=tz_offset, is_dst=is_dst)

                    # Find and configure API version
                    version = (await self.ble_command.get_open_gopro_api_version()).data
                    if version != self.version:
                        raise InvalidOpenGoProVersion(version)
                    logger.info(f"Using Open GoPro API version {version}")

                    await self.cohn.wait_for_ready()

                # Establish Wifi / COHN connection if desired
                if self._should_enable_wifi:
                    await self._open_wifi(timeout, retries)
                elif self._should_enable_cohn:
                    # TODO DNS scan?
                    if await self.cohn.is_configured:
                        self._is_cohn_configured = True
                    else:
                        logger.warning("COHN needs to be configured.")

                # We need at least one connection to continue
                if not self.is_ble_connected and not self.is_http_connected:
                    raise InterfaceConfigFailure("No connections were established.")
                if not self.is_ble_connected and self._should_maintain_state:
                    logger.warning("Can not maintain state without BLE")
                    self._should_maintain_state = False
                self._open = True
                return

            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(f"Error while opening: {repr(e)}")
                traceback.print_exc()
                await self.close()
                if retry >= RETRIES - 1:
                    raise e

    async def close(self) -> None:
        """Safely stop the GoPro instance.

        This will disconnect BLE and WiFI if applicable.

        If not using the context manager, it is mandatory to call this before exiting the program in order to
        prevent reconnection issues because the OS has never disconnected from the previous session.
        """
        await self._close_wifi()
        await self._close_ble()
        try:
            for feature in [self.cohn, self.access_point, self.streaming]:
                try:
                    await feature.close()
                # TODO this should be a specific exception...or removed.
                except Exception as e:  # pylint: disable=broad-exception-caught
                    logger.error(f"Error while closing {feature}: {repr(e)}")
        except AttributeError:
            # This is possible if the GoPro was never opened
            pass
        self._open = False

    def register_update(self, callback: UpdateCb, update: UpdateType) -> None:
        """Register for callbacks when an update occurs

        Args:
            callback (UpdateCb): callback to be notified in
            update (UpdateType): update to register for
        """
        return self._register_update(callback, update)

    def _register_update(self, callback: UpdateCb, update: GoProBle._CompositeRegisterType | UpdateType) -> None:
        """Common register method for both public UpdateType and "protected" internal register type

        Args:
            callback (UpdateCb): callback to register
            update (GoProBle._CompositeRegisterType | UpdateType): update type to register for
        """
        self._listeners[update].add(callback)

    def unregister_update(self, callback: UpdateCb, update: UpdateType | None = None) -> None:
        """Unregister for asynchronous update(s)

        Args:
            callback (UpdateCb): callback to stop receiving update(s) on
            update (UpdateType | None): updates to unsubscribe for. Defaults to None (all
                updates that use this callback will be unsubscribed).
        """
        return self._unregister_update(callback, update)

    def _unregister_update(
        self, callback: UpdateCb, update: GoProBle._CompositeRegisterType | UpdateType | None = None
    ) -> None:
        """Common unregister method for both public UpdateType and "protected" internal register type

        Args:
            callback (UpdateCb): callback to unregister
            update (GoProBle._CompositeRegisterType | UpdateType | None): Update type to unregister for. Defaults to
                    None which will unregister the callback for all update types.
        """
        if update:
            try:
                self._listeners.get(update, set()).remove(callback)
            except KeyError:
                # This is possible if, for example, the register occurred with register and the unregister is now an
                # individual setting / status
                return
        else:
            # If update was not specified, remove all uses of callback
            for key in dict(self._listeners).keys():
                try:
                    self._listeners[key].remove(callback)
                except KeyError:
                    continue

    @property
    def is_open(self) -> bool:
        """Is this client ready for communication?

        Returns:
            bool: True if yes, False if no
        """
        return self._open

    @property
    async def is_ready(self) -> bool:
        """Is gopro ready to receive commands

        Returns:
            bool: yes if ready, no otherwise
        """
        return not (self._busy or self._encoding)

    ##########################################################################################################
    #### Abstracted commands

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    async def keep_alive(self) -> bool:
        """Send a heartbeat to prevent the BLE connection from dropping.

        This is sent automatically by the GoPro instance if its `maintain_ble` argument is not False.

        Returns:
            bool: True if it succeeded,. False otherwise

        """
        return (await self.ble_setting.led.set(66)).ok  # type: ignore

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    async def _enforce_message_rules(
        self, wrapped: Callable, message: Message, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        """Enforce rules around message sending"""
        if self._should_maintain_state and self.is_open and not rules.is_fastpass(**kwargs):
            logger.trace("Rule enforcer acquiring lock")  # type: ignore
            async with self._ready_lock as lock:
                lock.owner = _ReadyLock._LockOwner.RULE_ENFORCER
                logger.trace("Rule enforcer acquired lock")  # type: ignore
                response = await wrapped(message, **kwargs)
            logger.trace("Rule enforcer released lock")  # type: ignore
        else:
            response = await wrapped(message, **kwargs)

        # Handle post-response actions
        if self._should_maintain_state and rules.should_wait_for_encoding_start(**kwargs):
            await self._encoding_started.wait()
            self._encoding_started.clear()

        return response

    async def _notify_listeners(self, update: UpdateType, value: Any) -> None:
        """Notify all registered listeners of this update

        Args:
            update (UpdateType): update to notify
            value (Any): value to notify
        """
        listeners: set[UpdateCb] = set()
        # check individual updates
        for listener in self._listeners.get(update, []):
            listeners.add(listener)
        # Now check our internal composite updates
        match update:
            case StatusId():
                for listener in self._listeners.get(GoProBle._CompositeRegisterType.ALL_STATUSES, []):
                    listeners.add(listener)
            case SettingId():
                for listener in self._listeners.get(GoProBle._CompositeRegisterType.ALL_SETTINGS, []):
                    listeners.add(listener)
        for listener in listeners:
            await listener(update, value)

    async def _periodic_keep_alive(self) -> None:
        """Task to periodically send the keep alive message via BLE."""
        while True:
            if self.is_ble_connected:
                if not await self.keep_alive():
                    logger.error("Failed to send keep alive")
            await asyncio.sleep(self._keep_alive_interval)

    async def _open_ble(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect the instance to a device via BLE.

        Raises:
            InterfaceConfigFailure: failed to get identifier from BLE client

        Args:
            timeout (int): Time in seconds before considering establishment failed. Defaults to 10 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 5.
        """
        # Establish connection, pair, etc.
        await self._ble.open(timeout, retries)
        self._is_ble_connected = True
        if not self._ble.identifier:
            raise InterfaceConfigFailure("Failed to get identifier from BLE client")
        self._identifier = self._ble.identifier[-4:]

        # Start state maintenance
        if self._should_maintain_state:
            logger.trace("State manager initially acquiring lock")  # type: ignore
            await self._ready_lock.acquire(_ReadyLock._LockOwner.STATE_MANAGER)
            logger.trace("State manager initially acquired lock")  # type: ignore

            self._ble_disconnect_event.clear()

            async def _handle_encoding(observable: GoProObservable) -> None:
                async for encoding_status in observable.observe(debug_id=StatusId.ENCODING.name):
                    asyncio.create_task(self._update_internal_state(StatusId.ENCODING, encoding_status))

            async def _handle_busy(observable: GoProObservable) -> None:
                async for busy_status in observable.observe(debug_id=StatusId.BUSY.name):
                    asyncio.create_task(self._update_internal_state(StatusId.BUSY, busy_status))

            self._status_tasks.append(
                asyncio.create_task(_handle_encoding((await self.ble_status.encoding.get_value_observable()).unwrap()))
            )
            self._status_tasks.append(
                asyncio.create_task(_handle_busy((await self.ble_status.busy.get_value_observable()).unwrap()))
            )
        logger.info("BLE is ready!")

    async def _update_internal_state(self, update: UpdateType, value: int) -> None:
        """Update internal state based on camera status changes"""
        # Clean up pending tasks
        logger.trace(f"Received internal state update {update}: {value}")  # type: ignore
        for task in self._state_acquire_lock_tasks:
            task.cancel()
        self._state_acquire_lock_tasks.clear()

        # Update state variables
        previous_ready = await self.is_ready
        encoding_started = False
        if update == StatusId.ENCODING:
            encoding_started = not self._encoding and bool(value)
            self._encoding = bool(value)
        elif update == StatusId.BUSY:
            self._busy = bool(value)
        current_ready = await self.is_ready
        logger.trace(f"Current state: {self._encoding=}, {self._busy=}, {current_ready=}")  # type: ignore

        # Handle lock state transitions based on camera readiness
        if self._ready_lock.owner == _ReadyLock._LockOwner.STATE_MANAGER:
            if current_ready and not previous_ready:
                # Camera became ready, release lock
                self._ready_lock.release()
        elif not current_ready and self._ready_lock.owner != _ReadyLock._LockOwner.STATE_MANAGER:
            # Camera became busy, acquire lock
            try:
                task = asyncio.create_task(self._ready_lock.acquire(_ReadyLock._LockOwner.STATE_MANAGER))
                self._state_acquire_lock_tasks.append(task)
                await task
            except asyncio.CancelledError:
                pass

        # Notify encoding started if applicable
        if encoding_started and self.is_open:
            self._encoding_started.set()

    async def _route_response(self, response: GoProResp) -> None:
        """After parsing response, route it to any stakeholders (such as registered listeners)

        Args:
            response (GoProResp): parsed response to route
        """
        original_response = deepcopy(response)
        # We only support queries for either one ID or all ID's. If this is an individual query, extract the value
        # for cleaner response data
        if response._is_query and not response._is_push and len(response.data) == 1:
            response.data = list(response.data.values())[0]

        # Check if this is the awaited synchronous response (id matches). Note! these have to come in order.
        if await self._sync_resp_wait_q.peek_front() == response.identifier:
            logger.info(Logger.build_log_rx_str(original_response, asynchronous=False))
            # Dequeue it and put this on the ready queue
            await self._sync_resp_wait_q.get()
            await self._sync_resp_ready_q.put(response)
        # If this wasn't the awaited synchronous response...
        else:
            logger.info(Logger.build_log_rx_str(original_response, asynchronous=True))
        if response._is_push:
            for update_id, value in response.data.items():
                await self._notify_listeners(update_id, value)
        elif isinstance(response.identifier, ActionId):
            await self._notify_listeners(response.identifier, response.data)

    def _notification_handler(self, handle: int, data: bytearray) -> None:
        """Receive notifications from the BLE controller.

        Args:
            handle (int): Attribute handle that notification was received on.
            data (bytearray): Bytestream that was received.
        """

        async def _async_notification_handler() -> None:
            # Responses we don't care about. For now, just the BLE-spec defined battery characteristic
            if (uuid := self._ble.gatt_db.handle2uuid(handle)) == GoProUUID.BATT_LEVEL:
                return
            logger.debug(f'Received response on BleUUID [{uuid}]: {data.hex(":")}')
            # Add to response dict if not already there
            if uuid not in self._active_builders:
                builder = BleRespBuilder()
                builder.set_uuid(uuid)
                self._active_builders[uuid] = builder
            # Accumulate the packet
            self._active_builders[uuid].accumulate(data)
            if (builder := self._active_builders[uuid]).is_finished_accumulating:
                # Clear active response from response dict
                del self._active_builders[uuid]
                await self._route_response(builder.build())

        asyncio.run_coroutine_threadsafe(_async_notification_handler(), self._loop)

    async def _close_ble(self) -> None:
        """Terminate BLE connection if it is connected"""
        if self._should_maintain_state:
            self._keep_alive_task.cancel()
            for task in [*self._status_tasks, *self._state_acquire_lock_tasks]:
                task.cancel()
        if self.is_ble_connected and self._ble is not None:
            await self._ble.close()
            await self._ble_disconnect_event.wait()

    def _disconnect_handler(self, _: Any) -> None:
        """Disconnect callback from BLE controller

        Raises:
            ConnectionTerminated: We entered this callback in an unexpected state.
        """
        self._is_ble_connected = False
        if self._ble_disconnect_event.is_set():
            raise ConnectionTerminated("BLE connection terminated unexpectedly.")
        self._ble_disconnect_event.set()

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    @enforce_message_rules
    async def _send_ble_message(
        self, message: BleMessage, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        # Store information on the response we are expecting
        await self._sync_resp_wait_q.put(message._identifier)
        logger.info(Logger.build_log_tx_str(pretty_print(message._as_dict(**kwargs))))

        # Fragment data and write it
        for packet in self._fragment(message._build_data(**kwargs)):
            logger.debug(f"Writing to [{message._uuid.name}] UUID: {packet.hex(':')}")
            await self._ble.write(message._uuid, packet)

        # Wait to be notified that response was received
        try:
            response = await asyncio.wait_for(self._sync_resp_ready_q.get(), WirelessGoPro.WRITE_TIMEOUT)
        except asyncio.TimeoutError as e:
            logger.error(
                f"Response timeout of {WirelessGoPro.WRITE_TIMEOUT} seconds when sending {message._identifier}!"
            )
            raise ResponseTimeout(WirelessGoPro.WRITE_TIMEOUT) from e
        except queue.Empty as e:
            logger.error(
                f"Response timeout of {WirelessGoPro.WRITE_TIMEOUT} seconds when sending {message._identifier}!"
            )
            raise ResponseTimeout(WirelessGoPro.WRITE_TIMEOUT) from e

        # Check status
        if not response.ok:
            logger.warning(f"Received non-success status: {response.status}")

        return response

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    @enforce_message_rules
    async def _read_ble_characteristic(
        self, message: BleMessage, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        received_data = await self._ble.read(message._uuid)
        logger.debug(f"Reading from {message._uuid.name}")
        builder = BleRespBuilder()
        builder.set_uuid(message._uuid)
        builder.set_packet(received_data)
        return builder.build()

    def _handle_cohn(self, message: HttpMessage) -> HttpMessage:
        """Prepend COHN headers if COHN is provisioned

        Args:
            message (HttpMessage): HTTP message to append headers to

        Returns:
            HttpMessage: potentially modified HTTP message
        """
        try:
            if self._should_enable_cohn and self.cohn.credentials:
                message._headers["Authorization"] = self.cohn.credentials.auth_token
                message._certificate = self.cohn.credentials.certificate_as_path
            return message
        except GoProNotOpened:
            return message

    async def _get_json(self, message: HttpMessage, *args: Any, **kwargs: Any) -> GoProResp:
        message = self._handle_cohn(message)
        return await super()._get_json(*args, message=message, **kwargs)

    async def _get_stream(self, message: HttpMessage, *args: Any, **kwargs: Any) -> GoProResp:
        message = self._handle_cohn(message)
        return await super()._get_stream(*args, message=message, **kwargs)

    async def _put_json(self, message: HttpMessage, *args: Any, **kwargs: Any) -> GoProResp:
        message = self._handle_cohn(message)
        return await super()._put_json(*args, message=message, **kwargs)

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    async def _open_wifi(self, timeout: int = 30, retries: int = 5) -> None:
        """Connect to a GoPro device via Wifi.

        Args:
            timeout (int): Time before considering establishment failed. Defaults to 10 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 5.

        Raises:
            ConnectFailed: Was not able to establish the Wifi Connection
        """
        logger.info("Discovering Wifi AP info and enabling via BLE")
        password = (await self.ble_command.get_wifi_password()).data
        ssid = (await self.ble_command.get_wifi_ssid()).data
        for retry in range(1, retries):
            try:
                assert (await self.ble_command.enable_wifi_ap(enable=True)).ok

                async def _wait_for_camera_wifi_ready() -> None:
                    logger.debug("Waiting for camera wifi ready status")
                    while not (await self.ble_status.ap_mode.get_value()).data:
                        await asyncio.sleep(0.200)

                await asyncio.wait_for(_wait_for_camera_wifi_ready(), 5)
                await self._wifi.open(ssid, password, timeout, 1)
                break
            except ConnectFailed:
                logger.warning(f"Wifi connection failed. Retrying #{retry}")
                # In case camera Wifi is in strange disable, reset it
                assert (await self.ble_command.enable_wifi_ap(enable=False)).ok
        else:
            raise ConnectFailed("Wifi Connection failed", timeout, retries)

    async def _close_wifi(self) -> None:
        """Terminate the Wifi connection."""
        if hasattr(self, "_wifi"):  # Corner case where instantiation fails before superclass is initialized
            await self._wifi.close()

    @property
    def ip_address(self) -> str:  # noqa: D102
        return self.cohn.credentials.ip_address if self._should_enable_cohn and self.cohn.credentials else "10.5.5.9"

    @property
    def _base_url(self) -> str:
        return (
            f"https://{self.ip_address}:8080/"
            if self._should_enable_cohn and self.cohn.credentials
            else f"http://{self.ip_address}/"
        )

    @property
    def _requests_session(self) -> requests.Session:
        return (
            create_less_strict_requests_session(self.cohn.credentials.certificate_as_path)
            if self._should_enable_cohn and self.cohn.credentials
            else requests.Session()
        )

    @property
    def _api(self) -> WirelessApi:
        return self._wireless_api
