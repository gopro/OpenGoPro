# test_gopro.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:35 AM

"""Test the GoPro class"""

import time
import pytest
from typing import Optional

from bleak import BleakError

from open_gopro import params
from open_gopro.gopro import GoPro, InternalState
from open_gopro.interfaces import GoProNotInitialized, WifiController, ConnectFailed


class DummyWifi(WifiController):
    def connect(self, ssid: str, password: str):
        raise NotImplementedError

    def disconnect(self) -> bool:
        raise NotImplementedError

    def current(self):
        raise NotImplementedError

    def interfaces(self):
        raise NotImplementedError

    def interface(self, interface: Optional[str]):
        raise NotImplementedError

    def power(self, power: bool):
        raise NotImplementedError

    @property
    def is_on(self) -> bool:
        raise NotImplementedError


@pytest.fixture
def gopro():
    gopro = GoPro("dummy_token", wifi_adapter=DummyWifi)
    yield gopro


def test_state_properties(gopro):
    assert gopro.identifier is None
    assert not gopro.is_discovered
    assert not gopro.is_ble_connected
    assert not gopro.is_initialized


@pytest.mark.xfail
def test_wifi_connected(gopro):
    assert gopro.is_wifi_connected


# def test_failed_scan(gopro):
#     assert gopro.scan(timeout=0.1, retries=1) is None


def test_failed_connection(gopro):
    with pytest.raises(ConnectFailed) as e:
        gopro.establish_ble("12345678", retries=1, timeout=1)


# TODO fix initialized
@pytest.mark.xfail
def test_cant_send_write_unless_initialized(gopro):
    with pytest.raises(GoProNotInitialized) as e:
        gopro.ble_command.set_shutter(params.Shutter.OFF)


def test_cant_send_get_unless_initialized(gopro):
    with pytest.raises(GoProNotInitialized) as e:
        gopro.wifi_command.set_preset(params.Preset.PHOTO)


def test_control_semaphore(gopro):
    gopro._client = True
    gopro.state_thread.start()
    time.sleep(1)

    # Attempt to get the semaphore. It should fail
    assert gopro.ready.acquire(timeout=0.1) is False

    # Now appease the thread so it releases the semaphore
    with gopro._state_condition:
        gopro._internal_state = InternalState(0)
        gopro._state_condition.notify()

    assert gopro.ready.acquire(timeout=2)
    gopro.ready.release()
    # Make the thread acquire the semaphore
    with gopro._state_condition:
        gopro._internal_state = InternalState(1)
        gopro._state_condition.notify()

    gopro._client = None  # needed to allow thread to end after we release
    with gopro._state_condition:
        gopro._state_condition.notify()
