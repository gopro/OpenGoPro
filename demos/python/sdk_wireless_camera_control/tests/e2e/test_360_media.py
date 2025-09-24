# test_360_media.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Sep 24 20:06:47 UTC 2025

"""These tests are designed to run on a GoPro MAX 2 to exercise media querying."""

from asyncio import sleep
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest

from open_gopro import WiredGoPro, WirelessGoPro
from open_gopro.gopro_base import GoProBase
from open_gopro.models.constants import Toggle
from open_gopro.models.constants.settings import CameraMode, NUM360PhotoFilesExtension


@pytest.fixture(scope="function")
async def gut(wired_gopro: WiredGoPro) -> AsyncGenerator[WiredGoPro, None]:
    assert (await wired_gopro.http_command.delete_all_media()).ok
    yield wired_gopro


@pytest.fixture(scope="function")
async def wireless_gut(wireless_gopro: WirelessGoPro) -> AsyncGenerator[WirelessGoPro, None]:
    assert (await wireless_gopro.http_command.delete_all_media()).ok
    yield wireless_gopro


async def get_flat_presets(gut: GoProBase[Any]) -> list[dict[str, Any]]:
    preset_response = await gut.http_command.get_preset_status()
    assert preset_response.ok
    groups = preset_response.data["presetGroupArray"]
    flat_presets = []
    for group in groups:
        flat_presets.extend(group["presetArray"])
    return flat_presets


async def load_single_lens_video_mode(gut: GoProBase[Any]) -> None:
    assert (await gut.http_setting.camera_mode.set(CameraMode.SINGLE_LENS)).ok
    # Load a video preset
    video_preset = next(preset for preset in await get_flat_presets(gut) if preset["titleId"] == "PRESET_TITLE_VIDEO")
    assert (await gut.http_command.load_preset(preset=video_preset["id"])).ok


async def load_360_video_mode(gut: GoProBase[Any]) -> None:
    assert (await gut.http_setting.camera_mode.set(CameraMode.NUM_360_)).ok
    # Load a video preset
    video_preset = next(preset for preset in await get_flat_presets(gut) if preset["titleId"] == "PRESET_TITLE_VIDEO")
    assert (await gut.http_command.load_preset(preset=video_preset["id"])).ok


async def take_video(gut: GoProBase[Any], duration: int) -> None:
    assert (await gut.http_command.set_shutter(shutter=Toggle.ENABLE)).ok
    await sleep(duration)
    assert (await gut.http_command.set_shutter(shutter=Toggle.DISABLE)).ok


async def take_photo(gut: GoProBase[Any]) -> None:
    assert (await gut.http_command.set_shutter(shutter=Toggle.ENABLE)).ok


async def load_single_lens_photo_mode(gut: GoProBase[Any]) -> None:
    assert (await gut.http_setting.camera_mode.set(CameraMode.SINGLE_LENS)).ok
    # Load a video preset
    video_preset = next(preset for preset in await get_flat_presets(gut) if preset["titleId"] == "PRESET_TITLE_PHOTO")
    assert (await gut.http_command.load_preset(preset=video_preset["id"])).ok


async def load_360_photo_mode(gut: GoProBase[Any]) -> None:
    assert (await gut.http_setting.camera_mode.set(CameraMode.NUM_360_)).ok
    # Load a video preset
    video_preset = next(preset for preset in await get_flat_presets(gut) if preset["titleId"] == "PRESET_TITLE_PHOTO")
    assert (await gut.http_command.load_preset(preset=video_preset["id"])).ok


@pytest.mark.timeout(30)
async def test_360_photo_extensions_usb(gut: WiredGoPro):
    """Test capturing 360 photos with different file extensions."""
    await load_360_photo_mode(gut)
    # Set the extension to 36P and take a photo
    assert (await gut.http_setting.num_360_photo_files_extension.set(NUM360PhotoFilesExtension.NUM_36P)).ok
    await take_photo(gut)

    # Set the extension to JPG and take a photo
    assert (await gut.http_setting.num_360_photo_files_extension.set(NUM360PhotoFilesExtension.NUM_JPG)).ok
    await take_photo(gut)

    # Get the media list
    media_list_response = await gut.http_command.get_media_list()
    assert media_list_response.ok, "Failed to retrieve media list"
    media_list = media_list_response.data.files

    # THEN
    assert len(media_list) == 2, "There should be exactly two media files"
    assert Path(media_list[0].filename).suffix == ".36P", "The first media file should be an 36P"
    assert Path(media_list[1].filename).suffix == ".JPG", "The second media file should be a JPG"


@pytest.mark.timeout(60)
async def test_video_capturing_usb(gut: WiredGoPro, tmp_path: Path):
    # Take a 360 video
    await load_360_video_mode(gut)
    await take_video(gut, duration=1)

    # Take a single lens video
    await load_single_lens_video_mode(gut)
    await take_video(gut, duration=1)

    # Get the media list
    media_list_response = await gut.http_command.get_media_list()
    assert media_list_response.ok, "Failed to retrieve media list"
    media_list = media_list_response.data.files

    # THEN
    assert len(media_list) == 2, "There should be exactly two media files"
    assert Path(media_list[0].filename).suffix == ".360", "The first media file should be a 360"
    assert Path(media_list[1].filename).suffix == ".MP4", "The second media file should be a MP4"

    # Ensure we can download the images
    for media in media_list:
        download_response = await gut.http_command.download_file(
            camera_file=media.filename,
            local_file=tmp_path / Path(media.filename).name,
        )
        assert download_response.ok, f"Failed to download media {media.filename}"


@pytest.mark.timeout(60)
async def test_video_capturing_wifi(wireless_gut: WirelessGoPro, tmp_path: Path):
    # Take a 360 video
    await load_360_video_mode(wireless_gut)
    await take_video(wireless_gut, duration=1)

    # Take a single lens video
    await load_single_lens_video_mode(wireless_gut)
    await take_video(wireless_gut, duration=1)

    # Get the media list
    media_list_response = await wireless_gut.http_command.get_media_list()
    assert media_list_response.ok, "Failed to retrieve media list"
    media_list = media_list_response.data.files

    # THEN
    assert len(media_list) == 2, "There should be exactly two media files"
    assert Path(media_list[0].filename).suffix == ".360", "The first media file should be a 360"
    assert Path(media_list[1].filename).suffix == ".MP4", "The second media file should be a MP4"

    # Ensure we can download the images
    for media in media_list:
        download_response = await wireless_gut.http_command.download_file(
            camera_file=media.filename,
            local_file=tmp_path / Path(media.filename).name,
        )
        assert download_response.ok, f"Failed to download media {media.filename}"


@pytest.mark.timeout(60)
async def test_photo_capturing_usb(gut: WiredGoPro, tmp_path: Path):
    # Take a 360 photo
    await load_360_photo_mode(gut)
    await take_photo(gut)

    # Take a single lens photo
    await load_single_lens_photo_mode(gut)
    await take_photo(gut)

    # Get the media list
    media_list_response = await gut.http_command.get_media_list()
    assert media_list_response.ok, "Failed to retrieve media list"
    media_list = media_list_response.data.files

    # THEN
    assert len(media_list) == 2, "There should be exactly two media files"

    # Ensure we can download the images
    for media in media_list:
        download_response = await gut.http_command.download_file(
            camera_file=media.filename,
            local_file=tmp_path / Path(media.filename).name,
        )
        assert download_response.ok, f"Failed to download media {media.filename}"
