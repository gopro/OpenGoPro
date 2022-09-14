# responses.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:49 PM

"""Any responses that are returned from GoPro commands."""

from __future__ import annotations
import enum
import logging
from collections import defaultdict
from typing import (
    Any,
    Optional,
    Union,
    Iterator,
    ItemsView,
    ValuesView,
    KeysView,
    Final,
    ClassVar,
    Protocol,
    TypeVar,
)

import requests

from open_gopro.exceptions import ResponseParseError
from open_gopro.constants import (
    ActionId,
    FeatureId,
    GoProEnum,
    StatusId,
    CmdId,
    ErrorCode,
    SettingId,
    QueryCmdId,
    ResponseType,
    CmdType,
    GoProUUIDs,
)
from open_gopro.util import scrub, jsonify
from open_gopro.ble import BleUUID
from open_gopro.proto.response_generic_pb2 import EnumResultGeneric

logger = logging.getLogger(__name__)

CONT_MASK: Final = 0b10000000
HDR_MASK: Final = 0b01100000
GEN_LEN_MASK: Final = 0b00011111
EXT_13_BYTE0_MASK: Final = 0b00011111

T_co = TypeVar("T_co", covariant=True)


class BytesParser(Protocol[T_co]):
    """Base bytes parser protocol definition"""

    def parse(self, data: bytes) -> T_co:
        """Parse byte data into desired object

        # noqa: DAR202

        Args:
            data (bytes): data to parse

        Returns:
            T_co: parsed object
        """


class CustomBytesParser(BytesParser[dict]):
    """Bytes parser protocol to be used by non-construct parsers"""

    def parse(self, data: bytes) -> dict:
        """Parse byte data into dict

        # noqa: DAR202

        Args:
            data (bytes): data to parse

        Returns:
            dict: parsed dict
        """


class BytesBuilder(Protocol):
    """Base bytes serializer protocol definition"""

    def build(self, obj: Any) -> bytes:
        """Build bytestream from object

        # noqa: DAR202

        Args:
            obj (Any): object to serialize

        Returns:
            bytes: serialized bytestream
        """


class BytesParserBuilder(BytesParser[T_co], BytesBuilder):
    """Class capable of both building / parsing bytes to / from object"""

    def parse(self, data: bytes) -> T_co:
        """Parse byte data into dict

        # noqa: DAR202

        Args:
            data (bytes): data to parse

        Returns:
            T_co: parsed dict
        """

    def build(self, obj: Any) -> bytes:
        """Build bytestream from object

        # noqa: DAR202

        Args:
            obj (Any): object to serialize

        Returns:
            bytes: serialized bytestream
        """


class JsonParser(Protocol):
    """Protocol definition for a JSON parser"""

    @classmethod
    def parse(cls, json: dict[str, Any]) -> dict:
        """Parse JSON into a proprietary dict

        # noqa: DAR202

        Args:
            json (dict[str, Any]): input JSON

        Returns:
            dict: output parsed dict
        """


ParserType = Union[BytesParser, JsonParser]
ParserMapType = dict[ResponseType, ParserType]


