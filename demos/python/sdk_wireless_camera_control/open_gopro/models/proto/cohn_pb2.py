# cohn_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Jun  6 17:50:57 UTC 2025

"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ncohn.proto\x12\nopen_gopro\x1a\x16response_generic.proto"4\n\x14RequestGetCOHNStatus\x12\x1c\n\x14register_cohn_status\x18\x01 \x01(\x08"\xd9\x01\n\x10NotifyCOHNStatus\x12*\n\x06status\x18\x01 \x01(\x0e2\x1a.open_gopro.EnumCOHNStatus\x12/\n\x05state\x18\x02 \x01(\x0e2 .open_gopro.EnumCOHNNetworkState\x12\x10\n\x08username\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12\x11\n\tipaddress\x18\x05 \x01(\t\x12\x0f\n\x07enabled\x18\x06 \x01(\x08\x12\x0c\n\x04ssid\x18\x07 \x01(\t\x12\x12\n\nmacaddress\x18\x08 \x01(\t")\n\x15RequestCreateCOHNCert\x12\x10\n\x08override\x18\x01 \x01(\x08"\x16\n\x14RequestClearCOHNCert"\x11\n\x0fRequestCOHNCert"O\n\x10ResponseCOHNCert\x12-\n\x06result\x18\x01 \x01(\x0e2\x1d.open_gopro.EnumResultGeneric\x12\x0c\n\x04cert\x18\x02 \x01(\t",\n\x15RequestSetCOHNSetting\x12\x13\n\x0bcohn_active\x18\x01 \x01(\x08*>\n\x0eEnumCOHNStatus\x12\x16\n\x12COHN_UNPROVISIONED\x10\x00\x12\x14\n\x10COHN_PROVISIONED\x10\x01*\xec\x01\n\x14EnumCOHNNetworkState\x12\x13\n\x0fCOHN_STATE_Init\x10\x00\x12\x14\n\x10COHN_STATE_Error\x10\x01\x12\x13\n\x0fCOHN_STATE_Exit\x10\x02\x12\x13\n\x0fCOHN_STATE_Idle\x10\x05\x12\x1f\n\x1bCOHN_STATE_NetworkConnected\x10\x1b\x12"\n\x1eCOHN_STATE_NetworkDisconnected\x10\x1c\x12"\n\x1eCOHN_STATE_ConnectingToNetwork\x10\x1d\x12\x16\n\x12COHN_STATE_Invalid\x10\x1e'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "cohn_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ENUMCOHNSTATUS._serialized_start = 537
    _ENUMCOHNSTATUS._serialized_end = 599
    _ENUMCOHNNETWORKSTATE._serialized_start = 602
    _ENUMCOHNNETWORKSTATE._serialized_end = 838
    _REQUESTGETCOHNSTATUS._serialized_start = 50
    _REQUESTGETCOHNSTATUS._serialized_end = 102
    _NOTIFYCOHNSTATUS._serialized_start = 105
    _NOTIFYCOHNSTATUS._serialized_end = 322
    _REQUESTCREATECOHNCERT._serialized_start = 324
    _REQUESTCREATECOHNCERT._serialized_end = 365
    _REQUESTCLEARCOHNCERT._serialized_start = 367
    _REQUESTCLEARCOHNCERT._serialized_end = 389
    _REQUESTCOHNCERT._serialized_start = 391
    _REQUESTCOHNCERT._serialized_end = 408
    _RESPONSECOHNCERT._serialized_start = 410
    _RESPONSECOHNCERT._serialized_end = 489
    _REQUESTSETCOHNSETTING._serialized_start = 491
    _REQUESTSETCOHNSETTING._serialized_end = 535
