/* httpResponses.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package vectors

import com.gopro.open_gopro.operations.DateTimeHttpResponse
import com.gopro.open_gopro.operations.HardwareInfo
import com.gopro.open_gopro.operations.LivestreamConfigurationRequest
import com.gopro.open_gopro.operations.LivestreamFov
import com.gopro.open_gopro.operations.LivestreamResolution
import com.gopro.open_gopro.operations.MediaId
import com.gopro.open_gopro.operations.OgpVersionHttpResponse

val mockMediaId = MediaId("file", "folder")
val mockHardwareInfo =
    HardwareInfo(
        "modelNumber", "modelName", "firmwareVersion", "serialNumber", "apSsid", "apMacAddress")
val mockLivestreamRequest =
    LivestreamConfigurationRequest(
        url = "rtmp://192.168.50.55:8443/live/test",
        shouldEncode = true,
        maximumBitrate = 10,
        startingBitRate = 1,
        minimumBitrate = 0,
        resolution = LivestreamResolution.RES_480,
        fov = LivestreamFov.WIDE,
        certificate = null)
val mockOgpVersion = OgpVersionHttpResponse("2.0")

val photoMetadataJson: String =
    """
{
    "cre": "1648787120",
    "s": "3645396",
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
    "gumi": "a1a5834aa7714de5a36da58426829da2",
    "w": "5568",
    "h": "4872"
}
"""
        .trimIndent()

val videoMetadataJson: String =
    """
{
    "cre": "1659769382",
    "s": "4489890",
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
    "gumi": "4bd0acdfc13ff52ba7b3f8c593cc932f",
    "ls": "329080",
    "cl": "0",
    "avc_profile": "255",
    "profile": "255",
    "hc": "0",
    "hi": [],
    "dur": "3",
    "w": "3840",
    "h": "2160",
    "fps": "30000",
    "fps_denom": "1001",
    "prog": "1",
    "subsample": "0"
}
"""
        .trimIndent()

val videoMetadataJson2 =
    """
{
    "cre": "1725899031",
    "s": "3040046",
    "us": "0",
    "mos": [],
    "eis": "0",
    "pta": "1",
    "ao": "stereo",
    "tr": "0",
    "mp": "0",
    "ct": "0",
    "rot": "0",
    "lc": "0",
    "prjn": "9",
    "gumi": "c81c4d50b87a70ba85255aaab0210dab",
    "ls": "172154",
    "cl": "0",
    "avc_profile": "255",
    "profile": "255",
    "hc": "0",
    "hi": [],
    "dur": "2",
    "w": "3840",
    "h": "2160",
    "fps": "30000",
    "fps_denom": "1001",
    "prog": "1",
    "subsample": "0"
}
"""
        .trimIndent()

val problematicMetadataJson =
    """
{
    "cre": "3668857923",
    "s": "104378731",
    "us": "0",
    "mos": [],
    "eis": "1",
    "pta": "0",
    "ao": "auto",
    "tr": "0",
    "mp": "0",
    "ct": "0",
    "rot": "0",
    "lc": "0",
    "prjn": "9",
    "gumi": "d1708b90ca32d4cbe6988d8fdb0fda86",
    "ls": "5052423",
    "cl": "0",
    "avc_profile": "1",
    "profile": "150",
    "hc": "0",
    "hi": [],
    "dur": "35",
    "w": "1920",
    "h": "1080",
    "fps": "60000",
    "fps_denom": "1001",
    "prog": "1",
    "subsample": "0"
}
"""
        .trimIndent()

val singleMediaListItemJson: String =
    """
{
    "n": "GX017060.MP4",
    "cre": "1659744181",
    "mod": "1659744181",
    "glrv": "329080",
    "ls": "-1",
    "s": "4489890"
}
"""
        .trimIndent()

val groupedMediaListItemJson: String =
    """
{
    "n": "G0017061.JPG",
    "g": "1",
    "b": "7061",
    "l": "7090",
    "cre": "1729860144",
    "mod": "1729860144",
    "s": "170856763",
    "t": "b",
    "m": []
}
"""
        .trimIndent()

val mediaListJson: String =
    """
{
    "id": "3681934162299015560",
    "media": [
        {
            "d": "100GOPRO",
            "fs": [
                {
                    "n": "GOPR7056.JPG",
                    "cre": "1725619383",
                    "mod": "1725619383",
                    "s": "2064314"
                },
                {
                    "n": "GOPR7057.JPG",
                    "cre": "1725620421",
                    "mod": "1725620421",
                    "s": "2065629"
                },
                {
                    "n": "GOPR7058.JPG",
                    "cre": "1735862601",
                    "mod": "1735862601",
                    "s": "2211690"
                },
                {
                    "n": "GOPR7059.JPG",
                    "cre": "1648787121",
                    "mod": "1648787121",
                    "s": "3645396"
                },
                {
                    "n": "GX017060.MP4",
                    "cre": "1659744181",
                    "mod": "1659744181",
                    "glrv": "329080",
                    "ls": "-1",
                    "s": "4489890"
                },
                {
                    "n": "G0017061.JPG",
                    "g": "1",
                    "b": "7061",
                    "l": "7090",
                    "cre": "1729860144",
                    "mod": "1729860144",
                    "s": "170856763",
                    "t": "b",
                    "m": []
                }
            ]
        }
    ]
}
"""
        .trimIndent()

val mediaListJson2 =
    """
{
    "id": "2934290582809906320",
    "media": [
        {
            "d": "100GOPRO",
            "fs": [
                {
                    "n": "GP017064.JPG",
                    "cre": "1725633260",
                    "mod": "1725633260",
                    "s": "2252890"
                },
                {
                    "n": "GP017065.JPG",
                    "cre": "1725873745",
                    "mod": "1725873745",
                    "s": "2610672"
                },
                {
                    "n": "GX017066.MP4",
                    "cre": "1725873805",
                    "mod": "1725873805",
                    "glrv": "172154",
                    "ls": "-1",
                    "s": "3040046"
                },
                {
                    "n": "GX017067.MP4",
                    "cre": "1725874517",
                    "mod": "1725874517",
                    "glrv": "5052423",
                    "ls": "-1",
                    "s": "104378731"
                },
                {
                    "n": "GP017068.JPG",
                    "cre": "1725885620",
                    "mod": "1725885620",
                    "s": "2494097"
                },
                {
                    "n": "GX017069.MP4",
                    "cre": "1725885720",
                    "mod": "1725885720",
                    "glrv": "891061",
                    "ls": "-1",
                    "s": "15679872"
                },
                {
                    "n": "GP017070.JPG",
                    "cre": "1725966740",
                    "mod": "1725966740",
                    "s": "5223822"
                },
                {
                    "n": "GP017071.JPG",
                    "cre": "1725966853",
                    "mod": "1725966853",
                    "raw": "1",
                    "s": "3887538"
                },
                {
                    "n": "GP017072.JPG",
                    "cre": "1726134257",
                    "mod": "1726134257",
                    "s": "2455179"
                },
                {
                    "n": "GP017073.JPG",
                    "cre": "1726134671",
                    "mod": "1726134671",
                    "s": "2324945"
                },
                {
                    "n": "GP017074.JPG",
                    "cre": "1726134722",
                    "mod": "1726134722",
                    "s": "2356223"
                },
                {
                    "n": "GP017075.JPG",
                    "cre": "1726134968",
                    "mod": "1726134968",
                    "s": "2654067"
                },
                {
                    "n": "GP017076.JPG",
                    "cre": "1726135146",
                    "mod": "1726135146",
                    "s": "2726903"
                },
                {
                    "n": "GP017077.JPG",
                    "cre": "1726141022",
                    "mod": "1726141022",
                    "s": "2582986"
                },
                {
                    "n": "GP017078.JPG",
                    "cre": "1726141039",
                    "mod": "1726141039",
                    "s": "2595205"
                },
                {
                    "n": "GP017079.JPG",
                    "cre": "1726141092",
                    "mod": "1726141092",
                    "s": "2623933"
                },
                {
                    "n": "GX017080.MP4",
                    "cre": "1726142779",
                    "mod": "1726142779",
                    "glrv": "1296081",
                    "ls": "-1",
                    "s": "24370839"
                },
                {
                    "n": "GP017081.JPG",
                    "cre": "1726171874",
                    "mod": "1726171874",
                    "s": "2573194"
                },
                {
                    "n": "GP017082.JPG",
                    "cre": "1726171928",
                    "mod": "1726171928",
                    "s": "2593924"
                },
                {
                    "n": "GP017083.JPG",
                    "cre": "1726171982",
                    "mod": "1726171982",
                    "s": "2792860"
                },
                {
                    "n": "GP017084.JPG",
                    "cre": "1726143987",
                    "mod": "1726143987",
                    "s": "2969845"
                },
                {
                    "n": "GP017085.JPG",
                    "cre": "1726144093",
                    "mod": "1726144093",
                    "s": "2901553"
                },
                {
                    "n": "GX017086.MP4",
                    "cre": "1729616168",
                    "mod": "1729616168",
                    "glrv": "259590",
                    "ls": "-1",
                    "s": "4769350"
                },
                {
                    "n": "GP017087.JPG",
                    "cre": "1729772475",
                    "mod": "1729772475",
                    "s": "2682250"
                },
                {
                    "n": "GX017088.MP4",
                    "cre": "1730230636",
                    "mod": "1730230636",
                    "glrv": "210198",
                    "ls": "-1",
                    "s": "2559246"
                }
            ]
        }
    ]
}
"""
        .trimIndent()

val datetimeResponse =
    DateTimeHttpResponse(date = "2023_1_31", time = "3_4_5", dst = 1, tzone = -120)

val webcamStatusResponseJson =
    """
{
    "status": 0,
    "error": 0
}
"""
        .trimIndent()
