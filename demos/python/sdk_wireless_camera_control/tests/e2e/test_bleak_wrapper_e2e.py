# test_bleak_wrapper_e2e.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""End to end testing of BLE Controller(s)"""

# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

import re

import pytest
from bleak import BleakClient
from bleak.backends.device import BLEDevice as BleakDevice

from tests import cameras
from open_gopro.ble import FailedToFindDevice
from open_gopro.ble.adapters.bleak_wrapper import BleakWrapperController
from open_gopro.constants import GoProUUIDs


def disconnected_cb(_) -> None:
    print("Entered test disconnect callback")


def notification_cb(*_) -> None:
    print("Entered test notification callback")


@pytest.fixture(scope="module", params=list(cameras.keys()))
def device(bleak_wrapper: BleakWrapperController, request):
    print(f"\nScanning for {request.param}...")
    retries = 10
    for retry in range(retries):
        try:
            device = bleak_wrapper.scan(
                re.compile(cameras[request.param]), timeout=2, service_uuids=[GoProUUIDs.S_CONTROL_QUERY]
            )
            if device is not None and "gopro" in device.name.lower():
                yield device
                return
        except FailedToFindDevice as e:
            if retry == 10:
                raise FailedToFindDevice from e


@pytest.fixture(scope="module")
def client(bleak_wrapper: BleakWrapperController, device: BleakDevice):
    print("Connecting to device...")
    yield bleak_wrapper.connect(disconnected_cb, device)


def test_is_connected(client: BleakClient):
    assert client.is_connected


def test_pair(bleak_wrapper: BleakWrapperController, client: BleakClient):
    bleak_wrapper.pair(client)
    assert True


def test_discover_characteristics(bleak_wrapper: BleakWrapperController, client: BleakClient):
    attribute_table = bleak_wrapper.discover_chars(client)
    assert len(attribute_table.services) > 0


def test_enable_notifications(bleak_wrapper: BleakWrapperController, client: BleakClient):
    bleak_wrapper.enable_notifications(client, notification_cb)
    assert True


def test_disconnect(bleak_wrapper: BleakWrapperController, client: BleakClient):
    bleak_wrapper.disconnect(client)
    assert not client.is_connected
