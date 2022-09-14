# test_ble_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:54 PM

from construct import Int32ub

from open_gopro.interface import GoProBle
from open_gopro.constants import SettingId, StatusId, GoProUUIDs, CmdId, QueryCmdId
from open_gopro import proto, Params
from open_gopro.responses import GoProResp
from tests.conftest import BleCommunicatorTest


def test_write_command_correct_uuid_cmd_id(ble_communicator: GoProBle):
    response = ble_communicator.ble_command.set_shutter(Params.Toggle.ENABLE)
    assert response.uuid == GoProUUIDs.CQ_COMMAND
    assert response._raw_packet[0] == CmdId.SET_SHUTTER.value


def test_write_command_correct_parameter_data(ble_communicator: GoProBle):
    response = ble_communicator.ble_command.load_preset(5)
    assert response.uuid == GoProUUIDs.CQ_COMMAND
    assert Int32ub.parse(response._raw_packet[-4:]) == 5


def test_read_command_correct_uuid(ble_communicator: GoProBle):
    response = ble_communicator.ble_command.get_wifi_ssid()
    assert response.uuid == GoProUUIDs.WAP_SSID


def test_setting_set(ble_communicator: GoProBle):
    response = ble_communicator.ble_setting.resolution.set(Params.Resolution.RES_1080)
    assert response.uuid == GoProUUIDs.CQ_SETTINGS
    assert response._raw_packet[0] == SettingId.RESOLUTION.value
    assert response._raw_packet[2] == Params.Resolution.RES_1080.value


def test_setting_get_value(ble_communicator: GoProBle):
    response = ble_communicator.ble_setting.resolution.get_value()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.GET_SETTING_VAL.value
    assert response._raw_packet[1] == SettingId.RESOLUTION.value


def test_setting_get_capabilities_values(ble_communicator: GoProBle):
    response = ble_communicator.ble_setting.resolution.get_capabilities_values()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.GET_CAPABILITIES_VAL.value
    assert response._raw_packet[1] == SettingId.RESOLUTION.value


def test_setting_register_value_update(ble_communicator: GoProBle):
    response = ble_communicator.ble_setting.resolution.register_value_update()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.REG_SETTING_VAL_UPDATE.value
    assert response._raw_packet[1] == SettingId.RESOLUTION.value


def test_setting_unregister_value_update(ble_communicator: GoProBle):
    response = ble_communicator.ble_setting.resolution.unregister_value_update()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.UNREG_SETTING_VAL_UPDATE.value
    assert response._raw_packet[1] == SettingId.RESOLUTION.value


def test_setting_register_capability_update(ble_communicator: GoProBle):
    response = ble_communicator.ble_setting.resolution.register_capability_update()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.REG_CAPABILITIES_UPDATE.value
    assert response._raw_packet[1] == SettingId.RESOLUTION.value


def test_setting_unregister_capability_update(ble_communicator: GoProBle):
    response = ble_communicator.ble_setting.resolution.unregister_capability_update()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.UNREG_CAPABILITIES_UPDATE.value
    assert response._raw_packet[1] == SettingId.RESOLUTION.value


def test_status_get_value(ble_communicator: GoProBle):
    response = ble_communicator.ble_status.encoding_active.get_value()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.GET_STATUS_VAL.value
    assert response._raw_packet[1] == StatusId.ENCODING.value


def test_status_register_value_update(ble_communicator: GoProBle):
    assert ble_communicator._register_listener(None)
    response = ble_communicator.ble_status.encoding_active.register_value_update()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.REG_STATUS_VAL_UPDATE.value
    assert response._raw_packet[1] == StatusId.ENCODING.value


def test_status_unregister_value_update(ble_communicator: GoProBle):
    assert ble_communicator._unregister_listener(None)
    response = ble_communicator.ble_status.encoding_active.unregister_value_update()
    assert response.uuid == GoProUUIDs.CQ_QUERY
    assert response._raw_packet[0] == QueryCmdId.UNREG_STATUS_VAL_UPDATE.value
    assert response._raw_packet[1] == StatusId.ENCODING.value


def test_proto_command_arg(ble_communicator: GoProBle):
    response = ble_communicator.ble_command.set_turbo_mode(True)
    assert response.uuid == GoProUUIDs.CQ_COMMAND
    assert response._raw_packet == bytearray(b"\xf1k\x08\x01")
    out = proto.ResponseGeneric.FromString(response._raw_packet[2:])
    str(out)


def test_commands_iteration(ble_communicator: BleCommunicatorTest):
    for commands in [
        ble_communicator._api.ble_command,
        ble_communicator._api.ble_setting,
        ble_communicator._api.ble_status,
        ble_communicator._api.wifi_command,
        ble_communicator._api.wifi_setting,
    ]:
        count = 0
        for _ in commands:
            count += 1
        assert count > 0


def test_commands_subscriptable(ble_communicator: BleCommunicatorTest):
    for commands, identifier in zip(
        [
            ble_communicator._api.ble_command,
            ble_communicator._api.ble_setting,
            ble_communicator._api.ble_status,
            # ble_communicator._api.wifi_command,
            ble_communicator._api.wifi_setting,
        ],
        [
            CmdId,
            SettingId,
            StatusId,
            # CmdId,
            SettingId,
        ],
    ):
        try:
            assert commands[list(identifier)[0]]
        except TypeError:
            assert True
            continue
