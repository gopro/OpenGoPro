# http_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http:/gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""HTTP API for Open GoPro version 2.0"""

# mypy: disable-error-code=empty-body

from __future__ import annotations

import datetime
import logging
from pathlib import Path

from open_gopro import proto
from open_gopro.api.builders import (
    HttpSetting,
    http_get_binary_command,
    http_get_json_command,
    http_put_json_command,
)
from open_gopro.api.parsers import JsonParsers
from open_gopro.communicator_interface import (
    GoProHttp,
    HttpMessage,
    HttpMessages,
    MessageRules,
)
from open_gopro.constants import SettingId
from open_gopro.models import CameraInfo, MediaList, MediaMetadata, MediaPath
from open_gopro.models.general import WebcamResponse
from open_gopro.models.response import GoProResp
from open_gopro.parser_interface import Parser
from open_gopro.types import CameraState, JsonDict

from . import params as Params

logger = logging.getLogger(__name__)


class HttpCommands(HttpMessages[HttpMessage]):
    """All of the HTTP commands.

    To be used as a delegate for a GoProHttp to build commands
    """

    @http_get_json_command(endpoint="/gp/gpControl/command/storage/delete/all")
    async def delete_all(self) -> GoProResp[None]:
        """Delete all files on the SD card.

        Returns:
            GoProResp[None]: command status
        """

    @http_get_json_command(endpoint="gopro/media/delete/file", arguments=["path"])
    async def delete_file(self, *, path: str) -> GoProResp[None]:
        """Delete a single file including single files that are part of a group.

        Args:
            path (str): path to file to delete

        Returns:
            GoProResp[None]: command status
        """

    @http_get_json_command(endpoint="/gp/gpControl/command/storage/delete/group", arguments=["p"])
    async def delete_group(self, *, path: str) -> GoProResp[None]:
        """Delete all contents of a group. Should not be used on non-group files.

        Args:
            path (str): path to first file in the group.

        Returns:
            GoProResp[None]: command status
        """
        return {"p": path}  # type: ignore

    @http_get_json_command(
        endpoint="gopro/media/last_captured",
        parser=Parser(json_parser=JsonParsers.PydanticAdapter(MediaPath)),
    )
    async def get_last_captured_media(self) -> GoProResp[MediaPath]:
        """Get the last captured media file.

        Returns:
            GoProResp[MediaPath]: path of last captured media file
        """

    @http_put_json_command(
        endpoint="gopro/camera/presets/update_custom",
        body_args=["custom_name", "icon_id", "title_id"],
    )
    async def update_custom_preset(
        self,
        *,
        icon_id: proto.EnumPresetIcon.ValueType | None = None,
        title_id: str | proto.EnumPresetTitle.ValueType | None = None,
        custom_name: str | None = None,
    ) -> GoProResp[None]:
        """For a custom preset, update the Icon and / or the Title

        Args:
            icon_id (proto.EnumPresetIcon.ValueType | None): Icon to use. Defaults to None.
            title_id (str | proto.EnumPresetTitle.ValueType | None): Title to use. Defaults to None.
            custom_name (str | None): Custom name to use if title_id is set to
                `proto.EnumPresetTitle.PRESET_TITLE_USER_DEFINED_CUSTOM_NAME`. Defaults to None.

        Returns:
            GoProResp[None]: command status
        """

    @http_get_json_command(endpoint="gopro/camera/digital_zoom", arguments=["percent"])
    async def set_digital_zoom(self, *, percent: int) -> GoProResp[None]:
        """Set digital zoom in percent.

        Args:
            percent (int): Desired zoom as a percentage

        Returns:
            GoProResp[None]: command status
        """

    @http_get_json_command(
        endpoint="gopro/camera/state",
        parser=Parser(json_parser=JsonParsers.CameraStateParser()),
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
    )
    async def get_camera_state(self) -> GoProResp[CameraState]:
        """Get all camera statuses and settings

        Returns:
            GoProResp[CameraState]: status and settings as JSON
        """

    @http_get_json_command(
        endpoint="gopro/camera/info", parser=Parser(json_parser=JsonParsers.PydanticAdapter(CameraInfo))
    )
    async def get_camera_info(self) -> GoProResp[CameraInfo]:
        """Get general information about the camera such as firmware version

        Returns:
            GoProResp[CameraInfo]: status and settings as JSON
        """

    @http_get_json_command(endpoint="gopro/camera/keep_alive")
    async def set_keep_alive(self) -> GoProResp[None]:
        """Send the keep alive signal to maintain the connection.

        Returns:
            GoProResp[None]: command status
        """

    @http_get_json_command(
        endpoint="gopro/media/info",
        arguments=["path"],
        parser=Parser(json_parser=JsonParsers.PydanticAdapter(MediaMetadata)),
    )
    async def get_media_metadata(self, *, path: str) -> GoProResp[MediaMetadata]:
        """Get media metadata for a file.

        Args:
            path (str): Path on camera of media file to get metadata for

        Returns:
            GoProResp[MediaMetadata]: Media metadata JSON structure
        """

    @http_get_json_command(
        endpoint="gopro/media/list",
        parser=Parser(json_parser=JsonParsers.PydanticAdapter(MediaList)),
    )
    async def get_media_list(self) -> GoProResp[MediaList]:
        """Get a list of media on the camera.

        Returns:
            GoProResp[MediaList]: Media list JSON structure
        """

    @http_get_json_command(endpoint="gopro/media/turbo_transfer", arguments=["p"])
    async def set_turbo_mode(self, *, mode: Params.Toggle) -> GoProResp[None]:
        """Enable or disable Turbo transfer mode.

        Args:
            mode (Params.Toggle): enable / disable turbo mode

        Returns:
            GoProResp[None]: Status
        """
        return {"p": mode}  # type: ignore

    @http_get_json_command(
        endpoint="gopro/version",
        parser=Parser(json_parser=JsonParsers.LambdaParser(lambda data: f"{data['version']}")),
    )
    async def get_open_gopro_api_version(self) -> GoProResp[str]:
        """Get Open GoPro API version

        Returns:
            GoProResp[str]: Open GoPro Version
        """

    # TODO make pydantic model of preset status
    @http_get_json_command(endpoint="gopro/camera/presets/get")
    async def get_preset_status(self) -> GoProResp[JsonDict]:
        """Get status of current presets

        Returns:
            GoProResp[JsonDict]: JSON describing currently available presets and preset groups
        """

    @http_get_json_command(endpoint="gopro/camera/presets/load", arguments=["id"])
    async def load_preset(self, *, preset: int) -> GoProResp[None]:
        """Set camera to a given preset

        The preset ID can be found from :py:class:`open_gopro.api.http_commands.HttpCommands.get_preset_status`

        Args:
            preset (int): preset to load

        Returns:
            GoProResp[None]: command status
        """
        return {"id": preset}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/presets/set_group", arguments=["id"])
    async def load_preset_group(self, *, group: proto.EnumPresetGroup.ValueType) -> GoProResp[None]:
        """Set the active preset group.

        The most recently used Preset in this group will be set.

        Args:
            group (proto.EnumPresetGroup.ValueType): desired Preset Group

        Returns:
            GoProResp[None]: command status
        """
        return {"id": group}  # type: ignore

    @http_get_json_command(
        endpoint="gopro/camera/stream", arguments=["port"], components=["mode"], identifier="Preview Stream"
    )
    async def set_preview_stream(self, *, mode: Params.Toggle, port: int | None = None) -> GoProResp[None]:
        """Start or stop the preview stream

        Args:
            mode (Params.Toggle): enable to start or disable to stop
            port (int | None): Port to use for Preview Stream. Defaults to 8554 if None.
                Only relevant when starting the stream.

        Returns:
            GoProResp[None]: command status
        """
        return {"mode": "start" if mode is Params.Toggle.ENABLE else "stop", "port": port}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/analytics/set_client_info")
    async def set_third_party_client_info(self) -> GoProResp[None]:
        """Flag as third party app

        Returns:
            GoProResp[None]: command status
        """

    @http_get_json_command(
        endpoint="gopro/camera/shutter",
        components=["mode"],
        rules=MessageRules(
            fastpass_analyzer=lambda **kwargs: kwargs["mode"] == "stop",
            wait_for_encoding_analyzer=lambda **kwargs: kwargs["mode"] == "start",
        ),
    )
    async def set_shutter(self, *, shutter: Params.Toggle) -> GoProResp[None]:
        """Set the shutter on or off

        Args:
            shutter (Params.Toggle): on or off (i.e. start or stop encoding)

        Returns:
            GoProResp[None]: command status
        """
        return {"mode": "start" if shutter is Params.Toggle.ENABLE else "stop"}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/control/set_ui_controller", arguments=["p"])
    async def set_camera_control(self, *, mode: Params.CameraControl) -> GoProResp[None]:
        """Configure global behaviors by setting camera control (to i.e. Idle, External)

        Args:
            mode (Params.CameraControl): desired camera control value

        Returns:
            GoProResp[None]: command status
        """
        return {"p": mode}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/set_date_time", arguments=["date", "time", "tzone", "dst"])
    async def set_date_time(
        self,
        *,
        date_time: datetime.datetime,
        tz_offset: int = 0,
        is_dst: bool = False,
    ) -> GoProResp[None]:
        """Update the date and time of the camera

        Args:
            date_time (datetime.datetime): date and time
            tz_offset (int): timezone (as UTC offset). Defaults to 0.
            is_dst (bool): is daylight savings time?. Defaults to False.

        Returns:
            GoProResp[None]: command status
        """
        return {  # type: ignore
            "date": f"{date_time.year}_{date_time.month}_{date_time.day}",
            "time": f"{date_time.hour}_{date_time.minute}_{date_time.second}",
            "tzone": tz_offset,
            "dst": int(is_dst),
        }

    @http_get_json_command(endpoint="gopro/camera/get_date_time")
    async def get_date_time(self) -> GoProResp[datetime.datetime]:
        """Get the date and time of the camera (Non timezone / DST aware)

        Returns:
            GoProResp[datetime.datetime]: current date and time on camera
        """

    @http_get_json_command(endpoint="gopro/webcam/version")
    async def get_webcam_version(self) -> GoProResp[str]:
        """Get the version of the webcam implementation

        Returns:
            GoProResp[str]: version
        """

    @http_get_json_command(
        endpoint="gopro/media/hilight/file",
        arguments=["path", "ms"],
    )
    async def add_file_hilight(
        self,
        *,
        file: str,
        offset: int | None = None,
    ) -> GoProResp[None]:
        """Add a hilight to a media file (.mp4)

        Args:
            file (str):  the media to add the hilight to
            offset (int | None): offset in ms from start of media

        Returns:
            GoProResp[None]: command status
        """
        return {"path": file, "ms": offset or None}  # type: ignore

    @http_get_json_command(
        endpoint="gopro/media/hilight/remove",
        arguments=["path", "ms"],
    )
    async def remove_file_hilight(
        self,
        *,
        file: str,
        offset: int | None = None,
    ) -> GoProResp[None]:
        """Remove a hilight from a media file (.mp4)

        Args:
            file (str):  the media to remove the hilight from
            offset (int | None): offset in ms from start of media

        Returns:
            GoProResp[None]: command status
        """
        return {"path": file, "ms": offset}  # type: ignore

    @http_get_json_command(
        endpoint="gopro/webcam/exit",
        parser=Parser(json_parser=JsonParsers.PydanticAdapter(WebcamResponse)),
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
    )
    async def webcam_exit(self) -> GoProResp[WebcamResponse]:
        """Exit the webcam.

        Returns:
            GoProResp[WebcamResponse]: command status
        """

    @http_get_json_command(
        endpoint="gopro/webcam/preview",
        parser=Parser(json_parser=JsonParsers.PydanticAdapter(WebcamResponse)),
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
    )
    async def webcam_preview(self) -> GoProResp[WebcamResponse]:
        """Start the webcam preview.

        Returns:
            GoProResp[WebcamResponse]: command status
        """

    @http_get_json_command(
        endpoint="gopro/webcam/start",
        arguments=["res", "fov", "port", "protocol"],
        parser=Parser(json_parser=JsonParsers.PydanticAdapter(WebcamResponse)),
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
    )
    async def webcam_start(
        self,
        *,
        resolution: Params.WebcamResolution | None = None,
        fov: Params.WebcamFOV | None = None,
        port: int | None = None,
        protocol: Params.WebcamProtocol | None = None,
    ) -> GoProResp[WebcamResponse]:
        """Start the webcam.

        Args:
            resolution (Params.WebcamResolution | None): resolution to use. If not set, camera default will be used.
            fov (Params.WebcamFOV | None): field of view to use. If not set, camera default will be used.
            port (int | None): port to use for streaming. If not set, camera default of 8554 will be used.
            protocol (Params.WebcamProtocol | None): streaming protocol to use. If not set, camera default of TS will
                be used.

        Returns:
            GoProResp[WebcamResponse]: command status
        """
        return {"res": resolution, "fov": fov, "port": port, "protocol": protocol}  # type: ignore

    @http_get_json_command(
        endpoint="gopro/webcam/stop",
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
        parser=Parser(json_parser=JsonParsers.PydanticAdapter(WebcamResponse)),
    )
    async def webcam_stop(self) -> GoProResp[WebcamResponse]:
        """Stop the webcam.

        Returns:
            GoProResp[WebcamResponse]: command status
        """

    @http_get_json_command(
        endpoint="gopro/webcam/status",
        parser=Parser(json_parser=JsonParsers.PydanticAdapter(WebcamResponse)),
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
    )
    async def webcam_status(self) -> GoProResp[WebcamResponse]:
        """Get the current status of the webcam

        Returns:
            GoProResp[WebcamResponse]: command status including the webcam status
        """

    @http_get_json_command(
        endpoint="gopro/camera/control/wired_usb",
        arguments=["p"],
    )
    async def wired_usb_control(self, *, control: Params.Toggle) -> GoProResp[None]:
        """Enable / disable wired usb control

        Args:
            control (Params.Toggle): enable or disable

        Returns:
            GoProResp[None]: command status
        """
        return {"p": control}  # type: ignore

    @http_get_binary_command(endpoint="gopro/media/gpmf", arguments=["path"])
    async def get_gpmf_data(self, *, camera_file: str, local_file: Path | None = None) -> GoProResp[Path]:
        """Get GPMF data for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Path | None): Location on computer to write output. Defaults to None.

        Returns:
            GoProResp[Path]: Path to local_file that output was written to
        """

    @http_get_binary_command(endpoint="gopro/media/screennail", arguments=["path"])
    async def get_screennail__call__(self, *, camera_file: str, local_file: Path | None = None) -> GoProResp[Path]:
        """Get screennail for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Path | None): Location on computer to write output. Defaults to None.

        Returns:
            GoProResp[Path]: Path to local_file that output was written to
        """

    @http_get_binary_command(endpoint="gopro/media/thumbnail", arguments=["path"])
    async def get_thumbnail(self, *, camera_file: str, local_file: Path | None = None) -> GoProResp[Path]:
        """Get thumbnail for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Path | None): Location on computer to write output. Defaults to None.

        Returns:
            GoProResp[Path]: Path to local_file that output was written to
        """

    @http_get_binary_command(endpoint="gopro/media/telemetry", arguments=["path"])
    async def get_telemetry(self, *, camera_file: str, local_file: Path | None = None) -> GoProResp[Path]:
        """Download the telemetry data for a camera file and store in a local file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Path | None): Location on computer to write output. Defaults to None.

        Returns:
            GoProResp[Path]: Path to local_file that output was written to
        """

    @http_get_binary_command(endpoint="videos/DCIM", components=["path"], identifier="Download File")
    async def download_file(self, *, camera_file: str, local_file: Path | None = None) -> GoProResp[Path]:
        """Download a video from the camera to a local file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Path | None): Location on computer to write output. Defaults to None.

        Returns:
            GoProResp[Path]: Path to local_file that output was written to
        """


