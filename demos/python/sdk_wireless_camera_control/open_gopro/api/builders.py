# builders.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""Common functionality across API versions to build commands, settings, and statuses"""

from __future__ import annotations

import enum
import logging
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Final, Generic, TypeVar, Union
from urllib.parse import urlencode

import construct
import wrapt

from open_gopro import types
from open_gopro.api.parsers import ByteParserBuilders, JsonParsers
from open_gopro.communicator_interface import (
    BleMessage,
    BleMessages,
    GoProBle,
    GoProHttp,
    HttpMessage,
    HttpMessages,
    MessageRules,
    RuleSignature,
)
from open_gopro.constants import (
    ActionId,
    BleUUID,
    CmdId,
    FeatureId,
    GoProUUIDs,
    QueryCmdId,
    SettingId,
    StatusId,
)
from open_gopro.enum import GoProEnum
from open_gopro.logger import Logger
from open_gopro.models.general import HttpInvalidSettingResponse
from open_gopro.models.response import GlobalParsers, GoProResp
from open_gopro.parser_interface import BytesBuilder, BytesParserBuilder, Parser
from open_gopro.util import pretty_print

logger = logging.getLogger(__name__)

ValueType = TypeVar("ValueType")
IdType = TypeVar("IdType")

QueryParserType = Union[construct.Construct, type[GoProEnum], BytesParserBuilder]


######################################################## BLE #################################################

T = TypeVar("T")


class BleReadCommand(BleMessage[BleUUID]):
    """A BLE command that reads data from a BleUUID"""

    def __init__(self, uuid: BleUUID, parser: Parser) -> None:
        """Constructor

        Args:
            uuid (BleUUID):  BleUUID to read from
            parser (Parser): the parser that will parse the received bytestream into a JSON dict
        """
        super().__init__(uuid=uuid, parser=parser, identifier=uuid)

    async def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> GoProResp:  # noqa: D102
        logger.info(Logger.build_log_tx_str(pretty_print(self._as_dict())))
        response = await __communicator__._read_characteristic(self._uuid)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def __str__(self) -> str:
        return f"Read {self._uuid.name.lower().replace('_', ' ').title()}"

    def _as_dict(self, *_: Any, **kwargs: Any) -> types.JsonDict:
        """Return the attributes of the command as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            types.JsonDict: command as dict
        """
        return {"id": "Read " + self._uuid.name, **self._base_dict} | kwargs


