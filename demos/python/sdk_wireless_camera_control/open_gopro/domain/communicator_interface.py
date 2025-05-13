# communication_client.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""GoPro specific BLE client"""

from __future__ import annotations

import enum
import inspect
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, Iterator, Pattern, Protocol, TypeVar
from urllib.parse import urlencode

from construct import Bit, BitsInteger, BitStruct, Const, Construct, Padding

from open_gopro.domain.parser_interface import (
    BytesParser,
    BytesTransformer,
    GlobalParsers,
    JsonParser,
    JsonTransformer,
    Parser,
)
from open_gopro.models import GoProBlePacketHeader, GoProResp
from open_gopro.models.constants import GoProUUID
from open_gopro.models.types import IdType, JsonDict, UpdateCb, UpdateType
from open_gopro.network.ble import (
    BleClient,
    BLEController,
    BleDevice,
    BleHandle,
    BleUUID,
    DisconnectHandlerType,
    NotiHandlerType,
)
from open_gopro.network.wifi import WifiClient, WifiController

logger = logging.getLogger(__name__)


class MessageRules:
    """Message Rules Manager

    Attributes:
        always_false (Analyzer): helper analyzer for a property that is always false
        always_true (Analyzer): helper analyzer for a property that is always true

    Args:
        fastpass_analyzer (Analyzer): Analyzer to decide if the message is fastpass. Defaults to always_false.
        wait_for_encoding_analyzer (Analyzer): Analyzer to decide if the message should wait for encoding.
            Defaults to always_false.
    """

    class Analyzer(Protocol):
        """Protocol definition of message rules analyzer"""

        def __call__(self, **kwargs: Any) -> bool:
            """Analyze the current inputs to see if the rule should be applied

            Args:
                **kwargs (Any): input arguments

            Returns:
                bool: Should the rule be applied?
            """

    always_false: Analyzer = lambda **kwargs: False
    always_true: Analyzer = lambda **kwargs: True

    def __init__(
        self, fastpass_analyzer: Analyzer = always_false, wait_for_encoding_analyzer: Analyzer = always_false
    ) -> None:
        self._analyze_fastpass = fastpass_analyzer
        self._analyze_wait_for_encoding = wait_for_encoding_analyzer

    def is_fastpass(self, **kwargs: Any) -> bool:
        """Is this command fastpass?

        Args:
            **kwargs (Any) : Arguments passed into the message

        Returns:
            bool: result of rule check
        """
        return self._analyze_fastpass(**kwargs)

    def should_wait_for_encoding_start(self, **kwargs: Any) -> bool:
        """Should this message wait for encoding to start?

        Args:
            **kwargs (Any) : Arguments passed into the message

        Returns:
            bool: result of rule check
        """
        return self._analyze_wait_for_encoding(**kwargs)


##############################################################################################################
####### Communicators / Clients
##############################################################################################################


