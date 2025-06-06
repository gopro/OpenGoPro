# live_streaming_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Jun  6 17:50:57 UTC 2025

"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x14live_streaming.proto\x12\nopen_gopro"\xcb\x04\n\x16NotifyLiveStreamStatus\x12<\n\x12live_stream_status\x18\x01 \x01(\x0e2 .open_gopro.EnumLiveStreamStatus\x12:\n\x11live_stream_error\x18\x02 \x01(\x0e2\x1f.open_gopro.EnumLiveStreamError\x12\x1a\n\x12live_stream_encode\x18\x03 \x01(\x08\x12\x1b\n\x13live_stream_bitrate\x18\x04 \x01(\x05\x12K\n\'live_stream_window_size_supported_array\x18\x05 \x03(\x0e2\x1a.open_gopro.EnumWindowSize\x12$\n\x1clive_stream_encode_supported\x18\x06 \x01(\x08\x12(\n live_stream_max_lens_unsupported\x18\x07 \x01(\x08\x12*\n"live_stream_minimum_stream_bitrate\x18\x08 \x01(\x05\x12*\n"live_stream_maximum_stream_bitrate\x18\t \x01(\x05\x12"\n\x1alive_stream_lens_supported\x18\n \x01(\x08\x12>\n live_stream_lens_supported_array\x18\x0b \x03(\x0e2\x14.open_gopro.EnumLens\x12%\n\x1dlive_stream_protune_supported\x18\r \x01(\x08"\xbc\x01\n\x1aRequestGetLiveStreamStatus\x12M\n\x1bregister_live_stream_status\x18\x01 \x03(\x0e2(.open_gopro.EnumRegisterLiveStreamStatus\x12O\n\x1dunregister_live_stream_status\x18\x02 \x03(\x0e2(.open_gopro.EnumRegisterLiveStreamStatus"\xe6\x01\n\x18RequestSetLiveStreamMode\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0e\n\x06encode\x18\x02 \x01(\x08\x12/\n\x0bwindow_size\x18\x03 \x01(\x0e2\x1a.open_gopro.EnumWindowSize\x12\x0c\n\x04cert\x18\x06 \x01(\x0c\x12\x17\n\x0fminimum_bitrate\x18\x07 \x01(\x05\x12\x17\n\x0fmaximum_bitrate\x18\x08 \x01(\x05\x12\x18\n\x10starting_bitrate\x18\t \x01(\x05\x12"\n\x04lens\x18\n \x01(\x0e2\x14.open_gopro.EnumLens*>\n\x08EnumLens\x12\r\n\tLENS_WIDE\x10\x00\x12\x0f\n\x0bLENS_LINEAR\x10\x04\x12\x12\n\x0eLENS_SUPERVIEW\x10\x03*\xde\x03\n\x13EnumLiveStreamError\x12\x1a\n\x16LIVE_STREAM_ERROR_NONE\x10\x00\x12\x1d\n\x19LIVE_STREAM_ERROR_NETWORK\x10\x01\x12"\n\x1eLIVE_STREAM_ERROR_CREATESTREAM\x10\x02\x12!\n\x1dLIVE_STREAM_ERROR_OUTOFMEMORY\x10\x03\x12!\n\x1dLIVE_STREAM_ERROR_INPUTSTREAM\x10\x04\x12\x1e\n\x1aLIVE_STREAM_ERROR_INTERNET\x10\x05\x12\x1f\n\x1bLIVE_STREAM_ERROR_OSNETWORK\x10\x06\x12,\n(LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT\x10\x07\x12#\n\x1fLIVE_STREAM_ERROR_SSL_HANDSHAKE\x10\x08\x12$\n LIVE_STREAM_ERROR_CAMERA_BLOCKED\x10\t\x12\x1d\n\x19LIVE_STREAM_ERROR_UNKNOWN\x10\n\x12"\n\x1eLIVE_STREAM_ERROR_SD_CARD_FULL\x10(\x12%\n!LIVE_STREAM_ERROR_SD_CARD_REMOVED\x10)*\xa3\x02\n\x14EnumLiveStreamStatus\x12\x1a\n\x16LIVE_STREAM_STATE_IDLE\x10\x00\x12\x1c\n\x18LIVE_STREAM_STATE_CONFIG\x10\x01\x12\x1b\n\x17LIVE_STREAM_STATE_READY\x10\x02\x12\x1f\n\x1bLIVE_STREAM_STATE_STREAMING\x10\x03\x12&\n"LIVE_STREAM_STATE_COMPLETE_STAY_ON\x10\x04\x12$\n LIVE_STREAM_STATE_FAILED_STAY_ON\x10\x05\x12"\n\x1eLIVE_STREAM_STATE_RECONNECTING\x10\x06\x12!\n\x1dLIVE_STREAM_STATE_UNAVAILABLE\x10\x07*\xbc\x01\n\x1cEnumRegisterLiveStreamStatus\x12&\n"REGISTER_LIVE_STREAM_STATUS_STATUS\x10\x01\x12%\n!REGISTER_LIVE_STREAM_STATUS_ERROR\x10\x02\x12$\n REGISTER_LIVE_STREAM_STATUS_MODE\x10\x03\x12\'\n#REGISTER_LIVE_STREAM_STATUS_BITRATE\x10\x04*P\n\x0eEnumWindowSize\x12\x13\n\x0fWINDOW_SIZE_480\x10\x04\x12\x13\n\x0fWINDOW_SIZE_720\x10\x07\x12\x14\n\x10WINDOW_SIZE_1080\x10\x0c'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "live_streaming_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ENUMLENS._serialized_start = 1050
    _ENUMLENS._serialized_end = 1112
    _ENUMLIVESTREAMERROR._serialized_start = 1115
    _ENUMLIVESTREAMERROR._serialized_end = 1593
    _ENUMLIVESTREAMSTATUS._serialized_start = 1596
    _ENUMLIVESTREAMSTATUS._serialized_end = 1887
    _ENUMREGISTERLIVESTREAMSTATUS._serialized_start = 1890
    _ENUMREGISTERLIVESTREAMSTATUS._serialized_end = 2078
    _ENUMWINDOWSIZE._serialized_start = 2080
    _ENUMWINDOWSIZE._serialized_end = 2160
    _NOTIFYLIVESTREAMSTATUS._serialized_start = 37
    _NOTIFYLIVESTREAMSTATUS._serialized_end = 624
    _REQUESTGETLIVESTREAMSTATUS._serialized_start = 627
    _REQUESTGETLIVESTREAMSTATUS._serialized_end = 815
    _REQUESTSETLIVESTREAMMODE._serialized_start = 818
    _REQUESTSETLIVESTREAMMODE._serialized_end = 1048
