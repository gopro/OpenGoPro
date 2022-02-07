# test_gopro_wifi_commands_e2e.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""End to end testing of GoPro BLE functionality"""

import enum
from pathlib import Path
from typing import List

import pytest

from tests import versions
from open_gopro import GoPro, Params


async def test_get_media_list(gopro_ble_and_wifi: GoPro):
    assert gopro_ble_and_wifi.wifi_command.get_media_list().is_ok


async def test_get_state(gopro_ble_and_wifi: GoPro):
    assert gopro_ble_and_wifi.wifi_command.get_camera_state().is_ok


async def test_get_version(gopro_ble_and_wifi: GoPro):
    result = gopro_ble_and_wifi.wifi_command.get_open_gopro_api_version()
    assert result.is_ok
    assert result.flatten in versions


async def test_set_turbo_mode(gopro_ble_and_wifi: GoPro):
    print("Setting turbo mode on")
    assert gopro_ble_and_wifi.wifi_command.set_turbo_mode(Params.Toggle.ENABLE).is_ok
    print("Setting turbo mode off")
    assert gopro_ble_and_wifi.wifi_command.set_turbo_mode(Params.Toggle.DISABLE).is_ok


async def test_set_resolution(gopro_ble_and_wifi: GoPro):
    if gopro_ble_and_wifi.version >= 2.0:
        assert gopro_ble_and_wifi.ble_setting.video_performance_mode.set(
            Params.PerformanceMode.MAX_PERFORMANCE
        ).is_ok
        assert gopro_ble_and_wifi.ble_setting.max_lens_mode.set(Params.MaxLensMode.DEFAULT).is_ok
    assert gopro_ble_and_wifi.wifi_command.set_preset(Params.Preset.CINEMATIC).is_ok
    for resolution in Params.Resolution:
        print(f"Setting resolution to {resolution.name}")
        assert gopro_ble_and_wifi.wifi_setting.resolution.set(resolution).is_ok


@pytest.fixture(scope="class")
async def media_list(gopro_ble_and_wifi: GoPro):
    media_list = gopro_ble_and_wifi.wifi_command.get_media_list().flatten
    yield media_list


class TestMediaList:
    class MediaType(enum.Enum):
        PHOTO = enum.auto()
        VIDEO = enum.auto()

    @staticmethod
    def find_media(media_type: MediaType, media_list: List) -> str:
        for file in [x["n"] for x in media_list]:
            if media_type is TestMediaList.MediaType.PHOTO and file.lower().endswith(".jpg"):
                return file
            if media_type is TestMediaList.MediaType.VIDEO and file.lower().endswith(".mp4"):
                return file
        else:
            raise ValueError(f"No {type} found")

    @staticmethod
    def find_picture(media_list: List) -> str:
        return TestMediaList.find_media(TestMediaList.MediaType.PHOTO, media_list)

    @staticmethod
    def find_video(media_list: List) -> str:
        return TestMediaList.find_media(TestMediaList.MediaType.VIDEO, media_list)

    async def test_download_photo(self, gopro_ble_and_wifi: GoPro, media_list):
        picture = self.find_picture(media_list)
        write_location = Path("out.jpg")
        gopro_ble_and_wifi.wifi_command.download_file(camera_file=picture, local_file=write_location)
        assert write_location.exists()

    async def test_video_hilights(self, gopro_ble_and_wifi: GoPro, media_list):
        video = self.find_video(media_list)
        assert gopro_ble_and_wifi.wifi_command.add_video_hilight((video, 1)).is_ok
        assert gopro_ble_and_wifi.wifi_command.remove_video_hilight((video, 1)).is_ok
