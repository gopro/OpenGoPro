# set_camera_control_status_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Jun  6 17:50:57 UTC 2025

"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1fset_camera_control_status.proto\x12\nopen_gopro"c\n\x1dRequestSetCameraControlStatus\x12B\n\x15camera_control_status\x18\x01 \x02(\x0e2#.open_gopro.EnumCameraControlStatus*q\n\x17EnumCameraControlStatus\x12\x0f\n\x0bCAMERA_IDLE\x10\x00\x12\x12\n\x0eCAMERA_CONTROL\x10\x01\x12\x1b\n\x17CAMERA_EXTERNAL_CONTROL\x10\x02\x12\x14\n\x10CAMERA_COF_SETUP\x10\x03'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "set_camera_control_status_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ENUMCAMERACONTROLSTATUS._serialized_start = 148
    _ENUMCAMERACONTROLSTATUS._serialized_end = 261
    _REQUESTSETCAMERACONTROLSTATUS._serialized_start = 47
    _REQUESTSETCAMERACONTROLSTATUS._serialized_end = 146
