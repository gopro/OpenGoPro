# bleak_wrapper.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Manage a Bluetooth connection using bleak."""

import asyncio
import logging
import threading
from typing import Pattern, Dict, Any, Callable, Optional

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice as BleakDevice

from open_gopro.exceptions import ConnectFailed
from open_gopro.util import Singleton
from open_gopro.ble import (
    Service,
    Characteristic,
    Descriptor,
    AttributeTable,
    BLEController,
    NotiHandlerType,
    FailedToFindDevice,
    UUID,
)

logger = logging.getLogger(__name__)


class BleakWrapperController(BLEController[BleakDevice, BleakClient], Singleton):
    """Wrapper around bleak to manage a Bluetooth connection.

    Note, this is a singleton.
    """

    def __init__(self) -> None:
        # Thread to run ble controller asyncio loop (to abstract asyncio from client as well as handle async notifications)
        self._module_loop: asyncio.AbstractEventLoop  # Will be set when module thread starts
        self._module_thread = threading.Thread(daemon=True, target=self._run, name="data")
        self._ready = threading.Event()
        self._module_thread.start()
        self._ready.wait()

    def _run(self) -> None:
        """Thread to keep the event loop running to interface with the BLE adapter."""
        # Create loop for this new thread
        self._module_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._module_loop)

        # Run forever
        self._ready.set()
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

    def read(self, handle: BleakClient, uuid: str) -> bytearray:
        """read data from a UUID.

        Args:
            handle (BleakClient): client to read from
            uuid (str): uuid to read

        Returns:
            bytearray: read data
        """

        async def _async_read() -> bytearray:  # pylint: disable=missing-return-doc
            logger.debug(f"Reading from {uuid}")
            response = await handle.read_gatt_char(uuid)
            logger.debug(f'Received response on {uuid}: {response.hex( ":")}')
            return response

        return self._as_coroutine(_async_read)

    def write(self, handle: BleakClient, uuid: str, data: bytearray) -> None:
        """Write data to a UUID.

        Perform a write, then wait for event to be notified (from a notification handler)

        Args:
            handle (BleakClient): Device to write to
            uuid (str): characteristic UUID to write to
            data (bytearray): data to write
        """

        async def _async_write() -> None:
            logger.debug(f"Writing to {uuid}: {data.hex(':')}")
            await handle.write_gatt_char(uuid, data)

        self._as_coroutine(_async_write)

    def scan(self, token: Pattern, timeout: int = 5) -> BleakDevice:
        """scan for a regex.

        Args:
            token (Pattern): Regex to look for when scanning.
            timeout (int, optional): Time to scan. Defaults to 5.

        Raises:
            FailedToFindDevice: Did not find any of the token when scanning.

        Returns:
            BleakDevice: The first matched device that was discovered
        """

        async def _async_scan() -> BleakDevice:  # pylint: disable=missing-return-doc
            logger.info(f"Scanning for {token.pattern} bluetooth devices...")
            devices: Dict[str, BleakDevice] = {}

            def _scan_callback(device: BleakDevice, _: Any) -> None:
                """Bleak optional scan callback to receive every scan result.

                We need this because the GoPro will sometimes only show as a
                nonconnectable scan response from bleak.

                Also, if the device shows as both the above as well as a connectable advertisement,
                the latter must be used in order to avoid an exception from CoreBluetooth on Mac.

                Args:
                    device (BleakDevice): discovered device
                    _ : advertisement that we're ignoring
                """
                # Add to the dict if not unknown
                if device.name != "Unknown" and device.name is not None:
                    devices[device.name] = device

            # Now get list of connectable advertisements
            for device in await BleakScanner.discover(timeout=timeout, detection_callback=_scan_callback):
                if device.name != "Unknown" and device.name is not None:
                    devices[device.name] = device
            for d in devices:
                logger.info(f"\tDiscovered: {d}")

            # Now look for our matching device(s)
            matched_devices = [device for name, device in devices.items() if token.match(name)]
            if len(matched_devices) == 0:
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
            timeout (int, optional): How long to try connecting before timing out and raising exception. Defaults to 15.

        Raises:
            ConnectFailed: Connection failed to establish

        Returns:
            BleakClient: Connected device
        """

        async def _async_connect() -> Optional[BleakClient]:  # pylint: disable=missing-return-doc
            logger.info(f"Establishing BLE connection to {device}...")
            bleak_client = BleakClient(device, disconnected_callback=disconnect_cb)
            try:
                await bleak_client.connect(timeout=timeout)
            except Exception as e:  # pylint: disable= broad-except
                logger.warning(f"Bleak failed to connect: {repr(e)}")
                return None

            return bleak_client

        client = self._as_coroutine(_async_connect)
        if client is None:
            raise ConnectFailed("Bleak Connection Timed out", timeout, 1)
        return client

    def pair(self, handle: BleakClient) -> None:
        """pair to a device after connection.

        This is required for Windows and not allowed on Mac...

        Args:
            handle (BleakClient): Device to pair to
        """

        async def _async_def_pair() -> None:
            logger.debug("Attempting to pair...")
            try:
                await handle.pair()
            except NotImplementedError:
                # This is expected on Mac
                pass
            logger.debug("Pairing complete!")

        self._as_coroutine(_async_def_pair)

    def enable_notifications(self, handle: BleakClient, handler: NotiHandlerType) -> None:
        """enable all notifications.

        Search through all characteristics and enable any that have notification property.

        Args:
            handle (BleakClient): Device to enable notifications for
            handler (Callable): Notification callback handler
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

    def discover_chars(self, handle: BleakClient) -> AttributeTable:
        """discover all characteristics.

        Args:
            handle (BleakClient): Device to perform discovery on

        Returns:
            AttributeTable: Dict of services by UUID
        """

        async def _async_discover_chars() -> AttributeTable:  # pylint: disable=missing-return-doc
            logger.info("Discovering characteristics...")
            services: Dict[UUID, Service] = {}

            for service in handle.services:
                logger.debug("[Service] {0}: {1}".format(service.uuid, service.description))
                try:
                    # Create new service
                    services[UUID(service.uuid)] = Service(UUID(service.uuid), service.description)
                except ValueError:
                    logger.error(f"{service.uuid} is not a known service")
                    continue

                # Loop over all chars in service
                chars: Dict[UUID, Characteristic] = {}
                for char in service.characteristics:
                    # Read if applicable
                    value = bytes(await handle.read_gatt_char(char.uuid)) if "read" in char.properties else b""
                    # Create and log characteristic
                    c = Characteristic(char.handle, UUID(char.uuid), char.properties, char.description, value)
                    # Get any descriptors if they exist
                    descriptors = []
                    for descriptor in char.descriptors:
                        value = await handle.read_gatt_descriptor(descriptor.handle)
                        descriptors.append(Descriptor(descriptor.handle, value))
                    # Update char and add to dict
                    c.descriptors = descriptors
                    # Add characteristic to char dic
                    chars[c.uuid] = c

                # Add char dict to service
                services[UUID(service.uuid)].chars = chars

            logger.info("Done discovering characteristics!")
            return AttributeTable(services)

        return self._as_coroutine(_async_discover_chars)

    def disconnect(self, handle: BleakClient) -> None:
        """terminate a BLE connection.

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
