# cohn_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
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
    name="cohn.proto",
    package="open_gopro",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n\ncohn.proto\x12\nopen_gopro\x1a\x16response_generic.proto"4\n\x14RequestGetCOHNStatus\x12\x1c\n\x14register_cohn_status\x18\x01 \x01(\x08"Ù\x01\n\x10NotifyCOHNStatus\x12*\n\x06status\x18\x01 \x01(\x0e2\x1a.open_gopro.EnumCOHNStatus\x12/\n\x05state\x18\x02 \x01(\x0e2 .open_gopro.EnumCOHNNetworkState\x12\x10\n\x08username\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12\x11\n\tipaddress\x18\x05 \x01(\t\x12\x0f\n\x07enabled\x18\x06 \x01(\x08\x12\x0c\n\x04ssid\x18\x07 \x01(\t\x12\x12\n\nmacaddress\x18\x08 \x01(\t")\n\x15RequestCreateCOHNCert\x12\x10\n\x08override\x18\x01 \x01(\x08"\x16\n\x14RequestClearCOHNCert"\x11\n\x0fRequestCOHNCert"O\n\x10ResponseCOHNCert\x12-\n\x06result\x18\x01 \x01(\x0e2\x1d.open_gopro.EnumResultGeneric\x12\x0c\n\x04cert\x18\x02 \x01(\t",\n\x15RequestSetCOHNSetting\x12\x13\n\x0bcohn_active\x18\x01 \x01(\x08*>\n\x0eEnumCOHNStatus\x12\x16\n\x12COHN_UNPROVISIONED\x10\x00\x12\x14\n\x10COHN_PROVISIONED\x10\x01*ì\x01\n\x14EnumCOHNNetworkState\x12\x13\n\x0fCOHN_STATE_Init\x10\x00\x12\x14\n\x10COHN_STATE_Error\x10\x01\x12\x13\n\x0fCOHN_STATE_Exit\x10\x02\x12\x13\n\x0fCOHN_STATE_Idle\x10\x05\x12\x1f\n\x1bCOHN_STATE_NetworkConnected\x10\x1b\x12"\n\x1eCOHN_STATE_NetworkDisconnected\x10\x1c\x12"\n\x1eCOHN_STATE_ConnectingToNetwork\x10\x1d\x12\x16\n\x12COHN_STATE_Invalid\x10\x1e'
    ),
    dependencies=[response__generic__pb2.DESCRIPTOR],
)
_ENUMCOHNSTATUS = _descriptor.EnumDescriptor(
    name="EnumCOHNStatus",
    full_name="open_gopro.EnumCOHNStatus",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="COHN_UNPROVISIONED", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(name="COHN_PROVISIONED", index=1, number=1, serialized_options=None, type=None),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=537,
    serialized_end=599,
)
_sym_db.RegisterEnumDescriptor(_ENUMCOHNSTATUS)
EnumCOHNStatus = enum_type_wrapper.EnumTypeWrapper(_ENUMCOHNSTATUS)
_ENUMCOHNNETWORKSTATE = _descriptor.EnumDescriptor(
    name="EnumCOHNNetworkState",
    full_name="open_gopro.EnumCOHNNetworkState",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(name="COHN_STATE_Init", index=0, number=0, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(name="COHN_STATE_Error", index=1, number=1, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(name="COHN_STATE_Exit", index=2, number=2, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(name="COHN_STATE_Idle", index=3, number=5, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="COHN_STATE_NetworkConnected", index=4, number=27, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="COHN_STATE_NetworkDisconnected", index=5, number=28, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="COHN_STATE_ConnectingToNetwork", index=6, number=29, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="COHN_STATE_Invalid", index=7, number=30, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=602,
    serialized_end=838,
)
_sym_db.RegisterEnumDescriptor(_ENUMCOHNNETWORKSTATE)
EnumCOHNNetworkState = enum_type_wrapper.EnumTypeWrapper(_ENUMCOHNNETWORKSTATE)
COHN_UNPROVISIONED = 0
COHN_PROVISIONED = 1
COHN_STATE_Init = 0
COHN_STATE_Error = 1
COHN_STATE_Exit = 2
COHN_STATE_Idle = 5
COHN_STATE_NetworkConnected = 27
COHN_STATE_NetworkDisconnected = 28
COHN_STATE_ConnectingToNetwork = 29
COHN_STATE_Invalid = 30
_REQUESTGETCOHNSTATUS = _descriptor.Descriptor(
    name="RequestGetCOHNStatus",
    full_name="open_gopro.RequestGetCOHNStatus",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="register_cohn_status",
            full_name="open_gopro.RequestGetCOHNStatus.register_cohn_status",
            index=0,
            number=1,
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
    serialized_start=50,
    serialized_end=102,
)
_NOTIFYCOHNSTATUS = _descriptor.Descriptor(
    name="NotifyCOHNStatus",
    full_name="open_gopro.NotifyCOHNStatus",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="status",
            full_name="open_gopro.NotifyCOHNStatus.status",
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
            name="state",
            full_name="open_gopro.NotifyCOHNStatus.state",
            index=1,
            number=2,
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
            name="username",
            full_name="open_gopro.NotifyCOHNStatus.username",
            index=2,
            number=3,
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
            name="password",
            full_name="open_gopro.NotifyCOHNStatus.password",
            index=3,
            number=4,
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
            name="ipaddress",
            full_name="open_gopro.NotifyCOHNStatus.ipaddress",
            index=4,
            number=5,
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
            name="enabled",
            full_name="open_gopro.NotifyCOHNStatus.enabled",
            index=5,
            number=6,
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
            name="ssid",
            full_name="open_gopro.NotifyCOHNStatus.ssid",
            index=6,
            number=7,
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
            name="macaddress",
            full_name="open_gopro.NotifyCOHNStatus.macaddress",
            index=7,
            number=8,
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
    serialized_start=105,
    serialized_end=322,
)
_REQUESTCREATECOHNCERT = _descriptor.Descriptor(
    name="RequestCreateCOHNCert",
    full_name="open_gopro.RequestCreateCOHNCert",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="override",
            full_name="open_gopro.RequestCreateCOHNCert.override",
            index=0,
            number=1,
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
    serialized_start=324,
    serialized_end=365,
)
_REQUESTCLEARCOHNCERT = _descriptor.Descriptor(
    name="RequestClearCOHNCert",
    full_name="open_gopro.RequestClearCOHNCert",
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
    serialized_start=367,
    serialized_end=389,
)
_REQUESTCOHNCERT = _descriptor.Descriptor(
    name="RequestCOHNCert",
    full_name="open_gopro.RequestCOHNCert",
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
    serialized_start=391,
    serialized_end=408,
)
_RESPONSECOHNCERT = _descriptor.Descriptor(
    name="ResponseCOHNCert",
    full_name="open_gopro.ResponseCOHNCert",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="result",
            full_name="open_gopro.ResponseCOHNCert.result",
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
            name="cert",
            full_name="open_gopro.ResponseCOHNCert.cert",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=410,
    serialized_end=489,
)
_REQUESTSETCOHNSETTING = _descriptor.Descriptor(
    name="RequestSetCOHNSetting",
    full_name="open_gopro.RequestSetCOHNSetting",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="cohn_active",
            full_name="open_gopro.RequestSetCOHNSetting.cohn_active",
            index=0,
            number=1,
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
    serialized_start=491,
    serialized_end=535,
)
_NOTIFYCOHNSTATUS.fields_by_name["status"].enum_type = _ENUMCOHNSTATUS
_NOTIFYCOHNSTATUS.fields_by_name["state"].enum_type = _ENUMCOHNNETWORKSTATE
_RESPONSECOHNCERT.fields_by_name["result"].enum_type = response__generic__pb2._ENUMRESULTGENERIC
DESCRIPTOR.message_types_by_name["RequestGetCOHNStatus"] = _REQUESTGETCOHNSTATUS
DESCRIPTOR.message_types_by_name["NotifyCOHNStatus"] = _NOTIFYCOHNSTATUS
DESCRIPTOR.message_types_by_name["RequestCreateCOHNCert"] = _REQUESTCREATECOHNCERT
DESCRIPTOR.message_types_by_name["RequestClearCOHNCert"] = _REQUESTCLEARCOHNCERT
DESCRIPTOR.message_types_by_name["RequestCOHNCert"] = _REQUESTCOHNCERT
DESCRIPTOR.message_types_by_name["ResponseCOHNCert"] = _RESPONSECOHNCERT
DESCRIPTOR.message_types_by_name["RequestSetCOHNSetting"] = _REQUESTSETCOHNSETTING
DESCRIPTOR.enum_types_by_name["EnumCOHNStatus"] = _ENUMCOHNSTATUS
DESCRIPTOR.enum_types_by_name["EnumCOHNNetworkState"] = _ENUMCOHNNETWORKSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
RequestGetCOHNStatus = _reflection.GeneratedProtocolMessageType(
    "RequestGetCOHNStatus", (_message.Message,), dict(DESCRIPTOR=_REQUESTGETCOHNSTATUS, __module__="cohn_pb2")
)
_sym_db.RegisterMessage(RequestGetCOHNStatus)
NotifyCOHNStatus = _reflection.GeneratedProtocolMessageType(
    "NotifyCOHNStatus", (_message.Message,), dict(DESCRIPTOR=_NOTIFYCOHNSTATUS, __module__="cohn_pb2")
)
_sym_db.RegisterMessage(NotifyCOHNStatus)
RequestCreateCOHNCert = _reflection.GeneratedProtocolMessageType(
    "RequestCreateCOHNCert", (_message.Message,), dict(DESCRIPTOR=_REQUESTCREATECOHNCERT, __module__="cohn_pb2")
)
_sym_db.RegisterMessage(RequestCreateCOHNCert)
RequestClearCOHNCert = _reflection.GeneratedProtocolMessageType(
    "RequestClearCOHNCert", (_message.Message,), dict(DESCRIPTOR=_REQUESTCLEARCOHNCERT, __module__="cohn_pb2")
)
_sym_db.RegisterMessage(RequestClearCOHNCert)
RequestCOHNCert = _reflection.GeneratedProtocolMessageType(
    "RequestCOHNCert", (_message.Message,), dict(DESCRIPTOR=_REQUESTCOHNCERT, __module__="cohn_pb2")
)
_sym_db.RegisterMessage(RequestCOHNCert)
ResponseCOHNCert = _reflection.GeneratedProtocolMessageType(
    "ResponseCOHNCert", (_message.Message,), dict(DESCRIPTOR=_RESPONSECOHNCERT, __module__="cohn_pb2")
)
_sym_db.RegisterMessage(ResponseCOHNCert)
RequestSetCOHNSetting = _reflection.GeneratedProtocolMessageType(
    "RequestSetCOHNSetting", (_message.Message,), dict(DESCRIPTOR=_REQUESTSETCOHNSETTING, __module__="cohn_pb2")
)
_sym_db.RegisterMessage(RequestSetCOHNSetting)