class BleWriteCommand(BleMessage[CmdId]):
    """A BLE command that writes to a BleUUID and does not accept any parameters"""

    def __init__(
        self,
        uuid: BleUUID,
        cmd: CmdId,
        param_builder: BytesBuilder | None = None,
        parser: Parser | None = None,
        rules: dict[MessageRules, RuleSignature] | None = None,
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
        super().__init__(uuid, parser, cmd, rules)

    async def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> GoProResp:
        """Execute the command by sending it via BLE

        Args:
            __communicator__ (GoProBle): BLE communicator to send the message
            **kwargs (Any): arguments to BLE write command

        Returns:
            GoProResp: Response received via BLE
        """
        logger.info(Logger.build_log_tx_str(pretty_print(self._as_dict(**kwargs))))

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
        response = await __communicator__._send_ble_message(
            self._uuid, data, self._identifier, rules=self._evaluate_rules(**kwargs)
        )
        logger.info(Logger.build_log_rx_str(response))
        return response

    def __str__(self) -> str:
        return self.cmd.name.lower().replace("_", " ").removeprefix("cmdid").title()

    def _as_dict(self, *_: Any, **kwargs: Any) -> types.JsonDict:
        """Return the attributes of the command as a dict

        Args:
            *_ (Any): unused
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
        responded_cmd: QueryCmdId,
        action: Action,
        parser: Parser | None = None,
    ) -> None:
        """Constructor

        Args:
            uuid (BleUUID): UUID to write to
            cmd (CmdId): Command ID that is being sent
            update_set (type[SettingId] | type[StatusId]): what are registering / unregistering for?
            responded_cmd (QueryCmdId): not used currently
            action (Action): whether to register or unregister
            parser (Optional[BytesParser], optional): Optional response parser. Defaults to None.
        """
        self.action = action
        self.update_set = update_set
        self.responded_cmd = responded_cmd
        super().__init__(uuid=uuid, cmd=cmd, parser=parser)

    async def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> GoProResp:  # noqa: D102
        response = await super().__call__(__communicator__)
        if response.ok:
            for update in self.update_set:
                (  # type: ignore
                    __communicator__.register_update
                    if self.action is RegisterUnregisterAll.Action.REGISTER
                    else __communicator__.unregister_update
                )(kwargs["callback"], update)
        return response


class BleProtoCommand(BleMessage[ActionId]):
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
        super().__init__(uuid=uuid, parser=p, identifier=action_id)
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

    async def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> GoProResp:  # noqa: D102
        # The method that will actually build and send the protobuf command
        logger.info(Logger.build_log_tx_str(pretty_print(self._as_dict(**kwargs))))
        data = self.build_data(**kwargs)
        # Allow exception to pass through if protobuf not completely initialized
        response = await __communicator__._send_ble_message(self._uuid, data, self.response_action_id)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def __str__(self) -> str:
        return self.action_id.name.lower().replace("_", " ").removeprefix("actionid").title()

    def _as_dict(self, *_: Any, **kwargs: Any) -> types.JsonDict:
        """Return the attributes of the command as a dict

        Args:
            *_ (Any): unused
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
    rules: dict[MessageRules, RuleSignature] | None = None,
) -> Callable:
    """Factory to build a BleWriteCommand and wrapper to execute it

    Args:
        uuid (BleUUID): BleUUID to write to
        cmd (CmdId): Command ID that is being sent
        param_builder (BytesBuilder, optional): is responsible for building the bytestream to send from the input params
        parser (Parser, optional): the parser that will parse the received bytestream into a JSON dict
        rules (dict[MessageRules, RuleSignature], optional): Rules to be applied to message execution

    Returns:
        Callable: Generated method to perform command
    """
    message = BleWriteCommand(uuid, cmd, param_builder, parser, rules=rules)

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return await message(instance._communicator, **(await wrapped(**kwargs) or kwargs))

    return wrapper


def ble_read_command(uuid: BleUUID, parser: Parser) -> Callable:
    """Factory to build a BleReadCommand and wrapper to execute it

    Args:
        uuid (BleUUID):  BleUUID to read from
        parser (Parser): the parser that will parse the received bytestream into a JSON dict

    Returns:
        Callable: Generated method to perform command
    """
    message = BleReadCommand(uuid, parser)

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return await message(instance._communicator, **(await wrapped(**kwargs) or kwargs))

    return wrapper


