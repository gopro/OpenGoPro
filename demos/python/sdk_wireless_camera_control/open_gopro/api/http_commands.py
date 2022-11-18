# http_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http:/gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""HTTP API for Open GoPro version 2.0"""

from __future__ import annotations
import logging
import datetime
from pathlib import Path
from typing import Any, Optional

from open_gopro.interface import GoProHttp, HttpCommand, Commands
from open_gopro.constants import SettingId, StatusId, CmdId
from open_gopro.responses import GoProResp, JsonParser
from open_gopro.api.builders import HttpGetJsonCommand, HttpGetBinary, HttpSetting
from . import params as Params

logger = logging.getLogger(__name__)


# TODO check this doc
class HttpCommands(Commands[HttpCommand, CmdId]):
    """All of the HTTP commands.

    To be used as a delegate for a GoProHttp to build commands

    All of these return a GoProResp
    """

    # pylint: disable = missing-class-docstring, arguments-differ, useless-super-delegation
    def __init__(self, communicator: GoProHttp):
        """Constructor

        Args:
            communicator (GoProHttp):  Adapter to read / write commands
        """
        ######################################################################################################
        #                          HTTP GET JSON COMMANDS
        ######################################################################################################

        class SetZoom(HttpGetJsonCommand):
            def __call__(self, percent: int) -> GoProResp:
                """Set digital zoom in percent.

                Args:
                    percent (int): Desired zoom as a percentage

                Returns:
                    GoProResp: command status
                """
                return super().__call__(percent=percent)

        #: Sphinx docstring redirect
        self.set_digital_zoom = SetZoom(
            communicator,
            endpoint="gopro/camera/digital_zoom",
            arguments=["percent"],
        )

        class GetCameraState(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Get all camera statuses and settings

                Returns:
                    GoProResp: status and settings as JSON
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_camera_state = GetCameraState(
            communicator,
            endpoint="gopro/camera/state",
            parser=HttpParsers.CameraStateParser(),
        )

        class KeepAlive(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Send the keep alive signal to maintain the connection.

                Returns:
                    GoProResp: command status
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.set_keep_alive = KeepAlive(
            communicator,
            endpoint="gopro/camera/keep_alive",
        )

        class GetMediaInfo(HttpGetJsonCommand):
            def __call__(self, file: str) -> GoProResp:
                """Get media info for a file.

                Args:
                    file (str): Media file to get info for

                Returns:
                    GoProResp: Media info as JSON
                """
                return super().__call__(path=f"100GOPRO/{file}")

        #: Sphinx docstring redirect
        self.get_media_info = GetMediaInfo(
            communicator,
            endpoint="gopro/media/info",
            arguments=["path"],
        )

        class GetMediaList(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Get a list of media on the camera.

                Returns:
                    GoProResp: Media list JSON structure
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_media_list = GetMediaList(
            communicator,
            endpoint="gopro/media/list",
            parser=HttpParsers.MediaListParser(),
        )

        class SetTurboMode(HttpGetJsonCommand):
            def __call__(self, mode: Params.Toggle) -> GoProResp:
                """Enable or disable Turbo transfer mode.

                Args:
                    mode (open_gopro.api.params.Toggle): enable / disable turbo mode

                Returns:
                    GoProResp: _description_
                """
                return super().__call__(p=mode)

        #: Sphinx docstring redirect
        self.set_turbo_mode = SetTurboMode(
            communicator,
            endpoint="gopro/media/turbo_transfer",
            arguments=["p"],
        )

        class GetOgpVersion(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Get Open GoPro API version

                Returns:
                    GoProResp: Open GoPro Version
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_open_gopro_api_version = GetOgpVersion(
            communicator,
            endpoint="gopro/version",
        )

        class GetPresetStatus(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Get status of current presets

                Returns:
                    GoProResp: JSON describing currently available presets and preset groups
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_preset_status = GetPresetStatus(
            communicator,
            endpoint="gopro/camera/presets/get",
        )

        class SetPreset(HttpGetJsonCommand):
            def __call__(self, preset: int) -> GoProResp:
                """Set camera to a given preset

                The preset ID can be found from :py:class:`open_gopro.api.http_commands.HttpCommands.get_preset_status`

                Args:
                    preset (int): preset to load

                Returns:
                    GoProResp: command status
                """
                return super().__call__(id=preset)

        #: Sphinx docstring redirect
        self.set_preset = SetPreset(
            communicator,
            endpoint="gopro/camera/presets/load",
            arguments=["id"],
        )

        class SetPresetGroup(HttpGetJsonCommand):
            def __call__(self, group: Params.PresetGroup) -> GoProResp:
                """Set the active preset group.

                The most recently used Preset in this group will be set.

                Args:
                    group (open_gopro.api.params.PresetGroup): desired Preset Group

                Returns:
                    GoProResp: command status
                """
                return super().__call__(id=group)

        #: Sphinx docstring redirect
        self.set_preset_group = SetPresetGroup(
            communicator,
            endpoint="gopro/camera/presets/set_group",
            arguments=["id"],
        )

        class SetPreviewStream(HttpGetJsonCommand):
            def __call__(self, mode: Params.Toggle) -> GoProResp:
                """Start or stop the preview stream

                Args:
                    mode (open_gopro.api.params.Toggle): enable to start or disable to stop

                Returns:
                    GoProResp: command status
                """
                return super().__call__(mode="start" if mode is Params.Toggle.ENABLE else "stop")

        #: Sphinx docstring redirect
        self.set_preview_stream = SetPreviewStream(
            communicator,
            endpoint="gopro/camera/stream",
            components=["mode"],
            identifier="Preview Stream",
        )

        class SetThirdPartyInfo(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Flag as third party app

                Returns:
                    GoProResp: command status
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.set_third_party_client_info = SetThirdPartyInfo(
            communicator,
            endpoint="gopro/camera/analytics/set_client_info",
        )

        class SetShutter(HttpGetJsonCommand):
            def __call__(self, shutter: Params.Toggle) -> GoProResp:
                """Set the shutter on or off

                Args:
                    shutter (open_gopro.api.params.Toggle): on or off (i.e. start or stop encoding)

                Returns:
                    GoProResp: command status
                """
                return super().__call__(mode="start" if shutter is Params.Toggle.ENABLE else "stop")

        #: Sphinx docstring redirect
        self.set_shutter_on = SetShutter(
            communicator,
            endpoint="gopro/camera/shutter",
            components=["mode"],
        )

        class SetCameraControl(HttpGetJsonCommand):
            def __call__(self, mode: Params.CameraControl) -> GoProResp:
                """Configure global behaviors by setting camera control (to i.e. Idle, External)

                Args:
                    mode (open_gopro.api.params.CameraControl): desired camera control value

                Returns:
                    GoProResp: command status
                """
                return super().__call__(p=mode)

        #: Sphinx docstring redirect
        self.set_camera_control = SetCameraControl(
            communicator,
            endpoint="gopro/camera/control/set_ui_controller",
            arguments=["p"],
        )

        class SetDateTime(HttpGetJsonCommand):
            def __call__(
                self,
                date_time: datetime.datetime,
                tz_offset: int = 0,
                is_dst: bool = False,
            ) -> GoProResp:
                """Update the date and time of the camera

                Args:
                    date_time (datetime.datetime): date and time
                    tz_offset (int): timezone (as UTC offset). Defaults to 0.
                    is_dst (bool): is daylight savings time?. Defaults to False.

                Returns:
                    GoProResp: command status
                """
                return super().__call__(
                    date=f"{date_time.year}_{date_time.month}_{date_time.day}",
                    time=f"{date_time.hour}_{date_time.minute}_{date_time.second}",
                    tzone=tz_offset,
                    dst=int(is_dst),
                )

        #: Sphinx docstring redirect
        self.set_date_time = SetDateTime(
            communicator,
            endpoint="gopro/camera/set_date_time",
            arguments=["date", "time", "tzone", "dst"],
        )

        class GetDateTime(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Get the date and time of the camera (Non timezone / DST aware)

                Returns:
                    GoProResp: current date and time on camera
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_date_time = GetDateTime(
            communicator,
            endpoint="gopro/camera/get_date_time",
        )

        class GetWebcamStatus(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Get the status of the webcam endpoint

                Returns:
                    GoProResp: webcam status
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_webcam_status = GetWebcamStatus(
            communicator,
            endpoint="gopro/webcam/status",
        )

        class GetWebcamVersion(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Get the version of the webcam implementation

                Returns:
                    GoProResp: version
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.get_webcam_version = GetWebcamVersion(
            communicator,
            endpoint="gopro/webcam/version",
        )

        class AddHilight(HttpGetJsonCommand):
            def __call__(self, file: str, offset: Optional[int] = None) -> GoProResp:
                """Add a hilight to a media file (.mp4)

                Args:
                    file (str):  the media to add the hilight to
                    offset (Optional[int]): offset in ms from start of media

                Returns:
                    GoProResp: command status
                """
                return super().__call__(path=f"100GOPRO/{file}", ms=offset or None)

        #: Sphinx docstring redirect
        self.add_file_hilight = AddHilight(
            communicator,
            endpoint="gopro/media/hilight/file",
            arguments=["path", "ms"],
        )

        class RemoveHilight(HttpGetJsonCommand):
            def __call__(self, file: str, offset: Optional[int] = None) -> GoProResp:
                """Remove a hilight from a media file (.mp4)

                Args:
                    file (str):  the media to remove the hilight from
                    offset (Optional[int]): offset in ms from start of media

                Returns:
                    GoProResp: command status
                """
                return super().__call__(path=f"100GOPRO/{file}", ms=offset)

        #: Sphinx docstring redirect
        self.remove_file_hilight = RemoveHilight(
            communicator,
            endpoint="gopro/media/hilight/remove",
            arguments=["path", "ms"],
        )

        ######################################################################################################
        #                          HTTP GET BINARY COMMANDS
        ######################################################################################################

        class GetGpmfData(HttpGetBinary):
            def __call__(self, camera_file: str, local_file: Optional[Path] = None) -> Path:
                """Get GPMF data for a file.

                If local_file is none, the output location will be the same name as the camera_file.

                Args:
                    camera_file (str): filename on camera to operate on
                    local_file (Optional[Path]): Location on computer to write output. Defaults to None.

                Returns:
                    Path: Path to local_file that output was written to
                """
                return super().__call__(camera_file, local_file)

        #: Sphinx docstring redirect
        self.get_gpmf_data = GetGpmfData(communicator, endpoint="gopro/media/gpmf?path=100GOPRO")

        class GetScreennail(HttpGetBinary):
            def __call__(self, camera_file: str, local_file: Optional[Path] = None) -> Path:
                """Get screennail for a file.

                If local_file is none, the output location will be the same name as the camera_file.

                Args:
                    camera_file (str): filename on camera to operate on
                    local_file (Optional[Path]): Location on computer to write output. Defaults to None.

                Returns:
                    Path: Path to local_file that output was written to
                """
                return super().__call__(camera_file, local_file)

        #: Sphinx docstring redirect
        self.get_screennail = GetScreennail(communicator, endpoint="gopro/media/screennail?path=100GOPRO")

        class GetThumbnail(HttpGetBinary):
            def __call__(self, camera_file: str, local_file: Optional[Path] = None) -> Path:
                """Get thumbnail for a file.

                If local_file is none, the output location will be the same name as the camera_file.

                Args:
                    camera_file (str): filename on camera to operate on
                    local_file (Optional[Path]): Location on computer to write output. Defaults to None.

                Returns:
                    Path: Path to local_file that output was written to
                """
                return super().__call__(camera_file, local_file)

        #: Sphinx docstring redirect
        self.get_thumbnail = GetThumbnail(communicator, endpoint="gopro/media/thumbnail?path=100GOPRO")

        class GetTelemetry(HttpGetBinary):
            def __call__(self, camera_file: str, local_file: Optional[Path] = None) -> Path:
                """Download the telemetry data for a camera file and store in a local file.

                If local_file is none, the output location will be the same name as the camera_file.

                Args:
                    camera_file (str): filename on camera to operate on
                    local_file (Optional[Path]): Location on computer to write output. Defaults to None.

                Returns:
                    Path: Path to local_file that output was written to
                """
                return super().__call__(camera_file, local_file)

        #: Sphinx docstring redirect
        self.get_telemetry = GetTelemetry(communicator, endpoint="gopro/media/telemetry?path=100GOPRO")

        class DownloadFile(HttpGetBinary):
            def __call__(self, camera_file: str, local_file: Optional[Path] = None) -> Path:
                """Download a video from the camera to a local file.

                If local_file is none, the output location will be the same name as the camera_file.

                Args:
                    camera_file (str): filename on camera to operate on
                    local_file (Optional[Path]): Location on computer to write output. Defaults to None.

                Returns:
                    Path: Path to local_file that output was written to
                """
                return super().__call__(camera_file, local_file)

        #: Sphinx docstring redirect
        self.download_file = DownloadFile(
            communicator, endpoint="videos/DCIM/100GOPRO", identifier="Download File"
        )

        super().__init__(communicator)


class UsbOnlyCommands(Commands[HttpCommand, CmdId]):
    """The HTTP commands which can only be sent via USB"""

    # pylint: disable = missing-class-docstring, arguments-differ, useless-super-delegation
    def __init__(self, communicator: GoProHttp):
        """Constructor

        Args:
            communicator (GoProHttp):  Adapter to read / write commands
        """
        ######################################################################################################
        #                          HTTP GET JSON COMMANDS
        ######################################################################################################

        class WebcamExit(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Exit the webcam.

                Returns:
                    GoProResp: command status
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.webcam_exit = WebcamExit(communicator, endpoint="gopro/webcam/exit")

        class WebcamPreview(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Start the webcam preview.

                Returns:
                    GoProResp: command status
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.webcam_preview = WebcamPreview(communicator, endpoint="gopro/webcam/preview")

        class WebcamStart(HttpGetJsonCommand):
            def __call__(
                self, resolution: Optional[Params.Resolution] = None, fov: Optional[Params.PhotoFOV] = None
            ) -> GoProResp:
                """Start the webcam.

                Args:
                    resolution (Params.Resolution, optional): resolution to use. If not set, camera default will be used.
                    fov (Params.PhotoFOV, optional): field of view to use. If not set, camera default will be used.

                Returns:
                    GoProResp: command status
                """
                return super().__call__(res=resolution, fov=fov)

        #: Sphinx docstring redirect
        self.webcam_start = WebcamStart(communicator, endpoint="gopro/webcam/start", arguments=["res", "fov"])

        class WebcamStop(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Stop the webcam.

                Returns:
                    GoProResp: command status
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.webcam_stop = WebcamStop(communicator, endpoint="gopro/webcam/stop")

        class WebcamStatus(HttpGetJsonCommand):
            def __call__(self) -> GoProResp:
                """Get the current status of the webcam

                Returns:
                    GoProResp: command status including the webcam status
                """
                return super().__call__()

        #: Sphinx docstring redirect
        self.webcam_status = WebcamStatus(communicator, endpoint="gopro/webcam/status")

        class UsbControl(HttpGetJsonCommand):
            def __call__(self, control: Params.Toggle) -> GoProResp:
                """Enable / disable wired usb control

                Args:
                    control (params.Toggle): enable or disable

                Returns:
                    GoProResp: command status
                """
                return super().__call__(p=control)

        #: Sphinx docstring redirect
        self.wired_usb_control = UsbControl(
            communicator, endpoint="gopro/camera/control/wired_usb", arguments=["p"]
        )

        super().__init__(communicator)


class HttpSettings(Commands[HttpSetting, SettingId]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all HTTP Settings

    Args:
        communicator (GoProHttp): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProHttp):
        self.resolution = HttpSetting[Params.Resolution](communicator, SettingId.RESOLUTION)
        """Resolution. Set with :py:class:`open_gopro.api.params.Resolution`"""

        self.fps = HttpSetting[Params.FPS](communicator, SettingId.FPS)
        """Frames per second. Set with :py:class:`open_gopro.api.params.FPS`"""

        self.auto_off = HttpSetting[Params.AutoOff](communicator, SettingId.AUTO_OFF)
        """Set the auto off time. Set with :py:class:`open_gopro.api.params.AutoOff`"""

        self.video_field_of_view = HttpSetting[Params.VideoFOV](communicator, SettingId.VIDEO_FOV)
        """Video FOV. Set with :py:class:`open_gopro.api.params.VideoFOV`"""

        self.photo_field_of_view = HttpSetting[Params.PhotoFOV](communicator, SettingId.PHOTO_FOV)
        """Photo FOV. Set with :py:class:`open_gopro.api.params.PhotoFOV`"""

        self.multi_shot_field_of_view = HttpSetting[Params.MultishotFOV](
            communicator, SettingId.MULTI_SHOT_FOV
        )
        """Multi-shot FOV. Set with :py:class:`open_gopro.api.params.MultishotFOV`"""

        self.max_lens_mode = HttpSetting[Params.MaxLensMode](communicator, SettingId.MAX_LENS_MOD)
        """Enable / disable max lens mod. Set with :py:class:`open_gopro.api.params.MaxLensMode`"""

        self.hypersmooth = HttpSetting[Params.HypersmoothMode](communicator, SettingId.HYPERSMOOTH)
        """Set / disable hypersmooth. Set with :py:class:`open_gopro.api.params.HypersmoothMode`"""

        self.video_performance_mode = HttpSetting[Params.PerformanceMode](
            communicator, SettingId.VIDEO_PERFORMANCE_MODE
        )
        """Video Performance Mode (extended battery, tripod, etc). Set with :py:class:`open_gopro.api.params.PerformanceMode`"""

        self.media_format = HttpSetting[Params.MediaFormat](communicator, SettingId.MEDIA_FORMAT)
        """Set the media format. Set with :py:class:`open_gopro.api.params.MediaFormat`"""

        self.anti_flicker = HttpSetting[Params.AntiFlicker](communicator, SettingId.ANTI_FLICKER)
        """Anti Flicker frequency. Set with :py:class:`open_gopro.api.params.AntiFlicker`"""

        self.camera_ux_mode = HttpSetting[Params.CameraUxMode](communicator, SettingId.CAMERA_UX_MODE)
        """Camera controls configuration. Set with :py:class:`open_gopro.api.params.CameraUxMode`"""

        self.video_easy_mode = HttpSetting[Params.Speed](communicator, SettingId.VIDEO_EASY_MODE)
        """Video easy mode speed. Set with :py:class:`open_gopro.api.params.Speed`"""

        self.photo_easy_mode = HttpSetting[Params.PhotoEasyMode](communicator, SettingId.PHOTO_EASY_MODE)
        """Night Photo easy mode. Set with :py:class:`open_gopro.api.params.PhotoEasyMode`"""

        self.wifi_band = HttpSetting[Params.WifiBand](communicator, SettingId.WIFI_BAND)
        """Current WiFi band being used. Set with :py:class:`open_gopro.api.params.WifiBand`"""

        self.star_trail_length = HttpSetting[Params.StarTrailLength](communicator, SettingId.STAR_TRAIL_LENGTH)
        """Multi shot star trail length. Set with :py:class:`open_gopro.api.params.StarTrailLength`"""

        self.system_video_mode = HttpSetting[Params.SystemVideoMode](communicator, SettingId.SYSTEM_VIDEO_MODE)
        """System video mode. Set with :py:class:`open_gopro.api.params.SystemVideoMode`"""

        self.video_horizon_leveling = HttpSetting[Params.HorizonLeveling](
            communicator, SettingId.VIDEO_HORIZON_LEVELING
        )
        """Lock / unlock horizon leveling for video. Set with :py:class:`open_gopro.api.params.HorizonLeveling`"""

        self.photo_horizon_leveling = HttpSetting[Params.HorizonLeveling](
            communicator, SettingId.PHOTO_HORIZON_LEVELING
        )
        """Lock / unlock horizon leveling for photo. Set with :py:class:`open_gopro.api.params.HorizonLeveling`"""

        super().__init__(communicator)


# pylint: disable = missing-class-docstring
class HttpParsers:
    """The collection of parsers used for additional JSON parsing"""

    class CameraStateParser(JsonParser):
        """Parse integer numbers into Enums"""

        def parse(self, data: dict) -> dict:  # noqa: D102
            parsed: dict[Any, Any] = {}
            # Parse status and settings values into nice human readable things
            for (name, id_map) in [("status", StatusId), ("settings", SettingId)]:
                for k, v in data[name].items():
                    identifier = id_map(int(k))
                    parsed[identifier] = (
                        container(v) if (container := GoProResp._get_query_container(identifier)) else v  # type: ignore
                    )
            return parsed

    class MediaListParser(JsonParser):
        """Extract the list of files from the media list JSON"""

        def parse(self, data: dict) -> dict:  # noqa: D102
            return {"files": data["media"][0]["fs"]}