class HttpSettings(HttpMessages[HttpSetting]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all HTTP Settings

    Args:
        communicator (GoProHttp): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProHttp):
        self.resolution: HttpSetting[Params.Resolution] = HttpSetting[Params.Resolution](
            communicator, SettingId.RESOLUTION
        )
        """Resolution."""

        self.fps: HttpSetting[Params.FPS] = HttpSetting[Params.FPS](communicator, SettingId.FPS)
        """Frames per second."""

        self.auto_off: HttpSetting[Params.AutoOff] = HttpSetting[Params.AutoOff](communicator, SettingId.AUTO_OFF)
        """Set the auto off time."""

        self.video_field_of_view: HttpSetting[Params.VideoFOV] = HttpSetting[Params.VideoFOV](
            communicator, SettingId.VIDEO_FOV
        )
        """Video FOV."""

        self.photo_field_of_view: HttpSetting[Params.PhotoFOV] = HttpSetting[Params.PhotoFOV](
            communicator, SettingId.PHOTO_FOV
        )
        """Photo FOV."""

        self.multi_shot_field_of_view: HttpSetting[Params.MultishotFOV] = HttpSetting[Params.MultishotFOV](
            communicator, SettingId.MULTI_SHOT_FOV
        )
        """Multi-shot FOV."""

        self.max_lens_mode: HttpSetting[Params.MaxLensMode] = HttpSetting[Params.MaxLensMode](
            communicator, SettingId.MAX_LENS_MOD
        )
        """Enable / disable max lens mod."""

        self.hypersmooth: HttpSetting[Params.HypersmoothMode] = HttpSetting[Params.HypersmoothMode](
            communicator, SettingId.HYPERSMOOTH
        )
        """Set / disable hypersmooth."""

        self.video_performance_mode: HttpSetting[Params.PerformanceMode] = HttpSetting[Params.PerformanceMode](
            communicator, SettingId.VIDEO_PERFORMANCE_MODE
        )
        """Video Performance Mode (extended battery, tripod, etc)."""

        self.media_format: HttpSetting[Params.MediaFormat] = HttpSetting[Params.MediaFormat](
            communicator, SettingId.MEDIA_FORMAT
        )
        """Set the media format."""

        self.anti_flicker: HttpSetting[Params.AntiFlicker] = HttpSetting[Params.AntiFlicker](
            communicator, SettingId.ANTI_FLICKER
        )
        """Anti Flicker frequency."""

        self.camera_ux_mode: HttpSetting[Params.CameraUxMode] = HttpSetting[Params.CameraUxMode](
            communicator, SettingId.CAMERA_UX_MODE
        )
        """Camera controls configuration."""

        self.video_easy_mode: HttpSetting[int] = HttpSetting[int](communicator, SettingId.VIDEO_EASY_MODE)
        """Video easy mode speed."""

        self.photo_easy_mode: HttpSetting[Params.PhotoEasyMode] = HttpSetting[Params.PhotoEasyMode](
            communicator, SettingId.PHOTO_EASY_MODE
        )
        """Night Photo easy mode."""

        self.wifi_band: HttpSetting[Params.WifiBand] = HttpSetting[Params.WifiBand](communicator, SettingId.WIFI_BAND)
        """Current WiFi band being used."""

        self.star_trail_length: HttpSetting[Params.StarTrailLength] = HttpSetting[Params.StarTrailLength](
            communicator, SettingId.STAR_TRAIL_LENGTH
        )
        """Multi shot star trail length."""

        self.system_video_mode: HttpSetting[Params.SystemVideoMode] = HttpSetting[Params.SystemVideoMode](
            communicator, SettingId.SYSTEM_VIDEO_MODE
        )
        """System video mode."""

        self.video_horizon_leveling: HttpSetting[Params.HorizonLeveling] = HttpSetting[Params.HorizonLeveling](
            communicator, SettingId.VIDEO_HORIZON_LEVELING
        )
        """Lock / unlock horizon leveling for video."""

        self.photo_horizon_leveling: HttpSetting[Params.HorizonLeveling] = HttpSetting[Params.HorizonLeveling](
            communicator, SettingId.PHOTO_HORIZON_LEVELING
        )
        """Lock / unlock horizon leveling for photo."""

        self.bit_rate: HttpSetting[Params.BitRate] = HttpSetting[Params.BitRate](
            communicator,
            SettingId.BIT_RATE,
        )
        """System Video Bit Rate."""

        self.bit_depth: HttpSetting[Params.BitDepth] = HttpSetting[Params.BitDepth](
            communicator,
            SettingId.BIT_DEPTH,
        )
        """System Video Bit depth."""

        self.video_profile: HttpSetting[Params.VideoProfile] = HttpSetting[Params.VideoProfile](
            communicator,
            SettingId.VIDEO_PROFILE,
        )
        """Video Profile (hdr, etc.)"""

        self.video_aspect_ratio: HttpSetting[Params.VideoAspectRatio] = HttpSetting[Params.VideoAspectRatio](
            communicator,
            SettingId.VIDEO_ASPECT_RATIO,
        )
        """Video aspect ratio"""

        self.video_easy_aspect_ratio: HttpSetting[Params.EasyAspectRatio] = HttpSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.VIDEO_EASY_ASPECT_RATIO,
        )
        """Video easy aspect ratio"""

        self.multi_shot_easy_aspect_ratio: HttpSetting[Params.EasyAspectRatio] = HttpSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.MULTI_SHOT_EASY_ASPECT_RATIO,
        )
        """Multi shot easy aspect ratio"""

        self.multi_shot_nlv_aspect_ratio: HttpSetting[Params.EasyAspectRatio] = HttpSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.MULTI_SHOT_NLV_ASPECT_RATIO,
        )
        """Multi shot NLV aspect ratio"""

        self.video_mode: HttpSetting[Params.VideoMode] = HttpSetting[Params.VideoMode](
            communicator,
            SettingId.VIDEO_MODE,
        )
        """Video Mode (i.e. quality)"""

        self.timelapse_mode: HttpSetting[Params.TimelapseMode] = HttpSetting[Params.TimelapseMode](
            communicator,
            SettingId.TIMELAPSE_MODE,
        )
        """Timelapse Mode"""

        self.maxlens_mod_type: HttpSetting[Params.MaxLensModType] = HttpSetting[Params.MaxLensModType](
            communicator,
            SettingId.ADDON_MAX_LENS_MOD,
        )
        """Max lens mod? If so, what type?"""

        self.maxlens_status: HttpSetting[Params.Toggle] = HttpSetting[Params.Toggle](
            communicator,
            SettingId.ADDON_MAX_LENS_MOD_ENABLE,
        )
        """Enable / disable max lens mod"""

        self.photo_mode: HttpSetting[Params.PhotoMode] = HttpSetting[Params.PhotoMode](
            communicator,
            SettingId.PHOTO_MODE,
        )
        """Photo Mode"""

        self.framing: HttpSetting[Params.Framing] = HttpSetting[Params.Framing](
            communicator,
            SettingId.FRAMING,
        )
        """Video Framing Mode"""

        self.hindsight: HttpSetting[Params.Hindsight] = HttpSetting[Params.Hindsight](
            communicator,
            SettingId.HINDSIGHT,
        )
        """Hindsight time / disable"""

        self.photo_interval: HttpSetting[Params.PhotoInterval] = HttpSetting[Params.PhotoInterval](
            communicator,
            SettingId.PHOTO_INTERVAL,
        )
        """Interval between photo captures"""

        self.photo_duration: HttpSetting[Params.PhotoDuration] = HttpSetting[Params.PhotoDuration](
            communicator,
            SettingId.PHOTO_INTERVAL_DURATION,
        )
        """Interval between photo captures"""

        self.photo_output: HttpSetting[Params.PhotoOutput] = HttpSetting[Params.PhotoOutput](
            communicator,
            SettingId.PHOTO_OUTPUT,
        )
        """File type of photo output"""

        self.video_duration: HttpSetting[Params.VideoDuration] = HttpSetting[Params.VideoDuration](
            communicator, SettingId.VIDEO_DURATION
        )
        """If set, a video will automatically be stopped after recording for this long."""

        self.regional_format: HttpSetting[Params.RegionalFormat] = HttpSetting[Params.RegionalFormat](
            communicator, SettingId.REGIONAL_FORMAT
        )

        self.quality_control: HttpSetting[Params.QualityControl] = HttpSetting[Params.QualityControl](
            communicator, SettingId.QUALITY_CONTROL
        )

        self.camera_volume: HttpSetting[Params.Volume] = HttpSetting[Params.Volume](
            communicator, SettingId.CAMERA_VOLUME
        )

        self.lens_attachment: HttpSetting[Params.LensAttachment] = HttpSetting[Params.LensAttachment](
            communicator, SettingId.LENS_ATTACHMENT
        )

        self.setup_screensaver: HttpSetting[Params.ScreenSaverTimeout] = HttpSetting[Params.ScreenSaverTimeout](
            communicator, SettingId.SETUP_SCREEN_SAVER
        )

        self.setup_language: HttpSetting[Params.SetupLanguage] = HttpSetting[Params.SetupLanguage](
            communicator, SettingId.SETUP_LANGUAGE
        )

        self.auto_power_off: HttpSetting[Params.AutoPowerOff] = HttpSetting[Params.AutoPowerOff](
            communicator, SettingId.AUTO_POWER_OFF
        )

        self.photo_mode_v2: HttpSetting[Params.PhotoModeV2] = HttpSetting[Params.PhotoModeV2](
            communicator, SettingId.PHOTO_MODE_V2
        )

        self.video_digital_lens_v2: HttpSetting[Params.VideoLensV2] = HttpSetting[Params.VideoLensV2](
            communicator, SettingId.VIDEO_DIGITAL_LENSES_V2
        )

        self.photo_digital_lens_v2: HttpSetting[Params.PhotoLensV2] = HttpSetting[Params.PhotoLensV2](
            communicator, SettingId.PHOTO_DIGITAL_LENSES_V2
        )

        self.timelapse_digital_lens_v2: HttpSetting[Params.TimelapseLensV2] = HttpSetting[Params.TimelapseLensV2](
            communicator, SettingId.TIMELAPSE_DIGITAL_LENSES_V2
        )

        self.video_framing: HttpSetting[Params.VideoFraming] = HttpSetting[Params.VideoFraming](
            communicator, SettingId.VIDEO_FRAMING
        )

        self.multi_shot_framing: HttpSetting[Params.MultishotFraming] = HttpSetting[Params.MultishotFraming](
            communicator, SettingId.MULTI_SHOT_FRAMING
        )

        self.frame_rate: HttpSetting[Params.FrameRate] = HttpSetting[Params.FrameRate](
            communicator, SettingId.FRAME_RATE
        )

        super().__init__(communicator)
