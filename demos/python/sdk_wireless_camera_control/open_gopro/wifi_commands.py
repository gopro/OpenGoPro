# wifi_commands.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Builds HTTP commands and defines parsing for anything sent over WiFi."""

import enum
import logging
from pathlib import Path
from abc import abstractmethod, ABC
from typing import Any, Optional, Dict, Callable

import wrapt
import requests

from open_gopro import params
from open_gopro.responses import GoProResp, ParserType, Parser
from open_gopro.constants import SettingId, StatusId

logger = logging.getLogger(__name__)


class WifiCommunicator(ABC):
    """Interface definition for a client to communicate via WiFi.

    This interface is used to build commands parse responses for:
    - :py:class:`open_gopro.wifi_commands.WifiCommands`
    - :py:class:`open_gopro.wifi_commands.WifiSettings`
    - :py:class:`open_gopro.wifi_commands.WifiStatuses`
    """

    @abstractmethod
    def get(self, url: str) -> GoProResp:
        """Send an HTTP GET request to a string endpoint.

        Args:
            url (str): endpoint not including GoPro base path

        Returns:
            GoProResp: GoPro response
        """
        raise NotImplementedError

    @abstractmethod
    def stream_to_file(self, url: str, file: Path) -> None:
        """Send an HTTP GET request to an Open GoPro endpoint to download a binary file.

        Args:
            url (str): endpoint URL
            file (Path): location where file should be downloaded to
        """
        raise NotImplementedError


# ======================================================Framework Builders==================================


def get_json(endpoint: str, response_parser: ParserType = None) -> Callable:
    """Build a command to send a GET HTTP request and return JSON response as GoProResp.

    Args:
        endpoint (str): endpoint to GET
        response_parser (ParserType, optional): Optional additional parsing to be done on the response data. Defaults to None.

    Returns:
        Callable: function to send GET request
    """

    @wrapt.decorator
    # pylint: disable = E, W
    def _wrapper(wrapped, instance, args, _):  # type: ignore
        logger.info(f'<----------- {wrapped.__name__} : {" ".join([str(x) for x in list(args)])}')

        if response_parser is not None:
            GoProResp.parser_map[endpoint] = response_parser

        # Build list of args as they should be represented in URL
        url_params = []
        for arg in args:
            if issubclass(type(arg), enum.Enum):
                url_params.append(arg.value)
            else:
                url_params.append(arg)
        url = endpoint.format(*url_params)
        # Send to camera
        response = instance.communicator.get(url)
        logger.info(f"-----------> \n{response}")
        return response

    return _wrapper


def get_binary(endpoint: str) -> Callable:
    """Build a command to send a GET HTTP request and receive a binary file.

    Args:
        endpoint (str): endpoint to GET

    Returns:
        Callable: function to send GET request
    """

    @wrapt.decorator
    # pylint: disable = E, W
    def _wrapper(wrapped, instance, _, kwargs):  # type: ignore
        logger.info(f'<----------- {wrapped.__name__} : {" ".join([str(x) for x in list(kwargs.values())])}')
        camera_file = kwargs["camera_file"]
        try:
            local_file = Path(kwargs["local_file"])
        except KeyError:
            local_file = Path(".") / f"{wrapped.__name__}-{camera_file}"

        url = endpoint.format(camera_file)
        # Send to camera
        try:
            instance.communicator.stream_to_file(url, local_file)
        except requests.exceptions.HTTPError as e:
            logger.error(repr(e))
        else:
            logger.info("-----------> SUCCESS")
        return local_file

    return _wrapper


@wrapt.decorator
# pylint: disable = E, W
def setter_cmd(wrapped, instance, args, _):  # type: ignore
    """Build a WiF i command that sets a Setting value."""
    logger.info(f"<----------- {wrapped.__name__} : {' '.join([str(a) for a in args])}")
    # Build url
    url = "gopro/camera/setting?setting_id={}&opt_value={}".format(instance.id.value, args[0].value)
    # Send to camera
    response = instance.communicator.get(url)
    if response is not None:
        logger.info(f"-----------> \n{response}")
    return response


# ======================================================Commands============================================


class ParseCameraState(Parser):
    """Additional parsing to do on received camera state."""

    def parse(self, json: Dict[str, Any]) -> Dict[Any, Any]:
        """Parse the raw state values into user friendly types / values.

        Args:
            json (Dict[str, Any]): input dict to parse

        Returns:
            Dict[Any, Any]: parsed output dict
        """
        parsed: Dict[Any, Any] = {}
        # Parse status and settings values into nice human readable things
        for (name, id_map) in [("status", StatusId), ("settings", SettingId)]:
            for k, v in json[name].items():
                id = id_map(int(k))
                try:
                    parser = GoProResp.parser_map[id]
                    # GreedyBytes, GreedyString, etc can't be built since they don't have a length
                    val = v if "Greedy" in str(parser) else parser.parse(parser.build(v))  # type: ignore
                except KeyError:
                    logger.warning(f"unparsed {name}: {id}")
                    val = v
                parsed[id] = val

        return parsed


