# builders.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Common functionality across API versions to build commands, settings, and statuses"""

from __future__ import annotations
import enum
import logging
from pathlib import Path
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import (
    Any,
    ClassVar,
    TypeVar,
    Generic,
    TYPE_CHECKING,
    Type,
    Union,
    no_type_check,
    Optional,
    Dict,
    Callable,
)

import wrapt
import requests
import betterproto
from construct import Int8ub, Struct, Adapter, GreedyBytes

from open_gopro.responses import (
    BytesParser,
    BytesBuilder,
    BytesParserBuilder,
    JsonParser,
    GoProResp,
)
from open_gopro.constants import (
    ActionId,
    UUID,
    CmdId,
    ResponseType,
    SettingId,
    QueryCmdId,
    StatusId,
    ErrorCode,
)
from open_gopro.communication_client import GoProBle, GoProWifi

if TYPE_CHECKING:
    from . import Params

logger = logging.getLogger(__name__)

SettingValueType = TypeVar("SettingValueType", bound=Union[enum.Enum, bool, int, str])
CommandValueType = TypeVar("CommandValueType", bound=Union[enum.Enum, bool, int, str])

####################################################### Genearl##############################################


@wrapt.decorator
# pylint: disable = E, W
def log_query(
    wrapped: Callable, instance: Union[BleSetting, BleStatus, WifiSetting], args: Any, kwargs: Any
) -> Callable:
    """Log a query write."""
    logger.info(f"<----------- {wrapped.__name__} : {instance.identifier}")
    response = wrapped(*args, **kwargs)
    logger.info(f"-----------> {response}")
    return response


######################################################## BLE #################################################


def build_enum_adapter(target: Type[enum.Enum]) -> Adapter:
    """Build an enum to Construct parsing and building adapter

    This adapter only works on byte data of length 1

    Args:
        target (Type[enum.Enum]): Enum to use use for parsing / building

    Returns:
        Adapter: adapter to be used by Construct
    """

    class EnumByteAdapter(Adapter):
        """An enum to Construct adapter"""

        target: ClassVar[Type[enum.Enum]]

        def _decode(self, obj: bytearray, *_: Any) -> enum.Enum:
            """Parse a bytestream of length 1 into an Enum

            Args:
                obj (bytearray): bytestream to parse

            Returns:
                enum.Enum: Enum value
            """
            return self.target(obj)

        def _encode(self, obj: Union[enum.Enum, int], *_: Any) -> int:
            """Adapt an enum for use by Construct

            Args:
                obj (Union[enum.Enum, int]): Enum to adapt

            Returns:
                int: int value of Enum
            """
            return obj if isinstance(obj, int) else obj.value

    setattr(EnumByteAdapter, "target", target)
    return EnumByteAdapter(Int8ub)


status_struct = Struct("status" / build_enum_adapter(ErrorCode))


# Ignoring because hitting this mypy bug: https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class BleCommand(ABC):
    """The base class for all BLE commands to store common info

    Args:
        communicator (GoProBle): BLE client to read / write
        uuid (UUID): UUID to read / write to
    """

    communicator: GoProBle
    uuid: UUID

    def __post_init__(self) -> None:
        self.communicator._add_parser(self._identifier, self._response_parser)

    @property
    @abstractmethod
    def _identifier(self) -> ResponseType:
        raise NotImplementedError

    @property
    @abstractmethod
    def _response_parser(self) -> BytesParser:
        raise NotImplementedError


@dataclass
class BleReadCommand(BleCommand):
    """A BLE command that reads data from a UUID

    Args:
        communicator (GoProBle): BLE client to read
        uuid (UUID): UUID to read to
        response_parser (BytesParser): the parser that will parse the received bytestream into a JSON dict
    """

    response_parser: BytesParser

    @property
    def _identifier(self) -> ResponseType:
        return self.uuid

    @property
    def _response_parser(self) -> BytesParser:
        return self.response_parser

    def __call__(self) -> GoProResp:
        """The method that will actually build and send the command.

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.uuid.name}")
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
        response_parser (Optional[ConstructBytesParser]): the parser that will parse the received bytestream into a JSON dict.
            Defaults to None
    """

    cmd: CmdId
    response_parser: Optional[BytesParser] = None

    @property
    def _identifier(self) -> ResponseType:
        return self.cmd

    @property
    def _response_parser(self) -> BytesParser:
        return status_struct if self.response_parser is None else status_struct + self.response_parser

    def __call__(self) -> GoProResp:
        """The method that will actually build and send the command

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.cmd.name}")
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

    cmd: CmdId
    param_builder: BytesBuilder
    response_parser: Optional[BytesParser] = None

    @property
    def _identifier(self) -> ResponseType:
        return self.cmd

    @property
    def _response_parser(self) -> BytesParser:
        return status_struct if self.response_parser is None else status_struct + self.response_parser

    def __call__(self, value: CommandValueType) -> GoProResp:
        """The method that will actually build and send the command

        When this class is subclassed, the CommandValueType will be taken from the generic definition

        Args:
            value (CommandValueType): Value to send

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.cmd.name}: {str(value)}")
        # Build data buffer
        data = bytearray([self.cmd.value])
        # Mypy is not understanding the subclass check here
        param = value.value if issubclass(type(value), enum.Enum) else value  # type: ignore
        # There must be a param builder if we have a param
        param = self.param_builder.build(param)
        data.extend([len(param), *param])
        data.insert(0, len(data))
        # Send the data and receive the response
        response = self.communicator._write_characteristic_receive_notification(self.uuid, data)
        logger.info(f"-----------> \n{response}")
        return response


