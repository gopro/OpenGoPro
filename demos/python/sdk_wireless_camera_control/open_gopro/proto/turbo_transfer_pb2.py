# turbo_transfer_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Feb 21 18:05:42 UTC 2025

import sys

_b = ((sys.version_info[0] < 3) and (lambda x: x)) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(
    name="turbo_transfer.proto",
    package="open_gopro",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        "\n\x14turbo_transfer.proto\x12\nopen_gopro\"'\n\x15RequestSetTurboActive\x12\x0e\n\x06active\x18\x01 \x02(\x08"
    ),
)
_REQUESTSETTURBOACTIVE = _descriptor.Descriptor(
    name="RequestSetTurboActive",
    full_name="open_gopro.RequestSetTurboActive",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="active",
            full_name="open_gopro.RequestSetTurboActive.active",
            index=0,
            number=1,
            type=8,
            cpp_type=7,
            label=2,
            has_default_value=False,
            default_value=False,
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
    serialized_start=36,
    serialized_end=75,
)
DESCRIPTOR.message_types_by_name["RequestSetTurboActive"] = _REQUESTSETTURBOACTIVE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
RequestSetTurboActive = _reflection.GeneratedProtocolMessageType(
    "RequestSetTurboActive",
    (_message.Message,),
    dict(DESCRIPTOR=_REQUESTSETTURBOACTIVE, __module__="turbo_transfer_pb2"),
)
_sym_db.RegisterMessage(RequestSetTurboActive)
