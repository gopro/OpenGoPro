# test_gopro_ble_e2e.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""End to end testing of GoPro BLE Client"""

import pytest

from open_gopro.communication_client import GoProBle


def disconnected_cb(_) -> None:
    print("Entered test disconnect callback")


def notification_cb(handle: int, data: bytearray) -> None:
    print("Entered test notification callback")


@pytest.mark.asyncio
def test_bleak_not_open(gopro_bleak_client: GoProBle):
    assert not gopro_bleak_client._ble.is_discovered
    assert not gopro_bleak_client._ble.is_connected
    assert gopro_bleak_client._ble.identifier is None


@pytest.mark.asyncio
def test_bleak_open(gopro_bleak_client: GoProBle):
    gopro_bleak_client._ble.open()
    assert gopro_bleak_client._ble.is_discovered
    assert gopro_bleak_client._ble.is_connected
    assert gopro_bleak_client._ble.identifier is not None


@pytest.mark.asyncio
def test_bleak_attributes_discovered(gopro_bleak_client: GoProBle):
    assert len(gopro_bleak_client._ble.gatt_db.services) > 0
    gopro_bleak_client._ble.services_as_csv()


# @pytest.mark.asyncio
# def test_bleak_write(gopro_bleak_client: GoProBle):
#     gopro_bleak_client.write(uuid, data)

# @pytest.mark.asyncio
# def test_bleak_read(gopro_bleak_client: GoProBle):
#     result = gopro_bleak_client.read(uuid)


@pytest.mark.asyncio
def test_bleak_close(gopro_bleak_client: GoProBle):
    gopro_bleak_client._ble.close()
    assert not gopro_bleak_client._ble.is_connected
