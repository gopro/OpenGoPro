# test_operations.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Sep 24 20:06:47 UTC 2025

from typing import Any

import pytest

from open_gopro import WiredGoPro, WirelessGoPro
from open_gopro.models.proto import EnumPresetGroup, EnumPresetTitle, Preset


# This was tested on Max 2
@pytest.mark.timeout(180)
async def test_can_set_camera_name_on(wireless_gopro: WirelessGoPro):
    old_name = (await wireless_gopro.http_command.get_camera_name()).data
    new_name = "Test Camera"

    if old_name == new_name:
        new_name += " newer"

    # Set via HTTP to new name and verify
    assert (await wireless_gopro.http_command.set_camera_name(name=new_name)).ok
    current_name = (await wireless_gopro.http_command.get_camera_name()).data
    assert current_name == new_name

    # Now set back to old name via BLE and verify (via HTTP)
    assert (await wireless_gopro.ble_command.set_camera_name(name=old_name)).ok
    current_name = (await wireless_gopro.http_command.get_camera_name()).data
    assert current_name == old_name


# This was tested on Max 2. Before running, use the camera UI to ensure all video group presets are visible.
@pytest.mark.timeout(30)
async def test_can_set_preset_visibility_wired_http(wired_gopro: WiredGoPro):
    async def get_string_set_of_video_presets(include_hidden: bool) -> list[dict[str, Any]]:
        # Load video preset group
        assert (await wired_gopro.http_command.load_preset_group(group=EnumPresetGroup.PRESET_GROUP_ID_VIDEO)).ok

        # Get list of video presets
        preset_status = await wired_gopro.http_command.get_preset_status(include_hidden=include_hidden)
        assert preset_status.ok
        return next(
            (group for group in preset_status.data["presetGroupArray"] if group["id"] == "PRESET_GROUP_ID_VIDEO")
        )["presetArray"]

    # Control case: All presets should be visible
    initial_video_presets = await get_string_set_of_video_presets(include_hidden=False)
    assert {preset["titleId"] for preset in initial_video_presets} == {
        "PRESET_TITLE_VIDEO",
        "PRESET_TITLE_LOOPING",
    }, "All video presets should be visible before running this test. Use the camera UI to enable them."

    # Hide the looping preset
    looping_preset_id = next(
        preset["id"] for preset in initial_video_presets if preset["titleId"] == "PRESET_TITLE_LOOPING"
    )
    assert (await wired_gopro.http_command.set_preset_visibility(preset_id=looping_preset_id, is_visible=False)).ok

    # Ensure looping is now hidden
    new_video_presets = await get_string_set_of_video_presets(include_hidden=False)
    assert {preset["titleId"] for preset in new_video_presets} == {"PRESET_TITLE_VIDEO"}

    # Ensure we can get all presets if we don't filter out hidden ones
    all_video_presets = await get_string_set_of_video_presets(include_hidden=True)
    assert {preset["titleId"] for preset in all_video_presets} == {
        "PRESET_TITLE_VIDEO",
        "PRESET_TITLE_LOOPING",
    }


# This was tested on Max 2. Before running, use the camera UI to ensure all video group presets are visible.
@pytest.mark.timeout(30)
async def test_can_set_preset_visibility_ble(wireless_gopro_ble: WirelessGoPro):
    async def get_string_set_of_video_presets(include_hidden: bool) -> list[Preset]:
        # Load video preset group
        assert (await wireless_gopro_ble.ble_command.load_preset_group(group=EnumPresetGroup.PRESET_GROUP_ID_VIDEO)).ok

        # Get list of video presets
        preset_status = await wireless_gopro_ble.ble_command.get_preset_status(include_hidden=include_hidden)
        assert preset_status.ok
        return list(
            next(
                (
                    group
                    for group in preset_status.data.preset_group_array
                    if group.id == EnumPresetGroup.PRESET_GROUP_ID_VIDEO
                )
            ).preset_array
        )

    # Control case: All presets should be visible
    initial_video_presets = await get_string_set_of_video_presets(include_hidden=False)
    assert {int(preset.title_id) for preset in initial_video_presets} == {
        int(EnumPresetTitle.PRESET_TITLE_VIDEO),
        int(EnumPresetTitle.PRESET_TITLE_LOOPING),
    }, "All video presets should be visible before running this test. Use the camera UI to enable them."

    # Hide the looping preset
    looping_preset_id = next(
        preset.id for preset in initial_video_presets if preset.title_id == EnumPresetTitle.PRESET_TITLE_LOOPING
    )
    assert (
        await wireless_gopro_ble.ble_command.set_preset_visibility(preset_id=looping_preset_id, is_visible=False)
    ).ok

    # Ensure looping is now hidden
    new_video_presets = await get_string_set_of_video_presets(include_hidden=False)
    assert {int(preset.title_id) for preset in new_video_presets} == {
        int(EnumPresetTitle.PRESET_TITLE_VIDEO),
    }

    # Ensure we can get all presets if we don't filter out hidden ones
    all_video_presets = await get_string_set_of_video_presets(include_hidden=True)
    assert {int(preset.title_id) for preset in all_video_presets} == {
        int(EnumPresetTitle.PRESET_TITLE_VIDEO),
        int(EnumPresetTitle.PRESET_TITLE_LOOPING),
    }
