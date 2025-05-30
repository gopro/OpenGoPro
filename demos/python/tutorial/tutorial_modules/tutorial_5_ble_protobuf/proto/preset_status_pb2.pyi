"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*
Defines the structure of protobuf message received from camera containing preset status
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _EnumFlatMode:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _EnumFlatModeEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_EnumFlatMode.ValueType], builtins.type
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    FLAT_MODE_UNKNOWN: _EnumFlatMode.ValueType
    FLAT_MODE_PLAYBACK: _EnumFlatMode.ValueType
    FLAT_MODE_SETUP: _EnumFlatMode.ValueType
    FLAT_MODE_VIDEO: _EnumFlatMode.ValueType
    FLAT_MODE_TIME_LAPSE_VIDEO: _EnumFlatMode.ValueType
    FLAT_MODE_LOOPING: _EnumFlatMode.ValueType
    FLAT_MODE_PHOTO_SINGLE: _EnumFlatMode.ValueType
    FLAT_MODE_PHOTO: _EnumFlatMode.ValueType
    FLAT_MODE_PHOTO_NIGHT: _EnumFlatMode.ValueType
    FLAT_MODE_PHOTO_BURST: _EnumFlatMode.ValueType
    FLAT_MODE_TIME_LAPSE_PHOTO: _EnumFlatMode.ValueType
    FLAT_MODE_NIGHT_LAPSE_PHOTO: _EnumFlatMode.ValueType
    FLAT_MODE_BROADCAST_RECORD: _EnumFlatMode.ValueType
    FLAT_MODE_BROADCAST_BROADCAST: _EnumFlatMode.ValueType
    FLAT_MODE_TIME_WARP_VIDEO: _EnumFlatMode.ValueType
    FLAT_MODE_LIVE_BURST: _EnumFlatMode.ValueType
    FLAT_MODE_NIGHT_LAPSE_VIDEO: _EnumFlatMode.ValueType
    FLAT_MODE_SLOMO: _EnumFlatMode.ValueType
    FLAT_MODE_IDLE: _EnumFlatMode.ValueType
    FLAT_MODE_VIDEO_STAR_TRAIL: _EnumFlatMode.ValueType
    FLAT_MODE_VIDEO_LIGHT_PAINTING: _EnumFlatMode.ValueType
    FLAT_MODE_VIDEO_LIGHT_TRAIL: _EnumFlatMode.ValueType
    FLAT_MODE_VIDEO_BURST_SLOMO: _EnumFlatMode.ValueType

class EnumFlatMode(_EnumFlatMode, metaclass=_EnumFlatModeEnumTypeWrapper): ...

FLAT_MODE_UNKNOWN: EnumFlatMode.ValueType
FLAT_MODE_PLAYBACK: EnumFlatMode.ValueType
FLAT_MODE_SETUP: EnumFlatMode.ValueType
FLAT_MODE_VIDEO: EnumFlatMode.ValueType
FLAT_MODE_TIME_LAPSE_VIDEO: EnumFlatMode.ValueType
FLAT_MODE_LOOPING: EnumFlatMode.ValueType
FLAT_MODE_PHOTO_SINGLE: EnumFlatMode.ValueType
FLAT_MODE_PHOTO: EnumFlatMode.ValueType
FLAT_MODE_PHOTO_NIGHT: EnumFlatMode.ValueType
FLAT_MODE_PHOTO_BURST: EnumFlatMode.ValueType
FLAT_MODE_TIME_LAPSE_PHOTO: EnumFlatMode.ValueType
FLAT_MODE_NIGHT_LAPSE_PHOTO: EnumFlatMode.ValueType
FLAT_MODE_BROADCAST_RECORD: EnumFlatMode.ValueType
FLAT_MODE_BROADCAST_BROADCAST: EnumFlatMode.ValueType
FLAT_MODE_TIME_WARP_VIDEO: EnumFlatMode.ValueType
FLAT_MODE_LIVE_BURST: EnumFlatMode.ValueType
FLAT_MODE_NIGHT_LAPSE_VIDEO: EnumFlatMode.ValueType
FLAT_MODE_SLOMO: EnumFlatMode.ValueType
FLAT_MODE_IDLE: EnumFlatMode.ValueType
FLAT_MODE_VIDEO_STAR_TRAIL: EnumFlatMode.ValueType
FLAT_MODE_VIDEO_LIGHT_PAINTING: EnumFlatMode.ValueType
FLAT_MODE_VIDEO_LIGHT_TRAIL: EnumFlatMode.ValueType
FLAT_MODE_VIDEO_BURST_SLOMO: EnumFlatMode.ValueType
global___EnumFlatMode = EnumFlatMode

class _EnumPresetGroup:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _EnumPresetGroupEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_EnumPresetGroup.ValueType], builtins.type
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PRESET_GROUP_ID_VIDEO: _EnumPresetGroup.ValueType
    PRESET_GROUP_ID_PHOTO: _EnumPresetGroup.ValueType
    PRESET_GROUP_ID_TIMELAPSE: _EnumPresetGroup.ValueType

class EnumPresetGroup(_EnumPresetGroup, metaclass=_EnumPresetGroupEnumTypeWrapper): ...

PRESET_GROUP_ID_VIDEO: EnumPresetGroup.ValueType
PRESET_GROUP_ID_PHOTO: EnumPresetGroup.ValueType
PRESET_GROUP_ID_TIMELAPSE: EnumPresetGroup.ValueType
global___EnumPresetGroup = EnumPresetGroup

