# bleak_wrapper.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Manage a Bluetooth connection using bleak."""

import asyncio
import logging
import platform
import tempfile
from pathlib import Path
from typing import Any, Callable, Optional, Pattern

import bleak
import pexpect
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice as BleakDevice
from bleak.backends.scanner import AdvertisementData
from packaging.version import Version

from open_gopro.ble import (
    BLEController,
    BleUUID,
    Characteristic,
    CharProps,
    Descriptor,
    FailedToFindDevice,
    GattDB,
    NotiHandlerType,
    Service,
    UUIDs,
)
from open_gopro.exceptions import ConnectFailed
from open_gopro.util import Singleton

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


class BleakWrapperController(BLEController[BleakDevice, bleak.BleakClient], Singleton):
    """Wrapper around bleak to manage a Bluetooth connection."""

    def __init__(self, exception_handler: Optional[Callable] = None) -> None:
        """Constructor

        Note, this is a singleton.

        Args:
            exception_handler (Callable, Optional): Used to catch asyncio exceptions from other tasks. Defaults to None.
        """
        BLEController.__init__(self, exception_handler)

    async def read(self, handle: bleak.BleakClient, uuid: BleUUID) -> bytearray:
        """Read data from a BleUUID.

        Args:
            handle (bleak.BleakClient): client to read from
            uuid (BleUUID): uuid to read

        Returns:
            bytearray: read data
        """
        logger.debug(f"Reading from {uuid}")
        response = await handle.read_gatt_char(uuid2bleak_string(uuid))
        logger.debug(f'Received response on BleUUID [{uuid}]: {response.hex( ":")}')
        return response

    async def write(self, handle: bleak.BleakClient, uuid: BleUUID, data: bytearray) -> None:
        """Write data to a BleUUID.

        Args:
            handle (bleak.BleakClient): Device to write to
            uuid (BleUUID): characteristic BleUUID to write to
            data (bytearray): data to write
        """
        logger.debug(f"Writing to {uuid}: {uuid.hex}")
        await handle.write_gatt_char(uuid2bleak_string(uuid), data, response=True)

    async def scan(
        self, token: Pattern, timeout: int = 5, service_uuids: Optional[list[BleUUID]] = None
    ) -> BleakDevice:
        """Scan for a regex in advertising data strings, optionally filtering on service BleUUID's

        Args:
            token (Pattern): Regex to look for when scanning.
            timeout (int): Time to scan. Defaults to 5.
            service_uuids (Optional[list[BleUUID]]): The list of BleUUID's to filter on. Defaults to None.

        Raises:
            FailedToFindDevice: scan timed out without finding device

        Returns:
            BleakDevice: The first matched device that was discovered
        """
        stop_event = asyncio.Event()
        logger.info(f"Scanning for {token.pattern} bluetooth devices...")
        devices: dict[str, BleakDevice] = {}
        uuids = [] if service_uuids is None else [uuid2bleak_string(uuid) for uuid in service_uuids]

        def scan_callback(device: BleakDevice, adv_data: AdvertisementData) -> None:
            """Only keep devices that have a device name token

            Args:
                device (BleakDevice): discovered device
                adv_data (AdvertisementData): advertisement (and / or scan response) data
            """
            if (name := adv_data.local_name or device.name) and name not in devices:
                devices[name] = device
                logger.info(f"\tDiscovered: {device}")
                stop_event.set()

        # Now get list of connectable advertisements
        async with bleak.BleakScanner(timeout=timeout, detection_callback=scan_callback, service_uuids=uuids):
            # The bleak scan timeout appears to not be used at least in some versions of bleak
            try:
                await asyncio.wait_for(stop_event.wait(), timeout)
            except asyncio.TimeoutError as e:
                raise FailedToFindDevice from e
        # Now look for our matching device(s)
        if not (matched_devices := [device for name, device in devices.items() if token.match(name)]):
            raise FailedToFindDevice
        logger.info(f"Found {len(matched_devices)} matching devices.")
        # If there's more than 1, the first one gets lucky.
        return matched_devices[0]

    async def connect(self, disconnect_cb: Callable, device: BleakDevice, timeout: int = 15) -> bleak.BleakClient:
        """Connect to a device.

        Args:
            disconnect_cb (Callable): function called when a disconnect is received
            device (BleakDevice): Device to connect to
            timeout (int): How long to try connecting before timing out and raising exception. Defaults to 15.

        Raises:
            ConnectFailed: Connection was not established

        Returns:
            bleak.BleakClient: Connected device
        """

        class ConnectSession:
            """Catch connection failures and multiplex disconnect handler callback

            Args:
                client_cb (Callable): client's disconnect callback
            """

            def __init__(self, client_cb: Callable) -> None:
                self._disconnected = asyncio.Event()
                self._disconnected.clear()
                self._client_cb = client_cb
                self._should_use_client_cb = False

            def disconnect_cb(self, *args: Any) -> None:
                """Multiplex between client and during-connection disconnect handler callback

                Args:
                    *args (Any): passed through
                """
                # pylint: disable=expression-not-assigned
                self._client_cb(args) if self._should_use_client_cb else self._connecting_cb(args)

            @property
            def did_fail(self) -> bool:
                """Did the connection fail during establishment?

                Returns:
                    bool: True if it failed, False otherwise
                """
                return self._disconnected.is_set()

            def _connecting_cb(self, _: Any) -> None:
                """Disconnect handler which is only used while connection is being established.

                Will be set to App's passed-in disconnect handler once connection is established
                """
                # From sniffer capture analysis, this is always due to the slave not receiving the master's
                # connection request. This is (potentially) normal BLE behavior.
                self._disconnected.set()

            def use_client_cb(self) -> None:
                """Use the client's requested connection handler callback when a disconnection is caught"""
                self._should_use_client_cb = True

            async def catch_connection_failure(self) -> None:
                """Disconnection callback to be used during connection establishment"""
                await self._disconnected.wait()

        logger.info(f"Establishing BLE connection to {device}...")

        connect_session = ConnectSession(disconnect_cb)
        client = bleak.BleakClient(
            device, disconnected_callback=connect_session.disconnect_cb, use_cached=False, timeout=timeout
        )
        exception = None
        try:
            task_connect: asyncio.Task = asyncio.create_task(client.connect(timeout=timeout), name="connect")
            task_disconnected: asyncio.Task = asyncio.create_task(
                connect_session.catch_connection_failure(), name="disconnect"
            )
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
            if connect_session.did_fail:
                exception = Exception("Connection failed during establishment..")
            else:
                connect_session.use_client_cb()
        except Exception as e:  # pylint: disable=broad-except
            exception = e

        if exception:
            logger.warning(exception)
            raise ConnectFailed("BLE", 1, 1) from exception
        return client

    async def pair(self, handle: bleak.BleakClient) -> None:
        """Pair to a device after connection.

        This is required for Windows and not allowed on Mac.
        Linux requires a separate process to interact with bluetoothctl to accept pairing.

        Args:
            handle (bleak.BleakClient): Device to pair to
        """
        logger.debug("Attempting to pair...")

        if (OS := platform.system()) == "Linux":
            temp_file = Path(tempfile.gettempdir()) / "pexpect.log"
            with open(temp_file, "wb") as fp:
                logger.info("Pairing with bluetoothctl")
                # Manually control bluetoothctl on Linux
                bluetoothctl = pexpect.spawn("bluetoothctl")
                bluetoothctl.logfile = fp
                bluetoothctl.expect("Agent registered")
                # Get the version
                bluetoothctl.sendline("version")
                bluetoothctl.expect(r"Version")
                bluetoothctl.expect(r"\n")
                version = Version(bluetoothctl.before.decode("utf-8").strip())
                # First see if we are already paired
                if version >= Version("5.66"):
                    bluetoothctl.sendline("devices Paired")
                    bluetoothctl.expect("devices Paired")
                else:
                    bluetoothctl.sendline("paired-devices")
                    bluetoothctl.expect("paired-devices")
                bluetoothctl.expect(r"#")
                for device in bluetoothctl.before.decode("utf-8").splitlines():
                    if "Device" in device and device.split()[1] == handle.address:
                        break  # The device is already paired
                else:
                    # We're not paired so do it now
                    bluetoothctl.sendline(f"pair {handle.address}")
                    if (match := bluetoothctl.expect(["Accept pairing", "Pairing successful"])) == 0:
                        bluetoothctl.sendline("yes")
                        bluetoothctl.expect("Pairing successful")
                    elif match == 1:  # We received pairing successful so nothing else to do
                        pass

            logger.debug(temp_file.read_bytes().decode("utf-8"))

        elif OS == "Darwin":
            # No pairing on Mac
            pass
        else:
            await handle.pair()

        logger.debug("Pairing complete!")

    async def enable_notifications(self, handle: bleak.BleakClient, handler: NotiHandlerType) -> None:
        """Enable all notifications.

        Search through all characteristics and enable any that have notification property.

        Args:
            handle (bleak.BleakClient): Device to enable notifications for
            handler (NotiHandlerType): Notification callback handler
        """

        def bleak_notification_cb_adapter(characteristic: BleakGATTCharacteristic, data: bytearray) -> None:
            """Adapt bleak notification callback signature to our interface signature

            Args:
                characteristic (BleakGATTCharacteristic): characteristic that notification was received on
                data (bytearray): data received as part of notification
            """
            handler(characteristic.handle, data)

        logger.info("Enabling notifications...")
        for service in handle.services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    logger.debug(f"Enabling notification on char {char.uuid}")
                    await handle.start_notify(char, bleak_notification_cb_adapter)
        logger.info("Done enabling notifications")

    async def discover_chars(self, handle: bleak.BleakClient, uuids: Optional[type[UUIDs]] = None) -> GattDB:
        """Discover all characteristics for a connected handle.

        By default, the BLE controller only knows Spec-Defined BleUUID's so any additional BleUUID's should
        be passed in with the uuids argument

        Args:
            handle (bleak.BleakClient): BLE handle to discover for
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

    async def disconnect(self, handle: bleak.BleakClient) -> None:
        """Terminate a BLE connection.

        Args:
            handle (bleak.BleakClient): client to disconnect from
        """
        if handle.is_connected:
            logger.info("Disconnecting...")
            await handle.disconnect()
            # Disconnect handler registered during connect will be asynchronously called
        logger.info("Device disconnected!")
