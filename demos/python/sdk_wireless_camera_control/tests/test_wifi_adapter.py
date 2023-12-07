# test_wireless_wifi.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Sep 15 23:48:50 UTC 2021

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass
from enum import Enum, auto
from typing import Literal

import pytest

from open_gopro.wifi.adapters.wireless import SsidState, WifiCli

operating_systems = ["windows"]

OS_TYPE = Literal["windows"]

SSID = "GP24500456"
PASSWORD = "TEST_PASSWORD"


class InterfaceState(Enum):
    DISCONNECTED = auto()
    ASSOCIATING = auto()
    CONNECTED = auto()
    DISABLED = auto()


class CommandSender(ABC):
    def __init__(self) -> None:
        self.interface_state: InterfaceState = InterfaceState.DISCONNECTED

    @classmethod
    def from_os(cls, operating_system: str) -> "CommandSender":
        if operating_system == "windows":
            return WindowsCommandSender()
        else:
            raise NotImplementedError

    @abstractmethod
    def which(self, request: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, command: str) -> str:
        raise NotImplementedError


class WindowsCommandSender(CommandSender):
    def __init__(self) -> None:
        super().__init__()
        self.os: OS_TYPE = "windows"

    def which(self, request: str) -> str:
        if request == "netsh":
            return "valid"

    def __call__(self, command: str) -> str:
        response = None
        if command == r"where netsh":
            response = r"C:\Windows\System32\netsh.exe"
        elif command == r"netsh wlan show interfaces":
            if self.interface_state == InterfaceState.DISCONNECTED:
                response = r"""
There is 1 interface on the system:



    Name                   : Wi-Fi

    Description            : TP-Link Wireless USB Adapter

    GUID                   : 093d8022-33cb-4400-8362-275eaf24cb86

    Physical address       : 98:48:27:88:cb:18

    State                  : disconnected

    Radio status           : Hardware On

                             Software On



    Hosted network status  : Not available"""
            elif self.interface_state == InterfaceState.ASSOCIATING:
                response = r"""
There is 1 interface on the system:



    Name                   : Wi-Fi

    Description            : TP-Link Wireless USB Adapter

    GUID                   : 093d8022-33cb-4400-8362-275eaf24cb86

    Physical address       : 98:48:27:88:cb:18

    State                  : associating

    Radio status           : Hardware On

                             Software On



    Hosted network status  : Not available"""
            elif self.interface_state == InterfaceState.CONNECTED:
                response = r"""
There is 1 interface on the system:


    Name                   : Wi-Fi

    Description            : TP-Link Wireless USB Adapter

    GUID                   : 093d8022-33cb-4400-8362-275eaf24cb86

    Physical address       : 98:48:27:88:cb:18

    State                  : connected

    SSID                   : GP24500456

    BSSID                  : 26:74:f7:4c:46:33

    Network type           : Infrastructure

    Radio type             : 802.11ac

    Authentication         : WPA2-Personal

    Cipher                 : CCMP

    Connection mode        : Profile

    Channel                : 161

    Receive rate (Mbps)    : 433.3

    Transmit rate (Mbps)   : 433.3

    Signal                 : 100%

    Profile                : GP24500456



    Hosted network status  : Not available"""
            elif self.interface_state == InterfaceState.DISABLED:
                response = r"""
There is no wireless interface on the system.
    Hosted network status  : Not available"""
        elif command == r"netsh wlan disconnect":
            response = ""
        elif command == r'netsh wlan delete profile name="GP24500456"':
            response = r'Profile "GP24500456" is deleted from interface "Wi-Fi".'
        elif command == r"add_profile":
            response = r"Profile GP24500456 is added on interface Wi-Fi."
        elif command == r'netsh wlan connect ssid="GP24500456" name="GP24500456" interface="Wi-Fi"':
            response = r"Connection request was completed successfully."
        elif command == r'netsh interface set interface "Wi-Fi" "enable"':
            response = r"This network connection does not exist."
        elif command == r'netsh interface set interface "Wi-Fi" "disable"':
            response = ""
        elif r"netsh wlan add profile filename" in command:
            response = r"Profile GP24500456 is added on interface Wi-Fi."
        elif r"netsh wlan disconnect interface" in command:
            response = r'Disconnection request was completed successfully for interface "Wi-Fi".'
        else:
            raise Exception(f"Not a handled command: {command}")

        assert response is not None
        return response.replace("\n", "\r\n")


@dataclass
class MockOs:
    os: str
    name: str = ""
    lang: InitVar[str] = "en_US"

    def __post_init__(self, lang):
        if self.os == "windows":
            self.name = "nt"
        else:
            raise NotImplementedError
        self.environ = {"LANG": lang}

    def write(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        pass

    def remove(self, *args, **kwargs):
        pass


@pytest.fixture(scope="function", params=operating_systems)
def command_sender(request, monkeypatch):
    command_sender = CommandSender.from_os(request.param)
    mock_os = MockOs(request.param)
    monkeypatch.setattr("open_gopro.wifi.adapters.wireless.cmd", command_sender)
    monkeypatch.setattr("open_gopro.wifi.adapters.wireless.os", mock_os)
    monkeypatch.setattr("open_gopro.wifi.adapters.wireless.which", command_sender.which)
    yield command_sender


@pytest.fixture(scope="function")
def wireless(command_sender):
    test_client = WifiCli()
    yield test_client


def test_power(wireless: WifiCli):
    assert wireless.power(True) is False
    assert wireless.power(False) is True


def test_initialized(wireless: WifiCli):
    assert wireless.current() == (None, SsidState.DISCONNECTED)


def test_connect(wireless: WifiCli, command_sender: CommandSender):
    command_sender.interface_state = InterfaceState.CONNECTED
    assert wireless.connect(SSID, PASSWORD, timeout=1)


def test_disconnect(wireless: WifiCli):
    assert wireless.disconnect()


def test_is_on(wireless: WifiCli, command_sender: CommandSender):
    assert wireless.is_on
    command_sender.interface_state = InterfaceState.DISABLED
    assert not wireless.is_on