class _EnumPresetGroupIcon:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _EnumPresetGroupIconEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_EnumPresetGroupIcon.ValueType], builtins.type
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PRESET_GROUP_VIDEO_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_PHOTO_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_TIMELAPSE_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_MAX_VIDEO_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_MAX_PHOTO_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_MAX_TIMELAPSE_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_ND_MOD_VIDEO_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_ND_MOD_PHOTO_ICON_ID: _EnumPresetGroupIcon.ValueType
    PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID: _EnumPresetGroupIcon.ValueType

class EnumPresetGroupIcon(_EnumPresetGroupIcon, metaclass=_EnumPresetGroupIconEnumTypeWrapper): ...

PRESET_GROUP_VIDEO_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_PHOTO_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_TIMELAPSE_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_MAX_VIDEO_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_MAX_PHOTO_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_MAX_TIMELAPSE_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_ND_MOD_VIDEO_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_ND_MOD_PHOTO_ICON_ID: EnumPresetGroupIcon.ValueType
PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID: EnumPresetGroupIcon.ValueType
global___EnumPresetGroupIcon = EnumPresetGroupIcon

class _EnumPresetIcon:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _EnumPresetIconEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_EnumPresetIcon.ValueType], builtins.type
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PRESET_ICON_VIDEO: _EnumPresetIcon.ValueType
    PRESET_ICON_ACTIVITY: _EnumPresetIcon.ValueType
    PRESET_ICON_CINEMATIC: _EnumPresetIcon.ValueType
    PRESET_ICON_PHOTO: _EnumPresetIcon.ValueType
    PRESET_ICON_LIVE_BURST: _EnumPresetIcon.ValueType
    PRESET_ICON_BURST: _EnumPresetIcon.ValueType
    PRESET_ICON_PHOTO_NIGHT: _EnumPresetIcon.ValueType
    PRESET_ICON_TIMEWARP: _EnumPresetIcon.ValueType
    PRESET_ICON_TIMELAPSE: _EnumPresetIcon.ValueType
    PRESET_ICON_NIGHTLAPSE: _EnumPresetIcon.ValueType
    PRESET_ICON_SNAIL: _EnumPresetIcon.ValueType
    PRESET_ICON_VIDEO_2: _EnumPresetIcon.ValueType
    PRESET_ICON_PHOTO_2: _EnumPresetIcon.ValueType
    PRESET_ICON_PANORAMA: _EnumPresetIcon.ValueType
    PRESET_ICON_BURST_2: _EnumPresetIcon.ValueType
    PRESET_ICON_TIMEWARP_2: _EnumPresetIcon.ValueType
    PRESET_ICON_TIMELAPSE_2: _EnumPresetIcon.ValueType
    PRESET_ICON_CUSTOM: _EnumPresetIcon.ValueType
    PRESET_ICON_AIR: _EnumPresetIcon.ValueType
    PRESET_ICON_BIKE: _EnumPresetIcon.ValueType
    PRESET_ICON_EPIC: _EnumPresetIcon.ValueType
    PRESET_ICON_INDOOR: _EnumPresetIcon.ValueType
    PRESET_ICON_MOTOR: _EnumPresetIcon.ValueType
    PRESET_ICON_MOUNTED: _EnumPresetIcon.ValueType
    PRESET_ICON_OUTDOOR: _EnumPresetIcon.ValueType
    PRESET_ICON_POV: _EnumPresetIcon.ValueType
    PRESET_ICON_SELFIE: _EnumPresetIcon.ValueType
    PRESET_ICON_SKATE: _EnumPresetIcon.ValueType
    PRESET_ICON_SNOW: _EnumPresetIcon.ValueType
    PRESET_ICON_TRAIL: _EnumPresetIcon.ValueType
    PRESET_ICON_TRAVEL: _EnumPresetIcon.ValueType
    PRESET_ICON_WATER: _EnumPresetIcon.ValueType
    PRESET_ICON_LOOPING: _EnumPresetIcon.ValueType
    PRESET_ICON_STARS: _EnumPresetIcon.ValueType
    PRESET_ICON_ACTION: _EnumPresetIcon.ValueType
    PRESET_ICON_FOLLOW_CAM: _EnumPresetIcon.ValueType
    PRESET_ICON_SURF: _EnumPresetIcon.ValueType
    PRESET_ICON_CITY: _EnumPresetIcon.ValueType
    PRESET_ICON_SHAKY: _EnumPresetIcon.ValueType
    PRESET_ICON_CHESTY: _EnumPresetIcon.ValueType
    PRESET_ICON_HELMET: _EnumPresetIcon.ValueType
    PRESET_ICON_BITE: _EnumPresetIcon.ValueType
    PRESET_ICON_CUSTOM_CINEMATIC: _EnumPresetIcon.ValueType
    PRESET_ICON_VLOG: _EnumPresetIcon.ValueType
    PRESET_ICON_FPV: _EnumPresetIcon.ValueType
    PRESET_ICON_HDR: _EnumPresetIcon.ValueType
    PRESET_ICON_LANDSCAPE: _EnumPresetIcon.ValueType
    PRESET_ICON_LOG: _EnumPresetIcon.ValueType
    PRESET_ICON_CUSTOM_SLOMO: _EnumPresetIcon.ValueType
    PRESET_ICON_TRIPOD: _EnumPresetIcon.ValueType
    PRESET_ICON_MAX_VIDEO: _EnumPresetIcon.ValueType
    PRESET_ICON_MAX_PHOTO: _EnumPresetIcon.ValueType
    PRESET_ICON_MAX_TIMEWARP: _EnumPresetIcon.ValueType
    PRESET_ICON_BASIC: _EnumPresetIcon.ValueType
    PRESET_ICON_ULTRA_SLO_MO: _EnumPresetIcon.ValueType
    PRESET_ICON_STANDARD_ENDURANCE: _EnumPresetIcon.ValueType
    PRESET_ICON_ACTIVITY_ENDURANCE: _EnumPresetIcon.ValueType
    PRESET_ICON_CINEMATIC_ENDURANCE: _EnumPresetIcon.ValueType
    PRESET_ICON_SLOMO_ENDURANCE: _EnumPresetIcon.ValueType
    PRESET_ICON_STATIONARY_1: _EnumPresetIcon.ValueType
    PRESET_ICON_STATIONARY_2: _EnumPresetIcon.ValueType
    PRESET_ICON_STATIONARY_3: _EnumPresetIcon.ValueType
    PRESET_ICON_STATIONARY_4: _EnumPresetIcon.ValueType
    PRESET_ICON_SIMPLE_SUPER_PHOTO: _EnumPresetIcon.ValueType
    PRESET_ICON_SIMPLE_NIGHT_PHOTO: _EnumPresetIcon.ValueType
    PRESET_ICON_HIGHEST_QUALITY_VIDEO: _EnumPresetIcon.ValueType
    PRESET_ICON_STANDARD_QUALITY_VIDEO: _EnumPresetIcon.ValueType
    PRESET_ICON_BASIC_QUALITY_VIDEO: _EnumPresetIcon.ValueType
    PRESET_ICON_STAR_TRAIL: _EnumPresetIcon.ValueType
    PRESET_ICON_LIGHT_PAINTING: _EnumPresetIcon.ValueType
    PRESET_ICON_LIGHT_TRAIL: _EnumPresetIcon.ValueType
    PRESET_ICON_FULL_FRAME: _EnumPresetIcon.ValueType
    PRESET_ICON_EASY_MAX_VIDEO: _EnumPresetIcon.ValueType
    PRESET_ICON_EASY_MAX_PHOTO: _EnumPresetIcon.ValueType
    PRESET_ICON_EASY_MAX_TIMEWARP: _EnumPresetIcon.ValueType
    PRESET_ICON_EASY_MAX_STAR_TRAIL: _EnumPresetIcon.ValueType
    PRESET_ICON_EASY_MAX_LIGHT_PAINTING: _EnumPresetIcon.ValueType
    PRESET_ICON_EASY_MAX_LIGHT_TRAIL: _EnumPresetIcon.ValueType
    PRESET_ICON_MAX_STAR_TRAIL: _EnumPresetIcon.ValueType
    PRESET_ICON_MAX_LIGHT_PAINTING: _EnumPresetIcon.ValueType
    PRESET_ICON_MAX_LIGHT_TRAIL: _EnumPresetIcon.ValueType
    PRESET_ICON_EASY_STANDARD_PROFILE: _EnumPresetIcon.ValueType
    PRESET_ICON_EASY_HDR_PROFILE: _EnumPresetIcon.ValueType
    PRESET_ICON_BURST_SLOMO: _EnumPresetIcon.ValueType
    PRESET_ICON_TIMELAPSE_PHOTO: _EnumPresetIcon.ValueType
    PRESET_ICON_NIGHTLAPSE_PHOTO: _EnumPresetIcon.ValueType

