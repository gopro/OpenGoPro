# test_bleak_wrapper.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""Unit testing of bleak controller"""

import asyncio
import re
from dataclasses import dataclass, field

import pytest

from open_gopro.ble import BleUUID
from open_gopro.ble.adapters.bleak_wrapper import BleakWrapperController
from open_gopro.constants import GoProUUIDs
from open_gopro.exceptions import ConnectFailed, FailedToFindDevice


def test_singleton(mock_bleak_wrapper: BleakWrapperController):
    new_bleak_wrapper = BleakWrapperController()
    assert mock_bleak_wrapper is new_bleak_wrapper


@pytest.mark.asyncio
async def test_scan_success(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    callback = asyncio.Queue()

    @dataclass
    class MockDevice:
        address: str = "address"

    @dataclass
    class MockAdvData:
        local_name: str = "GoPro 1234"

    class MockBleakScanner:
        def __init__(self, *args, **kwargs) -> None:
            self.callback = kwargs["detection_callback"]

        async def __aenter__(self, *args, **kwargs):
            await callback.put(self.callback)
            return self

        async def __aexit__(self, *_) -> None:
            pass

    async def provide_device():
        cb = await callback.get()
        cb(MockDevice(), MockAdvData())

    monkeypatch.setattr("bleak.BleakScanner", MockBleakScanner)

    results = await asyncio.gather(
        mock_bleak_wrapper.scan(
            token=re.compile(r"GoPro [A-Z0-9]{4}"),
            timeout=1,
            service_uuids=[GoProUUIDs.CQ_QUERY],
        ),
        provide_device(),
    )
    assert results[0].address == "address"


@pytest.mark.asyncio
async def test_scan_wrong_devices_found(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    callback = asyncio.Queue()

    @dataclass
    class MockDevice:
        address: str = "address"

    @dataclass
    class MockAdvData:
        local_name: str = "GoPro 1234"

    class MockBleakScanner:
        def __init__(self, *args, **kwargs) -> None:
            self.callback = kwargs["detection_callback"]

        async def __aenter__(self, *args, **kwargs):
            await callback.put(self.callback)
            return self

        async def __aexit__(self, *_) -> None:
            pass

    async def provide_device():
        cb = await callback.get()
        cb(MockDevice(), MockAdvData())

    monkeypatch.setattr("bleak.BleakScanner", MockBleakScanner)

    with pytest.raises(FailedToFindDevice):
        await asyncio.gather(
            mock_bleak_wrapper.scan(
                token=re.compile(r"something_else"),
                timeout=1,
                service_uuids=[GoProUUIDs.CQ_QUERY],
            ),
            provide_device(),
        )


@pytest.mark.asyncio
async def test_scan_timeout(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    class MockBleakScanner:
        def __init__(self, *args, **kwargs) -> None:
            ...

        async def __aenter__(self, *args, **kwargs):
            return self

        async def __aexit__(self, *_) -> None:
            pass

    monkeypatch.setattr("bleak.BleakScanner", MockBleakScanner)

    # Validate error if timeout
    with pytest.raises(FailedToFindDevice):
        await mock_bleak_wrapper.scan(
            token=re.compile(r"something_else"),
            timeout=1,
            service_uuids=[GoProUUIDs.CQ_QUERY],
        )


@pytest.mark.asyncio
async def test_connect_success(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    class MockBleakClient:
        def __init__(self, *args, **kwargs) -> None:
            self.is_connected = False

        async def connect(self, *args, **kwargs):
            self.is_connected = True

    @dataclass
    class MockDevice:
        address: str = "address"

    monkeypatch.setattr("bleak.BleakClient", MockBleakClient)
    client = await mock_bleak_wrapper.connect(lambda *args: None, MockDevice())
    assert client.is_connected


@pytest.mark.asyncio
async def test_connect_timeout(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    class MockBleakClient:
        def __init__(self, *args, **kwargs) -> None:
            self.is_connected = False

        async def connect(self, *args, **kwargs):
            raise asyncio.exceptions.TimeoutError

    @dataclass
    class MockDevice:
        address: str = "address"

    monkeypatch.setattr("bleak.BleakClient", MockBleakClient)
    with pytest.raises(ConnectFailed):
        await mock_bleak_wrapper.connect(lambda *args: None, MockDevice())


@pytest.mark.asyncio
async def test_connect_fail_during_establishment(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    callback = asyncio.Queue()

    class MockBleakClient:
        def __init__(self, *args, **kwargs) -> None:
            self.is_connected = False
            self.callback = kwargs["disconnected_callback"]

        async def connect(self, *args, **kwargs):
            await callback.put(self.callback)

    @dataclass
    class MockDevice:
        address: str = "address"

    async def disconnect():
        cb = await callback.get()
        cb()

    monkeypatch.setattr("bleak.BleakClient", MockBleakClient)
    with pytest.raises(ConnectFailed):
        await asyncio.gather(
            mock_bleak_wrapper.connect(lambda *args: None, MockDevice()),
            disconnect(),
        )


@pytest.mark.asyncio
async def test_discovery(mock_bleak_wrapper: BleakWrapperController):
    @dataclass
    class MockDescriptor:
        handle: int = 0
        uuid: BleUUID = GoProUUIDs.ACC_APPEARANCE
        description: str = "descriptor"

    @dataclass
    class MockChar:
        descriptors: list[MockDescriptor] = field(default_factory=lambda: [MockDescriptor()])
        handle: int = 1
        uuid: BleUUID = GoProUUIDs.ACC_CENTRAL_ADDR_RES
        properties: list[str] = field(default_factory=lambda: ["broadcast", "read"])
        description: str = "characteristic"

    @dataclass
    class MockService:
        characteristics: list[MockChar] = field(default_factory=lambda: [MockChar()])
        handle: int = 2
        uuid: BleUUID = GoProUUIDs.ACC_DEVICE_NAME
        description: str = "service"

    @dataclass
    class MockBleakClient:
        services: list[MockService] = field(default_factory=lambda: [MockService()])

        async def read_gatt_descriptor(self, *args):
            return 0

    gatt_db = await mock_bleak_wrapper.discover_chars(MockBleakClient(), uuids=GoProUUIDs)
    assert len(gatt_db.services) == 1
    assert len(gatt_db.characteristics) == 1
    assert len(list(gatt_db.characteristics.values())[0].descriptors) == 1
