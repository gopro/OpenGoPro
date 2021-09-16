# builders.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Common functionality across API versions to build commands, settings, and statuses"""

from __future__ import annotations
import enum
import logging
from pathlib import Path
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, TYPE_CHECKING, Type, Union, no_type_check, Optional

import wrapt
import requests
import construct  # For enum
import betterproto
from construct import Int8ub, Struct

from open_gopro.responses import (
    ProtobufResponseAdapter,
    BytesParser,
    BytesBuilder,
    BytesParserBuilder,
    JsonParser,
    GoProResp,
)
from open_gopro.constants import ActionId, UUID, CmdId, SettingId, QueryCmdId, StatusId, ErrorCode
from open_gopro.communication_client import GoProBle, GoProWifi

if TYPE_CHECKING:
    from . import Params

logger = logging.getLogger(__name__)

SettingValueType = TypeVar("SettingValueType", bound=Union[enum.Enum, bool, int, str])
CommandValueType = TypeVar("CommandValueType", bound=Union[enum.Enum, bool, int, str])

####################################################### Genearl##############################################


@wrapt.decorator
# pylint: disable = E, W
def log_query(wrapped, instance, args, kwargs):  # type: ignore
    """Log a query write."""
    logger.info(f"<----------- {wrapped.__name__} : {instance.identifier}")
    response = wrapped(*args, **kwargs)
    logger.info(f"-----------> {response}")
    return response


######################################################## BLE #################################################

status_struct = Struct("status" / construct.Enum(Int8ub, ErrorCode))


@dataclass
class BleCommand:
    """The base class for all BLE commands to store common info

    Args:
        communicator (GoProBle): BLE client to read / write
        uuid (UUID): UUID to read / write to
    """

    communicator: GoProBle
    uuid: UUID


@dataclass
class BleReadCommand(BleCommand):
    """A BLE command that reads data from a UUID

    Args:
        communicator (GoProBle): BLE client to read
        uuid (UUID): UUID to read to
        response_parser (BytesParser): the parser that will parse the received bytestream into a JSON dict
    """

    communicator: GoProBle
    uuid: UUID
    response_parser: BytesParser

    def __call__(self) -> GoProResp:
        """The method that will actually build and send the command.

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.uuid.name}")
        self.communicator._add_parser(self.uuid, self.response_parser)
        response = self.communicator._read_characteristic(self.uuid)
        logger.info(f"-----------> {self.uuid.name} : {response}")
        return response


@dataclass
class BleWriteNoParamsCommand(BleCommand):
    """A BLE command that writes to a UUID and does not accept any parameters

    Args:
        communicator (GoProBle): BLE client to write
        uuid (UUID): UUID to write to
        cmd (CmdId): Command ID that is being sent
        response_parser (BytesParser): the parser that will parse the received bytestream into a JSON dict
    """

    communicator: GoProBle
    uuid: UUID
    cmd: CmdId
    response_parser: Optional[BytesParser] = None

    def __call__(self) -> GoProResp:
        """The method that will actually build and send the command

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.cmd.name}")
        # Append optional additional response parser to status parser
        self.communicator._add_parser(
            identifier=self.cmd,
            parser=status_struct if self.response_parser is None else status_struct + self.response_parser,
        )
        # Build data buffer
        data = bytearray([self.cmd.value])
        data.insert(0, len(data))
        # Send the data and receive the response
        response = self.communicator._write_characteristic_receive_notification(self.uuid, data)
        logger.info(f"-----------> \n{response}")
        return response


