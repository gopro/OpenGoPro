# settings.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 20 23:24:52 UTC 2025

"""Setting-related constants"""

########################################################################################################################
#
# Warning!! This file is auto-generated. Do not modify it manually.
#
########################################################################################################################

from open_gopro.enum import GoProIntEnum


class SettingId(GoProIntEnum):
    """Setting ID's that identify settings and are written to GoProUUID.CQ_SETTINGS."""

    MEDIA_FORMAT = 128
    VIDEO_RESOLUTION = 2
    FRAMES_PER_SECOND = 3
    VIDEO_TIMELAPSE_RATE = 5
    ANTI_FLICKER = 134
    HYPERSMOOTH = 135
    VIDEO_HORIZON_LEVELING = 150
    PHOTO_HORIZON_LEVELING = 151
    PHOTO_TIMELAPSE_RATE = 30
    NIGHTLAPSE_RATE = 32
    MAX_LENS = 162
    HINDSIGHT = 167
    WEBCAM_DIGITAL_LENSES = 43
    PHOTO_SINGLE_INTERVAL = 171
    PHOTO_INTERVAL_DURATION = 172
    VIDEO_PERFORMANCE_MODE = 173
    CONTROLS = 175
    EASY_MODE_SPEED = 176
    ENABLE_NIGHT_PHOTO = 177
    WIRELESS_BAND = 178
    STAR_TRAILS_LENGTH = 179
    SYSTEM_VIDEO_MODE = 180
    VIDEO_BIT_RATE = 182
    BIT_DEPTH = 183
    PROFILES = 184
    VIDEO_EASY_MODE = 186
    AUTO_POWER_DOWN = 59
    LAPSE_MODE = 187
    MAX_LENS_MOD = 189
    MAX_LENS_MOD_ENABLE = 190
    EASY_NIGHT_PHOTO = 191
    MULTI_SHOT_ASPECT_RATIO = 192
    FRAMING = 193
    GPS = 83
    CAMERA_VOLUME = 216
    LED = 91
    SETUP_SCREEN_SAVER = 219
    SETUP_LANGUAGE = 223
    PHOTO_MODE = 227
    VIDEO_FRAMING = 232
    MULTI_SHOT_FRAMING = 233
    FRAME_RATE = 234
    VIDEO_ASPECT_RATIO = 108
    VIDEO_LENS = 121
    PHOTO_LENS = 122
    TIME_LAPSE_DIGITAL_LENSES = 123
    PHOTO_OUTPUT = 125


