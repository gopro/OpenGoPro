# builders.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Common functionality across API versions to build commands, settings, and statuses"""

from __future__ import annotations
import enum
import logging
from pathlib import Path
from urllib.parse import urlencode
from collections.abc import Iterable
from dataclasses import dataclass, InitVar, field
from typing import Any, TypeVar, Generic, Union, Optional, Final, Callable

import wrapt
import google.protobuf.json_format
from google.protobuf import descriptor
from google.protobuf.message import Message as Protobuf
from google.protobuf.json_format import MessageToDict as ProtobufToDict
import construct

from open_gopro.responses import BytesBuilder, BytesParser, GoProResp, JsonParser, BytesParserBuilder, Parser
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
    GoProEnum,
)
from open_gopro.interface import (
    GoProBle,
    GoProHttp,
    BleMessage,
    HttpMessage,
    BleMessages,
    HttpMessages,
    MessageRules,
    RuleSignature,
)
from open_gopro.util import Logger, jsonify

logger = logging.getLogger(__name__)

ValueType = TypeVar("ValueType")
IdType = TypeVar("IdType")
ProtobufProducerType = tuple[Union[type[SettingId], type[StatusId]], QueryCmdId]

ProtobufPrinter = google.protobuf.json_format._Printer  # type: ignore # noqa
original_field_to_json = ProtobufPrinter._FieldToJsonObject

QueryParserType = Union[construct.Construct, type[GoProEnum], BytesParserBuilder]
AsyncParserType = Union[construct.Construct, BytesParser[dict], type[Protobuf]]


######################################################## BLE #################################################


def enum_parser_factory(target: type[GoProEnum]) -> BytesParserBuilder:
    """Build an Enum ParserBuilder

    Args:
        target (type[GoProEnum]): enum to use for parsing and building

    Returns:
        BytesParserBuilder: instance of generated class
    """

    class ParserBuilder(BytesParserBuilder[GoProEnum]):
        """Adapt enums to / from a one byte value"""

        container = target

        def parse(self, data: bytes) -> GoProEnum:
            return self.container(data[0])

        def build(self, *args: Any, **_: Any) -> bytes:
            return bytes([int(args[0])])

    return ParserBuilder()


def construct_adapter_factory(target: construct.Construct) -> BytesParserBuilder:
    """Build a construct parser adapter from a construct

    Args:
        target (construct.Construct): construct to use for parsing and building

    Returns:
        BytesParserBuilder: instance of generated class
    """

    class ParserBuilder(BytesParserBuilder):
        """Adapt the construct for our interface"""

        container = target

        def parse(self, data: bytes) -> Any:
            return self.container.parse(data)

        def build(self, *args: Any, **kwargs: Any) -> bytes:
            return self.container.build(*args, **kwargs)

    return ParserBuilder()


def protobuf_parser_factory(proto: type[Protobuf]) -> BytesParser[dict]:
    """Build a BytesParser from a protobuf definition

    Args:
        proto (type[Protobuf]): protobuf definition to build class from

    Returns:
        BytesParser[dict]: instance of generated class
    """

    class ProtobufByteParser(BytesParser[dict]):
        """Parse bytes into a dict using the protobuf"""

        protobuf = proto

        def parse(self, data: bytes) -> dict:
            response: Protobuf = self.protobuf().FromString(bytes(data))

            # Monkey patch the field-to-json function to use our enum translation
            ProtobufPrinter._FieldToJsonObject = (
                lambda self, field, value: enum_factory(field.enum_type)(value)  # pylint: disable=not-callable
                if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_ENUM
                else original_field_to_json(self, field, value)
            )
            return ProtobufToDict(response, preserving_proto_field_name=True)

    return ProtobufByteParser()


