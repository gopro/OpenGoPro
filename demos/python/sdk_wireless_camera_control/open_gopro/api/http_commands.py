# http_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http:/gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""HTTP API for Open GoPro version 2.0"""

# mypy: disable-error-code=empty-body

from __future__ import annotations
import logging
import datetime
from pathlib import Path
from typing import Any, Optional

from open_gopro.interface import GoProHttp, HttpMessage, HttpMessages, MessageRules
from open_gopro.constants import SettingId, StatusId, CmdId
from open_gopro.responses import GoProResp, JsonParser
from open_gopro.api.builders import HttpSetting, http_get_binary_command, http_get_json_command
from . import params as Params

logger = logging.getLogger(__name__)

# pylint: disable = missing-class-docstring
class HttpParsers:
    """The collection of parsers used for additional JSON parsing"""

    class CameraStateParser(JsonParser):
        """Parse integer numbers into Enums"""

        def parse(self, data: dict) -> dict:
            """Parse dict of integer values into human readable (i.e. enum'ed) setting / status map

            Args:
                data (dict): input dict to parse

            Returns:
                dict: output human readable dict
            """
            parsed: dict[Any, Any] = {}
            # Parse status and settings values into nice human readable things
            for (name, id_map) in [("status", StatusId), ("settings", SettingId)]:
                for k, v in data[name].items():
                    identifier = id_map(int(k))
                    try:
                        parsed[identifier] = (
                            container(v) if (container := GoProResp._get_query_container(identifier)) else v  # type: ignore
                        )
                    except ValueError:
                        # This is the case where we receive a value that is not defined in our params.
                        # This shouldn't happen and is either a firmware bug or means the documentation needs to
                        # be updated. However, it isn't functionally critical.
                        logger.warning(f"{identifier.name} does not contain a value {v}")
                        parsed[identifier] = v
            return parsed

    class MediaListParser(JsonParser):
        """Extract the list of files from the media list JSON"""

        def parse(self, data: dict) -> dict:
            """Get the list of files from the media list

            Args:
                data (dict): media list response

            Returns:
                dict: list of files
            """
            return {"files": data["media"][0]["fs"] if data["media"] else []}


