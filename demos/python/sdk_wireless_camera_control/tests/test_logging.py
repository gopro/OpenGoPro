# test_logging.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:49 UTC 2024

from typing import Generic, TypeVar

import construct
import pytest

from open_gopro import GoProResp
from open_gopro.api.builders import (
    BleProtoCommand,
    BleReadCommand,
    BleSettingFacade,
    BleStatusFacade,
    BleWriteCommand,
    HttpSetting,
)
from open_gopro.communicator_interface import HttpMessage, Message
from open_gopro.constants import (
    ActionId,
    CmdId,
    ErrorCode,
    FeatureId,
    GoProUUIDs,
    QueryCmdId,
    SettingId,
    StatusId,
)

dummy_kwargs = {"first": 1, "second": 2}


def assert_kwargs(message: dict):
    assert message.pop("first") == 1
    assert message.pop("second") == 2


@pytest.mark.asyncio
async def test_ble_read_command():
    message = BleReadCommand(uuid=GoProUUIDs.ACC_APPEARANCE, parser=None)
    d = message._as_dict(**dummy_kwargs)
    assert d.pop("id") == GoProUUIDs.ACC_APPEARANCE
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.ACC_APPEARANCE
    assert_kwargs(d)
    assert not d


@pytest.mark.asyncio
async def test_ble_write_command():
    message = BleWriteCommand(uuid=GoProUUIDs.ACC_APPEARANCE, cmd=CmdId.GET_CAMERA_CAPABILITIES)
    d = message._as_dict(**dummy_kwargs)
    assert d.pop("id") == CmdId.GET_CAMERA_CAPABILITIES
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.ACC_APPEARANCE
    assert_kwargs(d)
    assert not d


@pytest.mark.asyncio
async def test_ble_proto_command():
    message = BleProtoCommand(
        uuid=GoProUUIDs.ACC_APPEARANCE,
        feature_id=FeatureId.COMMAND,
        action_id=ActionId.GET_AP_ENTRIES,
        response_action_id=ActionId.GET_AP_ENTRIES_RSP,
        request_proto=None,
        response_proto=None,
        parser=None,
    )
    d = message._as_dict(**dummy_kwargs)
    assert d.pop("id") == ActionId.GET_AP_ENTRIES
    assert d.pop("feature_id") == FeatureId.COMMAND
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.ACC_APPEARANCE
    assert_kwargs(d)
    assert not d


T = TypeVar("T", bound=Message)


class MockCommunicator(Generic[T]):
    def __init__(self) -> None:
        self.message: T

    async def _send_ble_message(self, message: T) -> GoProResp:
        self.message = message
        return GoProResp(
            protocol=GoProResp.Protocol.BLE, status=ErrorCode.SUCCESS, data=bytes(), identifier=message._identifier
        )

    async def _get_json(self, message, **kwargs) -> GoProResp:
        self.message = message
        return GoProResp(protocol=GoProResp.Protocol.BLE, status=ErrorCode.SUCCESS, data=bytes(), identifier="unknown")

    def register_update(self, *args, **kwargs):
        ...

    def unregister_update(self, *args, **kwargs):
        ...


@pytest.mark.asyncio
async def test_ble_setting():
    class Communicator(MockCommunicator[BleSettingFacade.BleSettingMessageBase]):
        ...

    communicator = Communicator()
    message = BleSettingFacade(
        communicator=communicator, identifier=SettingId.ADDON_MAX_LENS_MOD, parser_builder=construct.Flag
    )

    # Set Setting Value
    await message.set(bytes())
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("setting_id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_SETTINGS
    assert_kwargs(d)
    assert not d

    # Get Setting Value
    await message.get_value()
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.GET_SETTING_VAL
    assert d.pop("setting_id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d

    # Get Setting Capabilities Values
    await message.get_capabilities_values()
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.GET_CAPABILITIES_VAL
    assert d.pop("setting_id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d

    # Register value updates
    await message.register_value_update(None)
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.REG_SETTING_VAL_UPDATE
    assert d.pop("setting_id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d

    # Unregister value updates
    await message.unregister_value_update(None)
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.UNREG_SETTING_VAL_UPDATE
    assert d.pop("setting_id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d

    # Register capability updates
    await message.register_capability_update(None)
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.REG_CAPABILITIES_UPDATE
    assert d.pop("setting_id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d

    # Unregister capability updates
    await message.unregister_capability_update(None)
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.UNREG_CAPABILITIES_UPDATE
    assert d.pop("setting_id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d


@pytest.mark.asyncio
async def test_ble_status():
    class Communicator(MockCommunicator[BleStatusFacade.BleStatusMessageBase]):
        ...

    communicator = Communicator()
    message = BleStatusFacade(communicator=communicator, identifier=StatusId.ACC_MIC_STAT, parser=construct.Flag)

    # Get Status Value
    await message.get_value()
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.GET_STATUS_VAL
    assert d.pop("status_id") == StatusId.ACC_MIC_STAT
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d

    # Register value updates
    await message.register_value_update(None)
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.REG_STATUS_VAL_UPDATE
    assert d.pop("status_id") == StatusId.ACC_MIC_STAT
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d

    # Unregister value updates
    await message.unregister_value_update(None)
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == QueryCmdId.UNREG_STATUS_VAL_UPDATE
    assert d.pop("status_id") == StatusId.ACC_MIC_STAT
    assert d.pop("protocol") == GoProResp.Protocol.BLE
    assert d.pop("uuid") == GoProUUIDs.CQ_QUERY
    assert_kwargs(d)
    assert not d


@pytest.mark.asyncio
async def test_http_command():
    message = HttpMessage("endpoint", identifier=None)
    d = message._as_dict(**dummy_kwargs)
    assert d.pop("id") == "Endpoint"
    assert d.pop("protocol") == GoProResp.Protocol.HTTP
    assert d.pop("endpoint") == "endpoint"
    assert_kwargs(d)
    assert not d


@pytest.mark.asyncio
async def test_http_setting():
    class Communicator(MockCommunicator[HttpMessage]):
        ...

    communicator = Communicator()
    message = HttpSetting(communicator=communicator, identifier=SettingId.ADDON_MAX_LENS_MOD)
    await message.set(1)
    d = communicator.message._as_dict(**dummy_kwargs)
    assert d.pop("id") == SettingId.ADDON_MAX_LENS_MOD
    assert d.pop("protocol") == GoProResp.Protocol.HTTP
    assert d.pop("endpoint") == r"gopro/camera/setting?setting={setting}&option={option}"
    assert_kwargs(d)
    assert not d
