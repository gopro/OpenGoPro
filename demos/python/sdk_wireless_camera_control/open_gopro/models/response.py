# responses.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:49 PM

"""Any responses that are returned from GoPro commands."""

from __future__ import annotations

import enum
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Final, Generic, TypeVar

import requests

from open_gopro import types
from open_gopro.api.parsers import JsonParsers
from open_gopro.ble import BleUUID
from open_gopro.constants import (
    ActionId,
    CmdId,
    ErrorCode,
    FeatureId,
    GoProEnum,
    GoProUUIDs,
    QueryCmdId,
    SettingId,
    StatusId,
)
from open_gopro.exceptions import ResponseParseError
from open_gopro.parser_interface import GlobalParsers, Parser
from open_gopro.proto import EnumResultGeneric
from open_gopro.util import pretty_print

logger = logging.getLogger(__name__)

CONT_MASK: Final = 0b10000000
HDR_MASK: Final = 0b01100000
GEN_LEN_MASK: Final = 0b00011111
EXT_13_BYTE0_MASK: Final = 0b00011111


class Header(enum.Enum):
    """Packet Headers."""

    GENERAL = 0b00
    EXT_13 = 0b01
    EXT_16 = 0b10
    RESERVED = 0b11
    CONT = enum.auto()


T = TypeVar("T")


@dataclass
class GoProResp(Generic[T]):
    """The object used to encapsulate all GoPro responses.

    It consists of several common properties / attribute and a data attribute that varies per response.

    >>> gopro = WirelessGoPro()
    >>> await gopro.open()
    >>> response = await (gopro.ble_setting.resolution).get_value()
    >>> print(response)

    Now let's inspect the responses various attributes / properties:

    >>> print(response.status)
    ErrorCode.SUCCESS
    >>> print(response.ok)
    True
    >>> print(response.identifier)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.protocol)
    Protocol.BLE

    Now let's print it's data as (as JSON):

    >>> print(response)
    {
        "id" : "QueryCmdId.GET_SETTING_VAL",
        "status" : "ErrorCode.SUCCESS",
        "protocol" : "Protocol.BLE",
        "data" : {
            "SettingId.RESOLUTION" : "Resolution.RES_4K_16_9",
        },
    }

    Attributes:
        protocol (GoProResp.Protocol): protocol response was received on
        status (ErrorCode): status of response
        data (T): parsed response data
        identifier (types.ResponseType): response identifier, the type of which will vary depending on the response
    """

    class Protocol(enum.Enum):
        """Protocol that Command will be sent on."""

        BLE = "BLE"
        HTTP = "HTTP"

    protocol: GoProResp.Protocol
    status: ErrorCode
    data: T
    identifier: types.ResponseType

    def _as_dict(self) -> dict:
        """Represent the response as dictionary, merging it's data and meta information

        Returns:
            dict: dict representation
        """
        d = {
            "id": self.identifier,
            "status": self.status,
            "protocol": self.protocol,
        }
        if self.data:
            d["data"] = self.data  # type: ignore
        return d

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, GoProEnum):
            return self.identifier == obj
        if isinstance(obj, GoProResp):
            return self.identifier == obj.identifier
        raise TypeError("Equal can only compare GoProResp and types.ResponseType")

    def __str__(self) -> str:
        return pretty_print(self._as_dict())

    def __repr__(self) -> str:
        return f"GoProResp <{str(self.identifier)}>"

    @property
    def ok(self) -> bool:
        """Are there any errors in this response?

        Returns:
            bool: True if the response is ok (i.e. there are no errors), False otherwise
        """
        return self.status in [ErrorCode.SUCCESS, ErrorCode.UNKNOWN]

    @property
    def _is_push(self) -> bool:
        """Was this response an asynchronous push?

        Returns:
            bool: True if yes, False otherwise
        """
        return self.identifier in [
            QueryCmdId.STATUS_VAL_PUSH,
            QueryCmdId.SETTING_VAL_PUSH,
            QueryCmdId.SETTING_CAPABILITY_PUSH,
        ]

    @property
    def _is_query(self) -> bool:
        """Is this response to a settings / status query?

        Returns:
            bool: True if yes, False otherwise
        """
        return isinstance(self.identifier, QueryCmdId)


