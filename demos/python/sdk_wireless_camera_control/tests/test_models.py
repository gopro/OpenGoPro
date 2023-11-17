# test_media_list.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jun 26 18:26:05 UTC 2023

from typing import Final

from open_gopro import constants
from open_gopro.models import (
    GroupedMediaItem,
    MediaItem,
    MediaList,
    MediaMetadata,
    PhotoMetadata,
    VideoMetadata,
)
from open_gopro.models.general import HttpInvalidSettingResponse, WebcamResponse

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
    assert len(items) == 12
    assert len([item for item in items if isinstance(item, GroupedMediaItem)]) == 2
    assert media_list.files[0].filename == "100GOPRO/GX010001.MP4"


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
    assert response.status == constants.WebcamStatus.HIGH_POWER_PREVIEW
    assert response.error == constants.WebcamError.SUCCESS


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
    assert response.error == constants.WebcamError.SHUTTER
    # Test our scrubbing of null values
    assert "None" not in str(response)


HTTP_INVALID_SETTING_RSP = {
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
