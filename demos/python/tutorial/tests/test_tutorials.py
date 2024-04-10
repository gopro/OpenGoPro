# test_tutorials.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jan  5 23:22:13 UTC 2022

# Simply run each demo for some naive sanity checking

import time
from pathlib import Path

import pytest

from tutorial_modules.tutorial_1_connect_ble.ble_connect import main as ble_connect
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_load_group import (
    main as ble_command_load_group,
)
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_fps import (
    main as ble_command_set_fps,
)
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_resolution import (
    main as ble_command_set_resolution,
)
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_shutter import (
    main as ble_command_set_shutter,
)
from tutorial_modules.tutorial_3_parse_ble_tlv_responses.ble_command_get_hardware_info import (
    main as ble_get_hardware_info,
)
from tutorial_modules.tutorial_3_parse_ble_tlv_responses.ble_command_get_version import (
    main as ble_command_get_version,
)
from tutorial_modules.tutorial_4_ble_queries.ble_query_poll_multiple_setting_values import (
    main as ble_query_poll_multiple_setting_values,
)
from tutorial_modules.tutorial_4_ble_queries.ble_query_poll_resolution_value import (
    main as ble_query_poll_resolution_value,
)
from tutorial_modules.tutorial_4_ble_queries.ble_query_register_resolution_value_updates import (
    main as ble_query_register_resolution_value_updates,
)
from tutorial_modules.tutorial_5_ble_protobuf.set_turbo_mode import (
    main as set_turbo_mode,
)
from tutorial_modules.tutorial_6_connect_wifi.connect_as_sta import main as connect_sta
from tutorial_modules.tutorial_6_connect_wifi.enable_wifi_ap import main as wifi_enable
from tutorial_modules.tutorial_7_send_wifi_commands.wifi_command_get_media_list import (
    main as wifi_command_get_media_list,
)
from tutorial_modules.tutorial_7_send_wifi_commands.wifi_command_get_state import (
    main as wifi_command_get_state,
)
from tutorial_modules.tutorial_7_send_wifi_commands.wifi_command_load_group import (
    main as wifi_command_load_group,
)
from tutorial_modules.tutorial_7_send_wifi_commands.wifi_command_preview_stream import (
    main as wifi_command_preview_stream,
)
from tutorial_modules.tutorial_7_send_wifi_commands.wifi_command_set_resolution import (
    main as wifi_command_set_resolution,
)
from tutorial_modules.tutorial_7_send_wifi_commands.wifi_command_set_shutter import (
    main as wifi_command_set_shutter,
)
from tutorial_modules.tutorial_8_camera_media_list.wifi_media_download_file import (
    main as wifi_media_download_file,
)
from tutorial_modules.tutorial_8_camera_media_list.wifi_media_get_gpmf import (
    main as wifi_media_get_gpmf,
)
from tutorial_modules.tutorial_8_camera_media_list.wifi_media_get_screennail import (
    main as wifi_media_get_screennail,
)
from tutorial_modules.tutorial_8_camera_media_list.wifi_media_get_thumbnail import (
    main as wifi_media_get_thumbnail,
)
from tutorial_modules.tutorial_9_cohn.communicate_via_cohn import (
    main as communicate_via_cohn,
)
from tutorial_modules.tutorial_9_cohn.provision_cohn import main as provision_cohn


@pytest.fixture(scope="module")
def connect_wifi():
    print("\n\nPress enter when WiFi is connected to GoPro camera...\n")
    input("")
    yield


class TestTutorial1ConnectBle:
    @pytest.mark.asyncio
    async def test_ble_connect(self):
        await ble_connect(None)


class TestTutorial2SendBleCommands:
    @pytest.mark.asyncio
    async def test_ble_command_load_group(self):
        await ble_command_load_group(None)

    @pytest.mark.asyncio
    async def test_ble_command_set_resolution(self):
        await ble_command_set_resolution(None)

    @pytest.mark.asyncio
    async def test_ble_command_set_fps(self):
        await ble_command_set_fps(None)

    @pytest.mark.asyncio
    async def test_ble_command_set_shutter(self):
        await ble_command_set_shutter(None)


class TestTutorial3ParseBleTlvResponses:
    @pytest.mark.asyncio
    async def test_ble_command_get_version(self):
        await ble_command_get_version(None)

    @pytest.mark.asyncio
    async def test_ble_get_hardware_info(self):
        await ble_get_hardware_info(None)


class TestTutorial4BleQueries:
    @pytest.mark.asyncio
    async def test_ble_query_poll_multiple_setting_values(self):
        await ble_query_poll_multiple_setting_values(None)

    @pytest.mark.asyncio
    async def test_ble_query_poll_resolution_value(self):
        await ble_query_poll_resolution_value(None)

    @pytest.mark.asyncio
    async def test_ble_query_register_resolution_value_updates(self):
        await ble_query_register_resolution_value_updates(None)


class TestTutorial5ConnectWifi:
    @pytest.mark.asyncio
    async def test_wifi_enable(self):
        await wifi_enable(None, timeout=1)


class TestTutorial6BleProtobuf:
    @pytest.mark.asyncio
    async def test_set_turbo_mode(self):
        await set_turbo_mode(None)


class TestTutorial9Cohn:
    @pytest.mark.asyncio
    async def test_connect_sta(self, pytestconfig):
        await connect_sta(pytestconfig.getoption("ssid"), pytestconfig.getoption("password"), None)

    @pytest.mark.asyncio
    async def test_cohn(self, pytestconfig):
        credentials = await provision_cohn(
            pytestconfig.getoption("ssid"), pytestconfig.getoption("password"), None, Path("cohn.crt")
        )
        assert credentials
        await communicate_via_cohn(credentials.ip_address, credentials.username, credentials.password, Path("cohn.crt"))


class TestTutorial7SendWifiCommands:
    def test_wifi_command_get_media_list(self, connect_wifi):
        wifi_command_get_media_list()

    def test_wifi_command_get_state(self, connect_wifi):
        wifi_command_get_state()

    def test_wifi_command_load_group(self, connect_wifi):
        wifi_command_load_group()

    def test_wifi_command_set_resolution(self, connect_wifi):
        wifi_command_set_resolution()

    def test_wifi_command_preview_stream(self, connect_wifi):
        wifi_command_preview_stream()

    def test_wifi_command_set_shutter(self, connect_wifi):
        wifi_command_set_shutter()
        time.sleep(2)  # wait for camera to be ready


class TestTutorial8CameraMediaList:
    def test_wifi_media_download_file(self, connect_wifi):
        wifi_media_download_file()

    def test_wifi_media_get_gpmf(self, connect_wifi):
        wifi_media_get_gpmf()

    def test_wifi_media_get_screennail(self, connect_wifi):
        wifi_media_get_screennail()

    def test_wifi_media_get_thumbnail(self, connect_wifi):
        wifi_media_get_thumbnail()
