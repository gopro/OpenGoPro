# builders.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Common functionality across API versions to build commands, settings, and statuses"""

from __future__ import annotations
import enum
import logging
from pathlib import Path
from abc import abstractmethod
from dataclasses import dataclass
from urllib.parse import urlencode
from collections.abc import Iterable
from typing import Any, ClassVar, TypeVar, Generic, Union, no_type_check, Optional, Final

import google.protobuf.json_format
from google.protobuf import descriptor
from google.protobuf.message import Message as Protobuf
from google.protobuf.json_format import MessageToDict as ProtobufToDict
from construct import Adapter, GreedyBytes, Construct

from open_gopro.responses import BytesBuilder, BytesParser, GoProResp, JsonParser, BytesParserBuilder
from open_gopro.constants import (
    ActionId,
    FeatureId,
    BleUUID,
    CmdId,
    SettingId,
    QueryCmdId,
    StatusId,
    GoProUUIDs,
    enum_factory,
)
from open_gopro.interface import GoProBle, GoProWifi, BleCommand, WifiCommand
from open_gopro.util import Logger, jsonify

logger = logging.getLogger(__name__)

ValueType = TypeVar("ValueType")
IdType = TypeVar("IdType")
ProtobufProducerType = tuple[Union[type[SettingId], type[StatusId]], QueryCmdId]

ProtobufPrinter = google.protobuf.json_format._Printer  # type: ignore # noqa
original_field_to_json = ProtobufPrinter._FieldToJsonObject


######################################################## BLE #################################################


def build_enum_adapter(target: type[enum.Enum]) -> BytesParserBuilder:
    """Build an enum to Construct parsing and building adapter

    This adapter only works on byte data of length 1

    Args:
        target (type[enum.Enum]): Enum to use use for parsing / building

    Returns:
        BytesParserBuilder: dynamically created parser / builder class
    """

    class EnumByteAdapter(BytesParserBuilder[enum.Enum]):
        """Adapt enums to / from a one byte value"""

        container: ClassVar[type[enum.Enum]] = target

        def parse(self, data: bytes) -> enum.Enum:
            return self.container(data[0])

        def build(self, *args: Any, **kwargs: Any) -> bytes:
            return bytes([args[0].value])

    return EnumByteAdapter()


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


class BleReadCommand(BleCommand[BleUUID]):
    """A BLE command that reads data from a BleUUID

    Args:
        communicator (GoProBle): BLE client to read
        uuid (BleUUID): BleUUID to read from
        response_parser (BytesParser): the parser that will parse the received bytestream into a JSON dict
    """

    def __init__(self, communicator: GoProBle, uuid: BleUUID, parser: BytesParser) -> None:
        super().__init__(communicator, uuid=uuid, parser=parser, identifier=uuid)

    def __call__(self) -> GoProResp:  # noqa: D102
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict())))
        response = self._communicator._read_characteristic(self._uuid)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def __str__(self) -> str:
        return f"Read {self._uuid.name.lower().replace('_', ' ').title()}"

    def _as_dict(self, *_: Any, **kwargs: Any) -> dict[str, Any]:
        """Return the attributes of the command as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: command as dict
        """
        return dict(id="Read " + self._uuid.name, **self._base_dict) | kwargs


