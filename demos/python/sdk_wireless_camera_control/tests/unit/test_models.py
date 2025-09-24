# test_media_list.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jun 26 18:26:05 UTC 2023

from typing import Final

from open_gopro.models import (
    GroupedMediaItem,
    HttpInvalidSettingResponse,
    MediaItem,
    MediaList,
    MediaMetadata,
    PhotoMetadata,
    ScheduledCapture,
    VideoMetadata,
    streaming,
)
from open_gopro.models.streaming import WebcamResponse
from open_gopro.parsers import ScheduledCaptureParser

SINGLE_MEDIA_ITEM: Final = {
    "n": "GX010001.MP4",
    "cre": "1656931398",
    "mod": "1656931398",
    "glrv": "1366268",
    "ls": "-1",
    "s": "27469309",
}

GROUPED_MEDIA_ITEM: Final = {
    "n": "G0010010.JPG",
    "g": "1",
    "b": "10",
    "l": "39",
    "cre": "1657016833",
    "mod": "1657016833",
    "s": "170696972",
    "t": "b",
    "m": [],
}


MEDIA_LIST: Final = {
    "id": "23544241138403583",
    "media": [
        {
            "d": "100GOPRO",
            "fs": [
                {
                    "n": "GX010001.MP4",
                    "cre": "1656931398",
                    "mod": "1656931398",
                    "glrv": "1366268",
                    "ls": "-1",
                    "s": "27469309",
                },
                {"n": "GOPR0002.JPG", "cre": "1656931409", "mod": "1656931409", "s": "5518647"},
                {"n": "GOPR0003.JPG", "cre": "1656931440", "mod": "1656931440", "s": "4672440"},
                {
                    "n": "GX010004.MP4",
                    "cre": "1657013120",
                    "mod": "1657013120",
                    "glrv": "2489198",
                    "ls": "-1",
                    "s": "47939086",
                },
                {"n": "GOPR0005.JPG", "cre": "1657013127", "mod": "1657013127", "s": "7010699"},
                {"n": "GOPR0006.JPG", "cre": "1657013129", "mod": "1657013129", "s": "8596771"},
                {
                    "n": "GX010007.MP4",
                    "cre": "1657013162",
                    "mod": "1657013162",
                    "glrv": "1800635",
                    "ls": "-1",
                    "s": "33849822",
                },
                {
                    "n": "GX010008.MP4",
                    "cre": "1657013166",
                    "mod": "1657013166",
                    "glrv": "2400680",
                    "ls": "-1",
                    "s": "45571078",
                },
                {
                    "n": "GX010009.MP4",
                    "cre": "1657013171",
                    "mod": "1657013171",
                    "glrv": "2121971",
                    "ls": "-1",
                    "s": "41702381",
                },
                {
                    "n": "G0010010.JPG",
                    "g": "1",
                    "b": "10",
                    "l": "39",
                    "cre": "1657016833",
                    "mod": "1657016833",
                    "s": "170696972",
                    "t": "b",
                    "m": [],
                },
                {
                    "n": "G0020041.JPG",
                    "g": "2",
                    "b": "41",
                    "l": "70",
                    "cre": "1657018747",
                    "mod": "1657018747",
                    "s": "166729035",
                    "t": "b",
                    "m": [],
                },
                {
                    "n": "GX010040.MP4",
                    "cre": "1657018743",
                    "mod": "1657018743",
                    "glrv": "1167331",
                    "ls": "-1",
                    "s": "25086075",
                },
                {"n": "GOPR0039.JPG", "cre": "1724339068", "mod": "1724339068", "raw": "1", "s": "783927"},
            ],
        }
    ],
}

