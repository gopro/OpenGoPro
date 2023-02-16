# response_generic_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 16 20:04:51 UTC 2023

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(
    name="response_generic.proto",
    package="open_gopro",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x16response_generic.proto\x12\nopen_gopro"@\n\x0fResponseGeneric\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric*¬\x01\n\x11EnumResultGeneric\x12\x12\n\x0eRESULT_UNKNOWN\x10\x00\x12\x12\n\x0eRESULT_SUCCESS\x10\x01\x12\x15\n\x11RESULT_ILL_FORMED\x10\x02\x12\x18\n\x14RESULT_NOT_SUPPORTED\x10\x03\x12!\n\x1dRESULT_ARGUMENT_OUT_OF_BOUNDS\x10\x04\x12\x1b\n\x17RESULT_ARGUMENT_INVALID\x10\x05'
    ),
)
_ENUMRESULTGENERIC = _descriptor.EnumDescriptor(
    name="EnumResultGeneric",
    full_name="open_gopro.EnumResultGeneric",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="RESULT_UNKNOWN", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="RESULT_SUCCESS", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="RESULT_ILL_FORMED", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="RESULT_NOT_SUPPORTED", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="RESULT_ARGUMENT_OUT_OF_BOUNDS", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="RESULT_ARGUMENT_INVALID", index=5, number=5, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=105,
    serialized_end=277,
)
_sym_db.RegisterEnumDescriptor(_ENUMRESULTGENERIC)
EnumResultGeneric = enum_type_wrapper.EnumTypeWrapper(_ENUMRESULTGENERIC)
RESULT_UNKNOWN = 0
RESULT_SUCCESS = 1
RESULT_ILL_FORMED = 2
RESULT_NOT_SUPPORTED = 3
RESULT_ARGUMENT_OUT_OF_BOUNDS = 4
RESULT_ARGUMENT_INVALID = 5
_RESPONSEGENERIC = _descriptor.Descriptor(
    name="ResponseGeneric",
    full_name="open_gopro.ResponseGeneric",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="result",
            full_name="open_gopro.ResponseGeneric.result",
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
    serialized_start=38,
    serialized_end=102,
)
_RESPONSEGENERIC.fields_by_name["result"].enum_type = _ENUMRESULTGENERIC
DESCRIPTOR.message_types_by_name["ResponseGeneric"] = _RESPONSEGENERIC
DESCRIPTOR.enum_types_by_name["EnumResultGeneric"] = _ENUMRESULTGENERIC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
ResponseGeneric = _reflection.GeneratedProtocolMessageType(
    "ResponseGeneric",
    (_message.Message,),
    dict(DESCRIPTOR=_RESPONSEGENERIC, __module__="response_generic_pb2"),
)
_sym_db.RegisterMessage(ResponseGeneric)
