# test_delete_media.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Apr 16 20:07:53 UTC 2024

import asyncio
from typing import AsyncGenerator

import pytest

from open_gopro.gopro_wired import WiredGoPro
from open_gopro.models import MediaPath, constants, proto


@pytest.fixture(scope="function")
async def gopro() -> AsyncGenerator[WiredGoPro, None]:
    async with WiredGoPro() as gopro:
        assert (await gopro.http_setting.control_mode.set(constants.settings.ControlMode.PRO)).ok
        assert (await gopro.http_command.delete_all()).ok
        yield gopro


async def create_single_photo(gopro: WiredGoPro) -> MediaPath:
    # Set a "single" photo preset
    presets = (await gopro.http_command.get_preset_status()).data
    photo_presets = next(group for group in presets["presetGroupArray"] if "photo" in group["id"].lower())
    single_preset_id = next(preset for preset in photo_presets["presetArray"] if "single" in preset["mode"].lower())[
        "id"
    ]
    assert (await gopro.http_command.load_preset(preset=single_preset_id)).ok

    assert (await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)).ok
    photo = (await gopro.http_command.get_last_captured_media()).data
    # Sanity check photo is in media list
    assert photo in (await gopro.http_command.get_media_list()).data
    return photo


async def create_burst_photo(gopro: WiredGoPro) -> MediaPath:
    # Set a "burst" photo preset
    presets = (await gopro.http_command.get_preset_status()).data
    photo_presets = next(group for group in presets["presetGroupArray"] if "photo" in group["id"].lower())
    burst_preset_id = next(preset for preset in photo_presets["presetArray"] if "burst" in preset["mode"].lower())["id"]
    assert (await gopro.http_command.load_preset(preset=burst_preset_id)).ok

    assert (await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)).ok
    grouped_photo = (await gopro.http_command.get_last_captured_media()).data
    # Sanity check photo is in media list
    assert grouped_photo in (await gopro.http_command.get_media_list()).data
    return grouped_photo


async def create_timelapse_photo(gopro: WiredGoPro) -> MediaPath:
    # Set a "timelapse" photo preset
    presets = (await gopro.http_command.get_preset_status()).data
    timelapse_presets = next(group for group in presets["presetGroupArray"] if "timelapse" in group["id"].lower())
    # Get to timelapse preset group
    assert (await gopro.http_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_TIMELAPSE)).ok
    # Get to a timelapse preset
    timelapse_preset = next(
        preset for preset in timelapse_presets["presetArray"] if "time_lapse" in preset["mode"].lower()
    )
    assert (await gopro.http_command.load_preset(preset=timelapse_preset["id"])).ok
    # Set the format to photo to get a "time lapse photo"
    assert (await gopro.http_setting.media_format.set(constants.settings.MediaFormat.TIME_LAPSE_PHOTO)).ok

    # Take a timelapse
    assert (await gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)).ok
    await asyncio.sleep(3)
    assert (await gopro.http_command.set_shutter(shutter=constants.Toggle.DISABLE)).ok

    grouped_photo = (await gopro.http_command.get_last_captured_media()).data
    # Sanity check photo is in media list
    assert grouped_photo in (await gopro.http_command.get_media_list()).data
    return grouped_photo


@pytest.mark.timeout(60)
class TestMediaDeletion:
    @pytest.mark.asyncio
    async def test_delete_file_deletes_single_file(self, gopro: WiredGoPro):
        # GIVEN
        photo = await create_single_photo(gopro)

        # WHEN
        assert (await gopro.http_command.delete_file(path=photo.as_path)).ok

        # THEN
        media_list = (await gopro.http_command.get_media_list()).data.files
        assert not media_list  # Media list should be empty

    @pytest.mark.asyncio
    async def test_delete_file_partially_deletes_burst_group(self, gopro: WiredGoPro):
        # GIVEN
        burst_group = await create_burst_photo(gopro)

        # WHEN
        assert (await gopro.http_command.delete_file(path=burst_group.as_path)).ok

        # THEN
        media_list = (await gopro.http_command.get_media_list()).data.files
        assert media_list
        assert burst_group not in media_list

    @pytest.mark.asyncio
    async def test_delete_file_partially_deletes_timelapse_group(self, gopro: WiredGoPro):
        # GIVEN
        timelapse_group = await create_timelapse_photo(gopro)

        # WHEN
        assert (await gopro.http_command.delete_file(path=timelapse_group.as_path)).ok

        # THEN
        media_list = (await gopro.http_command.get_media_list()).data.files
        assert media_list
        assert timelapse_group not in media_list

    @pytest.mark.asyncio
    async def test_delete_group_deletes_burst_group(self, gopro: WiredGoPro):
        # GIVEN
        burst_group = await create_burst_photo(gopro)

        # WHEN
        assert (await gopro.http_command.delete_group(path=burst_group.as_path)).ok

        # THEN
        media_list = (await gopro.http_command.get_media_list()).data.files
        assert not media_list

    @pytest.mark.asyncio
    async def test_delete_group_deletes_timelapse_group(self, gopro: WiredGoPro):
        # GIVEN
        timelapse_group = await create_timelapse_photo(gopro)

        # WHEN
        assert (await gopro.http_command.delete_group(path=timelapse_group.as_path)).ok

        # THEN
        media_list = (await gopro.http_command.get_media_list()).data.files
        assert not media_list
