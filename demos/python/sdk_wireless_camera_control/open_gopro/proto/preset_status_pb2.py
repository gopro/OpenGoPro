# preset_status_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Feb 21 18:05:42 UTC 2025

import sys

_b = ((sys.version_info[0] < 3) and (lambda x: x)) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import enum_type_wrapper

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="preset_status.proto",
    package="open_gopro",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x13preset_status.proto\x12\nopen_gopro\x1a\x16response_generic.proto"I\n\x12NotifyPresetStatus\x123\n\x12preset_group_array\x18\x01 \x03(\x0b2\x17.open_gopro.PresetGroup"¯\x02\n\x06Preset\x12\n\n\x02id\x18\x01 \x01(\x05\x12&\n\x04mode\x18\x02 \x01(\x0e2\x18.open_gopro.EnumFlatMode\x12-\n\x08title_id\x18\x03 \x01(\x0e2\x1b.open_gopro.EnumPresetTitle\x12\x14\n\x0ctitle_number\x18\x04 \x01(\x05\x12\x14\n\x0cuser_defined\x18\x05 \x01(\x08\x12(\n\x04icon\x18\x06 \x01(\x0e2\x1a.open_gopro.EnumPresetIcon\x120\n\rsetting_array\x18\x07 \x03(\x0b2\x19.open_gopro.PresetSetting\x12\x13\n\x0bis_modified\x18\x08 \x01(\x08\x12\x10\n\x08is_fixed\x18\t \x01(\x08\x12\x13\n\x0bcustom_name\x18\n \x01(\t"\x8c\x01\n\x19RequestCustomPresetUpdate\x12-\n\x08title_id\x18\x01 \x01(\x0e2\x1b.open_gopro.EnumPresetTitle\x12\x13\n\x0bcustom_name\x18\x02 \x01(\t\x12+\n\x07icon_id\x18\x03 \x01(\x0e2\x1a.open_gopro.EnumPresetIcon"Õ\x01\n\x0bPresetGroup\x12\'\n\x02id\x18\x01 \x01(\x0e2\x1b.open_gopro.EnumPresetGroup\x12(\n\x0cpreset_array\x18\x02 \x03(\x0b2\x12.open_gopro.Preset\x12\x16\n\x0ecan_add_preset\x18\x03 \x01(\x08\x12-\n\x04icon\x18\x04 \x01(\x0e2\x1f.open_gopro.EnumPresetGroupIcon\x12,\n\nmode_array\x18\x05 \x03(\x0e2\x18.open_gopro.EnumFlatMode">\n\rPresetSetting\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05\x12\x12\n\nis_caption\x18\x03 \x01(\x08*\x9b\x05\n\x0cEnumFlatMode\x12\x1e\n\x11FLAT_MODE_UNKNOWN\x10ÿÿÿÿÿÿÿÿÿ\x01\x12\x16\n\x12FLAT_MODE_PLAYBACK\x10\x04\x12\x13\n\x0fFLAT_MODE_SETUP\x10\x05\x12\x13\n\x0fFLAT_MODE_VIDEO\x10\x0c\x12\x1e\n\x1aFLAT_MODE_TIME_LAPSE_VIDEO\x10\r\x12\x15\n\x11FLAT_MODE_LOOPING\x10\x0f\x12\x1a\n\x16FLAT_MODE_PHOTO_SINGLE\x10\x10\x12\x13\n\x0fFLAT_MODE_PHOTO\x10\x11\x12\x19\n\x15FLAT_MODE_PHOTO_NIGHT\x10\x12\x12\x19\n\x15FLAT_MODE_PHOTO_BURST\x10\x13\x12\x1e\n\x1aFLAT_MODE_TIME_LAPSE_PHOTO\x10\x14\x12\x1f\n\x1bFLAT_MODE_NIGHT_LAPSE_PHOTO\x10\x15\x12\x1e\n\x1aFLAT_MODE_BROADCAST_RECORD\x10\x16\x12!\n\x1dFLAT_MODE_BROADCAST_BROADCAST\x10\x17\x12\x1d\n\x19FLAT_MODE_TIME_WARP_VIDEO\x10\x18\x12\x18\n\x14FLAT_MODE_LIVE_BURST\x10\x19\x12\x1f\n\x1bFLAT_MODE_NIGHT_LAPSE_VIDEO\x10\x1a\x12\x13\n\x0fFLAT_MODE_SLOMO\x10\x1b\x12\x12\n\x0eFLAT_MODE_IDLE\x10\x1c\x12\x1e\n\x1aFLAT_MODE_VIDEO_STAR_TRAIL\x10\x1d\x12"\n\x1eFLAT_MODE_VIDEO_LIGHT_PAINTING\x10\x1e\x12\x1f\n\x1bFLAT_MODE_VIDEO_LIGHT_TRAIL\x10\x1f\x12\x1f\n\x1bFLAT_MODE_VIDEO_BURST_SLOMO\x10 *i\n\x0fEnumPresetGroup\x12\x1a\n\x15PRESET_GROUP_ID_VIDEO\x10è\x07\x12\x1a\n\x15PRESET_GROUP_ID_PHOTO\x10é\x07\x12\x1e\n\x19PRESET_GROUP_ID_TIMELAPSE\x10ê\x07*µ\x03\n\x13EnumPresetGroupIcon\x12\x1e\n\x1aPRESET_GROUP_VIDEO_ICON_ID\x10\x00\x12\x1e\n\x1aPRESET_GROUP_PHOTO_ICON_ID\x10\x01\x12"\n\x1ePRESET_GROUP_TIMELAPSE_ICON_ID\x10\x02\x12\'\n#PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID\x10\x03\x12(\n$PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID\x10\x04\x12"\n\x1ePRESET_GROUP_MAX_VIDEO_ICON_ID\x10\x05\x12"\n\x1ePRESET_GROUP_MAX_PHOTO_ICON_ID\x10\x06\x12&\n"PRESET_GROUP_MAX_TIMELAPSE_ICON_ID\x10\x07\x12%\n!PRESET_GROUP_ND_MOD_VIDEO_ICON_ID\x10\x08\x12%\n!PRESET_GROUP_ND_MOD_PHOTO_ICON_ID\x10\t\x12)\n%PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID\x10\n*ÿ\x12\n\x0eEnumPresetIcon\x12\x15\n\x11PRESET_ICON_VIDEO\x10\x00\x12\x18\n\x14PRESET_ICON_ACTIVITY\x10\x01\x12\x19\n\x15PRESET_ICON_CINEMATIC\x10\x02\x12\x15\n\x11PRESET_ICON_PHOTO\x10\x03\x12\x1a\n\x16PRESET_ICON_LIVE_BURST\x10\x04\x12\x15\n\x11PRESET_ICON_BURST\x10\x05\x12\x1b\n\x17PRESET_ICON_PHOTO_NIGHT\x10\x06\x12\x18\n\x14PRESET_ICON_TIMEWARP\x10\x07\x12\x19\n\x15PRESET_ICON_TIMELAPSE\x10\x08\x12\x1a\n\x16PRESET_ICON_NIGHTLAPSE\x10\t\x12\x15\n\x11PRESET_ICON_SNAIL\x10\n\x12\x17\n\x13PRESET_ICON_VIDEO_2\x10\x0b\x12\x17\n\x13PRESET_ICON_PHOTO_2\x10\r\x12\x18\n\x14PRESET_ICON_PANORAMA\x10\x0e\x12\x17\n\x13PRESET_ICON_BURST_2\x10\x0f\x12\x1a\n\x16PRESET_ICON_TIMEWARP_2\x10\x10\x12\x1b\n\x17PRESET_ICON_TIMELAPSE_2\x10\x11\x12\x16\n\x12PRESET_ICON_CUSTOM\x10\x12\x12\x13\n\x0fPRESET_ICON_AIR\x10\x13\x12\x14\n\x10PRESET_ICON_BIKE\x10\x14\x12\x14\n\x10PRESET_ICON_EPIC\x10\x15\x12\x16\n\x12PRESET_ICON_INDOOR\x10\x16\x12\x15\n\x11PRESET_ICON_MOTOR\x10\x17\x12\x17\n\x13PRESET_ICON_MOUNTED\x10\x18\x12\x17\n\x13PRESET_ICON_OUTDOOR\x10\x19\x12\x13\n\x0fPRESET_ICON_POV\x10\x1a\x12\x16\n\x12PRESET_ICON_SELFIE\x10\x1b\x12\x15\n\x11PRESET_ICON_SKATE\x10\x1c\x12\x14\n\x10PRESET_ICON_SNOW\x10\x1d\x12\x15\n\x11PRESET_ICON_TRAIL\x10\x1e\x12\x16\n\x12PRESET_ICON_TRAVEL\x10\x1f\x12\x15\n\x11PRESET_ICON_WATER\x10 \x12\x17\n\x13PRESET_ICON_LOOPING\x10!\x12\x15\n\x11PRESET_ICON_STARS\x10"\x12\x16\n\x12PRESET_ICON_ACTION\x10#\x12\x1a\n\x16PRESET_ICON_FOLLOW_CAM\x10$\x12\x14\n\x10PRESET_ICON_SURF\x10%\x12\x14\n\x10PRESET_ICON_CITY\x10&\x12\x15\n\x11PRESET_ICON_SHAKY\x10\'\x12\x16\n\x12PRESET_ICON_CHESTY\x10(\x12\x16\n\x12PRESET_ICON_HELMET\x10)\x12\x14\n\x10PRESET_ICON_BITE\x10*\x12 \n\x1cPRESET_ICON_CUSTOM_CINEMATIC\x10+\x12\x14\n\x10PRESET_ICON_VLOG\x10,\x12\x13\n\x0fPRESET_ICON_FPV\x10-\x12\x13\n\x0fPRESET_ICON_HDR\x10.\x12\x19\n\x15PRESET_ICON_LANDSCAPE\x10/\x12\x13\n\x0fPRESET_ICON_LOG\x100\x12\x1c\n\x18PRESET_ICON_CUSTOM_SLOMO\x101\x12\x16\n\x12PRESET_ICON_TRIPOD\x102\x12\x19\n\x15PRESET_ICON_MAX_VIDEO\x107\x12\x19\n\x15PRESET_ICON_MAX_PHOTO\x108\x12\x1c\n\x18PRESET_ICON_MAX_TIMEWARP\x109\x12\x15\n\x11PRESET_ICON_BASIC\x10:\x12\x1c\n\x18PRESET_ICON_ULTRA_SLO_MO\x10;\x12"\n\x1ePRESET_ICON_STANDARD_ENDURANCE\x10<\x12"\n\x1ePRESET_ICON_ACTIVITY_ENDURANCE\x10=\x12#\n\x1fPRESET_ICON_CINEMATIC_ENDURANCE\x10>\x12\x1f\n\x1bPRESET_ICON_SLOMO_ENDURANCE\x10?\x12\x1c\n\x18PRESET_ICON_STATIONARY_1\x10@\x12\x1c\n\x18PRESET_ICON_STATIONARY_2\x10A\x12\x1c\n\x18PRESET_ICON_STATIONARY_3\x10B\x12\x1c\n\x18PRESET_ICON_STATIONARY_4\x10C\x12"\n\x1ePRESET_ICON_SIMPLE_SUPER_PHOTO\x10F\x12"\n\x1ePRESET_ICON_SIMPLE_NIGHT_PHOTO\x10G\x12%\n!PRESET_ICON_HIGHEST_QUALITY_VIDEO\x10I\x12&\n"PRESET_ICON_STANDARD_QUALITY_VIDEO\x10J\x12#\n\x1fPRESET_ICON_BASIC_QUALITY_VIDEO\x10K\x12\x1a\n\x16PRESET_ICON_STAR_TRAIL\x10L\x12\x1e\n\x1aPRESET_ICON_LIGHT_PAINTING\x10M\x12\x1b\n\x17PRESET_ICON_LIGHT_TRAIL\x10N\x12\x1a\n\x16PRESET_ICON_FULL_FRAME\x10O\x12\x1e\n\x1aPRESET_ICON_EASY_MAX_VIDEO\x10P\x12\x1e\n\x1aPRESET_ICON_EASY_MAX_PHOTO\x10Q\x12!\n\x1dPRESET_ICON_EASY_MAX_TIMEWARP\x10R\x12#\n\x1fPRESET_ICON_EASY_MAX_STAR_TRAIL\x10S\x12\'\n#PRESET_ICON_EASY_MAX_LIGHT_PAINTING\x10T\x12$\n PRESET_ICON_EASY_MAX_LIGHT_TRAIL\x10U\x12\x1e\n\x1aPRESET_ICON_MAX_STAR_TRAIL\x10Y\x12"\n\x1ePRESET_ICON_MAX_LIGHT_PAINTING\x10Z\x12\x1f\n\x1bPRESET_ICON_MAX_LIGHT_TRAIL\x10[\x12%\n!PRESET_ICON_EASY_STANDARD_PROFILE\x10d\x12 \n\x1cPRESET_ICON_EASY_HDR_PROFILE\x10e\x12\x1b\n\x17PRESET_ICON_BURST_SLOMO\x10f\x12 \n\x1bPRESET_ICON_TIMELAPSE_PHOTO\x10è\x07\x12!\n\x1cPRESET_ICON_NIGHTLAPSE_PHOTO\x10é\x07*·\x11\n\x0fEnumPresetTitle\x12\x19\n\x15PRESET_TITLE_ACTIVITY\x10\x00\x12\x19\n\x15PRESET_TITLE_STANDARD\x10\x01\x12\x1a\n\x16PRESET_TITLE_CINEMATIC\x10\x02\x12\x16\n\x12PRESET_TITLE_PHOTO\x10\x03\x12\x1b\n\x17PRESET_TITLE_LIVE_BURST\x10\x04\x12\x16\n\x12PRESET_TITLE_BURST\x10\x05\x12\x16\n\x12PRESET_TITLE_NIGHT\x10\x06\x12\x1a\n\x16PRESET_TITLE_TIME_WARP\x10\x07\x12\x1b\n\x17PRESET_TITLE_TIME_LAPSE\x10\x08\x12\x1c\n\x18PRESET_TITLE_NIGHT_LAPSE\x10\t\x12\x16\n\x12PRESET_TITLE_VIDEO\x10\n\x12\x16\n\x12PRESET_TITLE_SLOMO\x10\x0b\x12\x18\n\x14PRESET_TITLE_PHOTO_2\x10\r\x12\x19\n\x15PRESET_TITLE_PANORAMA\x10\x0e\x12\x1c\n\x18PRESET_TITLE_TIME_WARP_2\x10\x10\x12\x17\n\x13PRESET_TITLE_CUSTOM\x10\x12\x12\x14\n\x10PRESET_TITLE_AIR\x10\x13\x12\x15\n\x11PRESET_TITLE_BIKE\x10\x14\x12\x15\n\x11PRESET_TITLE_EPIC\x10\x15\x12\x17\n\x13PRESET_TITLE_INDOOR\x10\x16\x12\x16\n\x12PRESET_TITLE_MOTOR\x10\x17\x12\x18\n\x14PRESET_TITLE_MOUNTED\x10\x18\x12\x18\n\x14PRESET_TITLE_OUTDOOR\x10\x19\x12\x14\n\x10PRESET_TITLE_POV\x10\x1a\x12\x17\n\x13PRESET_TITLE_SELFIE\x10\x1b\x12\x16\n\x12PRESET_TITLE_SKATE\x10\x1c\x12\x15\n\x11PRESET_TITLE_SNOW\x10\x1d\x12\x16\n\x12PRESET_TITLE_TRAIL\x10\x1e\x12\x17\n\x13PRESET_TITLE_TRAVEL\x10\x1f\x12\x16\n\x12PRESET_TITLE_WATER\x10 \x12\x18\n\x14PRESET_TITLE_LOOPING\x10!\x12\x16\n\x12PRESET_TITLE_STARS\x10"\x12\x17\n\x13PRESET_TITLE_ACTION\x10#\x12\x1b\n\x17PRESET_TITLE_FOLLOW_CAM\x10$\x12\x15\n\x11PRESET_TITLE_SURF\x10%\x12\x15\n\x11PRESET_TITLE_CITY\x10&\x12\x16\n\x12PRESET_TITLE_SHAKY\x10\'\x12\x17\n\x13PRESET_TITLE_CHESTY\x10(\x12\x17\n\x13PRESET_TITLE_HELMET\x10)\x12\x15\n\x11PRESET_TITLE_BITE\x10*\x12!\n\x1dPRESET_TITLE_CUSTOM_CINEMATIC\x10+\x12\x15\n\x11PRESET_TITLE_VLOG\x10,\x12\x14\n\x10PRESET_TITLE_FPV\x10-\x12\x14\n\x10PRESET_TITLE_HDR\x10.\x12\x1a\n\x16PRESET_TITLE_LANDSCAPE\x10/\x12\x14\n\x10PRESET_TITLE_LOG\x100\x12\x1d\n\x19PRESET_TITLE_CUSTOM_SLOMO\x101\x12\x17\n\x13PRESET_TITLE_TRIPOD\x102\x12\x16\n\x12PRESET_TITLE_BASIC\x10:\x12\x1d\n\x19PRESET_TITLE_ULTRA_SLO_MO\x10;\x12#\n\x1fPRESET_TITLE_STANDARD_ENDURANCE\x10<\x12#\n\x1fPRESET_TITLE_ACTIVITY_ENDURANCE\x10=\x12$\n PRESET_TITLE_CINEMATIC_ENDURANCE\x10>\x12 \n\x1cPRESET_TITLE_SLOMO_ENDURANCE\x10?\x12\x1d\n\x19PRESET_TITLE_STATIONARY_1\x10@\x12\x1d\n\x19PRESET_TITLE_STATIONARY_2\x10A\x12\x1d\n\x19PRESET_TITLE_STATIONARY_3\x10B\x12\x1d\n\x19PRESET_TITLE_STATIONARY_4\x10C\x12\x1d\n\x19PRESET_TITLE_SIMPLE_VIDEO\x10D\x12!\n\x1dPRESET_TITLE_SIMPLE_TIME_WARP\x10E\x12#\n\x1fPRESET_TITLE_SIMPLE_SUPER_PHOTO\x10F\x12#\n\x1fPRESET_TITLE_SIMPLE_NIGHT_PHOTO\x10G\x12\'\n#PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE\x10H\x12 \n\x1cPRESET_TITLE_HIGHEST_QUALITY\x10I\x12!\n\x1dPRESET_TITLE_EXTENDED_BATTERY\x10J\x12 \n\x1cPRESET_TITLE_LONGEST_BATTERY\x10K\x12\x1b\n\x17PRESET_TITLE_STAR_TRAIL\x10L\x12\x1f\n\x1bPRESET_TITLE_LIGHT_PAINTING\x10M\x12\x1c\n\x18PRESET_TITLE_LIGHT_TRAIL\x10N\x12\x1b\n\x17PRESET_TITLE_FULL_FRAME\x10O\x12\'\n#PRESET_TITLE_STANDARD_QUALITY_VIDEO\x10R\x12$\n PRESET_TITLE_BASIC_QUALITY_VIDEO\x10S\x12&\n"PRESET_TITLE_HIGHEST_QUALITY_VIDEO\x10]\x12)\n%PRESET_TITLE_USER_DEFINED_CUSTOM_NAME\x10^\x12&\n"PRESET_TITLE_EASY_STANDARD_PROFILE\x10c\x12!\n\x1dPRESET_TITLE_EASY_HDR_PROFILE\x10d\x12\x1c\n\x18PRESET_TITLE_BURST_SLOMO\x10j'
    ),
    dependencies=[response__generic__pb2.DESCRIPTOR],
)
_ENUMFLATMODE = _descriptor.EnumDescriptor(
    name="EnumFlatMode",
    full_name="open_gopro.EnumFlatMode",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_UNKNOWN", index=0, number=(-1), serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_PLAYBACK", index=1, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(name="FLAT_MODE_SETUP", index=2, number=5, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(name="FLAT_MODE_VIDEO", index=3, number=12, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_TIME_LAPSE_VIDEO", index=4, number=13, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_LOOPING", index=5, number=15, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_PHOTO_SINGLE", index=6, number=16, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(name="FLAT_MODE_PHOTO", index=7, number=17, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_PHOTO_NIGHT", index=8, number=18, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_PHOTO_BURST", index=9, number=19, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_TIME_LAPSE_PHOTO", index=10, number=20, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_NIGHT_LAPSE_PHOTO", index=11, number=21, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_BROADCAST_RECORD", index=12, number=22, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_BROADCAST_BROADCAST", index=13, number=23, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_TIME_WARP_VIDEO", index=14, number=24, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_LIVE_BURST", index=15, number=25, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_NIGHT_LAPSE_VIDEO", index=16, number=26, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_SLOMO", index=17, number=27, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(name="FLAT_MODE_IDLE", index=18, number=28, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_VIDEO_STAR_TRAIL", index=19, number=29, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_VIDEO_LIGHT_PAINTING", index=20, number=30, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_VIDEO_LIGHT_TRAIL", index=21, number=31, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="FLAT_MODE_VIDEO_BURST_SLOMO", index=22, number=32, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=864,
    serialized_end=1531,
)
_sym_db.RegisterEnumDescriptor(_ENUMFLATMODE)
EnumFlatMode = enum_type_wrapper.EnumTypeWrapper(_ENUMFLATMODE)
_ENUMPRESETGROUP = _descriptor.EnumDescriptor(
    name="EnumPresetGroup",
    full_name="open_gopro.EnumPresetGroup",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_ID_VIDEO", index=0, number=1000, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_ID_PHOTO", index=1, number=1001, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_ID_TIMELAPSE", index=2, number=1002, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1533,
    serialized_end=1638,
)
_sym_db.RegisterEnumDescriptor(_ENUMPRESETGROUP)
EnumPresetGroup = enum_type_wrapper.EnumTypeWrapper(_ENUMPRESETGROUP)
_ENUMPRESETGROUPICON = _descriptor.EnumDescriptor(
    name="EnumPresetGroupIcon",
    full_name="open_gopro.EnumPresetGroupIcon",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_VIDEO_ICON_ID", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_PHOTO_ICON_ID", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_TIMELAPSE_ICON_ID", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_MAX_VIDEO_ICON_ID", index=5, number=5, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_MAX_PHOTO_ICON_ID", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_MAX_TIMELAPSE_ICON_ID", index=7, number=7, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_ND_MOD_VIDEO_ICON_ID", index=8, number=8, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_ND_MOD_PHOTO_ICON_ID", index=9, number=9, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID", index=10, number=10, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1641,
    serialized_end=2078,
)
_sym_db.RegisterEnumDescriptor(_ENUMPRESETGROUPICON)
EnumPresetGroupIcon = enum_type_wrapper.EnumTypeWrapper(_ENUMPRESETGROUPICON)
_ENUMPRESETICON = _descriptor.EnumDescriptor(
    name="EnumPresetIcon",
    full_name="open_gopro.EnumPresetIcon",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_VIDEO", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_ACTIVITY", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_CINEMATIC", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_PHOTO", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_LIVE_BURST", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_BURST", index=5, number=5, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_PHOTO_NIGHT", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_TIMEWARP", index=7, number=7, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_TIMELAPSE", index=8, number=8, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_NIGHTLAPSE", index=9, number=9, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SNAIL", index=10, number=10, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_VIDEO_2", index=11, number=11, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_PHOTO_2", index=12, number=13, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_PANORAMA", index=13, number=14, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_BURST_2", index=14, number=15, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_TIMEWARP_2", index=15, number=16, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_TIMELAPSE_2", index=16, number=17, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_CUSTOM", index=17, number=18, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_AIR", index=18, number=19, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_BIKE", index=19, number=20, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EPIC", index=20, number=21, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_INDOOR", index=21, number=22, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_MOTOR", index=22, number=23, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_MOUNTED", index=23, number=24, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_OUTDOOR", index=24, number=25, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_POV", index=25, number=26, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SELFIE", index=26, number=27, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SKATE", index=27, number=28, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SNOW", index=28, number=29, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_TRAIL", index=29, number=30, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_TRAVEL", index=30, number=31, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_WATER", index=31, number=32, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_LOOPING", index=32, number=33, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_STARS", index=33, number=34, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_ACTION", index=34, number=35, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_FOLLOW_CAM", index=35, number=36, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SURF", index=36, number=37, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_CITY", index=37, number=38, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SHAKY", index=38, number=39, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_CHESTY", index=39, number=40, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_HELMET", index=40, number=41, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_BITE", index=41, number=42, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_CUSTOM_CINEMATIC", index=42, number=43, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_VLOG", index=43, number=44, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_FPV", index=44, number=45, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_HDR", index=45, number=46, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_LANDSCAPE", index=46, number=47, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_LOG", index=47, number=48, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_CUSTOM_SLOMO", index=48, number=49, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_TRIPOD", index=49, number=50, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_MAX_VIDEO", index=50, number=55, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_MAX_PHOTO", index=51, number=56, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_MAX_TIMEWARP", index=52, number=57, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_BASIC", index=53, number=58, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_ULTRA_SLO_MO", index=54, number=59, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_STANDARD_ENDURANCE", index=55, number=60, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_ACTIVITY_ENDURANCE", index=56, number=61, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_CINEMATIC_ENDURANCE", index=57, number=62, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SLOMO_ENDURANCE", index=58, number=63, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_STATIONARY_1", index=59, number=64, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_STATIONARY_2", index=60, number=65, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_STATIONARY_3", index=61, number=66, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_STATIONARY_4", index=62, number=67, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SIMPLE_SUPER_PHOTO", index=63, number=70, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_SIMPLE_NIGHT_PHOTO", index=64, number=71, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_HIGHEST_QUALITY_VIDEO", index=65, number=73, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_STANDARD_QUALITY_VIDEO", index=66, number=74, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_BASIC_QUALITY_VIDEO", index=67, number=75, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_STAR_TRAIL", index=68, number=76, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_LIGHT_PAINTING", index=69, number=77, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_LIGHT_TRAIL", index=70, number=78, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_FULL_FRAME", index=71, number=79, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EASY_MAX_VIDEO", index=72, number=80, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EASY_MAX_PHOTO", index=73, number=81, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EASY_MAX_TIMEWARP", index=74, number=82, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EASY_MAX_STAR_TRAIL", index=75, number=83, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EASY_MAX_LIGHT_PAINTING", index=76, number=84, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EASY_MAX_LIGHT_TRAIL", index=77, number=85, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_MAX_STAR_TRAIL", index=78, number=89, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_MAX_LIGHT_PAINTING", index=79, number=90, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_MAX_LIGHT_TRAIL", index=80, number=91, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EASY_STANDARD_PROFILE", index=81, number=100, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_EASY_HDR_PROFILE", index=82, number=101, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_BURST_SLOMO", index=83, number=102, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_TIMELAPSE_PHOTO", index=84, number=1000, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_ICON_NIGHTLAPSE_PHOTO", index=85, number=1001, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=2081,
    serialized_end=4512,
)
_sym_db.RegisterEnumDescriptor(_ENUMPRESETICON)
EnumPresetIcon = enum_type_wrapper.EnumTypeWrapper(_ENUMPRESETICON)
_ENUMPRESETTITLE = _descriptor.EnumDescriptor(
    name="EnumPresetTitle",
    full_name="open_gopro.EnumPresetTitle",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_ACTIVITY", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STANDARD", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_CINEMATIC", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_PHOTO", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_LIVE_BURST", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_BURST", index=5, number=5, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_NIGHT", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_TIME_WARP", index=7, number=7, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_TIME_LAPSE", index=8, number=8, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_NIGHT_LAPSE", index=9, number=9, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_VIDEO", index=10, number=10, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SLOMO", index=11, number=11, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_PHOTO_2", index=12, number=13, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_PANORAMA", index=13, number=14, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_TIME_WARP_2", index=14, number=16, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_CUSTOM", index=15, number=18, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_AIR", index=16, number=19, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_BIKE", index=17, number=20, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_EPIC", index=18, number=21, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_INDOOR", index=19, number=22, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_MOTOR", index=20, number=23, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_MOUNTED", index=21, number=24, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_OUTDOOR", index=22, number=25, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_POV", index=23, number=26, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SELFIE", index=24, number=27, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SKATE", index=25, number=28, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SNOW", index=26, number=29, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_TRAIL", index=27, number=30, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_TRAVEL", index=28, number=31, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_WATER", index=29, number=32, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_LOOPING", index=30, number=33, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STARS", index=31, number=34, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_ACTION", index=32, number=35, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_FOLLOW_CAM", index=33, number=36, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SURF", index=34, number=37, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_CITY", index=35, number=38, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SHAKY", index=36, number=39, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_CHESTY", index=37, number=40, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_HELMET", index=38, number=41, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_BITE", index=39, number=42, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_CUSTOM_CINEMATIC", index=40, number=43, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_VLOG", index=41, number=44, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_FPV", index=42, number=45, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_HDR", index=43, number=46, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_LANDSCAPE", index=44, number=47, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_LOG", index=45, number=48, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_CUSTOM_SLOMO", index=46, number=49, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_TRIPOD", index=47, number=50, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_BASIC", index=48, number=58, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_ULTRA_SLO_MO", index=49, number=59, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STANDARD_ENDURANCE", index=50, number=60, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_ACTIVITY_ENDURANCE", index=51, number=61, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_CINEMATIC_ENDURANCE", index=52, number=62, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SLOMO_ENDURANCE", index=53, number=63, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STATIONARY_1", index=54, number=64, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STATIONARY_2", index=55, number=65, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STATIONARY_3", index=56, number=66, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STATIONARY_4", index=57, number=67, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SIMPLE_VIDEO", index=58, number=68, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SIMPLE_TIME_WARP", index=59, number=69, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SIMPLE_SUPER_PHOTO", index=60, number=70, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SIMPLE_NIGHT_PHOTO", index=61, number=71, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE", index=62, number=72, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_HIGHEST_QUALITY", index=63, number=73, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_EXTENDED_BATTERY", index=64, number=74, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_LONGEST_BATTERY", index=65, number=75, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STAR_TRAIL", index=66, number=76, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_LIGHT_PAINTING", index=67, number=77, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_LIGHT_TRAIL", index=68, number=78, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_FULL_FRAME", index=69, number=79, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_STANDARD_QUALITY_VIDEO", index=70, number=82, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_BASIC_QUALITY_VIDEO", index=71, number=83, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_HIGHEST_QUALITY_VIDEO", index=72, number=93, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_USER_DEFINED_CUSTOM_NAME", index=73, number=94, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_EASY_STANDARD_PROFILE", index=74, number=99, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_EASY_HDR_PROFILE", index=75, number=100, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PRESET_TITLE_BURST_SLOMO", index=76, number=106, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=4515,
    serialized_end=6746,
)
_sym_db.RegisterEnumDescriptor(_ENUMPRESETTITLE)
EnumPresetTitle = enum_type_wrapper.EnumTypeWrapper(_ENUMPRESETTITLE)
FLAT_MODE_UNKNOWN = -1
FLAT_MODE_PLAYBACK = 4
FLAT_MODE_SETUP = 5
FLAT_MODE_VIDEO = 12
FLAT_MODE_TIME_LAPSE_VIDEO = 13
FLAT_MODE_LOOPING = 15
FLAT_MODE_PHOTO_SINGLE = 16
FLAT_MODE_PHOTO = 17
FLAT_MODE_PHOTO_NIGHT = 18
FLAT_MODE_PHOTO_BURST = 19
FLAT_MODE_TIME_LAPSE_PHOTO = 20
FLAT_MODE_NIGHT_LAPSE_PHOTO = 21
FLAT_MODE_BROADCAST_RECORD = 22
FLAT_MODE_BROADCAST_BROADCAST = 23
FLAT_MODE_TIME_WARP_VIDEO = 24
FLAT_MODE_LIVE_BURST = 25
FLAT_MODE_NIGHT_LAPSE_VIDEO = 26
FLAT_MODE_SLOMO = 27
FLAT_MODE_IDLE = 28
FLAT_MODE_VIDEO_STAR_TRAIL = 29
FLAT_MODE_VIDEO_LIGHT_PAINTING = 30
FLAT_MODE_VIDEO_LIGHT_TRAIL = 31
FLAT_MODE_VIDEO_BURST_SLOMO = 32
PRESET_GROUP_ID_VIDEO = 1000
PRESET_GROUP_ID_PHOTO = 1001
PRESET_GROUP_ID_TIMELAPSE = 1002
PRESET_GROUP_VIDEO_ICON_ID = 0
PRESET_GROUP_PHOTO_ICON_ID = 1
PRESET_GROUP_TIMELAPSE_ICON_ID = 2
PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID = 3
PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID = 4
PRESET_GROUP_MAX_VIDEO_ICON_ID = 5
PRESET_GROUP_MAX_PHOTO_ICON_ID = 6
PRESET_GROUP_MAX_TIMELAPSE_ICON_ID = 7
PRESET_GROUP_ND_MOD_VIDEO_ICON_ID = 8
PRESET_GROUP_ND_MOD_PHOTO_ICON_ID = 9
PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID = 10
PRESET_ICON_VIDEO = 0
PRESET_ICON_ACTIVITY = 1
PRESET_ICON_CINEMATIC = 2
PRESET_ICON_PHOTO = 3
PRESET_ICON_LIVE_BURST = 4
PRESET_ICON_BURST = 5
PRESET_ICON_PHOTO_NIGHT = 6
PRESET_ICON_TIMEWARP = 7
PRESET_ICON_TIMELAPSE = 8
PRESET_ICON_NIGHTLAPSE = 9
PRESET_ICON_SNAIL = 10
PRESET_ICON_VIDEO_2 = 11
PRESET_ICON_PHOTO_2 = 13
PRESET_ICON_PANORAMA = 14
PRESET_ICON_BURST_2 = 15
PRESET_ICON_TIMEWARP_2 = 16
PRESET_ICON_TIMELAPSE_2 = 17
PRESET_ICON_CUSTOM = 18
PRESET_ICON_AIR = 19
PRESET_ICON_BIKE = 20
PRESET_ICON_EPIC = 21
PRESET_ICON_INDOOR = 22
PRESET_ICON_MOTOR = 23
PRESET_ICON_MOUNTED = 24
PRESET_ICON_OUTDOOR = 25
PRESET_ICON_POV = 26
PRESET_ICON_SELFIE = 27
PRESET_ICON_SKATE = 28
PRESET_ICON_SNOW = 29
PRESET_ICON_TRAIL = 30
PRESET_ICON_TRAVEL = 31
PRESET_ICON_WATER = 32
PRESET_ICON_LOOPING = 33
PRESET_ICON_STARS = 34
PRESET_ICON_ACTION = 35
PRESET_ICON_FOLLOW_CAM = 36
PRESET_ICON_SURF = 37
PRESET_ICON_CITY = 38
PRESET_ICON_SHAKY = 39
PRESET_ICON_CHESTY = 40
PRESET_ICON_HELMET = 41
PRESET_ICON_BITE = 42
PRESET_ICON_CUSTOM_CINEMATIC = 43
PRESET_ICON_VLOG = 44
PRESET_ICON_FPV = 45
PRESET_ICON_HDR = 46
PRESET_ICON_LANDSCAPE = 47
PRESET_ICON_LOG = 48
PRESET_ICON_CUSTOM_SLOMO = 49
PRESET_ICON_TRIPOD = 50
PRESET_ICON_MAX_VIDEO = 55
PRESET_ICON_MAX_PHOTO = 56
PRESET_ICON_MAX_TIMEWARP = 57
PRESET_ICON_BASIC = 58
PRESET_ICON_ULTRA_SLO_MO = 59
PRESET_ICON_STANDARD_ENDURANCE = 60
PRESET_ICON_ACTIVITY_ENDURANCE = 61
PRESET_ICON_CINEMATIC_ENDURANCE = 62
PRESET_ICON_SLOMO_ENDURANCE = 63
PRESET_ICON_STATIONARY_1 = 64
PRESET_ICON_STATIONARY_2 = 65
PRESET_ICON_STATIONARY_3 = 66
PRESET_ICON_STATIONARY_4 = 67
PRESET_ICON_SIMPLE_SUPER_PHOTO = 70
PRESET_ICON_SIMPLE_NIGHT_PHOTO = 71
PRESET_ICON_HIGHEST_QUALITY_VIDEO = 73
PRESET_ICON_STANDARD_QUALITY_VIDEO = 74
PRESET_ICON_BASIC_QUALITY_VIDEO = 75
PRESET_ICON_STAR_TRAIL = 76
PRESET_ICON_LIGHT_PAINTING = 77
PRESET_ICON_LIGHT_TRAIL = 78
PRESET_ICON_FULL_FRAME = 79
PRESET_ICON_EASY_MAX_VIDEO = 80
PRESET_ICON_EASY_MAX_PHOTO = 81
PRESET_ICON_EASY_MAX_TIMEWARP = 82
PRESET_ICON_EASY_MAX_STAR_TRAIL = 83
PRESET_ICON_EASY_MAX_LIGHT_PAINTING = 84
PRESET_ICON_EASY_MAX_LIGHT_TRAIL = 85
PRESET_ICON_MAX_STAR_TRAIL = 89
PRESET_ICON_MAX_LIGHT_PAINTING = 90
PRESET_ICON_MAX_LIGHT_TRAIL = 91
PRESET_ICON_EASY_STANDARD_PROFILE = 100
PRESET_ICON_EASY_HDR_PROFILE = 101
PRESET_ICON_BURST_SLOMO = 102
PRESET_ICON_TIMELAPSE_PHOTO = 1000
PRESET_ICON_NIGHTLAPSE_PHOTO = 1001
PRESET_TITLE_ACTIVITY = 0
PRESET_TITLE_STANDARD = 1
PRESET_TITLE_CINEMATIC = 2
PRESET_TITLE_PHOTO = 3
PRESET_TITLE_LIVE_BURST = 4
PRESET_TITLE_BURST = 5
PRESET_TITLE_NIGHT = 6
PRESET_TITLE_TIME_WARP = 7
PRESET_TITLE_TIME_LAPSE = 8
PRESET_TITLE_NIGHT_LAPSE = 9
PRESET_TITLE_VIDEO = 10
PRESET_TITLE_SLOMO = 11
PRESET_TITLE_PHOTO_2 = 13
PRESET_TITLE_PANORAMA = 14
PRESET_TITLE_TIME_WARP_2 = 16
PRESET_TITLE_CUSTOM = 18
PRESET_TITLE_AIR = 19
PRESET_TITLE_BIKE = 20
PRESET_TITLE_EPIC = 21
PRESET_TITLE_INDOOR = 22
PRESET_TITLE_MOTOR = 23
PRESET_TITLE_MOUNTED = 24
PRESET_TITLE_OUTDOOR = 25
PRESET_TITLE_POV = 26
PRESET_TITLE_SELFIE = 27
PRESET_TITLE_SKATE = 28
PRESET_TITLE_SNOW = 29
PRESET_TITLE_TRAIL = 30
PRESET_TITLE_TRAVEL = 31
PRESET_TITLE_WATER = 32
PRESET_TITLE_LOOPING = 33
PRESET_TITLE_STARS = 34
PRESET_TITLE_ACTION = 35
PRESET_TITLE_FOLLOW_CAM = 36
PRESET_TITLE_SURF = 37
PRESET_TITLE_CITY = 38
PRESET_TITLE_SHAKY = 39
PRESET_TITLE_CHESTY = 40
PRESET_TITLE_HELMET = 41
PRESET_TITLE_BITE = 42
PRESET_TITLE_CUSTOM_CINEMATIC = 43
PRESET_TITLE_VLOG = 44
PRESET_TITLE_FPV = 45
PRESET_TITLE_HDR = 46
PRESET_TITLE_LANDSCAPE = 47
PRESET_TITLE_LOG = 48
PRESET_TITLE_CUSTOM_SLOMO = 49
PRESET_TITLE_TRIPOD = 50
PRESET_TITLE_BASIC = 58
PRESET_TITLE_ULTRA_SLO_MO = 59
PRESET_TITLE_STANDARD_ENDURANCE = 60
PRESET_TITLE_ACTIVITY_ENDURANCE = 61
PRESET_TITLE_CINEMATIC_ENDURANCE = 62
PRESET_TITLE_SLOMO_ENDURANCE = 63
PRESET_TITLE_STATIONARY_1 = 64
PRESET_TITLE_STATIONARY_2 = 65
PRESET_TITLE_STATIONARY_3 = 66
PRESET_TITLE_STATIONARY_4 = 67
PRESET_TITLE_SIMPLE_VIDEO = 68
PRESET_TITLE_SIMPLE_TIME_WARP = 69
PRESET_TITLE_SIMPLE_SUPER_PHOTO = 70
PRESET_TITLE_SIMPLE_NIGHT_PHOTO = 71
PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE = 72
PRESET_TITLE_HIGHEST_QUALITY = 73
PRESET_TITLE_EXTENDED_BATTERY = 74
PRESET_TITLE_LONGEST_BATTERY = 75
PRESET_TITLE_STAR_TRAIL = 76
PRESET_TITLE_LIGHT_PAINTING = 77
PRESET_TITLE_LIGHT_TRAIL = 78
PRESET_TITLE_FULL_FRAME = 79
PRESET_TITLE_STANDARD_QUALITY_VIDEO = 82
PRESET_TITLE_BASIC_QUALITY_VIDEO = 83
PRESET_TITLE_HIGHEST_QUALITY_VIDEO = 93
PRESET_TITLE_USER_DEFINED_CUSTOM_NAME = 94
PRESET_TITLE_EASY_STANDARD_PROFILE = 99
PRESET_TITLE_EASY_HDR_PROFILE = 100
PRESET_TITLE_BURST_SLOMO = 106
_NOTIFYPRESETSTATUS = _descriptor.Descriptor(
    name="NotifyPresetStatus",
    full_name="open_gopro.NotifyPresetStatus",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="preset_group_array",
            full_name="open_gopro.NotifyPresetStatus.preset_group_array",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=59,
    serialized_end=132,
)
_PRESET = _descriptor.Descriptor(
    name="Preset",
    full_name="open_gopro.Preset",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="open_gopro.Preset.id",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="mode",
            full_name="open_gopro.Preset.mode",
            index=1,
            number=2,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=(-1),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="title_id",
            full_name="open_gopro.Preset.title_id",
            index=2,
            number=3,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="title_number",
            full_name="open_gopro.Preset.title_number",
            index=3,
            number=4,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="user_defined",
            full_name="open_gopro.Preset.user_defined",
            index=4,
            number=5,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="icon",
            full_name="open_gopro.Preset.icon",
            index=5,
            number=6,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="setting_array",
            full_name="open_gopro.Preset.setting_array",
            index=6,
            number=7,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="is_modified",
            full_name="open_gopro.Preset.is_modified",
            index=7,
            number=8,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="is_fixed",
            full_name="open_gopro.Preset.is_fixed",
            index=8,
            number=9,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="custom_name",
            full_name="open_gopro.Preset.custom_name",
            index=9,
            number=10,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=135,
    serialized_end=438,
)
_REQUESTCUSTOMPRESETUPDATE = _descriptor.Descriptor(
    name="RequestCustomPresetUpdate",
    full_name="open_gopro.RequestCustomPresetUpdate",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="title_id",
            full_name="open_gopro.RequestCustomPresetUpdate.title_id",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="custom_name",
            full_name="open_gopro.RequestCustomPresetUpdate.custom_name",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="icon_id",
            full_name="open_gopro.RequestCustomPresetUpdate.icon_id",
            index=2,
            number=3,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=441,
    serialized_end=581,
)
_PRESETGROUP = _descriptor.Descriptor(
    name="PresetGroup",
    full_name="open_gopro.PresetGroup",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="open_gopro.PresetGroup.id",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=1000,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="preset_array",
            full_name="open_gopro.PresetGroup.preset_array",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="can_add_preset",
            full_name="open_gopro.PresetGroup.can_add_preset",
            index=2,
            number=3,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="icon",
            full_name="open_gopro.PresetGroup.icon",
            index=3,
            number=4,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="mode_array",
            full_name="open_gopro.PresetGroup.mode_array",
            index=4,
            number=5,
            type=14,
            cpp_type=8,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=584,
    serialized_end=797,
)
_PRESETSETTING = _descriptor.Descriptor(
    name="PresetSetting",
    full_name="open_gopro.PresetSetting",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="open_gopro.PresetSetting.id",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="open_gopro.PresetSetting.value",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="is_caption",
            full_name="open_gopro.PresetSetting.is_caption",
            index=2,
            number=3,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=799,
    serialized_end=861,
)
_NOTIFYPRESETSTATUS.fields_by_name["preset_group_array"].message_type = _PRESETGROUP
_PRESET.fields_by_name["mode"].enum_type = _ENUMFLATMODE
_PRESET.fields_by_name["title_id"].enum_type = _ENUMPRESETTITLE
_PRESET.fields_by_name["icon"].enum_type = _ENUMPRESETICON
_PRESET.fields_by_name["setting_array"].message_type = _PRESETSETTING
_REQUESTCUSTOMPRESETUPDATE.fields_by_name["title_id"].enum_type = _ENUMPRESETTITLE
_REQUESTCUSTOMPRESETUPDATE.fields_by_name["icon_id"].enum_type = _ENUMPRESETICON
_PRESETGROUP.fields_by_name["id"].enum_type = _ENUMPRESETGROUP
_PRESETGROUP.fields_by_name["preset_array"].message_type = _PRESET
_PRESETGROUP.fields_by_name["icon"].enum_type = _ENUMPRESETGROUPICON
_PRESETGROUP.fields_by_name["mode_array"].enum_type = _ENUMFLATMODE
DESCRIPTOR.message_types_by_name["NotifyPresetStatus"] = _NOTIFYPRESETSTATUS
DESCRIPTOR.message_types_by_name["Preset"] = _PRESET
DESCRIPTOR.message_types_by_name["RequestCustomPresetUpdate"] = _REQUESTCUSTOMPRESETUPDATE
DESCRIPTOR.message_types_by_name["PresetGroup"] = _PRESETGROUP
DESCRIPTOR.message_types_by_name["PresetSetting"] = _PRESETSETTING
DESCRIPTOR.enum_types_by_name["EnumFlatMode"] = _ENUMFLATMODE
DESCRIPTOR.enum_types_by_name["EnumPresetGroup"] = _ENUMPRESETGROUP
DESCRIPTOR.enum_types_by_name["EnumPresetGroupIcon"] = _ENUMPRESETGROUPICON
DESCRIPTOR.enum_types_by_name["EnumPresetIcon"] = _ENUMPRESETICON
DESCRIPTOR.enum_types_by_name["EnumPresetTitle"] = _ENUMPRESETTITLE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
NotifyPresetStatus = _reflection.GeneratedProtocolMessageType(
    "NotifyPresetStatus", (_message.Message,), dict(DESCRIPTOR=_NOTIFYPRESETSTATUS, __module__="preset_status_pb2")
)
_sym_db.RegisterMessage(NotifyPresetStatus)
Preset = _reflection.GeneratedProtocolMessageType(
    "Preset", (_message.Message,), dict(DESCRIPTOR=_PRESET, __module__="preset_status_pb2")
)
_sym_db.RegisterMessage(Preset)
RequestCustomPresetUpdate = _reflection.GeneratedProtocolMessageType(
    "RequestCustomPresetUpdate",
    (_message.Message,),
    dict(DESCRIPTOR=_REQUESTCUSTOMPRESETUPDATE, __module__="preset_status_pb2"),
)
_sym_db.RegisterMessage(RequestCustomPresetUpdate)
PresetGroup = _reflection.GeneratedProtocolMessageType(
    "PresetGroup", (_message.Message,), dict(DESCRIPTOR=_PRESETGROUP, __module__="preset_status_pb2")
)
_sym_db.RegisterMessage(PresetGroup)
PresetSetting = _reflection.GeneratedProtocolMessageType(
    "PresetSetting", (_message.Message,), dict(DESCRIPTOR=_PRESETSETTING, __module__="preset_status_pb2")
)
_sym_db.RegisterMessage(PresetSetting)
