# models.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Aug 17 20:05:18 UTC 2022

"""GUI models and associated common functionality"""

# pylint: disable = reimported, unused-import
# NOTE! The reason for the seemingly redundant, unnecessary import here is because we are using eval
# to dynamically build messages

from __future__ import annotations

import asyncio
import datetime
import enum
import inspect
import logging
import re
import typing
from pathlib import Path
from typing import (
    Any,
    Callable,
    Final,
    Generator,
    Optional,
    Pattern,
    Union,
    no_type_check,
)

import construct
from wrapt.decorators import BoundFunctionWrapper

import open_gopro.api.params  # needed for dynamic execution
import open_gopro.api.params as Params
from open_gopro import WirelessGoPro, constants, proto, types
from open_gopro.api import BleSetting, BleStatus, HttpSetting
from open_gopro.communicator_interface import (
    BleMessage,
    GoProBle,
    GoProHttp,
    HttpMessage,
    Message,
    Messages,
)
from open_gopro.models.response import GoProResp

PREVIEW_STREAM_URL: Final = r"udp://127.0.0.1:8554"

logger = logging.getLogger(__name__)


class CompoundGoPro(WirelessGoPro):
    """A GoPro that supports sending compound commands"""

    def __init__(self, target: Optional[Pattern] = None) -> None:
        """Constructor

        Args:
            target (Optional[Pattern], optional): BLE device (camera) to search for. Defaults to None (first
                found camera will be connected to).
        """

        super().__init__(target)
        self.compound_command = CompoundCommands(self)


