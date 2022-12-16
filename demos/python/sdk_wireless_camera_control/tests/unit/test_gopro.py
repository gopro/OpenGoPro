# test_Wirelessgopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://Wirelessgopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Sep 10 01:35:03 UTC 2021

# pylint: disable=redefined-outer-name


"""Unit testing of GoPro Client"""

import time
import threading
from pathlib import Path

import pytest
import requests
import requests_mock

from open_gopro.gopro_wireless import WirelessGoPro, Params, GoProResp
from open_gopro.exceptions import InvalidConfiguration, ResponseTimeout, GoProNotOpened
from open_gopro.constants import StatusId, SettingId

ready = False


def test_control():
    assert True


def test_ble_threads_start(gopro_client_maintain_ble: WirelessGoPro):
    def open_client():
        gopro_client_maintain_ble.open()
        global ready
        ready = True

    threading.Thread(target=open_client, daemon=True).start()
    while not ready:
        time.sleep(0.1)
    not_encoding = bytearray([0x05, 0x13, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    gopro_client_maintain_ble._notification_handler(0xFF, not_encoding)
    not_busy = bytearray([0x05, 0x13, 0x00, StatusId.SYSTEM_BUSY.value, 0x01, 0x00])
    gopro_client_maintain_ble._notification_handler(0xFF, not_busy)
    assert not gopro_client_maintain_ble.is_busy
    assert not gopro_client_maintain_ble.is_encoding


def test_gopro_open(gopro_client: WirelessGoPro):
    gopro_client.open()
    assert gopro_client.is_ble_connected
    assert gopro_client.is_http_connected
    assert gopro_client.identifier == "scanned_device"


def test_http_get(gopro_client: WirelessGoPro, monkeypatch):
    endpoint = "gopro/camera/stream/start"
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(gopro_client._base_url + endpoint, adapter)
    adapter.register_uri("GET", gopro_client._base_url + endpoint, json="{}")
    monkeypatch.setattr("open_gopro.gopro_base.requests.get", session.get)
    response = gopro_client._get(endpoint)
    assert response.is_ok


def test_http_file(gopro_client: WirelessGoPro, monkeypatch):
    out_file = Path("test.mp4")
    endpoint = "videos/DCIM/100GOPRO/dummy.MP4"
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(gopro_client._base_url + endpoint, adapter)
    adapter.register_uri("GET", gopro_client._base_url + endpoint, text="BINARY DATA")
    monkeypatch.setattr("open_gopro.gopro_base.requests.get", session.get)
    gopro_client._stream_to_file(endpoint, out_file)
    assert out_file.exists()


def test_http_response_timeout(gopro_client: WirelessGoPro, monkeypatch):
    with pytest.raises(ResponseTimeout):
        endpoint = "gopro/camera/stream/start"
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount(gopro_client._base_url + endpoint, adapter)
        adapter.register_uri("GET", gopro_client._base_url + endpoint, exc=requests.exceptions.ConnectTimeout)
        monkeypatch.setattr("open_gopro.gopro_base.requests.get", session.get)
        gopro_client._get(endpoint)


def test_http_response_error(gopro_client: WirelessGoPro, monkeypatch):
    endpoint = "gopro/camera/stream/start"
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(gopro_client._base_url + endpoint, adapter)
    adapter.register_uri(
        "GET", gopro_client._base_url + endpoint, status_code=403, reason="something bad happened", json="{}"
    )
    monkeypatch.setattr("open_gopro.gopro_base.requests.get", session.get)
    response = gopro_client._get(endpoint)
    assert not response.is_ok


def test_get_update(gopro_client: WirelessGoPro):
    gopro_client._out_q.put(1)
    assert gopro_client.get_notification() == 1


def test_keep_alive(gopro_client: WirelessGoPro):
    assert gopro_client.keep_alive()


def test_get_param_values_by_id(gopro_client: WirelessGoPro):
    vector = list(Params.Resolution)[0]
    assert GoProResp._get_query_container(SettingId.RESOLUTION)(vector.value) == vector
