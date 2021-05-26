# ble_commands.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Builds byte level commands and defines parsing for anything sent over BLE."""

import enum
import logging
from abc import abstractmethod, ABC
from typing import Any, Callable, Dict, List

import wrapt
import betterproto
import construct  # For enum
from construct import Int8ub, Int32ub, Int64ub, Flag, GreedyString, GreedyBytes, Struct

from open_gopro import params
from open_gopro.constants import (
    ActionId,
    ErrorCode,
    QueryCmdId,
    UUID,
    SettingId,
    CmdId,
    StatusId,
    ProducerType,
)
from open_gopro.responses import GoProResp, Parser, ParserType, BuilderType, ParserBuilderType
from open_gopro import proto

logger = logging.getLogger(__name__)


class BLECommunicator(ABC):
    """Interface definition for a client to communicate via BLE.

    This interface is used to build commands parse responses for:
    - :py:class:`open_gopro.ble_commands.BleCommands`
    - :py:class:`open_gopro.ble_commands.BleSettings`
    - :py:class:`open_gopro.ble_commands.BleStatuses`
    """

    @abstractmethod
    def write(self, uuid: UUID, data: bytearray) -> GoProResp:
        """Write data to a UUID.

        Args:
            uuid (UUID): UUID to write to
            data (bytearray): data to write

        Returns:
            GoProResp: response
        """
        raise NotImplementedError

    @abstractmethod
    def read(self, uuid: UUID) -> GoProResp:
        """Read data from an UUID.

        Args:
            uuid (UUID): UUID to read from

        Returns:
            GoProResp: data read from UUID
        """
        raise NotImplementedError

    @abstractmethod
    def register_listener(self, producer: ProducerType) -> None:
        """Register to receive notifications for a producer.

        Args:
            producer (ProducerType): producer that we want to receive notifications from
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_listener(self, producer: ProducerType) -> None:
        """Stop receiving notifications from a producer.

        Args:
            producer (ProducerType): Producer to stop receiving notifications for
        """
        raise NotImplementedError

    @abstractmethod
    def get_update(self, timeout: float = None) -> GoProResp:
        """Get a notification that was received from a registered producer.

        Args:
            timeout (float, optional): Time to wait for a notification before returning. Defaults to None (wait forever)

        Returns:
            GoProResp: the received update
        """
        raise NotImplementedError


# ========================================================Commands============================================


def read_cmd(uuid: UUID, response_parser: ParserType) -> Callable:
    """Build a BLE command that does a direct read from a UUID.

    Args:
        uuid (UUID): UUID to read from
        response_parser (ParserType): Parser to parse response. Can be either a construct Struct or a
        user defined Parser class

    Returns:
        Callable: function to build read command
    """

    @wrapt.decorator
    # pylint: disable = E, W
    def _wrapper(wrapped, instance, args, _):  # type: ignore
        logger.info(f"<----------- {wrapped.__name__} : {' '.join([str(a) for a in args])}")

        GoProResp.parser_map[uuid] = response_parser

        response = instance.communicator.read(uuid)
        logger.info(f"-----------> {wrapped.__name__} : {response}")
        return response

    return _wrapper


def write_cmd(
    id: CmdId,
    uuid: UUID,
    *,
    param_builder: BuilderType = None,
    response_parser: ParserType = None,
) -> Callable:
    """Build a BLE write command that writes to a UUID and receives responses via notifications.

    Args:
        id (CmdId): command to send
        uuid (UUID): uuid to write
        param_builder (BuilderType, optional): Optional builder that specifies how to build byte stream from param. Defaults to None.
        response_parser (ParserType, optional): Optional parser that defines how to build response from received byte stream. Defaults to None.

    Returns:
        Callable: function to build write command
    """

    @wrapt.decorator
    # pylint: disable = E, W
    def _wrapper(wrapped, instance, args, _):  # type: ignore
        status_struct = Struct("status" / construct.Enum(Int8ub, ErrorCode))

        logger.info(f"<----------- {wrapped.__name__} : {' '.join([str(a) for a in args])}")
        GoProResp.parser_map[id] = (
            status_struct if response_parser is None else (status_struct + response_parser)
        )

        data = bytearray([id.value])
        for arg in args:
            param = arg.value if issubclass(type(arg), enum.Enum) else arg
            # There must be a param builder if we have a param
            param = param_builder.build(param)  # type: ignore
            data.extend([len(param), *param])
        data.insert(0, len(data))
        response = instance.communicator.write(uuid, data)

        logger.info(f"-----------> \n{response}")
        return response

    return _wrapper


class ProtobufResponseAdapter(Parser):
    """Use a protobuf definition to parse a byte stream into a dict.

    Args:
        protobuf (Callable): protobuf to use as parser
    """

    def __init__(self, protobuf: betterproto.Message) -> None:
        self.protobuf = protobuf

    def parse(self, buf: bytearray) -> Dict[Any, Any]:
        """Parse byte stream into dict using protobuf.

        Args:
            buf (bytearray): input bytestream

        Returns:
            Dict[Any, Any]: output dict
        """
        return self.protobuf.FromString(buf).to_dict()


def proto_cmd(
    uuid: UUID, feature_id: CmdId, action_id: ActionId, request_proto: Callable, response_proto: Callable
) -> Callable:
    """Build a BLE command from a protobuf definition.

    Args:
        uuid (UUID): uuid to write to
        feature_id (CmdId): feature identifier
        action_id (ActionId): action identifier
        request_proto (Callable): protobuf definition to build request
        response_proto (Callable): protobuf definition to parse response

    Returns:
        Callable: function to build protobuf command
    """

    @wrapt.decorator
    # pylint: disable = E, W
    def _wrapper(wrapped, instance, args, kwargs):  # type: ignore
        logger.info(
            f"<----------- {wrapped.__name__} : {' '.join([*[str(a) for a in args], *[str(a) for a in kwargs.values()]])}"
        )

        if response_proto is not None:
            GoProResp.parser_map[action_id] = ProtobufResponseAdapter(response_proto)

        # Build request protobuf bytestream
        proto = request_proto()
        # Add args to protobuf request
        attrs = iter(wrapped.__annotations__.keys())
        for arg in args:
            param = arg.value if issubclass(type(arg), enum.Enum) else arg
            setattr(proto, next(attrs), param)
        # Add kwargs to protobuf request
        for name, arg in kwargs.items():
            if arg is not None:
                param = arg.value if issubclass(type(arg), enum.Enum) else arg
                setattr(proto, name, param)

        # Prepend headers and serialize
        request = bytearray([feature_id.value, action_id.value, *proto.SerializeToString()])
        # Prepend length
        request.insert(0, len(request))

        # Allow exception to pass through if protobuf not completely initialized
        response = instance.communicator.write(uuid, request)

        logger.info(f"-----------> \n{response}")
        return response

    return _wrapper


class BleCommands:
    """All of the BLE commands.

    To be used as a delegate for a BLECommunicator to build commands

    All of these return a GoProResp

    Args:
        communicator (BLECommunicator): [description]
    """

    def __init__(self, communicator: BLECommunicator):
        self.communicator = communicator

    @read_cmd(UUID.WAP_SSID, response_parser=Struct("ssid" / GreedyString("utf-8")))
    def get_wifi_ssid(self) -> GoProResp:
        """Get the Wifi SSID."""

    @read_cmd(UUID.WAP_PASSWORD, response_parser=Struct("password" / GreedyString("utf-8")))
    def get_wifi_password(self) -> GoProResp:
        """Get the WiFi password."""

    @write_cmd(CmdId.SET_SHUTTER, UUID.CQ_COMMAND, param_builder=Int8ub)
    def set_shutter(self, shutter: params.Shutter, /) -> GoProResp:
        """Set shutter on or off."""

    @write_cmd(CmdId.SET_PAIRING_COMPLETE, UUID.CQ_COMMAND, param_builder=Int8ub)
    def set_pairing_complete(self, status: bool, /) -> GoProResp:
        """Notify the peer that pairing has completed."""

    @write_cmd(CmdId.GET_CAMERA_STATUS, UUID.CQ_QUERY)
    def get_camera_status(self) -> GoProResp:
        """Get camera status."""

    @write_cmd(CmdId.GET_SETTINGS_JSON, UUID.CQ_COMMAND)
    def get_settings_json(self) -> GoProResp:
        """Get settings.json file."""

    @write_cmd(CmdId.GET_HW_INFO, UUID.CQ_COMMAND)
    def get_hardware_info(self) -> GoProResp:
        """Get hardware information."""

    @write_cmd(CmdId.LOAD_PRESET, UUID.CQ_COMMAND, param_builder=Int32ub)
    def load_preset(self, preset: params.Preset, /) -> GoProResp:
        """Load a Preset."""

    @write_cmd(CmdId.SET_WIFI, UUID.CQ_COMMAND, param_builder=Int8ub)
    def enable_wifi_ap(self, enable: bool, /) -> GoProResp:
        """Enable / disable the Wi-Fi Access Point."""

    @write_cmd(CmdId.SET_THIRD_PARTY_CLIENT_INFO, UUID.CQ_COMMAND)
    def set_third_party_client_info(self) -> GoProResp:
        """Flag as third party app."""

    @write_cmd(
        CmdId.GET_THIRD_PARTY_API_VERSION,
        UUID.CQ_COMMAND,
        response_parser=Struct("major" / Int8ub, "minor" / Int8ub),
    )
    def get_third_party_api_version(self) -> GoProResp:
        """Get Third party API version that is being used."""

    @proto_cmd(
        UUID.CQ_COMMAND,
        CmdId.SET_TURBO_MODE,
        ActionId.SET_TURBO_MODE,
        proto.RequestSetTurboActive,
        proto.ResponseGeneric,
    )
    def set_turbo_mode(self, active: bool, /) -> GoProResp:
        """Enable / disable turbo mode."""

    @proto_cmd(
        UUID.CQ_COMMAND,
        CmdId.GET_PRESET_STATUS,
        ActionId.GET_PRESET_STATUS,
        proto.RequestGetPresetStatus,
        proto.NotifyPresetStatus,
    )
    def get_preset_status(
        self,
        register_preset_status: List[params.EnumRegisterPresetStatus] = None,
        unregister_preset_status: List[params.EnumRegisterPresetStatus] = None,
    ) -> GoProResp:
        """Get the preset status.

        TODO This isn't working

        Args:
            register_preset_status (List[params.EnumRegisterPresetStatus], optional): [description]. Defaults to None.
            unregister_preset_status (List[params.EnumRegisterPresetStatus], optional): [description]. Defaults to None.

        Returns:
            GoProResp: the response
        """


# ========================================================Settings============================================


@wrapt.decorator
# pylint: disable = E, W
def setter_cmd(wrapped, instance, args, _):  # type: ignore
    """Build a BLE command that sets a Setting value."""
    logger.info(f"<----------- {wrapped.__name__} : {' '.join([str(a) for a in args])}")

    data = bytearray([instance.id.value])
    try:
        param = int(args[0])  # Do this first in separate step to allow IndexError to propagate
        param = instance.builder.build(param)  # There must be a param builder if we have a param
        data.extend([len(param), *param])
    except IndexError:
        pass
    data.insert(0, len(data))
    response = instance.communicator.write(instance.setter_uuid, data)

    logger.info(f"-----------> \n{response}")
    return response


@wrapt.decorator
# pylint: disable = E, W
def log_query(wrapped, instance, args, kwargs):  # type: ignore
    """Log a query write."""
    logger.info(f"<----------- {wrapped.__name__} : {instance.id}")
    response = wrapped(*args, **kwargs)
    logger.info(f"-----------> {response}")
    return response


class Setting(ABC):
    """An individual camera setting.

    Args:
        communicator (BLECommunicator): Adapter to read write settings data
        id (SettingId): ID of setting
        parser_builder (ParserBuilderType): object to both parse and build setting
    """

    def __init__(
        self, communicator: BLECommunicator, id: SettingId, parser_builder: ParserBuilderType
    ) -> None:
        self.id = id
        self.communicator: BLECommunicator = communicator
        self.setter_uuid: UUID = UUID.CQ_SETTINGS
        self.reader_uuid: UUID = UUID.CQ_QUERY
        self.parser: ParserBuilderType = parser_builder
        self.builder: ParserBuilderType = parser_builder  # Just syntactic sugar
        # Add to param parsing map
        GoProResp.parser_map[self.id] = self.parser

    @abstractmethod
    def set(self) -> GoProResp:
        """Set the value of the setting.

        This shall be implemented (and documented) by the subclass.

        Returns:
            GoProResp: Status of set
        """
        raise NotImplementedError("To be implemented by subclass")

    @log_query
    def get_value(self) -> GoProResp:
        """Get the settings value.

        Returns:
            GoProResp: settings value
        """
        return self.communicator.write(self.reader_uuid, self._build_cmd(QueryCmdId.GET_SETTING_VAL))

    @log_query
    def get_name(self) -> GoProResp:
        """Get the settings name.

        Raises:
            NotImplementedError: This isn't implemented on the camera

        Returns:
            GoProResp: settings name
        """
        # return self.communicator.write(
        #     self.reader_uuid, QueryCmdId.GET_SETTING_NAME, self._build_cmd(QueryCmdId.GET_SETTING_NAME)
        # )
        raise NotImplementedError("Not implemented on camera!")

    @log_query
    def get_capabilities_values(self) -> GoProResp:
        """Get currently supported settings capabilities values.

        Returns:
            GoProResp: settings capabilities values
        """
        return self.communicator.write(self.reader_uuid, self._build_cmd(QueryCmdId.GET_CAPABILITIES_VAL))

    @log_query
    def get_capabilities_names(self) -> GoProResp:
        """Get currently supported settings capabilities names.

        Raises:
            NotImplementedError: This isn't implemented on the camera

        Returns:
            GoProResp: settings capabilities names
        """
        # return self.communicator.write(
        #     self.reader_uuid,
        #     QueryCmdId.GET_CAPABILITIES_NAME,
        #     self._build_cmd(QueryCmdId.GET_CAPABILITIES_NAME),
        # )
        raise NotImplementedError("Not implemented on camera!")

    @log_query
    def register_value_update(self) -> GoProResp:
        """Register for asynchronous notifications when a given setting ID's value updates.

        Returns:
            GoProResp: Current value of respective setting ID
        """
        self.communicator.register_listener((QueryCmdId.SETTING_VAL_PUSH, self.id))
        return self.communicator.write(self.reader_uuid, self._build_cmd(QueryCmdId.REG_SETTING_VAL_UPDATE))

    @log_query
    def unregister_value_update(self) -> GoProResp:
        """Stop receiving notifications when a given setting ID's value updates.

        Returns:
            GoProResp: Status of unregister
        """
        self.communicator.unregister_listener((QueryCmdId.SETTING_VAL_PUSH, self.id))
        return self.communicator.write(self.reader_uuid, self._build_cmd(QueryCmdId.UNREG_SETTING_VAL_UPDATE))

    @log_query
    def register_capability_update(self) -> GoProResp:
        """Register for asynchronous notifications when a given setting ID's capabilities update.

        Returns:
            GoProResp: Current capabilities of respective setting ID
        """
        self.communicator.register_listener((QueryCmdId.SETTING_CAPABILITY_PUSH, self.id))
        return self.communicator.write(self.reader_uuid, self._build_cmd(QueryCmdId.REG_CAPABILITIES_UPDATE))

    @log_query
    def unregister_capability_update(self) -> GoProResp:
        """Stop receiving notifications when a given setting ID's capabilities change.

        Returns:
            GoProResp: Status of unregister
        """
        self.communicator.unregister_listener((QueryCmdId.SETTING_CAPABILITY_PUSH, self.id))
        return self.communicator.write(self.reader_uuid, self._build_cmd(QueryCmdId.UNREG_CAPABILITIES_UPDATE))

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data to send a settings query over-the-air.

        Args:
            cmd (QueryCmdId): command to build

        Returns:
            bytearray: data to send over-the-air
        """
        ret = bytearray([cmd.value, self.id.value])
        ret.insert(0, len(ret))
        return ret