class BleWriteCommand(BleCommand[CmdId]):
    """A BLE command that writes to a BleUUID and does not accept any parameters

    Args:
        communicator (GoProBle): BLE client to write
        uuid (BleUUID): BleUUID to write to
        cmd (CmdId): Command ID that is being sent
        param_builder (BytesBuilder, optional): is responsible for building the bytestream to send from the input params
        parser (BytesParser. optional): the parser that will parse the received bytestream into a JSON dict
    """

    def __init__(
        self,
        communicator: GoProBle,
        uuid: BleUUID,
        cmd: CmdId,
        param_builder: Optional[BytesBuilder] = None,
        parser: Optional[BytesParser] = None,
    ) -> None:
        self.param_builder = param_builder
        self.cmd = cmd
        super().__init__(communicator, uuid=uuid, parser=parser, identifier=cmd)

    @no_type_check
    def __call__(self, /, **kwargs: Any) -> GoProResp:  # noqa: D102
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict(**kwargs))))

        data = bytearray([self.cmd.value])
        params = bytearray()
        if self.param_builder:
            params.extend(self.param_builder.build(*kwargs.values()))
        else:
            for arg in kwargs.values():
                params.extend(arg.value if isinstance(arg, enum.Enum) else arg)
        if params:
            data.append(len(params))
            data.extend(params)
        response = self._communicator._send_ble_command(self._uuid, data, self._identifier)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def __str__(self) -> str:
        return self.cmd.name.lower().replace("_", " ").removeprefix("cmdid").title()

    def _as_dict(self, *_: Any, **kwargs: Any) -> dict[str, Any]:
        """Return the attributes of the command as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: command as dict
        """
        return dict(id=self.cmd, **self._base_dict) | kwargs


class RegisterUnregisterAll(BleWriteCommand):
    """Base class for register / unregister all commands

    This will loop over all of the elements (i.e. settings / statuses found from the element_set entry of the
    producer tuple parameter) and individually register / unregister (depending on the action parameter) each
    element in the set

    Args:
        producer: (ProtobufProducerType): Tuple of (element_set, query command) where element_set is the GoProEnum
            that this command relates to, i.e. SettingId for settings, StatusId for Statuses
        action: (Action): whether to register or unregister
    """

    class Action(enum.Enum):
        """Enum to differentiate between register actions"""

        REGISTER = enum.auto()
        UNREGISTER = enum.auto()

    def __init__(
        self,
        communicator: GoProBle,
        uuid: BleUUID,
        cmd: CmdId,
        producer: ProtobufProducerType,
        action: Action,
        parser: Optional[BytesParser] = None,
    ) -> None:
        self.action = action
        self.producer = producer
        super().__init__(communicator, uuid=uuid, cmd=cmd, parser=parser)

    def __call__(self, **kwargs: Any) -> GoProResp:  # noqa: D102
        element_set = self.producer[0]
        responded_command = self.producer[1]
        response = super().__call__()
        if response.is_ok:
            for element in element_set:
                (
                    self._communicator._register_listener
                    if self.action is RegisterUnregisterAll.Action.REGISTER
                    else self._communicator._unregister_listener
                )(
                    (responded_command, element)  # type: ignore
                )
        return response


def protobuf_construct_adapter_factory(protobuf: type[Protobuf]) -> Construct:
    """Build a protobuf to Construct parsing (only) adapter

    Args:
        protobuf (type[Protobuf]): protobuf to use as parser

    Returns:
        Construct: adapter to be used by Construct for parsing and building
    """

    class ProtobufConstructAdapter(Adapter):
        """Adapt a protobuf to be used by Construct (for parsing only)"""

        protobuf: type[Protobuf]

        def _decode(self, obj: bytearray, *_: Any) -> dict[Any, Any]:
            """Parse a byte stream into a JSON dict using a protobuf

            Args:
                obj (bytearray): byte stream to parse
                _ (Any): Not used

            Returns:
                dict[Any, Any]: parsed JSON dict
            """
            response: Protobuf = self.protobuf().FromString(bytes(obj))

            # Monkey patch the field-to-json function to use our enum translation
            ProtobufPrinter._FieldToJsonObject = (
                lambda self, field, value: enum_factory(field.enum_type)(value)  # pylint: disable=not-callable
                if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_ENUM
                else original_field_to_json(self, field, value)
            )
            return ProtobufToDict(response)

        def _encode(self, *_: Any) -> Any:
            raise NotImplementedError

    setattr(ProtobufConstructAdapter, "protobuf", protobuf)
    return ProtobufConstructAdapter(GreedyBytes)


