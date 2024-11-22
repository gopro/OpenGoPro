# test_parsers.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:06 UTC 2023

from open_gopro.api.ble_commands import BleCommands
from open_gopro.api.parsers import ByteParserBuilders
from open_gopro.communicator_interface import GoProBle
from open_gopro.constants import CmdId
from open_gopro.models.ble_advertisement import adv_data_struct, scan_response_struct
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


def test_ble_advertisement_parsing():
    # GIVEN
    adv_data = bytes(
        [
            0x02,
            0x01,
            0x02,
            0x03,
            0x02,
            0xA6,
            0xFE,
            0x0F,
            0xFF,
            0xF2,
            0x02,
            0x02,
            0x01,
            0x38,
            0x33,
            0x00,
            0xB3,
            0xFE,
            0x2A,
            0x79,
            0xDC,
            0xEB,
            0x0F,
        ]
    )

    # WHEN
    adv = adv_data_struct.parse(adv_data)
    manuf_data = adv.manuf_data
    camera_status = manuf_data.camera_status
    camera_capabilities = manuf_data.camera_capabilities
    media_offload_status = manuf_data.media_offload_status

    # THEN
    assert adv.flags == 0x0102
    assert adv.uuids == 0xFEA6
    assert adv.manuf_type == 0xFF
    assert adv.company_id == 0xF202

    assert manuf_data.schema_version == 2
    assert manuf_data.camera_id == 56
    assert manuf_data.id_hash == "b3:fe:2a:79:dc:eb"

    assert camera_status.processor_state == False
    assert camera_status.wifi_ap_state == False
    assert camera_status.peripheral_pairing_state == False
    assert camera_status.central_role_enabled == False
    assert camera_status.is_new_media_available == False

    assert camera_capabilities.cnc == False
    assert camera_capabilities.ble_metadata == False
    assert camera_capabilities.wideband_audio == True
    assert camera_capabilities.concurrent_master_slave == True
    assert camera_capabilities.onboarding == False
    assert camera_capabilities.new_media_available == False

    assert media_offload_status.available == False
    assert media_offload_status.new_media_available == False
    assert media_offload_status.battery_ok == False
    assert media_offload_status.sd_card_ok == False
    assert media_offload_status.busy == True
    assert media_offload_status.paused == True


def test_ble_scan_response_parsing():
    # GIVEN
    scan_response_data = bytes(
        [
            0x0B,
            0x09,
            0x47,
            0x6F,
            0x50,
            0x72,
            0x6F,
            0x20,
            0x31,
            0x30,
            0x35,
            0x38,
            0x0B,
            0x16,
            0xA6,
            0xFE,
            0xF7,
            0xA9,
            0x76,
            0x88,
            0x31,
            0x30,
            0x35,
            0x38,
        ]
    )

    # WHEN
    scan_response = scan_response_struct.parse(scan_response_data)

    # THEN
    assert scan_response.name == "GoPro 1058"
    assert scan_response.service_type == 0x16
    assert scan_response.service_uuid == 0xFEA6
    assert scan_response.service_data.ap_mac_address == "f7:a9:76:88"
    assert scan_response.service_data.serial_number == "1058"
