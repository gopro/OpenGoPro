# test_gopro_ble.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

# pylint: disable=redefined-outer-name


"""Unit testing of GoPro Wifi Client"""

import pytest

from open_gopro.domain.exceptions import ConnectFailed
from open_gopro.network.wifi import WifiClient


async def test_gopro_wifi_client_failed_to_connect(mock_wifi_client: WifiClient):
    with pytest.raises(ConnectFailed):
        await mock_wifi_client.open("test_ssid", "invalid_password")


async def test_gopro_wifi_client_open(mock_wifi_client: WifiClient):
    await mock_wifi_client.open("test_ssid", "password")
    assert mock_wifi_client.ssid == "test_ssid"
    assert mock_wifi_client.password == "password"


def test_gopro_wifi_client_is_connected(mock_wifi_client: WifiClient):
    assert mock_wifi_client.is_connected


async def test_gopro_wifi_client_close(mock_wifi_client: WifiClient):
    await mock_wifi_client.close()
