# test_settings.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025


import pytest

from open_gopro import WirelessGoPro
from open_gopro.models.constants import settings
from open_gopro.network.wifi.adapters.wireless import WifiCli


@pytest.mark.timeout(60)
async def test_enable_auto_access(wireless_gopro_ble: WirelessGoPro):
    assert (
        await wireless_gopro_ble.ble_setting.automatic_wi_fi_access_point.set(settings.AutomaticWi_FiAccessPoint.ON)
    ).ok

    password = (await wireless_gopro_ble.ble_command.get_wifi_password()).data
    ssid = (await wireless_gopro_ble.ble_command.get_wifi_ssid()).data

    scanner = WifiCli()

    assert await scanner.connect(ssid, password)


@pytest.mark.timeout(60)
async def test_enable_auto_access_point_and_connect(wireless_gopro_ble: WirelessGoPro):
    assert (
        await wireless_gopro_ble.ble_setting.automatic_wi_fi_access_point.set(settings.AutomaticWi_FiAccessPoint.ON)
    ).ok

    password = (await wireless_gopro_ble.ble_command.get_wifi_password()).data
    ssid = (await wireless_gopro_ble.ble_command.get_wifi_ssid()).data

    scanner = WifiCli()

    assert await scanner.connect(ssid, password)