class EnumPresetIcon(_EnumPresetIcon, metaclass=_EnumPresetIconEnumTypeWrapper): ...

PRESET_ICON_VIDEO: EnumPresetIcon.ValueType
PRESET_ICON_ACTIVITY: EnumPresetIcon.ValueType
PRESET_ICON_CINEMATIC: EnumPresetIcon.ValueType
PRESET_ICON_PHOTO: EnumPresetIcon.ValueType
PRESET_ICON_LIVE_BURST: EnumPresetIcon.ValueType
PRESET_ICON_BURST: EnumPresetIcon.ValueType
PRESET_ICON_PHOTO_NIGHT: EnumPresetIcon.ValueType
PRESET_ICON_TIMEWARP: EnumPresetIcon.ValueType
PRESET_ICON_TIMELAPSE: EnumPresetIcon.ValueType
PRESET_ICON_NIGHTLAPSE: EnumPresetIcon.ValueType
PRESET_ICON_SNAIL: EnumPresetIcon.ValueType
PRESET_ICON_VIDEO_2: EnumPresetIcon.ValueType
PRESET_ICON_PHOTO_2: EnumPresetIcon.ValueType
PRESET_ICON_PANORAMA: EnumPresetIcon.ValueType
PRESET_ICON_BURST_2: EnumPresetIcon.ValueType
PRESET_ICON_TIMEWARP_2: EnumPresetIcon.ValueType
PRESET_ICON_TIMELAPSE_2: EnumPresetIcon.ValueType
PRESET_ICON_CUSTOM: EnumPresetIcon.ValueType
PRESET_ICON_AIR: EnumPresetIcon.ValueType
PRESET_ICON_BIKE: EnumPresetIcon.ValueType
PRESET_ICON_EPIC: EnumPresetIcon.ValueType
PRESET_ICON_INDOOR: EnumPresetIcon.ValueType
PRESET_ICON_MOTOR: EnumPresetIcon.ValueType
PRESET_ICON_MOUNTED: EnumPresetIcon.ValueType
PRESET_ICON_OUTDOOR: EnumPresetIcon.ValueType
PRESET_ICON_POV: EnumPresetIcon.ValueType
PRESET_ICON_SELFIE: EnumPresetIcon.ValueType
PRESET_ICON_SKATE: EnumPresetIcon.ValueType
PRESET_ICON_SNOW: EnumPresetIcon.ValueType
PRESET_ICON_TRAIL: EnumPresetIcon.ValueType
PRESET_ICON_TRAVEL: EnumPresetIcon.ValueType
PRESET_ICON_WATER: EnumPresetIcon.ValueType
PRESET_ICON_LOOPING: EnumPresetIcon.ValueType
PRESET_ICON_STARS: EnumPresetIcon.ValueType
PRESET_ICON_ACTION: EnumPresetIcon.ValueType
PRESET_ICON_FOLLOW_CAM: EnumPresetIcon.ValueType
PRESET_ICON_SURF: EnumPresetIcon.ValueType
PRESET_ICON_CITY: EnumPresetIcon.ValueType
PRESET_ICON_SHAKY: EnumPresetIcon.ValueType
PRESET_ICON_CHESTY: EnumPresetIcon.ValueType
PRESET_ICON_HELMET: EnumPresetIcon.ValueType
PRESET_ICON_BITE: EnumPresetIcon.ValueType
PRESET_ICON_CUSTOM_CINEMATIC: EnumPresetIcon.ValueType
PRESET_ICON_VLOG: EnumPresetIcon.ValueType
PRESET_ICON_FPV: EnumPresetIcon.ValueType
PRESET_ICON_HDR: EnumPresetIcon.ValueType
PRESET_ICON_LANDSCAPE: EnumPresetIcon.ValueType
PRESET_ICON_LOG: EnumPresetIcon.ValueType
PRESET_ICON_CUSTOM_SLOMO: EnumPresetIcon.ValueType
PRESET_ICON_TRIPOD: EnumPresetIcon.ValueType
PRESET_ICON_MAX_VIDEO: EnumPresetIcon.ValueType
PRESET_ICON_MAX_PHOTO: EnumPresetIcon.ValueType
PRESET_ICON_MAX_TIMEWARP: EnumPresetIcon.ValueType
PRESET_ICON_BASIC: EnumPresetIcon.ValueType
PRESET_ICON_ULTRA_SLO_MO: EnumPresetIcon.ValueType
PRESET_ICON_STANDARD_ENDURANCE: EnumPresetIcon.ValueType
PRESET_ICON_ACTIVITY_ENDURANCE: EnumPresetIcon.ValueType
PRESET_ICON_CINEMATIC_ENDURANCE: EnumPresetIcon.ValueType
PRESET_ICON_SLOMO_ENDURANCE: EnumPresetIcon.ValueType
PRESET_ICON_STATIONARY_1: EnumPresetIcon.ValueType
PRESET_ICON_STATIONARY_2: EnumPresetIcon.ValueType
PRESET_ICON_STATIONARY_3: EnumPresetIcon.ValueType
PRESET_ICON_STATIONARY_4: EnumPresetIcon.ValueType
PRESET_ICON_SIMPLE_SUPER_PHOTO: EnumPresetIcon.ValueType
PRESET_ICON_SIMPLE_NIGHT_PHOTO: EnumPresetIcon.ValueType
PRESET_ICON_HIGHEST_QUALITY_VIDEO: EnumPresetIcon.ValueType
PRESET_ICON_STANDARD_QUALITY_VIDEO: EnumPresetIcon.ValueType
PRESET_ICON_BASIC_QUALITY_VIDEO: EnumPresetIcon.ValueType
PRESET_ICON_STAR_TRAIL: EnumPresetIcon.ValueType
PRESET_ICON_LIGHT_PAINTING: EnumPresetIcon.ValueType
PRESET_ICON_LIGHT_TRAIL: EnumPresetIcon.ValueType
PRESET_ICON_FULL_FRAME: EnumPresetIcon.ValueType
PRESET_ICON_EASY_MAX_VIDEO: EnumPresetIcon.ValueType
PRESET_ICON_EASY_MAX_PHOTO: EnumPresetIcon.ValueType
PRESET_ICON_EASY_MAX_TIMEWARP: EnumPresetIcon.ValueType
PRESET_ICON_EASY_MAX_STAR_TRAIL: EnumPresetIcon.ValueType
PRESET_ICON_EASY_MAX_LIGHT_PAINTING: EnumPresetIcon.ValueType
PRESET_ICON_EASY_MAX_LIGHT_TRAIL: EnumPresetIcon.ValueType
PRESET_ICON_MAX_STAR_TRAIL: EnumPresetIcon.ValueType
PRESET_ICON_MAX_LIGHT_PAINTING: EnumPresetIcon.ValueType
PRESET_ICON_MAX_LIGHT_TRAIL: EnumPresetIcon.ValueType
PRESET_ICON_EASY_STANDARD_PROFILE: EnumPresetIcon.ValueType
PRESET_ICON_EASY_HDR_PROFILE: EnumPresetIcon.ValueType
PRESET_ICON_BURST_SLOMO: EnumPresetIcon.ValueType
PRESET_ICON_TIMELAPSE_PHOTO: EnumPresetIcon.ValueType
PRESET_ICON_NIGHTLAPSE_PHOTO: EnumPresetIcon.ValueType
global___EnumPresetIcon = EnumPresetIcon