def ble_register_command(
    uuid: BleUUID,
    cmd: CmdId,
    update_set: type[SettingId] | type[StatusId],
    responded_cmd: QueryCmdId,
    action: RegisterUnregisterAll.Action,
    parser: Parser | None = None,
) -> Callable:
    """Factory to build a RegisterUnregisterAll command and wrapper to execute it

    Args:
        uuid (BleUUID): UUID to write to
        cmd (CmdId): Command ID that is being sent
        update_set (type[SettingId] | type[StatusId]): set of ID's being registered for
        responded_cmd (QueryCmdId): not currently used
        action (Action): whether to register or unregister
        parser (Parser, optional): Optional response parser. Defaults to None.

    Returns:
        Callable: Generated method to perform command
    """
    message = RegisterUnregisterAll(uuid, cmd, update_set, responded_cmd, action, parser)

    @wrapt.decorator
    async def wrapper(wrapped: Callable, instance: BleMessages, _: Any, kwargs: Any) -> GoProResp:
        return await message(instance._communicator, **(await wrapped(**kwargs) or kwargs))

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
    """Factory to build a BLE Protobuf command and wrapper to execute it

    Args:
        uuid (BleUUID): BleUUID to write to
        feature_id (FeatureId): Feature ID that is being executed
        action_id (ActionId): protobuf specific action ID that is being executed
        response_action_id (ActionId): the action ID that will be in the response to this command
        request_proto (type[types.Protobuf]): the action ID that will be in the response
        response_proto (type[types.Protobuf]): protobuf used to parse received bytestream
        parser (Parser | None, optional): _description_. Defaults to None.
        additional_matching_ids (Optional[set[Union[ActionId, CmdId]]], optional): Other action ID's to share
            this parser. This is used, for example, if a notification shares the same ID as the
            synchronous response. Defaults to None.. Defaults to None.

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
        return await message(instance._communicator, **(await wrapped(**kwargs) or kwargs))

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
        # TODO abstract this
        parser = Parser[types.CameraState]()
        if isinstance(parser_builder, construct.Construct):
            parser.byte_json_adapter = ByteParserBuilders.Construct(parser_builder)
        elif isinstance(parser_builder, BytesParserBuilder):
            parser.byte_json_adapter = parser_builder
        elif issubclass(parser_builder, GoProEnum):
            parser.byte_json_adapter = ByteParserBuilders.GoProEnum(parser_builder)
        else:
            raise TypeError(f"Unexpected {parser_builder=}")
        self._identifier = identifier
        self._builder = parser.byte_json_adapter
        self._communicator = communicator
        BleMessage.__init__(self, uuid=self.SETTER_UUID, parser=parser, identifier=identifier)

    def __str__(self) -> str:
        return str(self._identifier).lower().replace("_", " ").title()

    async def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> Any:
        """Not applicable for a BLE setting

        Args:
            __communicator__ (GoProBle): BLE communicator
            **kwargs (Any): not used

        Raises:
            NotImplementedError: Not applicable
        """
        raise NotImplementedError

    def _as_dict(  # pylint: disable = arguments-differ
        self, identifier: QueryCmdId | SettingId | str, *_: Any, **kwargs: Any
    ) -> types.JsonDict:
        """Return the attributes of the message as a dict

        Args:
            identifier (Union[QueryCmdId, SettingId, str]): identifier of the message for this send
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            types.JsonDict: setting as dict
        """
        return {"id": identifier, **self._base_dict} | kwargs

    async def set(self, value: ValueType) -> GoProResp[None]:
        """Set the value of the setting.

        Args:
            value (ValueType): The argument to use to set the setting value.

        Returns:
            GoProResp: Status of set
        """
        logger.info(Logger.build_log_tx_str(pretty_print(self._as_dict(f"Set {str(self._identifier)}", value=value))))
        # Special case. Can't use _send_query
        data = bytearray([int(self._identifier)])
        try:
            param = self._builder.build(value)
            data.extend([len(param), *param])
        except IndexError:
            pass

        response = await self._communicator._send_ble_message(self.SETTER_UUID, data, self._identifier)
        logger.info(Logger.build_log_rx_str(response))
        return response

    async def _send_query(self, response_id: QueryCmdId) -> GoProResp[types.CameraState | None]:
        """Build the byte data and query setting information

        Args:
            response_id (QueryCmdId): expected identifier of response

        Returns:
            GoProResp: query response
        """
        data = self._build_cmd(response_id)
        logger.info(Logger.build_log_tx_str(pretty_print(self._as_dict(f"{str(response_id)}.{str(self._identifier)}"))))
        response = await self._communicator._send_ble_message(self.READER_UUID, data, response_id)
        logger.info(Logger.build_log_rx_str(response))
        return response

    async def get_value(self) -> GoProResp[ValueType]:
        """Get the settings value.

        Returns:
            GoProResp: settings value
        """
        return await self._send_query(QueryCmdId.GET_SETTING_VAL)  # type: ignore

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
        return await self._send_query(QueryCmdId.GET_CAPABILITIES_VAL)  # type: ignore

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
        if (response := await self._send_query(QueryCmdId.REG_SETTING_VAL_UPDATE)).ok:
            self._communicator.register_update(callback, self._identifier)
        return response  # type: ignore

    async def unregister_value_update(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Stop receiving notifications when a given setting ID's value updates.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Status of unregister
        """
        if (response := await self._send_query(QueryCmdId.UNREG_SETTING_VAL_UPDATE)).ok:
            self._communicator.unregister_update(callback, self._identifier)
        return response  # type: ignore

    async def register_capability_update(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Register for asynchronous notifications when a given setting ID's capabilities update.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Current capabilities of respective setting ID
        """
        if (response := await self._send_query(QueryCmdId.REG_CAPABILITIES_UPDATE)).ok:
            self._communicator.register_update(callback, self._identifier)
        return response  # type: ignore

    async def unregister_capability_update(self, callback: types.UpdateCb) -> GoProResp[None]:
        """Stop receiving notifications when a given setting ID's capabilities change.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Status of unregister
        """
        if (response := await self._send_query(QueryCmdId.UNREG_CAPABILITIES_UPDATE)).ok:
            self._communicator.unregister_update(callback, self._identifier)
        return response  # type: ignore

    def _build_cmd(self, cmd: QueryCmdId) -> bytearray:
        """Build the data to send a settings query over-the-air.

        Args:
            cmd (QueryCmdId): command to build

        Returns:
            bytearray: data to send over-the-air
        """
        ret = bytearray([cmd.value, int(self._identifier)])
        return ret


class BleStatus(BleMessage[StatusId], Generic[ValueType]):
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
        # TODO abstract this
        parser_builder = Parser[types.CameraState]()
        # Is it a protobuf enum?
        if isinstance(parser, construct.Construct):
            parser_builder.byte_json_adapter = ByteParserBuilders.Construct(parser)
        elif isinstance(parser, BytesParserBuilder):
            parser_builder.byte_json_adapter = parser
        elif issubclass(parser, GoProEnum):
            parser_builder.byte_json_adapter = ByteParserBuilders.GoProEnum(parser)
        else:
            raise TypeError(f"Unexpected {parser_builder=}")

        self._communicator = communicator
        BleMessage.__init__(self, uuid=self.UUID, parser=parser_builder, identifier=identifier)
        self._identifier = identifier

    async def __call__(self, __communicator__: GoProBle, **kwargs: Any) -> Any:
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

    async def _send_query(self, response_id: QueryCmdId) -> GoProResp:
        """Build the byte data and query setting information

        Args:
            response_id (QueryCmdId): expected identifier of response

        Returns:
            GoProResp: query response
        """
        data = self._build_cmd(response_id)
        logger.info(Logger.build_log_tx_str(pretty_print(self._as_dict(f"{response_id.name}.{str(self._identifier)}"))))
        response = await self._communicator._send_ble_message(self.UUID, data, response_id)
        logger.info(Logger.build_log_rx_str(response))
        return response

    def _as_dict(  # pylint: disable = arguments-differ
        self,
        identifier: QueryCmdId | SettingId | str,
        *_: Any,
        **kwargs: Any,
    ) -> types.JsonDict:
        """Return the attributes of the command as a dict

        Args:
            identifier (Union[QueryCmdId, SettingId, str]): identifier of the command for this send
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            types.JsonDict: command as dict
        """
        return {"id": identifier, **self._base_dict} | kwargs

    async def get_value(self) -> GoProResp[ValueType]:
        """Get the current value of a status.

        Returns:
            GoProResp: current status value
        """
        return await self._send_query(QueryCmdId.GET_STATUS_VAL)

    async def register_value_update(self, callback: types.UpdateCb) -> GoProResp[ValueType]:
        """Register for asynchronous notifications when a status changes.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: current status value
        """
        if (response := await self._send_query(QueryCmdId.REG_STATUS_VAL_UPDATE)).ok:
            self._communicator.register_update(callback, self._identifier)
        return response

    async def unregister_value_update(self, callback: types.UpdateCb) -> GoProResp:
        """Stop receiving notifications when status changes.

        Args:
            callback (types.UpdateCb): callback to be notified with

        Returns:
            GoProResp: Status of unregister
        """
        if (response := await self._send_query(QueryCmdId.UNREG_STATUS_VAL_UPDATE)).ok:
            self._communicator.unregister_update(callback, self._identifier)
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
        components: list[str] | None = None,
        arguments: list[str] | None = None,
        parser: Parser | None = None,
        identifier: str | None = None,
        rules: dict[MessageRules, RuleSignature] | None = None,
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

    def build_url(self, **kwargs: Any) -> str:
        """Build the URL string from the passed in components and arguments

        Args:
            **kwargs (Any): additional entries for the dict

        Returns:
            str: built URL
        """
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
        return url


class HttpGetJsonCommand(HttpCommand):
    """An HTTP command that performs a GET operation and receives JSON as response"""

    async def __call__(
        self,
        __communicator__: GoProHttp,
        rules: list[MessageRules] | None = None,
        **kwargs: Any,
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
        url = self.build_url(**kwargs)
        # Send to camera
        logger.info(Logger.build_log_tx_str(pretty_print(self._as_dict(**kwargs, endpoint=url))))
        response = await __communicator__._http_get(url, self._parser, rules=rules)
        response.identifier = self._identifier
        logger.info(Logger.build_log_rx_str(response))
        return response


# pylint: disable = missing-class-docstring, arguments-differ
class HttpGetBinary(HttpCommand):
    """An HTTP command that performs a GET operation and receives a binary stream as response"""

    async def __call__(  # type: ignore
        self,
        __communicator__: GoProHttp,
        *,
        camera_file: str,
        local_file: Path | None = None,
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
        local_file = local_file or Path(".") / Path(camera_file).name
        url = self.build_url(path=camera_file)
        logger.info(
            Logger.build_log_tx_str(
                pretty_print(self._as_dict(endpoint=url, camera_file=camera_file, local_file=local_file))
            )
        )
        # Send to camera
        response = await __communicator__._stream_to_file(url, local_file)
        logger.info(
            Logger.build_log_rx_str(pretty_print(self._as_dict(status="SUCCESS", endpoint=url, local_file=local_file)))
        )
        return response


def http_get_json_command(
    endpoint: str,
    components: list[str] | None = None,
    arguments: list[str] | None = None,
    parser: Parser | None = None,
    identifier: str | None = None,
    rules: dict[MessageRules, RuleSignature] | None = None,
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
    async def wrapper(wrapped: Callable, instance: HttpMessages, _: Any, kwargs: Any) -> GoProResp:
        return await message(
            instance._communicator, message._evaluate_rules(**kwargs), **(await wrapped(**kwargs) or kwargs)
        )

    return wrapper


def http_get_binary_command(
    endpoint: str,
    components: list[str] | None = None,
    arguments: list[str] | None = None,
    parser: Parser | None = None,
    identifier: str | None = None,
) -> Callable:
    """Factory to build an HttpGetBinary command and wrapper to execute it

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
    async def wrapper(wrapped: Callable, instance: HttpMessages, _: Any, kwargs: Any) -> GoProResp:
        return await message(instance._communicator, **(await wrapped(**kwargs) or kwargs))

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

    async def __call__(self, __communicator__: GoProHttp, **kwargs: Any) -> Any:
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

    async def set(self, value: ValueType) -> GoProResp:
        """Set the value of the setting.

        Args:
            value (ValueType): value to set setting

        Returns:
            GoProResp: Status of set
        """
        value = value.value if isinstance(value, enum.Enum) else value
        url = self._endpoint.format(int(self._identifier), value)
        logger.info(Logger.build_log_tx_str(pretty_print(self._as_dict(value=value, endpoint=url))))
        # Send to camera
        if response := await self._communicator._http_get(
            url,
            parser=Parser(
                json_parser=JsonParsers.LambdaParser(lambda data: HttpInvalidSettingResponse(**data) if data else data)
            ),
        ):
            response.identifier = self._identifier
            logger.info(Logger.build_log_rx_str(response))
        return response
