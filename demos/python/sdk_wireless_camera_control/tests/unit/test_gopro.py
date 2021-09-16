# test_gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Sep 10 01:35:03 UTC 2021

# pylint: disable=redefined-outer-name
# pylint: disable=missing-return-doc

"""Unit testing of GoPro Client"""

from open_gopro.responses import GoProResp
import pytest

from open_gopro.gopro import GoPro
from open_gopro.ble import UUID
from open_gopro.exceptions import InvalidConfiguration
from open_gopro.constants import CmdId


@pytest.mark.asyncio
def test_gopro_is_instanciated(gopro_client: GoPro):
    assert gopro_client.version == "1.0"
    assert gopro_client.identifier is None
    assert gopro_client._is_ble_initialized
    with pytest.raises(InvalidConfiguration):
        assert gopro_client.is_busy
    with pytest.raises(InvalidConfiguration):
        assert gopro_client.is_encoding


@pytest.mark.asyncio
def test_gopro_open(gopro_client: GoPro):
    gopro_client.open()
    assert gopro_client.is_ble_connected
    assert gopro_client.is_wifi_connected
    assert gopro_client.identifier == "scanned_device"


@pytest.mark.asyncio
def test_get_update(gopro_client: GoPro):
    gopro_client._out_q.put(1)
    assert gopro_client.get_update() == 1


@pytest.mark.asyncio
def test_keep_alive(gopro_client: GoPro):
    assert gopro_client.keep_alive()


@pytest.mark.asyncio
def test_notification_handler(gopro_client: GoPro):
    response = gopro_client._write_characteristic_receive_notification(
        UUID.CQ_COMMAND,
        bytearray([0x03, 0x01, 0x01, 0x01]),
        response_data=[bytearray([0x02, 0x01, 0x00])],
        response_uuid=UUID.CQ_COMMAND_RESP,
        response_id=CmdId.SET_SHUTTER,
    )
    assert response.is_ok


@pytest.mark.asyncio
def test_gopro_close(gopro_client: GoPro):
    gopro_client.close()
    assert not gopro_client.is_ble_connected
