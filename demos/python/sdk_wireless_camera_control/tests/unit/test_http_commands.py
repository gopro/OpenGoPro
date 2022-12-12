# test_wifi_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:55 PM

import inspect
from pathlib import Path

from open_gopro.interface import GoProWifi


def test_get_with_no_params(wifi_communicator: GoProWifi):
    response = wifi_communicator.http_command.get_media_list()
    assert response.url == "gopro/media/list"


def test_get_with_params(wifi_communicator: GoProWifi):
    zoom = 99
    response = wifi_communicator.http_command.set_digital_zoom(percent=zoom)
    assert response.url == f"gopro/camera/digital_zoom?percent={zoom}"


def test_with_multiple_params(wifi_communicator: GoProWifi):
    media_file = "XXX.mp4"
    offset_ms = 2500
    response = wifi_communicator.http_command.add_file_hilight(file=media_file, offset=offset_ms)
    assert response.url == "gopro/media/hilight/file?path=100GOPRO/XXX.mp4&ms=2500"


def test_get_binary(wifi_communicator: GoProWifi):
    file = wifi_communicator.http_command.download_file(camera_file="test_file", local_file=Path("local_file"))
    assert file.name == "local_file"


def test_ensure_no_positional_args(wifi_communicator: GoProWifi):
    for command in wifi_communicator.http_command.values():
        if inspect.getfullargspec(command).args != ["self"]:
            logging.error("All arguments to commands must be keyword-only")
            assert True