class RespBuilder(ABC, Generic[T]):
    """Common Response Builder Interface"""

    class _State(enum.Enum):
        """Describes the state of building the response."""

        INITIALIZED = enum.auto()
        ACCUMULATED = enum.auto()
        PARSED = enum.auto()
        ERROR = enum.auto()

    def __init__(self) -> None:
        self._packet: T
        self._status: ErrorCode = ErrorCode.UNKNOWN
        self._state: RespBuilder._State = RespBuilder._State.INITIALIZED
        self._parser: Parser | None = None

    @abstractmethod
    def build(self) -> GoProResp:
        """Build a response

        Returns:
            GoProResp: built response
        """
        raise NotImplementedError


class HttpRespBuilder(RespBuilder[types.JsonDict]):
    """HTTP Response Builder

    This is not intended to be fool proof to use as the user must understand which fields are needed.
    Directors should be created if this needs to be simplified.
    """

    def __init__(self) -> None:
        super().__init__()
        self._endpoint: str
        self._response: types.JsonDict

    def set_response(self, response: types.JsonDict) -> None:
        """Store the JSON data. This is mandatory.

        Args:
            response (types.JsonDict): json data_
        """
        self._response = response

    def set_status(self, status: ErrorCode) -> None:
        """Store the status. This is mandatory.

        Args:
            status (ErrorCode): status of response
        """
        self._status = status

    def set_parser(self, parser: Parser) -> None:
        """Store a parser. This is optional.

        Args:
            parser (Parser): monolithic parser
        """
        self._parser = parser

    def set_endpoint(self, endpoint: str) -> None:
        """Store the endpoint. This is mandatory.

        Args:
            endpoint (str): endpoint of response.
        """
        self._endpoint = endpoint

    def build(self) -> GoProResp:
        """Build the GoPro response from the information accumulated about the HTTP response

        Returns:
            GoProResp: built response
        """
        # Is there a parser for this? Most of them do not have one yet.
        data = self._parser.parse(self._response) if self._parser else self._response
        return GoProResp(
            protocol=GoProResp.Protocol.HTTP,
            status=self._status,
            identifier=self._endpoint,
            data=data,
        )


class RequestsHttpRespBuilderDirector:
    """An abstraction to help simplify using the HTTP Response Builder for requests

    Args:
        response (requests.models.Response): direct response from requests
        parser (Parser | None): parsers to use on the requests response
    """

    def __init__(self, response: requests.models.Response, parser: Parser | None) -> None:

        self.response = response
        self.parser = parser or Parser(json_parser=JsonParsers.LambdaParser(lambda data: data))

    def __call__(self) -> GoProResp:
        """Build the response

        Returns:
            GoProResp: built response
        """
        builder = HttpRespBuilder()
        builder.set_endpoint(self.response.url)
        builder.set_status(ErrorCode.SUCCESS if self.response.ok else ErrorCode.ERROR)
        builder.set_parser(self.parser)
        builder.set_response(self.response.json() if self.response.text else {})
        return builder.build()


