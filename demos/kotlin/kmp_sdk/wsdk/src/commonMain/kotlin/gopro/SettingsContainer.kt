package gopro

/************************************************************************************************************
 *
 *
 * WARNING!!! This file is auto-generated. Do not modify it manually
 *
 *
 */

import domain.api.IOperationMarshaller
import domain.queries.Setting
import entity.queries.*

/**
 * Container for all per-setting-ID wrappers
 *
 * Note! This is a very small subset of the supported settings. TODO these need to be
 * automatically generated.
 *
 * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html)
 *
 * @param marshaller
 */
@OptIn(ExperimentalUnsignedTypes::class)
class SettingsContainer internal constructor(marshaller: IOperationMarshaller) {

    /**
     * Media Format
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#media-format-128)
     */
    val mediaFormat = Setting(SettingId.MEDIA_FORMAT, MediaFormat, marshaller)

    /**
     * Video Resolution
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-resolution-2)
     */
    val videoResolution = Setting(SettingId.VIDEO_RESOLUTION, VideoResolution, marshaller)

    /**
     * Frames Per Second
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frames-per-second-3)
     */
    val framesPerSecond = Setting(SettingId.FRAMES_PER_SECOND, FramesPerSecond, marshaller)

    /**
     * Video Timelapse Rate
     *
     * How frequently to take a video when performing a Video Timelapse
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-timelapse-rate-5)
     */
    val videoTimelapseRate = Setting(SettingId.VIDEO_TIMELAPSE_RATE, VideoTimelapseRate, marshaller)

    /**
     * Anti-Flicker
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#anti-flicker-134)
     */
    val anti_Flicker = Setting(SettingId.ANTI_FLICKER, Anti_Flicker, marshaller)

    /**
     * Hypersmooth
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hypersmooth-135)
     */
    val hypersmooth = Setting(SettingId.HYPERSMOOTH, Hypersmooth, marshaller)

    /**
     * Video Horizon Leveling
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-horizon-leveling-150)
     */
    val videoHorizonLeveling = Setting(SettingId.VIDEO_HORIZON_LEVELING, VideoHorizonLeveling, marshaller)

    /**
     * Photo Horizon Leveling
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-horizon-leveling-151)
     */
    val photoHorizonLeveling = Setting(SettingId.PHOTO_HORIZON_LEVELING, PhotoHorizonLeveling, marshaller)

    /**
     * Photo Timelapse Rate
     *
     * How frequently to take a photo when performing a Photo Timelapse.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-timelapse-rate-30)
     */
    val photoTimelapseRate = Setting(SettingId.PHOTO_TIMELAPSE_RATE, PhotoTimelapseRate, marshaller)

    /**
     * Nightlapse Rate
     *
     * How frequently to take a video or photo when performing a Nightlapse.
     *
     * This controls the Video or Photo Nightlapse rate if Setting 128 is set to 21 or 26 respectively.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#nightlapse-rate-32)
     */
    val nightlapseRate = Setting(SettingId.NIGHTLAPSE_RATE, NightlapseRate, marshaller)

    /**
     * Max Lens
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-162)
     */
    val maxLens = Setting(SettingId.MAX_LENS, MaxLens, marshaller)

    /**
     * HindSight
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hindsight-167)
     */
    val hindsight = Setting(SettingId.HINDSIGHT, Hindsight, marshaller)

    /**
     * Webcam Digital Lenses
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#webcam-digital-lenses-43)
     */
    val webcamDigitalLenses = Setting(SettingId.WEBCAM_DIGITAL_LENSES, WebcamDigitalLenses, marshaller)

    /**
     * Photo Single Interval
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-single-interval-171)
     */
    val photoSingleInterval = Setting(SettingId.PHOTO_SINGLE_INTERVAL, PhotoSingleInterval, marshaller)

    /**
     * Photo Interval Duration
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-interval-duration-172)
     */
    val photoIntervalDuration = Setting(SettingId.PHOTO_INTERVAL_DURATION, PhotoIntervalDuration, marshaller)

    /**
     * Video Performance Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-performance-mode-173)
     */
    val videoPerformanceMode = Setting(SettingId.VIDEO_PERFORMANCE_MODE, VideoPerformanceMode, marshaller)

    /**
     * Controls
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#controls-175)
     */
    val controls = Setting(SettingId.CONTROLS, Controls, marshaller)

    /**
     * Easy Mode Speed
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-mode-speed-176)
     */
    val easyModeSpeed = Setting(SettingId.EASY_MODE_SPEED, EasyModeSpeed, marshaller)

    /**
     * Enable Night Photo
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#enable-night-photo-177)
     */
    val enableNightPhoto = Setting(SettingId.ENABLE_NIGHT_PHOTO, EnableNightPhoto, marshaller)

    /**
     * Wireless Band
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#wireless-band-178)
     */
    val wirelessBand = Setting(SettingId.WIRELESS_BAND, WirelessBand, marshaller)

