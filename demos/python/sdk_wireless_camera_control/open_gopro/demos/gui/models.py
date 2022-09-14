# models.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Aug 17 20:05:18 UTC 2022

"""GUI models and associated common functionality"""

# pylint: disable = reimported, unused-import
# NOTE! The reason for the seemingly redundant, unnecessary import here is because we are using eval
# to dynamically  build commands

from __future__ import annotations
import re
import enum
import time
import logging
import inspect
from pathlib import Path
import datetime
import typing
from typing import Pattern, Any, Callable, Generator, Optional, no_type_check, Union, Final

import construct

from open_gopro import GoPro, constants
from open_gopro.api import BleStatus, WifiSetting, BleSetting
from open_gopro.interface import BleCommand, WifiCommand, Commands, Command
import open_gopro.api.params
import open_gopro.api.params as Params
from open_gopro.responses import GoProResp, ResponseType

PREVIEW_STREAM_URL: Final = r"udp://127.0.0.1:8554"

logger = logging.getLogger(__name__)


class CompoundGoPro(GoPro):
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

    def start(self, identifier: Optional[Pattern]) -> None:
        """Open the model (i.e. connect BLE and Wifi to camera)

        Args:
            identifier (Optional[Pattern]): regex to connect to. Defaults to None (connect to first camera)
        """
        # Reinstantiate
        self.gopro = CompoundGoPro(target=identifier)
        self.gopro.open()

    # NOTE: the following properties must be evaluated dynamically since self.gopro is changing

    @property
    def _command_types(self) -> list[Commands]:
        """Get the top level containers of the command types supported by the GoPro model

        Returns:
            list[Commands]: list of command type containers
        """
        return [
            self.gopro.ble_command,
            self.gopro.ble_setting,
            self.gopro.ble_status,
            self.gopro.wifi_command,
            self.gopro.wifi_setting,
            self.gopro.compound_command,
        ]

    @property
    def commands(self) -> list[Command]:
        """Get all of the available BLE and Wifi Commands

        Returns:
            list[Command]: list of available commands
        """
        commands = []
        for command_type in self._command_types:
            c = list(command_type)
            c.sort(key=lambda x: str(x))
            commands.extend(c)
        return commands

    @property
    def command_dict(self) -> dict[str, list[str]]:
        """Get flattened dictionary of commands indexed by their string name

        Returns:
            dict[str, list[str]]: flattened dict
        """
        d = {}
        for commands in self._command_types:
            d[type(commands).__name__] = [str(command) for command in commands]
            d[type(commands).__name__].sort()
        return d

    @classmethod
    def is_ble(cls, command: Command) -> bool:
        """Is this command a BLE command?

        Args:
            command (Command): command to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return type(command) in (BleSetting, BleStatus, BleCommand)

    @classmethod
    def is_wifi(cls, command: Command) -> bool:
        """Is this command a Wifi Command?

        Args:
            command (Command): command to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return type(command) in (WifiCommand, WifiSetting)

    @classmethod
    def is_setting(cls, command: Command) -> bool:
        """Is this command a setting?

        Args:
            command (Command): command to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return type(command) in (BleSetting, WifiSetting)

    @classmethod
    def is_status(cls, command: Command) -> bool:
        """Is this command a status?

        Args:
            command (Command): command to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return isinstance(command, BleStatus)

    @classmethod
    def is_command(cls, command: Command) -> bool:
        """Is this command a command (i.e. not setting or status)?

        Args:
            command (Command): command to analyze

        Returns:
            bool: True if yes, False otherwise
        """
        return (
            isinstance(command, (BleCommand, WifiCommand, CompoundCommand))
            and not cls.is_status(command)
            and not cls.is_setting(command)
        )

    @classmethod
    @no_type_check
    def get_args_info(cls, command: Command) -> tuple[list[str], list[type]]:
        """Get the argument names and types for a given command

        Args:
            command (Command): command to analyze

        Returns:
            tuple[list[str], list[type]]: (list[argument names], list[argument types])
        """
        arg_types: list[type] = []
        arg_names: list[str] = []
        method_info = inspect.getfullargspec(command if cls.is_command(command) else command.set)
        for arg in method_info.args[1:]:
            try:
                # Assume this is a generic and try to get the generic type of its original class
                arg_type = re.search(r"\[.*\]", str(command.__orig_class__))[0].strip("[]")
            except AttributeError:
                # This is not a generic so use the annotations from inspect
                arg_type = method_info.annotations[arg]

            # TODO temporary workaround to avoid handling parameter sequences. This is not an actual solution
            if "optional" in arg_type.lower():
                continue
            arg_types.append(eval(arg_type))  # pylint: disable = eval-used
            arg_names.append(arg)
        return arg_names, arg_types

    def get_command_info(
        self, command: Command
    ) -> tuple[list[Callable], list[Callable], list[type], list[str]]:
        """For a given command, get its adapters, validator, argument types, and argument names

        Args:
            command (Command): command to analyze

        Raises:
            Exception: unhandled type of argument

        Returns:
            tuple[list[Callable], list[Callable], list[type], list[str]]:
                (list[adapters], list[validators], list[arg_types], list[arg_names])
        """
        adapters: list[Callable] = []
        validators: list[Callable] = []
        names, arg_types = self.get_args_info(command)

        # Build adapters and validators
        # NOTE! These lambdas must define default variables since they are lost once the for loop scope exits
        for arg_type in arg_types:
            if "enum" in str(arg_type).lower():
                try:
                    format_field = command.param_builder.fmtstr  # type: ignore
                    for construct_field in (construct.Int8ub, construct.Int32ub):
                        if construct_field.fmtstr == format_field:
                            validators.append(lambda x, cs=construct_field: cs.build(int(x)))
                            adapters.append(lambda x, adapt=arg_type: adapt[x])
                            break
                    else:
                        raise Exception("unrecognized format field" + str(format_field))
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

        def get_update_type(container: GoProResp, identifier: ResponseType) -> GoProModel.Update:
            if container.protocol is GoProResp.Protocol.BLE:
                if container.cmd in [
                    constants.QueryCmdId.GET_CAPABILITIES_VAL,
                    constants.QueryCmdId.REG_CAPABILITIES_UPDATE,
                    constants.QueryCmdId.SETTING_CAPABILITY_PUSH,
                ]:
                    return GoProModel.Update.CAPABILITY
                if container.cmd in [
                    constants.QueryCmdId.GET_SETTING_VAL,
                    constants.QueryCmdId.REG_SETTING_VAL_UPDATE,
                    constants.QueryCmdId.SETTING_VAL_PUSH,
                ]:
                    return GoProModel.Update.SETTING
                if container.cmd in [
                    constants.QueryCmdId.GET_STATUS_VAL,
                    constants.QueryCmdId.REG_STATUS_VAL_UPDATE,
                    constants.QueryCmdId.STATUS_VAL_PUSH,
                ]:
                    return GoProModel.Update.STATUS
                # Must be protobuf
                return GoProModel.Update.PROTOBUF
            if container.protocol is GoProResp.Protocol.WIFI:
                if isinstance(identifier, constants.StatusId):
                    return GoProModel.Update.STATUS
                if isinstance(identifier, constants.SettingId):
                    return GoProModel.Update.SETTING
                raise TypeError(f"Received unexpected WiFi identifier: {identifier}")
            raise TypeError(f"Received unexpected protocol {container.protocol}")

        if isinstance(response, GoProResp):
            for identifier, value in response.items():
                if type(identifier) in (constants.SettingId, constants.StatusId):
                    yield identifier, value, get_update_type(response, identifier)
        elif response is None:
            while update := self.gopro.get_notification(0):
                for identifier, value in update.items():
                    yield identifier, value, get_update_type(update, identifier)