class MediaFormat(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#media-format-128)"""

    TIME_LAPSE_VIDEO = 13
    TIME_LAPSE_PHOTO = 20
    NIGHT_LAPSE_PHOTO = 21
    NIGHT_LAPSE_VIDEO = 26


class VideoResolution(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-resolution-2)"""

    NUM_5K = 24
    NUM_4K = 1
    NUM_4K_4_3 = 18
    NUM_2_7K = 4
    NUM_2_7K_4_3 = 6
    NUM_1440 = 7
    NUM_1080 = 9
    NUM_5_3K = 100
    NUM_5_3K_4_3 = 27
    NUM_5_3K_8_7 = 26
    NUM_4K_8_7 = 28
    NUM_5_3K_21_9 = 35
    NUM_5_3K_4_3_V2 = 113
    NUM_5_3K_8_7_V2 = 107
    NUM_4K_4_3_V2 = 112
    NUM_4K_8_7_V2 = 108
    NUM_4K_21_9 = 36
    NUM_4K_1_1 = 37
    NUM_2_7K_4_3_V2 = 111
    NUM_4K_9_16_V2 = 109
    NUM_1080_9_16_V2 = 110
    NUM_900 = 38
    NUM_720 = 12
    NUM_5K_4_3 = 25


class FramesPerSecond(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frames-per-second-3)"""

    NUM_240_0 = 0
    NUM_200_0 = 13
    NUM_120_0 = 1
    NUM_100_0 = 2
    NUM_60_0 = 5
    NUM_50_0 = 6
    NUM_30_0 = 8
    NUM_25_0 = 9
    NUM_24_0 = 10
    NUM_400_0 = 15
    NUM_360_0 = 16
    NUM_300_0 = 17


class VideoTimelapseRate(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-timelapse-rate-5)"""

    NUM_60_MINUTES = 10
    NUM_30_MINUTES = 9
    NUM_5_MINUTES = 8
    NUM_2_MINUTES = 7
    NUM_60_SECONDS = 6
    NUM_30_SECONDS = 5
    NUM_10_SECONDS = 4
    NUM_5_SECONDS = 3
    NUM_2_SECONDS = 2
    NUM_1_SECOND = 1
    NUM_0_5_SECONDS = 0
    NUM_3_SECONDS = 11


class Anti_Flicker(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#anti-flicker-134)"""

    NUM_60HZ = 2
    NUM_50HZ = 3
    NTSC = 0
    PAL = 1


class Hypersmooth(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hypersmooth-135)"""

    BOOST = 3
    HIGH = 2
    LOW = 1
    OFF = 0
    AUTO_BOOST = 4
    STANDARD = 100


class VideoHorizonLeveling(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-horizon-leveling-150)"""

    OFF = 0
    LOCKED = 2


class PhotoHorizonLeveling(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-horizon-leveling-151)"""

    OFF = 0
    LOCKED = 2


class PhotoTimelapseRate(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-timelapse-rate-30)"""

    NUM_60_MINUTES = 100
    NUM_30_MINUTES = 101
    NUM_5_MINUTES = 102
    NUM_2_MINUTES = 103
    NUM_60_SECONDS = 104
    NUM_30_SECONDS = 105
    NUM_10_SECONDS = 106
    NUM_5_SECONDS = 107
    NUM_2_SECONDS = 108
    NUM_1_SECOND = 109
    NUM_0_5_SECONDS = 110
    NUM_3_SECONDS = 11


class NightlapseRate(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#nightlapse-rate-32)"""

    NUM_60_MINUTES = 3600
    NUM_30_MINUTES = 1800
    NUM_5_MINUTES = 300
    NUM_2_MINUTES = 120
    NUM_60_SECONDS = 100
    NUM_30_SECONDS = 30
    NUM_20_SECONDS = 20
    NUM_15_SECONDS = 15
    NUM_10_SECONDS = 10
    NUM_5_SECONDS = 5
    NUM_4_SECONDS = 4
    AUTO = 3601


class MaxLens(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-162)"""

    OFF = 0
    ON = 1


class Hindsight(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hindsight-167)"""

    NUM_15_SECONDS = 2
    NUM_30_SECONDS = 3
    OFF = 4


class WebcamDigitalLenses(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#webcam-digital-lenses-43)"""

    SUPERVIEW = 3
    WIDE = 0
    LINEAR = 4
    NARROW = 2


class PhotoSingleInterval(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-single-interval-171)"""

    OFF = 0
    NUM_0_5S = 2
    NUM_1S = 3
    NUM_2S = 4
    NUM_3S = 10
    NUM_5S = 5
    NUM_10S = 6
    NUM_30S = 7
    NUM_60S = 8
    NUM_120S = 9


class PhotoIntervalDuration(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-interval-duration-172)"""

    OFF = 0
    NUM_15_SECONDS = 1
    NUM_30_SECONDS = 2
    NUM_1_MINUTE = 3
    NUM_5_MINUTES = 4
    NUM_15_MINUTES = 5
    NUM_30_MINUTES = 6
    NUM_1_HOUR = 7
    NUM_2_HOURS = 8
    NUM_3_HOURS = 9


class VideoPerformanceMode(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-performance-mode-173)"""

    MAXIMUM_VIDEO_PERFORMANCE = 0
    EXTENDED_BATTERY = 1
    TRIPOD_STATIONARY_VIDEO = 2


class Controls(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#controls-175)"""

    EASY = 0
    PRO = 1


class EasyModeSpeed(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-mode-speed-176)"""

    NUM_8X_ULTRA_SLO_MO = 0
    NUM_4X_SUPER_SLO_MO = 1
    NUM_4X_SUPER_SLO_MO_2_7K_ = 25
    NUM_2X_SLO_MO_4K_ = 24
    NUM_2X_SLO_MO = 2
    NUM_1X_SPEED_LOW_LIGHT_ = 3
    NUM_8X_ULTRA_SLO_MO_EXT_BATT_ = 14
    NUM_4X_SUPER_SLO_MO_EXT_BATT_ = 4
    NUM_2X_SLO_MO_EXT_BATT_ = 5
    NUM_1X_SPEED_EXT_BATT_LOW_LIGHT_ = 6
    NUM_8X_ULTRA_SLO_MO_50HZ_ = 7
    NUM_4X_SUPER_SLO_MO_50HZ_ = 8
    NUM_4X_SUPER_SLO_MO_2_7K_50HZ_ = 27
    NUM_2X_SLO_MO_4K_50HZ_ = 26
    NUM_2X_SLO_MO_50HZ_ = 9
    NUM_1X_SPEED_50HZ_LOW_LIGHT_ = 10
    NUM_8X_ULTRA_SLO_MO_50HZ_EXT_BATT_ = 15
    NUM_4X_SUPER_SLO_MO_50HZ_EXT_BATT_ = 11
    NUM_2X_SLO_MO_50HZ_EXT_BATT_ = 12
    NUM_1X_SPEED_50HZ_EXT_BATT_LOW_LIGHT_ = 13
    NUM_8X_ULTRA_SLO_MO_LONG_BATT_ = 16
    NUM_4X_SUPER_SLO_MO_LONG_BATT_ = 17
    NUM_2X_SLO_MO_LONG_BATT_ = 18
    NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_ = 19
    NUM_8X_ULTRA_SLO_MO_50HZ_LONG_BATT_ = 20
    NUM_4X_SUPER_SLO_MO_50HZ_LONG_BATT_ = 21
    NUM_2X_SLO_MO_50HZ_LONG_BATT_ = 22
    NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_ = 23
    NUM_1X_SPEED_LOW_LIGHT_V2_ = 103
    NUM_1X_SPEED_4K_LOW_LIGHT_V2_ = 126
    NUM_2X_SLO_MO_4K_V2_ = 116
    NUM_2X_SLO_MO_V2_ = 102
    NUM_4X_SUPER_SLO_MO_V2_ = 101
    NUM_8X_ULTRA_SLO_MO_V2_ = 100
    NUM_1X_SPEED_50HZ_LOW_LIGHT_V2_ = 107
    NUM_1X_SPEED_4K_50HZ_LOW_LIGHT_V2_ = 127
    NUM_2X_SLO_MO_4K_50HZ_V2_ = 117
    NUM_2X_SLO_MO_50HZ_V2_ = 106
    NUM_4X_SUPER_SLO_MO_50HZ_V2_ = 105
    NUM_8X_ULTRA_SLO_MO_50HZ_V2_ = 104
    NUM_1X_SPEED_LOW_LIGHT_V2_VERTICAL_ = 118
    NUM_1X_SPEED_50HZ_LOW_LIGHT_V2_VERTICAL_ = 119
    NUM_2X_SLO_MO_V2_VERTICAL_ = 120
    NUM_2X_SLO_MO_50HZ_V2_VERTICAL_ = 121
    NUM_1X_SPEED_FULL_FRAME_LOW_LIGHT_V2_ = 122
    NUM_1X_SPEED_50HZ_FULL_FRAME_LOW_LIGHT_V2_ = 123
    NUM_1X_SPEED_4K_FULL_FRAME_LOW_LIGHT_V2_ = 136
    NUM_1X_SPEED_4K_50HZ_FULL_FRAME_LOW_LIGHT_V2_ = 137
    NUM_2X_SLO_MO_FULL_FRAME_V2_ = 124
    NUM_2X_SLO_MO_50HZ_FULL_FRAME_V2_ = 125
    NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_V2_ = 111
    NUM_2X_SLO_MO_LONG_BATT_V2_ = 110
    NUM_4X_SUPER_SLO_MO_LONG_BATT_V2_ = 109
    NUM_8X_ULTRA_SLO_MO_LONG_BATT_V2_ = 108
    NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_V2_ = 115
    NUM_2X_SLO_MO_50HZ_LONG_BATT_V2_ = 114
    NUM_4X_SUPER_SLO_MO_50HZ_LONG_BATT_V2_ = 113
    NUM_8X_ULTRA_SLO_MO_50HZ_LONG_BATT_V2_ = 112
    NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_V2_VERTICAL_ = 134
    NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_V2_VERTICAL_ = 135
    NUM_2X_SLO_MO_LONG_BATT_V2_VERTICAL_ = 132
    NUM_2X_SLO_MO_50HZ_LONG_BATT_V2_VERTICAL_ = 133
    NUM_1X_NORMAL_SPEED_1_1_30_FPS_4K_V2_ = 138
    NUM_1X_NORMAL_SPEED_1_1_25_FPS_4K_V2_ = 139
    NUM_2X_SLO_MO_SPEED_1_1_4K_60_FPS_V2_ = 140
    NUM_2X_SLO_MO_SPEED_1_1_4K_50_FPS_V2_ = 141
    NUM_1X_NORMAL_SPEED_21_9_30_FPS_5_3K_V2_ = 142
    NUM_1X_NORMAL_SPEED_21_9_25_FPS_5_3K_V2_ = 143
    NUM_1X_NORMAL_SPEED_21_9_30_FPS_4K_V2_ = 146
    NUM_1X_NORMAL_SPEED_21_9_25_FPS_4K_V2_ = 147
    NUM_2X_SLO_MO_SPEED_21_9_5_3K_60_FPS_V2_ = 144
    NUM_2X_SLO_MO_SPEED_21_9_5_3K_50_FPS_V2_ = 145
    NUM_2X_SLO_MO_SPEED_21_9_4K_60_FPS_V2_ = 148
    NUM_2X_SLO_MO_SPEED_21_9_4K_50_FPS_V2_ = 149
    NUM_120_4X_SUPER_SLO_MO_SPEED_21_9_4K_V2_ = 150
    NUM_100_4X_SUPER_SLO_MO_SPEED_21_9_4K_V2_ = 151
    NUM_1X_NORMAL_SPEED_30_FPS_4_3_5_3K_V2_ = 152
    NUM_1X_NORMAL_SPEED_25_FPS_4_3_5_3K_V2_ = 153
    NUM_1X_NORMAL_SPEED_30_FPS_4_3_4K_V2_ = 154
    NUM_1X_NORMAL_SPEED_25_FPS_4_3_4K_V2_ = 155
    NUM_2X_SLO_MO_SPEED_4_3_4K_60_FPS_V2_ = 156
    NUM_2X_SLO_MO_SPEED_4_3_4K_50_FPS_V2_ = 157
    NUM_120_4X_SUPER_SLO_MO_SPEED_2_7K_4_3_V2_ = 158
    NUM_100_4X_SUPER_SLO_MO_SPEED_2_7K_4_3_V2_ = 159
    NUM_1X_SPEED_2_7K_LOW_LIGHT_V2_ = 128
    NUM_2X_SLO_MO_2_7K_V2_ = 130
    NUM_1X_SPEED_2_7K_50HZ_LOW_LIGHT_V2_ = 129
    NUM_2X_SLO_MO_2_7K_50HZ_V2_ = 131


class EnableNightPhoto(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#enable-night-photo-177)"""

    OFF = 0
    ON = 1


class WirelessBand(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#wireless-band-178)"""

    NUM_2_4GHZ = 0
    NUM_5GHZ = 1


class StarTrailsLength(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#star-trails-length-179)"""

    MAX = 3
    LONG = 2
    SHORT = 1


class SystemVideoMode(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#system-video-mode-180)"""

    HIGHEST_QUALITY = 0
    EXTENDED_BATTERY = 101
    LONGEST_BATTERY = 102
    BASIC_QUALITY = 112
    STANDARD_QUALITY = 111


class VideoBitRate(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-bit-rate-182)"""

    HIGH = 1
    STANDARD = 0


class BitDepth(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#bit-depth-183)"""

    NUM_8_BIT = 0
    NUM_10_BIT = 2


class Profiles(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#profiles-184)"""

    STANDARD = 0
    HDR = 1
    LOG = 2
    HLG_HDR = 101


class VideoEasyMode(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-easy-mode-186)"""

    STANDARD_VIDEO = 3
    HDR_VIDEO = 4
    HIGHEST_QUALITY = 0
    STANDARD_QUALITY = 1
    BASIC_QUALITY = 2


class AutoPowerDown(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#auto-power-down-59)"""

    NUM_5_MIN = 4
    NUM_15_MIN = 6
    NUM_30_MIN = 7
    NEVER = 0
    NUM_1_MIN = 1
    NUM_8_SECONDS = 11
    NUM_30_SECONDS = 12


class LapseMode(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#lapse-mode-187)"""

    TIMEWARP = 0
    STAR_TRAILS = 1
    LIGHT_PAINTING = 2
    VEHICLE_LIGHTS = 3
    TIME_LAPSE_VIDEO = 8
    NIGHT_LAPSE_VIDEO = 9
    MAX_TIMEWARP = 4
    MAX_STAR_TRAILS = 5
    MAX_LIGHT_PAINTING = 6
    MAX_VEHICLE_LIGHTS = 7


class MaxLensMod(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-189)"""

    ND_32 = 9
    ND_16 = 8
    ND_8 = 7
    ND_4 = 6
    STANDARD_LENS = 10
    AUTO_DETECT = 100
    MAX_LENS_2_0 = 2
    MAX_LENS_2_5 = 3
    MACRO = 4
    ANAMORPHIC = 5
    NONE = 0
    MAX_LENS_1_0 = 1


class MaxLensModEnable(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-enable-190)"""

    OFF = 0
    ON = 1


class EasyNightPhoto(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-night-photo-191)"""

    SUPER_PHOTO = 0
    NIGHT_PHOTO = 1
    BURST = 2


class MultiShotAspectRatio(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-aspect-ratio-192)"""

    NUM_4_3 = 0
    NUM_16_9 = 1
    NUM_8_7 = 3
    NUM_9_16 = 4


class Framing(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#framing-193)"""

    WIDESCREEN_16_9_V2 = 101
    VERTICAL_9_16_V2 = 104
    FULL_FRAME_8_7_V2 = 103
    FULL_FRAME_1_1_V2 = 106
    ULTRA_WIDESCREEN_21_9_V2 = 105
    TRADITIONAL_4_3_V2 = 100
    WIDESCREEN = 0
    VERTICAL = 1
    FULL_FRAME = 2


class Gps(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#gps-83)"""

    ON = 1
    OFF = 0


class CameraVolume(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#camera-volume-216)"""

    HIGH = 100
    MEDIUM = 85
    LOW = 70


class Led(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#led-91)"""

    ALL_ON = 3
    ALL_OFF = 4
    FRONT_OFF_ONLY = 5
    BACK_ONLY = 100
    ON = 2
    OFF = 0


class SetupScreenSaver(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-screen-saver-219)"""

    NUM_1_MIN = 1
    NUM_2_MIN = 2
    NUM_3_MIN = 3
    NUM_5_MIN = 4


class SetupLanguage(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-language-223)"""

    CHINESE = 8
    ENGLISH_AUS = 2
    ENGLISH_IND = 13
    ENGLISH_UK = 1
    ENGLISH_US = 0
    FRENCH = 4
    GERMAN = 3
    ITALIAN = 5
    JAPANESE = 9
    KOREAN = 10
    PORTUGUESE = 11
    RUSSIAN = 12
    SPANISH = 6
    SPANISH_NA = 7
    SWEDISH = 14


class PhotoMode(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-mode-227)"""

    SUPERPHOTO = 0
    NIGHT_PHOTO = 1
    BURST = 2


class VideoFraming(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-framing-232)"""

    NUM_4_3 = 0
    NUM_16_9 = 1
    NUM_8_7 = 3
    NUM_9_16 = 4
    NUM_21_9 = 5
    NUM_1_1 = 6


class MultiShotFraming(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-framing-233)"""

    NUM_4_3 = 0
    NUM_16_9 = 1
    NUM_8_7 = 3
    NUM_9_16 = 4


class FrameRate(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frame-rate-234)"""

    NUM_400_0 = 15
    NUM_360_0 = 16
    NUM_300_0 = 17
    NUM_240_0 = 0
    NUM_200_0 = 13
    NUM_120_0 = 1
    NUM_100_0 = 2
    NUM_60_0 = 5
    NUM_50_0 = 6
    NUM_30_0 = 8
    NUM_25_0 = 9
    NUM_24_0 = 10


class VideoAspectRatio(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-aspect-ratio-108)"""

    NUM_4_3 = 0
    NUM_16_9 = 1
    NUM_8_7 = 3
    NUM_9_16 = 4
    NUM_21_9 = 5
    NUM_1_1 = 6


class VideoLens(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-lens-121)"""

    MAX_SUPERVIEW = 7
    SUPERVIEW = 3
    WIDE = 0
    LINEAR = 4
    LINEAR_HORIZON_LEVELING = 8
    NARROW = 2
    HYPERVIEW = 9
    LINEAR_HORIZON_LOCK = 10
    ULTRA_LINEAR = 14
    ULTRA_WIDE = 13
    ULTRA_SUPERVIEW = 12
    ULTRA_HYPERVIEW = 104
    MAX_HYPERVIEW = 11


class PhotoLens(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-lens-122)"""

    MAX_SUPERVIEW = 100
    WIDE = 101
    LINEAR = 102
    NARROW = 19
    NUM_13MP_ULTRA_LINEAR = 44
    NUM_13MP_ULTRA_WIDE = 40
    ULTRA_WIDE_12_MP = 41
    WIDE_12_MP = 0
    NUM_13MP_WIDE = 39
    WIDE_23_MP = 27
    WIDE_27_MP = 31
    LINEAR_27_MP = 32
    NUM_13MP_LINEAR = 38
    LINEAR_23_MP = 28
    LINEAR_12_MP = 10


class TimeLapseDigitalLenses(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#time-lapse-digital-lenses-123)"""

    WIDE = 101
    LINEAR = 102
    NARROW = 19
    WIDE_27_MP = 31
    LINEAR_27_MP = 32
    MAX_SUPERVIEW = 100


class PhotoOutput(GoProIntEnum):
    """See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-output-125)"""

    SUPERPHOTO = 3
    HDR = 2
    STANDARD = 0
    RAW = 1