MEDIA_LIST_360 = {
    "id": "520435615311363",
    "media": [
        {
            "d": "100GOPRO",
            "fs": [
                {"n": "GS010001.36P", "cre": "1748346433", "mod": "1748346433", "s": "3264094"},
                {
                    "n": "GX010002.MP4",
                    "cre": "1748346556",
                    "mod": "1748346556",
                    "glrv": "323839",
                    "ls": "-1",
                    "s": "7475790",
                },
                {
                    "n": "GSAA0003.36P",
                    "g": "1001",
                    "b": "3",
                    "l": "11",
                    "cre": "1750861268",
                    "mod": "1750861268",
                    "s": "48802268",
                    "t": "b",
                    "m": [],
                },
                {
                    "n": "GSAB0013.36P",
                    "g": "1002",
                    "b": "13",
                    "l": "22",
                    "cre": "1750864146",
                    "mod": "1750864146",
                    "s": "54954054",
                    "t": "b",
                    "m": [],
                },
                {
                    "n": "GSAC0023.36P",
                    "g": "1003",
                    "b": "23",
                    "l": "32",
                    "cre": "1750864697",
                    "mod": "1750864697",
                    "s": "55312493",
                    "t": "b",
                    "m": [],
                },
                {"n": "GS010033.36P", "cre": "1753794324", "mod": "1753794324", "s": "3921602"},
                {"n": "GS010034.36P", "cre": "1753794372", "mod": "1753794372", "s": "4304293"},
                {
                    "n": "GSAD0035.36P",
                    "g": "1004",
                    "b": "35",
                    "l": "44",
                    "cre": "1753794383",
                    "mod": "1753794383",
                    "s": "54076311",
                    "t": "b",
                    "m": [],
                },
                {"n": "GS010045.36P", "cre": "1753794421", "mod": "1753794421", "s": "3784647"},
                {"n": "GS010046.360", "cre": "1753794424", "mod": "1753794424", "ls": "2760241", "s": "23327661"},
                {"n": "GS010047.360", "cre": "1753794433", "mod": "1753794433", "ls": "2517092", "s": "19105093"},
                {"n": "GS010048.360", "cre": "1753794437", "mod": "1753794437", "ls": "3236115", "s": "29375060"},
                {"n": "GS010049.360", "cre": "1753794442", "mod": "1753794442", "ls": "1524671", "s": "27109396"},
                {"n": "GS010050.360", "cre": "1753794496", "mod": "1753794496", "ls": "38857", "s": "38770"},
                {"n": "GS010051.360", "cre": "1753794508", "mod": "1753794508", "ls": "357824", "s": "3069973"},
                {"n": "GS010052.360", "cre": "1753794557", "mod": "1753794557", "ls": "409778", "s": "5958262"},
                {"n": "GS010053.36P", "cre": "1753794613", "mod": "1753794613", "s": "3501568"},
            ],
        }
    ],
}


def test_single_media_item():
    assert MediaItem(**SINGLE_MEDIA_ITEM)


def test_grouped_media_item():
    assert GroupedMediaItem(**GROUPED_MEDIA_ITEM)


def test_media_list():
    media_list = MediaList(**MEDIA_LIST)
    assert media_list
    items = media_list.files
    assert len(items) == 13
    assert len([item for item in items if isinstance(item, GroupedMediaItem)]) == 2
    assert media_list.files[0].filename == "100GOPRO/GX010001.MP4"
    assert media_list.files[-1].raw == "1"


def test_media_list_360():
    media_list = MediaList(**MEDIA_LIST_360)
    assert media_list
    items = media_list.files
    assert len(items) == 17
    assert len([item for item in items if isinstance(item, GroupedMediaItem)]) == 4
    assert media_list.files[0].filename == "100GOPRO/GS010001.36P"


VIDEO_METADATA: Final = {
    "cre": "1656927817",
    "s": "27469309",
    "mahs": "0",
    "us": "0",
    "mos": [],
    "eis": "0",
    "pta": "1",
    "ao": "stereo",
    "tr": "0",
    "mp": "0",
    "ct": "0",
    "rot": "0",
    "fov": "0",
    "lc": "0",
    "prjn": "9",
    "gumi": "1fd0ef36481b8ce8fdcb21e8f4ca2637",
    "ls": "1366268",
    "cl": "0",
    "avc_profile": "255",
    "profile": "255",
    "hc": "0",
    "hi": [],
    "dur": "4",
    "w": "5312",
    "h": "2988",
    "fps": "1001",
    "fps_denom": "30000",
    "prog": "1",
    "subsample": "0",
}

