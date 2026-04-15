# test_bleak_wrapper.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""Unit testing of bleak controller"""

import asyncio
import re
from dataclasses import dataclass, field

import pytest

from open_gopro.domain.exceptions import ConnectFailed, FailedToFindDevice
from open_gopro.models.constants import GoProUUID
from open_gopro.network.ble import BleUUID
from open_gopro.network.ble.adapters.bleak_wrapper import BleakWrapperController


async def test_singleton(mock_bleak_wrapper: BleakWrapperController):
    new_bleak_wrapper = BleakWrapperController()
    assert mock_bleak_wrapper is new_bleak_wrapper


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
            service_uuids=[GoProUUID.CQ_QUERY],
        ),
        provide_device(),
    )
    assert results[0].address == "address"


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
                service_uuids=[GoProUUID.CQ_QUERY],
            ),
            provide_device(),
        )


async def test_scan_timeout(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    class MockBleakScanner:
        def __init__(self, *args, **kwargs) -> None: ...

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
            service_uuids=[GoProUUID.CQ_QUERY],
        )


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


async def test_discovery(mock_bleak_wrapper: BleakWrapperController):
    @dataclass
    class MockDescriptor:
        handle: int = 0
        uuid: BleUUID = GoProUUID.ACC_APPEARANCE
        description: str = "descriptor"

    @dataclass
    class MockChar:
        descriptors: list[MockDescriptor] = field(default_factory=lambda: [MockDescriptor()])
        handle: int = 1
        uuid: BleUUID = GoProUUID.ACC_CENTRAL_ADDR_RES
        properties: list[str] = field(default_factory=lambda: ["broadcast", "read"])
        description: str = "characteristic"

    @dataclass
    class MockService:
        characteristics: list[MockChar] = field(default_factory=lambda: [MockChar()])
        handle: int = 2
        uuid: BleUUID = GoProUUID.ACC_DEVICE_NAME
        description: str = "service"

    @dataclass
    class MockBleakClient:
        services: list[MockService] = field(default_factory=lambda: [MockService()])

        async def read_gatt_descriptor(self, *args):
            return 0

    gatt_db = await mock_bleak_wrapper.discover_chars(MockBleakClient(), uuids=GoProUUID)
    assert len(gatt_db.services) == 1
    assert len(gatt_db.characteristics) == 1
    assert len(list(gatt_db.characteristics.values())[0].descriptors) == 1


async def test_concurrent_writes_to_same_characteristic(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    """Test that concurrent writes to the same characteristic both complete.

    Verifies the contract that when two writes to the same characteristic are issued
    concurrently, both writes must complete successfully without any being orphaned.
    """
    completed_writes = []

    @dataclass
    class MockBleakClient:
        async def write_gatt_char(self, uuid: str, data: bytes, response: bool = False):
            # Simulate BLE write taking some time
            await asyncio.sleep(0.05)
            completed_writes.append(data)

    client = MockBleakClient()
    test_uuid = GoProUUID.CQ_QUERY

    # Launch two concurrent writes to the same characteristic
    async def write_1():
        await mock_bleak_wrapper.write(client, test_uuid, b"data1")

    async def write_2():
        await mock_bleak_wrapper.write(client, test_uuid, b"data2")

    # Both writes should complete without error
    await asyncio.gather(write_1(), write_2())

    # Verify both writes completed (order may vary, but both must finish)
    assert b"data1" in completed_writes
    assert b"data2" in completed_writes
    assert len(completed_writes) == 2


async def test_ble_writes_are_serialized(mock_bleak_wrapper: BleakWrapperController, monkeypatch):
    """Test that BLE writes are serialized (not concurrent) via lock.

    This ensures the lock is working - writes should execute in sequence,
    not overlap.
    """
    execution_log = []

    @dataclass
    class MockBleakClient:
        async def write_gatt_char(self, uuid: str, data: bytes, response: bool = False):
            execution_log.append(f"write_start:{data}")
            await asyncio.sleep(0.02)  # Simulate BLE latency
            execution_log.append(f"write_end:{data}")

    client = MockBleakClient()
    test_uuid = GoProUUID.CQ_QUERY

    # Launch concurrent writes
    await asyncio.gather(
        mock_bleak_wrapper.write(client, test_uuid, b"A"),
        mock_bleak_wrapper.write(client, test_uuid, b"B"),
    )

    # With serialization, writes should NOT interleave
    # Either: start_A, end_A, start_B, end_B  OR  start_B, end_B, start_A, end_A
    assert len(execution_log) == 4

    # Check that writes don't interleave (start-end pairs are adjacent)
    if execution_log[0] == "write_start:b'A'":
        assert execution_log[1] == "write_end:b'A'"
        assert execution_log[2] == "write_start:b'B'"
        assert execution_log[3] == "write_end:b'B'"
    else:
        assert execution_log[0] == "write_start:b'B'"
        assert execution_log[1] == "write_end:b'B'"
        assert execution_log[2] == "write_start:b'A'"
        assert execution_log[3] == "write_end:b'A'"
