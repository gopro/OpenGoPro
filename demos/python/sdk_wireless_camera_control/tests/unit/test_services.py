# test_services.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:54 PM

# pylint: disable = redefined-outer-name

import uuid
from typing import List, Dict

import pytest

from open_gopro.ble.services import UUIDs, UUIDsMeta, UuidLength, BLE_BASE_UUID
from open_gopro.constants import BleUUID
from open_gopro.ble import Descriptor, Characteristic, Service, GattDB, BleUUID
from tests.conftest import gatt_db


def test_128_bit_uuid():
    u = BleUUID("128 bit from str", hex="12345678123456781234567812345678")
    assert len(u.hex)
    u = BleUUID("128 bit from int", int=0x12345678123456781234567812345678)
    assert len(u.hex)
    u = BleUUID("128 bit from bytes", bytes=b"\x12\x34\x56\x78" * 4)
    assert len(u.hex)
    u = BleUUID(
        "128 bit from byte le",
        bytes_le=b"\x78\x56\x34\x12\x34\x12\x78\x56" + b"\x12\x34\x56\x78\x12\x34\x56\x78",
    )
    assert len(u.hex)


def test_16_bit_uuid():
    u = BleUUID("16 bit from str", uuid_format=UuidLength.BIT_16, hex="FEA6")
    assert len(u.hex)
    u = BleUUID("16 bit from int", uuid_format=UuidLength.BIT_16, int=1234)
    assert len(u.hex)
    u = BleUUID("16 bit from bytes", uuid_format=UuidLength.BIT_16, bytes=bytes([0xAB, 0xCD]))
    assert len(u.hex)


def test_uuid_negative():
    with pytest.raises(ValueError):
        u = BleUUID("16 bit from bytes le", uuid_format=UuidLength.BIT_16, bytes_le=bytes([0xCD, 0xAB]))
    with pytest.raises(ValueError):
        u = BleUUID("Multiple inputs", uuid_format=UuidLength.BIT_16, hex="", int=1)
    with pytest.raises(ValueError):
        u = BleUUID("Bad string", uuid_format=UuidLength.BIT_16, hex="AB")
    with pytest.raises(ValueError):
        u = BleUUID("Bad bytes", uuid_format=UuidLength.BIT_16, bytes=bytes([0xAB, 0xCD, 0xEF]))


def test_ble_uuids():
    UUID_STR = "00001801-0000-1000-8000-00805f9b34fb"
    UUID_INT = 486857058725721441610830112830715

    class TestUUIDs(metaclass=UUIDsMeta):
        TEST_UUID = BleUUID("Test", hex=UUID_STR)

    assert UUID_STR in TestUUIDs
    assert BLE_BASE_UUID.format("ABCD") not in TestUUIDs
    assert UUID_INT in TestUUIDs
    assert 0xABCD not in TestUUIDs
    assert TestUUIDs.TEST_UUID in TestUUIDs
    assert uuid.UUID(hex=UUID_STR) in TestUUIDs
    assert TestUUIDs[UUID_STR].hex
    assert TestUUIDs[UUID_INT].hex
    assert TestUUIDs.TEST_UUID.hex
    assert TestUUIDs[uuid.UUID(hex=UUID_STR)].hex
    assert len([x for x in TestUUIDs]) == 1


def test_ble_uuids_negative():
    with pytest.raises(TypeError):

        class TestUUIDs(UUIDs):
            BAD_ATTRIBUTE = 1


def test_descriptor(descriptor: Descriptor):
    assert descriptor.handle > 0
    assert descriptor.name == descriptor.uuid.name


def test_characteristic(characteristic: Characteristic):
    assert characteristic.handle > 0
    assert characteristic.name == characteristic.uuid.name
    assert len(characteristic.descriptors)

    assert characteristic.is_readable
    assert not characteristic.is_writeable
    assert not characteristic.is_notifiable
    assert not characteristic.is_indicatable


def test_service(service: Service):
    assert service.start_handle > 0
    assert service.name == service.uuid.name
    assert len(service.characteristics) > 0


def test_characteristic_view(gatt_db: GattDB):
    # Get all attributes by nested looping through services
    chars: List[Characteristic] = []
    for service in gatt_db.services.values():
        for char in service.characteristics.values():
            chars.append(char)

    assert len(chars) == len(gatt_db.characteristics)

    for char in chars:
        assert char.uuid in gatt_db.characteristics

    for char in gatt_db.characteristics:
        assert len(char.uuid.hex)

    assert list(gatt_db.characteristics.keys()) == [c.uuid for c in chars]
    assert list([c.uuid for c in gatt_db.characteristics.values()]) == [c.uuid for c in chars]


def test_gatt_db(gatt_db: GattDB):
    handles = set([c.handle for c in gatt_db.characteristics])
    uuids = set([c.uuid for c in gatt_db.characteristics])
    assert handles == set([gatt_db.uuid2handle(uuid) for uuid in uuids])
    assert uuids == set([gatt_db.handle2uuid(handle) for handle in handles])

    gatt_db.dump_to_csv()