class _EnumPresetTitle:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _EnumPresetTitleEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_EnumPresetTitle.ValueType], builtins.type
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PRESET_TITLE_ACTIVITY: _EnumPresetTitle.ValueType
    PRESET_TITLE_STANDARD: _EnumPresetTitle.ValueType
    PRESET_TITLE_CINEMATIC: _EnumPresetTitle.ValueType
    PRESET_TITLE_PHOTO: _EnumPresetTitle.ValueType
    PRESET_TITLE_LIVE_BURST: _EnumPresetTitle.ValueType
    PRESET_TITLE_BURST: _EnumPresetTitle.ValueType
    PRESET_TITLE_NIGHT: _EnumPresetTitle.ValueType
    PRESET_TITLE_TIME_WARP: _EnumPresetTitle.ValueType
    PRESET_TITLE_TIME_LAPSE: _EnumPresetTitle.ValueType
    PRESET_TITLE_NIGHT_LAPSE: _EnumPresetTitle.ValueType
    PRESET_TITLE_VIDEO: _EnumPresetTitle.ValueType
    PRESET_TITLE_SLOMO: _EnumPresetTitle.ValueType
    PRESET_TITLE_PHOTO_2: _EnumPresetTitle.ValueType
    PRESET_TITLE_PANORAMA: _EnumPresetTitle.ValueType
    PRESET_TITLE_TIME_WARP_2: _EnumPresetTitle.ValueType
    PRESET_TITLE_CUSTOM: _EnumPresetTitle.ValueType
    PRESET_TITLE_AIR: _EnumPresetTitle.ValueType
    PRESET_TITLE_BIKE: _EnumPresetTitle.ValueType
    PRESET_TITLE_EPIC: _EnumPresetTitle.ValueType
    PRESET_TITLE_INDOOR: _EnumPresetTitle.ValueType
    PRESET_TITLE_MOTOR: _EnumPresetTitle.ValueType
    PRESET_TITLE_MOUNTED: _EnumPresetTitle.ValueType
    PRESET_TITLE_OUTDOOR: _EnumPresetTitle.ValueType
    PRESET_TITLE_POV: _EnumPresetTitle.ValueType
    PRESET_TITLE_SELFIE: _EnumPresetTitle.ValueType
    PRESET_TITLE_SKATE: _EnumPresetTitle.ValueType
    PRESET_TITLE_SNOW: _EnumPresetTitle.ValueType
    PRESET_TITLE_TRAIL: _EnumPresetTitle.ValueType
    PRESET_TITLE_TRAVEL: _EnumPresetTitle.ValueType
    PRESET_TITLE_WATER: _EnumPresetTitle.ValueType
    PRESET_TITLE_LOOPING: _EnumPresetTitle.ValueType
    PRESET_TITLE_STARS: _EnumPresetTitle.ValueType
    PRESET_TITLE_ACTION: _EnumPresetTitle.ValueType
    PRESET_TITLE_FOLLOW_CAM: _EnumPresetTitle.ValueType
    PRESET_TITLE_SURF: _EnumPresetTitle.ValueType
    PRESET_TITLE_CITY: _EnumPresetTitle.ValueType
    PRESET_TITLE_SHAKY: _EnumPresetTitle.ValueType
    PRESET_TITLE_CHESTY: _EnumPresetTitle.ValueType
    PRESET_TITLE_HELMET: _EnumPresetTitle.ValueType
    PRESET_TITLE_BITE: _EnumPresetTitle.ValueType
    PRESET_TITLE_CUSTOM_CINEMATIC: _EnumPresetTitle.ValueType
    PRESET_TITLE_VLOG: _EnumPresetTitle.ValueType
    PRESET_TITLE_FPV: _EnumPresetTitle.ValueType
    PRESET_TITLE_HDR: _EnumPresetTitle.ValueType
    PRESET_TITLE_LANDSCAPE: _EnumPresetTitle.ValueType
    PRESET_TITLE_LOG: _EnumPresetTitle.ValueType
    PRESET_TITLE_CUSTOM_SLOMO: _EnumPresetTitle.ValueType
    PRESET_TITLE_TRIPOD: _EnumPresetTitle.ValueType
    PRESET_TITLE_BASIC: _EnumPresetTitle.ValueType
    PRESET_TITLE_ULTRA_SLO_MO: _EnumPresetTitle.ValueType
    PRESET_TITLE_STANDARD_ENDURANCE: _EnumPresetTitle.ValueType
    PRESET_TITLE_ACTIVITY_ENDURANCE: _EnumPresetTitle.ValueType
    PRESET_TITLE_CINEMATIC_ENDURANCE: _EnumPresetTitle.ValueType
    PRESET_TITLE_SLOMO_ENDURANCE: _EnumPresetTitle.ValueType
    PRESET_TITLE_STATIONARY_1: _EnumPresetTitle.ValueType
    PRESET_TITLE_STATIONARY_2: _EnumPresetTitle.ValueType
    PRESET_TITLE_STATIONARY_3: _EnumPresetTitle.ValueType
    PRESET_TITLE_STATIONARY_4: _EnumPresetTitle.ValueType
    PRESET_TITLE_SIMPLE_VIDEO: _EnumPresetTitle.ValueType
    PRESET_TITLE_SIMPLE_TIME_WARP: _EnumPresetTitle.ValueType
    PRESET_TITLE_SIMPLE_SUPER_PHOTO: _EnumPresetTitle.ValueType
    PRESET_TITLE_SIMPLE_NIGHT_PHOTO: _EnumPresetTitle.ValueType
    PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE: _EnumPresetTitle.ValueType
    PRESET_TITLE_HIGHEST_QUALITY: _EnumPresetTitle.ValueType
    PRESET_TITLE_EXTENDED_BATTERY: _EnumPresetTitle.ValueType
    PRESET_TITLE_LONGEST_BATTERY: _EnumPresetTitle.ValueType
    PRESET_TITLE_STAR_TRAIL: _EnumPresetTitle.ValueType
    PRESET_TITLE_LIGHT_PAINTING: _EnumPresetTitle.ValueType
    PRESET_TITLE_LIGHT_TRAIL: _EnumPresetTitle.ValueType
    PRESET_TITLE_FULL_FRAME: _EnumPresetTitle.ValueType
    PRESET_TITLE_STANDARD_QUALITY_VIDEO: _EnumPresetTitle.ValueType
    PRESET_TITLE_BASIC_QUALITY_VIDEO: _EnumPresetTitle.ValueType
    PRESET_TITLE_HIGHEST_QUALITY_VIDEO: _EnumPresetTitle.ValueType
    PRESET_TITLE_USER_DEFINED_CUSTOM_NAME: _EnumPresetTitle.ValueType
    PRESET_TITLE_EASY_STANDARD_PROFILE: _EnumPresetTitle.ValueType
    PRESET_TITLE_EASY_HDR_PROFILE: _EnumPresetTitle.ValueType
    PRESET_TITLE_BURST_SLOMO: _EnumPresetTitle.ValueType
    PRESET_TITLE_4_3_VIDEO: _EnumPresetTitle.ValueType
    PRESET_TITLE_16_9_VIDEO: _EnumPresetTitle.ValueType
    PRESET_TITLE_16_9_SLOMO: _EnumPresetTitle.ValueType