class DeprecatedAdapter(BytesParserBuilder[str]):
    """Used to return "DEPRECATED" when a deprecated setting / status is attempted to be parsed / built"""

    def parse(self, data: bytes) -> str:
        """Return string indicating this ID is deprecated

        Args:
            data (bytes): ignored

        Returns:
            str: "DEPRECATED"
        """
        return "DEPRECATED"

    def build(self, obj: Any) -> bytes:
        """Return empty bytes since this ID is deprecated

        Args:
            obj (Any): ignored

        Returns:
            bytes: empty
        """
        return bytes()


class BleReadCommand(BleMessage[BleUUID]):
    """A BLE command that reads data from a BleUUID"""

    def __init__(self, uuid: BleUUID, parser: Optional[Union[construct.Construct, BytesParser[dict]]]) -> None:
        """Constructor

        Args:
            uuid (BleUUID):  BleUUID to read from
            parser (Optional[Union[construct.Construct, BytesParser[dict]]]): the parser that will parse the
                received bytestream into a JSON dict
        """
        super().__init__(
            uuid=uuid,
            parser=construct_adapter_factory(parser) if isinstance(parser, construct.Construct) else parser,
            identifier=uuid,
        )

    def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> GoProResp:  # noqa: D102
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict())))
        response = __communicator__._read_characteristic(self._uuid)
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
        return {"id": "Read " + self._uuid.name, **self._base_dict} | kwargs  # type: ignore


class BleWriteCommand(BleMessage[CmdId]):
    """A BLE command that writes to a BleUUID and does not accept any parameters"""

    def __init__(
        self,
        uuid: BleUUID,
        cmd: CmdId,
        param_builder: Optional[BytesBuilder] = None,
        parser: Optional[Union[construct.Construct, BytesParser[dict]]] = None,
        rules: Optional[dict[MessageRules, RuleSignature]] = None,
    ) -> None:
        """Constructor

        Args:
            uuid (BleUUID): BleUUID to write to
            cmd (CmdId): Command ID that is being sent
            param_builder (BytesBuilder, optional): is responsible for building the bytestream to send from the input params
            parser (BytesParser. optional): the parser that will parse the received bytestream into a JSON dict
            rules (Optional[dict[MessageRules, RuleSignature]], optional): rules to apply when executing this
                message. Defaults to None.
        """
        self.param_builder = param_builder
        self.cmd = cmd
        super().__init__(
            uuid,
            construct_adapter_factory(parser) if isinstance(parser, construct.Construct) else parser,
            cmd,
            rules,
        )

    def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> GoProResp:
        """Execute the command by sending it via BLE

        Args:
            __communicator__ (GoProBle): BLE communicator to send the message
            **kwargs (Any): arguments to BLE write command

        Returns:
            GoProResp: Response received via BLE
        """
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
        response = __communicator__._send_ble_message(
            self._uuid, data, self._identifier, rules=self._evaluate_rules(**kwargs)
        )
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
        return {"id": self.cmd, **self._base_dict} | kwargs  # type: ignore


class RegisterUnregisterAll(BleWriteCommand):
    """Base class for register / unregister all commands

    This will loop over all of the elements (i.e. settings / statuses found from the element_set entry of the
    producer tuple parameter) and individually register / unregister (depending on the action parameter) each
    element in the set
    """

    class Action(enum.Enum):
        """Enum to differentiate between register actions"""

        REGISTER = enum.auto()
        UNREGISTER = enum.auto()

    def __init__(
        self,
        uuid: BleUUID,
        cmd: CmdId,
        producer: ProtobufProducerType,
        action: Action,
        parser: Optional[BytesParser] = None,
    ) -> None:
        """Constructor

        Args:
            uuid (BleUUID): UUID to write to
            cmd (CmdId): Command ID that is being sent
            producer (ProtobufProducerType): Tuple of (element_set, query command) where element_set is the GoProEnum
                that this command relates to, i.e. SettingId for settings, StatusId for Statuses
            action (Action): whether to register or unregister
            parser (Optional[BytesParser], optional): Optional response parser. Defaults to None.
        """
        self.action = action
        self.producer = producer
        super().__init__(uuid=uuid, cmd=cmd, parser=parser)

    def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> GoProResp:  # noqa: D102
        element_set = self.producer[0]
        responded_command = self.producer[1]
        response = super().__call__(__communicator__)
        if response.is_ok:
            for element in element_set:
                (
                    __communicator__._register_listener
                    if self.action is RegisterUnregisterAll.Action.REGISTER
                    else __communicator__._unregister_listener
                )(
                    (responded_command, element)  # type: ignore
                )
        return response


