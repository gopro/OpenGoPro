# test_ble_commands.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:51 UTC 2021

import pytest
from construct import Int32ub

from open_gopro.ble_commands import BLECommunicator, BleCommands, BleSettings, BleStatuses
from open_gopro.constants import SettingId, StatusId, UUID, CmdId, QueryCmdId, ProducerType
from open_gopro import params, proto


@pytest.fixture
def ble():
    class Communicator(BLECommunicator):
        def __init__(self):
            self.commands = BleCommands(self)
            self.statuses = BleStatuses(self)
            self.settings = BleSettings(self)

        def read(self, uuid: UUID):
            return uuid

        def write(self, uuid: UUID, data: bytearray):
            return uuid, data

        def register_listener(self, producer: ProducerType) -> bool:
            return True

        def unregister_listener(self, producer: ProducerType) -> bool:
            return True

        def get_update(self) -> bool:
            return True

    yield Communicator()


def test_write_command_correct_uuid_cmd_id(ble):
    uuid, data = ble.commands.set_shutter(params.Shutter.ON)
    assert uuid is UUID.CQ_COMMAND
    assert data[1] == CmdId.SET_SHUTTER.value


def test_write_command_correct_parameter_data(ble):
    uuid, data = ble.commands.load_preset(params.Preset.TIME_LAPSE)
    assert uuid is UUID.CQ_COMMAND
    assert Int32ub.parse(data[-4:]) == params.Preset.TIME_LAPSE.value


def test_read_command_correct_uuid(ble):
    uuid = ble.commands.get_wifi_ssid()
    assert uuid is UUID.WAP_SSID


def test_setting_set(ble):
    uuid, data = ble.settings.resolution.set(params.Resolution.RES_1080)
    assert uuid is UUID.CQ_SETTINGS
    assert data[1] == SettingId.RESOLUTION.value
    assert data[3] == params.Resolution.RES_1080.value


def test_setting_get_value(ble):
    uuid, data = ble.settings.resolution.get_value()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.GET_SETTING_VAL.value
    assert data[2] == SettingId.RESOLUTION.value


def test_setting_get_capabilities_values(ble):
    uuid, data = ble.settings.resolution.get_capabilities_values()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.GET_CAPABILITIES_VAL.value
    assert data[2] == SettingId.RESOLUTION.value


def test_setting_register_value_update(ble):
    uuid, data = ble.settings.resolution.register_value_update()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.REG_SETTING_VAL_UPDATE.value
    assert data[2] == SettingId.RESOLUTION.value


def test_setting_unregister_value_update(ble):
    uuid, data = ble.settings.resolution.unregister_value_update()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.UNREG_SETTING_VAL_UPDATE.value
    assert data[2] == SettingId.RESOLUTION.value


def test_setting_register_capability_update(ble):
    uuid, data = ble.settings.resolution.register_capability_update()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.REG_CAPABILITIES_UPDATE.value
    assert data[2] == SettingId.RESOLUTION.value


def test_setting_unregister_capability_update(ble):
    uuid, data = ble.settings.resolution.unregister_capability_update()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.UNREG_CAPABILITIES_UPDATE.value
    assert data[2] == SettingId.RESOLUTION.value


def test_status_get_value(ble):
    uuid, data = ble.statuses.encoding_active.get_value()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.GET_STATUS_VAL.value
    assert data[2] == StatusId.ENCODING.value


def test_status_register_value_update(ble):
    assert ble.register_listener(None)
    uuid, data = ble.statuses.encoding_active.register_value_update()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.REG_STATUS_VAL_UPDATE.value
    assert data[2] == StatusId.ENCODING.value


def test_status_unregister_value_update(ble):
    assert ble.unregister_listener(None)
    uuid, data = ble.statuses.encoding_active.unregister_value_update()
    assert uuid is UUID.CQ_QUERY
    assert data[1] == QueryCmdId.UNREG_STATUS_VAL_UPDATE.value
    assert data[2] == StatusId.ENCODING.value


def test_proto_command_arg(ble):
    uuid, data = ble.commands.set_turbo_mode(True)
    assert uuid is UUID.CQ_COMMAND
    assert data == bytearray(b"\x04\xf1k\x08\x01")
    out = proto.ResponseGeneric.FromString(data[3:])
    print(out)
    d = out.to_dict()


def test_proto_command_kwargs(ble):
    uuid, data = ble.commands.get_preset_status(
        register_preset_status=[
            params.EnumRegisterPresetStatus.REGISTER_PRESET_STATUS_PRESET,
            params.EnumRegisterPresetStatus.REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY,
        ],
        unregister_preset_status=[params.EnumRegisterPresetStatus.REGISTER_PRESET_STATUS_PRESET],
    )
    assert uuid is UUID.CQ_COMMAND
    assert data == b"\t\xf5\x02\n\x02\x01\x02\x12\x01\x01"
