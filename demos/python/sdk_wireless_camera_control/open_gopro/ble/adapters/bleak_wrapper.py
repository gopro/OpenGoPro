# bleak_wrapper.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Manage a Bluetooth connection using bleak."""

import sys
import asyncio
import logging
import platform
import threading
from typing import Pattern, Any, Callable, Optional, Union

import pexpect
from bleak import BleakScanner, BleakClient, BleakError
from bleak.backends.device import BLEDevice as BleakDevice

from open_gopro.exceptions import ConnectFailed
from open_gopro.util import Singleton
from open_gopro.ble import (
    Service,
    Characteristic,
    Descriptor,
    GattDB,
    BLEController,
    NotiHandlerType,
    FailedToFindDevice,
    BleUUID,
    UUIDs,
    CharProps,
)

logger = logging.getLogger(__name__)

bleak_props_to_enum = {
    "broadcast": CharProps.BROADCAST,
    "read": CharProps.READ,
    "write-without-response": CharProps.WRITE_NO_RSP,
    "write": CharProps.WRITE_YES_RSP,
    "notify": CharProps.NOTIFY,
    "indicate": CharProps.INDICATE,
    "authenticated-signed-writes": CharProps.AUTH_SIGN_WRITE,
    "extended-properties": CharProps.EXTENDED,
}


def uuid2bleak_string(uuid: BleUUID) -> str:
    """Convert a BleUUID object to a string representation to appease bleak

    Bleak identifies UUID's by str(). Since BleUUID has overridden that method, we manually convert to the
    string representation that bleak expects.

    Args:
        uuid (BleUUID): uuid to convert

    Returns:
        str: bleakful string representation
    """
    return f"{uuid.hex[:8]}-{uuid.hex[8:12]}-{uuid.hex[12:16]}-{uuid.hex[16:20]}-{uuid.hex[20:]}"


