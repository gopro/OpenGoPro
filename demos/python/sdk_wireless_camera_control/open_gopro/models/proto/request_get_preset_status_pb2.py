# request_get_preset_status_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Jun  6 17:50:57 UTC 2025

"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1frequest_get_preset_status.proto\x12\nopen_gopro"\xc8\x01\n\x16RequestGetPresetStatus\x12D\n\x16register_preset_status\x18\x01 \x03(\x0e2$.open_gopro.EnumRegisterPresetStatus\x12F\n\x18unregister_preset_status\x18\x02 \x03(\x0e2$.open_gopro.EnumRegisterPresetStatus\x12 \n\x18use_constant_setting_ids\x18\x03 \x01(\x08*l\n\x18EnumRegisterPresetStatus\x12!\n\x1dREGISTER_PRESET_STATUS_PRESET\x10\x01\x12-\n)REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY\x10\x02'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "request_get_preset_status_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ENUMREGISTERPRESETSTATUS._serialized_start = 250
    _ENUMREGISTERPRESETSTATUS._serialized_end = 358
    _REQUESTGETPRESETSTATUS._serialized_start = 48
    _REQUESTGETPRESETSTATUS._serialized_end = 248