class GoProModel:
    """GoPro model interface for controllers"""

    class Update(enum.Enum):
        """The type of update that the response / element corresponds to"""

        SETTING = enum.auto()
        STATUS = enum.auto()
        CAPABILITY = enum.auto()
        PROTOBUF = enum.auto()

    def __init__(self) -> None:
        # Initial instantiation just to get command strings
        self.gopro: CompoundGoPro = CompoundGoPro()

    async def start(self, identifier: Optional[Pattern]) -> None:
        """Open the model (i.e. connect BLE and Wifi to camera)

        Args:
            identifier (Optional[Pattern]): regex to connect to. Defaults to None (connect to first camera)
        """
        # Reinstantiate
        self.gopro = CompoundGoPro(target=identifier)
        await self.gopro.open()

    # NOTE: the following properties must be evaluated dynamically since self.gopro is changing
    # TODO hash and evaluate lazily

    @property
    def _message_types(self) -> list[Messages]:
        """Get the top level containers of the message types supported by the GoPro model

        Returns:
            list[Union[Commands, SettingsStatuses]]: list of message type containers
        """
        return [
            self.gopro.ble_command,
            self.gopro.ble_setting,
            self.gopro.ble_status,
            self.gopro.http_command,
            self.gopro.http_setting,
            self.gopro.compound_command,
        ]

    @property
    def messages(self) -> list[tuple[str, Message]]:
        """Get all of the available BLE and Wifi Messages

        Returns:
            list[Message]: list of available messages
        """
        messages = []
        for message_type in self._message_types:
            c = list(message_type.items())
            c.sort(key=lambda x: str(x[0]))
            messages.extend(c)
        return messages

    @property
    def message_dict(self) -> dict[str, list[str]]:
        """Get flattened dictionary of message indexed by their string name

        Returns:
            dict[str, list[str]]: flattened dict
        """
        d = {}
        for messages in self._message_types:
            d[type(messages).__name__] = [str(message) for message in messages]
            d[type(messages).__name__].sort()
        return d

    @classmethod
    def is_ble(cls, message: Message) -> bool:
        """Is this message a BLE message?

        Args:
            message (Message): Message to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return type(message) in (BleSetting, BleStatus, BleMessage)

    @classmethod
    def is_wifi(cls, message: Message) -> bool:
        """Is this message a Wifi Message?

        Args:
            message (Message): Message to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return type(message) in (HttpMessage, HttpSetting)

    @classmethod
    def is_setting(cls, message: Message) -> bool:
        """Is this message a setting?

        Args:
            message (Message): Message to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return type(message) in (BleSetting, HttpSetting)

    @classmethod
    def is_status(cls, message: Message) -> bool:
        """Is this message a status?

        Args:
            message (Message): Message to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return isinstance(message, BleStatus)

    @classmethod
    def is_command(cls, message: Message) -> bool:
        """Is this message a command (i.e. not setting or status)?

        Args:
            message (Message): Message to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return isinstance(message, (BoundFunctionWrapper, CompoundCommand))

    @classmethod
    def is_compound_command(cls, message: Message) -> bool:
        """Is this message a compound command (i.e. a series of commands only used in the GUI)?

        Args:
            message (Message): Message to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return isinstance(message, CompoundCommand)

    @classmethod
    @no_type_check
    def get_args_info(cls, message: Message) -> tuple[list[str], list[type]]:
        """Get the argument names and types for a given message

        Args:
            message (Message): Message to analyze

        Returns:
            tuple[list[str], list[type]]: (list[argument names], list[argument types])
        """
        arg_types: list[type] = []
        arg_names: list[str] = []
        method_info = inspect.getfullargspec(message if (is_command := cls.is_command(message)) else message.set)
        for arg in method_info.kwonlyargs if is_command else method_info.args[1:]:
            if arg.startswith("_"):
                continue
            try:
                # Assume this is a generic and try to get the standard type of its original class
                arg_type = re.search(r"\[.*\]", str(message.__orig_class__))[0].strip("[]")
            except AttributeError:
                # This is not a generic so use the annotations from inspect
                arg_type = method_info.annotations[arg]

            # TODO temporary workaround to avoid handling parameter sequences. This is not an actual solution
            if "optional" in arg_type.lower():
                continue
            arg_types.append(eval(arg_type))  # pylint: disable = eval-used
            arg_names.append(arg)
        return arg_names, arg_types

    def get_message_info(self, message: Message) -> tuple[list[Callable], list[Callable], list[type], list[str]]:
        """For a given message, get its adapters, validator, argument types, and argument names

        Args:
            message (Message): Message to analyze

        Raises:
            ValueError: unhandled type of argument

        Returns:
            tuple[list[Callable], list[Callable], list[type], list[str]]:
                (list[adapters], list[validators], list[arg_types], list[arg_names])
        """
        adapters: list[Callable] = []
        validators: list[Callable] = []
        names, arg_types = self.get_args_info(message)

        # Build adapters and validators
        # NOTE! These lambdas must define default variables since they are lost once the for loop scope exits
        for arg_type in arg_types:
            if "enum" in str(arg_type).lower():
                try:
                    format_field = message.param_builder.fmtstr  # type: ignore
                    for construct_field in (construct.Int8ub, construct.Int32ub, construct.Int16ub):
                        if construct_field.fmtstr == format_field:
                            validators.append(lambda x, cs=construct_field: cs.build(int(x)))
                            adapters.append(lambda x, adapt=arg_type: adapt[x])
                            break
                    else:
                        raise ValueError("unrecognized format field" + str(format_field))
                except AttributeError:
                    validators.append(lambda x, adapt=arg_type: adapt(x))
                    adapters.append(lambda x, adapt=arg_type: adapt[x])
            elif arg_type is datetime.datetime:
                # Special case to be handled by controller
                adapters.append(datetime.datetime)
                validators.append(datetime.datetime)
            else:
                validators.append(lambda _: True)
                if arg_type is bool:
                    adapters.append(lambda x: bool(x.lower() == "true"))
                if arg_type in [bytes, bytearray]:  # type: ignore
                    adapters.append(lambda x, adapt=arg_type: adapt(x, "utf-8"))
                else:
                    adapters.append(lambda x, adapt=arg_type: adapt(x))

        return adapters, validators, arg_types, names

    def updates(
        self, response: Optional[GoProResp] = None
    ) -> Generator[tuple[enum.IntEnum, Any, GoProModel.Update], None, None]:
        """Generate updates from a response or any asynchronous updates

        Args:
            response (Optional[GoProResp], optional): Response to analyze. If none, get all asynchronous
                updates. Defaults to None.

        Yields:
            Generator[tuple[enum.IntEnum, Any, GoProModel.Update], None, None]: generates (updates identifier,
                update value, update type)
        """

        def get_update_type(container: GoProResp, identifier: types.ResponseType) -> GoProModel.Update:
            if container.protocol is GoProResp.Protocol.BLE:
                if container.identifier in [
                    constants.QueryCmdId.GET_CAPABILITIES_VAL,
                    constants.QueryCmdId.REG_CAPABILITIES_UPDATE,
                    constants.QueryCmdId.SETTING_CAPABILITY_PUSH,
                ]:
                    return GoProModel.Update.CAPABILITY
                if container.identifier in [
                    constants.QueryCmdId.GET_SETTING_VAL,
                    constants.QueryCmdId.REG_SETTING_VAL_UPDATE,
                    constants.QueryCmdId.SETTING_VAL_PUSH,
                ]:
                    return GoProModel.Update.SETTING
                if container.identifier in [
                    constants.QueryCmdId.GET_STATUS_VAL,
                    constants.QueryCmdId.REG_STATUS_VAL_UPDATE,
                    constants.QueryCmdId.STATUS_VAL_PUSH,
                ]:
                    return GoProModel.Update.STATUS
                # Must be protobuf
                return GoProModel.Update.PROTOBUF
            if container.protocol is GoProResp.Protocol.HTTP:
                if isinstance(identifier, constants.StatusId):
                    return GoProModel.Update.STATUS
                if isinstance(identifier, constants.SettingId):
                    return GoProModel.Update.SETTING
                raise TypeError(f"Received unexpected WiFi identifier: {identifier}")
            raise TypeError(f"Received unexpected protocol {container.protocol}")

        if isinstance(response, GoProResp):
            for identifier, value in response.data():
                if type(identifier) in (constants.SettingId, constants.StatusId):
                    yield identifier, value, get_update_type(response, identifier)
        elif response is None:
            # TODO need to update to new method. This is broken
            while update := self.gopro.get_notification(0):  # type: ignore
                for identifier, value in update.items():
                    yield identifier, value, get_update_type(update, identifier)