def build_protobuf_adapter(protobuf: Type[betterproto.Message]) -> Adapter:
    """Build a protobuf to Construct parsing (only) adapter

    Args:
        protobuf (Type[betterproto.Message]): protobuf to use as parser

    Returns:
        Adapter: adapter to be used by Construct
    """

    class ProtobufConstructAdapter(Adapter):
        """Adapt a protobuf to be used by Construct (for parsing only)"""

        protobuf: Type[betterproto.Message]

        def _decode(self, obj: bytearray, *_: Any) -> Dict[Any, Any]:
            """Parse a byte stream into a JSON dict using a protobuf

            Args:
                obj (bytearray): byte stream to parse

            Returns:
                Dict[Any, Any]: parsed JSON dict
            """
            return self.protobuf.FromString(bytes(obj)).to_dict()

        def _encode(self, *_: Any) -> Any:
            raise NotImplementedError

    setattr(ProtobufConstructAdapter, "protobuf", protobuf)
    return ProtobufConstructAdapter(GreedyBytes)


# Ignoring because hitting this mypy bug: https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class BleProtoCommand(BleCommand):
    """A BLE command that writes to a UUID and does not accept any parameters

    Args:
        communicator (GoProBle): BLE client to write
        uuid (UUID): UUID to write to
        feature_id (CmdId): Command ID that is being sent
        action_id (ActionId): protobuf specific action ID that is being sent
        request_proto (Type[betterproto.Message]): protobuf used to build command bytestream
        response_proto (Type[betterproto.Message]): protobuf used to parse received bytestream
    """

    feature_id: CmdId
    action_id: ActionId
    request_proto: Type[betterproto.Message]
    response_proto: Type[betterproto.Message]

    @property
    def _identifier(self) -> ResponseType:
        return self.action_id

    @property
    def _response_parser(self) -> BytesParser:
        return (
            self.response_proto if self.response_proto is None else build_protobuf_adapter(self.response_proto)
        )

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
        communicator._add_parser(self.identifier, self.parser)

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
class WifiGetJsonCommand:
    """The base class for all WiFi Commands. Stores common information.

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
    """

    communicator: GoProWifi
    endpoint: str
    response_parser: Optional[JsonParser] = None

    def __post_init__(self) -> None:
        if self.response_parser is not None:
            self.communicator._add_parser(self.endpoint, self.response_parser)


@dataclass
class WifiGetJsonWithParams(WifiGetJsonCommand, Generic[CommandValueType]):
    """A Wifi command that writes to a UUID (with parameters) and receives JSON as response

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
        response_parser (Optional[JsonParser]): the parser that will parse the received bytestream into a JSON dict
    """

    def __call__(self, value: CommandValueType) -> GoProResp:
        """The method that will actually build and send the command

        When this class is subclassed, the CommandValueType will be taken from the generic definition

        Args:
            value (CommandValueType): Value to send

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.endpoint} : {str(value)}")

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
class WifiGetJsonNoParams(WifiGetJsonCommand):
    """A Wifi command that writes to a UUID (with parameters) and receives JSON as response

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
        response_parser (Optional[JsonParser]): the parser that will parse the received bytestream into a JSON dict
    """

    def __call__(self) -> GoProResp:
        """The method that will actually build and send the command

        Returns:
            GoProResp: received and parsed response
        """
        logger.info(f"<----------- {self.endpoint}")

        url = self.endpoint
        # Send to camera
        response = self.communicator._get(url)
        logger.info(f"-----------> \n{response}")
        return response


# Ignoring because hitting this mypy bug: https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class WifiGetBinary(ABC):
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
        # Build url. TODO fix this type error with Mixin (or passing in endpoint as argument)
        value = value.value if isinstance(value, enum.Enum) else value
        url = self.communicator._api.wifi_setting.endpoint.format(self.identifier.value, value)  # type: ignore
        # Send to camera
        response = self.communicator._get(url)
        if response is not None:
            logger.info(f"-----------> \n{response}")
        return response
