# responses.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Any responses that are returned from GoPro commands."""

import enum
import json
import logging
from collections import defaultdict
from abc import abstractmethod, ABC
from typing import (
    Any,
    ClassVar,
    Dict,
    Callable,
    List,
    Optional,
    Union,
    Iterator,
    Type,
    ItemsView,
    ValuesView,
    KeysView,
)

import requests
import construct  # For enum
from construct import Struct, FormatField, StringEncoded

from open_gopro.constants import (
    ActionId,
    StatusId,
    UUID,
    CmdId,
    ErrorCode,
    SettingId,
    QueryCmdId,
    ResponseType,
    CmdType,
)
from open_gopro.util import scrub

logger = logging.getLogger(__name__)


# Type of data that will be parsed into a GoPro Response.
InputType = Optional[Union[bytearray, Dict[str, Any]]]


class Parser(ABC):
    """Interface definition for a non-Construct parser to be used by GoProResp for parsing."""

    @abstractmethod
    def parse(self, buf: Any) -> Dict[Any, Any]:
        """Parse any input type into a dict.

        Args:
            buf (InputType): input to parse

        Returns:
            Dict[Any, Any]: parsed output
        """
        raise NotImplementedError


class Builder(ABC):
    """Interface definition for a non-Construct builder to be used by GoProResp for building."""

    @abstractmethod
    def build(self, buf: Any) -> bytearray:
        """Build something into a bytestream.

        Args:
            buf (Any): The thing to build

        Returns:
            bytearray: The build bytestream.
        """
        raise NotImplementedError


class ParserBuilder(Parser, Builder):
    """A class that can both parse and build."""

    ...


FieldBuilder = Callable[..., FormatField]
ConstructType = Union[Struct, construct.Enum, FieldBuilder, StringEncoded]

ParserBuilderType = Union[ParserBuilder, ConstructType]
ParserType = Union[Parser, ParserBuilderType, ConstructType]
BuilderType = Union[Builder, ParserBuilderType, ConstructType]


CONT_MASK = 0b10000000
HDR_MASK = 0b01100000
GEN_LEN_MASK = 0b00011111
EXT_13_BYTE0_MASK = 0b00011111

id_map: Dict[UUID, Callable] = {
    UUID.CQ_SETTINGS_RESP: SettingId,
    UUID.CQ_COMMAND_RESP: CmdId,
    UUID.CQ_QUERY_RESP: QueryCmdId,
}

response_map: Dict[UUID, UUID] = {
    UUID.CQ_SETTINGS: UUID.CQ_SETTINGS_RESP,
    UUID.CQ_COMMAND: UUID.CQ_COMMAND_RESP,
    UUID.CQ_QUERY: UUID.CQ_QUERY_RESP,
}


