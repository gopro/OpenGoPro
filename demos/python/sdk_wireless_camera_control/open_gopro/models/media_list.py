# media_list.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jun 26 18:26:05 UTC 2023

"""Media List and Metadata containers and helper methods"""

from __future__ import annotations

from abc import ABC
from typing import Any, Optional

from pydantic import Field, PrivateAttr, validator

from open_gopro import types
from open_gopro.models.bases import CustomBaseModel

##############################################################################################################
# Generic
##############################################################################################################


class MediaPath(ABC, CustomBaseModel):
    """Model to represent media path"""

    folder: str  #: directory that media lives in
    file: str  #: media file name (including file extension)


##############################################################################################################
# Metadata
##############################################################################################################


class MediaMetadata(ABC, CustomBaseModel):
    """Base Media Metadata class"""

    content_type: str = Field(alias="ct")  #: Media content type
    creation_timestamp: str = Field(alias="cre")  #: Creation time in seconds since epoch
    file_size: str = Field(alias="s")  #: File size in bytes
    gumi: str = Field(alias="gumi")  #: Globally Unique Media ID
    height: str = Field(alias="h")  #: Height of media in pixels
    width: str = Field(alias="w")  #: Width of media in pixels
    hilight_count: str = Field(alias="hc")  #: Number of hilights in media
    image_stabilization: str = Field(alias="eis")  #: 1 if stabilized, 0 otherwise
    metadata_present: str = Field(alias="mp")  #: 1 if metadata is present, 0 otherwise
    rotate: str = Field(alias="rot")  #: Media rotation
    transcoded: str = Field(alias="tr")  #: 1 if file is transcoded, 0 otherwise
    upload_status: str = Field(alias="us")  #: Whether or not the media file has been uploaded
    media_offload_state: Optional[list[str]] = Field(alias="mos", default=None)  #: List of offload states
    parent_gumi: Optional[str] = Field(alias="pgumi", default=None)  #: Only present if in a clip
    field_of_view: Optional[str] = Field(alias="fov", default=None)  #: Field of View
    lens_config: Optional[str] = Field(alias="lc", default=None)  #: Lens configuration
    lens_projection: Optional[str] = Field(alias="prjn", default=None)  #: Lens projection

    @classmethod
    def from_json(cls, json_str: types.JsonDict) -> MediaMetadata:
        """Build a metadata object given JSON input

        Args:
            json_str (types.JsonDict): raw JSON

        Returns:
            MediaMetadata: parsed metadata
        """
        # Choose a field that only exists in video to see if this is a video
        return (VideoMetadata if "ao" in json_str else PhotoMetadata)(**json_str)


class VideoMetadata(MediaMetadata):
    """Metadata for a video file"""

    audio_option: str = Field(alias="ao")  #: Auto, wind, or stereo
    avc_level: str = Field(alias="profile")  #: Advanced Video Codec Level
    avc_profile: str = Field(alias="avc_profile")  #: Advanced Video Code Profile
    clipped: str = Field(alias="cl")  #: 1 if clipped, 0 otherwise
    duration: str = Field(alias="dur")  #: Video duration in seconds
    frame_rate: str = Field(alias="fps")  # Video frame rate in frames / second
    frame_rate_divisor: str = Field(alias="fps_denom")  #: Used to modify frame rate
    hilight_list: list[str] = Field(alias="hi")  #: List of hlights in ms offset from start of video
    lrv_file_size: str = Field(alias="ls")  #: Low Resolution Video file size in bytes. -1 if there is no LRV
    max_auto_hilight_score: str = Field(alias="mahs")  #: Maximum auto-hilight score
    protune_audio: str = Field(alias="pta")  #: 1 if protune audio is present, 0 otherwise
    subsample: str = Field(alias="subsample")  #: 1 if subsampled from other video, 0 otherwise
    progressive: Optional[str] = Field(alias="progr", default=None)  #: 1 if progressive, 0 otherwise


class PhotoMetadata(MediaMetadata):
    """Metadata for a Photo file"""

    raw: Optional[str] = Field(default=None)  #: 1 if photo has raw version, 0 otherwise
    """1 if photo taken with wide dynamic range, 0 otherwise"""
    wide_dynamic_range: Optional[str] = Field(alias="wdr", default=None)
    """1 if photo taken with high dynamic range, 0 otherwise"""
    high_dynamic_range: Optional[str] = Field(alias="hdr", default=None)


##############################################################################################################
# Media List
##############################################################################################################


class MediaItem(CustomBaseModel):
    """Base Media Item class"""

    filename: str = Field(alias="n")  #: Name of media item
    creation_timestamp: str = Field(alias="cre")  #: Creation time in seconds since epoch
    modified_time: str = Field(alias="mod")  #: Time file was last modified in seconds since epoch
    low_res_video_size: Optional[str] = Field(alias="glrv", default=None)  #: Low resolution video size
    lrv_file_size: Optional[str] = Field(alias="ls", default=None)  #: Low resolution file size
    session_id: Optional[str] = Field(alias="id", default=None)  # Media list session identifier


class GroupedMediaItem(MediaItem):
    """Media Item that is also a grouped item.

    An example of a grouped item is a burst photo.
    """

    group_id: str = Field(alias="g", default=None)  #: Group Identifier
    group_size: str = Field(alias="s", default=None)  # Number of files in the group
    group_first_member_id: str = Field(alias="b", default=None)  # ID of first member in the group
    group_last_member_id: str = Field(alias="l", default=None)  #: ID of last member in the group
    group_missing_ids: list[str] = Field(alias="m", default=None)  #: File ID's that are missing or deleted
    """(b -> burst, c -> continuous shot, n -> night lapse, t -> time lapse)"""
    group_type: str = Field(alias="t", default=None)


class MediaFileSystem(CustomBaseModel):
    """Grouping of media items into filesystem(s)"""

    directory: str = Field(alias="d")  # Directory that the files are in
    file_system: list[MediaItem] = Field(alias="fs")  #: List of files

    @validator("file_system", pre=True, each_item=True)
    @classmethod
    def identify_item(cls, item: types.JsonDict) -> MediaItem:
        """Extent item into GroupedMediaItem if it such an item

        A group item is identified by the presence of a "g" field

        Args:
            item (types.JsonDict): input JSON

        Returns:
            MediaItem: parsed media item
        """
        return (GroupedMediaItem if "g" in item else MediaItem)(**item)


class MediaList(CustomBaseModel):
    """Top level media list object"""

    identifier: str = Field(alias="id")  #: String identifier of this media list
    media: list[MediaFileSystem]  #: Media filesystem(s)
    _files: list[MediaItem] = PrivateAttr(default_factory=list)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # self.thing = 1
        # Modify each file name to use full path
        for directory in self.media:
            for media in directory.file_system:
                media.filename = f"{directory.directory}/{media.filename}"
                self._files.append(media)

    @property
    def files(self) -> list[MediaItem]:
        """Helper method to get list of media items

        Returns:
            list[MediaItem]: all media items in this media list
        """
        return self._files
