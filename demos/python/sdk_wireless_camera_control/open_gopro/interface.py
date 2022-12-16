# communication_client.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""GoPro specific BLE client"""

from __future__ import annotations
import re
import enum
import inspect
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Generic, Optional, Union, Pattern, Any, TypeVar, Generator, Protocol

from construct import BitStruct, BitsInteger, Padding, Const, Bit, Construct

from open_gopro.ble import (
    BleDevice,
    BleHandle,
    BLEController,
    DisconnectHandlerType,
    NotiHandlerType,
    BleClient,
    BleUUID,
)
from open_gopro.wifi import WifiClient, WifiController
from open_gopro.responses import GoProResp, Header, BytesParser, JsonParser
from open_gopro.constants import GoProUUIDs, ProducerType, ResponseType, SettingId, StatusId, ActionId, CmdId

logger = logging.getLogger(__name__)


class GoProHttp(ABC):
    """Base class interface for all HTTP commands"""

    @abstractmethod
    def _get(self, url: str, parser: Optional[JsonParser] = None, **kwargs: Any) -> GoProResp:
        """Send an HTTP GET request to a string endpoint.

        Args:
            url (str): endpoint not including GoPro base path
            parser (Optional[JsonParser]): Optional parser to further parse received JSON dict. Defaults to
                None.
            **kwargs (Any):
                - rules (list[MessageRules]): rules to be enforced for this message

        Returns:
            GoProResp: GoPro response
        """
        raise NotImplementedError

    @abstractmethod
    def _stream_to_file(self, url: str, file: Path) -> GoProResp:
        """Send an HTTP GET request to an Open GoPro endpoint to download a binary file.

        Args:
            url (str): endpoint URL
            file (Path): location where file should be downloaded to
        """
        raise NotImplementedError


class GoProWifi(GoProHttp):
    """GoPro specific WiFi Client

    Args:
        controller (WifiController): instance of Wifi Controller to use for this client
    """

    def __init__(self, controller: WifiController):
        GoProHttp.__init__(self)
        self._wifi: WifiClient = WifiClient(controller)

    @property
    def password(self) -> Optional[str]:
        """Get the GoPro AP's password

        Returns:
            Optional[str]: password or None if it is not known
        """
        return self._wifi.password

    @property
    def ssid(self) -> Optional[str]:
        """Get the GoPro AP's WiFi SSID

        Returns:
            Optional[str]: SSID or None if it is not known
        """
        return self._wifi.ssid


class GoProBle(ABC, Generic[BleHandle, BleDevice]):
    """GoPro specific BLE Client

    Args:
        controller (BLEController): controller implementation to use for this client
        disconnected_cb (DisconnectHandlerType): disconnected callback
        notification_cb (NotiHandlerType): notification callback
        target (Union[Pattern, BleDevice]): regex or device to connect to
    """

    def __init__(
        self,
        controller: BLEController,
        disconnected_cb: DisconnectHandlerType,
        notification_cb: NotiHandlerType,
        target: Union[Pattern, BleDevice],
    ) -> None:
        self._ble: BleClient = BleClient(
            controller,
            disconnected_cb,
            notification_cb,
            (re.compile(r"GoPro [A-Z0-9]{4}") if target is None else target, [GoProUUIDs.S_CONTROL_QUERY]),
            uuids=GoProUUIDs,
        )

    @abstractmethod
    def _register_listener(self, producer: ProducerType) -> None:
        """Register to receive notifications for a producer.

        Args:
            producer (ProducerType): producer that we want to receive notifications from
        """
        raise NotImplementedError

    @abstractmethod
    def _unregister_listener(self, producer: ProducerType) -> None:
        """Stop receiving notifications from a producer.

        Args:
            producer (ProducerType): Producer to stop receiving notifications for
        """
        raise NotImplementedError

    @abstractmethod
    def get_notification(self, timeout: Optional[float] = None) -> GoProResp:
        """Get a notification that was received from a registered producer.

        Args:
            timeout (float, Optional): Time to wait for a notification before returning. Defaults to None (wait forever)

        Returns:
            GoProResp: the received update
        """
        raise NotImplementedError

    @abstractmethod
    def _send_ble_message(
        self, uuid: BleUUID, data: bytearray, response_id: ResponseType, **kwargs: Any
    ) -> GoProResp:
        """Write a characteristic and block until its corresponding notification response is received.

        Args:
            uuid (BleUUID): characteristic to write to
            data (bytearray): bytes to write
            response_id (ResponseType): identifier to claim parsed response in notification handler
            **kwargs (Any):
                - rules (list[MessageRules]): rules to be enforced for this message

        Returns:
            GoProResp: received response
        """
        raise NotImplementedError

    @abstractmethod
    def _read_characteristic(self, uuid: BleUUID) -> GoProResp:
        """Read a characteristic and block until its corresponding notification response is received.

        Args:
            uuid (BleUUID): characteristic ro read

        Returns:
            GoProResp: data read from characteristic
        """
        raise NotImplementedError

    @classmethod
    def _fragment(cls, data: bytearray) -> Generator[bytearray, None, None]:
        """Fragment data in to MAX_BLE_PKT_LEN length packets

        Args:
            data (bytearray): data to fragment

        Raises:
            ValueError: data is too long

        Yields:
            Generator[bytearray, None, None]: Generator of packets as bytearrays
        """
        MAX_BLE_PKT_LEN = 20
        general_header = BitStruct(
            "continuation" / Const(0, Bit),
            "header" / Const(Header.GENERAL.value, BitsInteger(2)),
            "length" / BitsInteger(5),
        )

        extended_13_header = BitStruct(
            "continuation" / Const(0, Bit),
            "header" / Const(Header.EXT_13.value, BitsInteger(2)),
            "length" / BitsInteger(13),
        )

        extended_16_header = BitStruct(
            "continuation" / Const(0, Bit),
            "header" / Const(Header.EXT_16.value, BitsInteger(2)),
            "padding" / Padding(5),
            "length" / BitsInteger(16),
        )

        continuation_header = BitStruct(
            "continuation" / Const(1, Bit),
            "padding" / Padding(7),
        )

        header: Construct
        if (data_len := len(data)) < (2**5 - 1):
            header = general_header
        elif data_len < (2**13 - 1):
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
                packet = bytearray(header.build(dict(length=data_len)))
                header = continuation_header

            bytes_remaining = MAX_BLE_PKT_LEN - len(packet)
            current, data = (data[:bytes_remaining], data[bytes_remaining:])
            packet.extend(current)
            yield packet