class BleProtoCommand(BleMessage[ActionId]):
    """A BLE command that is sent and received as using the Protobuf protocol"""

    def __init__(
        self,
        uuid: BleUUID,
        feature_id: FeatureId,
        action_id: ActionId,
        response_action_id: ActionId,
        request_proto: type[Protobuf],
        response_proto: type[Protobuf],
        additional_matching_ids: Optional[set[Union[ActionId, CmdId]]] = None,
        additional_parsers: Optional[list[JsonParser]] = None,
    ) -> None:
        """Constructor

        Args:
            uuid (BleUUID): BleUUID to write to
            feature_id (FeatureId): Feature ID that is being executed
            action_id (ActionId): protobuf specific action ID that is being executed
            response_action_id (ActionId): the action ID that will be in the response to this command
            request_proto (type[Protobuf]): the action ID that will be in the response
            response_proto (type[Protobuf]): protobuf used to parse received bytestream
            additional_matching_ids (Optional[set[Union[ActionId, CmdId]]], optional): Other action ID's to share
                this parser. This is used, for example, if a notification shares the same ID as the
                synchronous response. Defaults to None.. Defaults to None.
            additional_parsers (Optional[list[JsonParser]], optional): Any additional JSON parsers to apply
                after normal protobuf response parsing. Defaults to None.
        """
        parser = protobuf_parser_factory(response_proto)
        for p in additional_parsers or []:
            parser += p  # type: ignore
        super().__init__(uuid=uuid, parser=parser, identifier=action_id)
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

    def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> GoProResp:  # noqa: D102
        # The method that will actually build and send the protobuf command
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict(**kwargs))))
        data = self.build_data(**kwargs)
        # Allow exception to pass through if protobuf not completely initialized
        response = __communicator__._send_ble_message(self._uuid, data, self.response_action_id)
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
        return {"id": self.action_id, "feature_id": self.feature_id, **self._base_dict} | kwargs  # type: ignore


def ble_write_command(
    uuid: BleUUID,
    cmd: CmdId,
    param_builder: Optional[BytesBuilder] = None,
    parser: Optional[Union[construct.Construct, BytesParser[dict]]] = None,
    rules: Optional[dict[MessageRules, RuleSignature]] = None,
) -> Callable:
    """Factory to build a BleWriteCommand and wrapper to execute it

    Args:
        uuid (BleUUID): BleUUID to write to
        cmd (CmdId): Command ID that is being sent
        param_builder (BytesBuilder, optional): is responsible for building the bytestream to send from the input params
        parser (BytesParser. optional): the parser that will parse the received bytestream into a JSON dict
        rules (dict[MessageRules, RuleSignature], optional): Rules to be applied to message execution

    Returns:
        Callable: Generated method to perform command
    """
    message = BleWriteCommand(uuid, cmd, param_builder, parser, rules=rules)

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return message(instance._communicator, **(wrapped(**kwargs) or kwargs))

    return wrapper


def ble_read_command(
    uuid: BleUUID, parser: Optional[Union[construct.Construct, BytesParser[dict]]]
) -> Callable:
    """Factory to build a BleReadCommand and wrapper to execute it

    Args:
        uuid (BleUUID):  BleUUID to read from
        parser (Optional[Union[construct.Construct, BytesParser[dict]]]): the parser that will parse the
            received bytestream into a JSON dict

    Returns:
        Callable: Generated method to perform command
    """
    message = BleReadCommand(uuid, parser)

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return message(instance._communicator, **(wrapped(**kwargs) or kwargs))

    return wrapper


