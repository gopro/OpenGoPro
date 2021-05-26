# test_responses.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:51 UTC 2021

"""Test the responses module"""

import requests

import requests_mock

from open_gopro.constants import QueryCmdId, SettingId, StatusId, UUID
from open_gopro.responses import GoProResp
from open_gopro.ble_commands import BleCommands, Status

test_complex_write_send = bytes([0x01, 0x13])
test_complex_write_receive = bytes(
    [
        0x21,
        0x72,
        0x13,
        0x00,
        0x01,
        0x01,
        0x01,
        0x02,
        0x01,
        0x04,
        0x03,
        0x01,
        0x00,
        0x04,
        0x01,
        0xFF,
        0x06,
        0x01,
        0x00,
        0x08,
        0x80,
        0x01,
        0x00,
        0x09,
        0x01,
        0x00,
        0x0A,
        0x01,
        0x00,
        0x0B,
        0x01,
        0x00,
        0x0D,
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x0E,
        0x04,
        0x81,
        0x00,
        0x00,
        0x00,
        0x00,
        0x11,
        0x01,
        0x01,
        0x13,
        0x01,
        0x04,
        0x14,
        0x01,
        0x01,
        0x15,
        0x04,
        0x00,
        0x00,
        0x3E,
        0xA4,
        0x82,
        0x16,
        0x01,
        0x00,
        0x17,
        0x01,
        0x00,
        0x18,
        0x01,
        0x00,
        0x1A,
        0x01,
        0x00,
        0x1B,
        0x01,
        0x00,
        0x1C,
        0x01,
        0x52,
        0x1D,
        0x83,
        0x00,
        0x1E,
        0x0A,
        0x47,
        0x50,
        0x32,
        0x34,
        0x35,
        0x30,
        0x30,
        0x34,
        0x35,
        0x36,
        0x1F,
        0x01,
        0x00,
        0x20,
        0x01,
        0x01,
        0x84,
        0x21,
        0x01,
        0x00,
        0x22,
        0x04,
        0x00,
        0x00,
        0x08,
        0x73,
        0x23,
        0x04,
        0x00,
        0x00,
        0x0F,
        0xD6,
        0x24,
        0x04,
        0x00,
        0x00,
        0x85,
        0x00,
        0x40,
        0x25,
        0x04,
        0x00,
        0x00,
        0x00,
        0x35,
        0x26,
        0x04,
        0x00,
        0x00,
        0x00,
        0x40,
        0x27,
        0x04,
        0x00,
        0x00,
        0x00,
        0x86,
        0x35,
        0x28,
        0x12,
        0x25,
        0x31,
        0x42,
        0x25,
        0x30,
        0x34,
        0x25,
        0x30,
        0x36,
        0x25,
        0x30,
        0x37,
        0x25,
        0x33,
        0x31,
        0x25,
        0x87,
        0x30,
        0x44,
        0x29,
        0x01,
        0x00,
        0x2A,
        0x01,
        0x00,
        0x2D,
        0x01,
        0x00,
        0x31,
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x36,
        0x08,
        0x88,
        0x00,
        0x00,
        0x00,
        0x00,
        0x01,
        0x95,
        0x82,
        0x60,
        0x37,
        0x01,
        0x01,
        0x38,
        0x01,
        0x01,
        0x39,
        0x04,
        0x00,
        0x6E,
        0x2F,
        0x89,
        0x81,
        0x3A,
        0x01,
        0x00,
        0x3B,
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x3C,
        0x04,
        0x00,
        0x00,
        0x01,
        0xF4,
        0x3D,
        0x01,
        0x02,
        0x8A,
        0x3E,
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x3F,
        0x01,
        0x00,
        0x40,
        0x04,
        0x00,
        0x00,
        0x04,
        0x39,
        0x41,
        0x01,
        0x00,
        0x42,
        0x8B,
        0x01,
        0x64,
        0x43,
        0x01,
        0x64,
        0x44,
        0x01,
        0x00,
        0x45,
        0x01,
        0x01,
        0x46,
        0x01,
        0x35,
        0x4A,
        0x01,
        0x00,
        0x4B,
        0x01,
        0x8C,
        0x00,
        0x4C,
        0x01,
        0x01,
        0x4D,
        0x01,
        0x01,
        0x4E,
        0x01,
        0x00,
        0x4F,
        0x01,
        0x00,
        0x51,
        0x01,
        0x01,
        0x52,
        0x01,
        0x01,
        0x8D,
        0x53,
        0x01,
        0x01,
        0x55,
        0x01,
        0x00,
        0x56,
        0x01,
        0x00,
        0x58,
        0x01,
        0x00,
        0x59,
        0x01,
        0x0C,
        0x5A,
        0x01,
        0x01,
        0x5B,
        0x8E,
        0x01,
        0x00,
        0x5D,
        0x04,
        0x00,
        0x00,
        0x00,
        0x02,
        0x5E,
        0x04,
        0x00,
        0x01,
        0x00,
        0x00,
        0x5F,
        0x04,
        0x00,
        0x02,
        0x00,
        0x8F,
        0x00,
        0x60,
        0x04,
        0x00,
        0x00,
        0x03,
        0xE8,
        0x61,
        0x04,
        0x00,
        0x00,
        0x00,
        0x02,
        0x62,
        0x04,
        0x01,
        0x00,
        0x00,
        0x02,
        0x80,
        0x63,
        0x04,
        0x00,
        0x00,
        0x05,
        0x47,
        0x64,
        0x04,
        0x00,
        0x00,
        0x00,
        0x00,
        0x65,
        0x01,
        0x00,
        0x66,
        0x01,
        0x00,
        0x67,
        0x81,
        0x01,
        0x00,
        0x68,
        0x01,
        0x01,
        0x69,
        0x01,
        0x00,
        0x6A,
        0x01,
        0x00,
        0x6B,
        0x04,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0x6C,
        0x01,
        0x82,
        0x00,
        0x6D,
        0x01,
        0x00,
        0x6E,
        0x01,
        0x00,
        0x71,
        0x01,
        0x00,
    ]
)


