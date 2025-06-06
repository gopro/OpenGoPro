# media_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Jun  6 17:50:57 UTC 2025

"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0bmedia.proto\x12\nopen_gopro\x1a\x16response_generic.proto"\x1d\n\x1bRequestGetLastCapturedMedia"l\n\x19ResponseLastCapturedMedia\x12-\n\x06result\x18\x01 \x01(\x0e2\x1d.open_gopro.EnumResultGeneric\x12 \n\x05media\x18\x02 \x01(\x0b2\x11.open_gopro.Media'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "media_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _REQUESTGETLASTCAPTUREDMEDIA._serialized_start = 51
    _REQUESTGETLASTCAPTUREDMEDIA._serialized_end = 80
    _RESPONSELASTCAPTUREDMEDIA._serialized_start = 82
    _RESPONSELASTCAPTUREDMEDIA._serialized_end = 190
