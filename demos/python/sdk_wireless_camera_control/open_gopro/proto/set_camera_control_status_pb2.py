# set_camera_control_status_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Feb 21 18:05:42 UTC 2025

import sys

_b = ((sys.version_info[0] < 3) and (lambda x: x)) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import enum_type_wrapper

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(
    name="set_camera_control_status.proto",
    package="open_gopro",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x1fset_camera_control_status.proto\x12\nopen_gopro"c\n\x1dRequestSetCameraControlStatus\x12B\n\x15camera_control_status\x18\x01 \x02(\x0e2#.open_gopro.EnumCameraControlStatus*q\n\x17EnumCameraControlStatus\x12\x0f\n\x0bCAMERA_IDLE\x10\x00\x12\x12\n\x0eCAMERA_CONTROL\x10\x01\x12\x1b\n\x17CAMERA_EXTERNAL_CONTROL\x10\x02\x12\x14\n\x10CAMERA_COF_SETUP\x10\x03'
    ),
)
_ENUMCAMERACONTROLSTATUS = _descriptor.EnumDescriptor(
    name="EnumCameraControlStatus",
    full_name="open_gopro.EnumCameraControlStatus",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(name="CAMERA_IDLE", index=0, number=0, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(name="CAMERA_CONTROL", index=1, number=1, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="CAMERA_EXTERNAL_CONTROL", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(name="CAMERA_COF_SETUP", index=3, number=3, serialized_options=None, type=None),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=148,
    serialized_end=261,
)
_sym_db.RegisterEnumDescriptor(_ENUMCAMERACONTROLSTATUS)
EnumCameraControlStatus = enum_type_wrapper.EnumTypeWrapper(_ENUMCAMERACONTROLSTATUS)
CAMERA_IDLE = 0
CAMERA_CONTROL = 1
CAMERA_EXTERNAL_CONTROL = 2
CAMERA_COF_SETUP = 3
_REQUESTSETCAMERACONTROLSTATUS = _descriptor.Descriptor(
    name="RequestSetCameraControlStatus",
    full_name="open_gopro.RequestSetCameraControlStatus",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="camera_control_status",
            full_name="open_gopro.RequestSetCameraControlStatus.camera_control_status",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
            label=2,
            has_default_value=False,
            default_value=0,
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
    serialized_start=47,
    serialized_end=146,
)
_REQUESTSETCAMERACONTROLSTATUS.fields_by_name["camera_control_status"].enum_type = _ENUMCAMERACONTROLSTATUS
DESCRIPTOR.message_types_by_name["RequestSetCameraControlStatus"] = _REQUESTSETCAMERACONTROLSTATUS
DESCRIPTOR.enum_types_by_name["EnumCameraControlStatus"] = _ENUMCAMERACONTROLSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
RequestSetCameraControlStatus = _reflection.GeneratedProtocolMessageType(
    "RequestSetCameraControlStatus",
    (_message.Message,),
    dict(DESCRIPTOR=_REQUESTSETCAMERACONTROLSTATUS, __module__="set_camera_control_status_pb2"),
)
_sym_db.RegisterMessage(RequestSetCameraControlStatus)