PHOTO_METADATA: Final = {
    "cre": "1656931408",
    "s": "5518647",
    "hc": "0",
    "us": "0",
    "mos": [],
    "eis": "0",
    "hdr": "0",
    "wdr": "0",
    "raw": "0",
    "tr": "0",
    "mp": "0",
    "ct": "4",
    "rot": "0",
    "fov": "28",
    "lc": "0",
    "prjn": "9",
    "gumi": "7e39f1de649dfdf94a84ca12d99c4ce5",
    "w": "5568",
    "h": "4872",
}


def test_video():
    meta = MediaMetadata.from_json(VIDEO_METADATA)
    assert isinstance(meta, VideoMetadata)


def test_photo():
    assert isinstance(MediaMetadata.from_json(PHOTO_METADATA), PhotoMetadata)


WEBCAM_SUCCESS_RSP = {
    "status": "2",
    "error": "0",
}


def test_webcam_success_response():
    response = WebcamResponse(**WEBCAM_SUCCESS_RSP)
    assert response.status == streaming.WebcamStatus.HIGH_POWER_PREVIEW
    assert response.error == streaming.WebcamError.SUCCESS


WEBCAM_FAILURE_RSP = {
    "error": "4",
    "option_id": "2",
    "setting_id": "135",
    "supported_options": [
        {
            "display_name": "Auto Boost",
            "id": "4",
        },
        {
            "display_name": "Boost",
            "id": "3",
        },
        {
            "display_name": "On",
            "id": "1",
        },
        {
            "display_name": "Off",
            "id": "0",
        },
    ],
}


def test_webcam_failure_response():
    response = WebcamResponse(**WEBCAM_FAILURE_RSP)
    assert response.error == streaming.WebcamError.SHUTTER
    # Test our scrubbing of null values
    assert "None" not in str(response)


HTTP_INVALID_SETTING_RSP: Final = {
    "error": "4",
    "option_id": "100",
    "setting_id": "135",
    "supported_options": [
        {
            "display_name": "Auto Boost",
            "id": "4",
        },
        {
            "display_name": "Boost",
            "id": "3",
        },
        {
            "display_name": "On",
            "id": "1",
        },
        {
            "display_name": "Off",
            "id": "0",
        },
    ],
}


def test_invalid_setting_http_response():
    response = HttpInvalidSettingResponse(**HTTP_INVALID_SETTING_RSP)
    assert response.error == 4
    assert len(response.supported_options) == 4


test = {
    "error": 4,
    "option_id": 100,
    "setting_id": 135,
    "supported_options": [
        {"display_name": "Auto Boost", "id": 4},
        {"display_name": "Boost", "id": 3},
        {"display_name": "On", "id": 1},
        {"display_name": "Off", "id": 0},
    ],
}


def test_printing():
    response = HttpInvalidSettingResponse(**HTTP_INVALID_SETTING_RSP)
    str(response)
    assert True


def test_parse_schedule_capture():
    # GIVEN
    raw_bytes = bytes([0x00, 0x00, 0x0C, 0x8B])

    # WHEN
    scheduled_capture = ScheduledCaptureParser().parse(raw_bytes)

    # THEN
    assert scheduled_capture.hour == 12
    assert scheduled_capture.minute == 34
    assert scheduled_capture.is_24_hour == True
    assert scheduled_capture.is_enabled == True


def test_build_schedule_capture():
    # GIVEN
    scheduled_capture = ScheduledCapture(hour=12, minute=34, is_24_hour=True, is_enabled=True)

    # WHEN
    raw_bytes = ScheduledCaptureParser().build(scheduled_capture)

    # THEN
    assert raw_bytes == bytes([0x00, 0x00, 0x0C, 0x8B])