def test_complex_write_command():
    r = GoProResp.from_write_command(UUID.CQ_QUERY, test_complex_write_send)

    idx = 0
    len(test_complex_write_receive)
    while not r.is_received:
        end = len(test_complex_write_receive) if idx + 20 > len(test_complex_write_receive) else idx + 20
        r._accumulate(test_complex_write_receive[idx:end])
        idx = end

    assert r.is_parsed
    assert r.is_received
    assert r.is_received
    assert r.is_ok
    assert r.id is QueryCmdId.GET_STATUS_VAL
    assert r.cmd is QueryCmdId.GET_STATUS_VAL
    assert r.uuid is UUID.CQ_QUERY_RESP
    assert StatusId.ENCODING in r
    # Test iterator
    for x in r:
        assert isinstance(x, StatusId)
    assert len(str(r)) > 0
    assert isinstance(r.flatten, dict)


test_push_receive_no_parameter = bytearray([0x08, 0xA2, 0x00, 0x02, 0x00, 0x03, 0x00, 0x79, 0x00])


def test_push_response_no_parameter_values():
    r = GoProResp([UUID.CQ_QUERY_RESP])
    r._accumulate(test_push_receive_no_parameter)

    assert r.is_parsed
    assert r.is_received
    assert r.is_received
    assert r.is_ok
    assert r.id is QueryCmdId.SETTING_CAPABILITY_PUSH
    assert r.cmd is QueryCmdId.SETTING_CAPABILITY_PUSH
    assert r.uuid is UUID.CQ_QUERY_RESP
    assert r.endpoint is None
    assert r[SettingId.RESOLUTION] == []
    assert isinstance(r.flatten, dict)


test_read_receive = bytearray([0x64, 0x62, 0x32, 0x2D, 0x73, 0x58, 0x56, 0x2D, 0x66, 0x62, 0x38])


def test_read_command():
    # Need to call the command to update the parser map
    b = BleCommands(None)
    try:
        b.get_wifi_password()
    except AttributeError:
        pass

    r = GoProResp.from_read_response(UUID.WAP_PASSWORD, test_read_receive)
    assert r.is_parsed
    assert r.is_received
    assert r.is_received
    assert r.is_ok
    assert r.id is UUID.WAP_PASSWORD
    assert r.cmd is None
    assert r.endpoint is None
    assert r["password"] == "db2-sXV-fb8"
    assert len(str(r)) > 0
    assert isinstance(r.flatten, str)


json_receive = {
    "status": "SUCCESS",
    "id": "gopro/media/info?path=100GOPRO/GX010672.MP4",
    "cre": "1451629395",
    "s": "4962693",
    "mahs": "1",
    "us": "0",
    "mos": [],
    "eis": "0",
    "pta": "0",
    "ao": "stereo",
    "tr": "0",
    "mp": "0",
    "ct": "0",
    "rot": "0",
    "fov": "0",
    "lc": "0",
    "prjn": "6",
    "gumi": "0277ed35237d1091e2c4506e6fc8a7e9",
    "ls": "890930",
    "cl": "0",
    "avc_profile": "1",
    "profile": "153",
    "hc": "0",
    "hi": [],
    "dur": "2",
    "w": "1920",
    "h": "1080",
    "fps": "90000",
    "fps_denom": "3003",
    "prog": "1",
    "subsample": "0",
}


def test_http_response():
    with requests_mock.Mocker() as m:
        m.get("http://test.com", json=json_receive)
        response = requests.get("http://test.com")
        r = GoProResp.from_http_response(response)

        assert r.is_parsed
        assert r.is_received
        assert r.is_received
        assert r.is_ok
        assert r.cmd is None
        assert r.uuid is None
        assert len(str(r)) > 0
