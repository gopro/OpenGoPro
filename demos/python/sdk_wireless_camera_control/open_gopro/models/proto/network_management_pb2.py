# network_management_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Jun  6 17:50:57 UTC 2025

"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x18network_management.proto\x12\nopen_gopro\x1a\x16response_generic.proto"R\n\x16NotifProvisioningState\x128\n\x12provisioning_state\x18\x01 \x02(\x0e2\x1c.open_gopro.EnumProvisioning"\x8d\x01\n\x12NotifStartScanning\x120\n\x0escanning_state\x18\x01 \x02(\x0e2\x18.open_gopro.EnumScanning\x12\x0f\n\x07scan_id\x18\x02 \x01(\x05\x12\x15\n\rtotal_entries\x18\x03 \x01(\x05\x12\x1d\n\x15total_configured_ssid\x18\x04 \x02(\x05"\x1e\n\x0eRequestConnect\x12\x0c\n\x04ssid\x18\x01 \x02(\t"\xae\x01\n\x11RequestConnectNew\x12\x0c\n\x04ssid\x18\x01 \x02(\t\x12\x10\n\x08password\x18\x02 \x02(\t\x12\x11\n\tstatic_ip\x18\x03 \x01(\x0c\x12\x0f\n\x07gateway\x18\x04 \x01(\x0c\x12\x0e\n\x06subnet\x18\x05 \x01(\x0c\x12\x13\n\x0bdns_primary\x18\x06 \x01(\x0c\x12\x15\n\rdns_secondary\x18\x07 \x01(\x0c\x12\x19\n\x11bypass_eula_check\x18\n \x01(\x08"P\n\x13RequestGetApEntries\x12\x13\n\x0bstart_index\x18\x01 \x02(\x05\x12\x13\n\x0bmax_entries\x18\x02 \x02(\x05\x12\x0f\n\x07scan_id\x18\x03 \x02(\x05"\x17\n\x15RequestReleaseNetwork"\x12\n\x10RequestStartScan"\x93\x01\n\x0fResponseConnect\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x128\n\x12provisioning_state\x18\x02 \x02(\x0e2\x1c.open_gopro.EnumProvisioning\x12\x17\n\x0ftimeout_seconds\x18\x03 \x02(\x05"\x96\x01\n\x12ResponseConnectNew\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x128\n\x12provisioning_state\x18\x02 \x02(\x0e2\x1c.open_gopro.EnumProvisioning\x12\x17\n\x0ftimeout_seconds\x18\x03 \x02(\x05"\x84\x02\n\x14ResponseGetApEntries\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x12\x0f\n\x07scan_id\x18\x02 \x02(\x05\x12;\n\x07entries\x18\x03 \x03(\x0b2*.open_gopro.ResponseGetApEntries.ScanEntry\x1ao\n\tScanEntry\x12\x0c\n\x04ssid\x18\x01 \x02(\t\x12\x1c\n\x14signal_strength_bars\x18\x02 \x02(\x05\x12\x1c\n\x14signal_frequency_mhz\x18\x04 \x02(\x05\x12\x18\n\x10scan_entry_flags\x18\x05 \x02(\x05"x\n\x15ResponseStartScanning\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x120\n\x0escanning_state\x18\x02 \x02(\x0e2\x18.open_gopro.EnumScanning"]\n\x14RequestPairingFinish\x122\n\x06result\x18\x01 \x02(\x0e2".open_gopro.EnumPairingFinishState\x12\x11\n\tphoneName\x18\x02 \x02(\t*\xb5\x03\n\x10EnumProvisioning\x12\x18\n\x14PROVISIONING_UNKNOWN\x10\x00\x12\x1e\n\x1aPROVISIONING_NEVER_STARTED\x10\x01\x12\x18\n\x14PROVISIONING_STARTED\x10\x02\x12"\n\x1ePROVISIONING_ABORTED_BY_SYSTEM\x10\x03\x12"\n\x1ePROVISIONING_CANCELLED_BY_USER\x10\x04\x12\x1f\n\x1bPROVISIONING_SUCCESS_NEW_AP\x10\x05\x12\x1f\n\x1bPROVISIONING_SUCCESS_OLD_AP\x10\x06\x12*\n&PROVISIONING_ERROR_FAILED_TO_ASSOCIATE\x10\x07\x12$\n PROVISIONING_ERROR_PASSWORD_AUTH\x10\x08\x12$\n PROVISIONING_ERROR_EULA_BLOCKING\x10\t\x12"\n\x1ePROVISIONING_ERROR_NO_INTERNET\x10\n\x12\'\n#PROVISIONING_ERROR_UNSUPPORTED_TYPE\x10\x0b*\xac\x01\n\x0cEnumScanning\x12\x14\n\x10SCANNING_UNKNOWN\x10\x00\x12\x1a\n\x16SCANNING_NEVER_STARTED\x10\x01\x12\x14\n\x10SCANNING_STARTED\x10\x02\x12\x1e\n\x1aSCANNING_ABORTED_BY_SYSTEM\x10\x03\x12\x1e\n\x1aSCANNING_CANCELLED_BY_USER\x10\x04\x12\x14\n\x10SCANNING_SUCCESS\x10\x05*\xb2\x01\n\x12EnumScanEntryFlags\x12\x12\n\x0eSCAN_FLAG_OPEN\x10\x00\x12\x1b\n\x17SCAN_FLAG_AUTHENTICATED\x10\x01\x12\x18\n\x14SCAN_FLAG_CONFIGURED\x10\x02\x12\x17\n\x13SCAN_FLAG_BEST_SSID\x10\x04\x12\x18\n\x14SCAN_FLAG_ASSOCIATED\x10\x08\x12\x1e\n\x1aSCAN_FLAG_UNSUPPORTED_TYPE\x10\x10*1\n\x16EnumPairingFinishState\x12\x0b\n\x07SUCCESS\x10\x00\x12\n\n\x06FAILED\x10\x01'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "network_management_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ENUMPROVISIONING._serialized_start = 1412
    _ENUMPROVISIONING._serialized_end = 1849
    _ENUMSCANNING._serialized_start = 1852
    _ENUMSCANNING._serialized_end = 2024
    _ENUMSCANENTRYFLAGS._serialized_start = 2027
    _ENUMSCANENTRYFLAGS._serialized_end = 2205
    _ENUMPAIRINGFINISHSTATE._serialized_start = 2207
    _ENUMPAIRINGFINISHSTATE._serialized_end = 2256
    _NOTIFPROVISIONINGSTATE._serialized_start = 64
    _NOTIFPROVISIONINGSTATE._serialized_end = 146
    _NOTIFSTARTSCANNING._serialized_start = 149
    _NOTIFSTARTSCANNING._serialized_end = 290
    _REQUESTCONNECT._serialized_start = 292
    _REQUESTCONNECT._serialized_end = 322
    _REQUESTCONNECTNEW._serialized_start = 325
    _REQUESTCONNECTNEW._serialized_end = 499
    _REQUESTGETAPENTRIES._serialized_start = 501
    _REQUESTGETAPENTRIES._serialized_end = 581
    _REQUESTRELEASENETWORK._serialized_start = 583
    _REQUESTRELEASENETWORK._serialized_end = 606
    _REQUESTSTARTSCAN._serialized_start = 608
    _REQUESTSTARTSCAN._serialized_end = 626
    _RESPONSECONNECT._serialized_start = 629
    _RESPONSECONNECT._serialized_end = 776
    _RESPONSECONNECTNEW._serialized_start = 779
    _RESPONSECONNECTNEW._serialized_end = 929
    _RESPONSEGETAPENTRIES._serialized_start = 932
    _RESPONSEGETAPENTRIES._serialized_end = 1192
    _RESPONSEGETAPENTRIES_SCANENTRY._serialized_start = 1081
    _RESPONSEGETAPENTRIES_SCANENTRY._serialized_end = 1192
    _RESPONSESTARTSCANNING._serialized_start = 1194
    _RESPONSESTARTSCANNING._serialized_end = 1314
    _REQUESTPAIRINGFINISH._serialized_start = 1316
    _REQUESTPAIRINGFINISH._serialized_end = 1409