class BleakWrapperController(BLEController[BleakDevice, BleakClient], Singleton):
    """Wrapper around bleak to manage a Bluetooth connection."""

    def __init__(self, exception_handler: Optional[Callable] = None) -> None:
        """Constructor

        Note, this is a singleton.

        Args:
            exception_handler (Callable, Optional): Used to catch asyncio exceptions from other tasks. Defaults to None.
        """
        # Thread to run ble controller asyncio loop (to abstract asyncio from client as well as handle async notifications)
        self._module_loop: asyncio.AbstractEventLoop  # Will be set when module thread starts
        self._module_thread = threading.Thread(daemon=True, target=self._run, name="data")
        self._ready = threading.Event()
        self._exception_handler = exception_handler
        self._module_thread.start()
        self._ready.wait()

    def _run(self) -> None:
        """Thread to keep the event loop running to interface with the BLE adapter."""
        # Create loop for this new thread
        self._module_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._module_loop)
        self._module_loop.set_exception_handler(self._exception_handler)

        # Run forever
        self._ready.set()
        self._module_loop.run_forever()

    def _as_coroutine(self, action: Callable, timeout: float = None) -> Any:
        """Run a function as a coroutine in the module thread.

        This will transfer execution of the given partial to the module thread of this instance

        Args:
            action (Callable): function and parameters to run as corouting
            timeout (float): Time to wait for coroutine to return (in seconds). Defaults to None (wait forever).

        Returns:
            Any: Passes return of coroutine through
        """
        # Allow timeout exception to propagate
        return asyncio.run_coroutine_threadsafe(action(), self._module_loop).result(timeout)

    def read(self, handle: BleakClient, uuid: BleUUID) -> bytearray:
        """Read data from a BleUUID.

        Args:
            handle (BleakClient): client to read from
            uuid (BleUUID): uuid to read

        Returns:
            bytearray: read data
        """

        async def _async_read() -> bytearray:
            logger.debug(f"Reading from {uuid}")
            response = await handle.read_gatt_char(uuid2bleak_string(uuid))
            logger.debug(f'Received response on BleUUID [{uuid}]: {response.hex( ":")}')
            return response

        return self._as_coroutine(_async_read)

    def write(self, handle: BleakClient, uuid: BleUUID, data: bytearray) -> None:
        """Write data to a BleUUID.

        Args:
            handle (BleakClient): Device to write to
            uuid (BleUUID): characteristic BleUUID to write to
            data (bytearray): data to write
        """

        async def _async_write() -> None:
            logger.debug(f"Writing to {uuid}: {uuid.hex}")
            # TODO make with / without response configurable
            await handle.write_gatt_char(uuid2bleak_string(uuid), data, response=True)

        self._as_coroutine(_async_write)

    def scan(
        self, token: Pattern, timeout: int = 5, service_uuids: Optional[list[BleUUID]] = None
    ) -> BleakDevice:
        """Scan for a regex in advertising data strings, optionally filtering on service BleUUID's

        Args:
            token (Pattern): Regex to look for when scanning.
            timeout (int): Time to scan. Defaults to 5.
            service_uuids (Optional[list[BleUUID]]): The list of BleUUID's to filter on. Defaults to None.

        Returns:
            BleakDevice: The first matched device that was discovered
        """

        async def _async_scan() -> BleakDevice:
            logger.info(f"Scanning for {token.pattern} bluetooth devices...")
            devices: dict[str, BleakDevice] = {}
            uuids = [] if service_uuids is None else [uuid2bleak_string(uuid) for uuid in service_uuids]

            def _scan_callback(device: BleakDevice, _: Any) -> None:
                """Only keep devices that have a device name token

                For GoPro, this must be coming from the scan response

                Args:
                    device (BleakDevice): discovered device
                """
                if (name := device.name) and name not in devices:
                    devices[name] = device
                    logger.info(f"\tDiscovered: {device}")

            # Now get list of connectable advertisements
            await BleakScanner(service_uuids=uuids).discover(
                timeout=timeout, detection_callback=_scan_callback, service_uuids=uuids
            )
            # Now look for our matching device(s)
            if not (matched_devices := [device for name, device in devices.items() if token.match(name)]):
                raise FailedToFindDevice
            logger.info(f"Found {len(matched_devices)} matching devices.")
            # If there's more than 1, the first one gets lucky.
            return matched_devices[0]

        return self._as_coroutine(_async_scan)

    def connect(
        self,
        disconnect_cb: Callable,
        device: BleakDevice,
        timeout: int = 15,
    ) -> BleakClient:
        """Connect to a device.

        Args:
            disconnect_cb (Callable): function called when a disconnect is received
            device (BleakDevice): Device to connect to
            timeout (int): How long to try connecting before timing out and raising exception. Defaults to 15.

        Raises:
            ConnectFailed: Connection failed to establish

        Returns:
            BleakClient: Connected device
        """

        class ConnectSession:
            """Transient connection manager to manage disconnects while connecting."""

            def __init__(self) -> None:
                self.disconnected = asyncio.Event()
                self.disconnected.clear()

            def disconnect_handler(self, _: Any) -> None:
                """Disconnect handler which is only used while connection is being established.

                Will be set to App's passed-in disconnect handler once connection is established
                """
                # From sniffer capture analysis, this is always due to the slave not receiving the master's
                # connection request. This is (potentially) normal BLE behavior.
                self.disconnected.set()

        async def _async_connect() -> tuple[Optional[BleakClient], Optional[Union[Exception, BaseException]]]:
            logger.info(f"Establishing BLE connection to {device}...")

            connect_session = ConnectSession()
            bleak_client = BleakClient(
                device, disconnected_callback=connect_session.disconnect_handler, use_cached=False
            )
            exception = None
            try:
                task_connect = asyncio.create_task(bleak_client.connect(timeout=timeout), name="connect")
                task_disconnected = asyncio.create_task(connect_session.disconnected.wait(), name="disconnect")
                finished, unfinished = await asyncio.wait(
                    [task_connect, task_disconnected], return_when=asyncio.FIRST_COMPLETED
                )
                for task in finished:
                    if exception := task.exception():
                        if isinstance(task.exception(), asyncio.exceptions.TimeoutError):
                            exception = Exception("Connection request timed out")
                        # Completion of these is tasks mutually exclusive so safe to stop now
                        break
                for task in unfinished:
                    task.cancel()
                if connect_session.disconnected.is_set():
                    exception = Exception("Connection failed during establishment..")
            except (BleakError, asyncio.TimeoutError) as e:
                exception = e

            bleak_client.set_disconnected_callback(disconnect_cb)
            return bleak_client, exception

        client, exception = self._as_coroutine(_async_connect)
        if exception:
            logger.warning(exception)
            raise ConnectFailed("BLE", 1, 1) from exception
        return client

    def pair(self, handle: BleakClient) -> None:
        """Pair to a device after connection.

        This is required for Windows and not allowed on Mac.
        Linux requires a separate process to interact with bluetoothctl to accept pairing.

        Args:
            handle (BleakClient): Device to pair to
        """

        async def _async_def_pair() -> None:
            logger.debug("Attempting to pair...")
            if OS := platform.system() == "Linux":
                # Manually control bluetoothctl on Linux
                bluetoothctl = pexpect.spawn("bluetoothctl")
                if logger.level == logging.DEBUG:
                    bluetoothctl.logfile = sys.stdout.buffer
                bluetoothctl.expect("Agent registered")
                # First see if we are already paired
                bluetoothctl.sendline("paired-devices")
                bluetoothctl.expect("paired-devices")
                bluetoothctl.expect(r"#")
                for device in bluetoothctl.before.decode("utf-8").splitlines():
                    if "Device" in device and device.split()[1] == handle.address:
                        break  # The device is already paired
                else:
                    # We're not paired so do it now
                    bluetoothctl.sendline(f"pair {handle.address}")
                    bluetoothctl.expect("Accept pairing")
                    bluetoothctl.sendline("yes")
                    bluetoothctl.expect("Pairing successful")

            elif OS == "Darwin":
                # No pairing on Mac
                pass
            else:
                await handle.pair()

            logger.debug("Pairing complete!")

        self._as_coroutine(_async_def_pair)

    def enable_notifications(self, handle: BleakClient, handler: NotiHandlerType) -> None:
        """Enable all notifications.

        Search through all characteristics and enable any that have notification property.

        Args:
            handle (BleakClient): Device to enable notifications for
            handler (NotiHandlerType): Notification callback handler
        """

        async def _async_enable_notifications() -> None:
            logger.info("Enabling notifications...")
            for service in handle.services:
                for char in service.characteristics:
                    if "notify" in char.properties:
                        logger.debug(f"Enabling notification on char {char.uuid}")
                        await handle.start_notify(char, handler)
            logger.info("Done enabling notifications")

        self._as_coroutine(_async_enable_notifications)

    def discover_chars(self, handle: BleakClient, uuids: type[UUIDs] = None) -> GattDB:
        """Discover all characteristics for a connected handle.

        By default, the BLE controller only knows Spec-Defined BleUUID's so any additional BleUUID's should
        be passed in with the uuids argument

        Args:
            handle (BleakClient): BLE handle to discover for
            uuids (type[UUIDs], Optional): Additional BleUUID information to use when building the
                Gatt Database. Defaults to None.

        Returns:
            GattDB: Gatt Database
        """

        def bleak_props_adapter(bleak_props: list[str]) -> CharProps:
            """Convert a list of bleak string properties into a CharProps

            Args:
                bleak_props (list[str]): bleak strings to convert

            Returns:
                CharProps: converted Enum
            """
            props = CharProps.NONE
            for prop in bleak_props:
                props |= bleak_props_to_enum[prop]
            return props

        async def _async_discover_chars() -> GattDB:
            logger.info("Discovering characteristics...")
            services: list[Service] = []
            for service in handle.services:
                service_uuid = (
                    uuids[service.uuid]
                    if uuids and service.uuid in uuids
                    else BleUUID(service.description, hex=service.uuid)
                )
                logger.debug(f"[Service] {service_uuid}")

                # Loop over all chars in service
                chars: list[Characteristic] = []
                for char in service.characteristics:
                    # Get any descriptors if they exist
                    descriptors: list[Descriptor] = []
                    for descriptor in char.descriptors:
                        descriptors.append(
                            Descriptor(
                                handle=descriptor.handle,
                                uuid=(
                                    uuids[descriptor.uuid]
                                    if uuids and descriptor.uuid in uuids
                                    else BleUUID(descriptor.description, hex=descriptor.uuid)
                                ),
                                value=await handle.read_gatt_descriptor(descriptor.handle),
                            )
                        )
                    # Create new characteristic
                    chars.append(
                        Characteristic(
                            handle=char.handle,
                            uuid=(
                                uuids[char.uuid]
                                if uuids and char.uuid in uuids
                                else BleUUID(char.description, hex=char.uuid)
                            ),
                            props=bleak_props_adapter(char.properties),
                            init_descriptors=descriptors,
                        )
                    )
                    logger.debug(f"\t[Characteristic] {chars[-1]}")

                # Create new service
                services.append(Service(uuid=service_uuid, start_handle=service.handle, init_chars=chars))

            logger.info("Done discovering characteristics!")
            return GattDB(services)

        return self._as_coroutine(_async_discover_chars)

    def disconnect(self, handle: BleakClient) -> None:
        """Terminate a BLE connection.

        Args:
            handle (BleakClient): client to disconnect from

        Returns:
            bool: True if disconnect was successful, False otherwise
        """

        async def _async_disconnect() -> None:
            if handle.is_connected:
                logger.info("Disconnecting...")
                await handle.disconnect()
                # Disconnect handler registered during connect will be asynchronously called
            logger.info("Device disconnected!")

        return self._as_coroutine(_async_disconnect)
