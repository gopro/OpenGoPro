# test_wifi_commands.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:35 AM

from pathlib import Path

import pytest

from open_gopro.wifi_commands import WifiCommands, WifiSettings, WifiCommunicator
from open_gopro import params


@pytest.fixture
def wifi():
    class Communicator(WifiCommunicator):
        def __init__(self):
            self.commands = WifiCommands(self)
            self.settings = WifiSettings(self)

        def get(self, url: str):
            return url

        def stream_to_file(self, url: str, file: Path):
            return url, file

    yield Communicator()


def test_get_with_no_params(wifi):
    url = wifi.commands.set_third_party_client_info()
    assert url == "gp/gpControl/command/set_client_info"


def test_get_with_params(wifi):
    zoom = 99
    url = wifi.commands.set_digital_zoom(zoom)
    assert url == f"gopro/camera/digital_zoom?percent={zoom}"


def test_get_binary(wifi):
    file = wifi.commands.download_file(camera_file="test_file", local_file=Path("local_file"))
    assert file.name == "local_file"