class EnumPresetTitle(_EnumPresetTitle, metaclass=_EnumPresetTitleEnumTypeWrapper): ...

PRESET_TITLE_ACTIVITY: EnumPresetTitle.ValueType
PRESET_TITLE_STANDARD: EnumPresetTitle.ValueType
PRESET_TITLE_CINEMATIC: EnumPresetTitle.ValueType
PRESET_TITLE_PHOTO: EnumPresetTitle.ValueType
PRESET_TITLE_LIVE_BURST: EnumPresetTitle.ValueType
PRESET_TITLE_BURST: EnumPresetTitle.ValueType
PRESET_TITLE_NIGHT: EnumPresetTitle.ValueType
PRESET_TITLE_TIME_WARP: EnumPresetTitle.ValueType
PRESET_TITLE_TIME_LAPSE: EnumPresetTitle.ValueType
PRESET_TITLE_NIGHT_LAPSE: EnumPresetTitle.ValueType
PRESET_TITLE_VIDEO: EnumPresetTitle.ValueType
PRESET_TITLE_SLOMO: EnumPresetTitle.ValueType
PRESET_TITLE_PHOTO_2: EnumPresetTitle.ValueType
PRESET_TITLE_PANORAMA: EnumPresetTitle.ValueType
PRESET_TITLE_TIME_WARP_2: EnumPresetTitle.ValueType
PRESET_TITLE_CUSTOM: EnumPresetTitle.ValueType
PRESET_TITLE_AIR: EnumPresetTitle.ValueType
PRESET_TITLE_BIKE: EnumPresetTitle.ValueType
PRESET_TITLE_EPIC: EnumPresetTitle.ValueType
PRESET_TITLE_INDOOR: EnumPresetTitle.ValueType
PRESET_TITLE_MOTOR: EnumPresetTitle.ValueType
PRESET_TITLE_MOUNTED: EnumPresetTitle.ValueType
PRESET_TITLE_OUTDOOR: EnumPresetTitle.ValueType
PRESET_TITLE_POV: EnumPresetTitle.ValueType
PRESET_TITLE_SELFIE: EnumPresetTitle.ValueType
PRESET_TITLE_SKATE: EnumPresetTitle.ValueType
PRESET_TITLE_SNOW: EnumPresetTitle.ValueType
PRESET_TITLE_TRAIL: EnumPresetTitle.ValueType
PRESET_TITLE_TRAVEL: EnumPresetTitle.ValueType
PRESET_TITLE_WATER: EnumPresetTitle.ValueType
PRESET_TITLE_LOOPING: EnumPresetTitle.ValueType
PRESET_TITLE_STARS: EnumPresetTitle.ValueType
PRESET_TITLE_ACTION: EnumPresetTitle.ValueType
PRESET_TITLE_FOLLOW_CAM: EnumPresetTitle.ValueType
PRESET_TITLE_SURF: EnumPresetTitle.ValueType
PRESET_TITLE_CITY: EnumPresetTitle.ValueType
PRESET_TITLE_SHAKY: EnumPresetTitle.ValueType
PRESET_TITLE_CHESTY: EnumPresetTitle.ValueType
PRESET_TITLE_HELMET: EnumPresetTitle.ValueType
PRESET_TITLE_BITE: EnumPresetTitle.ValueType
PRESET_TITLE_CUSTOM_CINEMATIC: EnumPresetTitle.ValueType
PRESET_TITLE_VLOG: EnumPresetTitle.ValueType
PRESET_TITLE_FPV: EnumPresetTitle.ValueType
PRESET_TITLE_HDR: EnumPresetTitle.ValueType
PRESET_TITLE_LANDSCAPE: EnumPresetTitle.ValueType
PRESET_TITLE_LOG: EnumPresetTitle.ValueType
PRESET_TITLE_CUSTOM_SLOMO: EnumPresetTitle.ValueType
PRESET_TITLE_TRIPOD: EnumPresetTitle.ValueType
PRESET_TITLE_BASIC: EnumPresetTitle.ValueType
PRESET_TITLE_ULTRA_SLO_MO: EnumPresetTitle.ValueType
PRESET_TITLE_STANDARD_ENDURANCE: EnumPresetTitle.ValueType
PRESET_TITLE_ACTIVITY_ENDURANCE: EnumPresetTitle.ValueType
PRESET_TITLE_CINEMATIC_ENDURANCE: EnumPresetTitle.ValueType
PRESET_TITLE_SLOMO_ENDURANCE: EnumPresetTitle.ValueType
PRESET_TITLE_STATIONARY_1: EnumPresetTitle.ValueType
PRESET_TITLE_STATIONARY_2: EnumPresetTitle.ValueType
PRESET_TITLE_STATIONARY_3: EnumPresetTitle.ValueType
PRESET_TITLE_STATIONARY_4: EnumPresetTitle.ValueType
PRESET_TITLE_SIMPLE_VIDEO: EnumPresetTitle.ValueType
PRESET_TITLE_SIMPLE_TIME_WARP: EnumPresetTitle.ValueType
PRESET_TITLE_SIMPLE_SUPER_PHOTO: EnumPresetTitle.ValueType
PRESET_TITLE_SIMPLE_NIGHT_PHOTO: EnumPresetTitle.ValueType
PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE: EnumPresetTitle.ValueType
PRESET_TITLE_HIGHEST_QUALITY: EnumPresetTitle.ValueType
PRESET_TITLE_EXTENDED_BATTERY: EnumPresetTitle.ValueType
PRESET_TITLE_LONGEST_BATTERY: EnumPresetTitle.ValueType
PRESET_TITLE_STAR_TRAIL: EnumPresetTitle.ValueType
PRESET_TITLE_LIGHT_PAINTING: EnumPresetTitle.ValueType
PRESET_TITLE_LIGHT_TRAIL: EnumPresetTitle.ValueType
PRESET_TITLE_FULL_FRAME: EnumPresetTitle.ValueType
PRESET_TITLE_STANDARD_QUALITY_VIDEO: EnumPresetTitle.ValueType
PRESET_TITLE_BASIC_QUALITY_VIDEO: EnumPresetTitle.ValueType
PRESET_TITLE_HIGHEST_QUALITY_VIDEO: EnumPresetTitle.ValueType
PRESET_TITLE_USER_DEFINED_CUSTOM_NAME: EnumPresetTitle.ValueType
PRESET_TITLE_EASY_STANDARD_PROFILE: EnumPresetTitle.ValueType
PRESET_TITLE_EASY_HDR_PROFILE: EnumPresetTitle.ValueType
PRESET_TITLE_BURST_SLOMO: EnumPresetTitle.ValueType
PRESET_TITLE_4_3_VIDEO: EnumPresetTitle.ValueType
PRESET_TITLE_16_9_VIDEO: EnumPresetTitle.ValueType
PRESET_TITLE_16_9_SLOMO: EnumPresetTitle.ValueType
global___EnumPresetTitle = EnumPresetTitle