class Header(enum.Enum):
    """Packet Headers."""

    GENERAL = 0b00
    EXT_13 = 0b01
    EXT_16 = 0b10
    RESERVED = 0b11
    CONT = enum.auto()


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
        "id": "GoProUUIDs.CQ_QUERY_RESP.QueryCmdId.GET_SETTING_VAL",
        "SettingId.RESOLUTION": [
            "RES_1080"
        ]
    }
    """

    _feature_action_id_map: ClassVar[dict[FeatureId, list[ActionId]]] = defaultdict(list)
    _global_parsers: ClassVar[ParserMapType] = {}

    class _State(enum.Enum):
        """Describes the state of the GoProResp."""

        INITIALIZED = enum.auto()
        ACCUMULATED = enum.auto()
        PARSED = enum.auto()
        ERROR = enum.auto()

    class Protocol(enum.Enum):
        """Protocol that Command will be sent on."""

        BLE = "BLE"
        WIFI = "WIFI"

    def __init__(
        self,
        meta: list[ResponseType],
        parser: Optional[ParserType] = None,
        status: ErrorCode = ErrorCode.SUCCESS,
        raw_packet: Optional[Union[bytearray, dict[str, Any]]] = None,
    ) -> None:
        """Constructor

        Args:
            meta (list[ResponseType]): A list of all information known about the response.
            parser (Optional[ParserType]): Optional parser. If not passed, parser will be found from global
                parsers
            status (ErrorCode): A status if known at time of instantiation. Defaults to ErrorCode.SUCCESS.
            raw_packet (Optional[Union[bytearray, dict[str, Any]]]): The unparsed input if known at time of
                instantiation. Defaults to None.
        """
        # A list describing all of the currently known information about the response.
        # This will be appended to as more information is discovered. The various properties of GoProResp will
        # use this list to parse out their relevant information.
        self._meta: list[ResponseType] = meta
        # Parsers to use to parse this response
        self._parser = parser

        self.status: ErrorCode = status
        """Status of the response"""

        # Start with empty list as default value in case we need to append.
        # If we end up not needing a list, we will just overwrite the default
        self.data: dict[Any, Any] = defaultdict(list)
        """Response data which is really JSON data stored as a dict"""

        self._raw_packet = raw_packet
        self._bytes_remaining = 0
        self._state: GoProResp._State = GoProResp._State.INITIALIZED

    @classmethod
    def _from_read_response(cls, uuid: BleUUID, data: bytearray) -> GoProResp:
        """Build a GoProResp from a read response.

        Args:
            uuid (BleUUID): BleUUID that read command was received from
            data (bytearray): received bytestream

        Returns:
            GoProResp: created instance
        """
        resp = cls(meta=[uuid], status=ErrorCode.SUCCESS, raw_packet=data)
        resp._parse()
        return resp

    @classmethod
    def _from_http_response(
        cls, parser: Optional[JsonParser], response: requests.models.Response
    ) -> GoProResp:
        """Build a GoProResp from an HTTP response from the requests package.

        Args:
            parser (Optional[JsonParser]): parsers to use to parse received data
            response (requests.models.Response): HTTP response

        Returns:
            GoProResp: created instance
        """
        resp = cls(
            meta=[response.url],
            parser=parser,
            status=ErrorCode.SUCCESS if response.ok else ErrorCode.ERROR,
            raw_packet=response.json() if response.text else {},
        )
        resp._parse()
        return resp

    @classmethod
    def _get_response_meta(cls, data: bytes, uuid: BleUUID) -> list[ResponseType]:
        """Get a response's meta information from raw bytes and the UUID it was received on

        Args:
            data (bytes): bytes received as BLE notification
            uuid (BleUUID): UUID response was received on

        Returns:
            list[ResponseType]: List of meta information in order from least to most specific
        """
        meta: list[ResponseType] = [uuid]

        # If it's a protobuf command
        identifier = data[0]
        try:
            FeatureId(identifier)
            meta.append(ActionId(data[1]))
        # Otherwise it's a TLV command
        except ValueError:
            if uuid is GoProUUIDs.CQ_SETTINGS_RESP:
                meta.append(SettingId(identifier))
            elif uuid is GoProUUIDs.CQ_QUERY_RESP:
                meta.append(QueryCmdId(identifier))
            elif uuid in [GoProUUIDs.CQ_COMMAND_RESP, GoProUUIDs.CN_NET_MGMT_RESP]:
                meta.append(CmdId(identifier))
            # Else case is direct so the UUID (which is already in meta) is the identifier
        return meta

    @classmethod
    def _add_feature_action_id_mapping(cls, feature_id: FeatureId, action_id: ActionId) -> None:
        """Add a feature id-to-action id mapping entry

        Args:
            feature_id (FeatureId): Feature ID of protobuf command
            action_id (ActionId): Action ID of protobuf command
        """
        cls._feature_action_id_map[feature_id].append(action_id)

    @classmethod
    def _add_global_parser(cls, identifier: ResponseType, parser: BytesParser) -> None:
        """Add a global parser that can be accessed by this class's class methods

        Args:
            identifier (ResponseType): identifier to add parser for
            parser (BytesParser): parser to add
        """
        cls._global_parsers[identifier] = parser

    @classmethod
    def _get_setting_possibilities(cls, identifier: SettingId) -> Optional[type[GoProEnum]]:
        """Given a setting ID, attempt to get enum container of its possible values.

        For example, get_param_values_from_id(SettingId.Resolution) will return
        :py:class:`open_gopro.api.params.Resolution`

        Note! Not all setting ID's are currently parsed so None will be returned if the container does not exist

        Note! This is a helper function since this same functionality can be accomplished with the parser
        returned from :py:meth:`open_gopro.responses.GoProResp._get_global_parser`

        Args:
            identifier (SettingId): identifier to find container for

        Raises:
            ValueError: Attempted to get param values from non-param ID

        Returns:
            type[GoProEnum]: container if found else None
        """
        try:
            return cls._global_parsers[identifier].container  # type: ignore
        except KeyError:
            return None
        except AttributeError as e:
            raise ValueError(f"Can only get possibilities for setting ID's, not {identifier}") from e

    @classmethod
    def _get_global_parser(cls, identifier: ResponseType) -> Optional[ParserType]:
        """Get a globally defined parser for the given ID.

        Currently, only BLE uses globally defined parsers

        Args:
            identifier (ResponseType): ID to get parser for

        Returns:
            Optional[Parser]: parser if found, else None
        """
        return cls._global_parsers.get(identifier)

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, GoProEnum):
            return self.identifier == obj
        if isinstance(obj, GoProResp):
            return self.identifier == obj.identifier
        raise TypeError("Equal can only compare GoProResp and ResponseType")

    def __getitem__(self, key: Any) -> Any:
        return self.data[key]

    def __contains__(self, item: Any) -> bool:
        return item in self.data

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __str__(self) -> str:
        return jsonify(self._as_dict())

    def _as_dict(self) -> dict[str, Any]:
        """Return the response as a dict

        Returns:
            dict[str, Any]: response as dict
        """
        work_dict = dict(id=self.identifier, protocol=self.protocol.name, status=self.status.name)
        if self.cmd:
            work_dict["command"] = self.cmd
        if self.uuid:
            work_dict["uuid"] = self.uuid
        if self.endpoint:
            work_dict["endpoint"] = self.endpoint
        return {**work_dict, **self.data}

    def __repr__(self) -> str:
        return f"GoProResp <{str(self.identifier)}: {self._state}>"

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
    def protocol(self) -> GoProResp.Protocol:
        """Get the protocol that the response was received on

        Returns:
            GoProResp.Protocol: protocol
        """
        return GoProResp.Protocol.BLE if self.uuid else GoProResp.Protocol.WIFI

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
    def identifier(self) -> ResponseType:
        """Get the identifier of the response.

        Will vary depending on what type of response this is:

        - for a direct BLE read / write to a characteristic, it will be a :py:class:`open_gopro.ble.services.BleUUID`
        - for a BLE command response, it will be a :py:class:`open_gopro.constants.CmdType`
        - for a BLE setting / status response / update, it will be a :py:class:`open_gopro.constants.SettingId`
            or :py:class:`open_gopro.constants.StatusId`
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
    def is_protobuf(self) -> bool:
        """Is this response a protobuf response

        Returns:
            bool: Yes if true, No otherwise
        """
        return bool({ActionId, FeatureId}.intersection({type(x) for x in self._meta}))

    @property
    def is_direct_read(self) -> bool:
        """Is this response a direct read of a BLE characteristic

        Returns:
            bool: Yes if true, No otherwise
        """
        return len(self._meta) == 1 and isinstance(self.identifier, BleUUID)

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
            ResponseParseError: Error when parsing data
            RuntimeError: unexpected state
        """
        # Is this a BLE response?
        if isinstance(self._raw_packet, bytearray):
            assert self.uuid
            buf: bytearray = self._raw_packet
            self._meta = self._get_response_meta(buf, self.uuid)

            if not self.is_direct_read:  # length byte
                buf.pop(0)
            if self.is_protobuf:  # feature ID byte
                buf.pop(0)

            try:
                query_type: Optional[Union[type[StatusId], type[SettingId], StatusId, SettingId]] = None
                # Need to delineate QueryCmd responses between settings and status
                if not self.is_protobuf:
                    if isinstance(self.identifier, (SettingId, StatusId)):
                        query_type = self.identifier
                    elif isinstance(self.identifier, QueryCmdId):
                        if self.identifier in [
                            QueryCmdId.GET_STATUS_VAL,
                            QueryCmdId.REG_STATUS_VAL_UPDATE,
                            QueryCmdId.UNREG_STATUS_VAL_UPDATE,
                            QueryCmdId.STATUS_VAL_PUSH,
                        ]:
                            query_type = StatusId
                        elif self.identifier is QueryCmdId.GET_SETTING_NAME:
                            raise NotImplementedError
                        else:
                            query_type = SettingId

                # Query (setting get value, status get value, etc.)
                if query_type:
                    self.status = ErrorCode(buf[0])
                    buf = buf[1:]
                    # Parse all parameters
                    while len(buf) != 0:
                        param_id = query_type(buf[0])  # type: ignore
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
                            if not (parser := self._get_global_parser(param_id)):
                                # We don't have defined params for all ID's yet. Just store raw bytes
                                logger.warning(f"No parser defined for {param_id}")
                                self.data[param_id] = param_val
                                continue
                            # These can be more than 1 value so use a list
                            if self.cmd in [
                                QueryCmdId.GET_CAPABILITIES_VAL,
                                QueryCmdId.REG_CAPABILITIES_UPDATE,
                                QueryCmdId.SETTING_CAPABILITY_PUSH,
                            ]:
                                # Parse using parser from global map and append
                                self.data[param_id].append(parser.parse(param_val))  # type: ignore
                            else:
                                # Parse using parser from map and set
                                self.data[param_id] = parser.parse(param_val)  # type: ignore
                        except ValueError:
                            # This is the case where we receive a value that is not defined in our params.
                            # This shouldn't happen and means the documentation needs to be updated. However, it
                            # isn't functionally critical
                            logger.warning(f"{param_id} does not contain a value {param_val}")
                            self.data[param_id] = param_val
                else:  # Commands,  Protobuf, and direct Reads
                    if is_cmd := isinstance(self.identifier, CmdId):
                        # All (non-protobuf) commands have a status
                        self.status = ErrorCode(buf[0])
                        buf = buf[1:]
                    # Use parser if explicitly passed otherwise get global parser
                    if not (parser := self._get_global_parser(self.identifier) or self._parser) and not is_cmd:
                        error_msg = f"No parser exists for {self.identifier}"
                        logger.error(error_msg)
                        raise ResponseParseError(str(self.identifier), self._raw_packet, msg=error_msg)
                    # Parse payload if a parser was found.
                    if parser:
                        self.data = parser.parse(buf)  # type: ignore
                    # Attempt to determine and / or extract status (we already got command status above)
                    if self.is_direct_read and len(self._raw_packet):
                        # Assume success on direct reads if there was any data
                        self.status = ErrorCode.SUCCESS
                    elif (
                        self.is_protobuf and self.data and "result" in self.data
                    ):  # Check for result field in protobuf's
                        self.status = (
                            ErrorCode.SUCCESS
                            if self.data["result"] == EnumResultGeneric.RESULT_SUCCESS
                            else ErrorCode.ERROR
                        )
                    elif not is_cmd:
                        self.status = ErrorCode.UNKNOWN
            except KeyError as e:
                self._state = GoProResp._State.ERROR
                raise ResponseParseError(str(self.identifier), buf) from e

        # Is this an HTTP response?
        elif isinstance(self._raw_packet, dict):
            # Is there a parser for this? Most of them do not have one yet.
            self.data = self._parser.parse(self._raw_packet) if self._parser else self._raw_packet  # type: ignore

        # This should never happen
        else:
            raise RuntimeError(
                f"Unexpected data type ({str(type(self._raw_packet))}) when attempting to parse response"
            )

        # Recursively scrub away parsing artifacts
        scrub(self.data, "_io")
        scrub(self.data, "status")
        self._state = GoProResp._State.PARSED
