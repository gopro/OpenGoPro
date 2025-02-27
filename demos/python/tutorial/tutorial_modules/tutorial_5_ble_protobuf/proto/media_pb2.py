# media_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Feb 21 18:05:41 UTC 2025

import sys

_b = ((sys.version_info[0] < 3) and (lambda x: x)) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="media.proto",
    package="open_gopro",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x0bmedia.proto\x12\nopen_gopro\x1a\x16response_generic.proto"\x1d\n\x1bRequestGetLastCapturedMedia"l\n\x19ResponseLastCapturedMedia\x12-\n\x06result\x18\x01 \x01(\x0e2\x1d.open_gopro.EnumResultGeneric\x12 \n\x05media\x18\x02 \x01(\x0b2\x11.open_gopro.Media'
    ),
    dependencies=[response__generic__pb2.DESCRIPTOR],
)
_REQUESTGETLASTCAPTUREDMEDIA = _descriptor.Descriptor(
    name="RequestGetLastCapturedMedia",
    full_name="open_gopro.RequestGetLastCapturedMedia",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=51,
    serialized_end=80,
)
_RESPONSELASTCAPTUREDMEDIA = _descriptor.Descriptor(
    name="ResponseLastCapturedMedia",
    full_name="open_gopro.ResponseLastCapturedMedia",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="result",
            full_name="open_gopro.ResponseLastCapturedMedia.result",
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
            name="media",
            full_name="open_gopro.ResponseLastCapturedMedia.media",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
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
    serialized_start=82,
    serialized_end=190,
)
_RESPONSELASTCAPTUREDMEDIA.fields_by_name["result"].enum_type = response__generic__pb2._ENUMRESULTGENERIC
_RESPONSELASTCAPTUREDMEDIA.fields_by_name["media"].message_type = response__generic__pb2._MEDIA
DESCRIPTOR.message_types_by_name["RequestGetLastCapturedMedia"] = _REQUESTGETLASTCAPTUREDMEDIA
DESCRIPTOR.message_types_by_name["ResponseLastCapturedMedia"] = _RESPONSELASTCAPTUREDMEDIA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
RequestGetLastCapturedMedia = _reflection.GeneratedProtocolMessageType(
    "RequestGetLastCapturedMedia",
    (_message.Message,),
    dict(DESCRIPTOR=_REQUESTGETLASTCAPTUREDMEDIA, __module__="media_pb2"),
)
_sym_db.RegisterMessage(RequestGetLastCapturedMedia)
ResponseLastCapturedMedia = _reflection.GeneratedProtocolMessageType(
    "ResponseLastCapturedMedia",
    (_message.Message,),
    dict(DESCRIPTOR=_RESPONSELASTCAPTUREDMEDIA, __module__="media_pb2"),
)
_sym_db.RegisterMessage(ResponseLastCapturedMedia)