class CompoundCommand(Command):
    """Functionality that consists of multiple BLE and / or Wifi commands"""

    def __str__(self) -> str:
        return self._identifier

    def _as_dict(self, *_: Any, **kwargs: Any) -> dict[str, Any]:
        """Return the command as a dict

        Args:
            *_ (Any): unused
            **kwargs (Any) : additional dict keys to append

        Returns:
            dict[str, Any]: command as dict
        """
        return dict(protocol="Complex", id=self._identifier) | kwargs


# pylint: disable = missing-class-docstring
class CompoundCommands(Commands):
    """The container for the compound commands"""

    def __init__(self, communicator: GoPro) -> None:
        """Constructor

        Args:
            communicator (GoPro): the communicator to send the commands
        """

        class LiveStream(CompoundCommand):
            def __call__(
                self,
                ssid: str,
                password: str,
                url: str,
                window_size: Params.WindowSize,
                lens_type: Params.LensType,
                min_bit: int,
                max_bit: int,
                start_bit: int,
            ) -> GoProResp:
                """Disable shutter, connect to WiFi, start livestream, and set shutter

                Args:
                    ssid (str): SSID to connect to
                    password (str): password of WiFi network
                    url (str): url used to stream. Set to empty string to invalidate/cancel stream
                    window_size (open_gopro.api.params.WindowSize): Streaming video resolution
                    lens_type (open_gopro.api.params.LensType): Streaming Field of View
                    min_bit (int): Desired minimum streaming bitrate (>= 800)
                    max_bit (int): Desired maximum streaming bitrate (<= 8000)
                    start_bit (int): Initial streaming bitrate (honored if 800 <= value <= 8000)

                Raises:
                    RuntimeError: Failed to connect Wifi or start livestream

                Returns:
                    GoProResp: status and url to start livestream
                """
                self._communicator.ble_command.set_shutter(Params.Toggle.DISABLE)

                self._communicator.ble_command.register_livestream_status([Params.RegisterLiveStream.STATUS])

                wifi_connected = False
                for retry in range(1, 5):
                    # Connect as STA
                    response = self._communicator.ble_command.request_wifi_connect(ssid, password)
                    assert response.is_ok
                    timeout = response["timeoutSeconds"] + 2

                    # Wait for connection
                    start = time.time()
                    while update := self._communicator.get_notification(timeout):
                        if update == constants.ActionId.NOTIF_PROVIS_STATE:
                            if (status := update["provisioningState"]) == Params.ProvisioningState.STARTED:
                                continue
                            if status == Params.ProvisioningState.SUCCESS_NEW_AP:
                                wifi_connected = True
                            else:  # This must be an error state
                                logger.warning(f"Received connect error {str(status)}")
                            break

                        if time.time() - start > timeout:
                            logger.warning("Received connect timeout")
                            break

                    if wifi_connected:
                        break
                    # We didn't receive a wifi update. Resend the connect
                    logger.warning(f"Connection to Wifi AP failed Retrying #{retry}")

                if not wifi_connected:
                    raise RuntimeError("Failed to connect to Wifi network")

                livestream_ready = False
                for retry in range(1, 3):
                    # Configure livestream
                    start = time.time()
                    response = self._communicator.ble_command.set_livestream_mode(
                        url=url,
                        window_size=window_size,
                        cert=bytes([0]),
                        minimum_bitrate=min_bit,
                        maximum_bitrate=max_bit,
                        starting_bitrate=start_bit,
                        lens=lens_type,
                    )

                    # We assume the livestream status will always eventually come
                    while update := self._communicator.get_notification():
                        if update == constants.ActionId.LIVESTREAM_STATUS_NOTIF:
                            if (status := update["liveStreamStatus"]) in [
                                Params.LiveStreamStatus.CONFIG,
                                Params.LiveStreamStatus.IDLE,
                            ]:
                                continue
                            if status == Params.LiveStreamStatus.READY:
                                livestream_ready = True
                            else:  # This must be an error state
                                logger.warning(f"Received livestream error {str(status)}")
                            break

                    if livestream_ready:
                        break
                    logger.warning(f"Failed to start livestream. Retrying #{retry}")

                if not livestream_ready:
                    raise RuntimeError("Failed to start livestream")

                # Start livestream
                self._communicator.ble_command.set_shutter(Params.Toggle.ENABLE)

                response = GoProResp(meta=["Livestream"], raw_packet=dict(url=url))
                response._parse()
                return response

        self.livestream = LiveStream(communicator, "Livestream")

        super().__init__(communicator)