class GoProResp:
    """A flexible object to be used to encapsulate all GoPro responses.

    It can be instantiated with varying levels of information and filled out as more is received.

    It is mostly a wrapper around a JSON-like dictionary (GoProResp.data)

    >>> response = ble_setting.resolution.get_value()
    >>> print(response.status)
    ErrorCode.SUCCESS
    >>> print(response.is_ok)
    True
    >>> print(response.id)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.cmd)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.uuid)
    UUID.CQ_QUERY_RESP
    >>> print(response.data)
    {
        "status": "SUCCESS",
        "id": "UUID.CQ_QUERY_RESP::QueryCmdId.GET_SETTING_VAL",
        "SettingId.RESOLUTION": [
            "RES_1080"
        ]
    }

    Args:
        info (List[ResponseType]): A list of all information known about the response.
        status (ErrorCode, optional): A status if known at time of instantiation. Defaults to ErrorCode.SUCCESS.
        raw_packet (InputType, optional): The unparsed input if known at time of instantiation. Defaults to None.
    """

    # To be filled out when settings / statuses are defined
    parser_map: ClassVar[Dict[ResponseType, ParserType]] = {}

    class State(enum.Enum):
        """Describes the state of the GoProResp."""

        INITIALIZED = enum.auto()
        ACCUMULATED = enum.auto()
        PARSED = enum.auto()

    def __init__(
        self,
        info: List[ResponseType],
        status: ErrorCode = ErrorCode.SUCCESS,
        raw_packet: InputType = None,
    ) -> None:
        self._info: List[ResponseType] = info
        """A list describing all of the currently known information about the response.

        This will be appended to as more information is discovered. The various properties of GoProResp will
        use this list to parse out their relevant information.
        """

        self.status: ErrorCode = status
        """Status of the response"""

        # Start with empty list as default value in case we need to append.
        # If we end up not needing a list, we will just overwrite the default
        self.data: Dict[Any, Any] = defaultdict(list)
        """Response data which is really JSON data stored as a dict"""

        self._raw_packet = raw_packet
        self._bytes_remaining = 0
        self._state = GoProResp.State.INITIALIZED

    @classmethod
    def from_write_command(cls, uuid: UUID, data: bytes) -> "GoProResp":
        """Build a GoProResp from a write command.

        This will discover the expected response UUID from the command UUID as well as parse the ID
        from the bytestream.

        Args:
            uuid (UUID): UUID that write command is writing to
            data (bytes): bytestream of the command

        Returns:
            GoProResp: created instance
        """
        # Find expected response and ID from the data
        response_uuid = response_map[uuid]
        cmd_id = id_map[response_uuid](data[1])
        info = [response_uuid, cmd_id]
        # If this is a protobuf command, it also has an action id
        if cmd_id.value >= 0xF0:
            info.append(ActionId(data[2]))
        return cls(info=info)

    @classmethod
    def from_read_response(cls, uuid: UUID, data: bytearray) -> "GoProResp":
        """Build a GoProResp from a read response.

        Args:
            uuid (UUID): UUID that read command was received from
            data (bytes): received bytestream

        Returns:
            GoProResp: created instance
        """
        resp = cls(info=[uuid], status=ErrorCode.SUCCESS, raw_packet=data)
        resp._parse()
        return resp

    @classmethod
    def from_http_response(cls, response: requests.models.Response) -> "GoProResp":
        """Build a GoProResp from an HTTP response from the requests package.

        Args:
            response (requests.models.Response): HTTP response

        Returns:
            GoProResp: created instance
        """
        resp = cls(
            info=[response.request.path_url.strip("/")],
            status=ErrorCode.SUCCESS if response.ok else ErrorCode.ERROR,
            raw_packet=response.json(),
        )
        resp._parse()
        return resp

    def __getitem__(self, key: Any) -> Any:  # pylint: disable=missing-return-doc
        return self.data[key]

    def __contains__(self, item: Any) -> bool:  # pylint: disable=missing-return-doc
        return item in self.data

    def __iter__(self) -> Iterator:  # pylint: disable=missing-return-doc
        return iter(self.data)

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return json.dumps(
            {
                "status": self.status.name,
                "id": "::".join([str(x) for x in self._info]),
                **{str(k): v for k, v in self.data.items()},
            },
            default=str,
            indent=4,
        )

    def items(self) -> ItemsView[Any, Any]:
        """Access data dict's "items" method

        Returns:
            ItemsView[Any, Any]: [description]
        """
        return self.data.items()

    def keys(self) -> KeysView[Any]:
        """Access data dict's "keys" method

        Returns:
            ItemsView[Any, Any]: [description]
        """
        return self.data.keys()

    def values(self) -> ValuesView[Any]:
        """Access data dict's "values" method

        Returns:
            ItemsView[Any, Any]: [description]
        """
        return self.data.values()

    @property
    def is_received(self) -> bool:
        """Has the response been completely received?

        Returns:
            bool: True if completely received, False if not
        """
        return self._state is GoProResp.State.ACCUMULATED or self._state is GoProResp.State.PARSED

    @property
    def is_parsed(self) -> bool:
        """Has the response been successfully parsed?

        Returns:
            bool: True if it has been parsed, False if not
        """
        return self._state is GoProResp.State.PARSED

    @property
    def is_ok(self) -> bool:
        """Are there any errors in this response?

        Returns:
            bool: True if the response is ok (i.e. there are no errors), False otherwise
        """
        return self.status is ErrorCode.SUCCESS

    @property
    def id(self) -> ResponseType:
        """Get the identifier of the response.

        Will vary depending on what type of response this is:

        - for a direct BLE read / write to a characteristic, it will be a :py:class:`open_gopro.constants.UUID`
        - for a BLE command response, it will be a :py:class:`open_gopro.constants.CmdType`
        - for a BLE setting / status response / update, it will be a :py:class:`open_gopro.constants.SettingId` or :py:class:`open_gopro.constants.StatusId`
        - for an HTTP response, it will be a string of the HTTP endpoint

        Returns:
            ResponseType: the identifier
        """
        return self._info[-1]

    @property
    def cmd(self) -> Optional[CmdType]:
        """Attempt to get the command ID of the response.

        If the response is not a command response, it won't have a command.

        Returns:
            Optional[CmdType]: Command ID if relevant, otherwise None
        """
        for x in self._info:
            if isinstance(x, (QueryCmdId, CmdId)):
                return x  # type: ignore
        return None

    @property
    def uuid(self) -> Optional[UUID]:
        """Attempt to get the UUID the response was received on.

        If the response is not a BLE response, it won't have a UUID.

        Returns:
            Optional[UUID]: UUID if relevant, otherwise None
        """
        for x in self._info:
            if isinstance(x, UUID):
                return x
        return None

    @property
    def endpoint(self) -> Optional[str]:
        """Attempt to get the endpoint that response was received from.

        If the response is not an HTTP response, it won't have an endpoint.

        Returns:
            Optional[str]: Endpoint if relevant, otherwise None
        """
        for x in self._info:
            if isinstance(x, str):
                return x
        return None

    @property
    def flatten(self) -> Any:
        """Attempt to flatten / simplify the JSON response (GoProResp.data).

        - If there is only one entry in the JSON dict and it is a single value, return the value
        - If there is only one entry in the JSON dict and it is a list of values, return the list
        - Otherwise, just return the JSON dict

        Returns:
            Any: A single value, a list of values, or the JSON dict
        """
        values = list(self.data.values())
        if len(values) == 1 and type(values[0] not in [list, dict]):
            return values[0]

        if len(values) == 1 and type(values[0] is list):
            return values

        return self.data

    # to be @overload'ed if anything besides BLE notifications need to be accumulated
    def _accumulate(self, data: bytes) -> None:
        """Accumulate BLE byte data.

        If there is no more data left to accumulate, the bytestream will be parsed.

        Args:
            data (bytes): byte level BLE data
        """

        class Header(enum.Enum):
            """Packet Headers."""

            GENERAL = 0b00
            EXT_13 = 0b01
            EXT_16 = 0b10
            RESERVED = 0b11
            CONT = enum.auto()

        buf = bytearray(data)
        if buf[0] & CONT_MASK:
            buf.pop(0)
        else:
            # This is a new packet so start with an empty byte array
            self._raw_packet = bytearray([])
            hdr = Header((buf[0] & HDR_MASK) >> 5)
            if hdr is Header.GENERAL:
                self._bytes_remaining = buf[0] & GEN_LEN_MASK
                buf = buf[1:]
            elif hdr is Header.EXT_13:
                self._bytes_remaining = ((buf[0] & EXT_13_BYTE0_MASK) << 8) + buf[1]
                buf = buf[2:]
            elif hdr is Header.EXT_16:
                self._bytes_remaining = (buf[1] << 8) + buf[2]
                buf = buf[3:]

        # Append payload to buffer and update remaining / complete
        self._raw_packet.extend(buf)  # type: ignore
        self._bytes_remaining -= len(buf)

        if self._bytes_remaining < 0:
            logger.error("received too much data. parsing is in unknown state")
        elif self._bytes_remaining == 0:
            self._state = GoProResp.State.ACCUMULATED
            self._parse()

    def _parse(self) -> None:
        """Parse the accumulated response (either from a BLE bytestream or an HTTP JSON dict)."""
        # Is this a BLE response?
        if isinstance(self._raw_packet, bytearray):
            buf: bytearray = self._raw_packet  # type: ignore

            # UUID's whose responses contain multiple parameters to parse
            if self.uuid in [UUID.CQ_QUERY_RESP, UUID.CQ_SETTINGS_RESP]:
                identifier: Optional[Union[Type[SettingId], Type[StatusId]]] = None
                if self.uuid is UUID.CQ_SETTINGS_RESP:
                    self._info.append(SettingId(buf[0]))
                    identifier = SettingId
                else:
                    self._info.append(QueryCmdId(buf[0]))
                    if self.id in [
                        QueryCmdId.GET_SETTING_VAL,
                        QueryCmdId.REG_SETTING_VAL_UPDATE,
                        QueryCmdId.SETTING_VAL_PUSH,
                        QueryCmdId.SETTING_CAPABILITY_PUSH,
                        QueryCmdId.GET_CAPABILITIES_VAL,
                        QueryCmdId.REG_CAPABILITIES_UPDATE,
                    ]:
                        identifier = SettingId
                    elif self.id is QueryCmdId.GET_SETTING_NAME:
                        raise NotImplementedError
                    elif self.id in [
                        QueryCmdId.GET_STATUS_VAL,
                        QueryCmdId.REG_STATUS_VAL_UPDATE,
                        QueryCmdId.STATUS_VAL_PUSH,
                    ]:
                        identifier = StatusId

                if identifier is None:
                    raise Exception("Identifier is unexpectedly None")

                # Parse all parameters
                self.status = ErrorCode(buf[1])
                buf = buf[2:]
                while len(buf) != 0:
                    param_id = identifier(buf[0])
                    param_len = buf[1]
                    buf = buf[2:]

                    # Special case where we register for a push notification for something that does not yet
                    # have a value
                    if param_len == 0:
                        self.data[param_id] = []
                        continue

                    param_val = buf[:param_len]
                    buf = buf[param_len:]

                    try:
                        # These can be more than 1 value so use a list
                        if self.cmd in [
                            QueryCmdId.GET_CAPABILITIES_VAL,
                            QueryCmdId.REG_CAPABILITIES_UPDATE,
                            QueryCmdId.SETTING_CAPABILITY_PUSH,
                        ]:
                            # Parse using parser from map and append
                            self.data[param_id].append(GoProResp.parser_map[param_id].parse(param_val))  # type: ignore
                        else:
                            # Parse using parser from map and set
                            self.data[param_id] = GoProResp.parser_map[param_id].parse(param_val)  # type: ignore
                    except KeyError:
                        # We don't have defined params for all ID's yet.
                        logger.warning(f"No parser defined for {param_id}")
                        self.data[param_id] = param_val

            else:  # Other UUID's have responses that can be parsed monolithically
                if self.uuid is UUID.CQ_COMMAND_RESP:
                    self._info.append(CmdId(buf[0]))
                    # If this is a protobuf, first get the action ID (after stripping msb)
                    if self.cmd.value >= 0xF0:  # type: ignore
                        self._info.append(ActionId(buf[1] & 0x7F))
                        buf = buf[1:]
                    buf = buf[1:]

                self.data = GoProResp.parser_map[self.id].parse(buf)  # type: ignore
                self.status = ErrorCode(int(self.data["status"])) if "status" in self.data else self.status  # type: ignore
                scrub(self.data, "status")

        # Is this an HTTP response?
        elif isinstance(self._raw_packet, dict):
            json_data: Dict[str, Any] = self._raw_packet  # type: ignore
            # Is there a parser for this? Most of them do not have one.
            try:
                self.data = GoProResp.parser_map[self.id].parse(json_data)  # type: ignore
            except KeyError:
                self.data = json_data
        else:
            raise Exception(
                f"Unexpected data type ({str(type(self._raw_packet))}) when attempting to parse response"
            )

        # Recursively scrub away parsing artifacts
        scrub(self.data, "_io")
        self._state = GoProResp.State.PARSED
