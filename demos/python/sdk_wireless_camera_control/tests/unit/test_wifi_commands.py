# test_wifi_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:55 PM

from pathlib import Path

from open_gopro.communication_client import GoProWifi


def test_get_with_no_params(wifi_communicator: GoProWifi):
    url = wifi_communicator.wifi_command.get_media_list()
    assert url == "gopro/media/list"


def test_get_with_params(wifi_communicator: GoProWifi):
    zoom = 99
    url = wifi_communicator.wifi_command.set_digital_zoom(zoom)
    assert url == f"gopro/camera/digital_zoom?percent={zoom}"


def test_with_multiple_params(wifi_communicator: GoProWifi):
    media_file = "XXX.mp4"
    offset_ms = 2500
    url = wifi_communicator.wifi_command.add_video_hilight((media_file, offset_ms))
    assert url == "gopro/media/hilight/file?path=100GOPRO/XXX.mp4&ms=2500"


def test_get_binary(wifi_communicator: GoProWifi):
    file = wifi_communicator.wifi_command.download_file(camera_file="test_file", local_file=Path("local_file"))
    assert file.name == "local_file"
