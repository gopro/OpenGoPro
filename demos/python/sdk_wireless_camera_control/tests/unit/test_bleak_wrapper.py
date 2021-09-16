# test_bleak_wrapper.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""Unit testing of bleak controller"""

import pytest

from open_gopro.ble.adapters.bleak_wrapper import BleakWrapperController


@pytest.mark.asyncio
def test_singleton(bleak_wrapper: BleakWrapperController):
    new_bleak_wrapper = BleakWrapperController()
    assert bleak_wrapper is new_bleak_wrapper


@pytest.mark.asyncio
def test_module_loop_running(bleak_wrapper: BleakWrapperController):
    assert bleak_wrapper._module_thread.is_alive()
    assert bleak_wrapper._ready.is_set()