class BleProtoCommand(BleCommand[ActionId]):
    """A BLE command that is sent and received as using the Protobuf protocol

    Args:
        communicator (GoProBle): BLE client to write
        uuid (BleUUID): BleUUID to write to
        feature_id (CmdId): Command ID that is being sent
        action_id (FeatureId): protobuf specific action ID that is being sent
        response_action_id (ActionId):  the action ID that will be in the response
        request_proto (type[Protobuf]): protobuf used to build command bytestream
        response_proto (type[Protobuf]): protobuf used to parse received bytestream
        additional_matching_ids: (Optional[set[ActionId]]): Other action ID's to share
            this parser. This is used, for example, if a notification shares the same ID as the
            synchronous response. Defaults to None.
    """

    def __init__(
        self,
        communicator: GoProBle,
        uuid: BleUUID,
        feature_id: FeatureId,
        action_id: ActionId,
        response_action_id: ActionId,
        request_proto: type[Protobuf],
        response_proto: type[Protobuf],
        additional_matching_ids: Optional[set[Union[ActionId, CmdId]]] = None,
    ) -> None:
        super().__init__(
            communicator,
            uuid=uuid,
            parser=protobuf_construct_adapter_factory(response_proto),
            identifier=action_id,
        )
        self.feature_id = feature_id
        self.action_id = action_id
        self.response_action_id = response_action_id
        self.request_proto = request_proto
        self.response_proto = response_proto
        self.additional_matching_ids: set[Union[ActionId, CmdId]] = additional_matching_ids or set()
        assert self._parser
        for matching_id in [*self.additional_matching_ids, response_action_id]:
            GoProResp._add_global_parser(matching_id, self._parser)
        GoProResp._add_feature_action_id_mapping(self.feature_id, self.response_action_id)

    def build_data(self, **kwargs: Any) -> bytearray:
        """Build the byte data to prepare for command sending

        Args:
            **kwargs (Any): arguments to command to use to build protobuf

        Returns:
            bytearray: built byte data
        """
        proto = self.request_proto()
        for attr_name, arg in kwargs.items():
            value = arg.value if issubclass(type(arg), enum.Enum) else arg
            attr = getattr(proto, attr_name)
            # Protobuf "repeatable" (i.e. iterable) fields can not be set directly and must be appended / extended
            if isinstance(attr, Iterable) and not isinstance(value, (str, bytes)):
                if isinstance(value, Iterable):
                    for element in value:
                        attr.append(element.value if isinstance(element, enum.Enum) else element)  # type: ignore
                else:
                    attr.append(value.value if isinstance(value, enum.Enum) else value)  # type:ignore
            else:
                setattr(proto, attr_name, value)
        # Prepend headers and serialize
        return bytearray([self.feature_id.value, self.action_id.value, *proto.SerializeToString()])

    @abstractmethod
    @no_type_check
    # pylint: disable=missing-return-doc
    def __call__(self, /, **kwargs: Any) -> GoProResp:  # noqa: D102
        # The method that will actually build and send the protobuf command
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict(**kwargs))))
        data = self.build_data(**kwargs)
        # Allow exception to pass through if protobuf not completely initialized
        response = self._communicator._send_ble_command(self._uuid, data, self.response_action_id)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def __str__(self) -> str:
        return self.action_id.name.lower().replace("_", " ").removeprefix("actionid").title()

    def _as_dict(self, *_: Any, **kwargs: Any) -> dict[str, Any]:
        """Return the attributes of the command as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: command as dict
        """
        return dict(id=self.action_id, feature_id=self.feature_id, **self._base_dict) | kwargs


@dataclass
class BleAsyncResponse:
    """A BLE protobuf response that is not associated with any command.

    Args:
        feature_id (FeatureId): Feature ID that response corresponds to
        action_id (ActionId): Action ID that response corresponds to
        parser (BytesParser): how to parse the response
    """

    feature_id: FeatureId
    action_id: ActionId
    parser: BytesParser

    def __str__(self) -> str:
        return self.action_id.name.lower().replace("_", " ").removeprefix("actionid").title()


