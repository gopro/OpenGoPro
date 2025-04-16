# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations

import asyncio
import enum
import logging
import queue
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Final

# These are imported this way for monkeypatching in pytest
import open_gopro.features.access_point
import open_gopro.features.cohn
from open_gopro import proto
from open_gopro.api import (
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    WirelessApi,
)
from open_gopro.ble import BleakWrapperController, BleUUID
from open_gopro.ble.controller import BLEController
from open_gopro.communicator_interface import (
    BleMessage,
    GoProBle,
    GoProWirelessInterface,
    HttpMessage,
    Message,
    MessageRules,
)
from open_gopro.constants import ActionId, GoProUUID, StatusId
from open_gopro.constants.settings import SettingId
from open_gopro.exceptions import (
    ConnectFailed,
    ConnectionTerminated,
    GoProNotOpened,
    InterfaceConfigFailure,
    InvalidOpenGoProVersion,
    ResponseTimeout,
)
from open_gopro.gopro_base import (
    GoProBase,
    GoProMessageInterface,
    enforce_message_rules,
)
from open_gopro.logger import Logger
from open_gopro.models.general import CohnInfo
from open_gopro.models.response import BleRespBuilder, GoProResp
from open_gopro.types import ResponseType, UpdateCb, UpdateType
from open_gopro.util import SnapshotQueue, get_current_dst_aware_time, pretty_print
from open_gopro.wifi import WifiCli
from open_gopro.wifi.controller import WifiController