class HttpCommands(HttpMessages[HttpMessage, CmdId]):
    """All of the HTTP commands.

    To be used as a delegate for a GoProHttp to build commands
    """

    #####################################################################################################
    #                         HTTP GET JSON COMMANDS
    #####################################################################################################

    @http_get_json_command(endpoint="gopro/camera/digital_zoom", arguments=["percent"])
    def set_digital_zoom(self, *, percent: int) -> GoProResp:
        """Set digital zoom in percent.

        Args:
            percent (int): Desired zoom as a percentage

        Returns:
            GoProResp: command status
        """

    @http_get_json_command(
        endpoint="gopro/camera/state",
        parser=HttpParsers.CameraStateParser(),
        rules={MessageRules.FASTPASS: lambda **kwargs: True},
    )
    def get_camera_state(self) -> GoProResp:
        """Get all camera statuses and settings

        Returns:
            GoProResp: status and settings as JSON
        """

    @http_get_json_command(endpoint="gopro/camera/keep_alive")
    def set_keep_alive(self) -> GoProResp:
        """Send the keep alive signal to maintain the connection.

        Returns:
            GoProResp: command status
        """

    @http_get_json_command(endpoint="gopro/media/info", arguments=["path"])
    def get_media_info(self, *, file: str) -> GoProResp:
        """Get media info for a file.

        Args:
            file (str): Media file to get info for

        Returns:
            GoProResp: Media info as JSON
        """
        return {"path": f"100GOPRO/{file}"}  # type: ignore

    @http_get_json_command(endpoint="gopro/media/list", parser=HttpParsers.MediaListParser())
    def get_media_list(self) -> GoProResp:
        """Get a list of media on the camera.

        Returns:
            GoProResp: Media list JSON structure
        """

    @http_get_json_command(endpoint="gopro/media/turbo_transfer", arguments=["p"])
    def set_turbo_mode(self, *, mode: Params.Toggle) -> GoProResp:
        """Enable or disable Turbo transfer mode.

        Args:
            mode (open_gopro.api.params.Toggle): enable / disable turbo mode

        Returns:
            GoProResp: Status
        """
        return {"p": mode}  # type: ignore

    @http_get_json_command(endpoint="gopro/version")
    def get_open_gopro_api_version(self) -> GoProResp:
        """Get Open GoPro API version

        Returns:
            GoProResp: Open GoPro Version
        """

    @http_get_json_command(endpoint="gopro/camera/presets/get")
    def get_preset_status(self) -> GoProResp:
        """Get status of current presets

        Returns:
            GoProResp: JSON describing currently available presets and preset groups
        """

    @http_get_json_command(endpoint="gopro/camera/presets/load", arguments=["id"])
    def load_preset(self, *, preset: int) -> GoProResp:
        """Set camera to a given preset

        The preset ID can be found from :py:class:`open_gopro.api.http_commands.HttpCommands.get_preset_status`

        Args:
            preset (int): preset to load

        Returns:
            GoProResp: command status
        """
        return {"id": preset}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/presets/set_group", arguments=["id"])
    def load_preset_group(self, *, group: Params.PresetGroup) -> GoProResp:
        """Set the active preset group.

        The most recently used Preset in this group will be set.

        Args:
            group (open_gopro.api.params.PresetGroup): desired Preset Group

        Returns:
            GoProResp: command status
        """
        return {"id": group}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/stream", components=["mode"], identifier="Preview Stream")
    def set_preview_stream(self, *, mode: Params.Toggle) -> GoProResp:
        """Start or stop the preview stream

        Args:
            mode (open_gopro.api.params.Toggle): enable to start or disable to stop

        Returns:
            GoProResp: command status
        """
        return {"mode": "start" if mode is Params.Toggle.ENABLE else "stop"}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/analytics/set_client_info")
    def set_third_party_client_info(self) -> GoProResp:
        """Flag as third party app

        Returns:
            GoProResp: command status
        """

    @http_get_json_command(
        endpoint="gopro/camera/shutter",
        components=["mode"],
        rules={
            MessageRules.FASTPASS: lambda **kwargs: kwargs["shutter"] == Params.Toggle.DISABLE,
            MessageRules.WAIT_FOR_ENCODING_START: lambda **kwargs: kwargs["shutter"] == Params.Toggle.ENABLE,
        },
    )
    def set_shutter(self, *, shutter: Params.Toggle) -> GoProResp:
        """Set the shutter on or off

        Args:
            shutter (open_gopro.api.params.Toggle): on or off (i.e. start or stop encoding)

        Returns:
            GoProResp: command status
        """
        return {"mode": "start" if shutter is Params.Toggle.ENABLE else "stop"}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/control/set_ui_controller", arguments=["p"])
    def set_camera_control(self, *, mode: Params.CameraControl) -> GoProResp:
        """Configure global behaviors by setting camera control (to i.e. Idle, External)

        Args:
            mode (open_gopro.api.params.CameraControl): desired camera control value

        Returns:
            GoProResp: command status
        """
        return {"p": mode}  # type: ignore

    @http_get_json_command(endpoint="gopro/camera/set_date_time", arguments=["date", "time", "tzone", "dst"])
    def set_date_time(
        self, *, date_time: datetime.datetime, tz_offset: int = 0, is_dst: bool = False
    ) -> GoProResp:
        """Update the date and time of the camera

        Args:
            date_time (datetime.datetime): date and time
            tz_offset (int): timezone (as UTC offset). Defaults to 0.
            is_dst (bool): is daylight savings time?. Defaults to False.

        Returns:
            GoProResp: command status
        """
        return {  # type: ignore
            "date": f"{date_time.year}_{date_time.month}_{date_time.day}",
            "time": f"{date_time.hour}_{date_time.minute}_{date_time.second}",
            "tzone": tz_offset,
            "dst": int(is_dst),
        }

    @http_get_json_command(endpoint="gopro/camera/get_date_time")
    def get_date_time(self) -> GoProResp:
        """Get the date and time of the camera (Non timezone / DST aware)

        Returns:
            GoProResp: current date and time on camera
        """

    @http_get_json_command(endpoint="gopro/webcam/status")
    def get_webcam_status(self) -> GoProResp:
        """Get the status of the webcam endpoint

        Returns:
            GoProResp: webcam status
        """

    @http_get_json_command(endpoint="gopro/webcam/version")
    def get_webcam_version(self) -> GoProResp:
        """Get the version of the webcam implementation

        Returns:
            GoProResp: version
        """

    @http_get_json_command(endpoint="gopro/media/hilight/file", arguments=["path", "ms"])
    def add_file_hilight(self, *, file: str, offset: Optional[int] = None) -> GoProResp:
        """Add a hilight to a media file (.mp4)

        Args:
            file (str):  the media to add the hilight to
            offset (Optional[int]): offset in ms from start of media

        Returns:
            GoProResp: command status
        """
        return {"path": f"100GOPRO/{file}", "ms": offset or None}  # type: ignore

    @http_get_json_command(endpoint="gopro/media/hilight/remove", arguments=["path", "ms"])
    def remove_file_hilight(self, *, file: str, offset: Optional[int] = None) -> GoProResp:
        """Remove a hilight from a media file (.mp4)

        Args:
            file (str):  the media to remove the hilight from
            offset (Optional[int]): offset in ms from start of media

        Returns:
            GoProResp: command status
        """
        return {"path": f"100GOPRO/{file}", "ms": offset}  # type: ignore

    @http_get_json_command(endpoint="gopro/webcam/exit")
    def webcam_exit(self) -> GoProResp:
        """Exit the webcam.

        Returns:
            GoProResp: command status
        """

    @http_get_json_command(endpoint="gopro/webcam/preview")
    def webcam_preview(self) -> GoProResp:
        """Start the webcam preview.

        Returns:
            GoProResp: command status
        """

    @http_get_json_command(endpoint="gopro/webcam/start", arguments=["res", "fov"])
    def webcam_start(
        self, *, resolution: Optional[Params.WebcamResolution] = None, fov: Optional[Params.WebcamFOV] = None
    ) -> GoProResp:
        """Start the webcam.

        Args:
            resolution (Optional[open_gopro.api.params.WebcamResolution]): resolution to use. If not set,
                camera default will be used.
            fov (Optional[open_gopro.api.params.WebcamFOV]): field of view to use. If not set, camera
                default will be used.

        Returns:
            GoProResp: command status
        """
        return {"res": resolution, "fov": fov}  # type: ignore

    @http_get_json_command(endpoint="gopro/webcam/stop", rules={MessageRules.FASTPASS: lambda **kwargs: True})
    def webcam_stop(self) -> GoProResp:
        """Stop the webcam.

        Returns:
            GoProResp: command status
        """

    @http_get_json_command(endpoint="gopro/webcam/status")
    def webcam_status(self) -> GoProResp:
        """Get the current status of the webcam

        Returns:
            GoProResp: command status including the webcam status
        """

    @http_get_json_command(endpoint="gopro/camera/control/wired_usb", arguments=["p"])
    def wired_usb_control(self, *, control: Params.Toggle) -> GoProResp:
        """Enable / disable wired usb control

        Args:
            control (params.Toggle): enable or disable

        Returns:
            GoProResp: command status
        """
        return {"p": control}  # type: ignore

    ######################################################################################################
    #                          HTTP GET BINARY COMMANDS
    ######################################################################################################

    @http_get_binary_command(endpoint="gopro/media/gpmf?path=100GOPRO")
    def get_gpmf_data(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Get GPMF data for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path]): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

    @http_get_binary_command(endpoint="gopro/media/screennail?path=100GOPRO")
    def get_screennail__call__(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Get screennail for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path]): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

    @http_get_binary_command(endpoint="gopro/media/thumbnail?path=100GOPRO")
    def get_thumbnail(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Get thumbnail for a file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path]): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

    @http_get_binary_command(endpoint="gopro/media/telemetry?path=100GOPRO")
    def get_telemetry(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Download the telemetry data for a camera file and store in a local file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path]): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """

    @http_get_binary_command(endpoint="videos/DCIM/100GOPRO", identifier="Download File")
    def download_file(self, *, camera_file: str, local_file: Optional[Path] = None) -> Path:
        """Download a video from the camera to a local file.

        If local_file is none, the output location will be the same name as the camera_file.

        Args:
            camera_file (str): filename on camera to operate on
            local_file (Optional[Path]): Location on computer to write output. Defaults to None.

        Returns:
            Path: Path to local_file that output was written to
        """


class HttpSettings(HttpMessages[HttpSetting, SettingId]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all HTTP Settings

    Args:
        communicator (GoProHttp): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProHttp):
        self.resolution: HttpSetting = HttpSetting[Params.Resolution](communicator, SettingId.RESOLUTION)
        """Resolution. Set with :py:class:`open_gopro.api.params.Resolution`"""

        self.fps: HttpSetting = HttpSetting[Params.FPS](communicator, SettingId.FPS)
        """Frames per second. Set with :py:class:`open_gopro.api.params.FPS`"""

        self.auto_off: HttpSetting = HttpSetting[Params.AutoOff](communicator, SettingId.AUTO_OFF)
        """Set the auto off time. Set with :py:class:`open_gopro.api.params.AutoOff`"""

        self.video_field_of_view: HttpSetting = HttpSetting[Params.VideoFOV](communicator, SettingId.VIDEO_FOV)
        """Video FOV. Set with :py:class:`open_gopro.api.params.VideoFOV`"""

        self.photo_field_of_view: HttpSetting = HttpSetting[Params.PhotoFOV](communicator, SettingId.PHOTO_FOV)
        """Photo FOV. Set with :py:class:`open_gopro.api.params.PhotoFOV`"""

        self.multi_shot_field_of_view: HttpSetting = HttpSetting[Params.MultishotFOV](
            communicator, SettingId.MULTI_SHOT_FOV
        )
        """Multi-shot FOV. Set with :py:class:`open_gopro.api.params.MultishotFOV`"""

        self.max_lens_mode: HttpSetting = HttpSetting[Params.MaxLensMode](communicator, SettingId.MAX_LENS_MOD)
        """Enable / disable max lens mod. Set with :py:class:`open_gopro.api.params.MaxLensMode`"""

        self.hypersmooth: HttpSetting = HttpSetting[Params.HypersmoothMode](
            communicator, SettingId.HYPERSMOOTH
        )
        """Set / disable hypersmooth. Set with :py:class:`open_gopro.api.params.HypersmoothMode`"""

        self.video_performance_mode: HttpSetting = HttpSetting[Params.PerformanceMode](
            communicator, SettingId.VIDEO_PERFORMANCE_MODE
        )
        """Video Performance Mode (extended battery, tripod, etc). Set with :py:class:`open_gopro.api.params.PerformanceMode`"""

        self.media_format: HttpSetting = HttpSetting[Params.MediaFormat](communicator, SettingId.MEDIA_FORMAT)
        """Set the media format. Set with :py:class:`open_gopro.api.params.MediaFormat`"""

        self.anti_flicker: HttpSetting = HttpSetting[Params.AntiFlicker](communicator, SettingId.ANTI_FLICKER)
        """Anti Flicker frequency. Set with :py:class:`open_gopro.api.params.AntiFlicker`"""

        self.camera_ux_mode: HttpSetting = HttpSetting[Params.CameraUxMode](
            communicator, SettingId.CAMERA_UX_MODE
        )
        """Camera controls configuration. Set with :py:class:`open_gopro.api.params.CameraUxMode`"""

        self.video_easy_mode: HttpSetting = HttpSetting[Params.Speed](communicator, SettingId.VIDEO_EASY_MODE)
        """Video easy mode speed. Set with :py:class:`open_gopro.api.params.Speed`"""

        self.photo_easy_mode: HttpSetting = HttpSetting[Params.PhotoEasyMode](
            communicator, SettingId.PHOTO_EASY_MODE
        )
        """Night Photo easy mode. Set with :py:class:`open_gopro.api.params.PhotoEasyMode`"""

        self.wifi_band: HttpSetting = HttpSetting[Params.WifiBand](communicator, SettingId.WIFI_BAND)
        """Current WiFi band being used. Set with :py:class:`open_gopro.api.params.WifiBand`"""

        self.star_trail_length: HttpSetting = HttpSetting[Params.StarTrailLength](
            communicator, SettingId.STAR_TRAIL_LENGTH
        )
        """Multi shot star trail length. Set with :py:class:`open_gopro.api.params.StarTrailLength`"""

        self.system_video_mode: HttpSetting = HttpSetting[Params.SystemVideoMode](
            communicator, SettingId.SYSTEM_VIDEO_MODE
        )
        """System video mode. Set with :py:class:`open_gopro.api.params.SystemVideoMode`"""

        self.video_horizon_leveling: HttpSetting = HttpSetting[Params.HorizonLeveling](
            communicator, SettingId.VIDEO_HORIZON_LEVELING
        )
        """Lock / unlock horizon leveling for video. Set with :py:class:`open_gopro.api.params.HorizonLeveling`"""

        self.photo_horizon_leveling: HttpSetting = HttpSetting[Params.HorizonLeveling](
            communicator, SettingId.PHOTO_HORIZON_LEVELING
        )
        """Lock / unlock horizon leveling for photo. Set with :py:class:`open_gopro.api.params.HorizonLeveling`"""

        super().__init__(communicator)