def ble_register_command(
    uuid: BleUUID,
    cmd: CmdId,
    producer: ProtobufProducerType,
    action: RegisterUnregisterAll.Action,
    parser: Optional[BytesParser] = None,
) -> Callable:
    """Factory to build a RegisterUnregisterAll command and wrapper to execute it

    Args:
        uuid (BleUUID): UUID to write to
        cmd (CmdId): Command ID that is being sent
        producer (ProtobufProducerType): Tuple of (element_set, query command) where element_set is the GoProEnum
            that this command relates to, i.e. SettingId for settings, StatusId for Statuses
        action (Action): whether to register or unregister
        parser (Optional[BytesParser], optional): Optional response parser. Defaults to None.

    Returns:
        Callable: Generated method to perform command
    """
    message = RegisterUnregisterAll(uuid, cmd, producer, action, parser)

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return message(instance._communicator, **(wrapped(**kwargs) or kwargs))

    return wrapper


def ble_proto_command(
    uuid: BleUUID,
    feature_id: FeatureId,
    action_id: ActionId,
    response_action_id: ActionId,
    request_proto: type[Protobuf],
    response_proto: type[Protobuf],
    additional_matching_ids: Optional[set[Union[ActionId, CmdId]]] = None,
    additional_parsers: Optional[list[JsonParser]] = None,
) -> Callable:
    """Factory to build a BLE Protobuf command and wrapper to execute it

    Args:
        uuid (BleUUID): BleUUID to write to
        feature_id (FeatureId): Feature ID that is being executed
        action_id (ActionId): protobuf specific action ID that is being executed
        response_action_id (ActionId): the action ID that will be in the response to this command
        request_proto (type[Protobuf]): the action ID that will be in the response
        response_proto (type[Protobuf]): protobuf used to parse received bytestream
        additional_matching_ids (Optional[set[Union[ActionId, CmdId]]], optional): Other action ID's to share
            this parser. This is used, for example, if a notification shares the same ID as the
            synchronous response. Defaults to None.. Defaults to None.
        additional_parsers (Optional[list[JsonParser]], optional): Any additional JSON parsers to apply
            after normal protobuf response parsing. Defaults to None.

    Returns:
        Callable: Generated method to perform command
    """
    message = BleProtoCommand(
        uuid,
        feature_id,
        action_id,
        response_action_id,
        request_proto,
        response_proto,
        additional_matching_ids,
        additional_parsers,
    )

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return message(instance._communicator, **(wrapped(**kwargs) or kwargs))

    return wrapper


@dataclass
class BleAsyncResponse:
    """A BLE protobuf response that is not associated with any message.

    Args:
        feature_id (FeatureId): Feature ID that response corresponds to
        action_id (ActionId): Action ID that response corresponds to
        parser_type (AsyncParserType): how to parse the response
    """

    feature_id: FeatureId
    action_id: ActionId
    parser_type: InitVar[AsyncParserType]
    parser: Parser = field(init=False)

    def __post_init__(self, parser_type: AsyncParserType) -> None:
        if isinstance(parser_type, construct.Construct):
            self.parser = construct_adapter_factory(parser_type)
        elif isinstance(parser_type, BytesParser):
            self.parser = parser_type
        elif issubclass(parser_type, Protobuf):
            self.parser = protobuf_parser_factory(parser_type)
        else:
            raise TypeError(f"Unexpected {parser_type=}")

    def __str__(self) -> str:
        return self.action_id.name.lower().replace("_", " ").removeprefix("actionid").title()


