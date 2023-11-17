# test_gopro_ble.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

# pylint: disable=redefined-outer-name


"""Unit testing of GoPro BLE Client"""

import re

import pytest

from open_gopro.ble import BleClient
from open_gopro.exceptions import ConnectFailed, FailedToFindDevice


def disconnection_handler(_) -> None:
    print("Entered test disconnect callback")


def test_gopro_ble_client_instantiation(mock_ble_client: BleClient):
    assert not mock_ble_client.is_discovered
    assert not mock_ble_client.is_connected


@pytest.mark.asyncio
async def test_gopro_ble_client_failed_to_find_device(mock_ble_client: BleClient):
    mock_ble_client._target = re.compile("invalid_device")
    with pytest.raises(FailedToFindDevice):
        await mock_ble_client._find_device()
    assert not mock_ble_client.is_discovered
    assert not mock_ble_client.is_connected


@pytest.mark.asyncio
async def test_gopro_ble_client_failed_to_connect(mock_ble_client: BleClient):
    mock_ble_client._target = re.compile("device")
    mock_ble_client._disconnected_cb = None
    with pytest.raises(ConnectFailed):
        await mock_ble_client.open()
    assert mock_ble_client.is_discovered
    assert not mock_ble_client.is_connected


@pytest.mark.asyncio
async def test_gopro_ble_client_open(mock_ble_client: BleClient):
    mock_ble_client._disconnected_cb = disconnection_handler
    await mock_ble_client.open()
    assert mock_ble_client.is_discovered
    assert mock_ble_client.is_connected


@pytest.mark.asyncio
async def test_gopro_ble_client_identifier(mock_ble_client: BleClient):
    assert mock_ble_client.identifier == "scanned_device"


@pytest.mark.asyncio
async def test_gopro_ble_client_read(mock_ble_client: BleClient):
    assert await mock_ble_client.read("uuid") == bytearray()


@pytest.mark.asyncio
async def test_gopro_ble_client_write(mock_ble_client: BleClient):
    await mock_ble_client.write("uuid", bytearray())
    assert True


@pytest.mark.asyncio
async def test_gopro_ble_client_close(mock_ble_client: BleClient):
    await mock_ble_client.close()
    assert not mock_ble_client.is_connected