class BleRespBuilder(RespBuilder[bytearray]):
    """BLE Response Builder

    This is not intended to be fool proof to use as the user must understand which fields are needed.
    Directors should be created if this needs to be simplified.
    """

    def __init__(self) -> None:
        self._bytes_remaining = 0
        self._uuid: BleUUID
        self._identifier: types.ResponseType
        self._feature_id: FeatureId | None = None
        self._action_id: ActionId | None = None
        super().__init__()

    @property
    def is_response_protobuf(self) -> bool:
        """Is this a protobuf response?

        Returns:
            bool: True if protobuf, False otherwise
        """
        return isinstance(self._identifier, (ActionId, FeatureId))

    def _set_response_meta(self) -> None:
        """Set the identifier based on what is currently known about the packet"""
        # If it's a protobuf command
        identifier = self._packet[0]
        try:
            FeatureId(identifier)
            self._identifier = ActionId(self._packet[1])
        # Otherwise it's a TLV command
        except ValueError:
            if self._uuid is GoProUUIDs.CQ_SETTINGS_RESP:
                self._identifier = SettingId(identifier)
            elif self._uuid is GoProUUIDs.CQ_QUERY_RESP:
                self._identifier = QueryCmdId(identifier)
            elif self._uuid in [GoProUUIDs.CQ_COMMAND_RESP, GoProUUIDs.CN_NET_MGMT_RESP]:
                self._identifier = CmdId(identifier)
            else:
                self._identifier = self._uuid

    def set_parser(self, parser: Parser) -> None:
        """Store a parser. This is optional.

        Args:
            parser (Parser): monolithic parser
        """
        self._parser = parser

    def set_packet(self, packet: bytes) -> None:
        """Store the complete data that comprises the response.

        This is mutually exclusive with accumulate. It is only for responses (such as direct UUID reads) that
        do not follow the packet fragmentation scheme.

        Args:
            packet (bytes): packet to store
        """
        self._packet = bytearray(packet)

    def accumulate(self, data: bytes) -> None:
        """Accumulate BLE byte data.

        This is mutually exclusive with accumulate. It should be used in any case where the response follows
        the packet fragmentation scheme.

        Args:
            data (bytes): byte level BLE data
        """
        buf = bytearray(data)
        if buf[0] & CONT_MASK:
            buf.pop(0)
        else:
            # This is a new packet so start with an empty byte array
            self._packet = bytearray([])
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
        self._packet.extend(buf)
        self._bytes_remaining -= len(buf)

        if self._bytes_remaining < 0:
            logger.error("received too much data. parsing is in unknown state")
        elif self._bytes_remaining == 0:
            self._state = RespBuilder._State.ACCUMULATED

    def set_status(self, status: ErrorCode) -> None:
        """Store the status. This is sometimes optional.

        Args:
            status (ErrorCode): status
        """
        self._status = status

    def set_uuid(self, uuid: BleUUID) -> None:
        """Store the UUID. This is mandatory.

        Args:
            uuid (BleUUID): uuid
        """
        self._uuid = uuid

    @property
    def is_finished_accumulating(self) -> bool:
        """Has the response been completely received?

        Returns:
            bool: True if completely received, False if not
        """
        return self._state is not RespBuilder._State.INITIALIZED

    @property
    def _is_protobuf(self) -> bool:
        """Is this response a protobuf response

        Returns:
            bool: Yes if true, No otherwise
        """
        return isinstance(self._identifier, (ActionId, FeatureId))

    @property
    def _is_direct_read(self) -> bool:
        """Is this response a direct read of a BLE characteristic

        Returns:
            bool: Yes if true, No otherwise
        """
        return isinstance(self._identifier, BleUUID)

    def build(self) -> GoProResp:
        """Parse the accumulated response (either from a BLE bytestream or an HTTP JSON dict).

        Raises:
            NotImplementedError: Parsing for this id is not yet supported
            ResponseParseError: Error when parsing data

        Returns:
            GoProResp: built response
        """
        self._set_response_meta()
        buf = self._packet

        if not self._is_direct_read:  # length byte
            buf.pop(0)
        if self._is_protobuf:  # feature ID byte
            buf.pop(0)

        try:
            parsed: Any = None
            query_type: type[StatusId] | type[SettingId] | StatusId | SettingId | None = None
            # Need to delineate QueryCmd responses between settings and status
            if not self._is_protobuf:
                if isinstance(self._identifier, (SettingId, StatusId)):
                    query_type = self._identifier
                elif isinstance(self._identifier, QueryCmdId):
                    if self._identifier in [
                        QueryCmdId.GET_STATUS_VAL,
                        QueryCmdId.REG_STATUS_VAL_UPDATE,
                        QueryCmdId.UNREG_STATUS_VAL_UPDATE,
                        QueryCmdId.STATUS_VAL_PUSH,
                    ]:
                        query_type = StatusId
                    elif self._identifier is QueryCmdId.GET_SETTING_NAME:
                        raise NotImplementedError
                    else:
                        query_type = SettingId

            # Query (setting get value, status get value, etc.)
            if query_type:
                camera_state: types.CameraState = defaultdict(list)
                self._status = ErrorCode(buf[0])
                buf = buf[1:]
                # Parse all parameters
                while len(buf) != 0:
                    param_id = query_type(buf[0])  # type: ignore
                    param_len = buf[1]
                    buf = buf[2:]
                    # Special case where we register for a push notification for something that does not yet
                    # have a value
                    if param_len == 0:
                        camera_state[param_id] = []
                        continue
                    param_val = buf[:param_len]
                    buf = buf[param_len:]

                    # Add parsed value to response's data dict
                    try:
                        if not (parser := GlobalParsers.get_parser(param_id)):
                            # We don't have defined params for all ID's yet. Just store raw bytes
                            logger.warning(f"No parser defined for {param_id}")
                            camera_state[param_id] = param_val
                            continue
                        # These can be more than 1 value so use a list
                        if self._identifier in [
                            QueryCmdId.GET_CAPABILITIES_VAL,
                            QueryCmdId.REG_CAPABILITIES_UPDATE,
                            QueryCmdId.SETTING_CAPABILITY_PUSH,
                        ]:
                            # Parse using parser from global map and append
                            camera_state[param_id].append(parser.parse(param_val))
                        else:
                            # Parse using parser from map and set
                            camera_state[param_id] = parser.parse(param_val)
                    except ValueError:
                        # This is the case where we receive a value that is not defined in our params.
                        # This shouldn't happen and means the documentation needs to be updated. However, it
                        # isn't functionally critical
                        logger.warning(f"{param_id} does not contain a value {param_val}")
                        camera_state[param_id] = param_val
                parsed = camera_state

            else:  # Commands,  Protobuf, and direct Reads
                if is_cmd := isinstance(self._identifier, CmdId):
                    # All (non-protobuf) commands have a status
                    self._status = ErrorCode(buf[0])
                    buf = buf[1:]
                # Use parser if explicitly passed otherwise get global parser
                if not (parser := self._parser or GlobalParsers.get_parser(self._identifier)) and not is_cmd:
                    error_msg = f"No parser exists for {self._identifier}"
                    logger.error(error_msg)
                    raise ResponseParseError(str(self._identifier), self._packet, msg=error_msg)
                # Parse payload if a parser was found.
                if parser:
                    parsed = parser.parse(buf)

                # TODO make status checking an abstract method of a shared base class
                # Attempt to determine and / or extract status (we already got command status above)
                if self._is_direct_read and len(self._packet):
                    # Assume success on direct reads if there was any data
                    self._status = ErrorCode.SUCCESS
                # Check for result field in protobuf's
                elif self._is_protobuf and "result" in parsed:
                    self._status = (
                        ErrorCode.SUCCESS
                        if parsed.get("result") == EnumResultGeneric.RESULT_SUCCESS
                        else ErrorCode.ERROR
                    )
        except KeyError as e:
            self._state = RespBuilder._State.ERROR
            raise ResponseParseError(str(self._identifier), buf) from e

        # Recursively scrub away parsing artifacts
        self._state = RespBuilder._State.PARSED

        return GoProResp(protocol=GoProResp.Protocol.BLE, status=self._status, data=parsed, identifier=self._identifier)
