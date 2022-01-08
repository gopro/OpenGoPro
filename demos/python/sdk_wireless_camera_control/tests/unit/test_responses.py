# test_responses.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:54 PM

"""Test the responses module"""

# pylint: disable= redefined-outer-name

import requests

import pytest
import requests_mock

from open_gopro import GoPro
from open_gopro.communication_client import GoProResponder
from open_gopro.api import Api
from open_gopro.constants import GoProUUIDs, QueryCmdId, SettingId, StatusId
from open_gopro.responses import GoProResp, ParserMapType
from open_gopro.api.v1_0.api import ApiV1_0


@pytest.fixture(scope="function")
def parser_map() -> ParserMapType:
    responder = GoProResponder()
    ApiV1_0(responder, responder)
    yield responder._parser_map


test_push_receive_no_parameter = bytearray([0x08, 0xA2, 0x00, 0x02, 0x00, 0x03, 0x00, 0x79, 0x00])


def test_push_response_no_parameter_values(parser_map: ParserMapType):
    r = GoProResp(parser_map, [GoProUUIDs.CQ_QUERY_RESP])
    r._accumulate(test_push_receive_no_parameter)
    assert r.is_received
    r._parse()
    assert r.is_parsed
    assert r.is_ok
    assert r.id is QueryCmdId.SETTING_CAPABILITY_PUSH
    assert r.cmd is QueryCmdId.SETTING_CAPABILITY_PUSH
    assert r.uuid == GoProUUIDs.CQ_QUERY_RESP
    assert r.endpoint is None
    assert r[SettingId.RESOLUTION] == []
    assert isinstance(r.flatten, dict)


test_read_receive = bytearray([0x64, 0x62, 0x32, 0x2D, 0x73, 0x58, 0x56, 0x2D, 0x66, 0x62, 0x38])


def test_read_command(parser_map: ParserMapType):
    r = GoProResp._from_read_response(parser_map, GoProUUIDs.WAP_PASSWORD, test_read_receive)
    assert r.is_parsed
    assert r.is_received
    assert r.is_received
    assert r.is_ok
    assert r.id is GoProUUIDs.WAP_PASSWORD
    assert r.cmd is None
    assert r.endpoint is None
    assert r["password"] == "db2-sXV-fb8"
    assert len(str(r)) > 0
    assert isinstance(r.flatten, str)


test_write_send = bytearray([0x01, 0x05])
test_write_recieve = bytearray([0x02, 0x05, 0x00])


def test_write_command(parser_map: ParserMapType):
    r = GoProResp._from_write_command(parser_map, GoProUUIDs.CQ_COMMAND, test_write_send)
    r._accumulate(test_write_recieve)
    assert r.is_received
    r._parse()
    assert r.is_parsed
    assert r.is_ok


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
        0x03,
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


def test_complex_write_command(parser_map: ParserMapType):
    r = GoProResp._from_write_command(parser_map, GoProUUIDs.CQ_QUERY, test_complex_write_send)
    idx = 0
    while not r.is_received:
        end = len(test_complex_write_receive) if idx + 20 > len(test_complex_write_receive) else idx + 20
        r._accumulate(test_complex_write_receive[idx:end])
        idx = end
    assert r.is_received
    r._parse()
    assert r.is_parsed
    assert r.is_received
    assert r.is_ok
    assert r.id is QueryCmdId.GET_STATUS_VAL
    assert r.cmd is QueryCmdId.GET_STATUS_VAL
    assert r.uuid == GoProUUIDs.CQ_QUERY_RESP
    assert StatusId.ENCODING in r
    # Test iterator
    for x in r:
        assert isinstance(x, StatusId)
    assert len(str(r)) > 0
    assert isinstance(r.flatten, dict)
    # Test dict methods
    assert len(r.items())
    assert len(r.keys())
    assert len(r.values())


