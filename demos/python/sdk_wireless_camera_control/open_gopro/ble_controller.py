# ble_controller.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Manage a Bluetooth connection using bleak."""

import asyncio
import logging
from typing import Pattern, Dict, Any

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice as BleakDevice

from open_gopro.constants import UUID
from open_gopro.util import Singleton
from open_gopro.services import Service, Characteristic, Descriptor, AttributeTable
from open_gopro.interfaces import ScanFailedToFindDevice, BLEController, NotiHandlerType

logger = logging.getLogger(__name__)


class Client:
    """Information per client to be stored in class database."""

    def __init__(self) -> None:
        self.disconnect_event = asyncio.Event()

    def disconnect_handler(self, client: BleakClient) -> None:
        """Handle the disconnect callback from bleak.

        Args:
            client (BleakClient): connected client to disconnect from
        """
        logger.debug(f"On device {client}, Disconnected callback called!")
        self.disconnect_event.set()


class BleakController(BLEController, Singleton):
    """Wrapper around bleak to manage a Bluetooth connection.

    Note, this is a singleton.
    """

    clients: Dict[BleakClient, Client] = {}

    async def read(self, client: BleakClient, uuid: str) -> bytearray:
        """AsyncIO method to read data from a UUID.

        Args:
            client (BleakClient): client to read from
            uuid (str): uuid to read

        Returns:
            bytearray: read data
        """
        logger.debug(f"Reading from {uuid}")
        response = await client.read_gatt_char(uuid)
        logger.debug(f'Received response on {uuid}: {response.hex( ":")}')

        return response

    async def write(self, client: BleakClient, uuid: str, value: bytearray) -> None:
        """AsyncIO method to write data to a UUID.

        Perform a write, then wait for event to be notified (from a notification handler)

        Args:
            client (BleakClient): Device to write to
            uuid (str): characteristic UUID to write to
            value (bytearray): data to write
            event (asyncio.Event): event to synchronize response
        """
        logger.debug(f"Writing to {uuid}: {value.hex(':')}")

        await client.write_gatt_char(uuid, value)

    async def scan(self, token: Pattern, timeout: int = 5) -> BleakDevice:
        """AsyncIO method to scan for a regex.

        Args:
            token (Pattern): Regex to look for when scanning.
            timeout (int, optional): Time to scan. Defaults to 5.

        Raises:
            ScanFailedToFindDevice: Did not find any of the token when scanning.

        Returns:
            BleakDevice: The first matched device that was discovered
        """
        name = token.pattern.strip(r"\d\d\d\d")
        logger.info(f"Scanning for {name} bluetooth devices...")

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
            raise ScanFailedToFindDevice
        logger.info(f"Found {len(matched_devices)} matching devices.")

        # If there's more than 1, the first one gets lucky.
        return matched_devices[0]

    async def connect(self, device: BleakDevice, timeout: int = 15) -> BleakClient:
        """AsyncIO method to connect to a device.

        Args:
            device (BleakDevice): Device to connect to

        Raises:
            Exception: Connection failed to establish

        Returns:
            BleakClient: Connected device
        """
        c = Client()
        bleak_client = BleakClient(device, disconnected_callback=c.disconnect_handler)
        BleakController.clients[bleak_client] = c

        logger.info(f"Establishing BLE connection to {device}...")
        await bleak_client.connect(timeout=timeout)

        return bleak_client

    async def pair(self, client: BleakClient) -> None:
        """AsyncIO method to pair to a device after connection.

        This is required for Windows and not allowed on Mac...

        Args:
            client (BleakClient): Device to pair to
        """
        logger.debug("Attempting to pair...")
        try:
            await client.pair()
        except NotImplementedError:
            # This is expected on Mac
            pass
        logger.debug("Pairing complete!")
        logger.info("BLE Connected!")

    async def enable_notifications(self, client: BleakClient, handler: NotiHandlerType) -> None:
        """AsyncIO method to enable all notifications.

        Search through all characteristics and enable any that have notification property.

        Args:
            client (BleakClient): Device to enable notifications for
            handler (Callable): Notification callback handler
        """
        logger.info("Enabling notifications...")
        for service in client.services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    logger.debug(f"Enabling notification on char {char.uuid}")
                    await client.start_notify(char, handler)
        logger.info("Done enabling notifications")

    async def discover_chars(self, client: BleakClient) -> AttributeTable:
        """AsyncIO method to discover all characteristics.

        Args:
            client (BleakClient): Device to perform discovery on

        Returns:
            AttributeTable: Dict of services by UUID
        """
        logger.info("Discovering characteristics...")
        services: Dict[UUID, Service] = {}

        for service in client.services:
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
                value = bytes(await client.read_gatt_char(char.uuid)) if "read" in char.properties else b""

                # Create and log characteristic
                c = Characteristic(char.handle, UUID(char.uuid), char.properties, char.description, value)

                # Get any descriptors if they exist
                descriptors = []
                for descriptor in char.descriptors:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    descriptors.append(Descriptor(descriptor.handle, value))

                # Update char and add to dict
                c.descriptors = descriptors
                # Add characteristic to char dic
                chars[c.uuid] = c

            # Add char dict to service
            services[UUID(service.uuid)].chars = chars

        logger.info("Done discovering characteristics!")
        return AttributeTable(services)

    async def disconnect(self, client: BleakClient) -> bool:
        """AsyncIO method to terminate a BLE connection.

        Args:
            client (BleakClient): client to disconnect from

        Returns:
            bool: True if disconnect was successful, False otherwise
        """
        if client.is_connected:
            logger.info("Disconnecting...")
            await client.disconnect()
            await BleakController.clients[client].disconnect_event.wait()
        logger.info("Device disconnected!")

        return True
