# responses.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:49 PM

"""Any responses that are returned from GoPro commands."""

from __future__ import annotations
import enum
import logging
from collections import defaultdict
from typing import Any, Dict, Callable, List, Optional, Union, Iterator, Type, ItemsView, ValuesView, KeysView

import requests
from construct import Construct

from open_gopro.exceptions import ResponseParseError
from open_gopro.constants import (
    ActionId,
    StatusId,
    CmdId,
    ErrorCode,
    SettingId,
    QueryCmdId,
    ResponseType,
    CmdType,
    GoProUUIDs,
)
from open_gopro.util import scrub, pretty_print
from open_gopro.ble import BleUUID
from open_gopro.proto.response_generic_pb import EnumResultGeneric

logger = logging.getLogger(__name__)

BytesParser = Construct
BytesBuilder = Construct
BytesParserBuilder = Construct
StringBuilder = Callable[[Any], str]
JsonParser = Callable[[Dict[str, Dict[Any, BytesParserBuilder]]], Dict[Any, Any]]
Parser = Union[BytesParser, JsonParser]

# Type of data that will be parsed into a GoPro Response.
InputType = Optional[Union[bytearray, Dict[str, Any]]]


ParserMapType = Dict[ResponseType, Parser]

CONT_MASK = 0b10000000
HDR_MASK = 0b01100000
GEN_LEN_MASK = 0b00011111
EXT_13_BYTE0_MASK = 0b00011111

id_map: Dict[BleUUID, Callable] = {
    GoProUUIDs.CQ_SETTINGS_RESP: SettingId,
    GoProUUIDs.CQ_COMMAND_RESP: CmdId,
    GoProUUIDs.CQ_QUERY_RESP: QueryCmdId,
}

response_map: Dict[BleUUID, BleUUID] = {
    GoProUUIDs.CQ_SETTINGS: GoProUUIDs.CQ_SETTINGS_RESP,
    GoProUUIDs.CQ_COMMAND: GoProUUIDs.CQ_COMMAND_RESP,
    GoProUUIDs.CQ_QUERY: GoProUUIDs.CQ_QUERY_RESP,
}


