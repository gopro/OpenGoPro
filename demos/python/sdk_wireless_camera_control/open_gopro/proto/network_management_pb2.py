# network_management_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x18network_management.proto\x12\nopen_gopro\x1a\x16response_generic.proto"R\n\x16NotifProvisioningState\x128\n\x12provisioning_state\x18\x01 \x02(\x0e2\x1c.open_gopro.EnumProvisioning"\x8d\x01\n\x12NotifStartScanning\x120\n\x0escanning_state\x18\x01 \x02(\x0e2\x18.open_gopro.EnumScanning\x12\x0f\n\x07scan_id\x18\x02 \x01(\x05\x12\x15\n\rtotal_entries\x18\x03 \x01(\x05\x12\x1d\n\x15total_configured_ssid\x18\x04 \x02(\x05"S\n\x0eRequestConnect\x12\x0c\n\x04ssid\x18\x01 \x02(\t\x123\n\rowner_purpose\x18\x02 \x01(\x0e2\x1c.open_gopro.EnumNetworkOwner"\xeb\x01\n\x11RequestConnectNew\x12\x0c\n\x04ssid\x18\x01 \x02(\t\x12\x10\n\x08password\x18\x02 \x02(\t\x12\x11\n\tstatic_ip\x18\x03 \x01(\x0c\x12\x0f\n\x07gateway\x18\x04 \x01(\x0c\x12\x0e\n\x06subnet\x18\x05 \x01(\x0c\x12\x13\n\x0bdns_primary\x18\x06 \x01(\x0c\x12\x15\n\rdns_secondary\x18\x07 \x01(\x0c\x12!\n\x19set_to_least_preferred_ap\x18\x08 \x01(\x08\x123\n\rowner_purpose\x18\t \x01(\x0e2\x1c.open_gopro.EnumNetworkOwner"P\n\x13RequestGetApEntries\x12\x13\n\x0bstart_index\x18\x01 \x02(\x05\x12\x13\n\x0bmax_entries\x18\x02 \x02(\x05\x12\x0f\n\x07scan_id\x18\x03 \x02(\x05"\x17\n\x15RequestReleaseNetwork"\x12\n\x10RequestStartScan"\x93\x01\n\x0fResponseConnect\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x128\n\x12provisioning_state\x18\x02 \x02(\x0e2\x1c.open_gopro.EnumProvisioning\x12\x17\n\x0ftimeout_seconds\x18\x03 \x02(\x05"\x96\x01\n\x12ResponseConnectNew\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x128\n\x12provisioning_state\x18\x02 \x02(\x0e2\x1c.open_gopro.EnumProvisioning\x12\x17\n\x0ftimeout_seconds\x18\x03 \x02(\x05"\xa4\x01\n\tScanEntry\x12\x0c\n\x04ssid\x18\x01 \x02(\t\x12\x1c\n\x14signal_strength_bars\x18\x02 \x02(\x05\x12\x1c\n\x14signal_frequency_mhz\x18\x04 \x02(\x05\x12\x18\n\x10scan_entry_flags\x18\x05 \x02(\x05\x123\n\rowner_purpose\x18\x06 \x01(\x0e2\x1c.open_gopro.EnumNetworkOwner"~\n\x14ResponseGetApEntries\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x12\x0f\n\x07scan_id\x18\x02 \x02(\x05\x12&\n\x07entries\x18\x03 \x03(\x0b2\x15.open_gopro.ScanEntry"x\n\x15ResponseStartScanning\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x120\n\x0escanning_state\x18\x02 \x02(\x0e2\x18.open_gopro.EnumScanning*\x90\x01\n\x10EnumNetworkOwner\x12\x10\n\x0cDEPRECATED_1\x10\x00\x12\x10\n\x0cDEPRECATED_2\x10\x01\x12\x10\n\x0cDEPRECATED_3\x10\x02\x12\x10\n\x0cDEPRECATED_4\x10\x03\x12\x10\n\x0cDEPRECATED_5\x10\x04\x12\x10\n\x0cDEPRECATED_6\x10\x08\x12\x10\n\x0cDEPRECATED_7\x10\x10*\xb5\x03\n\x10EnumProvisioning\x12\x18\n\x14PROVISIONING_UNKNOWN\x10\x00\x12\x1e\n\x1aPROVISIONING_NEVER_STARTED\x10\x01\x12\x18\n\x14PROVISIONING_STARTED\x10\x02\x12"\n\x1ePROVISIONING_ABORTED_BY_SYSTEM\x10\x03\x12"\n\x1ePROVISIONING_CANCELLED_BY_USER\x10\x04\x12\x1f\n\x1bPROVISIONING_SUCCESS_NEW_AP\x10\x05\x12\x1f\n\x1bPROVISIONING_SUCCESS_OLD_AP\x10\x06\x12*\n&PROVISIONING_ERROR_FAILED_TO_ASSOCIATE\x10\x07\x12$\n PROVISIONING_ERROR_PASSWORD_AUTH\x10\x08\x12$\n PROVISIONING_ERROR_EULA_BLOCKING\x10\t\x12"\n\x1ePROVISIONING_ERROR_NO_INTERNET\x10\n\x12\'\n#PROVISIONING_ERROR_UNSUPPORTED_TYPE\x10\x0b*\xac\x01\n\x0cEnumScanning\x12\x14\n\x10SCANNING_UNKNOWN\x10\x00\x12\x1a\n\x16SCANNING_NEVER_STARTED\x10\x01\x12\x14\n\x10SCANNING_STARTED\x10\x02\x12\x1e\n\x1aSCANNING_ABORTED_BY_SYSTEM\x10\x03\x12\x1e\n\x1aSCANNING_CANCELLED_BY_USER\x10\x04\x12\x14\n\x10SCANNING_SUCCESS\x10\x05*\xc2\x01\n\x12EnumScanEntryFlags\x12\x12\n\x0eSCAN_FLAG_OPEN\x10\x00\x12\x1b\n\x17SCAN_FLAG_AUTHENTICATED\x10\x01\x12\x18\n\x14SCAN_FLAG_CONFIGURED\x10\x02\x12\x17\n\x13SCAN_FLAG_BEST_SSID\x10\x04\x12\x18\n\x14SCAN_FLAG_ASSOCIATED\x10\x08\x12\x1e\n\x1aSCAN_FLAG_UNSUPPORTED_TYPE\x10\x10\x12\x0e\n\nDEPRECATED\x10 '
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "network_management_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ENUMNETWORKOWNER._serialized_start = 1463
    _ENUMNETWORKOWNER._serialized_end = 1607
    _ENUMPROVISIONING._serialized_start = 1610
    _ENUMPROVISIONING._serialized_end = 2047
    _ENUMSCANNING._serialized_start = 2050
    _ENUMSCANNING._serialized_end = 2222
    _ENUMSCANENTRYFLAGS._serialized_start = 2225
    _ENUMSCANENTRYFLAGS._serialized_end = 2419
    _NOTIFPROVISIONINGSTATE._serialized_start = 64
    _NOTIFPROVISIONINGSTATE._serialized_end = 146
    _NOTIFSTARTSCANNING._serialized_start = 149
    _NOTIFSTARTSCANNING._serialized_end = 290
    _REQUESTCONNECT._serialized_start = 292
    _REQUESTCONNECT._serialized_end = 375
    _REQUESTCONNECTNEW._serialized_start = 378
    _REQUESTCONNECTNEW._serialized_end = 613
    _REQUESTGETAPENTRIES._serialized_start = 615
    _REQUESTGETAPENTRIES._serialized_end = 695
    _REQUESTRELEASENETWORK._serialized_start = 697
    _REQUESTRELEASENETWORK._serialized_end = 720
    _REQUESTSTARTSCAN._serialized_start = 722
    _REQUESTSTARTSCAN._serialized_end = 740
    _RESPONSECONNECT._serialized_start = 743
    _RESPONSECONNECT._serialized_end = 890
    _RESPONSECONNECTNEW._serialized_start = 893
    _RESPONSECONNECTNEW._serialized_end = 1043
    _SCANENTRY._serialized_start = 1046
    _SCANENTRY._serialized_end = 1210
    _RESPONSEGETAPENTRIES._serialized_start = 1212
    _RESPONSEGETAPENTRIES._serialized_end = 1338
    _RESPONSESTARTSCANNING._serialized_start = 1340
    _RESPONSESTARTSCANNING._serialized_end = 1460
