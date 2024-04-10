# builders.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Common functionality across API versions to build commands, settings, and statuses"""

from __future__ import annotations

import enum
import logging
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Final, Generic, Protocol, TypeVar, Union

import construct
import wrapt

from open_gopro import types
from open_gopro.api.parsers import ByteParserBuilders
from open_gopro.ble import BleUUID
from open_gopro.communicator_interface import (
    BleMessage,
    BleMessages,
    GoProBle,
    GoProHttp,
    HttpMessage,
    HttpMessages,
    MessageRules,
)
from open_gopro.constants import (
    ActionId,
    CmdId,
    FeatureId,
    GoProUUIDs,
    QueryCmdId,
    SettingId,
    StatusId,
)
from open_gopro.enum import GoProIntEnum
from open_gopro.logger import Logger
from open_gopro.models.response import GlobalParsers, GoProResp
from open_gopro.parser_interface import BytesBuilder, BytesParserBuilder, Parser

logger = logging.getLogger(__name__)

ValueType = TypeVar("ValueType")

QueryParserType = Union[construct.Construct, type[GoProIntEnum], BytesParserBuilder]


######################################################## BLE #################################################

T = TypeVar("T")


class BleReadCommand(BleMessage):
    """A BLE command that reads data from a BleUUID"""

    def __init__(self, uuid: BleUUID, parser: Parser) -> None:
        """Constructor

        Args:
            uuid (BleUUID):  BleUUID to read from
            parser (Parser): the parser that will parse the received bytestream into a JSON dict
        """
        super().__init__(uuid=uuid, parser=parser, identifier=uuid)

    def _build_data(self, **kwargs: Any) -> bytearray:
        # Read commands do not have data
        raise NotImplementedError

    def __str__(self) -> str:
        return f"Read {self._uuid.name.lower().replace('_', ' ').title()}"

    def _as_dict(self, **kwargs: Any) -> types.JsonDict:
        """Return the attributes of the command as a dict

        Args:
            **kwargs (Any): additional entries for the dict

        Returns:
            types.JsonDict: command as dict
        """
        return {"id": self._uuid, **self._base_dict} | kwargs


class BleWriteCommand(BleMessage):
    """A BLE command that writes to a BleUUID and retrieves responses by accumulating notifications

    Args:
        uuid (BleUUID): UUID to write to
        cmd (CmdId): command identifier
        param_builder (BytesBuilder | None, optional): builds bytes from params. Defaults to None.
        parser (Parser | None, optional): response parser to parse received bytes. Defaults to None.
        rules (MessageRules): rules this Message must obey. Defaults to MessageRules().
    """

    def __init__(
        self,
        uuid: BleUUID,
        cmd: CmdId,
        param_builder: BytesBuilder | None = None,
        parser: Parser | None = None,
        rules: MessageRules = MessageRules(),
    ) -> None:
        self.param_builder = param_builder
        self.cmd = cmd
        self.rules = rules
        super().__init__(uuid, cmd, parser)

    def _build_data(self, **kwargs: Any) -> bytearray:
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
        return data

    def __str__(self) -> str:
        return self.cmd.name.lower().replace("_", " ").removeprefix("cmdid").title()

    def _as_dict(self, **kwargs: Any) -> types.JsonDict:
        """Return the attributes of the command as a dict

        Args:
            **kwargs (Any): additional entries for the dict

        Returns:
            types.JsonDict: command as dict
        """
        return {"id": self.cmd, **self._base_dict} | kwargs


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
        update_set: type[SettingId] | type[StatusId],
        action: Action,
        parser: Parser | None = None,
    ) -> None:
        """Constructor

        Args:
            uuid (BleUUID): UUID to write to
            cmd (CmdId): Command ID that is being sent
            update_set (type[SettingId] | type[StatusId]): what are registering / unregistering for?
            action (Action): whether to register or unregister
            parser (Optional[BytesParser], optional): Optional response parser. Defaults to None.
        """
        self.action = action
        self.update_set = update_set
        super().__init__(uuid=uuid, cmd=cmd, parser=parser)


