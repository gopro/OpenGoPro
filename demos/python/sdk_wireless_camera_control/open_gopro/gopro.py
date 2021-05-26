# gopro.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Implements top level interface to GoPro module."""

# TODO make scanning / connect more robust

import re
import csv
import time
import enum
import queue
import asyncio
import logging
import threading
from queue import Queue
from binascii import hexlify
from pathlib import Path
from functools import partial
from typing import Any, Dict, Optional, Pattern, Type, Callable, Generic

import wrapt
import requests

from open_gopro import params
from open_gopro.responses import GoProResp
from open_gopro.constants import CmdId, ErrorCode, UUID, StatusId, QueryCmdId, ProducerType
from open_gopro.ble_commands import BleSettings, BleStatuses, BleCommands, BLECommunicator
from open_gopro.ble_controller import BleakController
from open_gopro.services import AttributeTable, get_gopro_desc
from open_gopro.interfaces import (
    ResponseTimeout,
    ScanFailedToFindDevice,
    ConnectFailed,
    GoProNotInitialized,
    BLEController,
    BleDevice,
    BleClient,
    WifiController,
)
from open_gopro.wifi_commands import WifiCommands, WifiSettings, WifiCommunicator
from open_gopro.wifi_controller import Wireless
from open_gopro.util import SnapshotQueue

logger = logging.getLogger(__name__)

# Send a keep alive minimum every 5 seconds
KEEP_ALIVE_INTERVAL = 60

NUM_THREADS = 3

WRITE_TIMEOUT = 10


class InternalState(enum.IntFlag):
    """State used to manage whether the GoPro instance is ready or not."""

    READY = 0
    ENCODING = 1 << 0
    SYSTEM_BUSY = 1 << 1


@wrapt.decorator
def _ensure_initialized_acquire_ready_semaphore(wrapped, instance, args, kwargs) -> Callable:  # type: ignore
    """If the instance is initialized, acquire the semaphore before doing anything.

    Raises:
        GoProNotInitialized: The function can't be used yet because the GoPro device isn't initialized

    Returns:
        Callable: Function to call after semaphore has been acquired
    """
    if not instance.is_initialized:
        raise GoProNotInitialized
    # Since we're guaranteed to be initialized now, always acquire ready semaphore
    logger.debug(f"{wrapped.__name__} acquiring semaphore")
    with instance.ready:
        logger.debug(f"{wrapped.__name__} has the semaphore")
        ret = wrapped(*args, **kwargs)

    logger.debug(f"{wrapped.__name__} released the semaphore")
    return ret


