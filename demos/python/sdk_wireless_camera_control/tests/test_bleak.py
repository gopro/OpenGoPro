# test_bleak.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:35 AM

"""Test the bleak BLE Controller"""

import pytest

from open_gopro.ble_controller import BleakController


@pytest.fixture
def ble():
    ble = BleakController()
    yield ble


def test_scan(ble):
    # token =  re.compile(r"GoPro \d\d\d\d")
    # device = asyncio.run(ble.scan(token))
    # print(device)
    assert True


# device = None
# while device is None:
#     try:
#         device = await ble.scan(token)
#     except ScanFailedToFindDevice:
#         pass

# client = await ble.connect(device)

# await asyncio.sleep(5)

# await ble.disconnect(client)
