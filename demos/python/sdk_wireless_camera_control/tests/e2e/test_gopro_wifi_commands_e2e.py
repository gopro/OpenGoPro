# test_gopro_wifi_commands_e2e.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""End to end testing of GoPro BLE functionality"""

from pathlib import Path

import pytest

from open_gopro import GoPro
from open_gopro.api import api_versions


@pytest.mark.asyncio
async def test_get_media_list(gopro_ble_and_wifi: GoPro):
    assert gopro_ble_and_wifi.wifi_command.get_media_list().is_ok


@pytest.mark.asyncio
async def test_get_state(gopro_ble_and_wifi: GoPro):
    assert gopro_ble_and_wifi.wifi_command.get_camera_state().is_ok


@pytest.mark.asyncio
async def test_get_version(gopro_ble_and_wifi: GoPro):
    result = gopro_ble_and_wifi.wifi_command.get_open_gopro_api_version()
    assert result.is_ok
    assert result.flatten in list(api_versions.keys())


@pytest.mark.asyncio
async def test_set_turbo_mode(gopro_ble_and_wifi: GoPro):
    print("Setting turbo mode on")
    assert gopro_ble_and_wifi.wifi_command.set_turbo_mode(gopro_ble_and_wifi.params.Toggle.ENABLE).is_ok
    print("Setting turbo mode off")
    assert gopro_ble_and_wifi.wifi_command.set_turbo_mode(gopro_ble_and_wifi.params.Toggle.DISABLE).is_ok


@pytest.mark.asyncio
async def test_set_cinematic_mode(gopro_ble_and_wifi: GoPro):
    assert gopro_ble_and_wifi.wifi_command.set_preset(gopro_ble_and_wifi.params.Preset.CINEMATIC)


@pytest.mark.asyncio
async def test_set_resolution(gopro_ble_and_wifi: GoPro):
    for resolution in [
        res
        for res in gopro_ble_and_wifi.params.Resolution
        if res is not gopro_ble_and_wifi.params.Resolution.NOT_APPLICABLE
    ]:
        print(f"Setting resolution to {resolution.name}")
        assert gopro_ble_and_wifi.wifi_setting.resolution.set(resolution).is_ok


@pytest.mark.asyncio
async def test_download_photo(gopro_ble_and_wifi: GoPro):
    media_list = gopro_ble_and_wifi.wifi_command.get_media_list()["media"][0]["fs"]
    # Find a picture and download it
    picture = ""
    for file in [x["n"] for x in media_list]:
        if file.lower().endswith(".jpg"):
            picture = file
            write_location = Path("out.jpg")
            gopro_ble_and_wifi.wifi_command.download_file(camera_file=picture, local_file=write_location)
            assert write_location.exists()
            return
    assert False
