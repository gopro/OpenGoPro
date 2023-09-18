# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations

import asyncio
import logging
import queue
from collections import defaultdict
from pathlib import Path
from typing import Any, Final, Pattern

import wrapt

import open_gopro.exceptions as GpException
from open_gopro import proto, types
from open_gopro.api import (
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    Params,
    WirelessApi,
)
from open_gopro.ble import BleakWrapperController, BleUUID
from open_gopro.communicator_interface import GoProWirelessInterface, MessageRules
from open_gopro.constants import ActionId, GoProUUIDs, StatusId
from open_gopro.gopro_base import GoProBase, GoProMessageInterface, MessageMethodType
from open_gopro.logger import Logger
from open_gopro.models.response import BleRespBuilder, GoProResp
from open_gopro.parser_interface import Parser
from open_gopro.util import SnapshotQueue, get_current_dst_aware_time
from open_gopro.wifi import WifiCli

logger = logging.getLogger(__name__)

KEEP_ALIVE_INTERVAL: Final = 28


@wrapt.decorator
async def enforce_message_rules(
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
        await instance._ready_lock.acquire()
        logger.trace(f"{wrapped.__name__} has the lock")  # type: ignore
        have_lock = True
        response = await wrapped(*args, **kwargs)
    else:  # Either we're not maintaining state, we're not opened yet, or this is a fastpass message
        response = await wrapped(*args, **kwargs)

    # Release the lock if we acquired it
    if instance._should_maintain_state:
        if have_lock:
            instance._ready_lock.release()
            logger.trace(f"{wrapped.__name__} released the lock")  # type: ignore
        # Is there any special handling required after receiving the response?
        if MessageRules.WAIT_FOR_ENCODING_START in rules:
            logger.trace("Waiting to receive encoding started.")  # type: ignore
            await instance._encoding_started.wait()
            instance._encoding_started.clear()
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
    >>>     print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
    >>>     # Send some messages now

    Or without:

    >>> gopro = WirelessGoPro()
    >>> await gopro.open()
    >>> print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
    >>> # Send some messages now

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

    WRITE_TIMEOUT: Final = 5

    def __init__(
        self,
        target: Pattern | None = None,
        wifi_interface: str | None = None,
        sudo_password: str | None = None,
        enable_wifi: bool = True,
        **kwargs: Any,
    ) -> None:
        GoProBase.__init__(self, **kwargs)
        # Store initialization information
        self._should_enable_wifi = enable_wifi
        ble_adapter = kwargs.get("ble_adapter", BleakWrapperController)
        wifi_adapter = kwargs.get("wifi_adapter", WifiCli)
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

        # Builders for currently accumulating synchronous responses, indexed by GoProUUIDs. This assumes there
        # can only be one active response per BleUUID
        self._active_builders: dict[BleUUID, BleRespBuilder] = {}
        # Responses that we are waiting for.
        self._sync_resp_wait_q: SnapshotQueue[types.ResponseType] = SnapshotQueue()
        # Synchronous response that has been parsed and are ready for their sender to receive as the response.
        self._sync_resp_ready_q: SnapshotQueue[types.ResponseType] = SnapshotQueue()

        self._listeners: dict[types.UpdateType, set[types.UpdateCb]] = defaultdict(set)

        # TO be set up when opening in async context
        self._loop: asyncio.AbstractEventLoop
        self._open = False
        self._ble_disconnect_event: asyncio.Event

        if self._should_maintain_state:
            self._ready_lock: asyncio.Lock
            self._keep_alive_task: asyncio.Task
            self._encoding: bool
            self._busy: bool
            self._encoding_started: asyncio.Event

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
        try:
            return self._wifi.is_connected
        except AttributeError:
            return False

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

    async def open(self, timeout: int = 10, retries: int = 5) -> None:
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
        self._open = False
        self._ble_disconnect_event = asyncio.Event()

        # If we are to perform BLE housekeeping
        if self._should_maintain_state:
            self._ready_lock = asyncio.Lock()
            self._keep_alive_task = asyncio.create_task(self._periodic_keep_alive())
            self._encoding = True
            self._busy = True
            self._encoding_started = asyncio.Event()

        try:
            await self._open_ble(timeout, retries)

            # Set current dst-aware time
            assert (
                await self.ble_command.set_date_time_tz_dst(
                    **dict(zip(("date_time", "tz_offset", "is_dst"), get_current_dst_aware_time()))
                )
            ).ok

            # Find and configure API version
            version = (await self.ble_command.get_open_gopro_api_version()).data
            if version != self.version:
                raise GpException.InvalidOpenGoProVersion(version)
            logger.info(f"Using Open GoPro API version {version}")

            # Establish Wifi connection if desired
            if self._should_enable_wifi:
                await self._open_wifi(timeout, retries)
            else:
                # Otherwise, turn off Wifi
                logger.info("Turning off the camera's Wifi radio")
                await self.ble_command.enable_wifi_ap(enable=False)
            self._open = True

        except Exception as e:
            logger.error(f"Error while opening: {e}")
            await self.close()
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

    def register_update(self, callback: types.UpdateCb, update: types.UpdateType) -> None:
        """Register for callbacks when an update occurs

        Args:
            callback (types.UpdateCb): callback to be notified in
            update (types.UpdateType): update to register for
        """
        self._listeners[update].add(callback)

    def unregister_update(self, callback: types.UpdateCb, update: types.UpdateType | None = None) -> None:
        """Unregister for asynchronous update(s)

        Args:
            callback (types.UpdateCb): callback to stop receiving update(s) on
            update (types.UpdateType | None): updates to unsubscribe for. Defaults to None (all
                updates that use this callback will be unsubscribed).
        """
        if update:
            self._listeners.get(update, set()).remove(callback)
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

    # TODO move these into delegate / mixin?

    # TODO message rules are a mess here. Since these send other commands that need message rules, we deadlock
    # if we try to apply message rules to these

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    async def keep_alive(self) -> bool:
        """Send a heartbeat to prevent the BLE connection from dropping.

        This is sent automatically by the GoPro instance if its `maintain_ble` argument is not False.

        Returns:
            bool: True if it succeeded,. False otherwise
        """
        return (await self.ble_setting.led.set(Params.LED.BLE_KEEP_ALIVE)).ok

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    async def connect_to_access_point(self, ssid: str, password: str) -> bool:
        """Connect the camera to a Wifi Access Point

        Args:
            ssid (str): SSID of AP
            password (str): password of AP

        Returns:
            bool: True if AP is currently connected, False otherwise
        """
        scan_result: asyncio.Queue[proto.NotifStartScanning] = asyncio.Queue()
        provisioned_result: asyncio.Queue[proto.NotifProvisioningState] = asyncio.Queue()

        async def wait_for_scan(_: Any, result: proto.NotifStartScanning) -> None:
            await scan_result.put(result)

        async def wait_for_provisioning(_: Any, result: proto.NotifProvisioningState) -> None:
            await provisioned_result.put(result)

        # Wait to receive scanning success
        logger.info("Scanning for Wifi networks")
        self.register_update(wait_for_scan, ActionId.NOTIF_START_SCAN)
        await self.ble_command.scan_wifi_networks()
        if (sresult := await scan_result.get()).scanning_state != proto.EnumScanning.SCANNING_SUCCESS:
            logger.error(f"Scan failed: {str(sresult.scanning_state)}")
            return False
        scan_id = sresult.scan_id
        self.unregister_update(wait_for_scan)

        # Get scan results and see if we need to provision
        for entry in (await self.ble_command.get_ap_entries(scan_id=scan_id)).data.entries:
            if entry.ssid == ssid:
                self.register_update(wait_for_provisioning, ActionId.NOTIF_PROVIS_STATE)
                # Are we already provisioned?
                if entry.scan_entry_flags & proto.EnumScanEntryFlags.SCAN_FLAG_CONFIGURED:
                    logger.info(f"Connecting to already provisioned network {ssid}...")
                    await self.ble_command.request_wifi_connect(ssid=ssid)
                else:
                    logger.info(f"Provisioning new network {ssid}...")
                    await self.ble_command.request_wifi_connect_new(ssid=ssid, password=password)
                if (
                    presult := (await provisioned_result.get())
                ).provisioning_state != proto.EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP:
                    logger.error(f"Provision failed: {str(presult.provisioning_state)}")
                    return False
                self.unregister_update(wait_for_provisioning)
                return True
        return False

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    async def _notify_listeners(self, update: types.UpdateType, value: Any) -> None:
        """Notify all registered listeners of this update

        Args:
            update (types.UpdateType): update to notify
            value (Any): value to notify
        """
        for listener in self._listeners.get(update, []):
            await listener(update, value)

    async def _periodic_keep_alive(self) -> None:
        """Task to periodically send the keep alive message via BLE."""
        while True:
            await asyncio.sleep(KEEP_ALIVE_INTERVAL)
            if self.is_ble_connected:
                await self.keep_alive()

    async def _open_ble(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect the instance to a device via BLE.

        Args:
            timeout (int): Time in seconds before considering establishment failed. Defaults to 10 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 5.
        """
        # Establish connection, pair, etc.
        await self._ble.open(timeout, retries)
        # Start state maintenance
        if self._should_maintain_state:
            await self._ready_lock.acquire()
            encoding = (await self.ble_status.encoding_active.register_value_update(self._update_internal_state)).data
            await self._update_internal_state(StatusId.ENCODING, encoding)
            busy = (await self.ble_status.system_busy.register_value_update(self._update_internal_state)).data
            await self._update_internal_state(StatusId.SYSTEM_BUSY, busy)
        logger.info("BLE is ready!")

    async def _update_internal_state(self, update: types.UpdateType, value: int) -> None:
        """Update the internal state based on a status update.

        Used to update encoding and / or busy status

        Args:
            update (types.UpdateType): type of update (status ID)
            value (int): updated value
        """
        have_lock = not await self.is_ready
        logger.trace(f"State update received {update.name} ==> {value}, current {self._encoding=} {self._busy=}")  # type: ignore
        should_notify_encoding = False
        if update == StatusId.ENCODING:
            self._encoding = bool(value)
            if self._encoding:
                should_notify_encoding = True
        elif update == StatusId.SYSTEM_BUSY:
            self._busy = bool(value)

        ready_now = await self.is_ready
        if have_lock and ready_now:
            self._ready_lock.release()
            logger.trace("Control released lock")  # type: ignore
        elif not have_lock and not ready_now:
            logger.trace("Control acquiring lock")  # type: ignore
            await self._ready_lock.acquire()
            logger.trace("Control has lock")  # type: ignore

        if should_notify_encoding and self.is_open:
            logger.trace("Control setting encoded started")  # type: ignore
            self._encoding_started.set()

    # TODO this needs unit testing
    async def _route_response(self, response: GoProResp) -> None:
        """After parsing response, route it to any stakeholders (such as registered listeners)

        Args:
            response (GoProResp): parsed response
        """
        # Flatten data if possible
        if response._is_query and not response._is_push:
            response.data = list(response.data.values())[0]

        # Check if this is the awaited synchronous response (id matches). Note! these have to come in order.
        response_claimed = False
        if await self._sync_resp_wait_q.peek_front() == response.identifier:
            # Dequeue it and put this on the ready queue
            await self._sync_resp_wait_q.get()
            await self._sync_resp_ready_q.put(response)
            response_claimed = True
        # If this wasn't the awaited synchronous response...
        if not response_claimed:
            logger.info(Logger.build_log_rx_str(response, asynchronous=True))
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
            if (uuid := self._ble.gatt_db.handle2uuid(handle)) == GoProUUIDs.BATT_LEVEL:
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
                response = builder.build()
                # Perform response post-processing tasks
                await self._route_response(response)
                # Clear active response from response dict
                del self._active_builders[uuid]

        asyncio.run_coroutine_threadsafe(_async_notification_handler(), self._loop)

    async def _close_ble(self) -> None:
        """Terminate BLE connection if it is connected"""
        if self.is_ble_connected and self._ble is not None:
            self._ble_disconnect_event.clear()
            if self._should_maintain_state:
                self._keep_alive_task.cancel()
            await self._ble.close()
            await self._ble_disconnect_event.wait()

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
    async def _send_ble_message(
        self, uuid: BleUUID, data: bytearray, response_id: types.ResponseType, **_: Any
    ) -> GoProResp:
        """Write a characteristic and block until its corresponding notification response is received.

        Args:
            uuid (BleUUID): characteristic to write to
            data (bytearray): bytes to write
            response_id (types.ResponseType): identifier to claim parsed response in notification handler
            **_ (Any): not used

        Raises:
            ResponseTimeout: did not receive a response before timing out

        Returns:
            GoProResp: received response
        """
        # Store information on the response we are expecting
        await self._sync_resp_wait_q.put(response_id)

        # Fragment data and write it
        for packet in self._fragment(data):
            logger.debug(f"Writing to [{uuid.name}] UUID: {packet.hex(':')}")
            await self._ble.write(uuid, packet)

        # Wait to be notified that response was received
        try:
            response: GoProResp = await asyncio.wait_for(self._sync_resp_ready_q.get(), WirelessGoPro.WRITE_TIMEOUT)
        except queue.Empty as e:
            logger.error(f"Response timeout of {WirelessGoPro.WRITE_TIMEOUT} seconds!")
            raise GpException.ResponseTimeout(WirelessGoPro.WRITE_TIMEOUT) from e

        # Check status
        if not response.ok:
            logger.warning(f"Received non-success status: {response.status}")

        return response

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    @enforce_message_rules
    async def _read_characteristic(self, uuid: BleUUID) -> GoProResp:
        """Read a characteristic's data by GoProUUIDs.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.command, self.setting, self.ble_status)

        Args:
            uuid (BleUUID): characteristic data to read

        Returns:
            GoProResp: response from UUID read
        """
        received_data = await self._ble.read(uuid)
        logger.debug(f"Reading from {uuid.name}")
        builder = BleRespBuilder()
        builder.set_uuid(uuid)
        builder.set_packet(received_data)
        return builder.build()

    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    async def _open_wifi(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect to a GoPro device via Wifi.

        Args:
            timeout (int): Time before considering establishment failed. Defaults to 15 seconds.
            retries (int): How many tries to reconnect after failures. Defaults to 10.

        Raises:
            ConnectFailed: Was not able to establish the Wifi Connection
        """
        logger.info("Discovering Wifi AP info and enabling via BLE")
        password = (await self.ble_command.get_wifi_password()).data
        ssid = (await self.ble_command.get_wifi_ssid()).data
        for retry in range(1, retries):
            try:
                assert (await self.ble_command.enable_wifi_ap(enable=True)).ok
                self._wifi.open(ssid, password, timeout, 1)
                break
            except GpException.ConnectFailed:
                logger.warning(f"Wifi connection failed. Retrying #{retry}")
                # In case camera Wifi is in strange disable, reset it
                assert (await self.ble_command.enable_wifi_ap(enable=False)).ok
        else:
            raise GpException.ConnectFailed("Wifi Connection failed", timeout, retries)

    async def _close_wifi(self) -> None:
        """Terminate the Wifi connection."""
        if hasattr(self, "_wifi"):  # Corner case where instantiation fails before superclass is initialized
            self._wifi.close()

    @enforce_message_rules
    async def _http_get(
        self,
        url: str,
        parser: Parser | None = None,
        headers: dict | None = None,
        certificate: Path | None = None,
        timeout: int = GoProBase.GET_TIMEOUT,
        **kwargs: Any,
    ) -> GoProResp:
        return await super()._http_get(url, parser, **kwargs)

    @enforce_message_rules
    async def _stream_to_file(self, url: str, file: Path) -> GoProResp[Path]:
        return await super()._stream_to_file(url, file)

    @property
    def _base_url(self) -> str:
        return "http://10.5.5.9:8080/"

    @property
    def _api(self) -> WirelessApi:
        return self._wireless_api