# Lots of boiler-plate here. This is because we need a way to keep the type-hinting on the "set" method. And
# also to make the docstring generated documentation look nice.
class BleSettings:
    """The collection of all Settings.

    To be used by a BLECommunicator delegate to build setting commands.

    Args:
        communicator (BLECommunicator): Adapter to read / write settings
    """

    def __init__(self, communicator: BLECommunicator):
        self.communicator = communicator

        class Resolution(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, resolution: params.Resolution) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.resolution = Resolution(
            self.communicator, SettingId.RESOLUTION, construct.Enum(Int8ub, params.Resolution)
        )
        """Resolution. Set with :py:class:`open_gopro.params.Resolution`"""

        class FOV(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, fov: params.FieldOfView) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.video_field_of_view = FOV(
            self.communicator, SettingId.VIDEO_FOV, construct.Enum(Int8ub, params.FieldOfView)
        )
        """Video FOV. Set with :py:class:`open_gopro.params.FieldOfView`"""

        self.photo_field_of_view = FOV(
            self.communicator, SettingId.PHOTO_FOV, construct.Enum(Int8ub, params.FieldOfView)
        )
        """Photo FOV. Set with :py:class:`open_gopro.params.FieldOfView`"""

        self.multi_shot_field_of_view = FOV(
            self.communicator, SettingId.MULTI_SHOT_FOV, construct.Enum(Int8ub, params.FieldOfView)
        )
        """Multi-shot FOV. Set with :py:class:`open_gopro.params.FieldOfView`"""

        class FPS(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, fps: params.FPS) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.fps = FPS(self.communicator, SettingId.FPS, construct.Enum(Int8ub, params.FPS))
        """Frames per second. Set with :py:class:`open_gopro.params.FPS`"""

        class LED(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, led: params.LED) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.led = LED(self.communicator, SettingId.LED, construct.Enum(Int8ub, params.LED))
        """Set the LED options (or also send the BLE keep alive signal). Set with :py:class:`open_gopro.params.LED`"""

        class MaxLensMode(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, mode: params.MaxLensMode) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.max_lens_mode = MaxLensMode(
            self.communicator, SettingId.MAX_LENS_MOD, construct.Enum(Int8ub, params.MaxLensMode)
        )
        """Enable / disable max lens mod. Set with :py:class:`open_gopro.params.MaxLensMode`"""

        class Shortcut(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, shortcut: params.Shortcut) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.lower_left_shortcut = Shortcut(
            self.communicator, SettingId.SHORTCUT_LOWER_LEFT, construct.Enum(Int8ub, params.Shortcut)
        )
        """Lower left shortcut. Set with :py:class:`open_gopro.params.Shortcut`"""

        self.lower_right_shortcut = Shortcut(
            self.communicator, SettingId.SHORTCUT_LOWER_RIGHT, construct.Enum(Int8ub, params.Shortcut)
        )
        """Lower right shortcut. Set with :py:class:`open_gopro.params.Shortcut`"""

        self.upper_left_shortcut = Shortcut(
            self.communicator, SettingId.SHORTCUT_UPPER_LEFT, construct.Enum(Int8ub, params.Shortcut)
        )
        """Upper left shortcut. Set with :py:class:`open_gopro.params.Shortcut`"""

        self.upper_right_shortcut = Shortcut(
            self.communicator, SettingId.SHORTCUT_UPPER_RIGHT, construct.Enum(Int8ub, params.Shortcut)
        )
        """Upper right shortcut. Set with :py:class:`open_gopro.params.Shortcut`"""


