# builders.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Common functionality across API versions to build commands, settings, and statuses"""

from __future__ import annotations
import enum
import types
import logging
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import (
    Any,
    ClassVar,
    TypeVar,
    Generic,
    Type,
    Union,
    no_type_check,
    Optional,
    Dict,
    Callable,
    Tuple,
    List,
    Set,
)
from _collections_abc import Iterable

import wrapt
import betterproto
from construct import Int8ub, Int16ub, Struct, Adapter, GreedyBytes

from open_gopro.responses import (
    BytesParser,
    BytesBuilder,
    BytesParserBuilder,
    JsonParser,
    GoProResp,
    StringBuilder,
)
from open_gopro.constants import (
    ActionId,
    FeatureId,
    BleUUID,
    CmdId,
    ResponseType,
    SettingId,
    QueryCmdId,
    StatusId,
    ErrorCode,
    GoProUUIDs,
)
from open_gopro.communication_client import GoProBle, GoProWifi
from open_gopro.util import build_log_rx_str, build_log_tx_str, custom_betterproto_to_dict

logger = logging.getLogger(__name__)

SettingValueType = TypeVar("SettingValueType")
CommandValueType = TypeVar("CommandValueType")

####################################################### General ##############################################


@wrapt.decorator
def log_query(
    wrapped: Callable, instance: Union[BleSetting, BleStatus, WifiSetting], args: Any, kwargs: Any
) -> GoProResp:
    """Log a query write

    Args:
        wrapped (Callable): query to log
        instance (Union[BleSetting, BleStatus, WifiSetting]): status / setting that owns the write
        args (Any): positional args
        kwargs (Any): keyword args

    Returns:
        GoProResp: received response from write
    """
    logger.info(build_log_tx_str(f"{wrapped.__name__} : {instance.identifier}"))
    response = wrapped(*args, **kwargs)
    logger.info(build_log_rx_str(response))
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
                _ (Any): Not used

            Returns:
                enum.Enum: Enum value
            """
            return self.target(obj)

        def _encode(self, obj: Union[enum.Enum, int], *_: Any) -> int:
            """Adapt an enum for use by Construct

            Args:
                obj (Union[enum.Enum, int]): Enum to adapt
                _ (Any): Not used

            Returns:
                int: int value of Enum
            """
            return obj if isinstance(obj, int) else obj.value

    setattr(EnumByteAdapter, "target", target)
    return EnumByteAdapter(Int8ub)


status_struct = Struct("status" / build_enum_adapter(ErrorCode))


class DeprecatedAdapter(Adapter):
    """Used to return "DEPRECATED" when a deprecated setting / status is attempted to be parsed / built"""

    def _decode(self, *_: Any) -> str:
        """Return "DEPRECATED" when parse() is called

        Args:
            _ (Any): Not used

        Returns:
            str: "DEPRECATED"
        """
        return "DEPRECATED"

    def _encode(self, *_: Any) -> str:
        """Return "DEPRECATED" when parse() is called

        Args:
            _ (Any): Not used

        Returns:
            str: "DEPRECATED"
        """
        return self._decode()


class DateTimeAdapter(Adapter):
    """Translate between different date time representations"""

    def _decode(self, obj: Union[List, str], *_: Any) -> datetime:
        """Translate string or list of bytes into datetime

        Args:
            obj (list): input
            _ (Any): Not used

        Raises:
            TypeError: Unsupported input type

        Returns:
            datetime: built datetime
        """
        if isinstance(obj, str):
            # comes as '%14%01%02%03%09%2F'
            year, *remaining = [int(x, 16) for x in obj.split("%")[1:]]
            return datetime(year + 2000, *remaining)  # type: ignore
        if isinstance(obj, list):
            # When received from BLE, it includes garbage first byte
            obj = obj[-7:]
            year = Int16ub.parse(bytes(obj[0:2]))
            return datetime(year, *[int(x) for x in obj[2:]])  # type: ignore
        raise TypeError("Type must be in (str, list)")

    def _encode(self, obj: Union[datetime, str], *_: Any) -> Union[bytes, str]:
        """Translate datetime into bytes or pass through string

        Args:
            obj (Union[datetime, str]): Input
            _ (Any): Not used

        Raises:
            TypeError: Unsupported input type

        Returns:
            Union[bytes, str]: built bytes
        """
        if isinstance(obj, datetime):
            year = [int(x) for x in Int16ub.build(obj.year)]
            return bytes([*year, obj.month, obj.day, obj.hour, obj.minute, obj.second])
        if isinstance(obj, str):
            return obj
        raise TypeError("Type must be in (datetime, str)")


# Ignoring because hitting this mypy bug: https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class BleCommand(ABC):
    """The base class for all BLE commands to store common info

    Args:
        communicator (GoProBle): BLE client to read / write
        uuid (BleUUID): BleUUID to read / write to
    """

    communicator: GoProBle
    uuid: BleUUID

    def __post_init__(self) -> None:
        self.communicator._add_parser(self._identifier, self._response_parser)

    @property
    @abstractmethod
    def _identifier(self) -> ResponseType:
        """The most accurate identifier for this command."""
        raise NotImplementedError

    @property
    @abstractmethod
    def _response_parser(self) -> BytesParser:
        """Get the response parser associated with this command."""
        raise NotImplementedError


@dataclass
class BleReadCommand(BleCommand):
    """A BLE command that reads data from a BleUUID

    Args:
        communicator (GoProBle): BLE client to read
        uuid (BleUUID): BleUUID to read to
        response_parser (BytesParser): the parser that will parse the received bytestream into a JSON dict
    """

    response_parser: BytesParser

    @property
    def _identifier(self) -> ResponseType:
        return self.uuid

    @property
    def _response_parser(self) -> BytesParser:
        return self.response_parser

    def __call__(self) -> GoProResp:  # noqa: D102
        logger.info(build_log_tx_str(self.uuid.name))
        response = self.communicator._read_characteristic(self.uuid)
        logger.info(build_log_rx_str(f"{self.uuid.name} : {response}"))
        return response


@dataclass
class BleWriteNoParamsCommand(BleCommand):
    """A BLE command that writes to a BleUUID and does not accept any parameters

    Args:
        communicator (GoProBle): BLE client to write
        uuid (BleUUID): BleUUID to write to
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

    def __call__(self) -> GoProResp:  # noqa: D102
        logger.info(build_log_tx_str(self.cmd.name))
        # Build data buffer
        data = bytearray([self.cmd.value])
        data.insert(0, len(data))
        # Send the data and receive the response
        response = self.communicator._write_characteristic_receive_notification(self.uuid, data)
        logger.info(build_log_rx_str(response))
        return response