class BleSetting(BleCommand[SettingId], Generic[ValueType]):
    """An individual camera setting that is interacted with via BLE."""

    SETTER_UUID: Final[BleUUID] = GoProUUIDs.CQ_SETTINGS
    READER_UUID: Final[BleUUID] = GoProUUIDs.CQ_QUERY

    def __init__(
        self, communicator: GoProBle, identifier: SettingId, parser_builder: BytesParserBuilder
    ) -> None:
        """Constructor

        Args:
            communicator (GoProBle): Adapter to read / write settings data
            identifier (SettingId): ID of setting
            parser_builder (BytesParserBuilder): object to both parse and build setting
        """
        self._identifier = identifier
        self._builder = parser_builder
        BleCommand.__init__(
            self, communicator, uuid=self.SETTER_UUID, parser=parser_builder, identifier=identifier
        )

    def __str__(self) -> str:
        return str(self._identifier.name).lower().replace("_", " ").title()

    def _as_dict(  # type: ignore # pylint: disable = arguments-differ
        self, identifier: Union[QueryCmdId, SettingId, str], *_: Any, **kwargs: Any
    ) -> dict[str, Any]:
        """Return the attributes of the command as a dict

        Args:
            identifier (Union[QueryCmdId, SettingId, str]): identifier of the command for this send
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: setting as dict
        """
        return dict(id=identifier, **self._base_dict) | kwargs

    def set(self, value: ValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (ValueType): The argument to use to set the setting value.

        Returns:
            GoProResp: Status of set
        """
        logger.info(
            Logger.build_log_tx_str(jsonify(self._as_dict(f"Set {str(self._identifier)}", value=value)))
        )
        # Special case. Can't use _send_query
        data = bytearray([self._identifier.value])
        try:
            param = self._builder.build(value)
            data.extend([len(param), *param])
        except IndexError:
            pass

        response = self._communicator._send_ble_command(self.SETTER_UUID, data, self._identifier)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def _send_query(self, response_id: QueryCmdId) -> GoProResp:
        """Build the byte data and query setting information

        Args:
            response_id (QueryCmdId): expected identifier of response

        Returns:
            GoProResp: query response
        """
        data = self._build_cmd(response_id)
        logger.info(
            Logger.build_log_tx_str(jsonify(self._as_dict(f"{str(response_id)}.{self._identifier.name}")))
        )
        response = self._communicator._send_ble_command(self.READER_UUID, data, response_id)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def get_value(self) -> GoProResp:
        """Get the settings value.

        Returns:
            GoProResp: settings value
        """
        return self._send_query(QueryCmdId.GET_SETTING_VAL)

    def get_name(self) -> GoProResp:
        """Get the settings name.

        Raises:
            NotImplementedError: This isn't implemented on the camera
        """
        raise NotImplementedError("Not implemented on camera!")

    def get_capabilities_values(self) -> GoProResp:
        """Get currently supported settings capabilities values.

        Returns:
            GoProResp: settings capabilities values
        """
        return self._send_query(QueryCmdId.GET_CAPABILITIES_VAL)

    def get_capabilities_names(self) -> GoProResp:
        """Get currently supported settings capabilities names.

        Raises:
            NotImplementedError: This isn't implemented on the camera
        """
        raise NotImplementedError("Not implemented on camera!")

    def register_value_update(self) -> GoProResp:
        """Register for asynchronous notifications when a given setting ID's value updates.

        Returns:
            GoProResp: Current value of respective setting ID
        """
        if (response := self._send_query(QueryCmdId.REG_SETTING_VAL_UPDATE)).is_ok:
            self._communicator._register_listener((QueryCmdId.SETTING_VAL_PUSH, self._identifier))
        return response

    def unregister_value_update(self) -> GoProResp:
        """Stop receiving notifications when a given setting ID's value updates.

        Returns:
            GoProResp: Status of unregister
        """
        if (response := self._send_query(QueryCmdId.UNREG_SETTING_VAL_UPDATE)).is_ok:
            self._communicator._unregister_listener((QueryCmdId.SETTING_VAL_PUSH, self._identifier))
        return response

    def register_capability_update(self) -> GoProResp:
        """Register for asynchronous notifications when a given setting ID's capabilities update.

        Returns:
            GoProResp: Current capabilities of respective setting ID
        """
        if (response := self._send_query(QueryCmdId.REG_CAPABILITIES_UPDATE)).is_ok:
            self._communicator._register_listener((QueryCmdId.SETTING_CAPABILITY_PUSH, self._identifier))
        return response

    def unregister_capability_update(self) -> GoProResp:
        """Stop receiving notifications when a given setting ID's capabilities change.

        Returns:
            GoProResp: Status of unregister
        """
        if (response := self._send_query(QueryCmdId.UNREG_CAPABILITIES_UPDATE)).is_ok:
            self._communicator._unregister_listener((QueryCmdId.SETTING_CAPABILITY_PUSH, self._identifier))
        return response

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data to send a settings query over-the-air.

        Args:
            cmd (QueryCmdId): command to build

        Returns:
            bytearray: data to send over-the-air
        """
        ret = bytearray([cmd.value, self._identifier.value])
        return ret


class BleStatus(BleCommand[StatusId]):
    """An individual camera status that is interacted with via BLE."""

    UUID: Final[BleUUID] = GoProUUIDs.CQ_QUERY

    def __init__(self, communicator: GoProBle, identifier: StatusId, parser: BytesParser) -> None:
        """Constructor

        Args:
            communicator (GoProBle): Adapter to read status data
            identifier (StatusId): ID of status
            parser (BytesParser): parser used to build response
        """
        BleCommand.__init__(self, communicator, uuid=self.UUID, parser=parser, identifier=identifier)
        self._identifier = identifier

    def __str__(self) -> str:
        return str(self._identifier.name.lower().replace("_", " ")).title()

    def _send_query(self, response_id: QueryCmdId) -> GoProResp:
        """Build the byte data and query setting information

        Args:
            response_id (QueryCmdId): expected identifier of response

        Returns:
            GoProResp: query response
        """
        data = self._build_cmd(response_id)
        logger.info(
            Logger.build_log_tx_str(jsonify(self._as_dict(f"{response_id.name}.{self._identifier.name}")))
        )
        response = self._communicator._send_ble_command(self.UUID, data, response_id)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def _as_dict(  # type: ignore # pylint: disable = arguments-differ
        self,
        identifier: Union[QueryCmdId, SettingId, str],
        *_: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Return the attributes of the command as a dict

        Args:
            identifier (Union[QueryCmdId, SettingId, str]): identifier of the command for this send
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: command as dict
        """
        return dict(id=identifier, **self._base_dict) | kwargs

    def get_value(self) -> GoProResp:
        """Get the current value of a status.

        Returns:
            GoProResp: current status value
        """
        return self._send_query(QueryCmdId.GET_STATUS_VAL)

    def register_value_update(self) -> GoProResp:
        """Register for asynchronous notifications when a status changes.

        Returns:
            GoProResp: current status value
        """
        if (response := self._send_query(QueryCmdId.REG_STATUS_VAL_UPDATE)).is_ok:
            self._communicator._register_listener((QueryCmdId.STATUS_VAL_PUSH, self._identifier))
        return response

    def unregister_value_update(self) -> GoProResp:
        """Stop receiving notifications when status changes.

        Returns:
            GoProResp: Status of unregister
        """
        if (response := self._send_query(QueryCmdId.UNREG_STATUS_VAL_UPDATE)).is_ok:
            self._communicator._unregister_listener((QueryCmdId.STATUS_VAL_PUSH, self._identifier))
        return response

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data for a given status command.

        Args:
            cmd (QueryCmdId): command to build data for

        Returns:
            bytearray: data to send over-the-air
        """
        ret = bytearray([cmd.value, self._identifier.value])
        return ret


######################################################## Wifi #################################################


class WifiGetJsonCommand(WifiCommand[str]):
    """A Wifi command that writes to a BleUUID (with parameters) and receives JSON as response"""

    def __init__(
        self,
        communicator: GoProWifi,
        endpoint: str,
        components: Optional[list[str]] = None,
        arguments: Optional[list[str]] = None,
        parser: Optional[type[JsonParser]] = None,
        identifier: Optional[str] = None,
    ) -> None:
        if not identifier:
            # Build human-readable name from endpoint
            identifier = endpoint.lower().removeprefix("gopro/").replace("/", " ").replace("_", " ").title()
            try:
                identifier = identifier.split("?")[0].strip("{}")
            except IndexError:
                pass
        super().__init__(communicator, endpoint, identifier, components, arguments, parser)

    @no_type_check
    def __call__(self, **kwargs: Any) -> GoProResp:  # noqa: D102
        # Append components
        url = self._endpoint
        for component in self._components or []:
            url += "/" + kwargs.pop(component)
        # Append parameters
        if self._args:
            url += "?" + urlencode(
                {
                    k: kwargs[k].value if isinstance(kwargs[k], enum.Enum) else kwargs[k]
                    for k in self._args
                    if kwargs[k] is not None
                },
                safe="/",
            )
        # Send to camera
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict(**kwargs, endpoint=url))))
        response = self._communicator._get(url, self._parser)
        response._meta.append(self._identifier)
        logger.info(Logger.build_log_rx_str(response))
        return response