class WifiCommands:
    """All of the Wifi commands.

    To be used as a delegate for a WifiCommunicator to build commands

    All of these return a GoProResp

    Args:
        communicator (WifiCommunicator): [description]
    """

    def __init__(self, communicator: WifiCommunicator):
        self.communicator = communicator

    @get_json("gp/gpControl/command/set_client_info")
    def set_third_party_client_info(self) -> GoProResp:
        """Flag as third party app."""

    @get_json("gopro/camera/digital_zoom?percent={}")
    def set_digital_zoom(self, zoom: int, /) -> GoProResp:
        """Set digital zoom in percent (0 to 100)."""

    @get_json("gopro/media/list")
    def get_media_list(self) -> GoProResp:
        """Get a list of media on the camera."""

    @get_json("gopro/version")
    def get_version(self) -> GoProResp:
        """Get Open GoPro version."""

    @get_json("gopro/camera/presets/get")
    def get_preset_status(self) -> GoProResp:
        """Get current Preset status."""

    @get_json("gopro/camera/presets/load?id={}")
    def set_preset(self, preset: params.Preset, /) -> GoProResp:
        """Set the active preset."""

    @get_json("gopro/camera/presets/set_group?id={}")
    def set_preset_group(self, group: params.PresetGroup, /) -> GoProResp:
        """Load a preset group."""

    @get_json("gopro/camera/stream/start")
    def start_preview_stream(self) -> GoProResp:
        """Start the preview stream."""

    @get_json("gopro/camera/stream/stop")
    def stop_preview_stream(self) -> GoProResp:
        """Stop the preview stream."""

    @get_json("gopro/media/info?path=100GOPRO/{}")
    def get_media_info(self, file: str, /) -> GoProResp:
        """Get media info for a file."""

    @get_json("gopro/camera/state", response_parser=ParseCameraState())
    def get_camera_state(self) -> GoProResp:
        """Get camera status and settings."""

    @get_json("gopro/media/turbo_transfer?p={}")
    def set_turbo_mode(self, enable: params.Toggle, /) -> GoProResp:
        """Enable / disable turbo mode."""

    @get_binary("gopro/media/gpmf?path=100GOPRO/{}")
    def get_gpmf_data(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Get GPMF data for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

    @get_binary("gopro/media/screennail?path=100GOPRO/{}")
    def get_screennail(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Get screennail for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

    @get_binary("gopro/media/telemetry?path=100GOPRO/{}")
    def get_telemetry(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Get telemetry for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

    @get_binary("gopro/media/thumbnail?path=100GOPRO/{}")
    def get_thumbnail(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Get thumbnail for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

    @get_binary("videos/DCIM/100GOPRO/{}")
    def download_file(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Download a video from the camera to a local file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """


# =====================================================Settings============================================


class Setting(ABC):
    """An individual camera setting.

    Args:
        communicator (WifiCommunicator): Adapter to read write settings data
        id (SettingId): ID of setting
    """

    def __init__(self, communicator: WifiCommunicator, id: SettingId) -> None:
        self.id = id
        self.communicator = communicator

    @abstractmethod
    def set(self) -> GoProResp:
        """Set the value of the setting.

        This shall be implemented (and documented) by the subclass.

        Returns:
            GoProResp: Status of set
        """
        raise NotImplementedError


class WifiSettings:
    """The collection of all Settings.

    Args:
        communicator (WifiCommunicator): Adapter to read / write settings
    """

    def __init__(self, communicator: WifiCommunicator):
        self.communicator = communicator

        class Resolution(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, resolution: params.Resolution) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.resolution = Resolution(self.communicator, SettingId.RESOLUTION)
        """Resolution. Set with :py:class:`open_gopro.params.Resolution`"""

        class FOV(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, fov: params.FieldOfView) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.video_field_of_view = FOV(self.communicator, SettingId.VIDEO_FOV)
        """Video FOV. Set with :py:class:`open_gopro.params.FieldOfView`"""

        self.photo_field_of_view = FOV(self.communicator, SettingId.PHOTO_FOV)
        """Photo FOV. Set with :py:class:`open_gopro.params.FieldOfView`"""

        self.multi_shot_field_of_view = FOV(self.communicator, SettingId.MULTI_SHOT_FOV)
        """Multi-shot FOV. Set with :py:class:`open_gopro.params.FieldOfView`"""

        class FPS(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, fps: params.FPS) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.fps = FPS(self.communicator, SettingId.FPS)
        """Frames per second. Set with :py:class:`open_gopro.params.FPS`"""

        class MaxLensMode(Setting):  # pylint: disable=missing-class-docstring
            @setter_cmd
            def set(self, mode: params.MaxLensMode) -> GoProResp:  # pylint: disable=unused-argument
                ...

        self.max_lens_mode = MaxLensMode(self.communicator, SettingId.MAX_LENS_MOD)
        """Enable / disable max lens mod. Set with :py:class:`open_gopro.params.MaxLensMode`"""