class BleProtoCommand(BleMessage):
    """A BLE command that is sent and received as using the Protobuf protocol"""

    def __init__(
        self,
        uuid: BleUUID,
        feature_id: FeatureId,
        action_id: ActionId,
        response_action_id: ActionId,
        request_proto: type[types.Protobuf],
        response_proto: type[types.Protobuf],
        parser: Parser | None,
        additional_matching_ids: set[ActionId | CmdId] | None = None,
    ) -> None:
        """Constructor

        Args:
            uuid (BleUUID): BleUUID to write to
            feature_id (FeatureId): Feature ID that is being executed
            action_id (ActionId): protobuf specific action ID that is being executed
            response_action_id (ActionId): the action ID that will be in the response to this command
            request_proto (type[types.Protobuf]): the action ID that will be in the response
            response_proto (type[types.Protobuf]): protobuf used to parse received bytestream
            parser (Optional[BytesParser], optional): Optional response parser. Defaults to None.
            additional_matching_ids (Optional[set[Union[ActionId, CmdId]]], optional): Other action ID's to share
                this parser. This is used, for example, if a notification shares the same ID as the
                synchronous response. Defaults to None.. Defaults to None.
        """
        p = parser or Parser()
        p.byte_json_adapter = ByteParserBuilders.Protobuf(response_proto)
        super().__init__(uuid=uuid, parser=p, identifier=response_action_id)
        self.feature_id = feature_id
        self.action_id = action_id
        self.response_action_id = response_action_id
        self.request_proto = request_proto
        self.response_proto = response_proto
        self.additional_matching_ids: set[ActionId | CmdId] = additional_matching_ids or set()
        assert self._parser
        for matching_id in [*self.additional_matching_ids, response_action_id]:
            GlobalParsers.add(matching_id, self._parser)
        GlobalParsers.add_feature_action_id_mapping(self.feature_id, self.response_action_id)

    def _build_data(self, **kwargs: Any) -> bytearray:
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

    def __str__(self) -> str:
        return self.action_id.name.lower().replace("_", " ").removeprefix("actionid").title()

    def _as_dict(self, **kwargs: Any) -> types.JsonDict:
        """Return the attributes of the command as a dict

        Args:
            **kwargs (Any): additional entries for the dict

        Returns:
            types.JsonDict: command as dict
        """
        return {"id": self.action_id, "feature_id": self.feature_id, **self._base_dict} | kwargs


def ble_write_command(
    uuid: BleUUID,
    cmd: CmdId,
    param_builder: BytesBuilder | None = None,
    parser: Parser | None = None,
    rules: MessageRules = MessageRules(),
) -> Callable:
    """Decorator to build and encapsulate a BleWriteCommand in a Callable

    Args:
        uuid (BleUUID): UUID to write to
        cmd (CmdId): command identifier
        param_builder (BytesBuilder | None, optional): builds bytes from params. Defaults to None.
        parser (Parser | None, optional): response parser to parse received bytes. Defaults to None.
        rules (MessageRules): rules this Message must obey. Defaults to MessageRules().

    Returns:
        Callable: built callable to perform operation
    """
    message = BleWriteCommand(uuid, cmd, param_builder, parser)

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return await instance._communicator._send_ble_message(message, rules, **(await wrapped(**kwargs) or kwargs))

    return wrapper


def ble_read_command(uuid: BleUUID, parser: Parser) -> Callable:
    """Decorator to build a BleReadCommand and wrapper to execute it

    Args:
        uuid (BleUUID):  BleUUID to read from
        parser (Parser): the parser that will parse the received bytestream into a JSON dict

    Returns:
        Callable: Generated method to perform command
    """
    message = BleReadCommand(uuid, parser)

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return await instance._communicator._read_ble_characteristic(message, **(await wrapped(**kwargs) or kwargs))

    return wrapper


