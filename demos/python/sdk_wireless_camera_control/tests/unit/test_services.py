# test_services.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:54 PM

# pylint: disable = redefined-outer-name

from typing import List, Dict

from open_gopro.constants import BleUUID
from open_gopro.ble import Descriptor, Characteristic, Service, GattDB, BleClient


def test_descriptor(descriptor: Descriptor):
    assert len(str(descriptor))


def test_characteristic(characteristic: Characteristic):
    assert len(str(characteristic))


def test_service(service: Service):
    assert len(str(service))


def test_attribute_table(attribute_table: GattDB):
    assert len(attribute_table.services) == 2
    assert len(attribute_table.services[BleUUID.S_CONTROL_QUERY].chars) == 2


def test_handle2uuid(attribute_table: GattDB):
    assert attribute_table.handle2uuid(0xABCD) is BleUUID.CQ_QUERY


def test_services_to_csv(attribute_table: GattDB, ble_client: BleClient):
    ble_client._gatt_table = attribute_table
    ble_client.services_as_csv()
