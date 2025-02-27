# network_management_pb2.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Feb 21 18:05:41 UTC 2025

import sys

_b = ((sys.version_info[0] < 3) and (lambda x: x)) or (lambda x: x.encode("latin1"))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="network_management.proto",
    package="open_gopro",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n\x18network_management.proto\x12\nopen_gopro\x1a\x16response_generic.proto"R\n\x16NotifProvisioningState\x128\n\x12provisioning_state\x18\x01 \x02(\x0e2\x1c.open_gopro.EnumProvisioning"\x8d\x01\n\x12NotifStartScanning\x120\n\x0escanning_state\x18\x01 \x02(\x0e2\x18.open_gopro.EnumScanning\x12\x0f\n\x07scan_id\x18\x02 \x01(\x05\x12\x15\n\rtotal_entries\x18\x03 \x01(\x05\x12\x1d\n\x15total_configured_ssid\x18\x04 \x02(\x05"\x1e\n\x0eRequestConnect\x12\x0c\n\x04ssid\x18\x01 \x02(\t"\x93\x01\n\x11RequestConnectNew\x12\x0c\n\x04ssid\x18\x01 \x02(\t\x12\x10\n\x08password\x18\x02 \x02(\t\x12\x11\n\tstatic_ip\x18\x03 \x01(\x0c\x12\x0f\n\x07gateway\x18\x04 \x01(\x0c\x12\x0e\n\x06subnet\x18\x05 \x01(\x0c\x12\x13\n\x0bdns_primary\x18\x06 \x01(\x0c\x12\x15\n\rdns_secondary\x18\x07 \x01(\x0c"P\n\x13RequestGetApEntries\x12\x13\n\x0bstart_index\x18\x01 \x02(\x05\x12\x13\n\x0bmax_entries\x18\x02 \x02(\x05\x12\x0f\n\x07scan_id\x18\x03 \x02(\x05"\x17\n\x15RequestReleaseNetwork"\x12\n\x10RequestStartScan"\x93\x01\n\x0fResponseConnect\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x128\n\x12provisioning_state\x18\x02 \x02(\x0e2\x1c.open_gopro.EnumProvisioning\x12\x17\n\x0ftimeout_seconds\x18\x03 \x02(\x05"\x96\x01\n\x12ResponseConnectNew\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x128\n\x12provisioning_state\x18\x02 \x02(\x0e2\x1c.open_gopro.EnumProvisioning\x12\x17\n\x0ftimeout_seconds\x18\x03 \x02(\x05"\x84\x02\n\x14ResponseGetApEntries\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x12\x0f\n\x07scan_id\x18\x02 \x02(\x05\x12;\n\x07entries\x18\x03 \x03(\x0b2*.open_gopro.ResponseGetApEntries.ScanEntry\x1ao\n\tScanEntry\x12\x0c\n\x04ssid\x18\x01 \x02(\t\x12\x1c\n\x14signal_strength_bars\x18\x02 \x02(\x05\x12\x1c\n\x14signal_frequency_mhz\x18\x04 \x02(\x05\x12\x18\n\x10scan_entry_flags\x18\x05 \x02(\x05"x\n\x15ResponseStartScanning\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x120\n\x0escanning_state\x18\x02 \x02(\x0e2\x18.open_gopro.EnumScanning*µ\x03\n\x10EnumProvisioning\x12\x18\n\x14PROVISIONING_UNKNOWN\x10\x00\x12\x1e\n\x1aPROVISIONING_NEVER_STARTED\x10\x01\x12\x18\n\x14PROVISIONING_STARTED\x10\x02\x12"\n\x1ePROVISIONING_ABORTED_BY_SYSTEM\x10\x03\x12"\n\x1ePROVISIONING_CANCELLED_BY_USER\x10\x04\x12\x1f\n\x1bPROVISIONING_SUCCESS_NEW_AP\x10\x05\x12\x1f\n\x1bPROVISIONING_SUCCESS_OLD_AP\x10\x06\x12*\n&PROVISIONING_ERROR_FAILED_TO_ASSOCIATE\x10\x07\x12$\n PROVISIONING_ERROR_PASSWORD_AUTH\x10\x08\x12$\n PROVISIONING_ERROR_EULA_BLOCKING\x10\t\x12"\n\x1ePROVISIONING_ERROR_NO_INTERNET\x10\n\x12\'\n#PROVISIONING_ERROR_UNSUPPORTED_TYPE\x10\x0b*¬\x01\n\x0cEnumScanning\x12\x14\n\x10SCANNING_UNKNOWN\x10\x00\x12\x1a\n\x16SCANNING_NEVER_STARTED\x10\x01\x12\x14\n\x10SCANNING_STARTED\x10\x02\x12\x1e\n\x1aSCANNING_ABORTED_BY_SYSTEM\x10\x03\x12\x1e\n\x1aSCANNING_CANCELLED_BY_USER\x10\x04\x12\x14\n\x10SCANNING_SUCCESS\x10\x05*²\x01\n\x12EnumScanEntryFlags\x12\x12\n\x0eSCAN_FLAG_OPEN\x10\x00\x12\x1b\n\x17SCAN_FLAG_AUTHENTICATED\x10\x01\x12\x18\n\x14SCAN_FLAG_CONFIGURED\x10\x02\x12\x17\n\x13SCAN_FLAG_BEST_SSID\x10\x04\x12\x18\n\x14SCAN_FLAG_ASSOCIATED\x10\x08\x12\x1e\n\x1aSCAN_FLAG_UNSUPPORTED_TYPE\x10\x10'
    ),
    dependencies=[response__generic__pb2.DESCRIPTOR],
)
_ENUMPROVISIONING = _descriptor.EnumDescriptor(
    name="EnumProvisioning",
    full_name="open_gopro.EnumProvisioning",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_UNKNOWN", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_NEVER_STARTED", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_STARTED", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_ABORTED_BY_SYSTEM", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_CANCELLED_BY_USER", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_SUCCESS_NEW_AP", index=5, number=5, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_SUCCESS_OLD_AP", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_ERROR_FAILED_TO_ASSOCIATE", index=7, number=7, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_ERROR_PASSWORD_AUTH", index=8, number=8, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_ERROR_EULA_BLOCKING", index=9, number=9, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_ERROR_NO_INTERNET", index=10, number=10, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="PROVISIONING_ERROR_UNSUPPORTED_TYPE", index=11, number=11, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1290,
    serialized_end=1727,
)
_sym_db.RegisterEnumDescriptor(_ENUMPROVISIONING)
EnumProvisioning = enum_type_wrapper.EnumTypeWrapper(_ENUMPROVISIONING)
_ENUMSCANNING = _descriptor.EnumDescriptor(
    name="EnumScanning",
    full_name="open_gopro.EnumScanning",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(name="SCANNING_UNKNOWN", index=0, number=0, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="SCANNING_NEVER_STARTED", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(name="SCANNING_STARTED", index=2, number=2, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="SCANNING_ABORTED_BY_SYSTEM", index=3, number=3, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SCANNING_CANCELLED_BY_USER", index=4, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(name="SCANNING_SUCCESS", index=5, number=5, serialized_options=None, type=None),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1730,
    serialized_end=1902,
)
_sym_db.RegisterEnumDescriptor(_ENUMSCANNING)
EnumScanning = enum_type_wrapper.EnumTypeWrapper(_ENUMSCANNING)
_ENUMSCANENTRYFLAGS = _descriptor.EnumDescriptor(
    name="EnumScanEntryFlags",
    full_name="open_gopro.EnumScanEntryFlags",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(name="SCAN_FLAG_OPEN", index=0, number=0, serialized_options=None, type=None),
        _descriptor.EnumValueDescriptor(
            name="SCAN_FLAG_AUTHENTICATED", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SCAN_FLAG_CONFIGURED", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SCAN_FLAG_BEST_SSID", index=3, number=4, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SCAN_FLAG_ASSOCIATED", index=4, number=8, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SCAN_FLAG_UNSUPPORTED_TYPE", index=5, number=16, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1905,
    serialized_end=2083,
)
_sym_db.RegisterEnumDescriptor(_ENUMSCANENTRYFLAGS)
EnumScanEntryFlags = enum_type_wrapper.EnumTypeWrapper(_ENUMSCANENTRYFLAGS)
PROVISIONING_UNKNOWN = 0
PROVISIONING_NEVER_STARTED = 1
PROVISIONING_STARTED = 2
PROVISIONING_ABORTED_BY_SYSTEM = 3
PROVISIONING_CANCELLED_BY_USER = 4
PROVISIONING_SUCCESS_NEW_AP = 5
PROVISIONING_SUCCESS_OLD_AP = 6
PROVISIONING_ERROR_FAILED_TO_ASSOCIATE = 7
PROVISIONING_ERROR_PASSWORD_AUTH = 8
PROVISIONING_ERROR_EULA_BLOCKING = 9
PROVISIONING_ERROR_NO_INTERNET = 10
PROVISIONING_ERROR_UNSUPPORTED_TYPE = 11
SCANNING_UNKNOWN = 0
SCANNING_NEVER_STARTED = 1
SCANNING_STARTED = 2
SCANNING_ABORTED_BY_SYSTEM = 3
SCANNING_CANCELLED_BY_USER = 4
SCANNING_SUCCESS = 5
SCAN_FLAG_OPEN = 0
SCAN_FLAG_AUTHENTICATED = 1
SCAN_FLAG_CONFIGURED = 2
SCAN_FLAG_BEST_SSID = 4
SCAN_FLAG_ASSOCIATED = 8
SCAN_FLAG_UNSUPPORTED_TYPE = 16
_NOTIFPROVISIONINGSTATE = _descriptor.Descriptor(
    name="NotifProvisioningState",
    full_name="open_gopro.NotifProvisioningState",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="provisioning_state",
            full_name="open_gopro.NotifProvisioningState.provisioning_state",
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
    serialized_start=64,
    serialized_end=146,
)
_NOTIFSTARTSCANNING = _descriptor.Descriptor(
    name="NotifStartScanning",
    full_name="open_gopro.NotifStartScanning",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="scanning_state",
            full_name="open_gopro.NotifStartScanning.scanning_state",
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
        ),
        _descriptor.FieldDescriptor(
            name="scan_id",
            full_name="open_gopro.NotifStartScanning.scan_id",
            index=1,
            number=2,
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
            name="total_entries",
            full_name="open_gopro.NotifStartScanning.total_entries",
            index=2,
            number=3,
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
            name="total_configured_ssid",
            full_name="open_gopro.NotifStartScanning.total_configured_ssid",
            index=3,
            number=4,
            type=5,
            cpp_type=1,
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
    serialized_start=149,
    serialized_end=290,
)
_REQUESTCONNECT = _descriptor.Descriptor(
    name="RequestConnect",
    full_name="open_gopro.RequestConnect",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="ssid",
            full_name="open_gopro.RequestConnect.ssid",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=2,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
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
    serialized_start=292,
    serialized_end=322,
)
_REQUESTCONNECTNEW = _descriptor.Descriptor(
    name="RequestConnectNew",
    full_name="open_gopro.RequestConnectNew",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="ssid",
            full_name="open_gopro.RequestConnectNew.ssid",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=2,
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
            full_name="open_gopro.RequestConnectNew.password",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=2,
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
            name="static_ip",
            full_name="open_gopro.RequestConnectNew.static_ip",
            index=2,
            number=3,
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
            name="gateway",
            full_name="open_gopro.RequestConnectNew.gateway",
            index=3,
            number=4,
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
            name="subnet",
            full_name="open_gopro.RequestConnectNew.subnet",
            index=4,
            number=5,
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
            name="dns_primary",
            full_name="open_gopro.RequestConnectNew.dns_primary",
            index=5,
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
            name="dns_secondary",
            full_name="open_gopro.RequestConnectNew.dns_secondary",
            index=6,
            number=7,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=325,
    serialized_end=472,
)
_REQUESTGETAPENTRIES = _descriptor.Descriptor(
    name="RequestGetApEntries",
    full_name="open_gopro.RequestGetApEntries",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="start_index",
            full_name="open_gopro.RequestGetApEntries.start_index",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
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
        ),
        _descriptor.FieldDescriptor(
            name="max_entries",
            full_name="open_gopro.RequestGetApEntries.max_entries",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
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
        ),
        _descriptor.FieldDescriptor(
            name="scan_id",
            full_name="open_gopro.RequestGetApEntries.scan_id",
            index=2,
            number=3,
            type=5,
            cpp_type=1,
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
    serialized_start=474,
    serialized_end=554,
)
_REQUESTRELEASENETWORK = _descriptor.Descriptor(
    name="RequestReleaseNetwork",
    full_name="open_gopro.RequestReleaseNetwork",
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
    serialized_start=556,
    serialized_end=579,
)
_REQUESTSTARTSCAN = _descriptor.Descriptor(
    name="RequestStartScan",
    full_name="open_gopro.RequestStartScan",
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
    serialized_start=581,
    serialized_end=599,
)
_RESPONSECONNECT = _descriptor.Descriptor(
    name="ResponseConnect",
    full_name="open_gopro.ResponseConnect",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="result",
            full_name="open_gopro.ResponseConnect.result",
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
        ),
        _descriptor.FieldDescriptor(
            name="provisioning_state",
            full_name="open_gopro.ResponseConnect.provisioning_state",
            index=1,
            number=2,
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
        ),
        _descriptor.FieldDescriptor(
            name="timeout_seconds",
            full_name="open_gopro.ResponseConnect.timeout_seconds",
            index=2,
            number=3,
            type=5,
            cpp_type=1,
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
    serialized_start=602,
    serialized_end=749,
)
_RESPONSECONNECTNEW = _descriptor.Descriptor(
    name="ResponseConnectNew",
    full_name="open_gopro.ResponseConnectNew",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="result",
            full_name="open_gopro.ResponseConnectNew.result",
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
        ),
        _descriptor.FieldDescriptor(
            name="provisioning_state",
            full_name="open_gopro.ResponseConnectNew.provisioning_state",
            index=1,
            number=2,
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
        ),
        _descriptor.FieldDescriptor(
            name="timeout_seconds",
            full_name="open_gopro.ResponseConnectNew.timeout_seconds",
            index=2,
            number=3,
            type=5,
            cpp_type=1,
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
    serialized_start=752,
    serialized_end=902,
)
_RESPONSEGETAPENTRIES_SCANENTRY = _descriptor.Descriptor(
    name="ScanEntry",
    full_name="open_gopro.ResponseGetApEntries.ScanEntry",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="ssid",
            full_name="open_gopro.ResponseGetApEntries.ScanEntry.ssid",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=2,
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
            name="signal_strength_bars",
            full_name="open_gopro.ResponseGetApEntries.ScanEntry.signal_strength_bars",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
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
        ),
        _descriptor.FieldDescriptor(
            name="signal_frequency_mhz",
            full_name="open_gopro.ResponseGetApEntries.ScanEntry.signal_frequency_mhz",
            index=2,
            number=4,
            type=5,
            cpp_type=1,
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
        ),
        _descriptor.FieldDescriptor(
            name="scan_entry_flags",
            full_name="open_gopro.ResponseGetApEntries.ScanEntry.scan_entry_flags",
            index=3,
            number=5,
            type=5,
            cpp_type=1,
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
    serialized_start=1054,
    serialized_end=1165,
)
_RESPONSEGETAPENTRIES = _descriptor.Descriptor(
    name="ResponseGetApEntries",
    full_name="open_gopro.ResponseGetApEntries",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="result",
            full_name="open_gopro.ResponseGetApEntries.result",
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
        ),
        _descriptor.FieldDescriptor(
            name="scan_id",
            full_name="open_gopro.ResponseGetApEntries.scan_id",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
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
        ),
        _descriptor.FieldDescriptor(
            name="entries",
            full_name="open_gopro.ResponseGetApEntries.entries",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
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
    nested_types=[_RESPONSEGETAPENTRIES_SCANENTRY],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=905,
    serialized_end=1165,
)
_RESPONSESTARTSCANNING = _descriptor.Descriptor(
    name="ResponseStartScanning",
    full_name="open_gopro.ResponseStartScanning",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="result",
            full_name="open_gopro.ResponseStartScanning.result",
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
        ),
        _descriptor.FieldDescriptor(
            name="scanning_state",
            full_name="open_gopro.ResponseStartScanning.scanning_state",
            index=1,
            number=2,
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
    serialized_start=1167,
    serialized_end=1287,
)
_NOTIFPROVISIONINGSTATE.fields_by_name["provisioning_state"].enum_type = _ENUMPROVISIONING
_NOTIFSTARTSCANNING.fields_by_name["scanning_state"].enum_type = _ENUMSCANNING
_RESPONSECONNECT.fields_by_name["result"].enum_type = response__generic__pb2._ENUMRESULTGENERIC
_RESPONSECONNECT.fields_by_name["provisioning_state"].enum_type = _ENUMPROVISIONING
_RESPONSECONNECTNEW.fields_by_name["result"].enum_type = response__generic__pb2._ENUMRESULTGENERIC
_RESPONSECONNECTNEW.fields_by_name["provisioning_state"].enum_type = _ENUMPROVISIONING
_RESPONSEGETAPENTRIES_SCANENTRY.containing_type = _RESPONSEGETAPENTRIES
_RESPONSEGETAPENTRIES.fields_by_name["result"].enum_type = response__generic__pb2._ENUMRESULTGENERIC
_RESPONSEGETAPENTRIES.fields_by_name["entries"].message_type = _RESPONSEGETAPENTRIES_SCANENTRY
_RESPONSESTARTSCANNING.fields_by_name["result"].enum_type = response__generic__pb2._ENUMRESULTGENERIC
_RESPONSESTARTSCANNING.fields_by_name["scanning_state"].enum_type = _ENUMSCANNING
DESCRIPTOR.message_types_by_name["NotifProvisioningState"] = _NOTIFPROVISIONINGSTATE
DESCRIPTOR.message_types_by_name["NotifStartScanning"] = _NOTIFSTARTSCANNING
DESCRIPTOR.message_types_by_name["RequestConnect"] = _REQUESTCONNECT
DESCRIPTOR.message_types_by_name["RequestConnectNew"] = _REQUESTCONNECTNEW
DESCRIPTOR.message_types_by_name["RequestGetApEntries"] = _REQUESTGETAPENTRIES
DESCRIPTOR.message_types_by_name["RequestReleaseNetwork"] = _REQUESTRELEASENETWORK
DESCRIPTOR.message_types_by_name["RequestStartScan"] = _REQUESTSTARTSCAN
DESCRIPTOR.message_types_by_name["ResponseConnect"] = _RESPONSECONNECT
DESCRIPTOR.message_types_by_name["ResponseConnectNew"] = _RESPONSECONNECTNEW
DESCRIPTOR.message_types_by_name["ResponseGetApEntries"] = _RESPONSEGETAPENTRIES
DESCRIPTOR.message_types_by_name["ResponseStartScanning"] = _RESPONSESTARTSCANNING
DESCRIPTOR.enum_types_by_name["EnumProvisioning"] = _ENUMPROVISIONING
DESCRIPTOR.enum_types_by_name["EnumScanning"] = _ENUMSCANNING
DESCRIPTOR.enum_types_by_name["EnumScanEntryFlags"] = _ENUMSCANENTRYFLAGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
NotifProvisioningState = _reflection.GeneratedProtocolMessageType(
    "NotifProvisioningState",
    (_message.Message,),
    dict(DESCRIPTOR=_NOTIFPROVISIONINGSTATE, __module__="network_management_pb2"),
)
_sym_db.RegisterMessage(NotifProvisioningState)
NotifStartScanning = _reflection.GeneratedProtocolMessageType(
    "NotifStartScanning", (_message.Message,), dict(DESCRIPTOR=_NOTIFSTARTSCANNING, __module__="network_management_pb2")
)
_sym_db.RegisterMessage(NotifStartScanning)
RequestConnect = _reflection.GeneratedProtocolMessageType(
    "RequestConnect", (_message.Message,), dict(DESCRIPTOR=_REQUESTCONNECT, __module__="network_management_pb2")
)
_sym_db.RegisterMessage(RequestConnect)
RequestConnectNew = _reflection.GeneratedProtocolMessageType(
    "RequestConnectNew", (_message.Message,), dict(DESCRIPTOR=_REQUESTCONNECTNEW, __module__="network_management_pb2")
)
_sym_db.RegisterMessage(RequestConnectNew)
RequestGetApEntries = _reflection.GeneratedProtocolMessageType(
    "RequestGetApEntries",
    (_message.Message,),
    dict(DESCRIPTOR=_REQUESTGETAPENTRIES, __module__="network_management_pb2"),
)
_sym_db.RegisterMessage(RequestGetApEntries)
RequestReleaseNetwork = _reflection.GeneratedProtocolMessageType(
    "RequestReleaseNetwork",
    (_message.Message,),
    dict(DESCRIPTOR=_REQUESTRELEASENETWORK, __module__="network_management_pb2"),
)
_sym_db.RegisterMessage(RequestReleaseNetwork)
RequestStartScan = _reflection.GeneratedProtocolMessageType(
    "RequestStartScan", (_message.Message,), dict(DESCRIPTOR=_REQUESTSTARTSCAN, __module__="network_management_pb2")
)
_sym_db.RegisterMessage(RequestStartScan)
ResponseConnect = _reflection.GeneratedProtocolMessageType(
    "ResponseConnect", (_message.Message,), dict(DESCRIPTOR=_RESPONSECONNECT, __module__="network_management_pb2")
)
_sym_db.RegisterMessage(ResponseConnect)
ResponseConnectNew = _reflection.GeneratedProtocolMessageType(
    "ResponseConnectNew", (_message.Message,), dict(DESCRIPTOR=_RESPONSECONNECTNEW, __module__="network_management_pb2")
)
_sym_db.RegisterMessage(ResponseConnectNew)
ResponseGetApEntries = _reflection.GeneratedProtocolMessageType(
    "ResponseGetApEntries",
    (_message.Message,),
    dict(
        ScanEntry=_reflection.GeneratedProtocolMessageType(
            "ScanEntry",
            (_message.Message,),
            dict(DESCRIPTOR=_RESPONSEGETAPENTRIES_SCANENTRY, __module__="network_management_pb2"),
        ),
        DESCRIPTOR=_RESPONSEGETAPENTRIES,
        __module__="network_management_pb2",
    ),
)
_sym_db.RegisterMessage(ResponseGetApEntries)
_sym_db.RegisterMessage(ResponseGetApEntries.ScanEntry)
ResponseStartScanning = _reflection.GeneratedProtocolMessageType(
    "ResponseStartScanning",
    (_message.Message,),
    dict(DESCRIPTOR=_RESPONSESTARTSCANNING, __module__="network_management_pb2"),
)
_sym_db.RegisterMessage(ResponseStartScanning)
