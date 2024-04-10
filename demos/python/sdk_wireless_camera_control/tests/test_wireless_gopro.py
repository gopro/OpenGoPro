# test_Wirelessgopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://Wirelessgopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Sep 10 01:35:03 UTC 2021

# pylint: disable=redefined-outer-name


"""Unit testing of GoPro Client"""

import asyncio
from pathlib import Path

import pytest
import requests
import requests_mock

from open_gopro.communicator_interface import HttpMessage
from open_gopro.constants import SettingId, StatusId
from open_gopro.exceptions import GoProNotOpened, ResponseTimeout
from open_gopro.gopro_wireless import Params, WirelessGoPro, types
from open_gopro.models.response import GlobalParsers
from tests import mock_good_response


@pytest.mark.asyncio
async def test_lifecycle(mock_wireless_gopro: WirelessGoPro):
    async def set_disconnect_event():
        mock_wireless_gopro._disconnect_handler(None)

    # We're not yet open so can't send commands
    assert not mock_wireless_gopro.is_open
    with pytest.raises(GoProNotOpened):
        await mock_wireless_gopro.ble_command.enable_wifi_ap(enable=False)

    # Mock ble / wifi open
    await mock_wireless_gopro.open()
    assert mock_wireless_gopro.is_open

    # Ensure we can't send commands because not ready
    assert not await mock_wireless_gopro.is_ready
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(mock_wireless_gopro.ble_command.enable_wifi_ap(enable=False), 1)

    # Mock receiving initial not-encoding and not-busy statuses
    await mock_wireless_gopro._update_internal_state(update=StatusId.ENCODING, value=False)
    await mock_wireless_gopro._update_internal_state(update=StatusId.SYSTEM_BUSY, value=False)
    assert await mock_wireless_gopro.is_ready

    results = await asyncio.gather(
        mock_wireless_gopro.ble_command.enable_wifi_ap(enable=False),
        mock_wireless_gopro._sync_resp_ready_q.put(mock_good_response),
    )

    assert results[0].ok
    assert await mock_wireless_gopro.ble_command.get_open_gopro_api_version()

    # Mock closing
    asyncio.gather(mock_wireless_gopro.close(), set_disconnect_event())
    assert mock_wireless_gopro._keep_alive_task.cancelled


@pytest.mark.asyncio
async def test_gopro_open(mock_wireless_gopro_basic: WirelessGoPro):
    await mock_wireless_gopro_basic.open()
    assert mock_wireless_gopro_basic.is_ble_connected
    assert mock_wireless_gopro_basic.is_http_connected
    assert mock_wireless_gopro_basic.identifier == "scanned_device"


@pytest.mark.asyncio
async def test_http_get(mock_wireless_gopro_basic: WirelessGoPro, monkeypatch):
    message = HttpMessage("gopro/camera/stream/start", None)
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(mock_wireless_gopro_basic._base_url + message._endpoint, adapter)
    adapter.register_uri("GET", mock_wireless_gopro_basic._base_url + message._endpoint, json="{}")
    monkeypatch.setattr("open_gopro.gopro_base.requests.get", session.get)
    response = await mock_wireless_gopro_basic._get_json(message)
    assert response.ok


@pytest.mark.asyncio
async def test_http_file(mock_wireless_gopro_basic: WirelessGoPro, monkeypatch):
    message = HttpMessage("videos/DCIM/100GOPRO/dummy.MP4", None)
    out_file = Path("test.mp4")
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(mock_wireless_gopro_basic._base_url + message._endpoint, adapter)
    adapter.register_uri("GET", mock_wireless_gopro_basic._base_url + message._endpoint, text="BINARY DATA")
    monkeypatch.setattr("open_gopro.gopro_base.requests.get", session.get)
    await mock_wireless_gopro_basic._get_stream(message, camera_file=out_file, local_file=out_file)
    assert out_file.exists()


@pytest.mark.asyncio
async def test_http_response_timeout(mock_wireless_gopro_basic: WirelessGoPro, monkeypatch):
    with pytest.raises(ResponseTimeout):
        message = HttpMessage("gopro/camera/stream/start", None)
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount(mock_wireless_gopro_basic._base_url + message._endpoint, adapter)
        adapter.register_uri(
            "GET", mock_wireless_gopro_basic._base_url + message._endpoint, exc=requests.exceptions.ConnectTimeout
        )
        monkeypatch.setattr("open_gopro.gopro_base.requests.get", session.get)
        await mock_wireless_gopro_basic._get_json(message, timeout=1)


@pytest.mark.asyncio
async def test_http_response_error(mock_wireless_gopro_basic: WirelessGoPro, monkeypatch):
    message = HttpMessage("gopro/camera/stream/start", None)
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(mock_wireless_gopro_basic._base_url + message._endpoint, adapter)
    adapter.register_uri(
        "GET",
        mock_wireless_gopro_basic._base_url + message._endpoint,
        status_code=403,
        reason="something bad happened",
        json="{}",
    )
    monkeypatch.setattr("open_gopro.gopro_base.requests.get", session.get)
    response = await mock_wireless_gopro_basic._get_json(message)
    assert not response.ok


@pytest.mark.asyncio
async def test_get_update(mock_wireless_gopro_basic: WirelessGoPro):
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    event = asyncio.Event()

    async def receive_encoding_status(id: types.UpdateType, value: bool):
        event.set()

    mock_wireless_gopro_basic.register_update(receive_encoding_status, StatusId.ENCODING)
    not_encoding = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    mock_wireless_gopro_basic._notification_handler(0xFF, not_encoding)
    await event.wait()

    # Now ensure unregistering works
    event.clear()
    mock_wireless_gopro_basic.unregister_update(receive_encoding_status, StatusId.ENCODING)
    not_encoding = bytearray([0x05, 0x13, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    mock_wireless_gopro_basic._notification_handler(0xFF, not_encoding)
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(event.wait(), 1)


@pytest.mark.asyncio
async def test_get_update_unregister_all(mock_wireless_gopro_basic: WirelessGoPro):
    event = asyncio.Event()
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()

    async def receive_encoding_status(id: types.UpdateType, value: bool):
        event.set()

    mock_wireless_gopro_basic.register_update(receive_encoding_status, StatusId.ENCODING)
    not_encoding = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    mock_wireless_gopro_basic._notification_handler(0xFF, not_encoding)
    await event.wait()

    # Now ensure unregistering works
    event.clear()
    mock_wireless_gopro_basic.unregister_update(receive_encoding_status)
    not_encoding = bytearray([0x05, 0x13, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    mock_wireless_gopro_basic._notification_handler(0xFF, not_encoding)
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(event.wait(), 1)


def test_get_param_values_by_id():
    vector = list(Params.Resolution)[0]
    assert GlobalParsers.get_query_container(SettingId.RESOLUTION)(vector.value) == vector