test_json = {
    "status": {
        "1": 1,
        "2": 4,
        "3": 0,
        "4": 255,
        "6": 0,
        "8": 0,
        "9": 0,
        "10": 0,
        "11": 0,
        "13": 0,
        "14": 0,
        "17": 1,
        "19": 3,
        "20": 1,
        "21": 2317890,
        "22": 0,
        "23": 0,
        "24": 0,
        "26": 0,
        "27": 0,
        "28": 82,
        "29": "",
        "30": "GP24500480",
        "31": 1,
        "32": 0,
        "33": 0,
        "34": 1814,
        "35": 2954,
        "36": 0,
        "37": 31,
        "38": 0,
        "39": 31,
        "40": "%16%01%04%06%1E%21",
        "41": 0,
        "42": 0,
        "45": 0,
        "49": 0,
        "54": 25630304,
        "55": 1,
        "56": 2,
        "57": 23669405,
        "58": 0,
        "59": 0,
        "60": 500,
        "61": 2,
        "62": 0,
        "63": 0,
        "64": 907,
        "65": 0,
        "66": 100,
        "67": 100,
        "68": 1,
        "69": 1,
        "70": 36,
        "74": 0,
        "75": 0,
        "76": 1,
        "77": 1,
        "78": 0,
        "79": 0,
        "81": 1,
        "82": 1,
        "83": 1,
        "85": 0,
        "86": 0,
        "88": 0,
        "89": 12,
        "90": 1,
        "91": 0,
        "93": 2,
        "94": 65536,
        "95": 131072,
        "96": 1000,
        "97": 2,
        "98": 16777218,
        "99": 984,
        "100": 0,
        "101": 0,
        "102": 0,
        "103": 0,
        "104": 1,
        "105": 0,
        "106": 0,
        "107": 4294967295,
        "108": 0,
        "109": 0,
        "110": 0,
        "111": 1,
        "112": 0,
        "113": 0,
        "114": 0,
        "115": 0,
    },
    "settings": {
        "2": 9,
        "3": 8,
        "5": 0,
        "6": 1,
        "13": 1,
        "19": 0,
        "24": 0,
        "30": 110,
        "31": 0,
        "32": 10,
        "37": 0,
        "41": 9,
        "42": 5,
        "43": 0,
        "44": 9,
        "45": 5,
        "47": 4,
        "48": 3,
        "54": 1,
        "59": 0,
        "60": 0,
        "61": 0,
        "62": 0,
        "64": 4,
        "65": 0,
        "66": 0,
        "67": 0,
        "75": 0,
        "76": 0,
        "79": 0,
        "83": 1,
        "84": 0,
        "85": 0,
        "86": 0,
        "87": 40,
        "88": 64,
        "91": 2,
        "102": 8,
        "103": 3,
        "105": 0,
        "106": 1,
        "111": 10,
        "112": 255,
        "114": 1,
        "115": 0,
        "116": 0,
        "117": 0,
        "118": 4,
        "121": 0,
        "122": 22,
        "123": 22,
        "124": 100,
        "125": 0,
        "126": 0,
        "128": 12,
        "129": 2,
        "130": 1,
        "131": 3,
        "132": 12,
        "134": 2,
        "135": 2,
        "139": 3,
        "144": 12,
        "145": 0,
        "146": 0,
        "147": 0,
        "148": 2,
        "149": 2,
        "153": 100,
        "154": 3,
        "155": 0,
        "156": 100,
        "157": 100,
        "158": 0,
        "159": 0,
        "160": 0,
        "161": 100,
        "164": 100,
        "165": 0,
        "166": 0,
        "167": 4,
        "168": 0,
        "169": 1,
    },
}


def test_http_response_with_extra_parsing(parser_map: ParserMapType):
    url = "gopro/camera/state"
    url = GoPro._base_url + url
    with requests_mock.Mocker() as m:
        m.get(url, json=test_json)
        response = requests.get(url)
        r = GoProResp._from_http_response(parser_map, response)

        assert r.is_parsed
        assert r.is_received
        assert r.is_received
        assert r.is_ok
        assert r.cmd is None
        assert r.uuid == None
        assert len(str(r)) > 0
        assert r.endpoint


send_proto = bytearray(b"\x04\xf1k\x08\x01")
receive_proto = bytearray(b"\x04\xf1\xeb\x08\x01")


def test_proto(parser_map: ParserMapType):
    r = GoProResp._from_write_command(parser_map, GoProUUIDs.CQ_COMMAND, send_proto)
    r._accumulate(receive_proto)
    assert r.is_received
    r._parse()
    assert r.is_parsed
    assert r.is_ok