def ble_register_command(
    uuid: BleUUID,
    cmd: CmdId,
    update_set: type[SettingId] | type[StatusId],
    action: RegisterUnregisterAll.Action,
    parser: Parser | None = None,
) -> Callable:
    """Decorator to build a RegisterUnregisterAll command and wrapper to execute it

    Args:
        uuid (BleUUID): UUID to write to
        cmd (CmdId): Command ID that is being sent
        update_set (type[SettingId] | type[StatusId]): set of ID's being registered for
        action (Action): whether to register or unregister
        parser (Parser, optional): Optional response parser. Defaults to None.

    Returns:
        Callable: Generated method to perform command
    """
    message = RegisterUnregisterAll(uuid, cmd, update_set, action, parser)

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return await instance._communicator._send_ble_message(message, **(await wrapped(**kwargs) or kwargs))

    return wrapper


def ble_proto_command(
    uuid: BleUUID,
    feature_id: FeatureId,
    action_id: ActionId,
    response_action_id: ActionId,
    request_proto: type[types.Protobuf],
    response_proto: type[types.Protobuf],
    parser: Parser | None = None,
    additional_matching_ids: set[ActionId | CmdId] | None = None,
) -> Callable:
    """Decorator to build a BLE Protobuf command and wrapper to execute it

    Args:
        uuid (BleUUID): BleUUID to write to
        feature_id (FeatureId): Feature ID that is being executed
        action_id (ActionId): protobuf specific action ID that is being executed
        response_action_id (ActionId): the action ID that will be in the response to this command
        request_proto (type[types.Protobuf]): the action ID that will be in the response
        response_proto (type[types.Protobuf]): protobuf used to parse received bytestream
        parser (Parser | None, optional): Response parser to transform received Protobuf bytes. Defaults to None.
        additional_matching_ids (Optional[set[Union[ActionId, CmdId]]], optional): Other action ID's to share
            this parser. This is used, for example, if a notification shares the same ID as the
            synchronous response. Defaults to None.

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
        parser,
        additional_matching_ids,
    )

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return await instance._communicator._send_ble_message(message, **(await wrapped(**kwargs) or kwargs))

    return wrapper


@dataclass
class BleAsyncResponse:
    """A BLE protobuf response that is not associated with any message.

    Args:
        feature_id (FeatureId): Feature ID that response corresponds to
        action_id (ActionId): Action ID that response corresponds to
    """

    feature_id: FeatureId
    action_id: ActionId
    parser: Parser

    def __str__(self) -> str:
        return self.action_id.name.lower().replace("_", " ").removeprefix("actionid").title()


class BuilderProtocol(Protocol):
    """Protocol definition of data building methods"""

    def __call__(self, **kwargs: Any) -> bytearray:  # noqa: D102
        ...


class BleSettingFacade(Generic[ValueType]):
    """Wrapper around BleSetting since a BleSetting's message definition changes based on how it is being operated on.

    Args:
        communicator (GoProBle): BLE communicator that will operate on this object.
        identifier (SettingId): Setting Identifier
        parser_builder (QueryParserType): Parses responses from bytes and builds requests to bytes.
    """

    SETTER_UUID: Final[BleUUID] = GoProUUIDs.CQ_SETTINGS
    READER_UUID: Final[BleUUID] = GoProUUIDs.CQ_QUERY

    class BleSettingMessageBase(BleMessage):
        """Actual BLE Setting Message that is wrapped by the facade.

        Args:
            uuid (BleUUID): UUID to access this setting.
            identifier (SettingId | QueryCmdId): How responses to operations on this message will be identified.
            setting_id: (SettingId): Setting identifier. May match identifier in some cases.
            builder (BuilderProtocol): Build request bytes from the current message.
        """

        def __init__(
            self, uuid: BleUUID, identifier: SettingId | QueryCmdId, setting_id: SettingId, builder: BuilderProtocol
        ) -> None:
            self._build = builder
            self._setting_id = setting_id
            super().__init__(uuid, identifier, None)  # type: ignore

        def _build_data(self, **kwargs: Any) -> bytearray:
            return self._build(**kwargs)

        def _as_dict(self, **kwargs: Any) -> types.JsonDict:
            d = {"id": self._identifier, "setting_id": self._setting_id, **self._base_dict} | kwargs
            return d

    def __init__(self, communicator: GoProBle, identifier: SettingId, parser_builder: QueryParserType) -> None:
        # TODO abstract this
        parser = Parser[types.CameraState]()
        if isinstance(parser_builder, construct.Construct):
            parser.byte_json_adapter = ByteParserBuilders.Construct(parser_builder)
        elif isinstance(parser_builder, BytesParserBuilder):
            parser.byte_json_adapter = parser_builder
        elif issubclass(parser_builder, GoProIntEnum):
            parser.byte_json_adapter = ByteParserBuilders.GoProEnum(parser_builder)
        else:
            raise TypeError(f"Unexpected {parser_builder=}")
        GlobalParsers.add(identifier, parser)

        self._identifier = identifier
        self._builder = parser.byte_json_adapter
        self._communicator = communicator

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data

        Args:
            cmd (QueryCmdId): query command

        Returns:
            bytearray: built data
        """
        return bytearray([cmd.value, int(self._identifier)])

    async def set(self, value: ValueType) -> GoProResp[None]:
        """Set the value of the setting.

        Args:
            value (ValueType): The argument to use to set the setting value.

        Returns:
            GoProResp: Status of set
        """

        def _build_data(**kwargs: Any) -> bytearray:
            # Special case. Can't use _send_query
            data = bytearray([int(self._identifier)])
            try:
                param = self._builder.build(kwargs["value"])
                data.extend([len(param), *param])
            except IndexError:
                pass
            return data

        message = BleSettingFacade.BleSettingMessageBase(
            BleSettingFacade.SETTER_UUID,
            self._identifier,
            self._identifier,
            lambda **_: _build_data(value=value),
        )
        return await self._communicator._send_ble_message(message)

    async def get_value(self) -> GoProResp[ValueType]:
        """Get the settings value.

        Returns:
            GoProResp: settings value
        """
        message = BleSettingFacade.BleSettingMessageBase(
            BleSettingFacade.READER_UUID,
            QueryCmdId.GET_SETTING_VAL,
            self._identifier,
            lambda **_: self._build_cmd(QueryCmdId.GET_SETTING_VAL),
        )
        return await self._communicator._send_ble_message(message)

    async def get_name(self) -> GoProResp[str]:
        """Get the settings name.

        Raises:
            NotImplementedError: This isn't implemented on the camera
        """
        raise NotImplementedError("Not implemented on camera!")

    async def get_capabilities_values(self) -> GoProResp[list[ValueType]]:
        """Get currently supported settings capabilities values.

        Returns:
            GoProResp: settings capabilities values
        """
        message = BleSettingFacade.BleSettingMessageBase(
            BleSettingFacade.READER_UUID,
            QueryCmdId.GET_CAPABILITIES_VAL,
            self._identifier,
            lambda **_: self._build_cmd(QueryCmdId.GET_CAPABILITIES_VAL),
        )
        return await self._communicator._send_ble_message(message)

    async def get_capabilities_names(self) -> GoProResp[list[str]]:
        """Get currently supported settings capabilities names.

        Raises:
            NotImplementedError: This isn't implemented on the camera
        """
        raise NotImplementedError("Not implemented on camera!")

    async def register_value_update(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Register for asynchronous notifications when a given setting ID's value updates.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Current value of respective setting ID
        """
        message = BleSettingFacade.BleSettingMessageBase(
            BleSettingFacade.READER_UUID,
            QueryCmdId.REG_SETTING_VAL_UPDATE,
            self._identifier,
            lambda **_: self._build_cmd(QueryCmdId.REG_SETTING_VAL_UPDATE),
        )
        if (response := await self._communicator._send_ble_message(message)).ok:
            self._communicator.register_update(callback, self._identifier)
        return response

    async def unregister_value_update(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Stop receiving notifications when a given setting ID's value updates.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Status of unregister
        """
        message = BleSettingFacade.BleSettingMessageBase(
            BleSettingFacade.READER_UUID,
            QueryCmdId.UNREG_SETTING_VAL_UPDATE,
            self._identifier,
            lambda **_: self._build_cmd(QueryCmdId.UNREG_SETTING_VAL_UPDATE),
        )
        if (response := await self._communicator._send_ble_message(message)).ok:
            self._communicator.unregister_update(callback, self._identifier)
        return response

    async def register_capability_update(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Register for asynchronous notifications when a given setting ID's capabilities update.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Current capabilities of respective setting ID
        """
        message = BleSettingFacade.BleSettingMessageBase(
            BleSettingFacade.READER_UUID,
            QueryCmdId.REG_CAPABILITIES_UPDATE,
            self._identifier,
            lambda **_: self._build_cmd(QueryCmdId.REG_CAPABILITIES_UPDATE),
        )
        if (response := await self._communicator._send_ble_message(message)).ok:
            self._communicator.unregister_update(callback, self._identifier)
        return response

    async def unregister_capability_update(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Stop receiving notifications when a given setting ID's capabilities change.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Status of unregister
        """
        message = BleSettingFacade.BleSettingMessageBase(
            BleSettingFacade.READER_UUID,
            QueryCmdId.UNREG_CAPABILITIES_UPDATE,
            self._identifier,
            lambda **_: self._build_cmd(QueryCmdId.UNREG_CAPABILITIES_UPDATE),
        )
        if (response := await self._communicator._send_ble_message(message)).ok:
            self._communicator.unregister_update(callback, self._identifier)
        return response

    def __str__(self) -> str:
        return str(self._identifier).lower().replace("_", " ").title()


class BleStatusFacade(Generic[ValueType]):
    """Wrapper around BleStatus since a BleStatus's message definition changes based on how it is being operated on.

    Args:
        communicator (GoProBle): BLE communicator that will operate on this object.
        identifier (StatusId): Status identifier
        parser (QueryParserType): Parser responses from bytes

    Raises:
        TypeError: Attempted to pass an invalid parser type
    """

    UUID: Final[BleUUID] = GoProUUIDs.CQ_QUERY

    class BleStatusMessageBase(BleMessage):
        """An individual camera status that is interacted with via BLE.

        Args:
            uuid (BleUUID): UUID to access this status.
            identifier (StatusId | QueryCmdId): How responses to operations on this message will be identified.
            status_id (StatusId): Status identifier. May match identifier in some cases.
            builder (Callable[[Any], bytearray]): Build request bytes from the current message.
        """

        def __init__(
            self,
            uuid: BleUUID,
            identifier: StatusId | QueryCmdId,
            status_id: StatusId,
            builder: Callable[[Any], bytearray],
        ) -> None:
            self._build = builder
            self._status_id = status_id
            super().__init__(uuid, identifier, None)  # type: ignore

        def _build_data(self, **kwargs: Any) -> bytearray:
            return self._build(self, **kwargs)

        def _as_dict(self, **kwargs: Any) -> types.JsonDict:
            return {"id": self._identifier, "status_id": self._status_id, **self._base_dict} | kwargs

    def __init__(self, communicator: GoProBle, identifier: StatusId, parser: QueryParserType) -> None:
        # TODO abstract this
        parser_builder = Parser[types.CameraState]()
        # Is it a protobuf enum?
        if isinstance(parser, construct.Construct):
            parser_builder.byte_json_adapter = ByteParserBuilders.Construct(parser)
        elif isinstance(parser, BytesParserBuilder):
            parser_builder.byte_json_adapter = parser
        elif issubclass(parser, GoProIntEnum):
            parser_builder.byte_json_adapter = ByteParserBuilders.GoProEnum(parser)
        else:
            raise TypeError(f"Unexpected {parser_builder=}")
        GlobalParsers.add(identifier, parser_builder)

        self._communicator = communicator
        self._identifier = identifier

    def __str__(self) -> str:
        return str(self._identifier).lower().replace("_", " ").title()

    async def get_value(self) -> GoProResp[ValueType]:
        """Get the current value of a status.

        Returns:
            GoProResp: current status value
        """
        message = BleStatusFacade.BleStatusMessageBase(
            BleStatusFacade.UUID,
            QueryCmdId.GET_STATUS_VAL,
            self._identifier,
            lambda *args: self._build_cmd(QueryCmdId.GET_STATUS_VAL),
        )
        return await self._communicator._send_ble_message(message)

    async def register_value_update(self, callback: types.UpdateCb) -> GoProResp[ValueType]:
        """Register for asynchronous notifications when a status changes.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: current status value
        """
        message = BleStatusFacade.BleStatusMessageBase(
            BleStatusFacade.UUID,
            QueryCmdId.REG_STATUS_VAL_UPDATE,
            self._identifier,
            lambda *args: self._build_cmd(QueryCmdId.REG_STATUS_VAL_UPDATE),
        )
        if (response := await self._communicator._send_ble_message(message)).ok:
            self._communicator.register_update(callback, self._identifier)
        return response

    async def unregister_value_update(self, callback: types.UpdateCb) -> GoProResp:
        """Stop receiving notifications when status changes.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Status of unregister
        """
        message = BleStatusFacade.BleStatusMessageBase(
            BleStatusFacade.UUID,
            QueryCmdId.UNREG_STATUS_VAL_UPDATE,
            self._identifier,
            lambda *args: self._build_cmd(QueryCmdId.UNREG_STATUS_VAL_UPDATE),
        )
        if (response := await self._communicator._send_ble_message(message)).ok:
            self._communicator.register_update(callback, self._identifier)
        return response

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data for a given status command.

        Args:
            cmd (QueryCmdId): command to build data for

        Returns:
            bytearray: data to send over-the-air
        """
        return bytearray([cmd.value, int(self._identifier)])


######################################################## HTTP #################################################


def http_get_json_command(
    endpoint: str,
    components: list[str] | None = None,
    arguments: list[str] | None = None,
    parser: Parser | None = None,
    identifier: str | None = None,
    rules: MessageRules = MessageRules(),
) -> Callable:
    """Decorator to build and encapsulate a an Http Message that performs a GET to return JSON.

    Args:
        endpoint (str): base endpoint
        components (list[str] | None): Additional path components (i.e. endpoint/{COMPONENT}). Defaults to None.
        arguments (list[str] | None): Any arguments to be appended after endpoint (i.e. endpoint?{ARGUMENT}). Defaults to None.
        parser (Parser | None, optional): Parser to handle received JSON. Defaults to None.
        identifier (types.IdType | None): explicit message identifier. If None, will be generated from endpoint.
        rules (MessageRules): rules this Message must obey. Defaults to MessageRules().

    Returns:
        Callable: built callable to perform operation
    """
    message = HttpMessage(
        endpoint=endpoint, identifier=identifier, components=components, arguments=arguments, parser=parser
    )

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: HttpMessages, _: Any, kwargs: Any) -> GoProResp:
        return await instance._communicator._get_json(message, rules=rules, **(await wrapped(**kwargs) or kwargs))

    return wrapper


def http_get_binary_command(
    endpoint: str,
    components: list[str] | None = None,
    arguments: list[str] | None = None,
    parser: Parser | None = None,
    identifier: str | None = None,
    rules: MessageRules = MessageRules(),
) -> Callable:
    """Decorator to build and encapsulate a an Http Message that performs a GET to return a binary.

    Args:
        endpoint (str): base endpoint
        components (list[str] | None): Additional path components (i.e. endpoint/{COMPONENT}). Defaults to None.
        arguments (list[str] | None): Any arguments to be appended after endpoint (i.e. endpoint?{ARGUMENT}). Defaults to None.
        parser (Parser | None, optional): Parser to handle received JSON. Defaults to None.
        identifier (types.IdType | None): explicit message identifier. If None, will be generated from endpoint.
        rules (MessageRules): rules this Message must obey. Defaults to MessageRules().

    Returns:
        Callable: built callable to perform operation
    """
    message = HttpMessage(
        endpoint=endpoint, identifier=identifier, components=components, arguments=arguments, parser=parser
    )

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: HttpMessages, _: Any, kwargs: Any) -> GoProResp:
        kwargs = await wrapped(**kwargs) or kwargs
        # If no local file was passed, used the file name of the camera file
        kwargs["local_file"] = (
            kwargs.pop("local_file") if "local_file" in kwargs else Path(kwargs["camera_file"].split("/")[-1])
        )
        return await instance._communicator._get_stream(message, rules=rules, **kwargs)

    return wrapper


def http_put_json_command(
    endpoint: str,
    components: list[str] | None = None,
    arguments: list[str] | None = None,
    body_args: list[str] | None = None,
    parser: Parser | None = None,
    identifier: str | None = None,
    rules: MessageRules = MessageRules(),
) -> Callable:
    """Decorator to build and encapsulate a an Http Message that performs a PUT to return JSON.

    Args:
        endpoint (str): base endpoint
        components (list[str] | None): Additional path components (i.e. endpoint/{COMPONENT}). Defaults to None.
        arguments (list[str] | None): Any arguments to be appended after endpoint (i.e. endpoint?{ARGUMENT}). Defaults to None.
        body_args (list[str] | None, optional): Arguments to be added to the body JSON. Defaults to None.
        parser (Parser | None, optional): Parser to handle received JSON. Defaults to None.
        identifier (types.IdType | None): explicit message identifier. If None, will be generated from endpoint.
        rules (MessageRules): rules this Message must obey. Defaults to MessageRules().

    Returns:
        Callable: built callable to perform operation
    """
    message = HttpMessage(
        endpoint=endpoint,
        identifier=identifier,
        body_args=body_args,
        arguments=arguments,
        components=components,
        parser=parser,
    )

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: HttpMessages, _: Any, kwargs: Any) -> GoProResp:
        return await instance._communicator._put_json(message, rules=rules, **(await wrapped(**kwargs) or kwargs))

    return wrapper


class HttpSetting(HttpMessage, Generic[ValueType]):
    """An individual camera setting that is interacted with via Wifi."""

    def __init__(self, communicator: GoProHttp, identifier: SettingId) -> None:
        super().__init__("gopro/camera/setting?setting={setting}&option={option}", identifier)
        self._communicator = communicator
        # Note! It is assumed that BLE and HTTP settings are symmetric so we only add to the communicator's
        # parser in the BLE Setting.

    def __str__(self) -> str:
        return str(self._identifier).lower().replace("_", " ").title()

    def build_url(self, **kwargs: Any) -> str:
        """Build the endpoint from the current arguments

        Args:
            kwargs (Any): run-time arguments

        Returns:
            str: built URL
        """
        return self._endpoint.format(setting=int(self._identifier), option=int(kwargs["value"]))

    async def set(self, value: ValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (ValueType): value to set setting

        Returns:
            GoProResp: Status of set
        """
        response = await self._communicator._get_json(self, value=value)
        response.identifier = self._identifier
        logger.info(Logger.build_log_rx_str(response))
        return response
