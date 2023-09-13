# test_wifi_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:55 PM

import inspect
import logging
from pathlib import Path

import pytest

from open_gopro.communicator_interface import GoProWifi


@pytest.mark.asyncio
async def test_get_with_no_params(mock_wifi_communicator: GoProWifi):
    response = await mock_wifi_communicator.http_command.get_media_list()
    assert response.url == "gopro/media/list"


@pytest.mark.asyncio
async def test_get_with_params(mock_wifi_communicator: GoProWifi):
    zoom = 99
    response = await mock_wifi_communicator.http_command.set_digital_zoom(percent=zoom)
    assert response.url == f"gopro/camera/digital_zoom?percent={zoom}"


@pytest.mark.asyncio
async def test_with_multiple_params(mock_wifi_communicator: GoProWifi):
    media_file = "XXX.mp4"
    offset_ms = 2500
    response = await mock_wifi_communicator.http_command.add_file_hilight(file=media_file, offset=offset_ms)
    assert response.url == "gopro/media/hilight/file?path=100GOPRO/XXX.mp4&ms=2500"


@pytest.mark.asyncio
async def test_get_binary(mock_wifi_communicator: GoProWifi):
    file = await mock_wifi_communicator.http_command.download_file(
        camera_file="test_file", local_file=Path("local_file")
    )
    assert str(file[1]) == "local_file"


def test_ensure_no_positional_args(mock_wifi_communicator: GoProWifi):
    for command in mock_wifi_communicator.http_command.values():
        if inspect.getfullargspec(command).args != ["self"]:
            logging.error("All arguments to commands must be keyword-only")
            assert True