@dataclass
class BleWriteWithParamsCommand(BleCommand, Generic[CommandValueType]):
    """A BLE command that writes to a UUID and does not accept any parameters

    Args:
        communicator (GoProBle): BLE client to write
        uuid (UUID): UUID to write to
        cmd (CmdId): Command ID that is being sent
        param_builder (BytesBuilder): is responsible for building the bytestream to send from the input params
        response_parser (Optional[BytesParser]): the parser that will parse the received bytestream into a JSON dict
    """

    communicator: GoProBle
    uuid: UUID
    cmd: CmdId
    param_builder: BytesBuilder
    response_parser: Optional[BytesParser] = None

    def __call__(self, value: CommandValueType) -> GoProResp:
        """The method that will actually build and send the command

        When this class is subclassed, the CommandValueType will be taken from the generic definition

        Args:
            value (CommandValueType): Value to send

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.cmd.name}: {str(value)}")
        # Append optional additional response parser to status parser
        self.communicator._add_parser(
            identifier=self.cmd,
            parser=status_struct if self.response_parser is None else status_struct + self.response_parser,
        )
        # Build data buffer
        data = bytearray([self.cmd.value])
        param = value.value if issubclass(type(value), enum.Enum) else value
        # There must be a param builder if we have a param
        param = self.param_builder.build(param)
        data.extend([len(param), *param])
        data.insert(0, len(data))
        # Send the data and receive the response
        response = self.communicator._write_characteristic_receive_notification(self.uuid, data)
        logger.info(f"-----------> \n{response}")
        return response


# Ignoring because hitting this mypy bug: https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class BleProtoCommand(BleCommand, ABC):
    """A BLE command that writes to a UUID and does not accept any parameters

    Args:
        communicator (GoProBle): BLE client to write
        uuid (UUID): UUID to write to
        feature_id (CmdId): Command ID that is being sent
        action_id (ActionId): protobuf specific action ID that is being sent
        request_proto (Type[betterproto.Message]): protobuf used to build command bytestream
        response_proto (Type[betterproto.Message]): protobuf used to parse received bytestream
    """

    communicator: GoProBle
    uuid: UUID
    feature_id: CmdId
    action_id: ActionId
    request_proto: Type[betterproto.Message]
    response_proto: Type[betterproto.Message]

    @abstractmethod
    @no_type_check
    def __call__(self, *args: Any, **kwargs: Any) -> GoProResp:
        """The method that will actually build and send the protobuf command

        This method's signature shall be override by the subclass.
        The subclass shall then pass the arguments to this method and return it's returned response

        This pattern is technically violating the Liskov substitution principle. But we are accepting this as a
        tradeoff for exposing type hints on BLE Protobuf commands.

        Returns:
            GoProResp: the received and parsed response
        """
        logger.info(
            f"<----------- {self.feature_id.name} : {' '.join([*[str(a) for a in args], *[str(a) for a in kwargs.values()]])}"
        )

        if self.response_proto is not None:
            self.communicator._add_parser(self.action_id, ProtobufResponseAdapter(self.response_proto))

        # Build request protobuf bytestream
        proto = self.request_proto()
        # Add args to protobuf request
        attrs = iter(self.__call__.__annotations__.keys())
        for arg in args:
            param = arg.value if issubclass(type(arg), enum.Enum) else arg
            setattr(proto, next(attrs), param)
        # Add kwargs to protobuf request
        for name, arg in kwargs.items():
            if arg is not None:
                param = arg.value if issubclass(type(arg), enum.Enum) else arg
                setattr(proto, name, param)

        # Prepend headers and serialize
        request = bytearray([self.feature_id.value, self.action_id.value, *proto.SerializeToString()])
        # Prepend length
        request.insert(0, len(request))

        # Allow exception to pass through if protobuf not completely initialized
        response = self.communicator._write_characteristic_receive_notification(self.uuid, request)
        logger.info(f"-----------> \n{response}")
        return response


class BleSetting(Generic[SettingValueType]):
    """An individual camera setting that is interacted with via BLE.

    Args:
        communicator (GoProBle): Adapter to read / write settings data
        identifier (SettingId): ID of setting
        parser_builder (BytesParserBuilder): object to both parse and build setting
    """

    def __init__(
        self, communicator: GoProBle, identifier: SettingId, parser_builder: BytesParserBuilder
    ) -> None:
        self.identifier = identifier
        self.communicator: GoProBle = communicator
        self.setter_uuid: UUID = UUID.CQ_SETTINGS
        self.reader_uuid: UUID = UUID.CQ_QUERY
        self.parser: BytesParser = parser_builder
        self.builder: BytesBuilder = parser_builder  # Just syntactic sugar
        communicator._add_parser(self.identifier, self.parser)

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return str(self.identifier.name)

    def set(self, value: SettingValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (Any): The argument to use to set the setting value.

        Returns:
            GoProResp: Status of set
        """
        logger.info(f"<----------- Set {self.identifier.name}: {str(value)}")

        data = bytearray([self.identifier.value])
        try:
            param = self.builder.build(value)
            data.extend([len(param), *param])
        except IndexError:
            pass
        data.insert(0, len(data))
        response = self.communicator._write_characteristic_receive_notification(self.setter_uuid, data)

        logger.info(f"-----------> \n{response}")
        return response

    @log_query
    def get_value(self) -> GoProResp:
        """Get the settings value.

        Returns:
            GoProResp: settings value
        """
        return self.communicator._write_characteristic_receive_notification(
            self.reader_uuid, self._build_cmd(QueryCmdId.GET_SETTING_VAL)
        )

    @log_query
    def get_name(self) -> GoProResp:
        """Get the settings name.

        Raises:
            NotImplementedError: This isn't implemented on the camera

        Returns:
            GoProResp: settings name
        """
        # return self.communicator._write_characteristic_receive_notification(
        #     self.reader_uuid, QueryCmdId.GET_SETTING_NAME, self._build_cmd(QueryCmdId.GET_SETTING_NAME)
        # )
        raise NotImplementedError("Not implemented on camera!")

    @log_query
    def get_capabilities_values(self) -> GoProResp:
        """Get currently supported settings capabilities values.

        Returns:
            GoProResp: settings capabilities values
        """
        return self.communicator._write_characteristic_receive_notification(
            self.reader_uuid, self._build_cmd(QueryCmdId.GET_CAPABILITIES_VAL)
        )

    @log_query
    def get_capabilities_names(self) -> GoProResp:
        """Get currently supported settings capabilities names.

        Raises:
            NotImplementedError: This isn't implemented on the camera

        Returns:
            GoProResp: settings capabilities names
        """
        # return self.communicator._write_characteristic_receive_notification(
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
        self.communicator._register_listener((QueryCmdId.SETTING_VAL_PUSH, self.identifier))
        return self.communicator._write_characteristic_receive_notification(
            self.reader_uuid, self._build_cmd(QueryCmdId.REG_SETTING_VAL_UPDATE)
        )

    @log_query
    def unregister_value_update(self) -> GoProResp:
        """Stop receiving notifications when a given setting ID's value updates.

        Returns:
            GoProResp: Status of unregister
        """
        self.communicator._unregister_listener((QueryCmdId.SETTING_VAL_PUSH, self.identifier))
        return self.communicator._write_characteristic_receive_notification(
            self.reader_uuid, self._build_cmd(QueryCmdId.UNREG_SETTING_VAL_UPDATE)
        )

    @log_query
    def register_capability_update(self) -> GoProResp:
        """Register for asynchronous notifications when a given setting ID's capabilities update.

        Returns:
            GoProResp: Current capabilities of respective setting ID
        """
        self.communicator._register_listener((QueryCmdId.SETTING_CAPABILITY_PUSH, self.identifier))
        return self.communicator._write_characteristic_receive_notification(
            self.reader_uuid, self._build_cmd(QueryCmdId.REG_CAPABILITIES_UPDATE)
        )

    @log_query
    def unregister_capability_update(self) -> GoProResp:
        """Stop receiving notifications when a given setting ID's capabilities change.

        Returns:
            GoProResp: Status of unregister
        """
        self.communicator._unregister_listener((QueryCmdId.SETTING_CAPABILITY_PUSH, self.identifier))
        return self.communicator._write_characteristic_receive_notification(
            self.reader_uuid, self._build_cmd(QueryCmdId.UNREG_CAPABILITIES_UPDATE)
        )

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data to send a settings query over-the-air.

        Args:
            cmd (QueryCmdId): command to build

        Returns:
            bytearray: data to send over-the-air
        """
        ret = bytearray([cmd.value, self.identifier.value])
        ret.insert(0, len(ret))
        return ret


class BleStatus:
    """An individual camera status that is interacted with via BLE.

    Args:
        communicator (GoProBle): Adapter to read status data
        identifier (StatusId): ID of status
    """

    uuid = UUID.CQ_QUERY

    def __init__(self, communicator: GoProBle, identifier: StatusId, parser: BytesParser) -> None:
        self.identifier = identifier
        self.communicator = communicator
        self.parser = parser
        # Add to response parsing map
        communicator._parser_map[self.identifier] = self.parser

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return str(self.identifier.name)

    @log_query
    def get_value(self) -> GoProResp:
        """Get the current value of a status.

        Returns:
            GoProResp: current status value
        """
        return self.communicator._write_characteristic_receive_notification(
            BleStatus.uuid, self._build_cmd(QueryCmdId.GET_STATUS_VAL)
        )

    @log_query
    def register_value_update(self) -> GoProResp:
        """Register for asynchronous notifications when a status changes.

        Returns:
            GoProResp: current status value
        """
        self.communicator._register_listener((QueryCmdId.STATUS_VAL_PUSH, self.identifier))
        return self.communicator._write_characteristic_receive_notification(
            BleStatus.uuid, self._build_cmd(QueryCmdId.REG_STATUS_VAL_UPDATE)
        )

    @log_query
    def unregister_value_update(self) -> GoProResp:
        """Stop receiving notifications when status changes.

        Returns:
            GoProResp: Status of unregister
        """
        self.communicator._unregister_listener((QueryCmdId.STATUS_VAL_PUSH, self.identifier))
        return self.communicator._write_characteristic_receive_notification(
            BleStatus.uuid, self._build_cmd(QueryCmdId.UNREG_STATUS_VAL_UPDATE)
        )

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data for a given status command.

        Args:
            cmd (QueryCmdId): command to build data for

        Returns:
            bytearray: data to send over-the-air
        """
        ret = bytearray([cmd.value, self.identifier.value])
        ret.insert(0, len(ret))
        return ret


