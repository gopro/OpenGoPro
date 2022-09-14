# preset_status_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Sep 14 15:22:28 UTC 2022

"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13preset_status.proto\x12\nopen_gopro"I\n\x12NotifyPresetStatus\x123\n\x12preset_group_array\x18\x01 \x03(\x0b2\x17.open_gopro.PresetGroup"\x9a\x02\n\x06Preset\x12\n\n\x02id\x18\x01 \x01(\x05\x12&\n\x04mode\x18\x02 \x01(\x0e2\x18.open_gopro.EnumFlatMode\x12-\n\x08title_id\x18\x03 \x01(\x0e2\x1b.open_gopro.EnumPresetTitle\x12\x14\n\x0ctitle_number\x18\x04 \x01(\x05\x12\x14\n\x0cuser_defined\x18\x05 \x01(\x08\x12(\n\x04icon\x18\x06 \x01(\x0e2\x1a.open_gopro.EnumPresetIcon\x120\n\rsetting_array\x18\x07 \x03(\x0b2\x19.open_gopro.PresetSetting\x12\x13\n\x0bis_modified\x18\x08 \x01(\x08\x12\x10\n\x08is_fixed\x18\t \x01(\x08"x\n\x0bPresetGroup\x12\'\n\x02id\x18\x01 \x01(\x0e2\x1b.open_gopro.EnumPresetGroup\x12(\n\x0cpreset_array\x18\x02 \x03(\x0b2\x12.open_gopro.Preset\x12\x16\n\x0ecan_add_preset\x18\x03 \x01(\x08">\n\rPresetSetting\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05\x12\x12\n\nis_caption\x18\x03 \x01(\x08*\xfa\x04\n\x0cEnumFlatMode\x12\x1e\n\x11FLAT_MODE_UNKNOWN\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x16\n\x12FLAT_MODE_PLAYBACK\x10\x04\x12\x13\n\x0fFLAT_MODE_SETUP\x10\x05\x12\x13\n\x0fFLAT_MODE_VIDEO\x10\x0c\x12\x1e\n\x1aFLAT_MODE_TIME_LAPSE_VIDEO\x10\r\x12\x15\n\x11FLAT_MODE_LOOPING\x10\x0f\x12\x1a\n\x16FLAT_MODE_PHOTO_SINGLE\x10\x10\x12\x13\n\x0fFLAT_MODE_PHOTO\x10\x11\x12\x19\n\x15FLAT_MODE_PHOTO_NIGHT\x10\x12\x12\x19\n\x15FLAT_MODE_PHOTO_BURST\x10\x13\x12\x1e\n\x1aFLAT_MODE_TIME_LAPSE_PHOTO\x10\x14\x12\x1f\n\x1bFLAT_MODE_NIGHT_LAPSE_PHOTO\x10\x15\x12\x1e\n\x1aFLAT_MODE_BROADCAST_RECORD\x10\x16\x12!\n\x1dFLAT_MODE_BROADCAST_BROADCAST\x10\x17\x12\x1d\n\x19FLAT_MODE_TIME_WARP_VIDEO\x10\x18\x12\x18\n\x14FLAT_MODE_LIVE_BURST\x10\x19\x12\x1f\n\x1bFLAT_MODE_NIGHT_LAPSE_VIDEO\x10\x1a\x12\x13\n\x0fFLAT_MODE_SLOMO\x10\x1b\x12\x12\n\x0eFLAT_MODE_IDLE\x10\x1c\x12\x1e\n\x1aFLAT_MODE_VIDEO_STAR_TRAIL\x10\x1d\x12"\n\x1eFLAT_MODE_VIDEO_LIGHT_PAINTING\x10\x1e\x12\x1f\n\x1bFLAT_MODE_VIDEO_LIGHT_TRAIL\x10\x1f*\xfd\x01\n\x0fEnumPresetGroup\x12\x1a\n\x15PRESET_GROUP_ID_VIDEO\x10\xe8\x07\x12\x1a\n\x15PRESET_GROUP_ID_PHOTO\x10\xe9\x07\x12\x1e\n\x19PRESET_GROUP_ID_TIMELAPSE\x10\xea\x07\x12$\n\x1fPRESET_GROUP_ID_VIDEO_DUAL_LENS\x10\xeb\x07\x12$\n\x1fPRESET_GROUP_ID_PHOTO_DUAL_LENS\x10\xec\x07\x12(\n#PRESET_GROUP_ID_TIMELAPSE_DUAL_LENS\x10\xed\x07\x12\x1c\n\x17PRESET_GROUP_ID_SPECIAL\x10\xee\x07*\xa0\x0b\n\x0eEnumPresetIcon\x12\x15\n\x11PRESET_ICON_VIDEO\x10\x00\x12\x18\n\x14PRESET_ICON_ACTIVITY\x10\x01\x12\x19\n\x15PRESET_ICON_CINEMATIC\x10\x02\x12\x15\n\x11PRESET_ICON_PHOTO\x10\x03\x12\x1a\n\x16PRESET_ICON_LIVE_BURST\x10\x04\x12\x15\n\x11PRESET_ICON_BURST\x10\x05\x12\x1b\n\x17PRESET_ICON_PHOTO_NIGHT\x10\x06\x12\x18\n\x14PRESET_ICON_TIMEWARP\x10\x07\x12\x19\n\x15PRESET_ICON_TIMELAPSE\x10\x08\x12\x1a\n\x16PRESET_ICON_NIGHTLAPSE\x10\t\x12\x15\n\x11PRESET_ICON_SNAIL\x10\n\x12\x17\n\x13PRESET_ICON_VIDEO_2\x10\x0b\x12\x19\n\x15PRESET_ICON_360_VIDEO\x10\x0c\x12\x17\n\x13PRESET_ICON_PHOTO_2\x10\r\x12\x18\n\x14PRESET_ICON_PANORAMA\x10\x0e\x12\x17\n\x13PRESET_ICON_BURST_2\x10\x0f\x12\x1a\n\x16PRESET_ICON_TIMEWARP_2\x10\x10\x12\x1b\n\x17PRESET_ICON_TIMELAPSE_2\x10\x11\x12\x16\n\x12PRESET_ICON_CUSTOM\x10\x12\x12\x13\n\x0fPRESET_ICON_AIR\x10\x13\x12\x14\n\x10PRESET_ICON_BIKE\x10\x14\x12\x14\n\x10PRESET_ICON_EPIC\x10\x15\x12\x16\n\x12PRESET_ICON_INDOOR\x10\x16\x12\x15\n\x11PRESET_ICON_MOTOR\x10\x17\x12\x17\n\x13PRESET_ICON_MOUNTED\x10\x18\x12\x17\n\x13PRESET_ICON_OUTDOOR\x10\x19\x12\x13\n\x0fPRESET_ICON_POV\x10\x1a\x12\x16\n\x12PRESET_ICON_SELFIE\x10\x1b\x12\x15\n\x11PRESET_ICON_SKATE\x10\x1c\x12\x14\n\x10PRESET_ICON_SNOW\x10\x1d\x12\x15\n\x11PRESET_ICON_TRAIL\x10\x1e\x12\x16\n\x12PRESET_ICON_TRAVEL\x10\x1f\x12\x15\n\x11PRESET_ICON_WATER\x10 \x12\x17\n\x13PRESET_ICON_LOOPING\x10!\x12\x19\n\x15PRESET_ICON_MAX_VIDEO\x107\x12\x19\n\x15PRESET_ICON_MAX_PHOTO\x108\x12\x1c\n\x18PRESET_ICON_MAX_TIMEWARP\x109\x12\x15\n\x11PRESET_ICON_BASIC\x10:\x12\x1c\n\x18PRESET_ICON_ULTRA_SLO_MO\x10;\x12"\n\x1ePRESET_ICON_STANDARD_ENDURANCE\x10<\x12"\n\x1ePRESET_ICON_ACTIVITY_ENDURANCE\x10=\x12#\n\x1fPRESET_ICON_CINEMATIC_ENDURANCE\x10>\x12\x1f\n\x1bPRESET_ICON_SLOMO_ENDURANCE\x10?\x12\x1c\n\x18PRESET_ICON_STATIONARY_1\x10@\x12\x1c\n\x18PRESET_ICON_STATIONARY_2\x10A\x12\x1c\n\x18PRESET_ICON_STATIONARY_3\x10B\x12\x1c\n\x18PRESET_ICON_STATIONARY_4\x10C\x12\x1a\n\x16PRESET_ICON_STAR_TRAIL\x10L\x12\x1e\n\x1aPRESET_ICON_LIGHT_PAINTING\x10M\x12\x1b\n\x17PRESET_ICON_LIGHT_TRAIL\x10N\x12\x1a\n\x16PRESET_ICON_FULL_FRAME\x10O\x12 \n\x1bPRESET_ICON_TIMELAPSE_PHOTO\x10\xe8\x07\x12!\n\x1cPRESET_ICON_NIGHTLAPSE_PHOTO\x10\xe9\x07*\xcd\r\n\x0fEnumPresetTitle\x12\x19\n\x15PRESET_TITLE_ACTIVITY\x10\x00\x12\x19\n\x15PRESET_TITLE_STANDARD\x10\x01\x12\x1a\n\x16PRESET_TITLE_CINEMATIC\x10\x02\x12\x16\n\x12PRESET_TITLE_PHOTO\x10\x03\x12\x1b\n\x17PRESET_TITLE_LIVE_BURST\x10\x04\x12\x16\n\x12PRESET_TITLE_BURST\x10\x05\x12\x16\n\x12PRESET_TITLE_NIGHT\x10\x06\x12\x1a\n\x16PRESET_TITLE_TIME_WARP\x10\x07\x12\x1b\n\x17PRESET_TITLE_TIME_LAPSE\x10\x08\x12\x1c\n\x18PRESET_TITLE_NIGHT_LAPSE\x10\t\x12\x16\n\x12PRESET_TITLE_VIDEO\x10\n\x12\x16\n\x12PRESET_TITLE_SLOMO\x10\x0b\x12\x1a\n\x16PRESET_TITLE_360_VIDEO\x10\x0c\x12\x18\n\x14PRESET_TITLE_PHOTO_2\x10\r\x12\x19\n\x15PRESET_TITLE_PANORAMA\x10\x0e\x12\x1a\n\x16PRESET_TITLE_360_PHOTO\x10\x0f\x12\x1c\n\x18PRESET_TITLE_TIME_WARP_2\x10\x10\x12\x1e\n\x1aPRESET_TITLE_360_TIME_WARP\x10\x11\x12\x17\n\x13PRESET_TITLE_CUSTOM\x10\x12\x12\x14\n\x10PRESET_TITLE_AIR\x10\x13\x12\x15\n\x11PRESET_TITLE_BIKE\x10\x14\x12\x15\n\x11PRESET_TITLE_EPIC\x10\x15\x12\x17\n\x13PRESET_TITLE_INDOOR\x10\x16\x12\x16\n\x12PRESET_TITLE_MOTOR\x10\x17\x12\x18\n\x14PRESET_TITLE_MOUNTED\x10\x18\x12\x18\n\x14PRESET_TITLE_OUTDOOR\x10\x19\x12\x14\n\x10PRESET_TITLE_POV\x10\x1a\x12\x17\n\x13PRESET_TITLE_SELFIE\x10\x1b\x12\x16\n\x12PRESET_TITLE_SKATE\x10\x1c\x12\x15\n\x11PRESET_TITLE_SNOW\x10\x1d\x12\x16\n\x12PRESET_TITLE_TRAIL\x10\x1e\x12\x17\n\x13PRESET_TITLE_TRAVEL\x10\x1f\x12\x16\n\x12PRESET_TITLE_WATER\x10 \x12\x18\n\x14PRESET_TITLE_LOOPING\x10!\x12\x1e\n\x1aPRESET_TITLE_360_TIMELAPSE\x103\x12 \n\x1cPRESET_TITLE_360_NIGHT_LAPSE\x104\x12 \n\x1cPRESET_TITLE_360_NIGHT_PHOTO\x105\x12 \n\x1cPRESET_TITLE_PANO_TIME_LAPSE\x106\x12\x1a\n\x16PRESET_TITLE_MAX_VIDEO\x107\x12\x1a\n\x16PRESET_TITLE_MAX_PHOTO\x108\x12\x1d\n\x19PRESET_TITLE_MAX_TIMEWARP\x109\x12\x16\n\x12PRESET_TITLE_BASIC\x10:\x12\x1d\n\x19PRESET_TITLE_ULTRA_SLO_MO\x10;\x12#\n\x1fPRESET_TITLE_STANDARD_ENDURANCE\x10<\x12#\n\x1fPRESET_TITLE_ACTIVITY_ENDURANCE\x10=\x12$\n PRESET_TITLE_CINEMATIC_ENDURANCE\x10>\x12 \n\x1cPRESET_TITLE_SLOMO_ENDURANCE\x10?\x12\x1d\n\x19PRESET_TITLE_STATIONARY_1\x10@\x12\x1d\n\x19PRESET_TITLE_STATIONARY_2\x10A\x12\x1d\n\x19PRESET_TITLE_STATIONARY_3\x10B\x12\x1d\n\x19PRESET_TITLE_STATIONARY_4\x10C\x12\x1d\n\x19PRESET_TITLE_SIMPLE_VIDEO\x10D\x12!\n\x1dPRESET_TITLE_SIMPLE_TIME_WARP\x10E\x12#\n\x1fPRESET_TITLE_SIMPLE_SUPER_PHOTO\x10F\x12#\n\x1fPRESET_TITLE_SIMPLE_NIGHT_PHOTO\x10G\x12\'\n#PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE\x10H\x12\x1b\n\x17PRESET_TITLE_STAR_TRAIL\x10L\x12\x1f\n\x1bPRESET_TITLE_LIGHT_PAINTING\x10M\x12\x1c\n\x18PRESET_TITLE_LIGHT_TRAIL\x10N\x12\x1b\n\x17PRESET_TITLE_FULL_FRAME\x10O'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "preset_status_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ENUMFLATMODE._serialized_start = 582
    _ENUMFLATMODE._serialized_end = 1216
    _ENUMPRESETGROUP._serialized_start = 1219
    _ENUMPRESETGROUP._serialized_end = 1472
    _ENUMPRESETICON._serialized_start = 1475
    _ENUMPRESETICON._serialized_end = 2915
    _ENUMPRESETTITLE._serialized_start = 2918
    _ENUMPRESETTITLE._serialized_end = 4659
    _NOTIFYPRESETSTATUS._serialized_start = 35
    _NOTIFYPRESETSTATUS._serialized_end = 108
    _PRESET._serialized_start = 111
    _PRESET._serialized_end = 393
    _PRESETGROUP._serialized_start = 395
    _PRESETGROUP._serialized_end = 515
    _PRESETSETTING._serialized_start = 517
    _PRESETSETTING._serialized_end = 579