class BaseGoProCommunicator(ABC):
    """Common Communicator interface"""

    class _CompositeRegisterType(enum.Enum):
        """A composite register type to signify all elements of a given set should be (un)registered for"""

        ALL_SETTINGS = enum.auto()
        ALL_STATUSES = enum.auto()

    @abstractmethod
    def _register_update(self, callback: UpdateCb, update: _CompositeRegisterType | UpdateType) -> None:
        """Common register method for both public UpdateType and "protected" internal register type

        Args:
            callback (UpdateCb): callback to register
            update (_CompositeRegisterType | UpdateType): update type to register for
        """

    @abstractmethod
    def _unregister_update(self, callback: UpdateCb, update: _CompositeRegisterType | UpdateType | None = None) -> None:
        """Common unregister method for both public UpdateType and "protected" internal register type

        Args:
            callback (UpdateCb): callback to unregister
            update (_CompositeRegisterType | UpdateType | None): Update type to unregister for. Defaults to
                    None which will unregister the callback for all update types.
        """

    @property
    @abstractmethod
    def identifier(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """

    @abstractmethod
    def register_update(self, callback: UpdateCb, update: UpdateType) -> None:
        """Register for callbacks when an update occurs

        Args:
            callback (UpdateCb): callback to be notified in
            update (UpdateType): update to register for
        """

    @abstractmethod
    def unregister_update(self, callback: UpdateCb, update: UpdateType | None = None) -> None:
        """Unregister for asynchronous update(s)

        Args:
            callback (UpdateCb): callback to stop receiving update(s) on
            update (UpdateType | None): updates to unsubscribe for. Defaults to None (all
                updates that use this callback will be unsubscribed).
        """


class GoProHttp(BaseGoProCommunicator):
    """Interface definition for all HTTP communicators"""

    @abstractmethod
    async def _get_json(
        self, message: HttpMessage, *, timeout: int = 0, rules: MessageRules | None = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        """Perform a GET operation that returns JSON

        Args:
            message (HttpMessage): operation description
            timeout (int): time (in seconds) to wait to receive response before returning error. Defaults to 0.
            rules (MessageRules | None): message rules that this operation will obey. Defaults to MessageRules().
            **kwargs (Any) : any run-time arguments to apply to the operation

        Returns:
            GoProResp: response parsed from received JSON
        """

    @abstractmethod
    async def _get_stream(
        self, message: HttpMessage, *, timeout: int = 0, rules: MessageRules | None = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        """Perform a GET operation that returns a binary stream

        Args:
            message (HttpMessage): operation description
            timeout (int): time (in seconds) to wait to receive response before returning error. Defaults to 0.
            rules (MessageRules | None): message rules that this operation will obey. Defaults to MessageRules().
            **kwargs (Any) : any run-time arguments to apply to the operation

        Returns:
            GoProResp: response wrapper around downloaded binary
        """

    @abstractmethod
    async def _put_json(
        self, message: HttpMessage, *, timeout: int = 0, rules: MessageRules | None = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        """Perform a PUT operation that returns JSON

        Args:
            message (HttpMessage): operation description
            timeout (int): time (in seconds) to wait to receive response before returning error. Defaults to 0.
            rules (MessageRules | None): message rules that this operation will obey. Defaults to MessageRules().
            **kwargs (Any) : any run-time arguments to apply to the operation

        Returns:
            GoProResp: response parsed from received JSON
        """


class GoProWifi(GoProHttp):
    """GoPro specific WiFi Client

    Args:
        controller (WifiController): instance of Wifi Controller to use for this client
    """

    def __init__(self, controller: WifiController):
        self._wifi: WifiClient = WifiClient(controller)

    @property
    def password(self) -> str | None:
        """Get the GoPro AP's password

        Returns:
            str | None: password or None if it is not known
        """
        return self._wifi.password

    @property
    def ssid(self) -> str | None:
        """Get the GoPro AP's WiFi SSID

        Returns:
            str | None: SSID or None if it is not known
        """
        return self._wifi.ssid


class GoProBle(BaseGoProCommunicator, Generic[BleHandle, BleDevice]):
    """GoPro specific BLE Client

    Args:
        controller (BLEController): controller implementation to use for this client
        disconnected_cb (DisconnectHandlerType): disconnected callback
        notification_cb (NotiHandlerType): notification callback
        target (str | BleDevice): device to connect to or trailing digits of serial number
    """

    def __init__(
        self,
        controller: BLEController,
        disconnected_cb: DisconnectHandlerType,
        notification_cb: NotiHandlerType,
        target: str | BleDevice,
    ) -> None:
        self._ble: BleClient = BleClient(
            controller,
            disconnected_cb,
            notification_cb,
            (re.compile(r"GoPro [A-Z0-9]{4}") if target is None else f".*{target}", [GoProUUID.S_CONTROL_QUERY]),
            uuids=GoProUUID,
        )

    @abstractmethod
    async def _send_ble_message(
        self, message: BleMessage, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        """Perform a GATT write with response and accumulate received notifications into a response.

        Args:
            message (BleMessage): BLE operation description
            rules (MessageRules): message rules that this operation will obey. Defaults to MessageRules().
            **kwargs (Any) : any run-time arguments to apply to the operation

        Returns:
            GoProResp: response parsed from accumulated BLE notifications
        """

    @abstractmethod
    async def _read_ble_characteristic(
        self, message: BleMessage, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        """Perform a direct GATT read of a characteristic

        Args:
            message (BleMessage): BLE operation description
            rules (MessageRules): message rules that this operation will obey. Defaults to MessageRules().
            **kwargs (Any) : any run-time arguments to apply to the operation

        Returns:
            GoProResp: response parsed from bytes read from characteristic
        """

    # TODO this should be somewhere else
    @classmethod
    def _fragment(cls, data: bytes) -> Iterator[bytes]:
        """Fragment data in to MAX_BLE_PKT_LEN length packets

        Args:
            data (bytes): data to fragment

        Raises:
            ValueError: data is too long

        Yields:
            bytes: packet as bytes
        """
        MAX_BLE_PKT_LEN = 20

        extended_13_header = BitStruct(
            "continuation" / Const(0, Bit),
            "header" / Const(GoProBlePacketHeader.EXT_13.value, BitsInteger(2)),
            "length" / BitsInteger(13),
        )

        extended_16_header = BitStruct(
            "continuation" / Const(0, Bit),
            "header" / Const(GoProBlePacketHeader.EXT_16.value, BitsInteger(2)),
            "padding" / Padding(5),
            "length" / BitsInteger(16),
        )

        continuation_header = BitStruct(
            "continuation" / Const(1, Bit),
            "padding" / Padding(7),
        )

        header: Construct
        if (data_len := len(data)) < (2**13 - 1):
            header = extended_13_header
        elif data_len < (2**16 - 1):
            header = extended_16_header
        else:
            raise ValueError(f"Data length {data_len} is too long")

        assert header
        while data:
            if header == continuation_header:
                packet = bytearray(header.build({}))
            else:
                packet = bytearray(header.build({"length": data_len}))
                header = continuation_header

            bytes_remaining = MAX_BLE_PKT_LEN - len(packet)
            current, data = (data[:bytes_remaining], data[bytes_remaining:])
            packet.extend(current)
            yield bytes(packet)


class GoProWiredInterface(BaseGoProCommunicator):
    """The top-level interface for a Wired Open GoPro controller"""


class GoProWirelessInterface(GoProBle, GoProWifi, Generic[BleDevice, BleHandle]):
    """The top-level interface for a Wireless Open GoPro controller

    This always supports BLE and can optionally support Wifi

    Args:
        ble_controller (BLEController): BLE controller instance
        wifi_controller (WifiController): Wifi controller instance
        disconnected_cb (DisconnectHandlerType): callback for BLE disconnects
        notification_cb (NotiHandlerType): callback for BLE received notifications
        target (Pattern | BleDevice): BLE device to search for
    """

    def __init__(
        self,
        ble_controller: BLEController,
        wifi_controller: WifiController,
        disconnected_cb: DisconnectHandlerType,
        notification_cb: NotiHandlerType,
        target: Pattern | BleDevice,
    ) -> None:
        # Initialize GoPro Communication Client
        GoProBle.__init__(self, ble_controller, disconnected_cb, notification_cb, target)
        GoProWifi.__init__(self, wifi_controller)


ParserType = TypeVar("ParserType", BytesParser, JsonParser)
FilterType = TypeVar("FilterType", BytesTransformer, JsonTransformer)


##############################################################################################################
####### Messages (commands, etc.)
##############################################################################################################


class Message(ABC):
    """Base class for all messages that will be contained in a Messages class"""

    def __init__(
        self,
        identifier: IdType,
        parser: Parser | None = None,
    ) -> None:
        self._identifier: IdType = identifier
        self._parser = parser

    @abstractmethod
    def _as_dict(self, **kwargs: Any) -> JsonDict:
        """Return the attributes of the message as a dict

        Args:
            **kwargs (Any): additional entries for the dict

        Returns:
            JsonDict: message as dict
        """


class BleMessage(Message):
    """The base class for all BLE messages to store common info

    Args:
        uuid (BleUUID): BLE client to read / write
        identifier (IdType): BleUUID to read / write to
        parser (Parser | None): parser to interpret message
    """

    def __init__(
        self,
        uuid: BleUUID,
        identifier: IdType,
        parser: Parser | None,
    ) -> None:
        Message.__init__(self, identifier, parser)
        self._uuid = uuid
        self._base_dict = {"protocol": GoProResp.Protocol.BLE, "uuid": self._uuid}

        if parser:
            GlobalParsers.add(identifier, parser)

    @abstractmethod
    def _build_data(self, **kwargs: Any) -> bytearray:
        """Build the raw write request from operation description and run-time arguments

        Args:
            **kwargs (Any) : run-time arguments

        Returns:
            bytearray: raw bytes request
        """


class HttpMessage(Message):
    """The base class for all HTTP messages. Stores common information.

    Args:
        endpoint (str): base endpoint
        identifier (IdType | None): explicit message identifier. If None, will be generated from endpoint.
        components (list[str] | None): Additional path components (i.e. endpoint/{COMPONENT}). Defaults to None.
        arguments (list[str] | None): Any arguments to be appended after endpoint (i.e. endpoint?{ARGUMENT}). Defaults to None.
        body_args (list[str] | None): Arguments to be added to the body JSON. Defaults to None.
        headers (dict[str, Any] | None): A dict of values to be set in the HTTP operation headers. Defaults to None.
        certificate (Path | None): Path to SSL certificate bundle. Defaults to None.
        parser (Parser | None): Parser to interpret HTTP responses. Defaults to None.
    """

    def __init__(
        self,
        endpoint: str,
        identifier: IdType | None,
        components: list[str] | None = None,
        arguments: list[str] | None = None,
        body_args: list[str] | None = None,
        headers: dict[str, Any] | None = None,
        certificate: Path | None = None,
        parser: Parser | None = None,
    ) -> None:
        if not identifier:
            # Build human-readable name from endpoint
            identifier = endpoint.lower().removeprefix("gopro/").replace("/", " ").replace("_", " ").title()
            try:
                identifier = identifier.split("?")[0].strip("{}")
            except IndexError:
                pass

        self._headers = headers or {}
        self._endpoint = endpoint
        self._components = components or []
        self._arguments = arguments or []
        self._body_args = body_args or []
        self._certificate = certificate
        Message.__init__(self, identifier, parser)
        self._base_dict: JsonDict = {
            "id": self._identifier,
            "protocol": GoProResp.Protocol.HTTP,
            "endpoint": self._endpoint,
        }

    def __str__(self) -> str:
        return str(self._identifier).title()

    def _as_dict(self, **kwargs: Any) -> JsonDict:
        """Return the attributes of the message as a dict

        Args:
            **kwargs (Any): additional entries for the dict

        Returns:
            JsonDict: message as dict
        """
        # If any kwargs keys were to conflict with base dict, append underscore
        return self._base_dict | {f"{'_' if k in ['id', 'protocol'] else ''}{k}": v for k, v in kwargs.items()}

    def build_body(self, **kwargs: Any) -> dict[str, Any]:
        """Build JSON body from run-time body arguments

        Args:
            **kwargs (Any): run-time arguments to check to see if each should be added to the body

        Returns:
            dict[str, Any]: built JSON body
        """
        body: dict[str, Any] = {}
        for name, value in kwargs.items():
            if name in self._body_args:
                body[name] = value
        return body

    def build_url(self, **kwargs: Any) -> str:
        """Build the URL string from the passed in components and arguments

        Args:
            **kwargs (Any): additional entries for the dict

        Returns:
            str: built URL
        """
        url = self._endpoint
        for component in self._components:
            url += "/" + kwargs.pop(component)
        # Append parameters
        if self._arguments and (
            arg_part := urlencode(
                {
                    k: kwargs[k].value if isinstance(kwargs[k], enum.Enum) else kwargs[k]
                    for k in self._arguments
                    if kwargs[k] is not None
                },
                safe="/",
            )
        ):
            url += "?" + arg_part
        return url


MessageType = TypeVar("MessageType", bound=Message)

CommunicatorType = TypeVar("CommunicatorType", bound=BaseGoProCommunicator)


class Messages(ABC, dict, Generic[MessageType, CommunicatorType]):
    """Base class for setting and status containers

    Allows message groups to be iterable and supports dict-like access.

    Instance attributes that are an instance (or subclass) of Message are automatically accumulated during
    instantiation

    Args:
        communicator (CommunicatorType): communicator that will send messages
    """

    def __init__(self, communicator: CommunicatorType) -> None:
        self._communicator = communicator
        # Append any automatically discovered instance attributes (i.e. for settings and statuses)
        message_map: dict[IdType, MessageType] = {}
        for message in self.__dict__.values():
            if hasattr(message, "_identifier"):
                message_map[message._identifier] = message
        # Append any automatically discovered methods (i.e. for commands)
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if not name.startswith("_"):
                message_map[name.replace("_", " ").title()] = method  # type: ignore
        dict.__init__(self, message_map)


class BleMessages(Messages[MessageType, GoProBle]):
    """A container of BLE Messages.

    Identical to Messages and it just used for typing
    """


class HttpMessages(Messages[MessageType, GoProHttp]):
    """A container of HTTP Messages.

    Identical to Messages and it just used for typing
    """
