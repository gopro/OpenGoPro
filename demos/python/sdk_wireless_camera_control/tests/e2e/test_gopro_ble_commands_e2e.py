# test_gopro_ble_commands_e2e.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""End to end testing of GoPro BLE functionality"""

import time

import pytest

from open_gopro import GoPro
from open_gopro.api.v1_0 import params


@pytest.mark.asyncio
async def test_get_individual_statuses(gopro_ble_no_wifi: GoPro):
    for status in gopro_ble_no_wifi.ble_status:
        print(f"Getting {status} value...")
        assert status.get_value().is_ok


@pytest.mark.asyncio
async def test_get_all_statuses(gopro_ble_no_wifi: GoPro):
    assert gopro_ble_no_wifi.ble_command.get_camera_statuses()


@pytest.mark.asyncio
async def test_get_all_settings(gopro_ble_no_wifi: GoPro):
    assert gopro_ble_no_wifi.ble_command.get_camera_settings()


@pytest.mark.asyncio
async def test_get_individual_setting_values(gopro_ble_no_wifi: GoPro):
    for setting in gopro_ble_no_wifi.ble_setting:
        print(f"Getting {setting.identifier} value...")
        result = setting.get_value()
        assert result.is_ok


@pytest.mark.asyncio
async def test_register_setting_value_updates(gopro_ble_no_wifi: GoPro):
    for setting in gopro_ble_no_wifi.ble_setting:
        print(f"Registering for value updates for {setting.identifier}...")
        assert setting.register_value_update()
        print(f"Unregistering for value updates for {setting.identifier}...")
        assert setting.unregister_value_update()


@pytest.mark.asyncio
async def test_register_setting_capability_updates(gopro_ble_no_wifi: GoPro):
    for setting in gopro_ble_no_wifi.ble_setting:
        print(f"Registering for capability updates for {setting.identifier}...")
        assert setting.register_capability_update()
        print(f"Unregistering for capability updates for {setting.identifier}...")
        assert setting.unregister_capability_update()


@pytest.mark.asyncio
async def test_get_setting_capabilities(gopro_ble_no_wifi: GoPro):
    for setting in gopro_ble_no_wifi.ble_setting:
        print(f"Getting {setting.identifier} capabilities...")
        assert setting.get_capabilities_values().is_ok


@pytest.mark.asyncio
async def test_get_wifi_ssid(gopro_ble_no_wifi: GoPro):
    result = gopro_ble_no_wifi.ble_command.get_wifi_ssid()
    assert result.is_ok
    assert len(result.flatten)


@pytest.mark.asyncio
async def test_get_wifi_password(gopro_ble_no_wifi: GoPro):
    result = gopro_ble_no_wifi.ble_command.get_wifi_password()
    assert result.is_ok
    assert len(result.flatten)


@pytest.mark.asyncio
async def test_toggle_wifi_ap(gopro_ble_no_wifi: GoPro):
    print("Setting WiFI AP on...")
    assert gopro_ble_no_wifi.ble_command.enable_wifi_ap(True).is_ok
    print("Setting Wifi AP off...")
    assert gopro_ble_no_wifi.ble_command.enable_wifi_ap(True).is_ok


@pytest.mark.asyncio
async def test_shutter(gopro_ble_no_wifi: GoPro):
    print("Setting shutter on...")
    assert gopro_ble_no_wifi.ble_command.set_shutter(gopro_ble_no_wifi.params.Shutter.ON).is_ok
    time.sleep(1)
    print("Setting shutter off...")
    assert gopro_ble_no_wifi.ble_command.set_shutter(gopro_ble_no_wifi.params.Shutter.OFF).is_ok


@pytest.mark.asyncio
async def test_cycle_presets(gopro_ble_no_wifi: GoPro):
    for preset in gopro_ble_no_wifi.params.Preset:
        print(f"Setting {preset=}")
        assert gopro_ble_no_wifi.ble_command.load_preset(preset).is_ok


@pytest.mark.asyncio
async def test_turbo_mode(gopro_ble_no_wifi: GoPro):
    if gopro_ble_no_wifi.version == "1.0":
        pytest.skip("HERO9 not accepting Turbo Mode Off")
    response = gopro_ble_no_wifi.ble_command.set_turbo_mode(True)
    assert response.is_ok
    response = gopro_ble_no_wifi.ble_command.set_turbo_mode(False)
    assert response.is_ok


@pytest.mark.asyncio
async def test_cycle_resolutions(gopro_ble_no_wifi: GoPro):
    assert gopro_ble_no_wifi.ble_command.load_preset(gopro_ble_no_wifi.params.Preset.CINEMATIC).is_ok
    time.sleep(2)
    response = gopro_ble_no_wifi.ble_setting.resolution.get_capabilities_values()
    assert response.is_ok
    for resolution in response.flatten:
        print(f"Setting resolution to {str(resolution)}")
        assert gopro_ble_no_wifi.ble_setting.resolution.set(resolution).is_ok


@pytest.mark.asyncio
async def test_narrow_param_value(gopro_ble_no_wifi: GoPro):
    version = gopro_ble_no_wifi.version
    if version == "1.0":
        assert gopro_ble_no_wifi.params.VideoFOV.NARROW.value == 6
    elif version == "2.0":
        assert gopro_ble_no_wifi.params.VideoFOV.NARROW.value == 2
    else:
        pytest.fail(f"Need to implement test for version {version}")
