# test_tutorials.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jan  5 23:22:13 UTC 2022

import time
import asyncio
import threading

import pytest
from open_gopro.wifi.adapters.wireless import Wireless
from open_gopro.wifi.controller import SsidState

from tutorial_modules.tutorial_1_connect_ble.ble_connect import main as ble_connect
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_enable_analytics import main as ble_command_enable_analytics
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_load_group import main as ble_command_load_group
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_load_preset import main as ble_command_load_preset
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_fps import main as ble_command_set_fps
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_resolution import main as ble_command_set_resolution
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_shutter import main as ble_command_set_shutter
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_sleep import main as ble_command_sleep
from tutorial_modules.tutorial_3_parse_ble_tlv_responses.ble_command_get_state import main as ble_command_get_state
from tutorial_modules.tutorial_3_parse_ble_tlv_responses.ble_command_get_version import main as ble_command_get_version
from tutorial_modules.tutorial_4_ble_queries.ble_query_poll_multiple_setting_values import main as ble_query_poll_multiple_setting_values
from tutorial_modules.tutorial_4_ble_queries.ble_query_poll_resolution_value import main as ble_query_poll_resolution_value
from tutorial_modules.tutorial_4_ble_queries.ble_query_register_resolution_value_updates import main as ble_query_register_resolution_value_updates
from tutorial_modules.tutorial_5_connect_wifi.wifi_enable import main as wifi_enable
from tutorial_modules.tutorial_5_connect_wifi.wifi_enable_and_connect import main as wifi_enable_and_connect
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_media_list import main as wifi_command_get_media_list
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_preset_status import main as wifi_command_get_preset_status
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_state import main as wifi_command_get_state
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_version import main as wifi_command_get_version
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_keep_alive import main as wifi_command_keep_alive
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_load_group import main as wifi_command_load_group
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_load_preset import main as wifi_command_load_preset
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_preview_stream import main as wifi_command_preview_stream
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_set_resolution import main as wifi_command_set_resolution
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_set_shutter import main as wifi_command_set_shutter
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_zoom import main as wifi_command_zoom
from tutorial_modules.tutorial_7_camera_media_list.wifi_media_download_file import main as wifi_media_download_file
from tutorial_modules.tutorial_7_camera_media_list.wifi_media_get_gpmf import main as wifi_media_get_gpmf
from tutorial_modules.tutorial_7_camera_media_list.wifi_media_get_screennail import main as wifi_media_get_screennail
from tutorial_modules.tutorial_7_camera_media_list.wifi_media_get_thumbnail import main as wifi_media_get_thumbnail

@pytest.fixture(scope="module")
def connect_wifi():
    def maintain_wifi():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(wifi_enable_and_connect(None, None))

    threading.Thread(target=maintain_wifi, daemon=True).start()
    wifi = Wireless()
    while wifi.current()[1] is not SsidState.CONNECTED:
        time.sleep(2)
        print("Waiting for WiFi to connect...")
    yield

    wifi.disconnect()


class TestTutorial1ConnectBle:
    @pytest.mark.asyncio
    async def test_ble_connect(self):
        await ble_connect(None)


class TestTutorial2SendBleCommands:
    @pytest.mark.asyncio
    async def test_ble_command_enable_analytics(self):
        await ble_command_enable_analytics(None)

    @pytest.mark.asyncio
    async def test_ble_command_load_group(self):
        await ble_command_load_group(None)

    @pytest.mark.asyncio
    async def test_ble_command_load_preset(self):
        await ble_command_load_preset(None)

    @pytest.mark.asyncio
    async def test_ble_command_set_fps(self):
        await ble_command_set_fps(None)

    @pytest.mark.asyncio
    async def test_ble_command_set_resolution(self):
        await ble_command_set_resolution(None)

    @pytest.mark.asyncio
    async def test_ble_command_set_shutter(self):
        await ble_command_set_shutter(None)

    @pytest.mark.asyncio
    async def test_ble_command_sleep(self):
        await ble_command_sleep(None)


class TestTutorial3ParseBleTlvResponses:
    @pytest.mark.asyncio
    async def test_ble_command_get_state(self):
        await ble_command_get_state(None)

    @pytest.mark.asyncio
    async def test_ble_command_get_version(self):
        await ble_command_get_version(None)


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


class TestTutorial6SendWifiCommands:
    def test_wifi_command_get_media_list(self, connect_wifi):
        wifi_command_get_media_list()

    def test_wifi_command_get_preset_status(self, connect_wifi):
        wifi_command_get_preset_status()

    def test_wifi_command_get_state(self, connect_wifi):
        wifi_command_get_state()

    def test_wifi_command_get_version(self, connect_wifi):
        wifi_command_get_version()

    def test_wifi_command_keep_alive(self, connect_wifi):
        wifi_command_keep_alive()

    def test_wifi_command_load_group(self, connect_wifi):
        wifi_command_load_group()

    def test_wifi_command_load_preset(self, connect_wifi):
        wifi_command_load_preset()

    def test_wifi_command_preview_stream(self, connect_wifi):
        wifi_command_preview_stream()

    def test_wifi_command_set_resolution(self, connect_wifi):
        wifi_command_set_resolution()

    def test_wifi_command_zoom(self, connect_wifi):
        wifi_command_zoom(50)

    def test_wifi_command_set_shutter(self, connect_wifi):
        wifi_command_set_shutter()
        time.sleep(2) # wait for camera to be ready


class TestTutorial7CameraMediaList:
    def test_wifi_media_download_file(self, connect_wifi):
        wifi_media_download_file()

    def test_wifi_media_get_gpmf(self, connect_wifi):
        wifi_media_get_gpmf()

    def test_wifi_media_get_screennail(self, connect_wifi):
        wifi_media_get_screennail()

    def test_wifi_media_get_thumbnail(self, connect_wifi):
        wifi_media_get_thumbnail()