@dataclass
class BleWriteWithParamsCommand(BleCommand, Generic[CommandValueType]):
    """A BLE command that writes to a BleUUID and does not accept any parameters

    Args:
        communicator (GoProBle): BLE client to write
        uuid (BleUUID): BleUUID to write to
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

    def __call__(self, value: CommandValueType) -> GoProResp:  # noqa: D102
        logger.info(build_log_tx_str(f"{self.cmd.name}: {str(value)}"))
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
        logger.info(build_log_rx_str(response))
        return response


@dataclass
class RegisterUnregisterAll(BleWriteNoParamsCommand):
    """Base class for register / unregister all commands

    This will loop over all of the elements (i.e. settings / statusess found from the element_set entry of the
    producer tuple parameter) and individually register / unregister (depending on the action parameter) each
    element in the set

    Args:
        producer: (Optional[Tuple[Union[Type[SettingId], Type[StatusId]], QueryCmdId]]): Tuple of (element_set,
            query command) where element_set is the GoProEnum that this command relates to, i.e. SettingId for
            settings, StatusId for Statuses
        action: (Optional[Action]): whether to register or unregister
    """

    class Action(enum.Enum):
        """Enum to differentiate between register actions"""

        REGISTER = enum.auto()
        UNREGISTER = enum.auto()

    producer: Optional[Tuple[Union[Type[SettingId], Type[StatusId]], QueryCmdId]] = None
    action: Optional[Action] = None

    def __post_init__(self) -> None:
        # TODO refactor to not use dataclasses since derived classes can't have non default members if base classes do
        assert self.producer is not None
        assert self.action is not None

    def __call__(self) -> GoProResp:  # noqa: D102
        assert self.producer is not None
        assert self.action is not None
        element_set = self.producer[0]
        responded_command = self.producer[1]
        response = super().__call__()
        if response.is_ok:
            for element in element_set:
                (
                    self.communicator._register_listener
                    if self.action is RegisterUnregisterAll.Action.REGISTER
                    else self.communicator._unregister_listener
                )(
                    # Ignoring typing because this seems correct and looks like mypy error
                    (responded_command, element)  # type: ignore
                )

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

        protobuf: Type[betterproto.Message]  # TODO use instance instead of class

        def _decode(self, obj: bytearray, *_: Any) -> Dict[Any, Any]:
            """Parse a byte stream into a JSON dict using a protobuf

            Args:
                obj (bytearray): byte stream to parse
                _ (Any): Not used

            Returns:
                Dict[Any, Any]: parsed JSON dict
            """
            response: betterproto.Message = self.protobuf().FromString(bytes(obj))
            response.to_dict = types.MethodType(custom_betterproto_to_dict, response)  # type: ignore
            return response.to_dict()  # type: ignore

        def _encode(self, *_: Any) -> Any:
            raise NotImplementedError

    setattr(ProtobufConstructAdapter, "protobuf", protobuf)
    return ProtobufConstructAdapter(GreedyBytes)


# Ignoring because hitting this mypy bug: https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class BleProtoCommand(BleCommand):
    """A BLE command that is sent and received as using the Protobuf protocol

    Args:
        communicator (GoProBle): BLE client to write
        uuid (BleUUID): BleUUID to write to
        feature_id (CmdId): Command ID that is being sent
        action_id (FeatureId): protobuf specific action ID that is being sent
        request_proto (Type[betterproto.Message]): protobuf used to build command bytestream
        response_proto (Type[betterproto.Message]): protobuf used to parse received bytestream
        additional_matching_action_ids: (Optional[Set[ActionId]]): Other action ID's to share
            this parser. Defaults to None.
    """

    feature_id: FeatureId
    action_id: ActionId
    request_proto: Type[betterproto.Message]
    response_proto: Type[betterproto.Message]
    additional_matching_action_ids: Optional[Set[ActionId]] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.additional_matching_action_ids:
            for action_id in self.additional_matching_action_ids:
                self.communicator._add_parser(action_id, self._response_parser)

    @property
    def _identifier(self) -> ResponseType:
        return self.action_id

    @property
    def _response_parser(self) -> BytesParser:
        return build_protobuf_adapter(self.response_proto)

    @abstractmethod
    @no_type_check
    def __call__(self, *args: Any, **kwargs: Any) -> GoProResp:  # noqa: D102
        # The method that will actually build and send the protobuf command

        # This method's signature shall be overridden by the subclass.
        # The subclass shall then pass the arguments to this method and return it's returned response

        # This pattern is technically violating the Liskov substitution principle. But we are accepting this as a
        # tradeoff for exposing type hints on BLE Protobuf commands.
        logger.info(
            build_log_tx_str(
                f"{self.action_id.name} : {' '.join([*[str(a) for a in args], *[str(a) for a in kwargs.values()]])}"
            )
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
        logger.info(build_log_rx_str(response))
        return response


class BleSetting(Generic[SettingValueType]):
    """An individual camera setting that is interacted with via BLE."""

    def __init__(
        self, communicator: GoProBle, identifier: SettingId, parser_builder: BytesParserBuilder
    ) -> None:
        """Constructor

        Args:
            communicator (GoProBle): Adapter to read / write settings data
            identifier (SettingId): ID of setting
            parser_builder (BytesParserBuilder): object to both parse and build setting
        """
        self.identifier = identifier
        self.communicator: GoProBle = communicator
        self.setter_uuid: BleUUID = GoProUUIDs.CQ_SETTINGS
        self.reader_uuid: BleUUID = GoProUUIDs.CQ_QUERY
        self.parser: BytesParser = parser_builder
        self.builder: BytesBuilder = parser_builder  # Just syntactic sugar
        communicator._add_parser(self.identifier, self.parser)

    def __str__(self) -> str:
        return str(self.identifier.name)

    def set(self, value: SettingValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (SettingValueType): The argument to use to set the setting value.

        Returns:
            GoProResp: Status of set
        """
        logger.info(build_log_tx_str(f"Set {self.identifier.name}: {str(value)}"))

        data = bytearray([self.identifier.value])
        try:
            param = self.builder.build(value)
            data.extend([len(param), *param])
        except IndexError:
            pass
        data.insert(0, len(data))
        response = self.communicator._write_characteristic_receive_notification(self.setter_uuid, data)

        logger.info(build_log_rx_str(response))
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
    """An individual camera status that is interacted with via BLE."""

    uuid: BleUUID = GoProUUIDs.CQ_QUERY

    def __init__(self, communicator: GoProBle, identifier: StatusId, parser: BytesParser) -> None:
        """Constructor

        Args:
            communicator (GoProBle): Adapter to read status data
            identifier (StatusId): ID of status
            parser (BytesParser): parser used to build response
        """
        self.identifier = identifier
        self.communicator = communicator
        # Add to response parsing map
        communicator._add_parser(self.identifier, parser)

    def __str__(self) -> str:
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
        if (
            response := self.communicator._write_characteristic_receive_notification(
                BleStatus.uuid, self._build_cmd(QueryCmdId.REG_STATUS_VAL_UPDATE)
            )
        ).is_ok:
            self.communicator._register_listener((QueryCmdId.STATUS_VAL_PUSH, self.identifier))
        return response

    @log_query
    def unregister_value_update(self) -> GoProResp:
        """Stop receiving notifications when status changes.

        Returns:
            GoProResp: Status of unregister
        """
        if (
            response := self.communicator._write_characteristic_receive_notification(
                BleStatus.uuid, self._build_cmd(QueryCmdId.UNREG_STATUS_VAL_UPDATE)
            )
        ).is_ok:
            self.communicator._unregister_listener((QueryCmdId.STATUS_VAL_PUSH, self.identifier))
        return response

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
    """A Wifi command that writes to a BleUUID (with parameters) and receives JSON as response

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
        response_parser (Optional[JsonParser]): the parser that will parse the received bytestream into a JSON dict
    """

    communicator: GoProWifi
    endpoint: str
    response_parser: Optional[JsonParser] = None
    param_builder: Optional[StringBuilder] = None

    def __call__(self, value: CommandValueType) -> GoProResp:  # noqa: D102
        values: List[CommandValueType] = [*value] if isinstance(value, Iterable) else [value]
        logger.info(build_log_tx_str(f"{self.endpoint.format(*values)}"))

        # Build list of args as they should be represented in URL
        url_params = []
        if self.param_builder is not None:
            url_params.append(self.param_builder(value))
        elif issubclass(type(value), enum.Enum):
            url_params.append(value.value)  # type: ignore
        else:
            url_params.extend(values)  # type: ignore
        url = self.endpoint.format(*url_params)
        # Send to camera
        response = self.communicator._get(url)
        logger.info(build_log_rx_str(response))
        return response