######################################################## Wifi #################################################


@dataclass
class WifiCommand:
    """The base class for all WiFi Commands. Stores common information.

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
    """

    communicator: GoProWifi
    endpoint: str


@dataclass
class WifiGetJsonWithParams(WifiCommand, Generic[CommandValueType]):
    """A Wifi command that writes to a UUID (with parameters) and receives JSON as response

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
        response_parser (Optional[JsonParser]): the parser that will parse the received bytestream into a JSON dict
    """

    communicator: GoProWifi
    endpoint: str
    response_parser: Optional[JsonParser] = None

    def __call__(self, value: CommandValueType) -> GoProResp:
        """The method that will actually build and send the command

        When this class is subclassed, the CommandValueType will be taken from the generic definition

        Args:
            value (CommandValueType): Value to send

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.endpoint} : {str(value)}")

        if self.response_parser is not None:
            self.communicator._add_parser(self.endpoint, self.response_parser)

        # Build list of args as they should be represented in URL
        url_params = []
        if issubclass(type(value), enum.Enum):
            url_params.append(value.value)
        else:
            url_params.append(value)
        url = self.endpoint.format(*url_params)
        # Send to camera
        response = self.communicator._get(url)
        logger.info(f"-----------> \n{response}")
        return response


@dataclass
class WifiGetJsonNoParams(WifiCommand):
    """A Wifi command that writes to a UUID (with parameters) and receives JSON as response

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
        response_parser (Optional[JsonParser]): the parser that will parse the received bytestream into a JSON dict
    """

    communicator: GoProWifi
    endpoint: str
    response_parser: Optional[JsonParser] = None

    def __call__(self) -> GoProResp:
        """The method that will actually build and send the command

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.endpoint}")

        if self.response_parser is not None:
            self.communicator._add_parser(self.endpoint, self.response_parser)

        url = self.endpoint
        # Send to camera
        response = self.communicator._get(url)
        logger.info(f"-----------> \n{response}")
        return response