class GoProWiredInterface(GoProHttp):
    """The top-level interface for a Wired Open GoPro controller"""


class GoProWirelessInterface(GoProBle, GoProWifi, Generic[BleDevice, BleHandle]):
    """The top-level interface for a Wireless Open GoPro controller

    This always supports BLE and can optionally support Wifi
    """

    def __init__(
        self,
        ble_controller: BLEController,
        wifi_controller: Optional[WifiController],
        disconnected_cb: DisconnectHandlerType,
        notification_cb: NotiHandlerType,
        target: Union[Pattern, BleDevice],
    ) -> None:
        """Constructor

        Args:
            ble_controller (BLEController): BLE controller instance
            wifi_controller (Optional[WifiController]): Wifi controller instance
            disconnected_cb (DisconnectHandlerType): callback for BLE disconnects
            notification_cb (NotiHandlerType): callback for BLE received notifications
            target (Union[Pattern, BleDevice]): BLE device to search for
        """
        # Initialize GoPro Communication Client
        GoProBle.__init__(self, ble_controller, disconnected_cb, notification_cb, target)
        if wifi_controller:
            GoProWifi.__init__(self, wifi_controller)


CommunicatorType = TypeVar("CommunicatorType", bound=Union[GoProBle, GoProHttp])
IdType = TypeVar("IdType", SettingId, StatusId, ActionId, CmdId, BleUUID, str)
ParserType = TypeVar("ParserType", BytesParser, JsonParser)


class RuleSignature(Protocol):
    """Protocol definition for a rule evaluation function"""

    def __call__(self, **kwargs: Any) -> bool:
        """Function signature to evaluate a message rule

        Args:
            **kwargs (Any): arguments to user-facing message method

        Returns:
            bool: Whether or not message rule is currently enforced
        """


class MessageRules(enum.Enum):
    """Rules to be applied when message is executed"""

    FASTPASS = enum.auto()  #: Message can be sent when the camera is busy and / or encoding
    WAIT_FOR_ENCODING_START = enum.auto()  #: Message must not complete until encoding has started


