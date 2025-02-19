# test_ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:54 PM


import pytest
from construct import Int32ub

from open_gopro import Params
from open_gopro.constants import GoProUUID, SettingId
from open_gopro.gopro_base import GoProBase


@pytest.mark.asyncio
async def test_write_command_correct_uuid_cmd_id(mock_ble_communicator: GoProBase):
    response = await mock_ble_communicator.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
    assert response["uuid"] == GoProUUID.CQ_COMMAND
    assert response["packet"] == bytearray([1, 1, 1])


@pytest.mark.asyncio
async def test_write_command_correct_parameter_data(mock_ble_communicator: GoProBase):
    response = await mock_ble_communicator.ble_command.load_preset(preset=5)
    assert response["uuid"] == GoProUUID.CQ_COMMAND
    assert Int32ub.parse(response["packet"][-4:]) == 5


@pytest.mark.asyncio
async def test_read_command_correct_uuid(mock_ble_communicator: GoProBase):
    response = await mock_ble_communicator.ble_command.get_wifi_ssid()
    assert response["uuid"] == GoProUUID.WAP_SSID


@pytest.mark.asyncio
async def test_ble_setting(mock_ble_communicator: GoProBase):
    response = await mock_ble_communicator.ble_setting.led.set(Params.LED.BLE_KEEP_ALIVE)
    assert response["uuid"] == GoProUUID.CQ_SETTINGS
    assert response["packet"] == bytearray([SettingId.LED, 1, Params.LED.BLE_KEEP_ALIVE])


@pytest.mark.asyncio
async def test_fastpass_shutter(mock_ble_communicator: GoProBase):
    response = await mock_ble_communicator.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
    assert response["uuid"] == GoProUUID.CQ_COMMAND