@typing_extensions.final
class NotifyPresetStatus(google.protobuf.message.Message):
    """*
    Current Preset status

    Sent either:

    - Synchronously via initial response to @ref RequestGetPresetStatus
    - Asynchronously when Preset change if registered in @ref RequestGetPresetStatus
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PRESET_GROUP_ARRAY_FIELD_NUMBER: builtins.int

    @property
    def preset_group_array(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PresetGroup]:
        """List of currently available Preset Groups"""

    def __init__(self, *, preset_group_array: collections.abc.Iterable[global___PresetGroup] | None = ...) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["preset_group_array", b"preset_group_array"]
    ) -> None: ...

global___NotifyPresetStatus = NotifyPresetStatus

@typing_extensions.final
class Preset(google.protobuf.message.Message):
    """*
    An individual preset.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ID_FIELD_NUMBER: builtins.int
    MODE_FIELD_NUMBER: builtins.int
    TITLE_ID_FIELD_NUMBER: builtins.int
    TITLE_NUMBER_FIELD_NUMBER: builtins.int
    USER_DEFINED_FIELD_NUMBER: builtins.int
    ICON_FIELD_NUMBER: builtins.int
    SETTING_ARRAY_FIELD_NUMBER: builtins.int
    IS_MODIFIED_FIELD_NUMBER: builtins.int
    IS_FIXED_FIELD_NUMBER: builtins.int
    CUSTOM_NAME_FIELD_NUMBER: builtins.int
    id: builtins.int
    "Preset ID"
    mode: global___EnumFlatMode.ValueType
    "Preset flatmode ID"
    title_id: global___EnumPresetTitle.ValueType
    "Preset Title ID"
    title_number: builtins.int
    "Preset Title Number (e.g. 1/2/3 in Custom1, Custom2, Custom3)"
    user_defined: builtins.bool
    "Is the Preset custom/user-defined?"
    icon: global___EnumPresetIcon.ValueType
    "Preset Icon ID"

    @property
    def setting_array(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___PresetSetting]:
        """Array of settings associated with this Preset"""
    is_modified: builtins.bool
    "Has Preset been modified from factory defaults? (False for user-defined Presets)"
    is_fixed: builtins.bool
    "Is this Preset mutable?"
    custom_name: builtins.str
    "Custom string name given to this preset via @ref RequestCustomPresetUpdate"

    def __init__(
        self,
        *,
        id: builtins.int | None = ...,
        mode: global___EnumFlatMode.ValueType | None = ...,
        title_id: global___EnumPresetTitle.ValueType | None = ...,
        title_number: builtins.int | None = ...,
        user_defined: builtins.bool | None = ...,
        icon: global___EnumPresetIcon.ValueType | None = ...,
        setting_array: collections.abc.Iterable[global___PresetSetting] | None = ...,
        is_modified: builtins.bool | None = ...,
        is_fixed: builtins.bool | None = ...,
        custom_name: builtins.str | None = ...
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "custom_name",
            b"custom_name",
            "icon",
            b"icon",
            "id",
            b"id",
            "is_fixed",
            b"is_fixed",
            "is_modified",
            b"is_modified",
            "mode",
            b"mode",
            "title_id",
            b"title_id",
            "title_number",
            b"title_number",
            "user_defined",
            b"user_defined",
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "custom_name",
            b"custom_name",
            "icon",
            b"icon",
            "id",
            b"id",
            "is_fixed",
            b"is_fixed",
            "is_modified",
            b"is_modified",
            "mode",
            b"mode",
            "setting_array",
            b"setting_array",
            "title_id",
            b"title_id",
            "title_number",
            b"title_number",
            "user_defined",
            b"user_defined",
        ],
    ) -> None: ...