class Message(Generic[CommunicatorType, IdType, ParserType], ABC):
    """Base class for all messages that will be contained in a Messages class"""

    def __init__(
        self,
        identifier: IdType,
        parser: Optional[ParserType] = None,
        rules: Optional[dict[MessageRules, RuleSignature]] = None,
    ) -> None:
        """Constructor

        Args:
            identifier (IdType): id to access this message by
            parser (ParserType): optional parser and builder
            rules (Optional[dict[MessageRules, RuleSignature]], optional): rules to apply when executing this
                message. Defaults to None.
        """
        self._identifier: IdType = identifier
        self._parser: Optional[ParserType] = parser
        self._rules = rules or {}

    def _evaluate_rules(self, **kwargs: Any) -> list[MessageRules]:
        """Given the arguments for the current message execution, which rules should be enforced?

        Args:
            **kwargs (Any): user-facing arguments to the current message execution

        Returns:
            list[MessageRules]: list of rules to be enforced
        """
        enforced_rules = []
        for rule, evaluator in self._rules.items():
            if evaluator(**kwargs):
                enforced_rules.append(rule)
        return enforced_rules

    @abstractmethod
    def __call__(self, __communicator__: CommunicatorType, **kwargs: Any) -> Any:
        """Execute the message by sending it to the target device

        Args:
            __communicator__ (CommunicatorType): communicator to send the message
            **kwargs (Any): not used

        Returns:
            Any: Value received from the device
        """
        raise NotImplementedError

    @abstractmethod
    def _as_dict(self, *_: Any, **kwargs: Any) -> dict[str, Any]:
        """Return the attributes of the message as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: message as dict
        """
        raise NotImplementedError


class BleMessage(Message[GoProBle, IdType, BytesParser]):
    """The base class for all BLE messages to store common info

    Args:
        communicator (GoProBle): BLE client to read / write
        uuid (BleUUID): BleUUID to read / write to
    """

    def __init__(
        self,
        uuid: BleUUID,
        parser: Optional[BytesParser],
        identifier: IdType,
        rules: Optional[dict[MessageRules, RuleSignature]] = None,
    ) -> None:
        Message.__init__(self, identifier, parser, rules)
        self._uuid = uuid
        self._base_dict = dict(protocol="BLE", uuid=self._uuid)

        if self._parser:
            GoProResp._add_global_parser(identifier, self._parser)


class HttpMessage(Message[GoProHttp, IdType, JsonParser]):
    """The base class for all HTTP messages. Stores common information."""

    def __init__(
        self,
        endpoint: str,
        identifier: IdType,
        components: Optional[list[str]] = None,
        arguments: Optional[list[str]] = None,
        parser: Optional[JsonParser] = None,
        rules: Optional[dict[MessageRules, RuleSignature]] = None,
    ) -> None:
        """Constructor

        Args:
            endpoint (str): base endpoint
            identifier (IdType): explicitly set message identifier. Defaults to None (generated from endpoint).
            components (Optional[list[str]]): conditional endpoint components. Defaults to None.
            arguments (Optional[list[str]]): URL argument names. Defaults to None.
            parser (Optional[JsonParser]): additional parsing of JSON response. Defaults to None.
            rules (Optional[dict[MessageRules, RuleSignature]], optional): rules to apply when executing this
                message. Defaults to None.
        """
        self._endpoint = endpoint
        self._components = components
        self._args = arguments
        Message.__init__(self, identifier, parser, rules=rules)
        self._base_dict: dict[str, Any] = dict(id=self._identifier, protocol="HTTP", endpoint=self._endpoint)

    def __str__(self) -> str:
        return str(self._identifier).title()

    def _as_dict(self, *_: Any, **kwargs: Any) -> dict[str, Any]:
        """Return the attributes of the message as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: message as dict
        """
        # If any kwargs keys were to conflict with base dict, append underscore
        return self._base_dict | {f"{'_' if k in ['id', 'protocol'] else ''}{k}": v for k, v in kwargs.items()}


MessageType = TypeVar("MessageType", bound=Message)


class Messages(ABC, dict, Generic[MessageType, IdType, CommunicatorType]):
    """Base class for setting and status containers

    Allows message groups to be iterable and supports dict-like access.

    Instance attributes that are an instance (or subclass) of Message are automatically accumulated during
    instantiation
    """

    def __init__(self, communicator: CommunicatorType) -> None:
        """Constructor

        Args:
            communicator (CommunicatorType): communicator that will send messages
        """
        self._communicator = communicator
        # Append any automatically discovered instance attributes (i.e. for settings and statuses)
        message_map: dict[Union[IdType, str], MessageType] = {}
        for message in self.__dict__.values():
            if isinstance(message, Message):
                message_map[message._identifier] = message  # type: ignore
        # Append any automatically discovered methods (i.e. for commands)
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if not name.startswith("_"):
                message_map[name.replace("_", " ").title()] = method
        dict.__init__(self, message_map)


class BleMessages(Messages[MessageType, IdType, GoProBle]):
    """A container of BLE Messages.

    Identical to Messages and it just used for typing
    """


class HttpMessages(Messages[MessageType, IdType, GoProHttp]):
    """A container of HTTP Messages.

    Identical to Messages and it just used for typing
    """
