# test_parsers.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:06 UTC 2023

from typing import cast

from open_gopro.api.ble_commands import BleCommands
from open_gopro.api.parsers import ByteParserBuilders
from open_gopro.communicator_interface import GoProBle
from open_gopro.constants import CmdId
from open_gopro.models.response import GlobalParsers
from open_gopro.parser_interface import Parser
from open_gopro.proto import EnumResultGeneric, ResponseGetApEntries


def test_version_response(mock_ble_communicator: GoProBle):
    BleCommands(mock_ble_communicator)
    parser = GlobalParsers.get_parser(CmdId.GET_THIRD_PARTY_API_VERSION)
    builder = parser.byte_json_adapter.build
    raw_bytes = builder({"major": 1, "minor": 2})
    assert parser.parse(raw_bytes) == "1.2"


def test_recursive_protobuf_proxying():
    scan1 = ResponseGetApEntries.ScanEntry(
        ssid="one", signal_strength_bars=0, signal_frequency_mhz=0, scan_entry_flags=0
    )
    scan2 = ResponseGetApEntries.ScanEntry(
        ssid="two", signal_strength_bars=0, signal_frequency_mhz=0, scan_entry_flags=0
    )
    response = ResponseGetApEntries(result=EnumResultGeneric.RESULT_SUCCESS, scan_id=1, entries=[scan1, scan2])
    raw = response.SerializeToString()
    parser = Parser[ResponseGetApEntries](byte_json_adapter=ByteParserBuilders.Protobuf(ResponseGetApEntries))
    parsed = parser.parse(raw)
    assert len(parsed.entries) == 2
    assert parsed.entries[0].ssid == "one"
    assert parsed.entries[1].ssid == "two"
