package entity.queries

/************************************************************************************************************
 *
 *
 * WARNING!!! This file is auto-generated. Do not modify it manually
 *
 *
 */

import util.extensions.asInt64UB

enum class SettingId(override val value: UByte) : IValuedEnum<UByte> {
    VIDEO_RESOLUTION(2U),
    FRAMES_PER_SECOND(3U),
    VIDEO_TIMELAPSE_RATE(5U),
    VIDEO_LOOPING_INTERVAL(6U),
    VIDEO_PROTUNE_ISO_MAX(13U),
    PHOTO_EXPOSURE_TIME(19U),
    PHOTO_PROTUNE_ISO_MAX(24U),
    PHOTO_TIMELAPSE_RATE(30U),
    MULTI_SHOT_EXPOSURE_TIME(31U),
    NIGHTLAPSE_RATE(32U),
    MULTI_SHOT_PROTUNE_ISO_MAX(37U),
    BROADCAST_RESOLUTION(41U),
    FRAME_PER_SECOND(42U),
    WEBCAM_DIGITAL_LENSES(43U),
    BNR_RESOLUTION(44U),
    BNR_FRAME_PER_SECOND(45U),
    BROADCAST_WINDOW_SIZE(47U),
    PRIVACY(48U),
    QUICK_CAPTURE(54U),
    AUTO_POWER_DOWN(59U),
    SECONDARY_STREAM_GOP_SIZE(60U),
    SECONDARY_STREAM_IDR_INTERVAL(61U),
    SECONDARY_STREAM_BIT_RATE(62U),
    SECONDARY_STREAM_WINDOW_SIZE(64U),
    GOP_SIZE(65U),
    IDR_INTERVAL(66U),
    BROADCAST_BIT_RATE(67U),
    PHOTO_PROTUNE_ISO_MIN(75U),
    MULTI_SHOT_PROTUNE_ISO_MIN(76U),
    AUDIO_PROTUNE(79U),
    GPS(83U),
    LANGUAGE(84U),
    VOICE_CONTROL_LANGUAGE(85U),
    SETUP_BEEP_VOLUME(86U),
    BEEPS(87U),
    LCD_BRIGHTNESS(88U),
    LED(91U),
    NO_AUDIO_TRACK(96U),
    VIDEO_PROTUNE_ISO_MIN(102U),
    AUTO_LOCK(103U),
    WAKE_ON_VOICE(104U),
    TIMER(105U),
    VIDEO_COMPRESSION(106U),
    VIDEO_ASPECT_RATIO(108U),
    SPEED(111U),
    SETUP_LANDSCAPE_LOCK(112U),
    PROTUNE(114U),
    WHITE_BALANCE(115U),
    COLOR(116U),
    SHARPNESS(117U),
    EV_COMP(118U),
    VIDEO_LENS(121U),
    PHOTO_LENS(122U),
    TIME_LAPSE_DIGITAL_LENSES(123U),
    VIDEO_BIT_RATE_LEGACY_(124U),
    PHOTO_OUTPUT(125U),
    MULTI_SHOT_OUTPUT(126U),
    MEDIA_FORMAT(128U),
    LOWER_LEFT(129U),
    LOWER_RIGHT(130U),
    UPPER_LEFT(131U),
    UPPER_RIGHT(132U),
    MEGAPIXELS(133U),
    ANTI_FLICKER(134U),
    HYPERSMOOTH(135U),
    MICS(137U),
    NUM_360_AUDIO(138U),
    RAW_AUDIO(139U),
    QUIKCAPTURE_DEFAULT(141U),
    SPHERICAL_LENS(143U),
    MODE(144U),
    VIDEO_SHUTTER(145U),
    PHOTO_SHUTTER(146U),
    BURST_RATE(147U),
    MAX_HYPERSMOOTH(148U),
    WIND(149U),
    VIDEO_HORIZON_LEVELING(150U),
    PHOTO_HORIZON_LEVELING(151U),
    MODE_BUTTON(153U),
    FRONT_LCD_MODE(154U),
    SPEED_RAMP(155U),
    VIDEO_DURATION(156U),
    MULTI_SHOT_DURATION(157U),
    SCREEN_SAVER_FRONT(158U),
    SCREEN_SAVER_REAR(159U),
    MULTI_SHOT_BIT_RATE(160U),
    DEFAULT_PRESET(161U),
    MAX_LENS(162U),
    SETUP_LENS_DASHBOARD_BUTTON(163U),
    MEDIA_MOD(164U),
    VIDEO_HORIZON_LOCK(165U),
    PHOTO_HORIZON_LOCK(166U),
    HINDSIGHT(167U),
    SCHEDULED_CAPTURE(168U),
    MODS(169U),
    PHOTO_SINGLE_INTERVAL(171U),
    PHOTO_INTERVAL_DURATION(172U),
    VIDEO_PERFORMANCE_MODE(173U),
    NUM_10_BIT(174U),
    CONTROLS(175U),
    EASY_MODE_SPEED(176U),
    ENABLE_NIGHT_PHOTO(177U),
    WIRELESS_BAND(178U),
    STAR_TRAILS_LENGTH(179U),
    SYSTEM_VIDEO_MODE(180U),
    NIGHT_PHOTO(181U),
    VIDEO_BIT_RATE(182U),
    BIT_DEPTH(183U),
    PROFILES(184U),
    VIDEO_EASY_MODE(186U),
    LAPSE_MODE(187U),
    MAX_LENS_MOD(189U),
    MAX_LENS_MOD_ENABLE(190U),
    EASY_NIGHT_PHOTO(191U),
    MULTI_SHOT_ASPECT_RATIO(192U),
    FRAMING(193U),
    CAMERA_MODE(194U),
    REGIONAL_FORMAT(195U),
    NUM_360_PHOTO_FILES_EXTENSION(196U),
    SINGLE_LENS_EXPOSURE(197U),
    DENOISE(198U),
    HLG_HDR(199U),
    FOCUS_PEAKING(200U),
    QUALITY_CONTROL(201U),
    FOCUS_PEAKING_HIGH_SENSITIVITY(202U),
    AUDIO_TUNING(203U),
    BATTERY_SAVER(204U),
    PRESET_DASHBOARD_OVERRIDE(205U),
    VOICE_COMMANDS(206U),
    SCREEN_SAVER(207U),
    GENERAL_BEEP_ENABLE(208U),
    GENERAL_LOCKED_ORIENTATION(209U),
    FRONT_DISPLAY(210U),
    SCREEN_LOCK(211U),
    LEDS(212U),
    VIDEO_ANTI_FLICKER(213U),
    WIND_SUPPRESSION(214U),
    EXTERNAL_MICS(215U),
    CAMERA_VOLUME(216U),
    LENS_ATTACHMENT(217U),
    MOTION_BLUR(218U),
    SETUP_SCREEN_SAVER(219U),
    DASHBOARD_SCREEN_SAVER(220U),
    DASHBOARD_BEEPS(221U),
    DASHBOARD_LEDS(222U),
    SETUP_LANGUAGE(223U),
    SETUP_BRIGHTNESS(224U),
    AUTO_POWER_OFF(225U),
    SETUP_AUTO_LOCK(226U),
    PHOTO_MODE(227U),
    GLOBAL_DASHBOARD_FRONT_DISPLAY(228U),
    VIDEO_DIGITAL_LENSES_V2(229U),
    PHOTO_DIGITAL_LENSES_V2(230U),
    TIME_LAPSE_DIGITAL_LENSES_V2(231U),
    VIDEO_FRAMING(232U),
    MULTI_SHOT_FRAMING(233U),
    FRAME_RATE(234U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SettingId> {
        override fun fromUByteArray(value: UByteArray) = entries.first { it.value == value.last() }
    }
}



/**
 * Video Resolution
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Resolution-2)
 *
 * @property value
 */
enum class VideoResolution(override val value: UByte) : IValuedEnum<UByte> {
    NUM_5K(24U),
    NUM_4K(1U),
    NUM_4K_4_3(18U),
    NUM_2_7K(4U),
    NUM_2_7K_4_3(6U),
    NUM_1440(7U),
    NUM_1080(9U),
    NUM_5_3K(100U),
    NUM_5K_4_3(25U),
    NUM_4K_9_16_V2(109U),
    NUM_1080_9_16_V2(110U),
    NUM_8K(31U),
    NUM_5_6K(21U),
    NUM_4K_SPH(39U),
    NUM_5_3K_4_3(27U),
    NUM_5_3K_8_7(26U),
    NUM_4K_8_7(28U),
    NUM_5_3K_8_7_V2(107U),
    NUM_4K_8_7_V2(108U),
    NUM_2_7K_4_3_V2(111U),
    NUM_5_3K_21_9(35U),
    NUM_4K_21_9(36U),
    NUM_4K_1_1(37U),
    NUM_900(38U),
    NUM_720(12U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoResolution> {
        override fun fromUByteArray(value: UByteArray) = VideoResolution.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Frames Per Second
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Frames-Per-Second-3)
 *
 * @property value
 */
enum class FramesPerSecond(override val value: UByte) : IValuedEnum<UByte> {
    NUM_240_0(0U),
    NUM_200_0(13U),
    NUM_120_0(1U),
    NUM_100_0(2U),
    NUM_60_0(5U),
    NUM_50_0(6U),
    NUM_30_0(8U),
    NUM_25_0(9U),
    NUM_24_0(10U),
    NUM_90_0(3U),
    NUM_400_0(15U),
    NUM_360_0(16U),
    NUM_300_0(17U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<FramesPerSecond> {
        override fun fromUByteArray(value: UByteArray) = FramesPerSecond.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Timelapse Rate
 *
 * How frequently to take a video when performing a Video Timelapse
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Timelapse-Rate-5)
 *
 * @property value
 */
enum class VideoTimelapseRate(override val value: UByte) : IValuedEnum<UByte> {
    NUM_60_MINUTES(10U),
    NUM_30_MINUTES(9U),
    NUM_5_MINUTES(8U),
    NUM_2_MINUTES(7U),
    NUM_60_SECONDS(6U),
    NUM_30_SECONDS(5U),
    NUM_10_SECONDS(4U),
    NUM_5_SECONDS(3U),
    NUM_2_SECONDS(2U),
    NUM_1_SECOND(1U),
    NUM_0_5_SECONDS(0U),
    NUM_3_SECONDS(11U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoTimelapseRate> {
        override fun fromUByteArray(value: UByteArray) = VideoTimelapseRate.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Looping Interval
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Looping-Interval-6)
 *
 * @property value
 */
enum class VideoLoopingInterval(override val value: UByte) : IValuedEnum<UByte> {
    MAX(0U),
    NUM_120_MINUTES(4U),
    NUM_60_MINUTES(3U),
    NUM_20_MINUTES(2U),
    NUM_5_MINUTES(1U),
    NUM_30_MINUTES(9U),
    NUM_10_MINUTES(7U),
    NUM_3_MINUTES(6U),
    NUM_1_MINUTE(5U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoLoopingInterval> {
        override fun fromUByteArray(value: UByteArray) = VideoLoopingInterval.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Protune ISO Max
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Protune-ISO-Max-13)
 *
 * @property value
 */
enum class VideoProtuneIsoMax(override val value: UByte) : IValuedEnum<UByte> {
    NUM_6400_0(0U),
    NUM_3200_0(3U),
    NUM_1600_0(1U),
    NUM_800_0(4U),
    NUM_400_0(2U),
    NUM_200_0(7U),
    NUM_100_0(8U),
    AUTO(9U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoProtuneIsoMax> {
        override fun fromUByteArray(value: UByteArray) = VideoProtuneIsoMax.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Exposure Time
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Exposure-Time-19)
 *
 * @property value
 */
enum class PhotoExposureTime(override val value: UByte) : IValuedEnum<UByte> {
    NUM_30_SECONDS(6U),
    NUM_20_SECONDS(5U),
    NUM_15_SECONDS(4U),
    NUM_10_SECONDS(3U),
    NUM_5_SECONDS(2U),
    NUM_2_SECONDS(1U),
    AUTO(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoExposureTime> {
        override fun fromUByteArray(value: UByteArray) = PhotoExposureTime.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Protune ISO Max
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Protune-ISO-Max-24)
 *
 * @property value
 */
enum class PhotoProtuneIsoMax(override val value: UByte) : IValuedEnum<UByte> {
    NUM_3200_0(5U),
    NUM_1600_0(4U),
    NUM_800_0(0U),
    NUM_400_0(1U),
    NUM_200_0(2U),
    NUM_100_0(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoProtuneIsoMax> {
        override fun fromUByteArray(value: UByteArray) = PhotoProtuneIsoMax.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Timelapse Rate
 *
 * How frequently to take a photo when performing a Photo Timelapse.
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Timelapse-Rate-30)
 *
 * @property value
 */
enum class PhotoTimelapseRate(override val value: ULong) : IValuedEnum<ULong> {
    NUM_60_MINUTES(100U),
    NUM_30_MINUTES(101U),
    NUM_5_MINUTES(102U),
    NUM_2_MINUTES(103U),
    NUM_60_SECONDS(104U),
    NUM_30_SECONDS(105U),
    NUM_10_SECONDS(106U),
    NUM_5_SECONDS(107U),
    NUM_2_SECONDS(108U),
    NUM_1_SECOND(109U),
    NUM_0_5_SECONDS(110U),
    NUM_3_SECONDS(11U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoTimelapseRate> {
        override fun fromUByteArray(value: UByteArray) = PhotoTimelapseRate.entries.first {
            it.value == value.asInt64UB()
        }
    }
}

/**
 * Multi Shot Exposure Time
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Exposure-Time-31)
 *
 * @property value
 */
enum class MultiShotExposureTime(override val value: UByte) : IValuedEnum<UByte> {
    NUM_30_SECONDS(6U),
    NUM_20_SECONDS(5U),
    NUM_15_SECONDS(4U),
    NUM_10_SECONDS(3U),
    NUM_5_SECONDS(2U),
    NUM_2_SECONDS(1U),
    AUTO(0U),
    NUM_1_SECOND(8U),
    NUM_0_5_SECONDS(7U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MultiShotExposureTime> {
        override fun fromUByteArray(value: UByteArray) = MultiShotExposureTime.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Nightlapse Rate
 *
 * How frequently to take a video or photo when performing a Nightlapse.
 *
 * This controls the Video or Photo Nightlapse rate if Setting 128 is set to 21 or 26 respectively.
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Nightlapse-Rate-32)
 *
 * @property value
 */
enum class NightlapseRate(override val value: ULong) : IValuedEnum<ULong> {
    NUM_60_MINUTES(3600U),
    NUM_30_MINUTES(1800U),
    NUM_5_MINUTES(300U),
    NUM_2_MINUTES(120U),
    NUM_60_SECONDS(100U),
    NUM_30_SECONDS(30U),
    NUM_20_SECONDS(20U),
    NUM_15_SECONDS(15U),
    NUM_10_SECONDS(10U),
    NUM_5_SECONDS(5U),
    NUM_4_SECONDS(4U),
    AUTO(3601U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<NightlapseRate> {
        override fun fromUByteArray(value: UByteArray) = NightlapseRate.entries.first {
            it.value == value.asInt64UB()
        }
    }
}

/**
 * Multi Shot Protune ISO Max
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Protune-ISO-Max-37)
 *
 * @property value
 */
enum class MultiShotProtuneIsoMax(override val value: UByte) : IValuedEnum<UByte> {
    NUM_3200_0(5U),
    NUM_1600_0(4U),
    NUM_800_0(0U),
    NUM_400_0(1U),
    NUM_200_0(2U),
    NUM_100_0(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MultiShotProtuneIsoMax> {
        override fun fromUByteArray(value: UByteArray) = MultiShotProtuneIsoMax.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Broadcast Resolution
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Broadcast-Resolution-41)
 *
 * @property value
 */
enum class BroadcastResolution(override val value: UByte) : IValuedEnum<UByte> {
    NUM_1080_0(9U),
    NUM_720_0(12U),
    NUM_480_0(17U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<BroadcastResolution> {
        override fun fromUByteArray(value: UByteArray) = BroadcastResolution.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Frame Per Second
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Frame-Per-Second-42)
 *
 * @property value
 */
enum class FramePerSecond(override val value: UByte) : IValuedEnum<UByte> {
    NUM_30_0(8U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<FramePerSecond> {
        override fun fromUByteArray(value: UByteArray) = FramePerSecond.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Webcam Digital Lenses
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Webcam-Digital-Lenses-43)
 *
 * @property value
 */
enum class WebcamDigitalLenses(override val value: UByte) : IValuedEnum<UByte> {
    SUPERVIEW(3U),
    WIDE(0U),
    LINEAR(4U),
    NARROW(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<WebcamDigitalLenses> {
        override fun fromUByteArray(value: UByteArray) = WebcamDigitalLenses.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * BNR Resolution
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#BNR-Resolution-44)
 *
 * @property value
 */
enum class BnrResolution(override val value: UByte) : IValuedEnum<UByte> {
    NUM_1080_0(9U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<BnrResolution> {
        override fun fromUByteArray(value: UByteArray) = BnrResolution.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * BNR Frame Per Second
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#BNR-Frame-Per-Second-45)
 *
 * @property value
 */
enum class BnrFramePerSecond(override val value: UByte) : IValuedEnum<UByte> {
    NUM_30_0(8U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<BnrFramePerSecond> {
        override fun fromUByteArray(value: UByteArray) = BnrFramePerSecond.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Broadcast Window Size
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Broadcast-Window-Size-47)
 *
 * @property value
 */
enum class BroadcastWindowSize(override val value: UByte) : IValuedEnum<UByte> {
    NUM_480_0(4U),
    NUM_720_0(7U),
    NUM_1080_0(12U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<BroadcastWindowSize> {
        override fun fromUByteArray(value: UByteArray) = BroadcastWindowSize.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Privacy
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Privacy-48)
 *
 * @property value
 */
enum class Privacy(override val value: UByte) : IValuedEnum<UByte> {
    ASK(0U),
    PUBLIC(1U),
    HIDDEN(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Privacy> {
        override fun fromUByteArray(value: UByteArray) = Privacy.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Quick Capture
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Quick-Capture-54)
 *
 * @property value
 */
enum class QuickCapture(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<QuickCapture> {
        override fun fromUByteArray(value: UByteArray) = QuickCapture.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Auto Power Down
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Auto-Power-Down-59)
 *
 * @property value
 */
enum class AutoPowerDown(override val value: UByte) : IValuedEnum<UByte> {
    NUM_5_MIN(4U),
    NUM_15_MIN(6U),
    NUM_30_MIN(7U),
    NEVER(0U),
    NUM_1_MIN(1U),
    NUM_8_SECONDS(11U),
    NUM_30_SECONDS(12U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<AutoPowerDown> {
        override fun fromUByteArray(value: UByteArray) = AutoPowerDown.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Secondary Stream GOP Size
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Secondary-Stream-GOP-Size-60)
 *
 * @property value
 */
enum class SecondaryStreamGopSize(override val value: UByte) : IValuedEnum<UByte> {
    DEFAULT(0U),
    NUM_3_0(3U),
    NUM_4_0(4U),
    NUM_8_0(8U),
    NUM_15_0(15U),
    NUM_30_0(30U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SecondaryStreamGopSize> {
        override fun fromUByteArray(value: UByteArray) = SecondaryStreamGopSize.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Secondary Stream IDR Interval
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Secondary-Stream-IDR-Interval-61)
 *
 * @property value
 */
enum class SecondaryStreamIdrInterval(override val value: UByte) : IValuedEnum<UByte> {
    DEFAULT(0U),
    NUM_1_0(1U),
    NUM_2_0(2U),
    NUM_4_0(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SecondaryStreamIdrInterval> {
        override fun fromUByteArray(value: UByteArray) = SecondaryStreamIdrInterval.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Secondary Stream Bit Rate
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Secondary-Stream-Bit-Rate-62)
 *
 * @property value
 */
enum class SecondaryStreamBitRate(override val value: ULong) : IValuedEnum<ULong> {
    NUM_250_KBPS(250000U),
    NUM_400_KBPS(400000U),
    NUM_600_KBPS(600000U),
    NUM_700_KBPS(700000U),
    NUM_800_KBPS(800000U),
    NUM_1_MBPS(1000000U),
    NUM_1_2_MBPS(1200000U),
    NUM_1_6_MBPS(1600000U),
    NUM_2_MBPS(2000000U),
    NUM_2_4_MBPS(2400000U),
    NUM_2_5_MBPS(2500000U),
    NUM_4_MBPS(4000000U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SecondaryStreamBitRate> {
        override fun fromUByteArray(value: UByteArray) = SecondaryStreamBitRate.entries.first {
            it.value == value.asInt64UB()
        }
    }
}

/**
 * Secondary Stream Window Size
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Secondary-Stream-Window-Size-64)
 *
 * @property value
 */
enum class SecondaryStreamWindowSize(override val value: UByte) : IValuedEnum<UByte> {
    DEFAULT(0U),
    NUM_240_0(1U),
    NUM_240_3_4_SUBSAMPLE(2U),
    NUM_240_1_2_SUBSAMPLE(3U),
    NUM_480_0(4U),
    NUM_480_3_4_SUBSAMPLE(5U),
    NUM_480_1_2_SUBSAMPLE(6U),
    NUM_720_0(7U),
    NUM_720_3_4_SUBSAMPLE(8U),
    NUM_720_1_2_SUBSAMPLE(9U),
    NUM_720_SQUARE(10U),
    NUM_480_SQUARE(11U),
    NUM_1080_0(12U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SecondaryStreamWindowSize> {
        override fun fromUByteArray(value: UByteArray) = SecondaryStreamWindowSize.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * GOP Size
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#GOP-Size-65)
 *
 * @property value
 */
enum class GopSize(override val value: UByte) : IValuedEnum<UByte> {
    DEFAULT(0U),
    NUM_3_0(3U),
    NUM_4_0(4U),
    NUM_8_0(8U),
    NUM_15_0(15U),
    NUM_30_0(30U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<GopSize> {
        override fun fromUByteArray(value: UByteArray) = GopSize.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * IDR Interval
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#IDR-Interval-66)
 *
 * @property value
 */
enum class IdrInterval(override val value: UByte) : IValuedEnum<UByte> {
    DEFAULT(0U),
    NUM_1_0(1U),
    NUM_2_0(2U),
    NUM_4_0(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<IdrInterval> {
        override fun fromUByteArray(value: UByteArray) = IdrInterval.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Broadcast Bit Rate
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Broadcast-Bit-Rate-67)
 *
 * @property value
 */
enum class BroadcastBitRate(override val value: ULong) : IValuedEnum<ULong> {
    NUM_250_KBPS(250000U),
    NUM_400_KBPS(400000U),
    NUM_600_KBPS(600000U),
    NUM_700_KBPS(700000U),
    NUM_800_KBPS(800000U),
    NUM_1_MBPS(1000000U),
    NUM_1_2_MBPS(1200000U),
    NUM_1_6_MBPS(1600000U),
    NUM_2_MBPS(2000000U),
    NUM_2_4_MBPS(2400000U),
    NUM_2_5_MBPS(2500000U),
    NUM_4_MBPS(4000000U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<BroadcastBitRate> {
        override fun fromUByteArray(value: UByteArray) = BroadcastBitRate.entries.first {
            it.value == value.asInt64UB()
        }
    }
}

/**
 * Photo Protune ISO Min
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Protune-ISO-Min-75)
 *
 * @property value
 */
enum class PhotoProtuneIsoMin(override val value: UByte) : IValuedEnum<UByte> {
    NUM_3200_0(5U),
    NUM_1600_0(4U),
    NUM_800_0(0U),
    NUM_400_0(1U),
    NUM_200_0(2U),
    NUM_100_0(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoProtuneIsoMin> {
        override fun fromUByteArray(value: UByteArray) = PhotoProtuneIsoMin.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Multi Shot Protune ISO Min
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Protune-ISO-Min-76)
 *
 * @property value
 */
enum class MultiShotProtuneIsoMin(override val value: UByte) : IValuedEnum<UByte> {
    NUM_3200_0(5U),
    NUM_1600_0(4U),
    NUM_800_0(0U),
    NUM_400_0(1U),
    NUM_200_0(2U),
    NUM_100_0(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MultiShotProtuneIsoMin> {
        override fun fromUByteArray(value: UByteArray) = MultiShotProtuneIsoMin.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Audio Protune
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Audio-Protune-79)
 *
 * @property value
 */
enum class AudioProtune(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<AudioProtune> {
        override fun fromUByteArray(value: UByteArray) = AudioProtune.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * GPS
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#GPS-83)
 *
 * @property value
 */
enum class Gps(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Gps> {
        override fun fromUByteArray(value: UByteArray) = Gps.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Language
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Language-84)
 *
 * @property value
 */
enum class Language(override val value: UByte) : IValuedEnum<UByte> {
    ENGLISH(0U),
    FRENCH(6U),
    GERMAN(2U),
    ITALIAN(3U),
    SPANISH(4U),
    CHINESE(1U),
    JAPANESE(5U),
    KOREAN(7U),
    PORTUGUESE(8U),
    RUSSIAN(9U),
    SWEDISH(10U),
    CHINESE_TRADITIONAL_(11U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Language> {
        override fun fromUByteArray(value: UByteArray) = Language.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Voice Control Language
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Voice-Control-Language-85)
 *
 * @property value
 */
enum class VoiceControlLanguage(override val value: UByte) : IValuedEnum<UByte> {
    CHINESE(8U),
    ENGLISH_AUS(2U),
    ENGLISH_IND(13U),
    ENGLISH_UK(1U),
    ENGLISH_US(0U),
    FRENCH(4U),
    GERMAN(3U),
    ITALIAN(5U),
    JAPANESE(9U),
    KOREAN(10U),
    PORTUGUESE(11U),
    RUSSIAN(12U),
    SPANISH(6U),
    SPANISH_NA(7U),
    SWEDISH(14U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VoiceControlLanguage> {
        override fun fromUByteArray(value: UByteArray) = VoiceControlLanguage.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Setup Beep Volume
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Beep-Volume-86)
 *
 * @property value
 */
enum class SetupBeepVolume(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SetupBeepVolume> {
        override fun fromUByteArray(value: UByteArray) = SetupBeepVolume.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Beeps
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Beeps-87)
 *
 * @property value
 */
enum class Beeps(override val value: UByte) : IValuedEnum<UByte> {
    HIGH(100U),
    MEDIUM(70U),
    LOW(40U),
    MUTE(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Beeps> {
        override fun fromUByteArray(value: UByteArray) = Beeps.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * LCD Brightness
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#LCD-Brightness-88)
 *
 * @property value
 */
enum class LcdBrightness(override val value: UByte) : IValuedEnum<UByte> {
    NUM_10_(10U),
    NUM_20_(20U),
    NUM_30_(30U),
    NUM_40_(40U),
    NUM_50_(50U),
    NUM_60_(60U),
    NUM_70_(70U),
    NUM_80_(80U),
    NUM_90_(90U),
    NUM_100_(100U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<LcdBrightness> {
        override fun fromUByteArray(value: UByteArray) = LcdBrightness.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * LED
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#LED-91)
 *
 * @property value
 */
enum class Led(override val value: UByte) : IValuedEnum<UByte> {
    ALL_ON(3U),
    ALL_OFF(4U),
    FRONT_OFF_ONLY(5U),
    ON(2U),
    OFF(0U),
    BACK_ONLY(100U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Led> {
        override fun fromUByteArray(value: UByteArray) = Led.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * No Audio Track
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#No-Audio-Track-96)
 *
 * @property value
 */
enum class NoAudioTrack(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<NoAudioTrack> {
        override fun fromUByteArray(value: UByteArray) = NoAudioTrack.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Protune ISO Min
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Protune-ISO-Min-102)
 *
 * @property value
 */
enum class VideoProtuneIsoMin(override val value: UByte) : IValuedEnum<UByte> {
    NUM_6400_0(0U),
    NUM_3200_0(3U),
    NUM_1600_0(1U),
    NUM_800_0(4U),
    NUM_400_0(2U),
    NUM_200_0(7U),
    NUM_100_0(8U),
    AUTO(9U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoProtuneIsoMin> {
        override fun fromUByteArray(value: UByteArray) = VideoProtuneIsoMin.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Auto Lock
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Auto-Lock-103)
 *
 * @property value
 */
enum class AutoLock(override val value: UByte) : IValuedEnum<UByte> {
    OFF(3U),
    NUM_10_SECONDS(6U),
    ON(100U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<AutoLock> {
        override fun fromUByteArray(value: UByteArray) = AutoLock.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Wake On Voice
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Wake-On-Voice-104)
 *
 * @property value
 */
enum class WakeOnVoice(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<WakeOnVoice> {
        override fun fromUByteArray(value: UByteArray) = WakeOnVoice.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Timer
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Timer-105)
 *
 * @property value
 */
enum class Timer(override val value: UByte) : IValuedEnum<UByte> {
    NUM_10_SECONDS(2U),
    NUM_3_SECONDS(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Timer> {
        override fun fromUByteArray(value: UByteArray) = Timer.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Compression
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Compression-106)
 *
 * @property value
 */
enum class VideoCompression(override val value: UByte) : IValuedEnum<UByte> {
    HEVC(1U),
    H_264_HEVC(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoCompression> {
        override fun fromUByteArray(value: UByteArray) = VideoCompression.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Aspect Ratio
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Aspect-Ratio-108)
 *
 * @property value
 */
enum class VideoAspectRatio(override val value: UByte) : IValuedEnum<UByte> {
    NUM_4_3(0U),
    NUM_16_9(1U),
    NUM_9_16(4U),
    NUM_8_7(3U),
    NUM_21_9(5U),
    NUM_1_1(6U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoAspectRatio> {
        override fun fromUByteArray(value: UByteArray) = VideoAspectRatio.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Speed
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Speed-111)
 *
 * @property value
 */
enum class Speed(override val value: UByte) : IValuedEnum<UByte> {
    NUM_30X(1U),
    NUM_15X(0U),
    NUM_10X(9U),
    NUM_5X(8U),
    NUM_2X(7U),
    AUTO(10U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Speed> {
        override fun fromUByteArray(value: UByteArray) = Speed.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Setup Landscape Lock
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Landscape-Lock-112)
 *
 * @property value
 */
enum class SetupLandscapeLock(override val value: UByte) : IValuedEnum<UByte> {
    ALL(100U),
    LANDSCAPE(5U),
    LOCKED(255U),
    LOCKED_0(101U),
    LOCKED_90(104U),
    LOCKED_180(102U),
    LOCKED_270(103U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SetupLandscapeLock> {
        override fun fromUByteArray(value: UByteArray) = SetupLandscapeLock.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Protune
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Protune-114)
 *
 * @property value
 */
enum class Protune(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Protune> {
        override fun fromUByteArray(value: UByteArray) = Protune.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * White Balance
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#White-Balance-115)
 *
 * @property value
 */
enum class WhiteBalance(override val value: UByte) : IValuedEnum<UByte> {
    NUM_6500K(3U),
    NUM_6000K(7U),
    NUM_5500K(2U),
    NUM_5000K(12U),
    NUM_4500K(11U),
    AUTO(0U),
    NATIVE(4U),
    NUM_4000K(5U),
    NUM_3200K(10U),
    NUM_2800K(9U),
    NUM_2300K(8U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<WhiteBalance> {
        override fun fromUByteArray(value: UByteArray) = WhiteBalance.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Color
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Color-116)
 *
 * @property value
 */
enum class Color(override val value: UByte) : IValuedEnum<UByte> {
    FLAT(1U),
    GOPRO(0U),
    VIBRANT(100U),
    NATURAL(2U),
    LOG(3U),
    GP_LOG(101U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Color> {
        override fun fromUByteArray(value: UByteArray) = Color.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Sharpness
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Sharpness-117)
 *
 * @property value
 */
enum class Sharpness(override val value: UByte) : IValuedEnum<UByte> {
    HIGH(0U),
    MEDIUM(1U),
    LOW(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Sharpness> {
        override fun fromUByteArray(value: UByteArray) = Sharpness.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * EV Comp
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#EV-Comp-118)
 *
 * @property value
 */
enum class EvComp(override val value: UByte) : IValuedEnum<UByte> {
    NEG_2_0(8U),
    NEG_1_5(7U),
    NEG_1_0(6U),
    NEG_0_5(5U),
    NUM_0_0(4U),
    NUM_0_5(3U),
    NUM_1_0(2U),
    NUM_1_5(1U),
    NUM_2_0(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<EvComp> {
        override fun fromUByteArray(value: UByteArray) = EvComp.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Lens
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Lens-121)
 *
 * @property value
 */
enum class VideoLens(override val value: UByte) : IValuedEnum<UByte> {
    MAX_SUPERVIEW(7U),
    SUPERVIEW(3U),
    WIDE(0U),
    LINEAR(4U),
    LINEAR_HORIZON_LEVELING(8U),
    NARROW(2U),
    ULTRA_WIDE(13U),
    MAX_HYPERVIEW(11U),
    HYPERVIEW(9U),
    LINEAR_HORIZON_LOCK(10U),
    ULTRA_LINEAR(14U),
    ULTRA_SUPERVIEW(12U),
    ULTRA_HYPERVIEW(104U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoLens> {
        override fun fromUByteArray(value: UByteArray) = VideoLens.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Lens
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Lens-122)
 *
 * @property value
 */
enum class PhotoLens(override val value: UByte) : IValuedEnum<UByte> {
    MAX_SUPERVIEW(100U),
    WIDE(101U),
    LINEAR(102U),
    NARROW(19U),
    ULTRA_WIDE_12_MP(41U),
    NUM_9MP_WIDE(15U),
    NUM_9MP_LINEAR(37U),
    NUM_17MP_ULTRA_LINEAR(48U),
    NUM_17MP_ULTRA_WIDE(47U),
    WIDE_12_MP(0U),
    NUM_17MP_WIDE(46U),
    WIDE_23_MP(27U),
    WIDE_27_MP(31U),
    LINEAR_27_MP(32U),
    NUM_17MP_LINEAR(45U),
    LINEAR_23_MP(28U),
    LINEAR_12_MP(10U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoLens> {
        override fun fromUByteArray(value: UByteArray) = PhotoLens.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Time Lapse Digital Lenses
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Time-Lapse-Digital-Lenses-123)
 *
 * @property value
 */
enum class TimeLapseDigitalLenses(override val value: UByte) : IValuedEnum<UByte> {
    WIDE(101U),
    LINEAR(102U),
    NARROW(19U),
    MAX_SUPERVIEW(100U),
    WIDE_27_MP(31U),
    LINEAR_27_MP(32U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<TimeLapseDigitalLenses> {
        override fun fromUByteArray(value: UByteArray) = TimeLapseDigitalLenses.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Bit Rate (Legacy)
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Bit-Rate-(Legacy)-124)
 *
 * @property value
 */
enum class VideoBitRate_Legacy_(override val value: UByte) : IValuedEnum<UByte> {
    HIGH(1U),
    LOW(0U),
    STANDARD(100U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoBitRate_Legacy_> {
        override fun fromUByteArray(value: UByteArray) = VideoBitRate_Legacy_.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Output
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Output-125)
 *
 * @property value
 */
enum class PhotoOutput(override val value: UByte) : IValuedEnum<UByte> {
    SUPERPHOTO(3U),
    HDR(2U),
    STANDARD(0U),
    RAW(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoOutput> {
        override fun fromUByteArray(value: UByteArray) = PhotoOutput.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Multi Shot Output
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Output-126)
 *
 * @property value
 */
enum class MultiShotOutput(override val value: UByte) : IValuedEnum<UByte> {
    STANDARD(0U),
    RAW(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MultiShotOutput> {
        override fun fromUByteArray(value: UByteArray) = MultiShotOutput.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Media Format
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Media-Format-128)
 *
 * @property value
 */
enum class MediaFormat(override val value: UByte) : IValuedEnum<UByte> {
    TIME_LAPSE_VIDEO(13U),
    TIME_LAPSE_PHOTO(20U),
    NIGHT_LAPSE_PHOTO(21U),
    NIGHT_LAPSE_VIDEO(26U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MediaFormat> {
        override fun fromUByteArray(value: UByteArray) = MediaFormat.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Lower Left
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Lower-Left-129)
 *
 * @property value
 */
enum class LowerLeft(override val value: UByte) : IValuedEnum<UByte> {
    HORIZON_LOCK(107U),
    WIND(100U),
    MEDIA_MOD(106U),
    RAW_AUDIO(18U),
    COLOR(10U),
    SHARPNESS(19U),
    ISO_MAX(15U),
    ISO_MIN(14U),
    WHITE_BALANCE(5U),
    EV_COMP(11U),
    SHUTTER(6U),
    BIT_RATE(7U),
    ZOOM(1U),
    TIMER(20U),
    BURST_RATE(8U),
    HINDSIGHT(105U),
    DURATION(102U),
    SCHEDULED_CAPTURE(104U),
    HYPERSMOOTH_BOOST(108U),
    SPEED_RAMP(103U),
    SPEED(21U),
    OUTPUT(17U),
    INTERVAL(13U),
    LOOPING_INTERVAL(109U),
    LENS(2U),
    SLO_MO(3U),
    OFF(0U),
    HYPERSMOOTH(12U),
    BIT_DEPTH(113U),
    NUM_360_AUDIO(101U),
    ASPECT_RATIO(32U),
    DIGITAL_LENS(112U),
    PHOTO_INTERVAL(31U),
    MICS(16U),
    LENS_SWAP(34U),
    SETTINGS(33U),
    SINGLE_LENS_EXPOSURE(35U),
    TRAILS_LENGTH(30U),
    VIDEO_SHUTTER(111U),
    DENOISE(38U),
    FOCUS_PEAKING(37U),
    AUDIO_TUNING(39U),
    FRAMING(114U),
    HORIZON_LEVELING(24U),
    NUM_10_BIT(28U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<LowerLeft> {
        override fun fromUByteArray(value: UByteArray) = LowerLeft.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Lower Right
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Lower-Right-130)
 *
 * @property value
 */
enum class LowerRight(override val value: UByte) : IValuedEnum<UByte> {
    HORIZON_LOCK(107U),
    WIND(100U),
    MEDIA_MOD(106U),
    RAW_AUDIO(18U),
    COLOR(10U),
    SHARPNESS(19U),
    ISO_MAX(15U),
    ISO_MIN(14U),
    WHITE_BALANCE(5U),
    EV_COMP(11U),
    SHUTTER(6U),
    BIT_RATE(7U),
    ZOOM(1U),
    TIMER(20U),
    BURST_RATE(8U),
    HINDSIGHT(105U),
    DURATION(102U),
    SCHEDULED_CAPTURE(104U),
    HYPERSMOOTH_BOOST(108U),
    SPEED_RAMP(103U),
    SPEED(21U),
    OUTPUT(17U),
    INTERVAL(13U),
    LOOPING_INTERVAL(109U),
    LENS(2U),
    SLO_MO(3U),
    OFF(0U),
    HYPERSMOOTH(12U),
    BIT_DEPTH(113U),
    NUM_360_AUDIO(101U),
    ASPECT_RATIO(32U),
    DIGITAL_LENS(112U),
    PHOTO_INTERVAL(31U),
    MICS(16U),
    LENS_SWAP(34U),
    SETTINGS(33U),
    SINGLE_LENS_EXPOSURE(35U),
    TRAILS_LENGTH(30U),
    VIDEO_SHUTTER(111U),
    DENOISE(38U),
    FOCUS_PEAKING(37U),
    AUDIO_TUNING(39U),
    FRAMING(114U),
    HORIZON_LEVELING(24U),
    NUM_10_BIT(28U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<LowerRight> {
        override fun fromUByteArray(value: UByteArray) = LowerRight.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Upper Left
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Upper-Left-131)
 *
 * @property value
 */
enum class UpperLeft(override val value: UByte) : IValuedEnum<UByte> {
    HORIZON_LOCK(107U),
    WIND(100U),
    MEDIA_MOD(106U),
    RAW_AUDIO(18U),
    COLOR(10U),
    SHARPNESS(19U),
    ISO_MAX(15U),
    ISO_MIN(14U),
    WHITE_BALANCE(5U),
    EV_COMP(11U),
    SHUTTER(6U),
    BIT_RATE(7U),
    ZOOM(1U),
    TIMER(20U),
    BURST_RATE(8U),
    HINDSIGHT(105U),
    DURATION(102U),
    SCHEDULED_CAPTURE(104U),
    HYPERSMOOTH_BOOST(108U),
    SPEED_RAMP(103U),
    SPEED(21U),
    OUTPUT(17U),
    INTERVAL(13U),
    LOOPING_INTERVAL(109U),
    LENS(2U),
    SLO_MO(3U),
    OFF(0U),
    HYPERSMOOTH(12U),
    BIT_DEPTH(113U),
    NUM_360_AUDIO(101U),
    ASPECT_RATIO(32U),
    DIGITAL_LENS(112U),
    PHOTO_INTERVAL(31U),
    MICS(16U),
    LENS_SWAP(34U),
    SETTINGS(33U),
    SINGLE_LENS_EXPOSURE(35U),
    TRAILS_LENGTH(30U),
    VIDEO_SHUTTER(111U),
    DENOISE(38U),
    FOCUS_PEAKING(37U),
    AUDIO_TUNING(39U),
    FRAMING(114U),
    HORIZON_LEVELING(24U),
    NUM_10_BIT(28U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<UpperLeft> {
        override fun fromUByteArray(value: UByteArray) = UpperLeft.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Upper Right
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Upper-Right-132)
 *
 * @property value
 */
enum class UpperRight(override val value: UByte) : IValuedEnum<UByte> {
    HORIZON_LOCK(107U),
    WIND(100U),
    MEDIA_MOD(106U),
    RAW_AUDIO(18U),
    COLOR(10U),
    SHARPNESS(19U),
    ISO_MAX(15U),
    ISO_MIN(14U),
    WHITE_BALANCE(5U),
    EV_COMP(11U),
    SHUTTER(6U),
    BIT_RATE(7U),
    ZOOM(1U),
    TIMER(20U),
    BURST_RATE(8U),
    HINDSIGHT(105U),
    DURATION(102U),
    SCHEDULED_CAPTURE(104U),
    HYPERSMOOTH_BOOST(108U),
    SPEED_RAMP(103U),
    SPEED(21U),
    OUTPUT(17U),
    INTERVAL(13U),
    LOOPING_INTERVAL(109U),
    LENS(2U),
    SLO_MO(3U),
    OFF(0U),
    HYPERSMOOTH(12U),
    BIT_DEPTH(113U),
    NUM_360_AUDIO(101U),
    ASPECT_RATIO(32U),
    DIGITAL_LENS(112U),
    PHOTO_INTERVAL(31U),
    MICS(16U),
    LENS_SWAP(34U),
    SETTINGS(33U),
    SINGLE_LENS_EXPOSURE(35U),
    TRAILS_LENGTH(30U),
    VIDEO_SHUTTER(111U),
    DENOISE(38U),
    FOCUS_PEAKING(37U),
    AUDIO_TUNING(39U),
    FRAMING(114U),
    HORIZON_LEVELING(24U),
    NUM_10_BIT(28U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<UpperRight> {
        override fun fromUByteArray(value: UByteArray) = UpperRight.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * MegaPixels
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#MegaPixels-133)
 *
 * @property value
 */
enum class Megapixels(override val value: UByte) : IValuedEnum<UByte> {
    NUM_8MP(0U),
    NUM_12MP(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Megapixels> {
        override fun fromUByteArray(value: UByteArray) = Megapixels.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Anti-Flicker
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Anti-Flicker-134)
 *
 * @property value
 */
enum class Anti_Flicker(override val value: UByte) : IValuedEnum<UByte> {
    NUM_60HZ(2U),
    NUM_50HZ(3U),
    NTSC(0U),
    PAL(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Anti_Flicker> {
        override fun fromUByteArray(value: UByteArray) = Anti_Flicker.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Hypersmooth
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Hypersmooth-135)
 *
 * @property value
 */
enum class Hypersmooth(override val value: UByte) : IValuedEnum<UByte> {
    BOOST(3U),
    HIGH(2U),
    LOW(1U),
    OFF(0U),
    STANDARD(100U),
    AUTO_BOOST(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Hypersmooth> {
        override fun fromUByteArray(value: UByteArray) = Hypersmooth.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Mics
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Mics-137)
 *
 * @property value
 */
enum class Mics(override val value: UByte) : IValuedEnum<UByte> {
    STEREO(0U),
    FRONT(1U),
    BACK(2U),
    MATCH_LENS(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Mics> {
        override fun fromUByteArray(value: UByteArray) = Mics.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * 360 Audio
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#360-Audio-138)
 *
 * @property value
 */
enum class NUM360Audio(override val value: UByte) : IValuedEnum<UByte> {
    STEREO(0U),
    NUM_360_STEREO(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<NUM360Audio> {
        override fun fromUByteArray(value: UByteArray) = NUM360Audio.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * RAW Audio
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#RAW-Audio-139)
 *
 * @property value
 */
enum class RawAudio(override val value: UByte) : IValuedEnum<UByte> {
    HIGH(2U),
    MEDIUM(1U),
    LOW(0U),
    OFF(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<RawAudio> {
        override fun fromUByteArray(value: UByteArray) = RawAudio.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * QuikCapture Default
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#QuikCapture-Default-141)
 *
 * @property value
 */
enum class QuikcaptureDefault(override val value: UByte) : IValuedEnum<UByte> {
    LAST_USED_VIDEO(102U),
    NUM_360_VIDEO(101U),
    SINGLE_LENS_VIDEO(100U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<QuikcaptureDefault> {
        override fun fromUByteArray(value: UByteArray) = QuikcaptureDefault.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Spherical Lens
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Spherical-Lens-143)
 *
 * @property value
 */
enum class SphericalLens(override val value: UByte) : IValuedEnum<UByte> {
    FRONT(0U),
    REAR(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SphericalLens> {
        override fun fromUByteArray(value: UByteArray) = SphericalLens.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Mode
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Mode-144)
 *
 * @property value
 */
enum class Mode(override val value: UByte) : IValuedEnum<UByte> {
    VIDEO(12U),
    LOOPING(15U),
    PHOTO(17U),
    NIGHT_PHOTO(18U),
    BURST_PHOTO(19U),
    TIME_LAPSE_VIDEO(13U),
    TIME_LAPSE_PHOTO(20U),
    NIGHT_LAPSE_PHOTO(21U),
    TIME_WARP_VIDEO(24U),
    LIVE_BURST(25U),
    NIGHT_LAPSE_VIDEO(26U),
    SLO_MO(27U),
    SINGLE_PHOTO(16U),
    STAR_TRAIL(29U),
    LIGHT_PAINTING(30U),
    VEHICLE_LIGHTS(31U),
    POV(33U),
    SELFIE(34U),
    BURST_SLO_MO(32U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Mode> {
        override fun fromUByteArray(value: UByteArray) = Mode.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Shutter
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Shutter-145)
 *
 * @property value
 */
enum class VideoShutter(override val value: UByte) : IValuedEnum<UByte> {
    NUM_1_3840(31U),
    NUM_1_3200(30U),
    NUM_1_1920(24U),
    NUM_1_1600(29U),
    NUM_1_960(23U),
    NUM_1_800(28U),
    NUM_1_480(22U),
    NUM_1_400(21U),
    NUM_1_384(25U),
    NUM_1_240(18U),
    NUM_1_200(17U),
    NUM_1_192(16U),
    NUM_1_120(13U),
    NUM_1_100(12U),
    NUM_1_96(11U),
    NUM_1_60(8U),
    NUM_1_50(7U),
    NUM_1_48(6U),
    NUM_1_30(5U),
    NUM_1_25(4U),
    NUM_1_24(3U),
    AUTO(0U),
    NUM_1_7680(56U),
    NUM_1_6400(51U),
    NUM_1_6144(43U),
    NUM_1_5760(55U),
    NUM_1_4800(50U),
    NUM_1_4608(42U),
    NUM_1_3072(34U),
    NUM_1_2880(54U),
    NUM_1_2400(49U),
    NUM_1_2304(41U),
    NUM_1_1536(33U),
    NUM_1_1440(53U),
    NUM_1_1200(48U),
    NUM_1_1152(40U),
    NUM_1_768(32U),
    NUM_1_720(27U),
    NUM_1_600(47U),
    NUM_1_576(39U),
    NUM_1_360(20U),
    NUM_1_300(46U),
    NUM_1_288(38U),
    NUM_1_180(15U),
    NUM_1_150(45U),
    NUM_1_144(37U),
    NUM_1_90(10U),
    NUM_1_75(44U),
    NUM_1_72(36U),
    NUM_1_45(52U),
    NUM_1_36(35U),
    AUTO_CINEMATIC(57U),
    NUM_1_8640(67U),
    NUM_1_7200(66U),
    NUM_1_4320(65U),
    NUM_1_3600(64U),
    NUM_1_2160(63U),
    NUM_1_1800(62U),
    NUM_1_1080(61U),
    NUM_1_900(60U),
    NUM_1_540(59U),
    NUM_1_450(58U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoShutter> {
        override fun fromUByteArray(value: UByteArray) = VideoShutter.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Shutter
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Shutter-146)
 *
 * @property value
 */
enum class PhotoShutter(override val value: UByte) : IValuedEnum<UByte> {
    AUTO(0U),
    NUM_1_125(1U),
    NUM_1_250(2U),
    NUM_1_500(3U),
    NUM_1_1000(4U),
    NUM_1_2000(5U),
    AUTO_CINEMATIC(6U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoShutter> {
        override fun fromUByteArray(value: UByteArray) = PhotoShutter.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Burst Rate
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Burst-Rate-147)
 *
 * @property value
 */
enum class BurstRate(override val value: UByte) : IValuedEnum<UByte> {
    NUM_30_PHOTOS_10_SECONDS(11U),
    NUM_30_PHOTOS_6_SECONDS(8U),
    NUM_30_PHOTOS_3_SECONDS(7U),
    NUM_25_PHOTOS_1_SECOND(14U),
    NUM_10_PHOTOS_3_SECONDS(4U),
    NUM_10_PHOTOS_1_SECOND(2U),
    NUM_5_PHOTOS_1_SECOND(1U),
    NUM_3_PHOTOS_1_SECOND(0U),
    AUTO(9U),
    NUM_30_PHOTOS_10_SECONDS_V2(100U),
    NUM_60_PHOTOS_10_SECONDS(13U),
    NUM_60_PHOTOS_6_SECONDS(12U),
    NUM_30_PHOTOS_1_SECOND(5U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<BurstRate> {
        override fun fromUByteArray(value: UByteArray) = BurstRate.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Max HyperSmooth
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Max-HyperSmooth-148)
 *
 * @property value
 */
enum class MaxHypersmooth(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U),
    STANDARD(100U),
    AUTO_BOOST(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MaxHypersmooth> {
        override fun fromUByteArray(value: UByteArray) = MaxHypersmooth.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Wind
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Wind-149)
 *
 * @property value
 */
enum class Wind(override val value: UByte) : IValuedEnum<UByte> {
    AUTO(2U),
    ON(4U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Wind> {
        override fun fromUByteArray(value: UByteArray) = Wind.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Horizon Leveling
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Horizon-Leveling-150)
 *
 * @property value
 */
enum class VideoHorizonLeveling(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    LOCKED(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoHorizonLeveling> {
        override fun fromUByteArray(value: UByteArray) = VideoHorizonLeveling.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Horizon Leveling
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Horizon-Leveling-151)
 *
 * @property value
 */
enum class PhotoHorizonLeveling(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    LOCKED(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoHorizonLeveling> {
        override fun fromUByteArray(value: UByteArray) = PhotoHorizonLeveling.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Mode Button
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Mode-Button-153)
 *
 * @property value
 */
enum class ModeButton(override val value: UByte) : IValuedEnum<UByte> {
    SPEED_RAMP(100U),
    HILIGHT(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<ModeButton> {
        override fun fromUByteArray(value: UByteArray) = ModeButton.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Front LCD Mode
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Front-LCD-Mode-154)
 *
 * @property value
 */
enum class FrontLcdMode(override val value: UByte) : IValuedEnum<UByte> {
    SCREEN_OFF(0U),
    STATUS_ONLY(1U),
    ACTUAL_VIEW(2U),
    FULL_SCREEN(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<FrontLcdMode> {
        override fun fromUByteArray(value: UByteArray) = FrontLcdMode.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Speed Ramp
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Speed-Ramp-155)
 *
 * @property value
 */
enum class SpeedRamp(override val value: UByte) : IValuedEnum<UByte> {
    REAL_SPEED(100U),
    HALF_SPEED(101U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SpeedRamp> {
        override fun fromUByteArray(value: UByteArray) = SpeedRamp.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Duration
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Duration-156)
 *
 * @property value
 */
enum class VideoDuration(override val value: UByte) : IValuedEnum<UByte> {
    NUM_3_HOURS(9U),
    NUM_2_HOURS(8U),
    NUM_1_HOUR(7U),
    NUM_30_MINUTES(6U),
    NUM_15_MINUTES(5U),
    NUM_5_MINUTES(4U),
    NUM_1_MINUTE(3U),
    NUM_30_SECONDS(2U),
    NUM_15_SECONDS(1U),
    NO_LIMIT(100U),
    NUM_5_SECONDS(10U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoDuration> {
        override fun fromUByteArray(value: UByteArray) = VideoDuration.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Multi Shot Duration
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Duration-157)
 *
 * @property value
 */
enum class MultiShotDuration(override val value: UByte) : IValuedEnum<UByte> {
    NUM_3_HOURS(9U),
    NUM_2_HOURS(8U),
    NUM_1_HOUR(7U),
    NUM_30_MINUTES(6U),
    NUM_15_MINUTES(5U),
    NUM_5_MINUTES(4U),
    NUM_1_MINUTE(3U),
    NUM_30_SECONDS(2U),
    NUM_15_SECONDS(1U),
    NO_LIMIT(100U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MultiShotDuration> {
        override fun fromUByteArray(value: UByteArray) = MultiShotDuration.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Screen Saver Front
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Screen-Saver-Front-158)
 *
 * @property value
 */
enum class ScreenSaverFront(override val value: UByte) : IValuedEnum<UByte> {
    NEVER(0U),
    MATCH_REAR_SCREEN(1U),
    NUM_1_MIN(2U),
    NUM_2_MIN(3U),
    NUM_3_MIN(4U),
    NUM_5_MIN(5U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<ScreenSaverFront> {
        override fun fromUByteArray(value: UByteArray) = ScreenSaverFront.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Screen Saver Rear
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Screen-Saver-Rear-159)
 *
 * @property value
 */
enum class ScreenSaverRear(override val value: UByte) : IValuedEnum<UByte> {
    NUM_1_MIN(1U),
    NUM_2_MIN(2U),
    NUM_3_MIN(3U),
    NUM_5_MIN(4U),
    NEVER(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<ScreenSaverRear> {
        override fun fromUByteArray(value: UByteArray) = ScreenSaverRear.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Multi Shot Bit Rate
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Bit-Rate-160)
 *
 * @property value
 */
enum class MultiShotBitRate(override val value: UByte) : IValuedEnum<UByte> {
    HIGH(1U),
    STANDARD(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MultiShotBitRate> {
        override fun fromUByteArray(value: UByteArray) = MultiShotBitRate.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Default Preset
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Default-Preset-161)
 *
 * @property value
 */
enum class DefaultPreset(override val value: UByte) : IValuedEnum<UByte> {
    LAST_USED(200U),
    LAST_USED_VIDEO(100U),
    LAST_USED_PHOTO(101U),
    LAST_USED_TIME_LAPSE(102U),
    NUM_360_VIDEO(103U),
    NUM_360_PHOTO(104U),
    NUM_360_LAPSE(105U),
    SINGLE_LENS_VIDEO(106U),
    SINGLE_LENS_PHOTO(107U),
    SINGLE_LENS_LAPSE(108U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<DefaultPreset> {
        override fun fromUByteArray(value: UByteArray) = DefaultPreset.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Max Lens
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Max-Lens-162)
 *
 * @property value
 */
enum class MaxLens(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MaxLens> {
        override fun fromUByteArray(value: UByteArray) = MaxLens.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Setup Lens Dashboard Button
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Lens-Dashboard-Button-163)
 *
 * @property value
 */
enum class SetupLensDashboardButton(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SetupLensDashboardButton> {
        override fun fromUByteArray(value: UByteArray) = SetupLensDashboardButton.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Media Mod
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Media-Mod-164)
 *
 * @property value
 */
enum class MediaMod(override val value: UByte) : IValuedEnum<UByte> {
    CAMERA_MICS(100U),
    BACK(2U),
    FRONT(1U),
    FRONT_BACK(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MediaMod> {
        override fun fromUByteArray(value: UByteArray) = MediaMod.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Horizon Lock
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Horizon-Lock-165)
 *
 * @property value
 */
enum class VideoHorizonLock(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoHorizonLock> {
        override fun fromUByteArray(value: UByteArray) = VideoHorizonLock.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Horizon Lock
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Horizon-Lock-166)
 *
 * @property value
 */
enum class PhotoHorizonLock(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoHorizonLock> {
        override fun fromUByteArray(value: UByteArray) = PhotoHorizonLock.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * HindSight
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#HindSight-167)
 *
 * @property value
 */
enum class Hindsight(override val value: UByte) : IValuedEnum<UByte> {
    NUM_15_SECONDS(2U),
    NUM_30_SECONDS(3U),
    OFF(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Hindsight> {
        override fun fromUByteArray(value: UByteArray) = Hindsight.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Scheduled Capture
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Scheduled-Capture-168)
 *
 * @property value
 */
enum class ScheduledCapture(override val value: ULong) : IValuedEnum<ULong> {
    NUM_00_00_12_HOUR_DISABLED(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<ScheduledCapture> {
        override fun fromUByteArray(value: UByteArray) = ScheduledCapture.entries.first {
            it.value == value.asInt64UB()
        }
    }
}

/**
 * Mods
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Mods-169)
 *
 * @property value
 */
enum class Mods(override val value: UByte) : IValuedEnum<UByte> {
    STANDARD_MIC(1U),
    STANDARD_MIC_(2U),
    POWERED_MIC(3U),
    POWERED_MIC_(4U),
    LINE_IN(5U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Mods> {
        override fun fromUByteArray(value: UByteArray) = Mods.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Single Interval
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Single-Interval-171)
 *
 * @property value
 */
enum class PhotoSingleInterval(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    NUM_0_5S(2U),
    NUM_1S(3U),
    NUM_2S(4U),
    NUM_3S(10U),
    NUM_5S(5U),
    NUM_10S(6U),
    NUM_30S(7U),
    NUM_60S(8U),
    NUM_120S(9U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoSingleInterval> {
        override fun fromUByteArray(value: UByteArray) = PhotoSingleInterval.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Interval Duration
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Interval-Duration-172)
 *
 * @property value
 */
enum class PhotoIntervalDuration(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    NUM_15_SECONDS(1U),
    NUM_30_SECONDS(2U),
    NUM_1_MINUTE(3U),
    NUM_5_MINUTES(4U),
    NUM_15_MINUTES(5U),
    NUM_30_MINUTES(6U),
    NUM_1_HOUR(7U),
    NUM_2_HOURS(8U),
    NUM_3_HOURS(9U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoIntervalDuration> {
        override fun fromUByteArray(value: UByteArray) = PhotoIntervalDuration.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Performance Mode
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Performance-Mode-173)
 *
 * @property value
 */
enum class VideoPerformanceMode(override val value: UByte) : IValuedEnum<UByte> {
    MAXIMUM_VIDEO_PERFORMANCE(0U),
    EXTENDED_BATTERY(1U),
    TRIPOD_STATIONARY_VIDEO(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoPerformanceMode> {
        override fun fromUByteArray(value: UByteArray) = VideoPerformanceMode.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * 10 Bit
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#10-Bit-174)
 *
 * @property value
 */
enum class NUM10Bit(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<NUM10Bit> {
        override fun fromUByteArray(value: UByteArray) = NUM10Bit.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Controls
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Controls-175)
 *
 * @property value
 */
enum class Controls(override val value: UByte) : IValuedEnum<UByte> {
    EASY(0U),
    PRO(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Controls> {
        override fun fromUByteArray(value: UByteArray) = Controls.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Easy Mode Speed
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Easy-Mode-Speed-176)
 *
 * @property value
 */
enum class EasyModeSpeed(override val value: UByte) : IValuedEnum<UByte> {
    NUM_1X_SPEED_LOW_LIGHT_V2_(103U),
    NUM_1X_SPEED_4K_LOW_LIGHT_V2_(126U),
    NUM_1X_SPEED_2_7K_LOW_LIGHT_V2_(128U),
    NUM_2X_SLO_MO_4K_V2_(116U),
    NUM_2X_SLO_MO_2_7K_V2_(130U),
    NUM_2X_SLO_MO_V2_(102U),
    NUM_4X_SUPER_SLO_MO_V2_(101U),
    NUM_8X_ULTRA_SLO_MO_V2_(100U),
    NUM_1X_SPEED_50HZ_LOW_LIGHT_V2_(107U),
    NUM_1X_SPEED_4K_50HZ_LOW_LIGHT_V2_(127U),
    NUM_1X_SPEED_2_7K_50HZ_LOW_LIGHT_V2_(129U),
    NUM_2X_SLO_MO_4K_50HZ_V2_(117U),
    NUM_2X_SLO_MO_2_7K_50HZ_V2_(131U),
    NUM_2X_SLO_MO_50HZ_V2_(106U),
    NUM_4X_SUPER_SLO_MO_50HZ_V2_(105U),
    NUM_8X_ULTRA_SLO_MO_50HZ_V2_(104U),
    NUM_1X_SPEED_LOW_LIGHT_V2_VERTICAL_(118U),
    NUM_1X_SPEED_50HZ_LOW_LIGHT_V2_VERTICAL_(119U),
    NUM_2X_SLO_MO_V2_VERTICAL_(120U),
    NUM_2X_SLO_MO_50HZ_V2_VERTICAL_(121U),
    NUM_1X_SPEED_FULL_FRAME_LOW_LIGHT_V2_(122U),
    NUM_1X_SPEED_50HZ_FULL_FRAME_LOW_LIGHT_V2_(123U),
    NUM_1X_SPEED_4K_FULL_FRAME_LOW_LIGHT_V2_(136U),
    NUM_1X_SPEED_4K_50HZ_FULL_FRAME_LOW_LIGHT_V2_(137U),
    NUM_2X_SLO_MO_FULL_FRAME_V2_(124U),
    NUM_2X_SLO_MO_50HZ_FULL_FRAME_V2_(125U),
    NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_V2_(111U),
    NUM_2X_SLO_MO_LONG_BATT_V2_(110U),
    NUM_4X_SUPER_SLO_MO_LONG_BATT_V2_(109U),
    NUM_8X_ULTRA_SLO_MO_LONG_BATT_V2_(108U),
    NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_V2_(115U),
    NUM_2X_SLO_MO_50HZ_LONG_BATT_V2_(114U),
    NUM_4X_SUPER_SLO_MO_50HZ_LONG_BATT_V2_(113U),
    NUM_8X_ULTRA_SLO_MO_50HZ_LONG_BATT_V2_(112U),
    NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_V2_VERTICAL_(134U),
    NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_V2_VERTICAL_(135U),
    NUM_2X_SLO_MO_LONG_BATT_V2_VERTICAL_(132U),
    NUM_2X_SLO_MO_50HZ_LONG_BATT_V2_VERTICAL_(133U),
    NUM_1X_NORMAL_SPEED_1_1_30_FPS_4K_V2_(138U),
    NUM_1X_NORMAL_SPEED_1_1_25_FPS_4K_V2_(139U),
    NUM_2X_SLO_MO_SPEED_1_1_4K_60_FPS_V2_(140U),
    NUM_2X_SLO_MO_SPEED_1_1_4K_50_FPS_V2_(141U),
    NUM_1X_NORMAL_SPEED_21_9_30_FPS_5_3K_V2_(142U),
    NUM_1X_NORMAL_SPEED_21_9_25_FPS_5_3K_V2_(143U),
    NUM_1X_NORMAL_SPEED_21_9_30_FPS_4K_V2_(146U),
    NUM_1X_NORMAL_SPEED_21_9_25_FPS_4K_V2_(147U),
    NUM_2X_SLO_MO_SPEED_21_9_5_3K_60_FPS_V2_(144U),
    NUM_2X_SLO_MO_SPEED_21_9_5_3K_50_FPS_V2_(145U),
    NUM_2X_SLO_MO_SPEED_21_9_4K_60_FPS_V2_(148U),
    NUM_2X_SLO_MO_SPEED_21_9_4K_50_FPS_V2_(149U),
    NUM_120_4X_SUPER_SLO_MO_SPEED_21_9_4K_V2_(150U),
    NUM_100_4X_SUPER_SLO_MO_SPEED_21_9_4K_V2_(151U),
    NUM_1X_NORMAL_SPEED_30_FPS_4_3_5_3K_V2_(152U),
    NUM_1X_NORMAL_SPEED_25_FPS_4_3_5_3K_V2_(153U),
    NUM_1X_NORMAL_SPEED_30_FPS_4_3_4K_V2_(154U),
    NUM_1X_NORMAL_SPEED_25_FPS_4_3_4K_V2_(155U),
    NUM_2X_SLO_MO_SPEED_4_3_4K_60_FPS_V2_(156U),
    NUM_2X_SLO_MO_SPEED_4_3_4K_50_FPS_V2_(157U),
    NUM_120_4X_SUPER_SLO_MO_SPEED_2_7K_4_3_V2_(158U),
    NUM_100_4X_SUPER_SLO_MO_SPEED_2_7K_4_3_V2_(159U),
    NUM_8X_ULTRA_SLO_MO(0U),
    NUM_4X_SUPER_SLO_MO(1U),
    NUM_4X_SUPER_SLO_MO_2_7K_(25U),
    NUM_2X_SLO_MO_4K_(24U),
    NUM_2X_SLO_MO(2U),
    NUM_1X_SPEED_LOW_LIGHT_(3U),
    NUM_8X_ULTRA_SLO_MO_EXT_BATT_(14U),
    NUM_4X_SUPER_SLO_MO_EXT_BATT_(4U),
    NUM_2X_SLO_MO_EXT_BATT_(5U),
    NUM_1X_SPEED_EXT_BATT_LOW_LIGHT_(6U),
    NUM_8X_ULTRA_SLO_MO_50HZ_(7U),
    NUM_4X_SUPER_SLO_MO_50HZ_(8U),
    NUM_4X_SUPER_SLO_MO_2_7K_50HZ_(27U),
    NUM_2X_SLO_MO_4K_50HZ_(26U),
    NUM_2X_SLO_MO_50HZ_(9U),
    NUM_1X_SPEED_50HZ_LOW_LIGHT_(10U),
    NUM_8X_ULTRA_SLO_MO_50HZ_EXT_BATT_(15U),
    NUM_4X_SUPER_SLO_MO_50HZ_EXT_BATT_(11U),
    NUM_2X_SLO_MO_50HZ_EXT_BATT_(12U),
    NUM_1X_SPEED_50HZ_EXT_BATT_LOW_LIGHT_(13U),
    NUM_8X_ULTRA_SLO_MO_LONG_BATT_(16U),
    NUM_4X_SUPER_SLO_MO_LONG_BATT_(17U),
    NUM_2X_SLO_MO_LONG_BATT_(18U),
    NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_(19U),
    NUM_8X_ULTRA_SLO_MO_50HZ_LONG_BATT_(20U),
    NUM_4X_SUPER_SLO_MO_50HZ_LONG_BATT_(21U),
    NUM_2X_SLO_MO_50HZ_LONG_BATT_(22U),
    NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_(23U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<EasyModeSpeed> {
        override fun fromUByteArray(value: UByteArray) = EasyModeSpeed.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Enable Night Photo
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Enable-Night-Photo-177)
 *
 * @property value
 */
enum class EnableNightPhoto(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<EnableNightPhoto> {
        override fun fromUByteArray(value: UByteArray) = EnableNightPhoto.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Wireless Band
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Wireless-Band-178)
 *
 * @property value
 */
enum class WirelessBand(override val value: UByte) : IValuedEnum<UByte> {
    NUM_2_4GHZ(0U),
    NUM_5GHZ(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<WirelessBand> {
        override fun fromUByteArray(value: UByteArray) = WirelessBand.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Star Trails Length
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Star-Trails-Length-179)
 *
 * @property value
 */
enum class StarTrailsLength(override val value: UByte) : IValuedEnum<UByte> {
    MAX(3U),
    LONG(2U),
    SHORT(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<StarTrailsLength> {
        override fun fromUByteArray(value: UByteArray) = StarTrailsLength.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * System Video Mode
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#System-Video-Mode-180)
 *
 * @property value
 */
enum class SystemVideoMode(override val value: UByte) : IValuedEnum<UByte> {
    BASIC_QUALITY(112U),
    STANDARD_QUALITY(111U),
    HIGHEST_QUALITY(0U),
    EXTENDED_BATTERY(101U),
    LONGEST_BATTERY(102U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SystemVideoMode> {
        override fun fromUByteArray(value: UByteArray) = SystemVideoMode.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Night Photo
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Night-Photo-181)
 *
 * @property value
 */
enum class NightPhoto(override val value: UByte) : IValuedEnum<UByte> {
    SUPER_PHOTO(0U),
    NIGHT_PHOTO(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<NightPhoto> {
        override fun fromUByteArray(value: UByteArray) = NightPhoto.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Bit Rate
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Bit-Rate-182)
 *
 * @property value
 */
enum class VideoBitRate(override val value: UByte) : IValuedEnum<UByte> {
    HIGH(1U),
    STANDARD(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoBitRate> {
        override fun fromUByteArray(value: UByteArray) = VideoBitRate.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Bit Depth
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Bit-Depth-183)
 *
 * @property value
 */
enum class BitDepth(override val value: UByte) : IValuedEnum<UByte> {
    NUM_8_BIT(0U),
    NUM_10_BIT(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<BitDepth> {
        override fun fromUByteArray(value: UByteArray) = BitDepth.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Profiles
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Profiles-184)
 *
 * @property value
 */
enum class Profiles(override val value: UByte) : IValuedEnum<UByte> {
    STANDARD(0U),
    HDR(1U),
    LOG(2U),
    HLG_HDR(101U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Profiles> {
        override fun fromUByteArray(value: UByteArray) = Profiles.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Easy Mode
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Easy-Mode-186)
 *
 * @property value
 */
enum class VideoEasyMode(override val value: UByte) : IValuedEnum<UByte> {
    HIGHEST_QUALITY(0U),
    STANDARD_QUALITY(1U),
    BASIC_QUALITY(2U),
    STANDARD_VIDEO(3U),
    HDR_VIDEO(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoEasyMode> {
        override fun fromUByteArray(value: UByteArray) = VideoEasyMode.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Lapse Mode
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Lapse-Mode-187)
 *
 * @property value
 */
enum class LapseMode(override val value: UByte) : IValuedEnum<UByte> {
    TIMEWARP(0U),
    STAR_TRAILS(1U),
    LIGHT_PAINTING(2U),
    VEHICLE_LIGHTS(3U),
    MAX_TIMEWARP(4U),
    MAX_STAR_TRAILS(5U),
    MAX_LIGHT_PAINTING(6U),
    MAX_VEHICLE_LIGHTS(7U),
    TIME_LAPSE_VIDEO(8U),
    NIGHT_LAPSE_VIDEO(9U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<LapseMode> {
        override fun fromUByteArray(value: UByteArray) = LapseMode.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Max Lens Mod
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Max-Lens-Mod-189)
 *
 * @property value
 */
enum class MaxLensMod(override val value: UByte) : IValuedEnum<UByte> {
    NONE(0U),
    MAX_LENS_1_0(1U),
    MAX_LENS_2_0(2U),
    ND_32(9U),
    ND_16(8U),
    ND_8(7U),
    ND_4(6U),
    STANDARD_LENS(10U),
    AUTO_DETECT(100U),
    MAX_LENS_2_5(3U),
    MACRO(4U),
    ANAMORPHIC(5U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MaxLensMod> {
        override fun fromUByteArray(value: UByteArray) = MaxLensMod.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Max Lens Mod Enable
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Max-Lens-Mod-Enable-190)
 *
 * @property value
 */
enum class MaxLensModEnable(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MaxLensModEnable> {
        override fun fromUByteArray(value: UByteArray) = MaxLensModEnable.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Easy Night Photo
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Easy-Night-Photo-191)
 *
 * @property value
 */
enum class EasyNightPhoto(override val value: UByte) : IValuedEnum<UByte> {
    SUPER_PHOTO(0U),
    NIGHT_PHOTO(1U),
    BURST(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<EasyNightPhoto> {
        override fun fromUByteArray(value: UByteArray) = EasyNightPhoto.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Multi Shot Aspect Ratio
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Aspect-Ratio-192)
 *
 * @property value
 */
enum class MultiShotAspectRatio(override val value: UByte) : IValuedEnum<UByte> {
    NUM_4_3(0U),
    NUM_16_9(1U),
    NUM_8_7(3U),
    NUM_9_16(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MultiShotAspectRatio> {
        override fun fromUByteArray(value: UByteArray) = MultiShotAspectRatio.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Framing
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Framing-193)
 *
 * @property value
 */
enum class Framing(override val value: UByte) : IValuedEnum<UByte> {
    WIDESCREEN(0U),
    VERTICAL(1U),
    FULL_FRAME(2U),
    WIDESCREEN_16_9_V2(101U),
    VERTICAL_9_16_V2(104U),
    FULL_FRAME_8_7_V2(103U),
    FULL_FRAME_1_1_V2(106U),
    ULTRA_WIDESCREEN_21_9_V2(105U),
    TRADITIONAL_4_3_V2(100U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Framing> {
        override fun fromUByteArray(value: UByteArray) = Framing.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Camera Mode
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Camera-Mode-194)
 *
 * @property value
 */
enum class CameraMode(override val value: UByte) : IValuedEnum<UByte> {
    SINGLE_LENS(0U),
    NUM_360_(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<CameraMode> {
        override fun fromUByteArray(value: UByteArray) = CameraMode.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Regional Format
 *
 * Note that these can also be set via Setting 134
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Regional-Format-195)
 *
 * @property value
 */
enum class RegionalFormat(override val value: UByte) : IValuedEnum<UByte> {
    NUM_60HZ(0U),
    NUM_50HZ(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<RegionalFormat> {
        override fun fromUByteArray(value: UByteArray) = RegionalFormat.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * 360 Photo Files Extension
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#360-Photo-Files-Extension-196)
 *
 * @property value
 */
enum class NUM360PhotoFilesExtension(override val value: UByte) : IValuedEnum<UByte> {
    NUM_JPG(0U),
    NUM_36P(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<NUM360PhotoFilesExtension> {
        override fun fromUByteArray(value: UByteArray) = NUM360PhotoFilesExtension.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Single Lens Exposure
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Single-Lens-Exposure-197)
 *
 * @property value
 */
enum class SingleLensExposure(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SingleLensExposure> {
        override fun fromUByteArray(value: UByteArray) = SingleLensExposure.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Denoise
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Denoise-198)
 *
 * @property value
 */
enum class Denoise(override val value: UByte) : IValuedEnum<UByte> {
    HIGH(2U),
    MEDIUM(1U),
    LOW(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Denoise> {
        override fun fromUByteArray(value: UByteArray) = Denoise.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * HLG HDR
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#HLG-HDR-199)
 *
 * @property value
 */
enum class HlgHdr(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<HlgHdr> {
        override fun fromUByteArray(value: UByteArray) = HlgHdr.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Focus Peaking
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Focus-Peaking-200)
 *
 * @property value
 */
enum class FocusPeaking(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    AUTO(1U),
    BLUE(2U),
    YELLOW(3U),
    RED(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<FocusPeaking> {
        override fun fromUByteArray(value: UByteArray) = FocusPeaking.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Quality Control
 *
 * Note that these can also be set via Setting 180
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Quality-Control-201)
 *
 * @property value
 */
enum class QualityControl(override val value: UByte) : IValuedEnum<UByte> {
    BASIC_QUALITY(2U),
    STANDARD_QUALITY(1U),
    HIGHEST_QUALITY(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<QualityControl> {
        override fun fromUByteArray(value: UByteArray) = QualityControl.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Focus Peaking High Sensitivity
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Focus-Peaking-High-Sensitivity-202)
 *
 * @property value
 */
enum class FocusPeakingHighSensitivity(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<FocusPeakingHighSensitivity> {
        override fun fromUByteArray(value: UByteArray) = FocusPeakingHighSensitivity.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Audio Tuning
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Audio-Tuning-203)
 *
 * @property value
 */
enum class AudioTuning(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<AudioTuning> {
        override fun fromUByteArray(value: UByteArray) = AudioTuning.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Battery Saver
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Battery-Saver-204)
 *
 * @property value
 */
enum class BatterySaver(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<BatterySaver> {
        override fun fromUByteArray(value: UByteArray) = BatterySaver.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Preset Dashboard Override
 *
 * Allows the user to set some target settings individually per-Preset instead of globally.
 *
 * An example use case is that the user wants to have Beep Volume enabled while in Photo Preset but not for
 * Video Preset.
 *
 * When **PDO** is **ON**, the camera uses the global PDO setting. When **PDO** is **OFF**, the camera uses the
 * per-Preset setting.
 *
 * The below table illustrates which settings are configurable in this manner with the correspond setting ID's that
 * should be used to achieve the desired functionality.
 *
 * | Setting                | PDO: ON (global) | PDO: OFF (per-Preset) |
 * | ---------------------- | ---------------- | --------------------- |
 * | Voice Control          | 206              | 223                   |
 * | Screen Saver           | 207              | 220                   |
 * | Beep Enable            | 208              | 221                   |
 * | Locked Orientation     | 209              | 112                   |
 * | Front LCD Display Mode | 210              | 154                   |
 * | Auto Screen Lock       | 211              | 226                   |
 * | LED Control            | 212              | 222                   |
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Preset-Dashboard-Override-205)
 *
 * @property value
 */
enum class PresetDashboardOverride(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PresetDashboardOverride> {
        override fun fromUByteArray(value: UByteArray) = PresetDashboardOverride.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Voice Commands
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Voice-Commands-206)
 *
 * @property value
 */
enum class VoiceCommands(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VoiceCommands> {
        override fun fromUByteArray(value: UByteArray) = VoiceCommands.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Screen Saver
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Screen-Saver-207)
 *
 * @property value
 */
enum class ScreenSaver(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<ScreenSaver> {
        override fun fromUByteArray(value: UByteArray) = ScreenSaver.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * General Beep Enable
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#General-Beep-Enable-208)
 *
 * @property value
 */
enum class GeneralBeepEnable(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<GeneralBeepEnable> {
        override fun fromUByteArray(value: UByteArray) = GeneralBeepEnable.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * General Locked Orientation
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#General-Locked-Orientation-209)
 *
 * @property value
 */
enum class GeneralLockedOrientation(override val value: UByte) : IValuedEnum<UByte> {
    LOCKED_270(3U),
    LOCKED_180(2U),
    LOCKED_90(4U),
    LOCKED_0(1U),
    LOCKED_ALL(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<GeneralLockedOrientation> {
        override fun fromUByteArray(value: UByteArray) = GeneralLockedOrientation.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Front Display
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Front-Display-210)
 *
 * @property value
 */
enum class FrontDisplay(override val value: UByte) : IValuedEnum<UByte> {
    SCREEN_OFF(0U),
    STATUS_ONLY(1U),
    ACTUAL_VIEW(2U),
    FULL_SCREEN(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<FrontDisplay> {
        override fun fromUByteArray(value: UByteArray) = FrontDisplay.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Screen Lock
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Screen-Lock-211)
 *
 * @property value
 */
enum class ScreenLock(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<ScreenLock> {
        override fun fromUByteArray(value: UByteArray) = ScreenLock.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * LEDs
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#LEDs-212)
 *
 * @property value
 */
enum class Leds(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<Leds> {
        override fun fromUByteArray(value: UByteArray) = Leds.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Anti-Flicker
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Anti-Flicker-213)
 *
 * @property value
 */
enum class VideoAnti_Flicker(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U),
    NUM_60HZ_NTSC_(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoAnti_Flicker> {
        override fun fromUByteArray(value: UByteArray) = VideoAnti_Flicker.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Wind Suppression
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Wind-Suppression-214)
 *
 * @property value
 */
enum class WindSuppression(override val value: UByte) : IValuedEnum<UByte> {
    AUTO(2U),
    ON(4U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<WindSuppression> {
        override fun fromUByteArray(value: UByteArray) = WindSuppression.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * External Mics
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#External-Mics-215)
 *
 * @property value
 */
enum class ExternalMics(override val value: UByte) : IValuedEnum<UByte> {
    STANDARD_MIC(1U),
    STANDARD_MIC_(2U),
    POWERED_MIC(3U),
    POWERED_MIC_(4U),
    LINE_IN(5U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<ExternalMics> {
        override fun fromUByteArray(value: UByteArray) = ExternalMics.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Camera Volume
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Camera-Volume-216)
 *
 * @property value
 */
enum class CameraVolume(override val value: UByte) : IValuedEnum<UByte> {
    HIGH(100U),
    MEDIUM(85U),
    LOW(70U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<CameraVolume> {
        override fun fromUByteArray(value: UByteArray) = CameraVolume.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Lens Attachment
 *
 * Note that these can also be set via Setting 189
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Lens-Attachment-217)
 *
 * @property value
 */
enum class LensAttachment(override val value: UByte) : IValuedEnum<UByte> {
    ND_32(9U),
    ND_16(8U),
    ND_8(7U),
    ND_4(6U),
    STANDARD_LENS(10U),
    AUTO_DETECT(100U),
    MAX_LENS_2_0(2U),
    MAX_LENS_2_5(3U),
    MACRO(4U),
    ANAMORPHIC(5U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<LensAttachment> {
        override fun fromUByteArray(value: UByteArray) = LensAttachment.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Motion Blur
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Motion-Blur-218)
 *
 * @property value
 */
enum class MotionBlur(override val value: UByte) : IValuedEnum<UByte> {
    AUTO(0U),
    HIGH(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MotionBlur> {
        override fun fromUByteArray(value: UByteArray) = MotionBlur.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Setup Screen Saver
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Screen-Saver-219)
 *
 * @property value
 */
enum class SetupScreenSaver(override val value: UByte) : IValuedEnum<UByte> {
    NEVER(0U),
    NUM_1_MIN(1U),
    NUM_2_MIN(2U),
    NUM_3_MIN(3U),
    NUM_5_MIN(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SetupScreenSaver> {
        override fun fromUByteArray(value: UByteArray) = SetupScreenSaver.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Dashboard Screen Saver
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Dashboard-Screen-Saver-220)
 *
 * @property value
 */
enum class DashboardScreenSaver(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<DashboardScreenSaver> {
        override fun fromUByteArray(value: UByteArray) = DashboardScreenSaver.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Dashboard Beeps
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Dashboard-Beeps-221)
 *
 * @property value
 */
enum class DashboardBeeps(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<DashboardBeeps> {
        override fun fromUByteArray(value: UByteArray) = DashboardBeeps.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Dashboard LEDs
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Dashboard-LEDs-222)
 *
 * @property value
 */
enum class DashboardLeds(override val value: UByte) : IValuedEnum<UByte> {
    ON(1U),
    OFF(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<DashboardLeds> {
        override fun fromUByteArray(value: UByteArray) = DashboardLeds.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Setup Language
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Language-223)
 *
 * @property value
 */
enum class SetupLanguage(override val value: UByte) : IValuedEnum<UByte> {
    CHINESE(8U),
    ENGLISH_AUS(2U),
    ENGLISH_IND(13U),
    ENGLISH_UK(1U),
    ENGLISH_US(0U),
    FRENCH(4U),
    GERMAN(3U),
    ITALIAN(5U),
    JAPANESE(9U),
    KOREAN(10U),
    PORTUGUESE(11U),
    RUSSIAN(12U),
    SPANISH(6U),
    SPANISH_NA(7U),
    SWEDISH(14U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SetupLanguage> {
        override fun fromUByteArray(value: UByteArray) = SetupLanguage.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Setup Brightness
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Brightness-224)
 *
 * @property value
 */
enum class SetupBrightness(override val value: UByte) : IValuedEnum<UByte> {
    NUM_10_(10U),
    NUM_20_(20U),
    NUM_30_(30U),
    NUM_40_(40U),
    NUM_50_(50U),
    NUM_60_(60U),
    NUM_70_(70U),
    NUM_80_(80U),
    NUM_90_(90U),
    NUM_100_(100U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SetupBrightness> {
        override fun fromUByteArray(value: UByteArray) = SetupBrightness.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Auto Power Off
 *
 * Note that these can also be set via Setting 59
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Auto-Power-Off-225)
 *
 * @property value
 */
enum class AutoPowerOff(override val value: UByte) : IValuedEnum<UByte> {
    NUM_1_MIN(1U),
    NUM_5_MIN(4U),
    NUM_15_MIN(6U),
    NUM_30_MIN(7U),
    NEVER(0U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<AutoPowerOff> {
        override fun fromUByteArray(value: UByteArray) = AutoPowerOff.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Setup Auto Lock
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Auto-Lock-226)
 *
 * @property value
 */
enum class SetupAutoLock(override val value: UByte) : IValuedEnum<UByte> {
    OFF(0U),
    ON(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<SetupAutoLock> {
        override fun fromUByteArray(value: UByteArray) = SetupAutoLock.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Mode
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Mode-227)
 *
 * @property value
 */
enum class PhotoMode(override val value: UByte) : IValuedEnum<UByte> {
    SUPERPHOTO(0U),
    NIGHT_PHOTO(1U),
    BURST(2U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoMode> {
        override fun fromUByteArray(value: UByteArray) = PhotoMode.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Global Dashboard Front Display
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Global-Dashboard-Front-Display-228)
 *
 * @property value
 */
enum class GlobalDashboardFrontDisplay(override val value: UByte) : IValuedEnum<UByte> {
    SCREEN_OFF(0U),
    STATUS_ONLY(1U),
    ACTUAL_VIEW(2U),
    FULL_SCREEN(3U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<GlobalDashboardFrontDisplay> {
        override fun fromUByteArray(value: UByteArray) = GlobalDashboardFrontDisplay.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Digital Lenses V2
 *
 * Note that these can also be set via Setting 121
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Digital-Lenses-V2-229)
 *
 * @property value
 */
enum class VideoDigitalLensesV2(override val value: UByte) : IValuedEnum<UByte> {
    LINEAR(4U),
    WIDE(0U),
    ULTRA_WIDE(13U),
    MAX_HYPERVIEW(11U),
    LINEAR_HORIZON_LOCK(10U),
    LINEAR_HORIZON_LEVELING(8U),
    ULTRA_LINEAR(14U),
    SUPERVIEW(3U),
    HYPERVIEW(9U),
    NARROW(2U),
    ULTRA_SUPERVIEW(12U),
    ULTRA_HYPERVIEW(100U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoDigitalLensesV2> {
        override fun fromUByteArray(value: UByteArray) = VideoDigitalLensesV2.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Photo Digital Lenses V2
 *
 * Note that these can also be set via Setting 122
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Digital-Lenses-V2-230)
 *
 * @property value
 */
enum class PhotoDigitalLensesV2(override val value: UByte) : IValuedEnum<UByte> {
    NUM_12MP_ULTRA_WIDE(41U),
    NUM_9MP_WIDE(15U),
    NUM_9MP_LINEAR(37U),
    NUM_27MP_LINEAR(32U),
    NUM_17MP_LINEAR(45U),
    NUM_23MP_LINEAR(28U),
    NUM_12MP_LINEAR(10U),
    NUM_12MP_WIDE(0U),
    NUM_17MP_ULTRA_LINEAR(48U),
    NUM_17MP_WIDE(46U),
    NUM_23MP_WIDE(27U),
    NUM_27MP_WIDE(31U),
    NUM_17MP_ULTRA_WIDE(47U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<PhotoDigitalLensesV2> {
        override fun fromUByteArray(value: UByteArray) = PhotoDigitalLensesV2.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Time Lapse Digital Lenses V2
 *
 * Note that these can also be set via Setting 123
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Time-Lapse-Digital-Lenses-V2-231)
 *
 * @property value
 */
enum class TimeLapseDigitalLensesV2(override val value: UByte) : IValuedEnum<UByte> {
    NUM_27MP_LINEAR(32U),
    NUM_27MP_WIDE(31U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<TimeLapseDigitalLensesV2> {
        override fun fromUByteArray(value: UByteArray) = TimeLapseDigitalLensesV2.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Video Framing
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Framing-232)
 *
 * @property value
 */
enum class VideoFraming(override val value: UByte) : IValuedEnum<UByte> {
    NUM_4_3(0U),
    NUM_16_9(1U),
    NUM_8_7(3U),
    NUM_9_16(4U),
    NUM_21_9(5U),
    NUM_1_1(6U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<VideoFraming> {
        override fun fromUByteArray(value: UByteArray) = VideoFraming.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Multi Shot Framing
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Framing-233)
 *
 * @property value
 */
enum class MultiShotFraming(override val value: UByte) : IValuedEnum<UByte> {
    NUM_4_3(0U),
    NUM_16_9(1U),
    NUM_8_7(3U),
    NUM_9_16(4U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<MultiShotFraming> {
        override fun fromUByteArray(value: UByteArray) = MultiShotFraming.entries.first {
            it.value == value.last()
        }
    }
}

/**
 * Frame Rate
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Frame-Rate-234)
 *
 * @property value
 */
enum class FrameRate(override val value: UByte) : IValuedEnum<UByte> {
    NUM_100_0(2U),
    NUM_90_0(3U),
    NUM_60_0(5U),
    NUM_50_0(6U),
    NUM_30_0(8U),
    NUM_25_0(9U),
    NUM_24_0(10U),
    NUM_400_0(15U),
    NUM_360_0(16U),
    NUM_300_0(17U),
    NUM_240_0(0U),
    NUM_200_0(13U),
    NUM_120_0(1U);

    @ExperimentalUnsignedTypes
    companion object : IUByteArrayCompanion<FrameRate> {
        override fun fromUByteArray(value: UByteArray) = FrameRate.entries.first {
            it.value == value.last()
        }
    }
}