# test_ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:54 PM


import pytest
from construct import Int32ub

from open_gopro.api.builders import BleSettingFacade
from open_gopro.models import constants
from open_gopro.models.constants import GoProUUID, SettingId
from tests.mocks import MockBleCommunicator, MockGoproResp


@pytest.mark.asyncio
async def test_write_command_correct_uuid_cmd_id(mock_ble_communicator: MockBleCommunicator):
    await mock_ble_communicator.ble_command.set_shutter(shutter=constants.Toggle.ENABLE)
    assert mock_ble_communicator.spy["uuid"] == GoProUUID.CQ_COMMAND
    assert mock_ble_communicator.spy["packet"] == bytearray([1, 1, 1])


@pytest.mark.asyncio
async def test_write_command_correct_parameter_data(mock_ble_communicator: MockBleCommunicator):
    await mock_ble_communicator.ble_command.load_preset(preset=5)
    assert mock_ble_communicator.spy["uuid"] == GoProUUID.CQ_COMMAND
    assert Int32ub.parse(mock_ble_communicator.spy["packet"][-4:]) == 5


@pytest.mark.asyncio
async def test_read_command_correct_uuid(mock_ble_communicator: MockBleCommunicator):
    await mock_ble_communicator.ble_command.get_wifi_ssid()
    assert mock_ble_communicator.spy["uuid"] == GoProUUID.WAP_SSID


@pytest.mark.asyncio
async def test_ble_setting_set(mock_ble_communicator: MockBleCommunicator):
    await mock_ble_communicator.ble_setting.led.set(constants.LED_SPECIAL.BLE_KEEP_ALIVE)
    assert mock_ble_communicator.spy["uuid"] == GoProUUID.CQ_SETTINGS
    assert mock_ble_communicator.spy["packet"] == bytearray([SettingId.LED, 1, constants.LED_SPECIAL.BLE_KEEP_ALIVE])


@pytest.mark.asyncio
async def test_fastpass_shutter(mock_ble_communicator: MockBleCommunicator):
    await mock_ble_communicator.ble_command.set_shutter(shutter=constants.Toggle.ENABLE)
    assert mock_ble_communicator.spy["uuid"] == GoProUUID.CQ_COMMAND


@pytest.mark.asyncio
async def test_ble_setting_get_value(mock_ble_communicator: MockBleCommunicator):
    # GIVEN
    setting = BleSettingFacade(
        communicator=mock_ble_communicator,
        identifier=SettingId.ANTI_FLICKER,
        parser_builder=constants.settings.Anti_Flicker,
    )
    mock_ble_communicator.set_ble_message_response(MockGoproResp(constants.settings.Anti_Flicker.NTSC))

    # WHEN
    response = await setting.get_value()

    # THEN
    assert response.ok
    assert response.data == constants.settings.Anti_Flicker.NTSC


@pytest.mark.asyncio
async def test_ble_setting_get_capabilities(mock_ble_communicator: MockBleCommunicator):
    # GIVEN
    setting = BleSettingFacade(
        communicator=mock_ble_communicator,
        identifier=SettingId.ANTI_FLICKER,
        parser_builder=constants.settings.Anti_Flicker,
    )
    mock_ble_communicator.set_ble_message_response(MockGoproResp([constants.settings.Anti_Flicker.NTSC]))

    # WHEN
    response = await setting.get_capabilities_values()

    # THEN
    assert response.ok
    assert response.data == [constants.settings.Anti_Flicker.NTSC]