class GoPro(BLECommunicator, WifiCommunicator, Generic[BleDevice, BleClient]):
    """The top-level BLE and Wifi interface to a GoPro device.

    This will handle for BLE:

    - discovering devices
    - establishing connections
    - discovering GATT characteristics,
    - transferring data

    This will handle for WiFi:

    - finding SSID and password
    - establishing WiFi
    - transferring data

    It will also do some synchronization, etc:

    - ensuring camera is ready / not encoding before transferring data
    - send keep alive periodically

    If no token arg is passed in, the first discovered GoPro device will be connected to.

    It can be used via context manager:

    >>> with GoPro("1234") as gopro:
    >>>     gopro.ble_command.set_shutter(params.Shutter.ON)

    Or without:

    >>> gopro = GoPro("1234")
    >>> gopro.start()
    >>> gopro.ble_command.set_shutter(params.Shutter.ON)

    Args:
        identifier (str, optional): Last 4 of camera name / serial number (i.e. 0456 for GoPro0456). Defaults to None
        ble_adapter (BLEController, optional): Class used to control BLE connection / send data. Defaults to BleakController().
        wifi_adapter (WifiController, optional): Class used to control WiFi connection / send data. Defaults to Wireless().
    """

    base_url = "http://10.5.5.9:8080/"  #: Hard-coded Open GoPro base URL

    def __init__(
        self,
        identifier: Optional[str] = None,
        ble_adapter: Type[BLEController] = BleakController,
        wifi_adapter: Type[WifiController] = Wireless,
    ) -> None:
        # Initialize adapters
        self.ble: BLEController = ble_adapter()
        self.wifi: WifiController = wifi_adapter()

        # Connection information
        self._token: Pattern = re.compile(r"GoPro \d\d\d\d" if identifier is None else f"GoPro {identifier}")
        self.ssid: str
        self.password: str
        self._device: Optional[BleDevice] = None
        self._client: Optional[BleClient] = None
        self.gatt_table: Optional[AttributeTable] = None  #: Attribute storage / access

        # Delegates
        self.ble_command: BleCommands = BleCommands(self)  #: All BLE commands
        self.ble_setting: BleSettings = BleSettings(self)  #: All BLE settings
        self.ble_status: BleStatuses = BleStatuses(self)  #: All BLE statuses
        self.wifi_command: WifiCommands = WifiCommands(self)  #: All Wifi commands
        self.wifi_setting: WifiSettings = WifiSettings(self)  #: All Wifi settings

        # Current accumulating synchronous responses, indexed by UUID. This assumes there can only be one active response per UUID
        self._active_resp: Dict[UUID, GoProResp] = {}
        # Responses that we are waiting for.
        self._sync_resp_wait_q: SnapshotQueue = SnapshotQueue()
        # Synchronous response that has been parsed and are ready for their sender to receive as the response.
        self._sync_resp_ready_q: SnapshotQueue = SnapshotQueue()

        # For outputting asynchronously received information
        self._out_q: "Queue[GoProResp]" = Queue()
        self._listeners: Dict[ProducerType, bool] = {}

        # Set up threads
        self._start_threads_done = 0

        # Thread to run ble controller asyncio loop (to abstract asyncio from client as well as handle async notifications)
        self._module_loop: asyncio.AbstractEventLoop
        self.module_thread = threading.Thread(daemon=True, target=self._run, name="data")
        self.module_thread.start()
        # Wait for this thread to start
        while self._start_threads_done < 1:
            time.sleep(0.1)

        # Set up thread to send keep alive
        self.keep_alive_thread = threading.Thread(
            target=self._periodic_keep_alive, name="keep_alive", daemon=True
        )

        # Set up thread to block until camera is ready to receive commands
        self.ready = threading.BoundedSemaphore(value=1)
        self._state_condition = threading.Condition()
        self._internal_state = InternalState.ENCODING | InternalState.SYSTEM_BUSY
        self.state_thread = threading.Thread(target=self._maintain_state, name="state", daemon=True)

    # TODO if this fails, we will hang and not exit gracefully.
    def __enter__(self) -> "GoPro":
        """Context manager entrance.

        Raises:
            ScanFailedToFindDevice: Couldn't find a relevant device to connect to

        Returns:
            GoPro: initialized GoPro instance
        """
        device = self.scan()
        if device is None:
            raise ScanFailedToFindDevice

        self._device = device
        self.establish_ble(self._device)
        self.discover_chars()
        self.initialize()
        self.establish_wifi()
        return self

    def __exit__(self, *_: Any) -> None:
        self.terminate_wifi()
        self.terminate_ble()

    @property
    def identifier(self) -> Optional[str]:
        """Get a unique identifier for this instance.

        The identifier is the last 4 digits of the camera. That is, the same string that is used to
        scan for the camera for BLE.

        If no token has been provided and a camera is not yet found, this will be None

        Returns:
            Optional[str]: last 4 digits if available, else None
        """
        return None if self._device is None else str(self._device)

    @property
    def is_discovered(self) -> bool:
        """Have we found a relevant GoPro device to connect to?

        Returns:
            bool: True if yes, False if no
        """
        return self._device is not None

    @property
    def is_ble_connected(self) -> bool:
        """Are we connected via BLE to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        return self._client is not None

    @property
    def is_wifi_connected(self) -> bool:
        """Are we connected via WiFi to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        raise NotImplementedError

    @property
    def is_initialized(self) -> bool:
        """Can we send BLE and Wifi commands right now?

        Returns:
            bool: True if yes, False if no
        """
        return self._start_threads_done >= NUM_THREADS

    def _maintain_state(self) -> None:
        """Thread to keep track of ready / encoding and acquire / release ready semaphore."""
        self.ready.acquire()

        while self.is_ble_connected:
            internal_status_previous = self._internal_state

            with self._state_condition:
                self._state_condition.wait()

                # If we were ready but not now we're not, acquire the semaphore
                if internal_status_previous == 0 and self._internal_state != 0:
                    logger.debug("Control acquiring semaphore")
                    self.ready.acquire()
                    logger.debug("Control has semaphore")
                # If we weren't ready but now we are, release the semaphore
                elif internal_status_previous != 0 and self._internal_state == 0:
                    # If this is the first time, mark that we might now be initialized
                    if not self.is_initialized:
                        self._start_threads_done += 1
                    self.ready.release()
                    logger.debug("Control released semaphore")

        self._start_threads_done -= 1

    def _periodic_keep_alive(self) -> None:
        """Thread to periodically send the keep alive message via BLE."""
        while self.is_ble_connected:
            if not self.is_initialized:
                self._start_threads_done += 1

            try:
                if self.keep_alive():
                    time.sleep(KEEP_ALIVE_INTERVAL)
            except Exception:  # pylint: disable=W0703
                # If the connection disconnects while we were trying to send, there can be any number
                # of exceptions. This is expected and this thread will exit on the next while check.
                pass

        self._start_threads_done -= 1
        logger.debug("periodic keep alive thread exiting...")

    def _run(self) -> None:
        """Thread to keep the event loop running to interface with the BLE adapter."""
        # Create loop for this new thread
        self._module_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._module_loop)

        # Run forever
        self._start_threads_done += 1
        self._module_loop.run_forever()

    def _as_coroutine(self, action: Callable, timeout: float = None) -> Any:
        """Run a function as a coroutine in the module thread.

        This will transfer execution of the given partial to the module thread of this instance

        Args:
            action (Callable): function and parameters to run as corouting
            timeout (float, optional): Time to wait for coroutine to return (in seconds). Defaults to None (wait forever).

        Returns:
            Any: Passes return of coroutine through
        """
        # Allow timeout exception to propagate
        return asyncio.run_coroutine_threadsafe(action(), self._module_loop).result(timeout)

    def start(self) -> None:
        """Convenience API to easily perform all initialization commands if not using the context manager.

        That is, scan and find device, establish connection, discover characteristics, establish wifi, initialize
        """
        self.__enter__()

    def register_listener(self, producer: ProducerType) -> None:
        """Register a producer to store notifications from.

        The notifications can be accessed via the get_update() method.

        Args:
            producer (ProducerType): Producer to listen to.
        """
        self._listeners[producer] = True

    def unregister_listener(self, producer: ProducerType) -> None:
        """Unregister a producer in order to stop listening to its notifications.

        Args:
            producer (ProducerType): Producer to stop listening to.
        """
        del self._listeners[producer]

    def get_update(self, timeout: float = None) -> GoProResp:
        """Get a notification that we received from a registered listener.

        If timeout is None, this will block until a notification is received.

        Args:
            timeout (float, optional): Time to wait for a notification before returning. Defaults to None (wait forever)

        Returns:
            GoProResp: Received notification
        """
        return self._out_q.get(timeout=timeout)

    # ----------------------------------------------- BLE Functionality----------------------------------------

    def scan(self, timeout: float = 5, retries: int = 30) -> Optional[BleDevice]:
        """Scan for devices using the token passed into the instance's initialization.

        Args:
            timeout (float, optional): Time to scan for devices (in seconds). Defaults to 5.
            retries (int, optional): Number of retries before giving up. Defaults to 30.

        Returns:
            Optional[BleDevice]:: device if it was discovered, else None
        """
        for retry in range(1, retries):
            try:
                return self._as_coroutine(partial(self.ble.scan, self._token, timeout))
            except ScanFailedToFindDevice:
                logger.warning(f"Failed to find a device in {timeout} seconds. Retrying #{retry}")
        return None

    def establish_ble(self, device: BleDevice, timeout: float = 15, retries: int = 5) -> None:
        """Connect the instance to a device via BLE.

        Args:
            device (BleDevice): Device to connect to
            timeout (float, optional): Time before considering establishment failed. Defaults to 15 seconds.
            retries (int, optional): How many tries to reconnect after failures. Defaults to 5.

        Raises:
            Any BLE connecting, notification enabling, or pairing errors will be passed through
        """
        for retry in range(1, retries):
            try:
                # Establish connection
                self._client = self._as_coroutine(partial(self.ble.connect, device, timeout=timeout))
                # Attempt to pair
                self._as_coroutine(partial(self.ble.pair, self._client))
                # Enable all GATT notifications
                self._as_coroutine(
                    partial(self.ble.enable_notifications, self._client, self.notification_handler)
                )
                return
            # TODO narrow these down and find out why they're failing, is there a way to handle them?
            except Exception as e:  # pylint: disable=broad-except
                logger.warning(f"{repr(e)}. Retrying #{retry}")
        raise ConnectFailed("BLE", timeout, retries)

    def notification_handler(self, handle: int, data: bytes) -> None:
        """Receive notifications from the BLE controller.

        Args:
            handle (int): Attribute handle that notification was received on.
            data (bytes): Bytestream that was received.
        """
        # Convert handle to UUID
        try:
            uuid = self.gatt_table.handle2uuid(handle)  # type: ignore
        except AttributeError:
            # It's possible a non-Open GoPro service (i.e. battery) sends a notification before we have
            # built the attribute. For now, ignore these.
            logger.warning(f"Unhandled notification from handle {handle}")
            return

        logger.debug(f'Received response on {uuid}: {hexlify(data, ":")}')  # type: ignore

        if uuid not in self._active_resp:
            self._active_resp[uuid] = GoProResp(info=[uuid])

        self._active_resp[uuid]._accumulate(data)

        if self._active_resp[uuid].is_received:
            response = self._active_resp[uuid]

            # Handle internal statuses
            if (
                response.cmd
                in [QueryCmdId.REG_STATUS_VAL_UPDATE, QueryCmdId.GET_STATUS_VAL, QueryCmdId.STATUS_VAL_PUSH]
                and StatusId.ENCODING in response.data
            ):
                with self._state_condition:
                    if response[StatusId.ENCODING] is True:
                        self._internal_state |= InternalState.ENCODING
                    else:
                        self._internal_state &= ~InternalState.ENCODING
                    self._state_condition.notify()
            if (
                response.cmd
                in [QueryCmdId.REG_STATUS_VAL_UPDATE, QueryCmdId.GET_STATUS_VAL, QueryCmdId.STATUS_VAL_PUSH]
                and StatusId.SYSTEM_READY in response.data
            ):
                with self._state_condition:
                    if response[StatusId.SYSTEM_READY] is True:
                        self._internal_state &= ~InternalState.SYSTEM_BUSY
                    else:
                        self._internal_state |= InternalState.SYSTEM_BUSY
                    self._state_condition.notify()

            # Check if this is the awaited synchronous response (id matches). Note! these have to come in order.
            response_claimed = False
            if not self._sync_resp_wait_q.empty():
                queue_snapshot = self._sync_resp_wait_q.snapshot()
                if queue_snapshot[0].id is response.id:
                    # Dequeue it and put this on the ready queue
                    self._sync_resp_wait_q.get_nowait()
                    self._sync_resp_ready_q.put(response)
                    response_claimed = True

            # If this wasn't the awaited synchronous response...
            if not response_claimed:
                logger.info(f"--(ASYNC)--> {response}")
                # See if there are any registered responses that need to be enqueued for client consumption
                for key in response.data.keys():
                    if (response.cmd, key) not in self._listeners:
                        del response.data[key]

                # Enqueue the response if there is anything left
                if len(response.data) > 0:
                    self._out_q.put(response)

            # Clear active response
            del self._active_resp[uuid]

    def terminate_ble(self) -> None:
        """Terminate the BLE connection."""
        logger.info("Terminating the BLE connection")
        self._as_coroutine(partial(self.ble.disconnect, self._client))
        self._client = None

        # try:
        #     self.ready.release()
        # except ValueError:
        #     pass  # If we didn't actually have the semaphore
        # self.keep_alive_thread.join()

        # with self._state_condition:
        #     self._state_condition.notify()
        # self.state_thread.join()

    def discover_chars(self) -> None:
        """Discover all characteristics.

        They will be stored in the instance's gatt_table attribute.
        """
        self.gatt_table = self._as_coroutine(partial(self.ble.discover_chars, self._client))

    def initialize(self) -> None:
        """Register for statuses / information that is necessary for internal functionality."""
        self.state_thread.start()
        self.ble_status.encoding_active.register_value_update()
        self.ble_status.system_ready.register_value_update()
        self.password = self.ble_command.get_wifi_password().flatten
        self.ssid = self.ble_command.get_wifi_ssid().flatten
        self.ble_command.enable_wifi_ap(True)
        self.keep_alive_thread.start()

    def write(self, uuid: UUID, data: bytearray) -> GoProResp:
        """Perform a BLE write and wait for a corresponding notification response.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.ble_command, self.ble_setting, self.ble_status)

        Args:
            uuid (UUID): UUID to write to
            data (bytearray): data to write

        Raises:
            Exception: Unexpected functionality occurred

        Returns:
            GoProResp: parsed notification response data
        """
        # Acquire ready semaphore unless this is during initialization or is a Set Shutter Off command
        have_semaphore = False
        if self.is_initialized and not (
            GoProResp.from_write_command(uuid, data).id is CmdId.SET_SHUTTER and data[-1] == 0
        ):
            logger.debug(f"{GoProResp.from_write_command(uuid, data).id} acquiring semaphore")
            self.ready.acquire()
            logger.debug(f"{GoProResp.from_write_command(uuid, data).id} has semaphore")
            have_semaphore = True

        # Store information on the response we are expecting
        self._sync_resp_wait_q.put(GoProResp.from_write_command(uuid, data))
        # Perform write
        self._as_coroutine(partial(self.ble.write, self._client, uuid.value, data))
        # Wait to be notified that response was received
        try:
            response = self._sync_resp_ready_q.get(timeout=WRITE_TIMEOUT)
        except queue.Empty as e:
            logger.error(f"Response timeout of {WRITE_TIMEOUT} seconds!")
            raise ResponseTimeout(WRITE_TIMEOUT) from e

        # Check status
        try:
            if response.status is not ErrorCode.SUCCESS:
                logger.warning(f"Received non-success status: {response.status}")
        except AttributeError:
            logger.error("Not able to parse status from response")

        # If this was set shutter on, we need to wait to be notified that encoding has started
        if response.cmd is CmdId.SET_SHUTTER and data[-1] == 1:
            while not self._internal_state & InternalState.ENCODING:
                # We don't want to use the application's loop, can't use any of our loops due to potential deadlock,
                # and don't want to spawn a new thread for this. So just poll ¯\_(ツ)_/¯
                # A read to an int is atomic anyway.
                time.sleep(0.1)

        # Release the semaphore if we acquired it
        if have_semaphore:
            self.ready.release()
            logger.debug(f"{GoProResp.from_write_command(uuid, data).id} released the semaphore")

        if response is None:
            raise Exception("The synchronous response is unexpectedly None")

        return response

    def read(self, uuid: UUID) -> GoProResp:
        """Read a characteristic's data by UUID.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.command, self.setting, self.ble_status)

        Args:
            uuid (UUID): characteristic data to read

        Returns:
            bytearray: read data
        """
        have_semaphore = False
        if self.is_initialized:
            logger.debug(f"{uuid} acquiring semaphore")
            self.ready.acquire()
            logger.debug(f"{uuid} has the semaphore")
            have_semaphore = True

        received_data = self._as_coroutine(partial(self.ble.read, self._client, uuid.value))

        if have_semaphore:
            self.ready.release()
            logger.debug(f"{uuid} released the semaphore")

        return GoProResp.from_read_response(uuid, received_data)

    def services_as_csv(self, file: Path = Path("gopro_services.csv")) -> None:
        """Dump discovered services to a csv file.

        If the services haven't been discovered, they will be now.

        Args:
            file (Path, optional): File to write to. Defaults to Path("gopro_services.csv").
        """
        # If we don't yet have the characteristic information, perform a service discovery
        if self.gatt_table is None:
            self.discover_chars()
        with open(file, mode="w") as f:
            logger.debug(f"Dumping discovered BLE characteristics to {file}")
            w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(["handle", "description", "UUID", "properties", "value"])
            # For each service in table
            for s in self.gatt_table.services.values():  # type: ignore
                desc = get_gopro_desc(s.uuid.value) if s.name.lower() == "unknown" else s.name
                w.writerow(["SERVICE", desc, s.uuid.value, "SERVICE", "SERVICE"])
                # For each characteristic in service
                for c in s.chars.values():
                    desc = get_gopro_desc(c.uuid.value) if c.name.lower() == "unknown" else c.name
                    w.writerow([c.handle, desc, c.uuid.value, " ".join(c.props), c.value])
                    # For each descriptor in characteristic
                    for d in c.descriptors:
                        w.writerow([d.handle, "DESCRIPTOR", "", "", d.value])

    # ---------------------------------WiFi-------------------------------------------------------------------

    def establish_wifi(self, timeout: float = 15, retries: int = 5) -> None:
        """Connect to a GoPro device via WiFi.

        Args:
            timeout (float, optional): Time before considering establishment failed. Defaults to 15 seconds.
            retries (int, optional): How many tries to reconnect after failures. Defaults to 5.

        Raises:
            Exception: Wifi failed to connect.
        """
        logger.info("Establishing WiFi connection...")
        for retry in range(1, retries):
            if self.wifi.connect(self.ssid, self.password, timeout=timeout):
                return
            logger.warning(f"WiFi connection timed out. Retrying #{retry}")
        raise ConnectFailed("WiFi", timeout, retries)

    def terminate_wifi(self) -> None:
        """Terminate the WiFi connection."""
        logger.debug("Terminating the WiFi connection...")
        self.wifi.disconnect()

    @_ensure_initialized_acquire_ready_semaphore
    def get(self, url: str) -> GoProResp:
        """Send an HTTP GET request to an Open GoPro endpoint.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.wifi_command and self.wifi_status)

        Args:
            url (str): endpoint URL

        Raises:
            requests.models.HTTPError if there is an HTTP error

        Returns:
            GoProResp: response
        """
        url = GoPro.base_url + url
        logger.debug(f"Sending:  {url}")

        # TODO This is a terrible temporary hack. I just don't know why these are breaking.
        time.sleep(2)

        request = requests.get(url)
        request.raise_for_status()
        response = GoProResp.from_http_response(request)
        return response

    @_ensure_initialized_acquire_ready_semaphore
    def stream_to_file(self, url: str, file: Path) -> None:
        """Send an HTTP GET request to an Open GoPro endpoint to download a binary file.

        There should hopefully not be a scenario where this needs to be called directly as it is generally
        called from the instance's delegates (i.e. self.wifi_command and self.wifi_status)

        Args:
            url (str): endpoint URL
            file (Path): location where file should be downloaded to
        """
        url = GoPro.base_url + url
        logger.debug(f"Sending: {url}")
        with requests.get(url, stream=True) as request:
            request.raise_for_status()
            with open(file, "wb") as f:
                logger.debug(f"receiving stream to {file}...")
                for chunk in request.iter_content(chunk_size=8192):
                    f.write(chunk)

    # -----------------------------------Abstracted Data Functionality----------------------------------------

    def keep_alive(self) -> bool:
        """Send a heartbeat to prevent the BLE connection from dropping.

        This is sent automatically by the GoPro instance.

        Returns:
            bool: True if it succeeded,. False otherwise
        """
        return self.ble_setting.led.set(params.LED.BLE_KEEP_ALIVE).is_ok
