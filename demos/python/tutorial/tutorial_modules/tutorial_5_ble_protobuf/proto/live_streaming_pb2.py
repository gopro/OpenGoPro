# live_streaming_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Feb 21 18:05:41 UTC 2025

import sys

_b = ((sys.version_info[0] < 3) and (lambda x: x)) or (lambda x: x.encode("latin1"))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(
    name="live_streaming.proto",
    package="open_gopro",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x14live_streaming.proto\x12\nopen_gopro"Ë\x04\n\x16NotifyLiveStreamStatus\x12<\n\x12live_stream_status\x18\x01 \x01(\x0e2 .open_gopro.EnumLiveStreamStatus\x12:\n\x11live_stream_error\x18\x02 \x01(\x0e2\x1f.open_gopro.EnumLiveStreamError\x12\x1a\n\x12live_stream_encode\x18\x03 \x01(\x08\x12\x1b\n\x13live_stream_bitrate\x18\x04 \x01(\x05\x12K\n\'live_stream_window_size_supported_array\x18\x05 \x03(\x0e2\x1a.open_gopro.EnumWindowSize\x12$\n\x1clive_stream_encode_supported\x18\x06 \x01(\x08\x12(\n live_stream_max_lens_unsupported\x18\x07 \x01(\x08\x12*\n"live_stream_minimum_stream_bitrate\x18\x08 \x01(\x05\x12*\n"live_stream_maximum_stream_bitrate\x18\t \x01(\x05\x12"\n\x1alive_stream_lens_supported\x18\n \x01(\x08\x12>\n live_stream_lens_supported_array\x18\x0b \x03(\x0e2\x14.open_gopro.EnumLens\x12%\n\x1dlive_stream_protune_supported\x18\r \x01(\x08"¼\x01\n\x1aRequestGetLiveStreamStatus\x12M\n\x1bregister_live_stream_status\x18\x01 \x03(\x0e2(.open_gopro.EnumRegisterLiveStreamStatus\x12O\n\x1dunregister_live_stream_status\x18\x02 \x03(\x0e2(.open_gopro.EnumRegisterLiveStreamStatus"æ\x01\n\x18RequestSetLiveStreamMode\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0e\n\x06encode\x18\x02 \x01(\x08\x12/\n\x0bwindow_size\x18\x03 \x01(\x0e2\x1a.open_gopro.EnumWindowSize\x12\x0c\n\x04cert\x18\x06 \x01(\x0c\x12\x17\n\x0fminimum_bitrate\x18\x07 \x01(\x05\x12\x17\n\x0fmaximum_bitrate\x18\x08 \x01(\x05\x12\x18\n\x10starting_bitrate\x18\t \x01(\x05\x12"\n\x04lens\x18\n \x01(\x0e2\x14.open_gopro.EnumLens*>\n\x08EnumLens\x12\r\n\tLENS_WIDE\x10\x00\x12\x0f\n\x0bLENS_LINEAR\x10\x04\x12\x12\n\x0eLENS_SUPERVIEW\x10\x03*Þ\x03\n\x13EnumLiveStreamError\x12\x1a\n\x16LIVE_STREAM_ERROR_NONE\x10\x00\x12\x1d\n\x19LIVE_STREAM_ERROR_NETWORK\x10\x01\x12"\n\x1eLIVE_STREAM_ERROR_CREATESTREAM\x10\x02\x12!\n\x1dLIVE_STREAM_ERROR_OUTOFMEMORY\x10\x03\x12!\n\x1dLIVE_STREAM_ERROR_INPUTSTREAM\x10\x04\x12\x1e\n\x1aLIVE_STREAM_ERROR_INTERNET\x10\x05\x12\x1f\n\x1bLIVE_STREAM_ERROR_OSNETWORK\x10\x06\x12,\n(LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT\x10\x07\x12#\n\x1fLIVE_STREAM_ERROR_SSL_HANDSHAKE\x10\x08\x12$\n LIVE_STREAM_ERROR_CAMERA_BLOCKED\x10\t\x12\x1d\n\x19LIVE_STREAM_ERROR_UNKNOWN\x10\n\x12"\n\x1eLIVE_STREAM_ERROR_SD_CARD_FULL\x10(\x12%\n!LIVE_STREAM_ERROR_SD_CARD_REMOVED\x10)*£\x02\n\x14EnumLiveStreamStatus\x12\x1a\n\x16LIVE_STREAM_STATE_IDLE\x10\x00\x12\x1c\n\x18LIVE_STREAM_STATE_CONFIG\x10\x01\x12\x1b\n\x17LIVE_STREAM_STATE_READY\x10\x02\x12\x1f\n\x1bLIVE_STREAM_STATE_STREAMING\x10\x03\x12&\n"LIVE_STREAM_STATE_COMPLETE_STAY_ON\x10\x04\x12$\n LIVE_STREAM_STATE_FAILED_STAY_ON\x10\x05\x12"\n\x1eLIVE_STREAM_STATE_RECONNECTING\x10\x06\x12!\n\x1dLIVE_STREAM_STATE_UNAVAILABLE\x10\x07*¼\x01\n\x1cEnumRegisterLiveStreamStatus\x12&\n"REGISTER_LIVE_STREAM_STATUS_STATUS\x10\x01\x12%\n!REGISTER_LIVE_STREAM_STATUS_ERROR\x10\x02\x12$\n REGISTER_LIVE_STREAM_STATUS_MODE\x10\x03\x12\'\n#REGISTER_LIVE_STREAM_STATUS_BITRATE\x10\x04*P\n\x0eEnumWindowSize\x12\x13\n\x0fWINDOW_SIZE_480\x10\x04\x12\x13\n\x0fWINDOW_SIZE_720\x10\x07\x12\x14\n\x10WINDOW_SIZE_1080\x10\x0c'
    ),
)
_ENUMLENS = _descriptor.EnumDescriptor(
    name="EnumLens",
    full_name="open_gopro.EnumLens",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(name="LENS_WIDE", index=0, number=0, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(name="LENS_LINEAR", index=1, number=4, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(name="LENS_SUPERVIEW", index=2, number=3, serialized_options=None, type=None),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1050,
    serialized_end=1112,
)
_sym_db.RegisterEnumDescriptor(_ENUMLENS)
EnumLens = enum_type_wrapper.EnumTypeWrapper(_ENUMLENS)
_ENUMLIVESTREAMERROR = _descriptor.EnumDescriptor(
    name="EnumLiveStreamError",
    full_name="open_gopro.EnumLiveStreamError",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_NONE", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_NETWORK", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_CREATESTREAM", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_OUTOFMEMORY", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_INPUTSTREAM", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_INTERNET", index=5, number=5, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_OSNETWORK", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT", index=7, number=7, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_SSL_HANDSHAKE", index=8, number=8, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_CAMERA_BLOCKED", index=9, number=9, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_UNKNOWN", index=10, number=10, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_SD_CARD_FULL", index=11, number=40, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_ERROR_SD_CARD_REMOVED", index=12, number=41, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1115,
    serialized_end=1593,
)
_sym_db.RegisterEnumDescriptor(_ENUMLIVESTREAMERROR)
EnumLiveStreamError = enum_type_wrapper.EnumTypeWrapper(_ENUMLIVESTREAMERROR)
_ENUMLIVESTREAMSTATUS = _descriptor.EnumDescriptor(
    name="EnumLiveStreamStatus",
    full_name="open_gopro.EnumLiveStreamStatus",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_STATE_IDLE", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_STATE_CONFIG", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_STATE_READY", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_STATE_STREAMING", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_STATE_COMPLETE_STAY_ON", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_STATE_FAILED_STAY_ON", index=5, number=5, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_STATE_RECONNECTING", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="LIVE_STREAM_STATE_UNAVAILABLE", index=7, number=7, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1596,
    serialized_end=1887,
)
_sym_db.RegisterEnumDescriptor(_ENUMLIVESTREAMSTATUS)
EnumLiveStreamStatus = enum_type_wrapper.EnumTypeWrapper(_ENUMLIVESTREAMSTATUS)
_ENUMREGISTERLIVESTREAMSTATUS = _descriptor.EnumDescriptor(
    name="EnumRegisterLiveStreamStatus",
    full_name="open_gopro.EnumRegisterLiveStreamStatus",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="REGISTER_LIVE_STREAM_STATUS_STATUS", index=0, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="REGISTER_LIVE_STREAM_STATUS_ERROR", index=1, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="REGISTER_LIVE_STREAM_STATUS_MODE", index=2, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="REGISTER_LIVE_STREAM_STATUS_BITRATE", index=3, number=4, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1890,
    serialized_end=2078,
)
_sym_db.RegisterEnumDescriptor(_ENUMREGISTERLIVESTREAMSTATUS)
EnumRegisterLiveStreamStatus = enum_type_wrapper.EnumTypeWrapper(_ENUMREGISTERLIVESTREAMSTATUS)
_ENUMWINDOWSIZE = _descriptor.EnumDescriptor(
    name="EnumWindowSize",
    full_name="open_gopro.EnumWindowSize",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(name="WINDOW_SIZE_480", index=0, number=4, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(name="WINDOW_SIZE_720", index=1, number=7, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="WINDOW_SIZE_1080", index=2, number=12, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=2080,
    serialized_end=2160,
)
_sym_db.RegisterEnumDescriptor(_ENUMWINDOWSIZE)
EnumWindowSize = enum_type_wrapper.EnumTypeWrapper(_ENUMWINDOWSIZE)
LENS_WIDE = 0
LENS_LINEAR = 4
LENS_SUPERVIEW = 3
LIVE_STREAM_ERROR_NONE = 0
LIVE_STREAM_ERROR_NETWORK = 1
LIVE_STREAM_ERROR_CREATESTREAM = 2
LIVE_STREAM_ERROR_OUTOFMEMORY = 3
LIVE_STREAM_ERROR_INPUTSTREAM = 4
LIVE_STREAM_ERROR_INTERNET = 5
LIVE_STREAM_ERROR_OSNETWORK = 6
LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT = 7
LIVE_STREAM_ERROR_SSL_HANDSHAKE = 8
LIVE_STREAM_ERROR_CAMERA_BLOCKED = 9
LIVE_STREAM_ERROR_UNKNOWN = 10
LIVE_STREAM_ERROR_SD_CARD_FULL = 40
LIVE_STREAM_ERROR_SD_CARD_REMOVED = 41
LIVE_STREAM_STATE_IDLE = 0
LIVE_STREAM_STATE_CONFIG = 1
LIVE_STREAM_STATE_READY = 2
LIVE_STREAM_STATE_STREAMING = 3
LIVE_STREAM_STATE_COMPLETE_STAY_ON = 4
LIVE_STREAM_STATE_FAILED_STAY_ON = 5
LIVE_STREAM_STATE_RECONNECTING = 6
LIVE_STREAM_STATE_UNAVAILABLE = 7
REGISTER_LIVE_STREAM_STATUS_STATUS = 1
REGISTER_LIVE_STREAM_STATUS_ERROR = 2
REGISTER_LIVE_STREAM_STATUS_MODE = 3
REGISTER_LIVE_STREAM_STATUS_BITRATE = 4
WINDOW_SIZE_480 = 4
WINDOW_SIZE_720 = 7
WINDOW_SIZE_1080 = 12
_NOTIFYLIVESTREAMSTATUS = _descriptor.Descriptor(
    name="NotifyLiveStreamStatus",
    full_name="open_gopro.NotifyLiveStreamStatus",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="live_stream_status",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_status",
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
            name="live_stream_error",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_error",
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
            name="live_stream_encode",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_encode",
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
            name="live_stream_bitrate",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_bitrate",
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
            name="live_stream_window_size_supported_array",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_window_size_supported_array",
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
        _descriptor.FieldDescriptor(
            name="live_stream_encode_supported",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_encode_supported",
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
            name="live_stream_max_lens_unsupported",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_max_lens_unsupported",
            index=6,
            number=7,
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
            name="live_stream_minimum_stream_bitrate",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_minimum_stream_bitrate",
            index=7,
            number=8,
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
            name="live_stream_maximum_stream_bitrate",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_maximum_stream_bitrate",
            index=8,
            number=9,
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
            name="live_stream_lens_supported",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_lens_supported",
            index=9,
            number=10,
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
            name="live_stream_lens_supported_array",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_lens_supported_array",
            index=10,
            number=11,
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
        _descriptor.FieldDescriptor(
            name="live_stream_protune_supported",
            full_name="open_gopro.NotifyLiveStreamStatus.live_stream_protune_supported",
            index=11,
            number=13,
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
    serialized_start=37,
    serialized_end=624,
)
_REQUESTGETLIVESTREAMSTATUS = _descriptor.Descriptor(
    name="RequestGetLiveStreamStatus",
    full_name="open_gopro.RequestGetLiveStreamStatus",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="register_live_stream_status",
            full_name="open_gopro.RequestGetLiveStreamStatus.register_live_stream_status",
            index=0,
            number=1,
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
        _descriptor.FieldDescriptor(
            name="unregister_live_stream_status",
            full_name="open_gopro.RequestGetLiveStreamStatus.unregister_live_stream_status",
            index=1,
            number=2,
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
    serialized_start=627,
    serialized_end=815,
)
_REQUESTSETLIVESTREAMMODE = _descriptor.Descriptor(
    name="RequestSetLiveStreamMode",
    full_name="open_gopro.RequestSetLiveStreamMode",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="url",
            full_name="open_gopro.RequestSetLiveStreamMode.url",
            index=0,
            number=1,
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
            name="encode",
            full_name="open_gopro.RequestSetLiveStreamMode.encode",
            index=1,
            number=2,
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
            name="window_size",
            full_name="open_gopro.RequestSetLiveStreamMode.window_size",
            index=2,
            number=3,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=4,
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
            full_name="open_gopro.RequestSetLiveStreamMode.cert",
            index=3,
            number=6,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="minimum_bitrate",
            full_name="open_gopro.RequestSetLiveStreamMode.minimum_bitrate",
            index=4,
            number=7,
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
            name="maximum_bitrate",
            full_name="open_gopro.RequestSetLiveStreamMode.maximum_bitrate",
            index=5,
            number=8,
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
            name="starting_bitrate",
            full_name="open_gopro.RequestSetLiveStreamMode.starting_bitrate",
            index=6,
            number=9,
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
            name="lens",
            full_name="open_gopro.RequestSetLiveStreamMode.lens",
            index=7,
            number=10,
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
    serialized_start=818,
    serialized_end=1048,
)
_NOTIFYLIVESTREAMSTATUS.fields_by_name["live_stream_status"].enum_type = _ENUMLIVESTREAMSTATUS
_NOTIFYLIVESTREAMSTATUS.fields_by_name["live_stream_error"].enum_type = _ENUMLIVESTREAMERROR
_NOTIFYLIVESTREAMSTATUS.fields_by_name["live_stream_window_size_supported_array"].enum_type = _ENUMWINDOWSIZE
_NOTIFYLIVESTREAMSTATUS.fields_by_name["live_stream_lens_supported_array"].enum_type = _ENUMLENS
_REQUESTGETLIVESTREAMSTATUS.fields_by_name["register_live_stream_status"].enum_type = _ENUMREGISTERLIVESTREAMSTATUS
_REQUESTGETLIVESTREAMSTATUS.fields_by_name["unregister_live_stream_status"].enum_type = _ENUMREGISTERLIVESTREAMSTATUS
_REQUESTSETLIVESTREAMMODE.fields_by_name["window_size"].enum_type = _ENUMWINDOWSIZE
_REQUESTSETLIVESTREAMMODE.fields_by_name["lens"].enum_type = _ENUMLENS
DESCRIPTOR.message_types_by_name["NotifyLiveStreamStatus"] = _NOTIFYLIVESTREAMSTATUS
DESCRIPTOR.message_types_by_name["RequestGetLiveStreamStatus"] = _REQUESTGETLIVESTREAMSTATUS
DESCRIPTOR.message_types_by_name["RequestSetLiveStreamMode"] = _REQUESTSETLIVESTREAMMODE
DESCRIPTOR.enum_types_by_name["EnumLens"] = _ENUMLENS
DESCRIPTOR.enum_types_by_name["EnumLiveStreamError"] = _ENUMLIVESTREAMERROR
DESCRIPTOR.enum_types_by_name["EnumLiveStreamStatus"] = _ENUMLIVESTREAMSTATUS
DESCRIPTOR.enum_types_by_name["EnumRegisterLiveStreamStatus"] = _ENUMREGISTERLIVESTREAMSTATUS
DESCRIPTOR.enum_types_by_name["EnumWindowSize"] = _ENUMWINDOWSIZE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
NotifyLiveStreamStatus = _reflection.GeneratedProtocolMessageType(
    "NotifyLiveStreamStatus",
    (_message.Message,),
    dict(DESCRIPTOR=_NOTIFYLIVESTREAMSTATUS, __module__="live_streaming_pb2"),
)
_sym_db.RegisterMessage(NotifyLiveStreamStatus)
RequestGetLiveStreamStatus = _reflection.GeneratedProtocolMessageType(
    "RequestGetLiveStreamStatus",
    (_message.Message,),
    dict(DESCRIPTOR=_REQUESTGETLIVESTREAMSTATUS, __module__="live_streaming_pb2"),
)
_sym_db.RegisterMessage(RequestGetLiveStreamStatus)
RequestSetLiveStreamMode = _reflection.GeneratedProtocolMessageType(
    "RequestSetLiveStreamMode",
    (_message.Message,),
    dict(DESCRIPTOR=_REQUESTSETLIVESTREAMMODE, __module__="live_streaming_pb2"),
)
_sym_db.RegisterMessage(RequestSetLiveStreamMode)
