# http_commands.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http:/gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Sep  7 21:35:52 UTC 2021

"""HTTP Commands"""

# mypy: disable-error-code=empty-body

from __future__ import annotations

import datetime
import logging
from pathlib import Path

from open_gopro.api.builders import (
    http_get_binary_command,
    http_get_json_command,
    http_put_json_command,
)
from open_gopro.domain.communicator_interface import (
    HttpMessage,
    HttpMessages,
    MessageRules,
)
from open_gopro.domain.parser_interface import Parser
from open_gopro.models import (
    CameraInfo,
    GoProResp,
    MediaList,
    MediaMetadata,
    MediaPath,
    constants,
    proto,
    streaming,
)
from open_gopro.models.streaming import WebcamResponse
from open_gopro.models.types import CameraState, JsonDict
from open_gopro.parsers.json import (
    CameraStateJsonParser,
    LambdaJsonParser,
    PydanticAdapterJsonParser,
)

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
        parser=Parser(json_parser=PydanticAdapterJsonParser(MediaPath)),
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
        parser=Parser(json_parser=CameraStateJsonParser()),
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
    )
    async def get_camera_state(self) -> GoProResp[CameraState]:
        """Get all camera statuses and settings

        Returns:
            GoProResp[CameraState]: status and settings as JSON
        """

    @http_get_json_command(
        endpoint="gopro/camera/info", parser=Parser(json_parser=PydanticAdapterJsonParser(CameraInfo))
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
        parser=Parser(json_parser=PydanticAdapterJsonParser(MediaMetadata)),
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
        parser=Parser(json_parser=PydanticAdapterJsonParser(MediaList)),
    )
    async def get_media_list(self) -> GoProResp[MediaList]:
        """Get a list of media on the camera.

        Returns:
            GoProResp[MediaList]: Media list JSON structure
        """

    @http_get_json_command(endpoint="gopro/media/turbo_transfer", arguments=["p"])
    async def set_turbo_mode(self, *, mode: constants.Toggle) -> GoProResp[None]:
        """Enable or disable Turbo transfer mode.

        Args:
            mode (constants.Toggle): enable / disable turbo mode

        Returns:
            GoProResp[None]: Status
        """
        return {"p": mode}  # type: ignore

    @http_get_json_command(
        endpoint="gopro/version",
        parser=Parser(json_parser=LambdaJsonParser(lambda data: f"{data['version']}")),
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
    async def set_preview_stream(self, *, mode: constants.Toggle, port: int | None = None) -> GoProResp[None]:
        """Start or stop the preview stream

        Args:
            mode (constants.Toggle): enable to start or disable to stop
            port (int | None): Port to use for Preview Stream. Defaults to 8554 if None.
                Only relevant when starting the stream.

        Returns:
            GoProResp[None]: command status
        """
        return {"mode": "start" if mode is constants.Toggle.ENABLE else "stop", "port": port}  # type: ignore

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
    async def set_shutter(self, *, shutter: constants.Toggle) -> GoProResp[None]:
        """Set the shutter on or off

        Args:
            shutter (constants.Toggle): on or off (i.e. start or stop encoding)

        Returns:
            GoProResp[None]: command status
        """
        return {"mode": "start" if shutter is constants.Toggle.ENABLE else "stop"}  # type: ignore

    @http_get_json_command(
        endpoint="gp/gpControl/command/system/reset",
        rules=MessageRules(
            fastpass_analyzer=lambda **_: True,
        ),
    )
    async def reboot(self) -> GoProResp[None]:
        """Reboot the camera (approximating a battery pull)

        Returns:
            GoProResp[None]: command status
        """

    @http_get_json_command(endpoint="gopro/camera/control/set_ui_controller", arguments=["p"])
    async def set_camera_control(self, *, mode: constants.CameraControl) -> GoProResp[None]:
        """Configure global behaviors by setting camera control (to i.e. Idle, External)

        Args:
            mode (constants.CameraControl): desired camera control value

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
        parser=Parser(json_parser=PydanticAdapterJsonParser(WebcamResponse)),
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
    )
    async def webcam_exit(self) -> GoProResp[WebcamResponse]:
        """Exit the webcam.

        Returns:
            GoProResp[WebcamResponse]: command status
        """

    @http_get_json_command(
        endpoint="gopro/webcam/preview",
        parser=Parser(json_parser=PydanticAdapterJsonParser(WebcamResponse)),
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
        parser=Parser(json_parser=PydanticAdapterJsonParser(WebcamResponse)),
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
    )
    async def webcam_start(
        self,
        *,
        resolution: streaming.WebcamResolution | None = None,
        fov: streaming.WebcamFOV | None = None,
        port: int | None = None,
        protocol: streaming.WebcamProtocol | None = None,
    ) -> GoProResp[WebcamResponse]:
        """Start the webcam.

        Args:
            resolution (streaming.WebcamResolution | None): resolution to use. If not set, camera default will be used.
            fov (streaming.WebcamFOV | None): field of view to use. If not set, camera default will be used.
            port (int | None): port to use for streaming. If not set, camera default of 8554 will be used.
            protocol (streaming.WebcamProtocol | None): streaming protocol to use. If not set, camera default of TS will
                be used.

        Returns:
            GoProResp[WebcamResponse]: command status
        """
        return {"res": resolution, "fov": fov, "port": port, "protocol": protocol}  # type: ignore

    @http_get_json_command(
        endpoint="gopro/webcam/stop",
        rules=MessageRules(fastpass_analyzer=MessageRules.always_true),
        parser=Parser(json_parser=PydanticAdapterJsonParser(WebcamResponse)),
    )
    async def webcam_stop(self) -> GoProResp[WebcamResponse]:
        """Stop the webcam.

        Returns:
            GoProResp[WebcamResponse]: command status
        """

    @http_get_json_command(
        endpoint="gopro/webcam/status",
        parser=Parser(json_parser=PydanticAdapterJsonParser(WebcamResponse)),
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
    async def wired_usb_control(self, *, control: constants.Toggle) -> GoProResp[None]:
        """Enable / disable wired usb control

        Args:
            control (constants.Toggle): enable or disable

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
    async def get_screennail(self, *, camera_file: str, local_file: Path | None = None) -> GoProResp[Path]:
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
