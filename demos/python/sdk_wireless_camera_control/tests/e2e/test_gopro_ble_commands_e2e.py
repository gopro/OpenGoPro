# test_gopro_ble_commands_e2e.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""End to end testing of GoPro BLE functionality"""

import time

import pytest

from open_gopro import GoPro, gopro
from open_gopro.api.v1_0 import params


class TestCommon:
    @pytest.mark.asyncio
    async def test_get_individual_statuses(self, gopro_ble_no_wifi: GoPro):
        for status in gopro_ble_no_wifi.ble_status:
            print(f"Getting {status} value...")
            assert status.get_value().is_ok

    @pytest.mark.asyncio
    async def test_get_all_statuses(self, gopro_ble_no_wifi: GoPro):
        assert gopro_ble_no_wifi.ble_command.get_camera_statuses()

    @pytest.mark.asyncio
    async def test_get_all_settings(self, gopro_ble_no_wifi: GoPro):
        assert gopro_ble_no_wifi.ble_command.get_camera_settings()

    @pytest.mark.asyncio
    async def test_get_individual_setting_values(self, gopro_ble_no_wifi: GoPro):
        for setting in gopro_ble_no_wifi.ble_setting:
            print(f"Getting {setting.identifier} value...")
            result = setting.get_value()
            assert result.is_ok

    @pytest.mark.asyncio
    async def test_register_setting_value_updates(self, gopro_ble_no_wifi: GoPro):
        for setting in gopro_ble_no_wifi.ble_setting:
            print(f"Registering for value updates for {setting.identifier}...")
            assert setting.register_value_update()
            print(f"Unregistering for value updates for {setting.identifier}...")
            assert setting.unregister_value_update()

    @pytest.mark.asyncio
    async def test_register_setting_capability_updates(self, gopro_ble_no_wifi: GoPro):
        for setting in gopro_ble_no_wifi.ble_setting:
            print(f"Registering for capability updates for {setting.identifier}...")
            assert setting.register_capability_update()
            print(f"Unregistering for capability updates for {setting.identifier}...")
            assert setting.unregister_capability_update()

    @pytest.mark.asyncio
    async def test_get_setting_capabilities(self, gopro_ble_no_wifi: GoPro):
        for setting in gopro_ble_no_wifi.ble_setting:
            print(f"Getting {setting.identifier} capabilities...")
            assert setting.get_capabilities_values().is_ok

    @pytest.mark.asyncio
    async def test_get_wifi_ssid(self, gopro_ble_no_wifi: GoPro):
        result = gopro_ble_no_wifi.ble_command.get_wifi_ssid()
        assert result.is_ok
        assert len(result.flatten)

    @pytest.mark.asyncio
    async def test_get_wifi_password(self, gopro_ble_no_wifi: GoPro):
        result = gopro_ble_no_wifi.ble_command.get_wifi_password()
        assert result.is_ok
        assert len(result.flatten)

    @pytest.mark.asyncio
    async def test_toggle_wifi_ap(self, gopro_ble_no_wifi: GoPro):
        print("Setting WiFI AP on...")
        assert gopro_ble_no_wifi.ble_command.enable_wifi_ap(True).is_ok
        print("Setting Wifi AP off...")
        assert gopro_ble_no_wifi.ble_command.enable_wifi_ap(True).is_ok

    @pytest.mark.asyncio
    async def test_shutter(self, gopro_ble_no_wifi: GoPro):
        print("Setting shutter on...")
        assert gopro_ble_no_wifi.ble_command.set_shutter(gopro_ble_no_wifi.params.Shutter.ON).is_ok
        time.sleep(1)
        print("Setting shutter off...")
        assert gopro_ble_no_wifi.ble_command.set_shutter(gopro_ble_no_wifi.params.Shutter.OFF).is_ok

    @pytest.mark.asyncio
    @pytest.xfail  # TODO Hero9 is failing when disabling turbo mode. figure this out when verifying protobuf commands
    async def test_turbo_mode(self, gopro_ble_no_wifi: GoPro):
        if gopro_ble_no_wifi.version == "1.0":
            pytest.skip("HERO9 not accepting Turbo Mode Off")
        response = gopro_ble_no_wifi.ble_command.set_turbo_mode(True)
        assert response.is_ok
        response = gopro_ble_no_wifi.ble_command.set_turbo_mode(False)
        assert response.is_ok

    @pytest.mark.asyncio
    async def test_narrow_param_value(self, gopro_ble_no_wifi: GoPro):
        version = gopro_ble_no_wifi.version
        if version == 1.0:
            assert gopro_ble_no_wifi.params.VideoFOV.NARROW.value == 6
        elif version == 2.0:
            assert gopro_ble_no_wifi.params.VideoFOV.NARROW.value == 2
        else:
            pytest.fail(f"Need to implement test for version {version}")