global___Preset = Preset

@typing_extensions.final
class RequestCustomPresetUpdate(google.protobuf.message.Message):
    """*
    Request to Update the Title and / or Icon of the Active Custom Preset

    This only operates on the currently active Preset and will fail  if the current
    Preset is not custom.

    The use cases are:

    1. Update the Custom Preset Icon

        - `icon_id` is always optional and can always be passed

    and / or

    2. Update the Custom Preset Title to a...

         - **Factory Preset Title**: Set `title_id` to a non-PRESET_TITLE_USER_DEFINED_CUSTOM_NAME (94) value
         - **Custom Preset Name**: Set `title_id` to PRESET_TITLE_USER_DEFINED_CUSTOM_NAME (94) and specify a `custom_name`

    Returns a @ref ResponseGeneric with the status of the preset update request.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TITLE_ID_FIELD_NUMBER: builtins.int
    CUSTOM_NAME_FIELD_NUMBER: builtins.int
    ICON_ID_FIELD_NUMBER: builtins.int
    title_id: global___EnumPresetTitle.ValueType
    "*\n    Preset Title ID\n\n    The range of acceptable custom title ID's can be found in the initial @ref NotifyPresetStatus response\n    to @ref RequestGetPresetStatus\n    "
    custom_name: builtins.str
    "*\n    UTF-8 encoded custom preset name to be used if `title_id` is set to 94 (PRESET_TITLE_USER_DEFINED_CUSTOM_NAME)\n\n    The name must obey the following:\n\n      - Custom titles must be between 1 and 16 characters (inclusive)\n      - No special characters outside of the following languages: English, French, Italian, German,\n        Spanish, Portuguese, Swedish, Russian\n    "
    icon_id: global___EnumPresetIcon.ValueType
    "*\n    Preset Icon ID\n\n    The range of acceptable custom icon ID's can be found in the initial @ref NotifyPresetStatus response to\n    @ref RequestGetPresetStatus\n    "

    def __init__(
        self,
        *,
        title_id: global___EnumPresetTitle.ValueType | None = ...,
        custom_name: builtins.str | None = ...,
        icon_id: global___EnumPresetIcon.ValueType | None = ...
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "custom_name", b"custom_name", "icon_id", b"icon_id", "title_id", b"title_id"
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "custom_name", b"custom_name", "icon_id", b"icon_id", "title_id", b"title_id"
        ],
    ) -> None: ...

global___RequestCustomPresetUpdate = RequestCustomPresetUpdate

@typing_extensions.final
class PresetGroup(google.protobuf.message.Message):
    """
    Preset Group meta information and contained Presets
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ID_FIELD_NUMBER: builtins.int
    PRESET_ARRAY_FIELD_NUMBER: builtins.int
    CAN_ADD_PRESET_FIELD_NUMBER: builtins.int
    ICON_FIELD_NUMBER: builtins.int
    MODE_ARRAY_FIELD_NUMBER: builtins.int
    id: global___EnumPresetGroup.ValueType
    "Preset Group ID"

    @property
    def preset_array(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Preset]:
        """Array of Presets contained in this Preset Group"""
    can_add_preset: builtins.bool
    "Is there room in the group to add additional Presets?"
    icon: global___EnumPresetGroupIcon.ValueType
    "The icon to display for this preset group"

    @property
    def mode_array(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[global___EnumFlatMode.ValueType]:
        """A list of flatmodes available for this preset group"""

    def __init__(
        self,
        *,
        id: global___EnumPresetGroup.ValueType | None = ...,
        preset_array: collections.abc.Iterable[global___Preset] | None = ...,
        can_add_preset: builtins.bool | None = ...,
        icon: global___EnumPresetGroupIcon.ValueType | None = ...,
        mode_array: collections.abc.Iterable[global___EnumFlatMode.ValueType] | None = ...
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["can_add_preset", b"can_add_preset", "icon", b"icon", "id", b"id"]
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "can_add_preset",
            b"can_add_preset",
            "icon",
            b"icon",
            "id",
            b"id",
            "mode_array",
            b"mode_array",
            "preset_array",
            b"preset_array",
        ],
    ) -> None: ...

global___PresetGroup = PresetGroup

@typing_extensions.final
class PresetSetting(google.protobuf.message.Message):
    """*
    Setting representation that comprises a  @ref Preset
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ID_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    IS_CAPTION_FIELD_NUMBER: builtins.int
    id: builtins.int
    "Setting ID"
    value: builtins.int
    "Setting value"
    is_caption: builtins.bool
    'Does this setting appear on the Preset "pill" in the camera UI?'

    def __init__(
        self, *, id: builtins.int | None = ..., value: builtins.int | None = ..., is_caption: builtins.bool | None = ...
    ) -> None: ...
    def HasField(
        self, field_name: typing_extensions.Literal["id", b"id", "is_caption", b"is_caption", "value", b"value"]
    ) -> builtins.bool: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["id", b"id", "is_caption", b"is_caption", "value", b"value"]
    ) -> None: ...

global___PresetSetting = PresetSetting
