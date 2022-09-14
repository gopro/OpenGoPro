# communication_client.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:53 UTC 2021

"""GoPro specific BLE client"""

from __future__ import annotations
import re
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from collections.abc import Iterator, Iterable
from typing import Generic, Optional, Union, Pattern, TYPE_CHECKING, Any, TypeVar, Generator

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

if TYPE_CHECKING:
    from open_gopro import Params

logger = logging.getLogger(__name__)

MAX_BLE_PKT_LEN = 20


class GoProDataHandler:
    """A class that can both send and receive GoPro data

    This supports fragmentation of data if necessary if it is > MAX_BLE_PKT_LEN.
    """

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
        header: Construct
        if (data_len := len(data)) < (2**5 - 1):
            header = GoProDataHandler.general_header
        elif data_len < (2**13 - 1):
            header = GoProDataHandler.extended_13_header
        elif data_len < (2**16 - 1):
            header = GoProDataHandler.extended_16_header
        else:
            raise ValueError(f"Data length {data_len} is too long")

        assert header
        while data:
            if header == GoProDataHandler.continuation_header:
                packet = bytearray(header.build({}))
            else:
                packet = bytearray(header.build(dict(length=data_len)))
                header = GoProDataHandler.continuation_header

            bytes_remaining = MAX_BLE_PKT_LEN - len(packet)
            current, data = (data[:bytes_remaining], data[bytes_remaining:])
            packet.extend(current)
            yield packet


class GoProWifi(ABC, GoProDataHandler):
    """GoPro specific WiFi Client

    Args:
        controller (WifiController): instance of Wifi Controller to use for this client
    """

    def __init__(self, controller: WifiController):
        GoProDataHandler.__init__(self)
        self._wifi: WifiClient = WifiClient(controller)

    @abstractmethod
    def _get(self, url: str, parser: Optional[JsonParser] = None) -> GoProResp:
        """Send an HTTP GET request to a string endpoint.

        Args:
            url (str): endpoint not including GoPro base path
            parser (Optional[JsonParser]): Optional parser to further parse received JSON dict. Defaults to
                None.

        Returns:
            GoProResp: GoPro response
        """
        raise NotImplementedError

    @abstractmethod
    def _stream_to_file(self, url: str, file: Path) -> None:
        """Send an HTTP GET request to an Open GoPro endpoint to download a binary file.

        Args:
            url (str): endpoint URL
            file (Path): location where file should be downloaded to
        """
        raise NotImplementedError

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


class GoProBle(ABC, GoProDataHandler, Generic[BleHandle, BleDevice]):
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
        GoProDataHandler.__init__(self)
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
    def _send_ble_command(self, uuid: BleUUID, data: bytearray, response_id: ResponseType) -> GoProResp:
        """Write a characteristic and block until its corresponding notification response is received.

        Args:
            uuid (BleUUID): characteristic to write to
            data (bytearray): bytes to write
            response_id (ResponseType): identifier to claim parsed response in notification handler

        Returns:
            GoProResp: received response
        """
        raise NotImplementedError

    @abstractmethod
    def _read_characteristic(self, uuid: BleUUID) -> GoProResp:
        """Read a characteristic and block until its corresponding notification response is received.

        Args:
            uuid (BleUUID): _description_

        Returns:
            GoProResp: _description_
        """
        raise NotImplementedError


class GoProInterface(GoProBle, GoProWifi, Generic[BleDevice, BleHandle]):
    """The top-level interface to subclass for an Open GoPro controller"""

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


CommunicatorType = TypeVar("CommunicatorType", bound=Union[GoProBle, GoProWifi])
IdType = TypeVar("IdType", SettingId, StatusId, ActionId, CmdId, BleUUID, str)
ParserType = TypeVar("ParserType", BytesParser, JsonParser)