# =================================================Statuses============================================


class Status:
    """An individual camera status.

    Args:
        communicator (BLECommunicator): Adapter to read status data
        id (StatusId): ID of status
    """

    uuid = UUID.CQ_QUERY

    def __init__(self, communicator: BLECommunicator, id: StatusId, parser: ParserType) -> None:
        self.id = id
        self.communicator = communicator
        self.parser = parser
        # Add to response parsing map
        GoProResp.parser_map[self.id] = self.parser

    @log_query
    def get_value(self) -> GoProResp:
        """Get the current value of a status.

        Returns:
            GoProResp: current status value
        """
        return self.communicator.write(Status.uuid, self._build_cmd(QueryCmdId.GET_STATUS_VAL))

    @log_query
    def register_value_update(self) -> GoProResp:
        """Register for asynchronous notifications when a status changes.

        Returns:
            GoProResp: current status value
        """
        self.communicator.register_listener((QueryCmdId.STATUS_VAL_PUSH, self.id))
        return self.communicator.write(Status.uuid, self._build_cmd(QueryCmdId.REG_STATUS_VAL_UPDATE))

    @log_query
    def unregister_value_update(self) -> GoProResp:
        """Stop receiving notifications when status changes.

        Returns:
            GoProResp: Status of unregister
        """
        self.communicator.unregister_listener((QueryCmdId.STATUS_VAL_PUSH, self.id))
        return self.communicator.write(Status.uuid, self._build_cmd(QueryCmdId.UNREG_STATUS_VAL_UPDATE))

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data for a given status command.

        Args:
            cmd (QueryCmdId): command to build data for

        Returns:
            bytearray: data to send over-the-air
        """
        ret = bytearray([cmd.value, self.id.value])
        ret.insert(0, len(ret))
        return ret


class BleStatuses:
    """All of the BLE Statuses.

    To be used by a BLECommunicator delegate to build status commands.
    """

    def __init__(self, communicator: BLECommunicator) -> None:
        self.communicator = communicator

        self.batt_present: Status = Status(self.communicator, StatusId.BATT_PRESENT, Flag)  # type: ignore
        """Is the system's internal battery present?"""

        self.batt_level: Status = Status(self.communicator, StatusId.BATT_LEVEL, Int8ub)
        """Rough approximation of internal battery level in bars."""

        self.ext_batt_present: Status = Status(self.communicator, StatusId.EXT_BATT_PRESENT, Flag)  # type: ignore
        """Is an external battery connected?"""

        self.ext_batt_level: Status = Status(self.communicator, StatusId.EXT_BATT_LEVEL, Int8ub)
        """External battery power level in percent."""

        self.system_hot: Status = Status(self.communicator, StatusId.SYSTEM_HOT, Flag)  # type: ignore
        """Is the system currently overheating?"""

        self.system_busy: Status = Status(self.communicator, StatusId.SYSTEM_BUSY, Flag)  # type: ignore
        """Is the camera busy?"""

        self.quick_capture: Status = Status(self.communicator, StatusId.QUICK_CAPTURE, Flag)  # type: ignore
        """Is quick capture feature enabled?"""

        self.encoding_active: Status = Status(self.communicator, StatusId.ENCODING, Flag)  # type: ignore
        """Is the camera currently encoding (i.e. capturing photo / video)?"""

        self.lcd_lock_active: Status = Status(self.communicator, StatusId.LCD_LOCK_ACTIVE, Flag)  # type: ignore
        """Is the LCD lock currently active?"""

        self.video_progress: Status = Status(self.communicator, StatusId.VIDEO_PROGRESS, Int8ub)
        """When encoding video, this is the duration (seconds) of the video so far; 0 otherwise."""

        self.wireless_enabled: Status = Status(self.communicator, StatusId.WIRELESS_ENABLED, Flag)  # type: ignore
        """Are Wireless Connections enabled?"""

        self.pair_state: Status = Status(
            self.communicator, StatusId.PAIR_STATE, construct.Enum(Int8ub, params.PairState)
        )
        """What is the pair state?"""

        self.pair_type: Status = Status(
            self.communicator, StatusId.PAIR_TYPE, construct.Enum(Int8ub, params.PairType)
        )
        """The last type of pairing that the camera was engaged in."""

        self.pair_time: Status = Status(self.communicator, StatusId.PAIR_TIME, Int32ub)
        """	Time (milliseconds) since boot of last successful pairing complete action."""

        self.wap_scan_state: Status = Status(
            self.communicator, StatusId.WAP_SCAN_STATE, construct.Enum(Int8ub, params.WAPState)
        )
        """State of current scan for WiFi Access Points. Appears to only change for CAH-related scans."""

        self.wap_scan_time: Status = Status(self.communicator, StatusId.WAP_SCAN_TIME, Int8ub)
        """The time, in milliseconds since boot that the WiFi Access Point scan completed."""

        self.wap_prov_stat: Status = Status(
            self.communicator, StatusId.WAP_PROV_STAT, construct.Enum(Int8ub, params.WAPState)
        )
        """WiFi AP provisioning state."""

        self.remote_ctrl_ver: Status = Status(self.communicator, StatusId.REMOTE_CTRL_VER, Int8ub)
        """What is the remote control version?"""

        self.remote_ctrl_conn: Status = Status(self.communicator, StatusId.REMOTE_CTRL_CONN, Flag)  # type: ignore
        """Is the remote control connected?"""

        self.pair_state2: Status = Status(self.communicator, StatusId.PAIR_STATE2, GreedyBytes)  # type: ignore
        """Wireless Pairing State."""

        self.wlan_ssid: Status = Status(self.communicator, StatusId.WLAN_SSID, GreedyString(encoding="utf-8"))
        """Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int."""

        self.ap_ssid: Status = Status(self.communicator, StatusId.AP_SSID, GreedyString(encoding="utf-8"))
        """Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int."""

        self.app_count: Status = Status(self.communicator, StatusId.APP_COUNT, Int8ub)
        """The number of wireless devices connected to the camera."""

        self.preview_enabled: Status = Status(self.communicator, StatusId.PREVIEW_ENABLED, Flag)  # type: ignore
        """Is preview stream enabled?"""

        self.sd_status: Status = Status(
            self.communicator, StatusId.SD_STATUS, construct.Enum(Int8ub, params.SDStatus)
        )
        """Primary Storage Status."""

        self.photos_rem: Status = Status(self.communicator, StatusId.PHOTOS_REM, Int32ub)
        """How many photos can be taken before sdcard is full?"""

        self.video_rem: Status = Status(self.communicator, StatusId.VIDEO_REM, Int32ub)
        """How many minutes of video can be captured with current settings before sdcard is full?"""

        self.num_group_photo: Status = Status(self.communicator, StatusId.NUM_GROUP_PHOTO, Int32ub)
        """How many group photos can be taken with current settings before sdcard is full?"""

        self.num_group_video: Status = Status(self.communicator, StatusId.NUM_GROUP_VIDEO, Int32ub)
        """Total number of group videos on sdcard."""

        self.num_total_photo: Status = Status(self.communicator, StatusId.NUM_TOTAL_PHOTO, Int32ub)
        """Total number of photos on sdcard."""

        self.num_total_video: Status = Status(self.communicator, StatusId.NUM_TOTAL_VIDEO, Int32ub)
        """Total number of videos on sdcard."""

        self.date_time: Status = Status(self.communicator, StatusId.DATE_TIME, GreedyString(encoding="utf-8"))
        """Current date/time (format: %YY%MM%DD%HH%MM%SS, all values in hex)."""

        self.ota_stat: Status = Status(
            self.communicator, StatusId.OTA_STAT, construct.Enum(Int8ub, params.OTAStatus)
        )
        """The current status of Over The Air (OTA) update."""

        self.download_cancel_pend: Status = Status(self.communicator, StatusId.DOWNLAD_CANCEL_PEND, Flag)  # type: ignore
        """Is download firmware update cancel request pending?"""

        self.mode_group: Status = Status(self.communicator, StatusId.MODE_GROUP, Int8ub)
        """Current mode group (deprecated in HERO8)."""

        self.locate_active: Status = Status(self.communicator, StatusId.LOCATE_ACTIVE, Flag)  # type: ignore
        """Is locate camera feature active?"""

        self.multi_count_down: Status = Status(self.communicator, StatusId.MULTI_COUNT_DOWN, Int32ub)
        """The current timelapse interval countdown value (e.g. 5...4...3...2...1...)."""

        self.space_rem: Status = Status(self.communicator, StatusId.SPACE_REM, Int64ub)
        """Remaining space on the sdcard in Kilobytes."""

        self.streaming_supp: Status = Status(self.communicator, StatusId.STREAMING_SUPP, Flag)  # type: ignore
        """Is streaming supports in current recording/flatmode/secondary-stream?"""

        self.wifi_bars: Status = Status(self.communicator, StatusId.WIFI_BARS, Int8ub)
        """WiFi signal strength in bars."""

        self.current_time_ms: Status = Status(self.communicator, StatusId.CURRENT_TIME_MS, Int32ub)
        """System time in milliseconds since system was booted."""

        self.num_hilights: Status = Status(self.communicator, StatusId.NUM_HILIGHTS, Int8ub)
        """The number of hilights in encoding video (set to 0 when encoding stops)."""

        self.last_hilight: Status = Status(self.communicator, StatusId.LAST_HILIGHT, Int32ub)
        """Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)."""

        self.next_poll: Status = Status(self.communicator, StatusId.NEXT_POLL, Int32ub)
        """The min time between camera status updates (msec). Do not poll for status more often than this."""

        self.analytics_rdy: Status = Status(
            self.communicator, StatusId.ANALYTICS_RDY, construct.Enum(Int8ub, params.AnalyticsState)
        )
        """The current state of camera analytics."""

        self.analytics_size: Status = Status(self.communicator, StatusId.ANALYTICS_SIZE, Int32ub)
        """The size (units??) of the analytics file."""

        self.in_context_menu: Status = Status(self.communicator, StatusId.IN_CONTEXT_MENU, Flag)  # type: ignore
        """Is the camera currently in a contextual menu (e.g. Preferences)?"""

        self.timelapse_rem: Status = Status(self.communicator, StatusId.TIMELAPSE_REM, Int32ub)
        """How many min of Timelapse video can be captured with current settings before sdcard is full?"""

        self.exposure_type: Status = Status(
            self.communicator, StatusId.EXPOSURE_TYPE, construct.Enum(Int8ub, params.ExposureMode)
        )
        """Liveview Exposure Select Mode."""

        self.exposure_x: Status = Status(self.communicator, StatusId.EXPOSURE_X, Int8ub)
        """Liveview Exposure Select: y-coordinate (percent)."""

        self.exposure_y: Status = Status(self.communicator, StatusId.EXPOSURE_Y, Int8ub)
        """Liveview Exposure Select: y-coordinate (percent)."""

        self.gps_stat: Status = Status(self.communicator, StatusId.GPS_STAT, Flag)  # type: ignore
        """Does the camera currently have a GPS lock?"""

        self.ap_state: Status = Status(self.communicator, StatusId.AP_STATE, Flag)  # type: ignore
        """Is the WiFi radio enabled?"""

        self.int_batt_per: Status = Status(self.communicator, StatusId.INT_BATT_PER, Int8ub)
        """Internal battery level (percent)."""

        self.acc_mic_stat: Status = Status(
            self.communicator, StatusId.ACC_MIC_STAT, construct.Enum(Int8ub, params.ExposureMode)
        )
        """Microphone Accesstory status."""

        self.digital_zoom: Status = Status(self.communicator, StatusId.DIGITAL_ZOOM, Int8ub)
        """	Digital Zoom level (percent)."""

        self.wireless_band: Status = Status(
            self.communicator, StatusId.WIRELESS_BAND, construct.Enum(Int8ub, params.WiFiBand)
        )
        """Wireless Band."""

        self.dig_zoom_active: Status = Status(self.communicator, StatusId.DIG_ZOOM_ACTIVE, Flag)  # type: ignore
        """Is Digital Zoom feature available?"""

        self.mobile_video: Status = Status(self.communicator, StatusId.MOBILE_VIDEO, Flag)  # type: ignore
        """Are current video settings mobile friendly? (related to video compression and frame rate)."""

        self.first_time: Status = Status(self.communicator, StatusId.FIRST_TIME, Flag)  # type: ignore
        """Is the camera currently in First Time Use (FTU) UI flow?"""

        self.sec_sd_stat: Status = Status(
            self.communicator, StatusId.SEC_SD_STAT, construct.Enum(Int8ub, params.SDStatus)
        )
        """Secondary Storage Status (exclusive to Superbank)."""

        self.band_5ghz_avail: Status = Status(self.communicator, StatusId.BAND_5GHZ_AVAIL, Flag)  # type: ignore
        """Is 5GHz wireless band available?"""

        self.system_ready: Status = Status(self.communicator, StatusId.SYSTEM_READY, Flag)  # type: ignore
        """Is the system ready to accept commands?"""

        self.batt_ok_ota: Status = Status(self.communicator, StatusId.BATT_OK_OTA, Flag)  # type: ignore
        """Is the internal battery charged sufficiently to start Over The Air (OTA) update?"""

        self.video_low_temp: Status = Status(self.communicator, StatusId.VIDEO_LOW_TEMP, Flag)  # type: ignore
        """Is the camera getting too cold to continue recording?"""

        self.orientation: Status = Status(
            self.communicator, StatusId.ORIENTATION, construct.Enum(Int8ub, params.Orientation)
        )
        """The rotational orientation of the camera."""

        self.thermal_mit_mode: Status = Status(self.communicator, StatusId.THERMAL_MIT_MODE, Flag)  # type: ignore
        """Can camera use high resolution/fps (based on temperature)?"""

        self.zoom_encoding: Status = Status(self.communicator, StatusId.ZOOM_ENCODING, Flag)  # type: ignore
        """Is this camera capable of zooming while encoding (static value based on model, not settings)?"""

        self.flatmode_id: Status = Status(
            self.communicator, StatusId.FLATMODE_ID, construct.Enum(Int8ub, params.Flatmode)
        )
        """Current flatmode ID."""

        self.logs_ready: Status = Status(self.communicator, StatusId.LOGS_READY, Flag)  # type: ignore
        """	Are system logs ready to be downloaded?"""

        self.timewarp_1x_active: Status = Status(self.communicator, StatusId.TIMEWARP_1X_ACTIVE, Flag)  # type: ignore
        """Is Timewarp 1x active?"""

        self.video_presets: Status = Status(self.communicator, StatusId.VIDEO_PRESETS, Int32ub)
        """Current Video Preset (ID)."""

        self.photo_presets: Status = Status(self.communicator, StatusId.PHOTO_PRESETS, Int32ub)
        """Current Photo Preset (ID)."""

        self.timelapse_presets: Status = Status(self.communicator, StatusId.TIMELAPSE_PRESETS, Int32ub)
        """	Current Timelapse Preset (ID)."""

        self.presets_group: Status = Status(self.communicator, StatusId.PRESETS_GROUP, Int32ub)
        """Current Preset Group (ID)."""

        self.active_preset: Status = Status(self.communicator, StatusId.ACTIVE_PRESET, Int32ub)
        """Currently Preset (ID)."""

        self.preset_modified: Status = Status(self.communicator, StatusId.PRESET_MODIFIED, Int32ub)
        """Preset Modified Status, which contains an event ID and a preset (group) ID."""

        self.live_burst_rem: Status = Status(self.communicator, StatusId.LIVE_BURST_REM, Int32ub)
        """How many Live Bursts can be captured before sdcard is full?"""

        self.live_burst_total: Status = Status(self.communicator, StatusId.LIVE_BURST_TOTAL, Int32ub)
        """Total number of Live Bursts on sdcard."""

        self.capt_delay_active: Status = Status(self.communicator, StatusId.CAPT_DELAY_ACTIVE, Flag)  # type: ignore
        """Is Capture Delay currently active (i.e. counting down)?"""

        self.media_mod_mic_stat: Status = Status(
            self.communicator, StatusId.MEDIA_MOD_MIC_STAT, construct.Enum(Int8ub, params.MediaModMicStatus)
        )
        """Media mod State."""

        self.timewarp_speed_ramp: Status = Status(
            self.communicator, StatusId.TIMEWARP_SPEED_RAMP, construct.Enum(Int8ub, params.TimeWarpSpeed)
        )
        """Time Warp Speed."""

        self.linux_core_active: Status = Status(self.communicator, StatusId.LINUX_CORE_ACTIVE, Flag)  # type: ignore
        """Is the system's Linux core active?"""

        self.camera_lens_type: Status = Status(
            self.communicator, StatusId.CAMERA_LENS_TYPE, construct.Enum(Int8ub, params.MaxLensMode)
        )
        """Camera lens type (reflects changes to setting 162)."""

        self.video_hindsight: Status = Status(self.communicator, StatusId.VIDEO_HINDSIGHT, Flag)  # type: ignore
        """Is Video Hindsight Capture Active?"""

        self.scheduled_preset: Status = Status(self.communicator, StatusId.SCHEDULED_PRESET, Int32ub)
        """Scheduled Capture Preset ID."""

        self.scheduled_capture: Status = Status(self.communicator, StatusId.SCHEDULED_CAPTURE, Flag)  # type: ignore
        """Is Scheduled Capture set?"""

        self.creating_preset: Status = Status(self.communicator, StatusId.CREATING_PRESET, Flag)  # type: ignore
        """Is the camera in the process of creating a custom preset?"""

        self.media_mod_stat: Status = Status(
            self.communicator, StatusId.MEDIA_MOD_STAT, construct.Enum(Int8ub, params.MediaModStatus)
        )
        """Media Mode Status (bitmasked)."""

        self.turbo_mode: Status = Status(self.communicator, StatusId.TURBO_MODE, Flag)  # type: ignore
        """Is Turbo Transfer active?"""
