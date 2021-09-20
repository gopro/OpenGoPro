# wifi_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""WiFi API for Open GoPro version 1.0"""

from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Optional, Type, Dict, Callable

from open_gopro.communication_client import GoProWifi
from open_gopro.constants import SettingId, StatusId
from open_gopro.responses import BytesParserBuilder, GoProResp, JsonParser
from open_gopro.api.builders import WifiSetting, WifiGetJsonNoParams, WifiGetJsonWithParams, WifiGetBinary
from .params import ParamsV1_0 as Params

logger = logging.getLogger(__name__)


class WifiCommandsV1_0:
    # pylint: disable = missing-class-docstring, arguments-differ, useless-super-delegation, missing-return-doc
    """All of the Wifi commands.

    To be used as a delegate for a GoProWifi to build commands

    All of these return a GoProResp

    Args:
        communicator (GoProWifi): [description]
    """

    # TODO refactor this to reuse response parsing
    class _ParseCameraState(JsonParser):
        """Additional parsing to do on received camera state."""

        def parse(
            self, buf: Dict[str, Any], additional_parsers: Dict[Any, BytesParserBuilder] = None
        ) -> Dict[Any, Any]:
            """Parse the raw state values into user friendly types / values.

            Args:
                buf (Dict[str, Any]): input dict to parse
                additional_parsers (Dict[Any, BytesParserBuilder], optional): additional parsers to be used. Defaults to None

            Returns:
                Dict[Any, Any]: parsed output dict
            """
            assert additional_parsers is not None
            parsed: Dict[Any, Any] = {}
            # Parse status and settings values into nice human readable things
            for (name, id_map) in [("status", StatusId), ("settings", SettingId)]:
                for k, v in buf[name].items():
                    identifier = id_map(int(k))
                    try:
                        parser = additional_parsers[identifier]
                        # GreedyBytes, GreedyString, etc can't be built since they don't have a length
                        val = v if "Greedy" in str(parser) else parser.parse(parser.build(v))
                    except KeyError:
                        logger.warning(f"unparsed {name}: {identifier}")
                        val = v
                    except ValueError:
                        logger.warning(f"{identifier} does not contain a value {v}")
                        val = v

                    parsed[identifier] = val

            return parsed

    def __init__(self, communicator: GoProWifi):
        self.communicator = communicator

        # ======================== Classes used to build commands

        class GetJsonFromInt(WifiGetJsonWithParams[int]):
            ...

        class GetJsonFromStr(WifiGetJsonWithParams[str]):
            ...

        class GetJsonFromToggle(WifiGetJsonWithParams[Params.Toggle]):
            ...

        class GetJsonFromPreset(WifiGetJsonWithParams[Params.Preset]):
            ...

        class GetJsonFromPresetGroup(WifiGetJsonWithParams[Params.PresetGroup]):
            ...

        class CameraFileToLocalFile(WifiGetBinary):
            def __call__(self, /, camera_file: str, local_file: Optional[Path] = None) -> Path:
                return super().__call__(camera_file=camera_file, local_file=local_file or camera_file)

        # ======================================== Commands

        self.set_digital_zoom: Callable[[int], GoProResp] = GetJsonFromInt(
            communicator, "gopro/camera/digital_zoom?percent={}"
        )
        """Set digital zoom in percent (0 to 100)."""

        self.get_camera_state = WifiGetJsonNoParams(
            communicator, "gopro/camera/state", response_parser=WifiCommandsV1_0._ParseCameraState()
        )
        """Get camera status and settings."""

        self.set_keep_alive = WifiGetJsonNoParams(communicator, "/gopro/camera/keep_alive")
        """Send the keep alive signal to maintain the connection."""

        self.get_gpmf_data = CameraFileToLocalFile(communicator, "gopro/media/gpmf?path=100GOPRO/{}")
        """Get GPMF data for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

        self.get_media_info = GetJsonFromStr(communicator, "gopro/media/info?path=100GOPRO/{}")
        """Get media info for a file."""

        self.get_media_list = WifiGetJsonNoParams(communicator, "gopro/media/list")
        """Get a list of media on the camera."""

        self.get_screennail = CameraFileToLocalFile(communicator, "gopro/media/screennail?path=100GOPRO/{}")
        """Get screennail for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

        self.get_thumbnail = CameraFileToLocalFile(communicator, "gopro/media/thumbnail?path=100GOPRO/{}")
        """Get thumbnail for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

        self.set_turbo_mode = GetJsonFromToggle(communicator, "/gopro/media/turbo_transfer?p={}")
        """Enable or disable Turbo transfer mode."""

        self.get_open_gopro_api_version = WifiGetJsonNoParams(communicator, "gopro/version")
        """Get Open GoPro version."""

        self.get_preset_status = WifiGetJsonNoParams(communicator, "gopro/camera/presets/get")
        """Get current Preset status."""

        self.set_preset = GetJsonFromPreset(communicator, "gopro/camera/presets/load?id={}")
        """Set the active preset."""

        self.set_preset_group = GetJsonFromPresetGroup(communicator, "gopro/camera/presets/set_group?id={}")
        """Set the active preset group."""

        self.start_preview_stream = WifiGetJsonNoParams(communicator, "gopro/camera/stream/start")
        """Start the preview stream."""

        self.stop_preview_stream = WifiGetJsonNoParams(communicator, "gopro/camera/stream/stop")
        """Stop the preview stream."""

        self.get_telemetry = CameraFileToLocalFile(communicator, "gopro/media/telemetry?path=100GOPRO/{}")

        self.download_file = CameraFileToLocalFile(communicator, "videos/DCIM/100GOPRO/{}")
        """Download a video from the camera to a local file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path], optional): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """


# =====================================================Settings============================================


class WifiSettingsV1_0:
    # pylint: disable=missing-class-docstring
    # pylint: disable=unused-argument
    """The collection of all Settings.

    Args:
        communicator (GoProWifi): Adapter to read / write settings
    """

    class Iterator:
        """Iterator to iterate through a BleSettings instance's attributes

        Does not include the 'communicator' instance.
        """

        def __init__(self, settings: "WifiSettingsV1_0"):
            self._index = 0
            self._setting_attributes = list(settings.__dict__.values())[1:]  # Skip communicator

        def __next__(self) -> WifiSetting:
            """Return the next attribute

            Raises:
                StopIteration: Nothing left to iterate

            Returns:
                Setting: Instance of setting
            """
            if self._index < len(self._setting_attributes):
                setting = self._setting_attributes[self._index]
                self._index += 1
                return setting
            # End of Iteration
            raise StopIteration

    def __init__(
        self,
        communicator: GoProWifi,
        params: Type[Params],
        endpoint: str = "/gopro/camera/setting?setting_id={}&opt_value={}",
    ):
        self.endpoint = endpoint
        self.params = params  # Not currently used but will be in the future

        class Resolution(WifiSetting[Params.Resolution]):
            ...

        self.resolution = Resolution(communicator, SettingId.RESOLUTION)
        """Resolution. Set with :py:class:`open_gopro.Params.Resolution`"""

        class FPS(WifiSetting[Params.FPS]):
            ...

        self.fps = FPS(communicator, SettingId.FPS)
        """Frames per second. Set with :py:class:`open_gopro.Params.FPS`"""

        class AutoOffTime(WifiSetting[Params.AutoOff]):
            ...

        self.auto_off = AutoOffTime(communicator, SettingId.AUTO_OFF)
        """Set the auto off time."""

        class VideoFOV(WifiSetting[Params.VideoFOV]):
            ...

        self.video_field_of_view = VideoFOV(communicator, SettingId.VIDEO_FOV)
        """Video FOV. Set with :py:class:`open_gopro.Params.FieldOfView`"""

        class PhotoFOV(WifiSetting[Params.PhotoFOV]):
            ...

        self.photo_field_of_view = PhotoFOV(communicator, SettingId.PHOTO_FOV)
        """Photo FOV. Set with :py:class:`open_gopro.Params.FieldOfView`"""

        class MultishotFOV(WifiSetting[Params.MultishotFOV]):
            ...

        self.multi_shot_field_of_view = MultishotFOV(communicator, SettingId.MULTI_SHOT_FOV)
        """Multi-shot FOV. Set with :py:class:`open_gopro.Params.FieldOfView`"""

        class MaxLensMode(WifiSetting[Params.MaxLensMode]):
            ...

        self.max_lens_mode = MaxLensMode(communicator, SettingId.MAX_LENS_MOD)
        """Enable / disable max lens mod. Set with :py:class:`open_gopro.Params.MaxLensMode`"""

    def __iter__(self) -> Iterator:
        """Return an iterable of this instance's attributes

        Does not include the 'communicator' attribute

        Returns:
            Iterator: next attribute
        """
        return WifiSettingsV1_0.Iterator(self)