class Command(Generic[CommunicatorType, IdType, ParserType]):
    """Base class for all commands that will be contained in a Commands class"""

    def __init__(
        self,
        communicator: CommunicatorType,
        identifier: IdType,
        parser: Optional[ParserType] = None,
    ) -> None:
        """Constructor

        Args:
            communicator (CommunicatorType): BLE or WiFi communicator
            identifier (IdType): id to access this command by
            parser (ParserType): optional parser and builder
        """
        self._communicator = communicator
        self._identifier: IdType = identifier
        self._parser: Optional[ParserType] = parser

    @abstractmethod
    def _as_dict(self, *_: Any, **kwargs: Any) -> dict[str, Any]:
        """Return the attributes of the command as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: command as dict
        """
        raise NotImplementedError


class BleCommand(ABC, Command[GoProBle, IdType, BytesParser]):
    """The base class for all BLE commands to store common info

    Args:
        communicator (GoProBle): BLE client to read / write
        uuid (BleUUID): BleUUID to read / write to
    """

    def __init__(
        self,
        communicator: GoProBle,
        uuid: BleUUID,
        parser: Optional[BytesParser],
        identifier: IdType,
    ) -> None:
        super().__init__(communicator, identifier, parser)  # type: ignore
        self._uuid = uuid
        self._base_dict = dict(protocol="BLE", uuid=self._uuid)

        if self._parser:
            GoProResp._add_global_parser(identifier, self._parser)


class WifiCommand(Command[GoProWifi, IdType, JsonParser]):
    """The base class for all WiFi Commands. Stores common information.

    Args:
        communicator (GoProWifi): delegate owner to send commands and receive responses
        endpoint (str): base endpoint
        components (Optional[list[str]]): conditional endpoint components. Defaults to None.
        arguments (Optional[list[str]]): URL argument names. Defaults to None.
        parser (Optional[JsonParser]): additional parsing of JSON response. Defaults to None.
        name (Optional[str]): explicitly set command identifier. Defaults to None (generated from endpoint).
    """

    def __init__(
        self,
        communicator: GoProWifi,
        endpoint: str,
        identifier: IdType,
        components: Optional[list[str]] = None,
        arguments: Optional[list[str]] = None,
        parser: Optional[type[JsonParser]] = None,
    ) -> None:
        self._endpoint = endpoint
        self._components = components
        self._args = arguments
        super().__init__(communicator, identifier, parser)  # type: ignore
        self._base_dict: dict[str, Any] = dict(id=self._identifier, protocol="WiFi", endpoint=self._endpoint)

    def __str__(self) -> str:
        return str(self._identifier).title()

    def _as_dict(self, *_: Any, **kwargs: Any) -> dict[str, Any]:
        """Return the attributes of the command as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any): additional entries for the dict

        Returns:
            dict[str, Any]: command as dict
        """
        # If any kwargs keys were to conflict with base dict, append underscore
        return self._base_dict | {f"{'_' if k in ['id', 'protocol'] else ''}{k}": v for k, v in kwargs.items()}


CommandType = TypeVar("CommandType", bound=Command)


class Commands(Iterable, Generic[CommandType, IdType]):
    """Base class for command container

    Allows command groups to be iterable and supports dict-like access

    Args:
        communicator (Union[GoProBle, GoProWifi]): communicator that will send commands
    """

    def __init__(self, communicator: Union[GoProBle, GoProWifi]) -> None:
        self._communicator = communicator
        self._commands_list: list[CommandType] = []
        self._command_map: dict[IdType, CommandType] = {}
        for attribute, command in self.__dict__.items():
            if attribute.startswith("_"):
                continue
            self._commands_list.append(command)
            self._command_map[command._identifier] = command

    def __iter__(self) -> Iterator:
        return iter(self._commands_list)

    def __getitem__(self, key: IdType) -> CommandType:
        if self._command_map:
            return self._command_map[key]
        raise TypeError(f"{type(self)} object is not subscriptable")

    def __contains__(self, item: IdType) -> bool:
        return item in self._command_map