class GoProResp:
    """A flexible object to be used to encapsulate all GoPro responses.

    It can be instantiated with varying levels of information and filled out as more is received.
    The end user should never need to create a response and will only be consuming them.

    It is mostly a wrapper around a JSON-like dictionary (GoProResp.data)
    For example, first send the command and store the response:

    >>> response = ble_setting.resolution.get_value()

    Now let's inspect the responses various attributes / properties:

    >>> print(response.status)
    ErrorCode.SUCCESS
    >>> print(response.is_ok)
    True
    >>> print(response.id)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.cmd)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.uuid)
    GoProUUIDs.CQ_QUERY_RESP

    Now let's print it as (as JSON):

    >>> print(response.data)
    {
        "status": "SUCCESS",
        "id": "GoProUUIDs.CQ_QUERY_RESP::QueryCmdId.GET_SETTING_VAL",
        "SettingId.RESOLUTION": [
            "RES_1080"
        ]
    }
    """

    class _State(enum.Enum):
        """Describes the state of the GoProResp."""

        INITIALIZED = enum.auto()
        ACCUMULATED = enum.auto()
        PARSED = enum.auto()
        ERROR = enum.auto()

    def __init__(
        self,
        parsers: ParserMapType,
        meta: List[ResponseType],
        status: ErrorCode = ErrorCode.SUCCESS,
        raw_packet: Optional[InputType] = None,
    ) -> None:
        """Constructor

        Args:
            parsers (ParserMapType): The map of parsers to be used to build a GoProResp.
            meta (List[ResponseType]): A list of all information known about the response.
            status (ErrorCode): A status if known at time of instantiation. Defaults to ErrorCode.SUCCESS.
            raw_packet (InputType, optional): The unparsed input if known at time of instantiation. Defaults to None.
        """
        # A list describing all of the currently known information about the response.
        # This will be appended to as more information is discovered. The various properties of GoProResp will
        # use this list to parse out their relevant information.
        self._meta: List[ResponseType] = meta
        # Parsers to use to parse this response
        self._parsers = parsers

        self.status: ErrorCode = status
        """Status of the response"""

        # Start with empty list as default value in case we need to append.
        # If we end up not needing a list, we will just overwrite the default
        self.data: Dict[Any, Any] = defaultdict(list)
        """Response data which is really JSON data stored as a dict"""

        self._raw_packet = raw_packet
        self._bytes_remaining = 0
        self._state: GoProResp._State = GoProResp._State.INITIALIZED

    @classmethod
    def _from_write_command(cls, parsers: ParserMapType, uuid: BleUUID, data: bytes) -> "GoProResp":
        """Build a GoProResp from a write command.

        This will discover the expected response BleUUID from the command BleUUID as well as parse the ID
        from the bytestream.

        Args:
            parsers (ParserMapType): parsers to use to parse received data
            uuid (BleUUID): BleUUID that write command is writing to
            data (bytes): bytestream of the command

        Returns:
            GoProResp: created instance
        """
        # Find expected response and ID from the data
        response_uuid = response_map[uuid]
        cmd_id = id_map[response_uuid](data[1])
        meta = [response_uuid, cmd_id]
        # If this is a protobuf command, it also has an action id
        if cmd_id.value >= 0xF0:
            meta.append(ActionId(data[2]))
        return cls(parsers, meta=meta)

    @classmethod
    def _from_read_response(cls, parsers: ParserMapType, uuid: BleUUID, data: bytearray) -> "GoProResp":
        """Build a GoProResp from a read response.

        Args:
            parsers (ParserMapType): parsers to use to parse received data
            uuid (BleUUID): BleUUID that read command was received from
            data (bytearray): received bytestream

        Returns:
            GoProResp: created instance
        """
        resp = cls(parsers, meta=[uuid], status=ErrorCode.SUCCESS, raw_packet=data)
        resp._parse()
        return resp

    @classmethod
    def _from_http_response(cls, parsers: ParserMapType, response: requests.models.Response) -> "GoProResp":
        """Build a GoProResp from an HTTP response from the requests package.

        Args:
            parsers (ParserMapType): parsers to use to parse received data
            response (requests.models.Response): HTTP response

        Returns:
            GoProResp: created instance
        """
        resp = cls(
            parsers,
            meta=[response.request.path_url.strip("/")],
            status=ErrorCode.SUCCESS if response.ok else ErrorCode.ERROR,
            raw_packet=response.json(),
        )
        resp._parse()
        return resp

    def __getitem__(self, key: Any) -> Any:
        return self.data[key]

    def __contains__(self, item: Any) -> bool:
        return item in self.data

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __str__(self) -> str:
        return pretty_print(
            {"status": self.status.name, "id": "::".join([str(x) for x in self._meta]), **self.data}
        )

    def items(self) -> ItemsView[Any, Any]:
        """Pass-through to access data dict's "items" method

        Returns:
            ItemsView[Any, Any]: all of data's keys
        """
        return self.data.items()

    def keys(self) -> KeysView[Any]:
        """Pass-through to access data dict's "keys" method

        Returns:
            ItemsView[Any, Any]: all of data's items
        """
        return self.data.keys()

    def values(self) -> ValuesView[Any]:
        """Pass-through to access data dict's "values" method

        Returns:
            ItemsView[Any, Any]: all of data's values
        """
        return self.data.values()

    @property
    def is_received(self) -> bool:
        """Has the response been completely received?

        Returns:
            bool: True if completely received, False if not
        """
        return self._state is not GoProResp._State.INITIALIZED

    @property
    def is_parsed(self) -> bool:
        """Has the response been successfully parsed?

        Returns:
            bool: True if it has been parsed, False if not
        """
        return self._state is GoProResp._State.PARSED

    @property
    def is_ok(self) -> bool:
        """Are there any errors in this response?

        Returns:
            bool: True if the response is ok (i.e. there are no errors), False otherwise
        """
        return self.status in [ErrorCode.SUCCESS, ErrorCode.UNKNOWN]

    @property
    def id(self) -> ResponseType:
        """Get the identifier of the response.

        Will vary depending on what type of response this is:

        - for a direct BLE read / write to a characteristic, it will be a :py:class:`open_gopro.constants.BleUUID`
        - for a BLE command response, it will be a :py:class:`open_gopro.constants.CmdType`
        - for a BLE setting / status response / update, it will be a :py:class:`open_gopro.constants.SettingId` or :py:class:`open_gopro.constants.StatusId`
        - for an HTTP response, it will be a string of the HTTP endpoint

        Returns:
            ResponseType: the identifier
        """
        return self._meta[-1]

    @property
    def cmd(self) -> Optional[CmdType]:
        """Attempt to get the command ID of the response.

        If the response is not a command response, it won't have a command.

        Returns:
            Optional[CmdType]: Command ID if relevant, otherwise None
        """
        for x in self._meta:
            if isinstance(x, (QueryCmdId, CmdId)):
                return x
        return None

    @property
    def uuid(self) -> Optional[BleUUID]:
        """Attempt to get the BleUUID the response was received on.

        If the response is not a BLE response, it won't have a BleUUID.

        Returns:
            Optional[BleUUID]: BleUUID if relevant, otherwise None
        """
        for x in self._meta:
            if isinstance(x, BleUUID):
                return x
        return None

    @property
    def endpoint(self) -> Optional[str]:
        """Attempt to get the endpoint that response was received from.

        If the response is not an HTTP response, it won't have an endpoint.

        Returns:
            Optional[str]: Endpoint if relevant, otherwise None
        """
        for x in self._meta:
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
        assert isinstance(self._raw_packet, bytearray)
        self._raw_packet.extend(buf)
        self._bytes_remaining -= len(buf)

        if self._bytes_remaining < 0:
            logger.error("received too much data. parsing is in unknown state")
        elif self._bytes_remaining == 0:
            self._state = GoProResp._State.ACCUMULATED

    def _parse(self) -> None:
        """Parse the accumulated response (either from a BLE bytestream or an HTTP JSON dict).

        Raises:
            NotImplementedError: Parsing for this id is not yet supported
            Exception: Unexpected state
            ResponseParseError: Error when parsing data
        """
        # Is this a BLE response?
        if isinstance(self._raw_packet, bytearray):
            buf: bytearray = self._raw_packet

            # Find identifier or see if this is a protobuf or direct read
            is_protobuf = False
            is_direct_read = False
            identifier: Optional[Type[ResponseType]] = None
            if self.uuid == GoProUUIDs.CQ_SETTINGS_RESP:
                self._meta.append(SettingId(buf[0]))
                identifier = SettingId
            elif self.uuid == GoProUUIDs.CQ_QUERY_RESP:
                self._meta.append(QueryCmdId(buf[0]))
                if self.id in [
                    QueryCmdId.GET_SETTING_VAL,
                    QueryCmdId.REG_SETTING_VAL_UPDATE,
                    QueryCmdId.UNREG_SETTING_VAL_UPDATE,
                    QueryCmdId.SETTING_VAL_PUSH,
                    QueryCmdId.SETTING_CAPABILITY_PUSH,
                    QueryCmdId.GET_CAPABILITIES_VAL,
                    QueryCmdId.REG_CAPABILITIES_UPDATE,
                    QueryCmdId.UNREG_CAPABILITIES_UPDATE,
                ]:
                    identifier = SettingId
                elif self.id is QueryCmdId.GET_SETTING_NAME:
                    raise NotImplementedError
                elif self.id in [
                    QueryCmdId.GET_STATUS_VAL,
                    QueryCmdId.REG_STATUS_VAL_UPDATE,
                    QueryCmdId.UNREG_STATUS_VAL_UPDATE,
                    QueryCmdId.STATUS_VAL_PUSH,
                ]:
                    identifier = StatusId
                elif self.id in [QueryCmdId.PROTOBUF_QUERY, SettingId.PROTOBUF_SETTING]:
                    is_protobuf = True
                else:
                    raise Exception("Unhandled parse state")
            else:  # Other UUID's have responses that can be parsed monolithically
                if self.uuid is GoProUUIDs.CQ_COMMAND_RESP:
                    self._meta.append(CmdId(buf[0]))
                    # If this is a protobuf, first get the action ID (after stripping msb)
                    assert self.cmd is not None
                    if self.id == CmdId.PROTOBUF_COMMAND:
                        is_protobuf = True
                else:
                    # This is a direct read from a characteristic
                    is_direct_read = True

            # Additional parsing to add action ID fo protobuf
            if is_protobuf:
                self._meta.append(ActionId(buf[1] & 0x7F))
                buf = buf[1:]  # Pop off action ID

            if not is_direct_read:
                # Pop off ID
                buf = buf[1:]

            try:
                # Parse based on identifier
                if identifier in [SettingId, StatusId]:
                    # Parse all parameters
                    self.status = ErrorCode(buf[0])
                    buf = buf[1:]
                    while len(buf) != 0:
                        param_id = identifier(buf[0])  # type: ignore
                        param_len = buf[1]
                        buf = buf[2:]
                        # Special case where we register for a push notification for something that does not yet
                        # have a value
                        if param_len == 0:
                            self.data[param_id] = []
                            continue
                        param_val = buf[:param_len]
                        buf = buf[param_len:]

                        # Add parsed value to response's data dict
                        try:
                            # These can be more than 1 value so use a list
                            if self.cmd in [
                                QueryCmdId.GET_CAPABILITIES_VAL,
                                QueryCmdId.REG_CAPABILITIES_UPDATE,
                                QueryCmdId.SETTING_CAPABILITY_PUSH,
                            ]:
                                # Parse using parser from map and append
                                # Mypy can't follow that this parser is guarantted to be a ByteParser
                                self.data[param_id].append(self._parsers[param_id].parse(param_val))  # type: ignore
                            else:
                                # Parse using parser from map and set
                                # Mypy can't follow that this parser is guarantted to be a ByteParser
                                self.data[param_id] = self._parsers[param_id].parse(param_val)  # type: ignore
                        except KeyError:
                            # We don't have defined params for all ID's yet. Just store raw bytes
                            logger.warning(f"No parser defined for {param_id}")
                            self.data[param_id] = param_val
                        except ValueError:
                            # This is the case where we receive a value that is not defined in our params.
                            # This shouldn't happen and means the documentation needs to be updated. However, it
                            # isn't functionally critical
                            logger.warning(f"{param_id} does not contain a value {param_val}")
                            self.data[param_id] = param_val
                else:  # Commands,  Protobuf, and direct Reads
                    # Parse payload
                    self.data = self._parsers[self.id].parse(buf)  # type: ignore
                    # Attempt to determine and / or extract status
                    if is_direct_read and len(
                        self._raw_packet
                    ):  # Assume success on direct reads if there was any data
                        self.status = ErrorCode.SUCCESS
                    elif "status" in self.data:  # Check if the response contains a status
                        self.status = self.data["status"]
                    elif "result" in self.data:  # Check for result field in protobuf's
                        self.status = (
                            ErrorCode.SUCCESS
                            if self.data["result"] == EnumResultGeneric.RESULT_SUCCESS
                            else ErrorCode.ERROR
                        )
                    else:
                        self.status = ErrorCode.UNKNOWN
            except KeyError as e:
                self._state = GoProResp._State.ERROR
                raise ResponseParseError(str(self.id), buf) from e

        # Is this an HTTP response?
        elif isinstance(self._raw_packet, dict):
            json_data: Dict[str, Any] = self._raw_packet
            # Is there a parser for this? Most of them do not have one yet.
            self.data = self._parsers[self.id](json_data, self._parsers) if self.id in self._parsers else json_data  # type: ignore
        else:
            raise Exception(
                f"Unexpected data type ({str(type(self._raw_packet))}) when attempting to parse response"
            )

        # Recursively scrub away parsing artifacts
        scrub(self.data, "_io")
        scrub(self.data, "status")
        self._state = GoProResp._State.PARSED
