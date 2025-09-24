/* Settings.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Thu Feb 20 23:24:56 UTC 2025 */

package com.gopro.open_gopro.operations

/**
 * *********************************************************************************************************
 *
 * WARNING!!! This file is auto-generated. Do not modify it manually
 */
import com.gopro.open_gopro.util.extensions.asInt64UB
import com.gopro.open_gopro.util.extensions.toUByteArray

enum class SettingId(override val value: UByte) : IValuedEnum<UByte> {
  VIDEO_RESOLUTION(2U),
  FRAMES_PER_SECOND(3U),
  VIDEO_TIMELAPSE_RATE(5U),
  PHOTO_TIMELAPSE_RATE(30U),
  NIGHTLAPSE_RATE(32U),
  WEBCAM_DIGITAL_LENSES(43U),
  AUTO_POWER_DOWN(59U),
  GPS(83U),
  LCD_BRIGHTNESS(88U),
  LED(91U),
  VIDEO_ASPECT_RATIO(108U),
  VIDEO_LENS(121U),
  PHOTO_LENS(122U),
  TIME_LAPSE_DIGITAL_LENSES(123U),
  PHOTO_OUTPUT(125U),
  MEDIA_FORMAT(128U),
  ANTI_FLICKER(134U),
  HYPERSMOOTH(135U),
  VIDEO_HORIZON_LEVELING(150U),
  PHOTO_HORIZON_LEVELING(151U),
  VIDEO_DURATION(156U),
  MULTI_SHOT_DURATION(157U),
  MAX_LENS(162U),
  HINDSIGHT(167U),
  SCHEDULED_CAPTURE(168U),
  PHOTO_SINGLE_INTERVAL(171U),
  PHOTO_INTERVAL_DURATION(172U),
  VIDEO_PERFORMANCE_MODE(173U),
  CONTROL_MODE(175U),
  EASY_MODE_SPEED(176U),
  ENABLE_NIGHT_PHOTO(177U),
  WIRELESS_BAND(178U),
  STAR_TRAILS_LENGTH(179U),
  SYSTEM_VIDEO_MODE(180U),
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
  NUM_360_PHOTO_FILES_EXTENSION(196U),
  BEEP_VOLUME(216U),
  SETUP_SCREEN_SAVER(219U),
  SETUP_LANGUAGE(223U),
  PHOTO_MODE(227U),
  VIDEO_FRAMING(232U),
  MULTI_SHOT_FRAMING(233U),
  FRAME_RATE(234U),
  AUTOMATIC_WI_FI_ACCESS_POINT(236U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<SettingId> {
    override fun fromUByteArray(value: UByteArray) = entries.first { it.value == value.first() }

    override fun toUByteArray(value: SettingId) = value.value.toUByteArray()
  }
}

/**
 * Video Resolution
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-resolution-2)
 */
enum class VideoResolution(override val value: UByte) : IValuedEnum<UByte> {
  NUM_4K(1U),
  NUM_2_7K(4U),
  NUM_2_7K_4_3(6U),
  NUM_1440(7U),
  NUM_1080(9U),
  NUM_720(12U),
  NUM_4K_4_3(18U),
  NUM_5_6K(21U),
  NUM_5K(24U),
  NUM_5K_4_3(25U),
  NUM_5_3K_8_7(26U),
  NUM_5_3K_4_3(27U),
  NUM_4K_8_7(28U),
  NUM_8K(31U),
  NUM_5_3K_21_9(35U),
  NUM_4K_21_9(36U),
  NUM_4K_1_1(37U),
  NUM_900(38U),
  NUM_4K_SPH(39U),
  NUM_5_3K(100U),
  NUM_5_3K_8_7_V2(107U),
  NUM_4K_8_7_V2(108U),
  NUM_4K_9_16_V2(109U),
  NUM_1080_9_16_V2(110U),
  NUM_2_7K_4_3_V2(111U),
  NUM_4K_4_3_V2(112U),
  NUM_5_3K_4_3_V2(113U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoResolution> {
    override fun fromUByteArray(value: UByteArray) =
        VideoResolution.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoResolution) = value.value.toUByteArray()
  }
}

/**
 * Frames Per Second
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frames-per-second-3)
 */
enum class FramesPerSecond(override val value: UByte) : IValuedEnum<UByte> {
  NUM_240_0(0U),
  NUM_120_0(1U),
  NUM_100_0(2U),
  NUM_90_0(3U),
  NUM_60_0(5U),
  NUM_50_0(6U),
  NUM_30_0(8U),
  NUM_25_0(9U),
  NUM_24_0(10U),
  NUM_200_0(13U),
  NUM_400_0(15U),
  NUM_360_0(16U),
  NUM_300_0(17U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<FramesPerSecond> {
    override fun fromUByteArray(value: UByteArray) =
        FramesPerSecond.entries.first { it.value == value.last() }

    override fun toUByteArray(value: FramesPerSecond) = value.value.toUByteArray()
  }
}

/**
 * Video Timelapse Rate
 *
 * How frequently to take a video when performing a Video Timelapse
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-timelapse-rate-5)
 */
enum class VideoTimelapseRate(override val value: UByte) : IValuedEnum<UByte> {
  NUM_0_5_SECONDS(0U),
  NUM_1_SECOND(1U),
  NUM_2_SECONDS(2U),
  NUM_5_SECONDS(3U),
  NUM_10_SECONDS(4U),
  NUM_30_SECONDS(5U),
  NUM_60_SECONDS(6U),
  NUM_2_MINUTES(7U),
  NUM_5_MINUTES(8U),
  NUM_30_MINUTES(9U),
  NUM_60_MINUTES(10U),
  NUM_3_SECONDS(11U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoTimelapseRate> {
    override fun fromUByteArray(value: UByteArray) =
        VideoTimelapseRate.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoTimelapseRate) = value.value.toUByteArray()
  }
}

/**
 * Photo Timelapse Rate
 *
 * How frequently to take a photo when performing a Photo Timelapse.
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-timelapse-rate-30)
 */
enum class PhotoTimelapseRate(override val value: ULong) : IValuedEnum<ULong> {
  NUM_3_SECONDS(11U),
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
  NUM_0_5_SECONDS(110U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<PhotoTimelapseRate> {
    override fun fromUByteArray(value: UByteArray) =
        PhotoTimelapseRate.entries.first { it.value == value.asInt64UB() }

    override fun toUByteArray(value: PhotoTimelapseRate) = value.value.toUByteArray()
  }
}

/**
 * Nightlapse Rate
 *
 * How frequently to take a video or photo when performing a Nightlapse.
 *
 * This controls the Video or Photo Nightlapse rate if Setting 128 is set to 21 or 26 respectively.
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#nightlapse-rate-32)
 */
enum class NightlapseRate(override val value: ULong) : IValuedEnum<ULong> {
  NUM_4_SECONDS(4U),
  NUM_5_SECONDS(5U),
  NUM_10_SECONDS(10U),
  NUM_15_SECONDS(15U),
  NUM_20_SECONDS(20U),
  NUM_30_SECONDS(30U),
  NUM_60_SECONDS(100U),
  NUM_2_MINUTES(120U),
  NUM_5_MINUTES(300U),
  NUM_30_MINUTES(1800U),
  NUM_60_MINUTES(3600U),
  AUTO(3601U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<NightlapseRate> {
    override fun fromUByteArray(value: UByteArray) =
        NightlapseRate.entries.first { it.value == value.asInt64UB() }

    override fun toUByteArray(value: NightlapseRate) = value.value.toUByteArray()
  }
}

/**
 * Webcam Digital Lenses
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#webcam-digital-lenses-43)
 */
enum class WebcamDigitalLenses(override val value: UByte) : IValuedEnum<UByte> {
  WIDE(0U),
  NARROW(2U),
  SUPERVIEW(3U),
  LINEAR(4U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<WebcamDigitalLenses> {
    override fun fromUByteArray(value: UByteArray) =
        WebcamDigitalLenses.entries.first { it.value == value.last() }

    override fun toUByteArray(value: WebcamDigitalLenses) = value.value.toUByteArray()
  }
}

/**
 * Auto Power Down
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#auto-power-down-59)
 */
enum class AutoPowerDown(override val value: UByte) : IValuedEnum<UByte> {
  NEVER(0U),
  NUM_1_MIN(1U),
  NUM_5_MIN(4U),
  NUM_15_MIN(6U),
  NUM_30_MIN(7U),
  NUM_8_SECONDS(11U),
  NUM_30_SECONDS(12U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<AutoPowerDown> {
    override fun fromUByteArray(value: UByteArray) =
        AutoPowerDown.entries.first { it.value == value.last() }

    override fun toUByteArray(value: AutoPowerDown) = value.value.toUByteArray()
  }
}

/**
 * GPS
 *
 * @property value
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#gps-83)
 */
enum class Gps(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  ON(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<Gps> {
    override fun fromUByteArray(value: UByteArray) = Gps.entries.first { it.value == value.last() }

    override fun toUByteArray(value: Gps) = value.value.toUByteArray()
  }
}

/**
 * LED
 *
 * @property value
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#led-91)
 */
enum class Led(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  ON(2U),
  ALL_ON(3U),
  ALL_OFF(4U),
  FRONT_OFF_ONLY(5U),
  BACK_ONLY(100U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<Led> {
    override fun fromUByteArray(value: UByteArray) = Led.entries.first { it.value == value.last() }

    override fun toUByteArray(value: Led) = value.value.toUByteArray()
  }
}

/**
 * Video Aspect Ratio
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-aspect-ratio-108)
 */
enum class VideoAspectRatio(override val value: UByte) : IValuedEnum<UByte> {
  NUM_4_3(0U),
  NUM_16_9(1U),
  NUM_8_7(3U),
  NUM_9_16(4U),
  NUM_21_9(5U),
  NUM_1_1(6U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoAspectRatio> {
    override fun fromUByteArray(value: UByteArray) =
        VideoAspectRatio.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoAspectRatio) = value.value.toUByteArray()
  }
}

/**
 * Video Lens
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-lens-121)
 */
enum class VideoLens(override val value: UByte) : IValuedEnum<UByte> {
  WIDE(0U),
  NARROW(2U),
  SUPERVIEW(3U),
  LINEAR(4U),
  MAX_SUPERVIEW(7U),
  LINEAR_HORIZON_LEVELING(8U),
  HYPERVIEW(9U),
  LINEAR_HORIZON_LOCK(10U),
  MAX_HYPERVIEW(11U),
  ULTRA_SUPERVIEW(12U),
  ULTRA_WIDE(13U),
  ULTRA_LINEAR(14U),
  ULTRA_HYPERVIEW(104U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoLens> {
    override fun fromUByteArray(value: UByteArray) =
        VideoLens.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoLens) = value.value.toUByteArray()
  }
}

/**
 * Photo Lens
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-lens-122)
 */
enum class PhotoLens(override val value: UByte) : IValuedEnum<UByte> {
  WIDE_12_MP(0U),
  LINEAR_12_MP(10U),
  NUM_9MP_WIDE(15U),
  NARROW(19U),
  WIDE_23_MP(27U),
  LINEAR_23_MP(28U),
  WIDE_27_MP(31U),
  LINEAR_27_MP(32U),
  NUM_9MP_LINEAR(37U),
  NUM_13MP_LINEAR(38U),
  NUM_13MP_WIDE(39U),
  NUM_13MP_ULTRA_WIDE(40U),
  ULTRA_WIDE_12_MP(41U),
  NUM_13MP_ULTRA_LINEAR(44U),
  MAX_SUPERVIEW(100U),
  WIDE(101U),
  LINEAR(102U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<PhotoLens> {
    override fun fromUByteArray(value: UByteArray) =
        PhotoLens.entries.first { it.value == value.last() }

    override fun toUByteArray(value: PhotoLens) = value.value.toUByteArray()
  }
}

/**
 * Time Lapse Digital Lenses
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#time-lapse-digital-lenses-123)
 */
enum class TimeLapseDigitalLenses(override val value: UByte) : IValuedEnum<UByte> {
  NARROW(19U),
  WIDE_27_MP(31U),
  LINEAR_27_MP(32U),
  MAX_SUPERVIEW(100U),
  WIDE(101U),
  LINEAR(102U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<TimeLapseDigitalLenses> {
    override fun fromUByteArray(value: UByteArray) =
        TimeLapseDigitalLenses.entries.first { it.value == value.last() }

    override fun toUByteArray(value: TimeLapseDigitalLenses) = value.value.toUByteArray()
  }
}

/**
 * Photo Output
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-output-125)
 */
enum class PhotoOutput(override val value: UByte) : IValuedEnum<UByte> {
  STANDARD(0U),
  RAW(1U),
  HDR(2U),
  SUPERPHOTO(3U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<PhotoOutput> {
    override fun fromUByteArray(value: UByteArray) =
        PhotoOutput.entries.first { it.value == value.last() }

    override fun toUByteArray(value: PhotoOutput) = value.value.toUByteArray()
  }
}

/**
 * Media Format
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#media-format-128)
 */
enum class MediaFormat(override val value: UByte) : IValuedEnum<UByte> {
  TIME_LAPSE_VIDEO(13U),
  TIME_LAPSE_PHOTO(20U),
  NIGHT_LAPSE_PHOTO(21U),
  NIGHT_LAPSE_VIDEO(26U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<MediaFormat> {
    override fun fromUByteArray(value: UByteArray) =
        MediaFormat.entries.first { it.value == value.last() }

    override fun toUByteArray(value: MediaFormat) = value.value.toUByteArray()
  }
}

/**
 * Anti-Flicker
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#anti-flicker-134)
 */
enum class Anti_Flicker(override val value: UByte) : IValuedEnum<UByte> {
  NTSC(0U),
  PAL(1U),
  NUM_60HZ(2U),
  NUM_50HZ(3U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<Anti_Flicker> {
    override fun fromUByteArray(value: UByteArray) =
        Anti_Flicker.entries.first { it.value == value.last() }

    override fun toUByteArray(value: Anti_Flicker) = value.value.toUByteArray()
  }
}

/**
 * Hypersmooth
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hypersmooth-135)
 */
enum class Hypersmooth(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  LOW(1U),
  HIGH(2U),
  BOOST(3U),
  AUTO_BOOST(4U),
  STANDARD(100U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<Hypersmooth> {
    override fun fromUByteArray(value: UByteArray) =
        Hypersmooth.entries.first { it.value == value.last() }

    override fun toUByteArray(value: Hypersmooth) = value.value.toUByteArray()
  }
}

/**
 * Video Horizon Leveling
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-horizon-leveling-150)
 */
enum class VideoHorizonLeveling(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  LOCKED(2U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoHorizonLeveling> {
    override fun fromUByteArray(value: UByteArray) =
        VideoHorizonLeveling.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoHorizonLeveling) = value.value.toUByteArray()
  }
}

/**
 * Photo Horizon Leveling
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-horizon-leveling-151)
 */
enum class PhotoHorizonLeveling(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  LOCKED(2U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<PhotoHorizonLeveling> {
    override fun fromUByteArray(value: UByteArray) =
        PhotoHorizonLeveling.entries.first { it.value == value.last() }

    override fun toUByteArray(value: PhotoHorizonLeveling) = value.value.toUByteArray()
  }
}

/**
 * Video Duration
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-duration-156)
 */
enum class VideoDuration(override val value: UByte) : IValuedEnum<UByte> {
  NUM_15_SECONDS(1U),
  NUM_30_SECONDS(2U),
  NUM_1_MINUTE(3U),
  NUM_5_MINUTES(4U),
  NUM_15_MINUTES(5U),
  NUM_30_MINUTES(6U),
  NUM_1_HOUR(7U),
  NUM_2_HOURS(8U),
  NUM_3_HOURS(9U),
  NUM_5_SECONDS(10U),
  NO_LIMIT(100U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoDuration> {
    override fun fromUByteArray(value: UByteArray) =
        VideoDuration.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoDuration) = value.value.toUByteArray()
  }
}

/**
 * Multi Shot Duration
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-duration-157)
 */
enum class MultiShotDuration(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  NUM_15_SECONDS(1U),
  NUM_30_SECONDS(2U),
  NUM_1_MINUTE(3U),
  NUM_5_MINUTES(4U),
  NUM_15_MINUTES(5U),
  NUM_30_MINUTES(6U),
  NUM_1_HOUR(7U),
  NUM_2_HOURS(8U),
  NUM_3_HOURS(9U),
  NO_LIMIT(100U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<MultiShotDuration> {
    override fun fromUByteArray(value: UByteArray) =
        MultiShotDuration.entries.first { it.value == value.last() }

    override fun toUByteArray(value: MultiShotDuration) = value.value.toUByteArray()
  }
}

/**
 * Max Lens
 *
 * @property value
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-162)
 */
enum class MaxLens(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  ON(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<MaxLens> {
    override fun fromUByteArray(value: UByteArray) =
        MaxLens.entries.first { it.value == value.last() }

    override fun toUByteArray(value: MaxLens) = value.value.toUByteArray()
  }
}

/**
 * HindSight
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hindsight-167)
 */
enum class Hindsight(override val value: UByte) : IValuedEnum<UByte> {
  NUM_15_SECONDS(2U),
  NUM_30_SECONDS(3U),
  OFF(4U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<Hindsight> {
    override fun fromUByteArray(value: UByteArray) =
        Hindsight.entries.first { it.value == value.last() }

    override fun toUByteArray(value: Hindsight) = value.value.toUByteArray()
  }
}

/**
 * Photo Single Interval
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-single-interval-171)
 */
enum class PhotoSingleInterval(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  NUM_0_5S(2U),
  NUM_1S(3U),
  NUM_2S(4U),
  NUM_5S(5U),
  NUM_10S(6U),
  NUM_30S(7U),
  NUM_60S(8U),
  NUM_120S(9U),
  NUM_3S(10U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<PhotoSingleInterval> {
    override fun fromUByteArray(value: UByteArray) =
        PhotoSingleInterval.entries.first { it.value == value.last() }

    override fun toUByteArray(value: PhotoSingleInterval) = value.value.toUByteArray()
  }
}

/**
 * Photo Interval Duration
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-interval-duration-172)
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
    override fun fromUByteArray(value: UByteArray) =
        PhotoIntervalDuration.entries.first { it.value == value.last() }

    override fun toUByteArray(value: PhotoIntervalDuration) = value.value.toUByteArray()
  }
}

/**
 * Video Performance Mode
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-performance-mode-173)
 */
enum class VideoPerformanceMode(override val value: UByte) : IValuedEnum<UByte> {
  MAXIMUM_VIDEO_PERFORMANCE(0U),
  EXTENDED_BATTERY(1U),
  TRIPOD_STATIONARY_VIDEO(2U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoPerformanceMode> {
    override fun fromUByteArray(value: UByteArray) =
        VideoPerformanceMode.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoPerformanceMode) = value.value.toUByteArray()
  }
}

/**
 * Control Mode
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#control-mode-175)
 */
enum class ControlMode(override val value: UByte) : IValuedEnum<UByte> {
  EASY(0U),
  PRO(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<ControlMode> {
    override fun fromUByteArray(value: UByteArray) =
        ControlMode.entries.first { it.value == value.last() }

    override fun toUByteArray(value: ControlMode) = value.value.toUByteArray()
  }
}

/**
 * Easy Mode Speed
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-mode-speed-176)
 */
enum class EasyModeSpeed(override val value: UByte) : IValuedEnum<UByte> {
  NUM_8X_ULTRA_SLO_MO(0U),
  NUM_4X_SUPER_SLO_MO(1U),
  NUM_2X_SLO_MO(2U),
  NUM_1X_SPEED_LOW_LIGHT_(3U),
  NUM_4X_SUPER_SLO_MO_EXT_BATT_(4U),
  NUM_2X_SLO_MO_EXT_BATT_(5U),
  NUM_1X_SPEED_EXT_BATT_LOW_LIGHT_(6U),
  NUM_8X_ULTRA_SLO_MO_50HZ_(7U),
  NUM_4X_SUPER_SLO_MO_50HZ_(8U),
  NUM_2X_SLO_MO_50HZ_(9U),
  NUM_1X_SPEED_50HZ_LOW_LIGHT_(10U),
  NUM_4X_SUPER_SLO_MO_50HZ_EXT_BATT_(11U),
  NUM_2X_SLO_MO_50HZ_EXT_BATT_(12U),
  NUM_1X_SPEED_50HZ_EXT_BATT_LOW_LIGHT_(13U),
  NUM_8X_ULTRA_SLO_MO_EXT_BATT_(14U),
  NUM_8X_ULTRA_SLO_MO_50HZ_EXT_BATT_(15U),
  NUM_8X_ULTRA_SLO_MO_LONG_BATT_(16U),
  NUM_4X_SUPER_SLO_MO_LONG_BATT_(17U),
  NUM_2X_SLO_MO_LONG_BATT_(18U),
  NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_(19U),
  NUM_8X_ULTRA_SLO_MO_50HZ_LONG_BATT_(20U),
  NUM_4X_SUPER_SLO_MO_50HZ_LONG_BATT_(21U),
  NUM_2X_SLO_MO_50HZ_LONG_BATT_(22U),
  NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_(23U),
  NUM_2X_SLO_MO_4K_(24U),
  NUM_4X_SUPER_SLO_MO_2_7K_(25U),
  NUM_2X_SLO_MO_4K_50HZ_(26U),
  NUM_4X_SUPER_SLO_MO_2_7K_50HZ_(27U),
  NUM_8X_ULTRA_SLO_MO_V2_(100U),
  NUM_4X_SUPER_SLO_MO_V2_(101U),
  NUM_2X_SLO_MO_V2_(102U),
  NUM_1X_SPEED_LOW_LIGHT_V2_(103U),
  NUM_8X_ULTRA_SLO_MO_50HZ_V2_(104U),
  NUM_4X_SUPER_SLO_MO_50HZ_V2_(105U),
  NUM_2X_SLO_MO_50HZ_V2_(106U),
  NUM_1X_SPEED_50HZ_LOW_LIGHT_V2_(107U),
  NUM_8X_ULTRA_SLO_MO_LONG_BATT_V2_(108U),
  NUM_4X_SUPER_SLO_MO_LONG_BATT_V2_(109U),
  NUM_2X_SLO_MO_LONG_BATT_V2_(110U),
  NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_V2_(111U),
  NUM_8X_ULTRA_SLO_MO_50HZ_LONG_BATT_V2_(112U),
  NUM_4X_SUPER_SLO_MO_50HZ_LONG_BATT_V2_(113U),
  NUM_2X_SLO_MO_50HZ_LONG_BATT_V2_(114U),
  NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_V2_(115U),
  NUM_2X_SLO_MO_4K_V2_(116U),
  NUM_2X_SLO_MO_4K_50HZ_V2_(117U),
  NUM_1X_SPEED_LOW_LIGHT_V2_VERTICAL_(118U),
  NUM_1X_SPEED_50HZ_LOW_LIGHT_V2_VERTICAL_(119U),
  NUM_2X_SLO_MO_V2_VERTICAL_(120U),
  NUM_2X_SLO_MO_50HZ_V2_VERTICAL_(121U),
  NUM_1X_SPEED_FULL_FRAME_LOW_LIGHT_V2_(122U),
  NUM_1X_SPEED_50HZ_FULL_FRAME_LOW_LIGHT_V2_(123U),
  NUM_2X_SLO_MO_FULL_FRAME_V2_(124U),
  NUM_2X_SLO_MO_50HZ_FULL_FRAME_V2_(125U),
  NUM_1X_SPEED_4K_LOW_LIGHT_V2_(126U),
  NUM_1X_SPEED_4K_50HZ_LOW_LIGHT_V2_(127U),
  NUM_1X_SPEED_2_7K_LOW_LIGHT_V2_(128U),
  NUM_1X_SPEED_2_7K_50HZ_LOW_LIGHT_V2_(129U),
  NUM_2X_SLO_MO_2_7K_V2_(130U),
  NUM_2X_SLO_MO_2_7K_50HZ_V2_(131U),
  NUM_2X_SLO_MO_LONG_BATT_V2_VERTICAL_(132U),
  NUM_2X_SLO_MO_50HZ_LONG_BATT_V2_VERTICAL_(133U),
  NUM_1X_SPEED_LONG_BATT_LOW_LIGHT_V2_VERTICAL_(134U),
  NUM_1X_SPEED_50HZ_LONG_BATT_LOW_LIGHT_V2_VERTICAL_(135U),
  NUM_1X_SPEED_4K_FULL_FRAME_LOW_LIGHT_V2_(136U),
  NUM_1X_SPEED_4K_50HZ_FULL_FRAME_LOW_LIGHT_V2_(137U),
  NUM_1X_NORMAL_SPEED_1_1_30_FPS_4K_V2_(138U),
  NUM_1X_NORMAL_SPEED_1_1_25_FPS_4K_V2_(139U),
  NUM_2X_SLO_MO_SPEED_1_1_4K_60_FPS_V2_(140U),
  NUM_2X_SLO_MO_SPEED_1_1_4K_50_FPS_V2_(141U),
  NUM_1X_NORMAL_SPEED_21_9_30_FPS_5_3K_V2_(142U),
  NUM_1X_NORMAL_SPEED_21_9_25_FPS_5_3K_V2_(143U),
  NUM_2X_SLO_MO_SPEED_21_9_5_3K_60_FPS_V2_(144U),
  NUM_2X_SLO_MO_SPEED_21_9_5_3K_50_FPS_V2_(145U),
  NUM_1X_NORMAL_SPEED_21_9_30_FPS_4K_V2_(146U),
  NUM_1X_NORMAL_SPEED_21_9_25_FPS_4K_V2_(147U),
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
  NUM_100_4X_SUPER_SLO_MO_SPEED_2_7K_4_3_V2_(159U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<EasyModeSpeed> {
    override fun fromUByteArray(value: UByteArray) =
        EasyModeSpeed.entries.first { it.value == value.last() }

    override fun toUByteArray(value: EasyModeSpeed) = value.value.toUByteArray()
  }
}

/**
 * Enable Night Photo
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#enable-night-photo-177)
 */
enum class EnableNightPhoto(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  ON(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<EnableNightPhoto> {
    override fun fromUByteArray(value: UByteArray) =
        EnableNightPhoto.entries.first { it.value == value.last() }

    override fun toUByteArray(value: EnableNightPhoto) = value.value.toUByteArray()
  }
}

/**
 * Wireless Band
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#wireless-band-178)
 */
enum class WirelessBand(override val value: UByte) : IValuedEnum<UByte> {
  NUM_2_4GHZ(0U),
  NUM_5GHZ(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<WirelessBand> {
    override fun fromUByteArray(value: UByteArray) =
        WirelessBand.entries.first { it.value == value.last() }

    override fun toUByteArray(value: WirelessBand) = value.value.toUByteArray()
  }
}

/**
 * Star Trails Length
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#star-trails-length-179)
 */
enum class StarTrailsLength(override val value: UByte) : IValuedEnum<UByte> {
  SHORT(1U),
  LONG(2U),
  MAX(3U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<StarTrailsLength> {
    override fun fromUByteArray(value: UByteArray) =
        StarTrailsLength.entries.first { it.value == value.last() }

    override fun toUByteArray(value: StarTrailsLength) = value.value.toUByteArray()
  }
}

/**
 * System Video Mode
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#system-video-mode-180)
 */
enum class SystemVideoMode(override val value: UByte) : IValuedEnum<UByte> {
  HIGHEST_QUALITY(0U),
  EXTENDED_BATTERY(101U),
  LONGEST_BATTERY(102U),
  STANDARD_QUALITY(111U),
  BASIC_QUALITY(112U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<SystemVideoMode> {
    override fun fromUByteArray(value: UByteArray) =
        SystemVideoMode.entries.first { it.value == value.last() }

    override fun toUByteArray(value: SystemVideoMode) = value.value.toUByteArray()
  }
}

/**
 * Video Bit Rate
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-bit-rate-182)
 */
enum class VideoBitRate(override val value: UByte) : IValuedEnum<UByte> {
  STANDARD(0U),
  HIGH(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoBitRate> {
    override fun fromUByteArray(value: UByteArray) =
        VideoBitRate.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoBitRate) = value.value.toUByteArray()
  }
}

/**
 * Bit Depth
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#bit-depth-183)
 */
enum class BitDepth(override val value: UByte) : IValuedEnum<UByte> {
  NUM_8_BIT(0U),
  NUM_10_BIT(2U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<BitDepth> {
    override fun fromUByteArray(value: UByteArray) =
        BitDepth.entries.first { it.value == value.last() }

    override fun toUByteArray(value: BitDepth) = value.value.toUByteArray()
  }
}

/**
 * Profiles
 *
 * @property value
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#profiles-184)
 */
enum class Profiles(override val value: UByte) : IValuedEnum<UByte> {
  STANDARD(0U),
  HDR(1U),
  LOG(2U),
  HLG_HDR(101U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<Profiles> {
    override fun fromUByteArray(value: UByteArray) =
        Profiles.entries.first { it.value == value.last() }

    override fun toUByteArray(value: Profiles) = value.value.toUByteArray()
  }
}

/**
 * Video Easy Mode
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-easy-mode-186)
 */
enum class VideoEasyMode(override val value: UByte) : IValuedEnum<UByte> {
  HIGHEST_QUALITY(0U),
  STANDARD_QUALITY(1U),
  BASIC_QUALITY(2U),
  STANDARD_VIDEO(3U),
  HDR_VIDEO(4U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<VideoEasyMode> {
    override fun fromUByteArray(value: UByteArray) =
        VideoEasyMode.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoEasyMode) = value.value.toUByteArray()
  }
}

/**
 * Lapse Mode
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#lapse-mode-187)
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
    override fun fromUByteArray(value: UByteArray) =
        LapseMode.entries.first { it.value == value.last() }

    override fun toUByteArray(value: LapseMode) = value.value.toUByteArray()
  }
}

/**
 * Max Lens Mod
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-189)
 */
enum class MaxLensMod(override val value: UByte) : IValuedEnum<UByte> {
  NONE(0U),
  MAX_LENS_1_0(1U),
  MAX_LENS_2_0(2U),
  MAX_LENS_2_5(3U),
  MACRO(4U),
  ANAMORPHIC(5U),
  ND_4(6U),
  ND_8(7U),
  ND_16(8U),
  ND_32(9U),
  STANDARD_LENS(10U),
  AUTO_DETECT(100U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<MaxLensMod> {
    override fun fromUByteArray(value: UByteArray) =
        MaxLensMod.entries.first { it.value == value.last() }

    override fun toUByteArray(value: MaxLensMod) = value.value.toUByteArray()
  }
}

/**
 * Max Lens Mod Enable
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-enable-190)
 */
enum class MaxLensModEnable(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  ON(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<MaxLensModEnable> {
    override fun fromUByteArray(value: UByteArray) =
        MaxLensModEnable.entries.first { it.value == value.last() }

    override fun toUByteArray(value: MaxLensModEnable) = value.value.toUByteArray()
  }
}

/**
 * Easy Night Photo
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-night-photo-191)
 */
enum class EasyNightPhoto(override val value: UByte) : IValuedEnum<UByte> {
  SUPER_PHOTO(0U),
  NIGHT_PHOTO(1U),
  BURST(2U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<EasyNightPhoto> {
    override fun fromUByteArray(value: UByteArray) =
        EasyNightPhoto.entries.first { it.value == value.last() }

    override fun toUByteArray(value: EasyNightPhoto) = value.value.toUByteArray()
  }
}

/**
 * Multi Shot Aspect Ratio
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-aspect-ratio-192)
 */
enum class MultiShotAspectRatio(override val value: UByte) : IValuedEnum<UByte> {
  NUM_4_3(0U),
  NUM_16_9(1U),
  NUM_8_7(3U),
  NUM_9_16(4U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<MultiShotAspectRatio> {
    override fun fromUByteArray(value: UByteArray) =
        MultiShotAspectRatio.entries.first { it.value == value.last() }

    override fun toUByteArray(value: MultiShotAspectRatio) = value.value.toUByteArray()
  }
}

/**
 * Framing
 *
 * @property value
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#framing-193)
 */
enum class Framing(override val value: UByte) : IValuedEnum<UByte> {
  WIDESCREEN(0U),
  VERTICAL(1U),
  FULL_FRAME(2U),
  TRADITIONAL_4_3_V2(100U),
  WIDESCREEN_16_9_V2(101U),
  FULL_FRAME_8_7_V2(103U),
  VERTICAL_9_16_V2(104U),
  ULTRA_WIDESCREEN_21_9_V2(105U),
  FULL_FRAME_1_1_V2(106U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<Framing> {
    override fun fromUByteArray(value: UByteArray) =
        Framing.entries.first { it.value == value.last() }

    override fun toUByteArray(value: Framing) = value.value.toUByteArray()
  }
}

/**
 * Camera Mode
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#camera-mode-194)
 */
enum class CameraMode(override val value: UByte) : IValuedEnum<UByte> {
  SINGLE_LENS(0U),
  NUM_360_(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<CameraMode> {
    override fun fromUByteArray(value: UByteArray) =
        CameraMode.entries.first { it.value == value.last() }

    override fun toUByteArray(value: CameraMode) = value.value.toUByteArray()
  }
}

/**
 * 360 Photo Files Extension
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#360-photo-files-extension-196)
 */
enum class NUM360PhotoFilesExtension(override val value: UByte) : IValuedEnum<UByte> {
  NUM_JPG(0U),
  NUM_36P(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<NUM360PhotoFilesExtension> {
    override fun fromUByteArray(value: UByteArray) =
        NUM360PhotoFilesExtension.entries.first { it.value == value.last() }

    override fun toUByteArray(value: NUM360PhotoFilesExtension) = value.value.toUByteArray()
  }
}

/**
 * Beep Volume
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#beep-volume-216)
 */
enum class BeepVolume(override val value: UByte) : IValuedEnum<UByte> {
  LOW(70U),
  MEDIUM(85U),
  HIGH(100U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<BeepVolume> {
    override fun fromUByteArray(value: UByteArray) =
        BeepVolume.entries.first { it.value == value.last() }

    override fun toUByteArray(value: BeepVolume) = value.value.toUByteArray()
  }
}

/**
 * Setup Screen Saver
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-screen-saver-219)
 */
enum class SetupScreenSaver(override val value: UByte) : IValuedEnum<UByte> {
  NEVER(0U),
  NUM_1_MIN(1U),
  NUM_2_MIN(2U),
  NUM_3_MIN(3U),
  NUM_5_MIN(4U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<SetupScreenSaver> {
    override fun fromUByteArray(value: UByteArray) =
        SetupScreenSaver.entries.first { it.value == value.last() }

    override fun toUByteArray(value: SetupScreenSaver) = value.value.toUByteArray()
  }
}

/**
 * Setup Language
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-language-223)
 */
enum class SetupLanguage(override val value: UByte) : IValuedEnum<UByte> {
  ENGLISH_US(0U),
  ENGLISH_UK(1U),
  ENGLISH_AUS(2U),
  GERMAN(3U),
  FRENCH(4U),
  ITALIAN(5U),
  SPANISH(6U),
  SPANISH_NA(7U),
  CHINESE(8U),
  JAPANESE(9U),
  KOREAN(10U),
  PORTUGUESE(11U),
  RUSSIAN(12U),
  ENGLISH_IND(13U),
  SWEDISH(14U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<SetupLanguage> {
    override fun fromUByteArray(value: UByteArray) =
        SetupLanguage.entries.first { it.value == value.last() }

    override fun toUByteArray(value: SetupLanguage) = value.value.toUByteArray()
  }
}

/**
 * Photo Mode
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-mode-227)
 */
enum class PhotoMode(override val value: UByte) : IValuedEnum<UByte> {
  SUPERPHOTO(0U),
  NIGHT_PHOTO(1U),
  BURST(2U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<PhotoMode> {
    override fun fromUByteArray(value: UByteArray) =
        PhotoMode.entries.first { it.value == value.last() }

    override fun toUByteArray(value: PhotoMode) = value.value.toUByteArray()
  }
}

/**
 * Video Framing
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-framing-232)
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
    override fun fromUByteArray(value: UByteArray) =
        VideoFraming.entries.first { it.value == value.last() }

    override fun toUByteArray(value: VideoFraming) = value.value.toUByteArray()
  }
}

/**
 * Multi Shot Framing
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-framing-233)
 */
enum class MultiShotFraming(override val value: UByte) : IValuedEnum<UByte> {
  NUM_4_3(0U),
  NUM_16_9(1U),
  NUM_8_7(3U),
  NUM_9_16(4U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<MultiShotFraming> {
    override fun fromUByteArray(value: UByteArray) =
        MultiShotFraming.entries.first { it.value == value.last() }

    override fun toUByteArray(value: MultiShotFraming) = value.value.toUByteArray()
  }
}

/**
 * Frame Rate
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frame-rate-234)
 */
enum class FrameRate(override val value: UByte) : IValuedEnum<UByte> {
  NUM_240_0(0U),
  NUM_120_0(1U),
  NUM_100_0(2U),
  NUM_90_0(3U),
  NUM_60_0(5U),
  NUM_50_0(6U),
  NUM_30_0(8U),
  NUM_25_0(9U),
  NUM_24_0(10U),
  NUM_200_0(13U),
  NUM_400_0(15U),
  NUM_360_0(16U),
  NUM_300_0(17U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<FrameRate> {
    override fun fromUByteArray(value: UByteArray) =
        FrameRate.entries.first { it.value == value.last() }

    override fun toUByteArray(value: FrameRate) = value.value.toUByteArray()
  }
}

/**
 * Automatic Wi-Fi Access Point
 *
 * Configure the camera's wifi access point to automatically start on boot of the camera
 *
 * @property value
 * @see
 *   [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#automatic-wi-fi-access-point-236)
 */
enum class AutomaticWi_FiAccessPoint(override val value: UByte) : IValuedEnum<UByte> {
  OFF(0U),
  ON(1U);

  @ExperimentalUnsignedTypes
  companion object : IUByteArrayCompanion<AutomaticWi_FiAccessPoint> {
    override fun fromUByteArray(value: UByteArray) =
        AutomaticWi_FiAccessPoint.entries.first { it.value == value.last() }

    override fun toUByteArray(value: AutomaticWi_FiAccessPoint) = value.value.toUByteArray()
  }
}