    /**
     * Star Trails Length
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#star-trails-length-179)
     */
    val starTrailsLength = Setting(SettingId.STAR_TRAILS_LENGTH, StarTrailsLength, marshaller)

    /**
     * System Video Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#system-video-mode-180)
     */
    val systemVideoMode = Setting(SettingId.SYSTEM_VIDEO_MODE, SystemVideoMode, marshaller)

    /**
     * Video Bit Rate
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-bit-rate-182)
     */
    val videoBitRate = Setting(SettingId.VIDEO_BIT_RATE, VideoBitRate, marshaller)

    /**
     * Bit Depth
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#bit-depth-183)
     */
    val bitDepth = Setting(SettingId.BIT_DEPTH, BitDepth, marshaller)

    /**
     * Profiles
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#profiles-184)
     */
    val profiles = Setting(SettingId.PROFILES, Profiles, marshaller)

    /**
     * Video Easy Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-easy-mode-186)
     */
    val videoEasyMode = Setting(SettingId.VIDEO_EASY_MODE, VideoEasyMode, marshaller)

    /**
     * Auto Power Down
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#auto-power-down-59)
     */
    val autoPowerDown = Setting(SettingId.AUTO_POWER_DOWN, AutoPowerDown, marshaller)

    /**
     * Lapse Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#lapse-mode-187)
     */
    val lapseMode = Setting(SettingId.LAPSE_MODE, LapseMode, marshaller)

    /**
     * Max Lens Mod
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-189)
     */
    val maxLensMod = Setting(SettingId.MAX_LENS_MOD, MaxLensMod, marshaller)

    /**
     * Max Lens Mod Enable
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-enable-190)
     */
    val maxLensModEnable = Setting(SettingId.MAX_LENS_MOD_ENABLE, MaxLensModEnable, marshaller)

    /**
     * Easy Night Photo
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-night-photo-191)
     */
    val easyNightPhoto = Setting(SettingId.EASY_NIGHT_PHOTO, EasyNightPhoto, marshaller)

    /**
     * Multi Shot Aspect Ratio
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-aspect-ratio-192)
     */
    val multiShotAspectRatio = Setting(SettingId.MULTI_SHOT_ASPECT_RATIO, MultiShotAspectRatio, marshaller)

    /**
     * Framing
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#framing-193)
     */
    val framing = Setting(SettingId.FRAMING, Framing, marshaller)

    /**
     * GPS
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#gps-83)
     */
    val gps = Setting(SettingId.GPS, Gps, marshaller)

    /**
     * Camera Volume
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#camera-volume-216)
     */
    val cameraVolume = Setting(SettingId.CAMERA_VOLUME, CameraVolume, marshaller)

    /**
     * LED
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#led-91)
     */
    val led = Setting(SettingId.LED, Led, marshaller)

    /**
     * Setup Screen Saver
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-screen-saver-219)
     */
    val setupScreenSaver = Setting(SettingId.SETUP_SCREEN_SAVER, SetupScreenSaver, marshaller)

    /**
     * Setup Language
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-language-223)
     */
    val setupLanguage = Setting(SettingId.SETUP_LANGUAGE, SetupLanguage, marshaller)

    /**
     * Photo Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-mode-227)
     */
    val photoMode = Setting(SettingId.PHOTO_MODE, PhotoMode, marshaller)

    /**
     * Video Framing
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-framing-232)
     */
    val videoFraming = Setting(SettingId.VIDEO_FRAMING, VideoFraming, marshaller)

    /**
     * Multi Shot Framing
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-framing-233)
     */
    val multiShotFraming = Setting(SettingId.MULTI_SHOT_FRAMING, MultiShotFraming, marshaller)

    /**
     * Frame Rate
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frame-rate-234)
     */
    val frameRate = Setting(SettingId.FRAME_RATE, FrameRate, marshaller)

    /**
     * Video Aspect Ratio
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-aspect-ratio-108)
     */
    val videoAspectRatio = Setting(SettingId.VIDEO_ASPECT_RATIO, VideoAspectRatio, marshaller)

    /**
     * Video Lens
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-lens-121)
     */
    val videoLens = Setting(SettingId.VIDEO_LENS, VideoLens, marshaller)

    /**
     * Photo Lens
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-lens-122)
     */
    val photoLens = Setting(SettingId.PHOTO_LENS, PhotoLens, marshaller)

    /**
     * Time Lapse Digital Lenses
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#time-lapse-digital-lenses-123)
     */
    val timeLapseDigitalLenses = Setting(SettingId.TIME_LAPSE_DIGITAL_LENSES, TimeLapseDigitalLenses, marshaller)

    /**
     * Photo Output
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-output-125)
     */
    val photoOutput = Setting(SettingId.PHOTO_OUTPUT, PhotoOutput, marshaller);
}