class WifiGetBinary(WifiCommand[str]):
    """A Wifi command that writes to a BleUUID (with parameters) and receives a binary stream as response"""

    def __init__(
        self,
        communicator: GoProWifi,
        endpoint: str,
        components: Optional[list[str]] = None,
        arguments: Optional[list[str]] = None,
        parser: Optional[type[JsonParser]] = None,
        identifier: Optional[str] = None,
    ) -> None:
        if not identifier:
            # Build human-readable name from endpoint
            identifier = endpoint.lower().removeprefix("gopro/").replace("/", " ").replace("_", " ").title()
            try:
                identifier = identifier.split("?")[0].strip("{}")
            except IndexError:
                pass
        super().__init__(communicator, endpoint, identifier, components, arguments, parser)

    def __call__(self, /, camera_file: str, local_file: Optional[Path] = None) -> Path:  # noqa: D102
        # The method that will actually send the command and receive the stream
        local_file = local_file or Path(".") / camera_file
        url = self._endpoint + "/" + camera_file
        logger.info(
            Logger.build_log_tx_str(
                jsonify(self._as_dict(endpoint=url, camera_file=camera_file, local_file=local_file))
            )
        )
        # Send to camera
        self._communicator._stream_to_file(url, local_file)
        logger.info(
            Logger.build_log_rx_str(
                jsonify(self._as_dict(status="SUCCESS", endpoint=url, local_file=local_file))
            )
        )
        return local_file


class WifiSetting(WifiCommand[SettingId], Generic[ValueType]):
    """An individual camera setting that is interacted with via Wifi."""

    def __init__(self, communicator: GoProWifi, identifier: SettingId) -> None:
        super().__init__(
            communicator,
            "gopro/camera/setting?setting={}&option={}",
            identifier=identifier,
        )
        # Note! It is assumed that BLE and WiFi settings are symmetric so we only add to the communicator's
        # parser in the BLE Setting.

    def __str__(self) -> str:
        return str(self._identifier.name.lower().replace("_", " ")).title()

    def set(self, value: ValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (ValueType): value to set setting

        Returns:
            GoProResp: Status of set
        """
        url = self._endpoint.format(self._identifier.value, value)
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict(value=value, endpoint=url))))
        value = value.value if isinstance(value, enum.Enum) else value
        # Send to camera
        if response := self._communicator._get(url):
            response._meta.append(self._identifier)
            logger.info(Logger.build_log_rx_str(response))
        return response