logger = logging.getLogger(__name__)


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

    It will also do some synchronization, etc:

    - ensuring camera is ready / not encoding before transferring data
    - sending keep alive signal periodically

    If no target arg is passed in, the first discovered BLE GoPro device will be connected to.

    It can be used via context manager:

    >>> async with WirelessGoPro() as gopro:
    >>>     # Send some messages now

    Or without:

    >>> gopro = WirelessGoPro()
    >>> await gopro.open()
    >>> # Send some messages now

    Attributes:
        WRITE_TIMEOUT (Final[int]): BLE Write Timeout. Not configurable.

    Args:
        target (Pattern | None): A regex to search for the target GoPro's name. For example, "GoPro 0456").
            Defaults to None (i.e. connect to first discovered GoPro)
        wifi_interface (str | None): Set to specify the wifi interface the local machine will use to connect
            to the GoPro. If None (or not set), first discovered interface will be used.
        sudo_password (str | None): User password for sudo. If not passed, you will be prompted if a password
            is needed which should only happen on Nix systems.
        enable_wifi (bool): Optionally do not enable Wifi if set to False. Defaults to True.
        **kwargs (Any): additional parameters for internal use / testing

    Raises:
        InterfaceConfigFailure: In order to communicate via Wifi, there must be an available
            Wifi Interface. By default during initialization, the Wifi driver will attempt to automatically
            discover such an interface. If it does not find any, it will raise this exception. Note that
            the interface can also be specified manually with the 'wifi_interface' argument.
    """

    WRITE_TIMEOUT: Final[int] = 5

    class _LockOwner(enum.Enum):
        """Current owner of the communication lock"""

        RULE_ENFORCER = enum.auto()
        STATE_MANAGER = enum.auto()

    class Interface(enum.Enum):
        BLE = enum.auto()
        WIFI_AP = enum.auto()
        COHN = enum.auto()  # WIFI_STA

    def __init__(
        self,
        target: str | None = None,
        host_wifi_interface: str | None = None,
        host_sudo_password: str | None = None,
        cohn_credentials: CohnInfo | None = None,
        cohn_db: Path = Path("cohn_db.json"),
        interfaces: set[WirelessGoPro.Interface] = {Interface.BLE, Interface.WIFI_AP},
        **kwargs: Any,
    ) -> None:
        GoProBase.__init__(self, **kwargs)
        # Store initialization information
        self._should_enable_wifi = WirelessGoPro.Interface.WIFI_AP in interfaces
        self._should_enable_ble = WirelessGoPro.Interface.BLE in interfaces
        self._should_enable_cohn = WirelessGoPro.Interface.COHN in interfaces
        self._cohn_db_path = cohn_db
        self._cohn_credentials = cohn_credentials

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
        self._cohn: open_gopro.features.cohn.CohnFeature
        self._access_point: open_gopro.features.access_point.AccessPointFeature

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
            self._state_tasks: list[asyncio.Task] = []
            self._lock_owner: WirelessGoPro._LockOwner | None = WirelessGoPro._LockOwner.STATE_MANAGER
            self._ready_lock: asyncio.Lock
            self._keep_alive_task: asyncio.Task
            self._encoding: bool
            self._busy: bool
            self._encoding_started: asyncio.Event

    @property
    def cohn(self) -> open_gopro.features.cohn.CohnFeature:
        try:
            return self._cohn
        except AttributeError:
            raise GoProNotOpened("")

    @property
    def access_point(self) -> open_gopro.features.access_point.AccessPointFeature:
        try:
            return self._access_point
        except AttributeError:
            raise GoProNotOpened("")

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
        if not self._identifier:
            raise RuntimeError("Identifier not yet set")
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

        Returns:
            bool: True if yes, False if no
        """
        return self.cohn.is_ready or self._wifi.is_connected

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

        Args:
            timeout (int): How long to wait for each connection before timing out. Defaults to 10.
            retries (int): How many connection attempts before considering connection failed. Defaults to 5.
        """
        # Set up concurrency
        self._loop = asyncio.get_running_loop()
        self._ble_disconnect_event = asyncio.Event()

        self._cohn = open_gopro.features.cohn.CohnFeature(self._cohn_db_path, self, self._loop, self._cohn_credentials)
        self._access_point = open_gopro.features.access_point.AccessPointFeature(self, self._loop)

        # If we are to perform BLE housekeeping
        if self._should_maintain_state:
            self._ready_lock = asyncio.Lock()
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
                    await self.ble_command.set_date_time_tz_dst(
                        **dict(zip(("date_time", "tz_offset", "is_dst"), get_current_dst_aware_time()))
                    )

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
                    if not await self.cohn.is_configured:
                        logger.warning("COHN needs to be configured.")
                else:
                    # Otherwise, turn off Wifi
                    logger.info("Turning off the camera's Wifi radio")
                    await self.ble_command.enable_wifi_ap(enable=False)

                # We need at least one connection to continue
                if not self.is_ble_connected and not self.is_http_connected:
                    raise InterfaceConfigFailure("No connections were established.")
                self._open = True
                return

            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(f"Error while opening: {e}")
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
            update (GoProBle._CompositeRegisterType | UpdateType | None, optional): Update type to unregister for. Defaults to
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
        # Acquire ready lock unless we are initializing or this is a Set Shutter Off command
        if self._should_maintain_state and self.is_open and not rules.is_fastpass(**kwargs):
            logger.trace(f"{wrapped.__name__} acquiring lock")  # type: ignore
            await self._ready_lock.acquire()
            logger.trace(f"{wrapped.__name__} has the lock")  # type: ignore
            self._lock_owner = WirelessGoPro._LockOwner.RULE_ENFORCER
            response = await wrapped(message, **kwargs)
        else:  # Either we're not maintaining state, we're not opened yet, or this is a fastpass message
            response = await wrapped(message, **kwargs)

        # Release the lock if we acquired it
        if self._should_maintain_state:
            if self._lock_owner is WirelessGoPro._LockOwner.RULE_ENFORCER:
                logger.trace(f"{wrapped.__name__} releasing the lock")  # type: ignore
                self._lock_owner = None
                self._ready_lock.release()
                logger.trace(f"{wrapped.__name__} released the lock")  # type: ignore
            # Is there any special handling required after receiving the response?
            if rules.should_wait_for_encoding_start(**kwargs):
                logger.trace("Waiting to receive encoding started.")  # type: ignore
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

        Args:
            timeout (int): Time in seconds before considering establishment failed. Defaults to 10 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 5.
        """
        # Establish connection, pair, etc.
        await self._ble.open(timeout, retries)
        self._is_ble_connected = True
        # Start state maintenance
        if self._should_maintain_state:
            self._ble_disconnect_event.clear()
            await self._ready_lock.acquire()
            encoding = (await self.ble_status.encoding.register_value_update(self._update_internal_state)).data
            await self._update_internal_state(StatusId.ENCODING, encoding)
            busy = (await self.ble_status.busy.register_value_update(self._update_internal_state)).data
            await self._update_internal_state(StatusId.BUSY, busy)
        logger.info("BLE is ready!")

    async def _update_internal_state(self, update: UpdateType, value: int) -> None:
        """Update the internal state based on a status update.

        # Note!!! This needs to be reentrant-safe

        Used to update encoding and / or busy status

        Args:
            update (UpdateType): type of update (status ID)
            value (int): updated value
        """
        # Cancel any currently pending state update tasks
        for task in self._state_tasks:
            logger.trace("Cancelling pending acquire task.")  # type: ignore
            task.cancel()
        self._state_tasks = []

        logger.trace(f"State update received {update.name} ==> {value}")  # type: ignore
        should_notify_encoding = False
        if update == StatusId.ENCODING:
            self._encoding = bool(value)
            if self._encoding:
                should_notify_encoding = True
        elif update == StatusId.BUSY:
            self._busy = bool(value)
        logger.trace(f"Current internal states: {self._encoding=} {self._busy=}")  # type: ignore

        if self._lock_owner is WirelessGoPro._LockOwner.STATE_MANAGER and await self.is_ready:
            logger.trace("Control releasing lock")  # type: ignore
            self._lock_owner = None
            self._ready_lock.release()
            logger.trace("Control released lock")  # type: ignore
        elif not (self._lock_owner is WirelessGoPro._LockOwner.STATE_MANAGER) and not await self.is_ready:
            logger.trace("Control acquiring lock")  # type: ignore
            task = asyncio.create_task(self._ready_lock.acquire())
            self._state_tasks.append(task)
            await task
            logger.trace("Control has lock")  # type: ignore
            self._lock_owner = WirelessGoPro._LockOwner.STATE_MANAGER

        if should_notify_encoding and self.is_open:
            logger.trace("Control setting encoded started")  # type: ignore
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
                logger.trace(f"Finished accumulating on {uuid}")  # type: ignore
                # Clear active response from response dict
                del self._active_builders[uuid]
                await self._route_response(builder.build())

        asyncio.run_coroutine_threadsafe(_async_notification_handler(), self._loop)

    async def _close_ble(self) -> None:
        """Terminate BLE connection if it is connected"""
        if self._should_maintain_state:
            self._keep_alive_task.cancel()
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
        except queue.Empty as e:
            logger.error(f"Response timeout of {WirelessGoPro.WRITE_TIMEOUT} seconds!")
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

    # TODO make decorator?
    def _handle_cohn(self, message: HttpMessage) -> HttpMessage:
        """Prepend COHN headers if COHN is provisioned

        Args:
            message (HttpMessage): HTTP message to append headers to

        Returns:
            HttpMessage: potentially modified HTTP message
        """
        try:
            if self.cohn.credentials:
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
        if self.is_ble_connected:
            try:
                await self.ble_command.enable_wifi_ap(enable=False)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning(f"Error closing wifi: {repr(e)}")

    @property
    def _base_url(self) -> str:
        try:
            return f"https://{self.cohn.credentials.ip_address}/" if self.cohn.credentials else "http://10.5.5.9:8080/"
        except GoProNotOpened:
            return "http://10.5.5.9:8080/"

    @property
    def _api(self) -> WirelessApi:
        return self._wireless_api