@dataclass
class WifiGetJsonNoParams(WifiGetJsonCommand):
    """A Wifi command that writes to a BleUUID (with parameters) and receives JSON as response

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
        response_parser (Optional[JsonParser]): the parser that will parse the received bytestream into a JSON dict
    """

    def __call__(self) -> GoProResp:  # noqa: D102
        logger.info(build_log_tx_str(self.endpoint))
        url = self.endpoint
        # Send to camera
        response = self.communicator._get(url)
        logger.info(build_log_rx_str(response))
        return response


# Ignoring because hitting this mypy bug: https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class WifiGetBinary(ABC):
    """A Wifi command that writes to a BleUUID (with parameters) and receives a binary stream as response

    Args:
        communicator (GoProWifi): Wifi client to write command
        endpoint (str): endpoint to GET
    """

    communicator: GoProWifi
    endpoint: str

    @abstractmethod
    @no_type_check
    def __call__(self, /, **kwargs) -> Path:  # noqa: D102
        # The method that will actually send the command and receive the stream
        # This method's signature shall be override by the subclass.
        # The subclass shall then pass the arguments to this method and return it's returned response
        # This pattern is technically violating the Liskov substitution principle. But we are accepting this as a
        # tradeoff for exposing type hints on commands.
        camera_file = kwargs["camera_file"]
        local_file = Path(kwargs["local_file"]) if "local_file" in kwargs else Path(".") / camera_file
        logger.info(build_log_tx_str(f"{self.endpoint.format(camera_file)} ===> {local_file}"))

        url = self.endpoint.format(camera_file)
        # Send to camera
        self.communicator._stream_to_file(url, local_file)
        logger.info(build_log_rx_str("SUCCESS"))
        return local_file


class WifiSetting(Generic[SettingValueType]):
    """An individual camera setting that is interacted with via Wifi."""

    def __init__(self, communicator: GoProWifi, identifier: SettingId) -> None:
        """Constructor

        Args:
            communicator (GoProWifi): Adapter to read / write settings data
            identifier (SettingId): ID of setting
        """
        self.identifier = identifier
        self.communicator = communicator
        # Note! It is assumed that BLE and WiFi settings are symmetric so we only add to the communicator's
        # parser in the BLE Setting.

    def __str__(self) -> str:
        return str(self.identifier.name)

    def set(self, value: SettingValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (SettingValueType): value to set setting

        Returns:
            GoProResp: Status of set
        """
        logger.info(build_log_tx_str(f"Setting {self.identifier}: {value}"))
        # Build url. TODO fix this type error with Mixin (or passing in endpoint as argument)
        value = value.value if isinstance(value, enum.Enum) else value
        url = self.communicator._api.wifi_setting.endpoint.format(self.identifier.value, value)  # type: ignore
        # Send to camera
        response = self.communicator._get(url)
        if response is not None:
            logger.info(f"-----------> \n{response}")
        return response