class CompoundCommand(Message):
    """Functionality that consists of multiple BLE and / or Wifi Messages"""

    def __init__(self, communicator: WirelessGoPro, identifier: Any, parser: Any = None) -> None:
        self._communicator = communicator
        super().__init__(identifier, parser)

    def __str__(self) -> str:
        return self._identifier

    def _as_dict(self, *_: Any, **kwargs: Any) -> types.JsonDict:
        """Return the command as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any) : additional dict keys to append

        Returns:
            types.JsonDict: Message as dict
        """
        return {"protocol": "Complex", "id": self._identifier} | kwargs


# pylint: disable = missing-class-docstring, arguments-differ
class CompoundCommands(Messages[CompoundCommand, str, Union[GoProBle, GoProHttp]]):
    """The container for the compound commands"""

    def __init__(self, communicator: WirelessGoPro) -> None:
        """Constructor

        Args:
            communicator (WirelessGoPro): the communicator to send the commands
        """

        class LiveStream(CompoundCommand):
            async def __call__(  # type: ignore
                self,
                *,
                ssid: str,
                password: str,
                url: str,
                window_size: proto.EnumWindowSize,
                lens_type: proto.EnumLens,
                min_bit: int,
                max_bit: int,
                start_bit: int,
            ) -> GoProResp:
                """Disable shutter, connect to WiFi, start livestream, and set shutter

                Args:
                    ssid (str): SSID to connect to
                    password (str): password of WiFi network
                    url (str): url used to stream. Set to empty string to invalidate/cancel stream
                    window_size (open_gopro.api.proto.EnumWindowSize): Streaming video resolution
                    lens_type (open_gopro.api.proto.EnumLens): Streaming Field of View
                    min_bit (int): Desired minimum streaming bitrate (>= 800)
                    max_bit (int): Desired maximum streaming bitrate (<= 8000)
                    start_bit (int): Initial streaming bitrate (honored if 800 <= value <= 8000)

                Returns:
                    GoProResp: status and url to start livestream
                """
                await self._communicator.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)
                await self._communicator.ble_command.register_livestream_status(
                    register=[proto.EnumRegisterLiveStreamStatus]
                )

                await self._communicator.connect_to_access_point(ssid, password)

                # Start livestream
                await self._communicator.ble_command.set_livestream_mode(
                    url=url,
                    window_size=window_size,
                    cert=bytes(),
                    minimum_bitrate=min_bit,
                    maximum_bitrate=max_bit,
                    starting_bitrate=start_bit,
                    lens=lens_type,
                )

                live_stream_ready = asyncio.Event()

                async def wait_for_livestream_ready(_: Any, value: proto.NotifyLiveStreamStatus) -> None:
                    if value.live_stream_status == proto.EnumLiveStreamStatus.LIVE_STREAM_STATE_READY:
                        live_stream_ready.set()

                self._communicator.register_update(
                    wait_for_livestream_ready, constants.ActionId.LIVESTREAM_STATUS_NOTIF
                )
                logger.info("Starting livestream")
                assert (await self._communicator.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)).ok
                logger.info("Waiting for livestream to be ready...\n")
                await live_stream_ready.wait()

                assert self._communicator.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)

                return GoProResp(
                    protocol=GoProResp.Protocol.BLE,
                    status=constants.ErrorCode.SUCCESS,
                    data=None,
                    identifier="LiveStream",
                )

        self.livestream = LiveStream(communicator, "Livestream")

        super().__init__(communicator)