class BleSetting(BleMessage[SettingId], Generic[ValueType]):
    """An individual camera setting that is interacted with via BLE."""

    SETTER_UUID: Final[BleUUID] = GoProUUIDs.CQ_SETTINGS
    READER_UUID: Final[BleUUID] = GoProUUIDs.CQ_QUERY

    def __init__(self, communicator: GoProBle, identifier: SettingId, parser_builder: QueryParserType) -> None:
        """Constructor

        Args:
            communicator (GoProBle): BLE communicator to interact with setting
            identifier (SettingId): ID of setting
            parser_builder (QueryParserType): object to both parse and build setting

        Raises:
            TypeError: Invalid parser_builder type
        """
        if isinstance(parser_builder, construct.Construct):
            parser = construct_adapter_factory(parser_builder)
        elif isinstance(parser_builder, BytesParserBuilder):
            parser = parser_builder
        elif issubclass(parser_builder, GoProEnum):
            parser = enum_parser_factory(parser_builder)
        else:
            raise TypeError(f"Unexpected {parser_builder=}")
        self._identifier = identifier
        self._builder = parser
        self._communicator = communicator
        BleMessage.__init__(self, uuid=self.SETTER_UUID, parser=parser, identifier=identifier)

    def __str__(self) -> str:
        return str(self._identifier).lower().replace("_", " ").title()

    def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> Any:
        """Not applicable for a BLE setting

        Args:
            __communicator__ (GoProBle): BLE communicator
            **kwargs (Any): not used

        Raises:
            NotImplementedError: Not applicable
        """
        raise NotImplementedError

    def _as_dict(  # pylint: disable = arguments-differ
        self, identifier: Union[QueryCmdId, SettingId, str], *_: Any, **kwargs: Any
    ) -> dict[str, Any]:
        """Return the attributes of the message as a dict

        Args:
            identifier (Union[QueryCmdId, SettingId, str]): identifier of the message for this send
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: setting as dict
        """
        return {"id": identifier, **self._base_dict} | kwargs  # type: ignore

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
        data = bytearray([int(self._identifier)])
        try:
            param = self._builder.build(value)
            data.extend([len(param), *param])
        except IndexError:
            pass

        response = self._communicator._send_ble_message(self.SETTER_UUID, data, self._identifier)
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
            Logger.build_log_tx_str(jsonify(self._as_dict(f"{str(response_id)}.{str(self._identifier)}")))
        )
        response = self._communicator._send_ble_message(self.READER_UUID, data, response_id)
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
        ret = bytearray([cmd.value, int(self._identifier)])
        return ret


