# test_ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:54 PM

import inspect
import logging
from typing import cast

import pytest
from construct import Int32ub

from open_gopro import Params, proto
from open_gopro.communicator_interface import GoProBle
from open_gopro.constants import CmdId, GoProUUIDs, QueryCmdId, SettingId, StatusId
from open_gopro.gopro_base import GoProBase
from tests.conftest import MockBleCommunicator


@pytest.mark.asyncio
async def test_write_command_correct_uuid_cmd_id(mock_ble_communicator: GoProBase):
    response = await mock_ble_communicator.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
    response = cast(dict, response)
    assert response["uuid"] == GoProUUIDs.CQ_COMMAND
    assert response["packet"][0] == CmdId.SET_SHUTTER.value


@pytest.mark.asyncio
async def test_write_command_correct_parameter_data(mock_ble_communicator: GoProBase):
    response = await mock_ble_communicator.ble_command.load_preset(preset=5)
    response = cast(dict, response)
    assert response["uuid"] == GoProUUIDs.CQ_COMMAND
    assert Int32ub.parse(response["packet"][-4:]) == 5


@pytest.mark.asyncio
async def test_read_command_correct_uuid(mock_ble_communicator: GoProBase):
    response = await mock_ble_communicator.ble_command.get_wifi_ssid()
    response = cast(dict, response)
    assert response["uuid"] == GoProUUIDs.WAP_SSID
