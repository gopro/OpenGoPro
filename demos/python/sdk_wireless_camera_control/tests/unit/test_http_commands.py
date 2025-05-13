# test_wifi_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:55 PM

import inspect
import logging
from pathlib import Path

import pytest

from open_gopro.gopro_base import GoProBase
from open_gopro.models import constants, proto, streaming
from open_gopro.models.constants.settings import FramesPerSecond

camera_file = "100GOPRO/XXX.mp4"


@pytest.mark.asyncio
async def test_put_with_body_args(mock_wifi_communicator: GoProBase):
    response = await mock_wifi_communicator.http_command.update_custom_preset(
        custom_name="Custom Name",
        icon_id=proto.EnumPresetIcon.PRESET_ICON_ACTION,
        title_id=proto.EnumPresetTitle.PRESET_TITLE_ACTION,
    )
    assert response.url == "gopro/camera/presets/update_custom"
    assert response.body == {
        "custom_name": "Custom Name",
        "icon_id": proto.EnumPresetIcon.PRESET_ICON_ACTION,
        "title_id": proto.EnumPresetTitle.PRESET_TITLE_ACTION,
    }


@pytest.mark.asyncio
async def test_get_with_no_params(mock_wifi_communicator: GoProBase):
    response = await mock_wifi_communicator.http_command.get_media_list()
    assert response.url == "gopro/media/list"


@pytest.mark.asyncio
async def test_set_setting(mock_wifi_communicator: GoProBase):
    response = await mock_wifi_communicator.http_setting.frames_per_second.set(FramesPerSecond.NUM_100_0)
    assert response.url == "gopro/camera/setting?setting=3&option=2"


@pytest.mark.asyncio
async def test_get_with_params(mock_wifi_communicator: GoProBase):
    zoom = 99
    response = await mock_wifi_communicator.http_command.set_digital_zoom(percent=zoom)
    assert response.url == f"gopro/camera/digital_zoom?percent={zoom}"


@pytest.mark.asyncio
async def test_get_binary(mock_wifi_communicator: GoProBase):
    response, file = await mock_wifi_communicator.http_command.get_gpmf_data(camera_file=camera_file)
    assert response.url == f"gopro/media/gpmf?path={camera_file}"
    assert file == Path("XXX.mp4")


@pytest.mark.asyncio
async def test_get_binary_with_component(mock_wifi_communicator: GoProBase):
    response, file = await mock_wifi_communicator.http_command.download_file(
        camera_file=camera_file, local_file=Path("cheese.mp4")
    )
    assert response.url == f"videos/DCIM/{camera_file}"
    assert file == Path("cheese.mp4")


@pytest.mark.asyncio
async def test_with_multiple_params(mock_wifi_communicator: GoProBase):
    offset_ms = 2500
    response = await mock_wifi_communicator.http_command.add_file_hilight(file=camera_file, offset=offset_ms)
    assert response.url == f"gopro/media/hilight/file?path={camera_file}&ms=2500"


@pytest.mark.asyncio
async def test_string_arg(mock_wifi_communicator: GoProBase):
    response = await mock_wifi_communicator.http_command.webcam_start(protocol=streaming.WebcamProtocol.RTSP)
    assert response.url == f"gopro/webcam/start?protocol=RTSP"


def test_ensure_no_positional_args(mock_wifi_communicator: GoProBase):
    for command in mock_wifi_communicator.http_command.values():
        if inspect.getfullargspec(command).args != ["self"]:
            logging.error("All arguments to commands must be keyword-only")
            assert True