# Ignoring because hitting this mypy bug: https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class WifiGetBinary(WifiCommand, ABC):
    """A Wifi command that writes to a UUID (with parameters) and receives a binary stream as response

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
    """

    communicator: GoProWifi
    endpoint: str

    @abstractmethod
    @no_type_check
    def __call__(self, /, **kwargs) -> Path:
        """The method that will actually send the command and receive the stream

        This method's signature shall be override by the subclass.
        The subclass shall then pass the arguments to this method and return it's returned response

        This pattern is technically violating the Liskov substitution principle. But we are accepting this as a
        tradeoff for exposing type hints on BLE Protobuf commands.

        Returns:
            GoProResp: the received and parsed response
        """
        logger.info(f'<----------- {self.endpoint} : {" ".join([str(x) for x in list(kwargs.values())])}')
        camera_file = kwargs["camera_file"]
        try:
            local_file = Path(kwargs["local_file"])
        except KeyError:
            local_file = Path(".") / camera_file

        url = self.endpoint.format(camera_file)
        # Send to camera
        try:
            self.communicator._stream_to_file(url, local_file)
        except requests.exceptions.HTTPError as e:
            logger.error(repr(e))
        else:
            logger.info("-----------> SUCCESS")
        return local_file


class WifiSetting(Generic[SettingValueType]):
    """An individual camera setting that is interacted with via Wifi.

    Args:
        communicator (WifiCommunicator): Adapter to read / write settings data
        id (SettingId): ID of setting
        endpoint (str): HTTP endpoint to be used to set setting value
    """

    def __init__(self, communicator: GoProWifi, identifier: SettingId) -> None:
        self.identifier = identifier
        self.communicator = communicator

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return str(self.identifier.name)

    def set(self, value: SettingValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (Any): value to set setting

        Returns:
            GoProResp: Status of set
        """
        logger.info(f"<----------- Setting {self.identifier}: {value}")
        # Build url.. TODO fix this type error with Mixin (or passing in endpoint as argument)
        url = self.communicator._api.wifi_setting.endpoint.format(self.identifier.value, value)  # type: ignore
        # Send to camera
        response = self.communicator._get(url)
        if response is not None:
            logger.info(f"-----------> \n{response}")
        return response
