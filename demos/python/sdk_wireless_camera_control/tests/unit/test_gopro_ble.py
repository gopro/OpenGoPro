# test_gopro_ble.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

# pylint: disable=redefined-outer-name
# pylint: disable=missing-return-doc

"""Unit testing of GoPro BLE Client"""

import re

import pytest

from open_gopro.ble import BleClient
from open_gopro.exceptions import ConnectFailed, FailedToFindDevice


def disconnection_handler(_) -> None:
    print("Entered test disconnect callback")


@pytest.mark.asyncio
def test_gopro_ble_client_instantiation(ble_client: BleClient):
    assert not ble_client.is_discovered
    assert not ble_client.is_connected


@pytest.mark.asyncio
def test_gopro_ble_client_failed_to_find_device(ble_client: BleClient):
    ble_client._target = re.compile("invalid_device")
    with pytest.raises(FailedToFindDevice):
        ble_client._find_device()
    assert not ble_client.is_discovered
    assert not ble_client.is_connected


@pytest.mark.asyncio
def test_gopro_ble_client_failed_to_connect(ble_client: BleClient):
    ble_client._target = re.compile("device")
    ble_client._disconnected_cb = None
    with pytest.raises(ConnectFailed):
        ble_client.open()
    assert ble_client.is_discovered
    assert not ble_client.is_connected


@pytest.mark.asyncio
def test_gopro_ble_client_open(ble_client: BleClient):
    ble_client._disconnected_cb = disconnection_handler
    ble_client.open()
    assert ble_client.is_discovered
    assert ble_client.is_connected


@pytest.mark.asyncio
def test_gopro_ble_client_identifier(ble_client: BleClient):
    assert ble_client.identifier == "scanned_device"


@pytest.mark.asyncio
def test_gopro_ble_client_read(ble_client: BleClient):
    assert ble_client.read("uuid") == bytearray()


@pytest.mark.asyncio
def test_gopro_ble_client_write(ble_client: BleClient):
    ble_client.write("uuid", bytearray())
    assert True


@pytest.mark.asyncio
def test_get_gatt_table(ble_client: BleClient):
    ble_client._gatt_table = None
    assert ble_client.gatt_db is not None


@pytest.mark.asyncio
def test_gopro_ble_client_close(ble_client: BleClient):
    ble_client.close()
    assert not ble_client.is_connected