class BleStatus(BleMessage[StatusId]):
    """An individual camera status that is interacted with via BLE."""

    UUID: Final[BleUUID] = GoProUUIDs.CQ_QUERY

    def __init__(self, communicator: GoProBle, identifier: StatusId, parser: QueryParserType) -> None:
        """Constructor

        Args:
            communicator (GoProBle): Adapter to read status data
            identifier (StatusId): ID of status
            parser (QueryParserType): construct to parse or enum to represent status value

        Raises:
            TypeError: Invalid parser type
        """
        if isinstance(parser, construct.Construct):
            parser_builder = construct_adapter_factory(parser)
        elif isinstance(parser, BytesParserBuilder):
            parser_builder = parser
        elif issubclass(parser, GoProEnum):
            parser_builder = enum_parser_factory(parser)
        else:
            raise TypeError(f"Unexpected {parser=}")
        self._communicator = communicator
        BleMessage.__init__(self, uuid=self.UUID, parser=parser_builder, identifier=identifier)
        self._identifier = identifier

    def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> Any:
        """Not applicable for a BLE status

        Args:
            __communicator__ (GoProBle): BLE communicator
            **kwargs (Any): not used

        Raises:
            NotImplementedError: Not applicable
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self._identifier).lower().replace("_", " ").title()

    def _send_query(self, response_id: QueryCmdId) -> GoProResp:
        """Build the byte data and query setting information

        Args:
            response_id (QueryCmdId): expected identifier of response

        Returns:
            GoProResp: query response
        """
        data = self._build_cmd(response_id)
        logger.info(
            Logger.build_log_tx_str(jsonify(self._as_dict(f"{response_id.name}.{str(self._identifier)}")))
        )
        response = self._communicator._send_ble_message(self.UUID, data, response_id)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def _as_dict(  # pylint: disable = arguments-differ
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
        return {"id": identifier, **self._base_dict} | kwargs  # type: ignore

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
        ret = bytearray([cmd.value, int(self._identifier)])
        return ret


######################################################## HTTP #################################################


class HttpCommand(HttpMessage[str]):
    """The base class for HTTP Commands"""

    def __init__(
        self,
        endpoint: str,
        components: Optional[list[str]] = None,
        arguments: Optional[list[str]] = None,
        parser: Optional[JsonParser] = None,
        identifier: Optional[str] = None,
        rules: Optional[dict[MessageRules, RuleSignature]] = None,
    ) -> None:
        """Constructor

        Args:
            endpoint (str): base endpoint
            components (Optional[list[str]]): conditional endpoint components. Defaults to None.
            arguments (Optional[list[str]]): URL argument names. Defaults to None.
            parser (Optional[JsonParser]): additional parsing of JSON response. Defaults to None.
            identifier (Optional[IdType]): explicitly set message identifier. Defaults to None (generated from endpoint).
            rules (Optional[dict[MessageRules, RuleSignature]], optional): rules to apply when executing this
                message. Defaults to None.
        """
        if not identifier:
            # Build human-readable name from endpoint
            identifier = endpoint.lower().removeprefix("gopro/").replace("/", " ").replace("_", " ").title()
            try:
                identifier = identifier.split("?")[0].strip("{}")
            except IndexError:
                pass

        super().__init__(endpoint, identifier, components, arguments, parser, rules)


class HttpGetJsonCommand(HttpCommand):
    """An HTTP command that performs a GET operation and receives JSON as response"""

    def __call__(
        self, __communicator__: GoProHttp, rules: Optional[list[MessageRules]] = None, **kwargs: Any
    ) -> GoProResp:
        """Execute the command by sending it via HTTP

        Args:
            __communicator__ (GoProHttp): HTTP communicator
            rules (Optional[dict[MessageRules, RuleSignature]], optional): rules to apply when executing this
                message. Defaults to None.
            **kwargs (Any): arguments to message

        Returns:
            GoProResp: Response received via HTTP
        """
        # Append components
        url = self._endpoint
        for component in self._components or []:
            url += "/" + kwargs.pop(component)
        # Append parameters
        if self._args and (
            arg_part := urlencode(
                {
                    k: kwargs[k].value if isinstance(kwargs[k], enum.Enum) else kwargs[k]
                    for k in self._args
                    if kwargs[k] is not None
                },
                safe="/",
            )
        ):
            url += "?" + arg_part

        # Send to camera
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict(**kwargs, endpoint=url))))
        response = __communicator__._get(url, self._parser, rules=rules)
        response._meta.append(self._identifier)
        logger.info(Logger.build_log_rx_str(response))
        return response


# pylint: disable = missing-class-docstring, arguments-differ
class HttpGetBinary(HttpCommand):
    """An HTTP command that performs a GET operation and receives a binary stream as response"""

    def __call__(  # type: ignore
        self, __communicator__: GoProHttp, *, camera_file: str, local_file: Optional[Path] = None
    ) -> GoProResp:
        """Execute the command by getting the binary data from the communicator

        Args:
            __communicator__ (GoProHttp): HTTP communicator to query
            camera_file (str): file on camera to access
            local_file (Optional[Path], optional): file on local device to write to. Defaults to None
                (camera-file will be used).

        Returns:
            GoProResp: location on local device that file was written to
        """
        # The method that will actually send the command and receive the stream
        local_file = local_file or Path(".") / camera_file
        url = self._endpoint + "/" + camera_file
        logger.info(
            Logger.build_log_tx_str(
                jsonify(self._as_dict(endpoint=url, camera_file=camera_file, local_file=local_file))
            )
        )
        # Send to camera
        response = __communicator__._stream_to_file(url, local_file)
        logger.info(
            Logger.build_log_rx_str(
                jsonify(self._as_dict(status="SUCCESS", endpoint=url, local_file=local_file))
            )
        )
        return response


def http_get_json_command(
    endpoint: str,
    components: Optional[list[str]] = None,
    arguments: Optional[list[str]] = None,
    parser: Optional[JsonParser] = None,
    identifier: Optional[str] = None,
    rules: Optional[dict[MessageRules, RuleSignature]] = None,
) -> Callable:
    """Factory to build an HttpGetJson command and wrapper to execute it

    Args:
        endpoint (str): base endpoint
        components (Optional[list[str]]): conditional endpoint components. Defaults to None.
        arguments (Optional[list[str]]): URL argument names. Defaults to None.
        parser (Optional[JsonParser]): additional parsing of JSON response. Defaults to None.
        identifier (Optional[str]): explicitly set message identifier. Defaults to None (generated from endpoint).
        rules (dict[MessageRules, RuleSignature], optional): Rules to be applied to message execution

    Returns:
        Callable: Generated method to perform command
    """
    message = HttpGetJsonCommand(endpoint, components, arguments, parser, identifier, rules=rules)

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: HttpMessages, _: Any, kwargs: Any) -> GoProResp:
        return message(
            instance._communicator, message._evaluate_rules(**kwargs), **(wrapped(**kwargs) or kwargs)
        )

    return wrapper


def http_get_binary_command(
    endpoint: str,
    components: Optional[list[str]] = None,
    arguments: Optional[list[str]] = None,
    parser: Optional[JsonParser] = None,
    identifier: Optional[str] = None,
) -> Callable:
    """Factory to build am HttpGetBinary command and wrapper to execute it

    Args:
        endpoint (str): base endpoint
        components (Optional[list[str]]): conditional endpoint components. Defaults to None.
        arguments (Optional[list[str]]): URL argument names. Defaults to None.
        parser (Optional[JsonParser]): additional parsing of JSON response. Defaults to None.
        identifier (Optional[IdType]): explicitly set message identifier. Defaults to None (generated from endpoint).

    Returns:
        Callable: Generated method to perform command
    """
    message = HttpGetBinary(endpoint, components, arguments, parser, identifier)

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: HttpMessages, _: Any, kwargs: Any) -> GoProResp:
        return message(instance._communicator, **(wrapped(**kwargs) or kwargs))

    return wrapper


class HttpSetting(HttpMessage[SettingId], Generic[ValueType]):
    """An individual camera setting that is interacted with via Wifi."""

    def __init__(self, communicator: GoProHttp, identifier: SettingId) -> None:
        super().__init__(
            "gopro/camera/setting?setting={}&option={}",
            identifier=identifier,
        )
        self._communicator = communicator
        # Note! It is assumed that BLE and HTTP settings are symmetric so we only add to the communicator's
        # parser in the BLE Setting.

    def __call__(self, __communicator__: GoProHttp, **kwargs: Any) -> Any:
        """Not applicable for settings

        Args:
            __communicator__ (GoProHttp): HTTP communicator
            **kwargs (Any): not used

        Raises:
            NotImplementedError: not applicable
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self._identifier).lower().replace("_", " ").title()

    def set(self, value: ValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (ValueType): value to set setting

        Returns:
            GoProResp: Status of set
        """
        url = self._endpoint.format(int(self._identifier), value)
        logger.info(Logger.build_log_tx_str(jsonify(self._as_dict(value=value, endpoint=url))))
        value = value.value if isinstance(value, enum.Enum) else value
        # Send to camera
        if response := self._communicator._get(url):
            response._meta.append(self._identifier)
            logger.info(Logger.build_log_rx_str(response))
        return response