@pytest.mark.parametrize("gopro_ble_no_wifi", ["HERO9"], indirect=True)
class TestHero9Specific:
    @pytest.mark.asyncio
    async def test_cycle_resolutions(self, gopro_ble_no_wifi: GoPro):
        assert gopro_ble_no_wifi.ble_command.load_preset(gopro_ble_no_wifi.params.Preset.CINEMATIC).is_ok
        time.sleep(2)
        response = gopro_ble_no_wifi.ble_setting.resolution.get_capabilities_values()
        assert response.is_ok
        for resolution in response.flatten:
            print(f"Setting resolution to {str(resolution)}")
            assert gopro_ble_no_wifi.ble_setting.resolution.set(resolution).is_ok

    @pytest.mark.asyncio
    async def test_cycle_presets(self, gopro_ble_no_wifi: GoPro):
        for preset in gopro_ble_no_wifi.params.Preset:
            print(f"Setting {preset=}")
            assert gopro_ble_no_wifi.ble_command.load_preset(preset).is_ok


@pytest.mark.parametrize("gopro_ble_no_wifi", ["HERO10"], indirect=True)
class TestHero10Specific:
    @pytest.mark.asyncio
    async def test_cycle_resolutions(self, gopro_ble_no_wifi: GoPro):
        assert gopro_ble_no_wifi.ble_setting.max_lens_mode.set(
            gopro_ble_no_wifi.params.MaxLensMode.DEFAULT
        ).is_ok
        assert gopro_ble_no_wifi.ble_setting.video_performance_mode.set(
            gopro_ble_no_wifi.params.VideoPerformanceMode.MAX_PERFORMANCE
        )
        assert gopro_ble_no_wifi.ble_command.load_preset(gopro_ble_no_wifi.params.Preset.CINEMATIC).is_ok
        time.sleep(2)
        response = gopro_ble_no_wifi.ble_setting.resolution.get_capabilities_values()
        assert response.is_ok
        for resolution in response.flatten:
            print(f"Setting resolution to {str(resolution)}")
            assert gopro_ble_no_wifi.ble_setting.resolution.set(resolution).is_ok

    @pytest.mark.asyncio
    async def test_cycle_presets(self, gopro_ble_no_wifi: GoPro):
        # First test for Max Lens-compatible presets only
        print("Testing Max-Lens-compatible presets...")
        assert gopro_ble_no_wifi.ble_setting.max_lens_mode.set(
            gopro_ble_no_wifi.params.MaxLensMode.MAX_LENS
        ).is_ok
        for preset in [x for x in gopro_ble_no_wifi.params.Preset if "max" in x.name.lower()]:
            print(f"Setting {preset=}")
            assert gopro_ble_no_wifi.ble_command.load_preset(preset).is_ok

        # Now test non-Max Lens-compatible presets that are not extended battery
        print("Testing Max Performance Mode presets...")
        assert gopro_ble_no_wifi.ble_setting.max_lens_mode.set(
            gopro_ble_no_wifi.params.MaxLensMode.DEFAULT
        ).is_ok
        assert gopro_ble_no_wifi.ble_setting.video_performance_mode.set(
            gopro_ble_no_wifi.params.VideoPerformanceMode.MAX_PERFORMANCE
        ).is_ok
        for preset in [
            x
            for x in gopro_ble_no_wifi.params.Preset
            if "max" not in x.name.lower()
            and not x.name.lower().endswith("_eb")
            and "tripod" not in x.name.lower()
        ]:
            print(f"Setting {preset=}")
            assert gopro_ble_no_wifi.ble_command.load_preset(preset).is_ok

        # Now test extended battery presets
        print("Testing Extended Battery Presets")
        assert gopro_ble_no_wifi.ble_setting.video_performance_mode.set(
            gopro_ble_no_wifi.params.VideoPerformanceMode.EXTENDED_BATTERY
        ).is_ok
        for preset in [
            x
            for x in gopro_ble_no_wifi.params.Preset
            if "max" not in x.name.lower() and x.name.endswith("_EB")
        ]:
            print(f"Setting {preset=}")
            assert gopro_ble_no_wifi.ble_command.load_preset(preset).is_ok

        # Now test tripod presets
        print("Testing Tripod Presets")
        assert gopro_ble_no_wifi.ble_setting.video_performance_mode.set(
            gopro_ble_no_wifi.params.VideoPerformanceMode.STATIONARY
        ).is_ok
        for preset in [
            x
            for x in gopro_ble_no_wifi.params.Preset
            if "max" not in x.name.lower() and "tripod" in x.name.lower()
        ]:
            print(f"Setting {preset=}")
            assert gopro_ble_no_wifi.ble_command.load_preset(preset).is_ok
