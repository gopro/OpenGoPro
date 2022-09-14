# network_management_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Sep 14 15:22:28 UTC 2022

"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x18network_management.proto\x12\nopen_gopro\x1a\x16response_generic.proto"R\n\x16NotifProvisioningState\x128\n\x12provisioning_state\x18\x01 \x02(\x0e2\x1c.open_gopro.EnumProvisioning"\xe6\x01\n\x11RequestConnectNew\x12\x0c\n\x04ssid\x18\x01 \x02(\t\x12\x10\n\x08password\x18\x02 \x02(\t\x12\x11\n\tstatic_ip\x18\x03 \x01(\x0c\x12\x0f\n\x07gateway\x18\x04 \x01(\x0c\x12\x0e\n\x06subnet\x18\x05 \x01(\x0c\x12\x13\n\x0bdns_primary\x18\x06 \x01(\x0c\x12\x15\n\rdns_secondary\x18\x07 \x01(\x0c\x12!\n\x19set_to_least_preferred_ap\x18\x08 \x01(\x08\x12.\n\ndeprecated\x18\t \x01(\x0e2\x1a.open_gopro.EnumDeprecated"\x96\x01\n\x12ResponseConnectNew\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x128\n\x12provisioning_state\x18\x02 \x02(\x0e2\x1c.open_gopro.EnumProvisioning\x12\x17\n\x0ftimeout_seconds\x18\x03 \x02(\x05*\x97\x01\n\x0eEnumDeprecated\x12\x10\n\x0cDEPRECATED_1\x10\x00\x12\x10\n\x0cDEPRECATED_2\x10\x01\x12\x10\n\x0cDEPRECATED_3\x10\x02\x12\x19\n\x15DEPRECATED_2_OR_CLOUD\x10\x03\x12\x10\n\x0cDEPRECATED_5\x10\x04\x12\x10\n\x0cDEPRECATED_6\x10\x08\x12\x10\n\x0cDEPRECATED_7\x10\x10*\xb5\x03\n\x10EnumProvisioning\x12\x18\n\x14PROVISIONING_UNKNOWN\x10\x00\x12\x1e\n\x1aPROVISIONING_NEVER_STARTED\x10\x01\x12\x18\n\x14PROVISIONING_STARTED\x10\x02\x12"\n\x1ePROVISIONING_ABORTED_BY_SYSTEM\x10\x03\x12"\n\x1ePROVISIONING_CANCELLED_BY_USER\x10\x04\x12\x1f\n\x1bPROVISIONING_SUCCESS_NEW_AP\x10\x05\x12\x1f\n\x1bPROVISIONING_SUCCESS_OLD_AP\x10\x06\x12*\n&PROVISIONING_ERROR_FAILED_TO_ASSOCIATE\x10\x07\x12$\n PROVISIONING_ERROR_PASSWORD_AUTH\x10\x08\x12$\n PROVISIONING_ERROR_EULA_BLOCKING\x10\t\x12"\n\x1ePROVISIONING_ERROR_NO_INTERNET\x10\n\x12\'\n#PROVISIONING_ERROR_UNSUPPORTED_TYPE\x10\x0b'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "network_management_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ENUMDEPRECATED._serialized_start = 535
    _ENUMDEPRECATED._serialized_end = 686
    _ENUMPROVISIONING._serialized_start = 689
    _ENUMPROVISIONING._serialized_end = 1126
    _NOTIFPROVISIONINGSTATE._serialized_start = 64
    _NOTIFPROVISIONINGSTATE._serialized_end = 146
    _REQUESTCONNECTNEW._serialized_start = 149
    _REQUESTCONNECTNEW._serialized_end = 379
    _RESPONSECONNECTNEW._serialized_start = 382
    _RESPONSECONNECTNEW._serialized_end = 532
