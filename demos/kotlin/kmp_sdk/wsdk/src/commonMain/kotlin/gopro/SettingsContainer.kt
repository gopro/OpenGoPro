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
     * Video Resolution
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Resolution-2)
     */
    val videoResolution = Setting(SettingId.VIDEO_RESOLUTION, VideoResolution, marshaller)

    /**
     * Frames Per Second
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Frames-Per-Second-3)
     */
    val framesPerSecond = Setting(SettingId.FRAMES_PER_SECOND, FramesPerSecond, marshaller)

    /**
     * Video Timelapse Rate
     *
     * How frequently to take a video when performing a Video Timelapse
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Timelapse-Rate-5)
     */
    val videoTimelapseRate = Setting(SettingId.VIDEO_TIMELAPSE_RATE, VideoTimelapseRate, marshaller)

    /**
     * Video Looping Interval
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Looping-Interval-6)
     */
    val videoLoopingInterval = Setting(SettingId.VIDEO_LOOPING_INTERVAL, VideoLoopingInterval, marshaller)

    /**
     * Video Protune ISO Max
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Protune-ISO-Max-13)
     */
    val videoProtuneIsoMax = Setting(SettingId.VIDEO_PROTUNE_ISO_MAX, VideoProtuneIsoMax, marshaller)

    /**
     * Photo Exposure Time
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Exposure-Time-19)
     */
    val photoExposureTime = Setting(SettingId.PHOTO_EXPOSURE_TIME, PhotoExposureTime, marshaller)

    /**
     * Photo Protune ISO Max
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Protune-ISO-Max-24)
     */
    val photoProtuneIsoMax = Setting(SettingId.PHOTO_PROTUNE_ISO_MAX, PhotoProtuneIsoMax, marshaller)

    /**
     * Photo Timelapse Rate
     *
     * How frequently to take a photo when performing a Photo Timelapse.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Timelapse-Rate-30)
     */
    val photoTimelapseRate = Setting(SettingId.PHOTO_TIMELAPSE_RATE, PhotoTimelapseRate, marshaller)

    /**
     * Multi Shot Exposure Time
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Exposure-Time-31)
     */
    val multiShotExposureTime = Setting(SettingId.MULTI_SHOT_EXPOSURE_TIME, MultiShotExposureTime, marshaller)

    /**
     * Nightlapse Rate
     *
     * How frequently to take a video or photo when performing a Nightlapse.
     *
     * This controls the Video or Photo Nightlapse rate if Setting 128 is set to 21 or 26 respectively.
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Nightlapse-Rate-32)
     */
    val nightlapseRate = Setting(SettingId.NIGHTLAPSE_RATE, NightlapseRate, marshaller)

    /**
     * Multi Shot Protune ISO Max
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Protune-ISO-Max-37)
     */
    val multiShotProtuneIsoMax = Setting(SettingId.MULTI_SHOT_PROTUNE_ISO_MAX, MultiShotProtuneIsoMax, marshaller)

    /**
     * Broadcast Resolution
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Broadcast-Resolution-41)
     */
    val broadcastResolution = Setting(SettingId.BROADCAST_RESOLUTION, BroadcastResolution, marshaller)

    /**
     * Frame Per Second
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Frame-Per-Second-42)
     */
    val framePerSecond = Setting(SettingId.FRAME_PER_SECOND, FramePerSecond, marshaller)

    /**
     * Webcam Digital Lenses
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Webcam-Digital-Lenses-43)
     */
    val webcamDigitalLenses = Setting(SettingId.WEBCAM_DIGITAL_LENSES, WebcamDigitalLenses, marshaller)

    /**
     * BNR Resolution
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#BNR-Resolution-44)
     */
    val bnrResolution = Setting(SettingId.BNR_RESOLUTION, BnrResolution, marshaller)

    /**
     * BNR Frame Per Second
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#BNR-Frame-Per-Second-45)
     */
    val bnrFramePerSecond = Setting(SettingId.BNR_FRAME_PER_SECOND, BnrFramePerSecond, marshaller)

    /**
     * Broadcast Window Size
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Broadcast-Window-Size-47)
     */
    val broadcastWindowSize = Setting(SettingId.BROADCAST_WINDOW_SIZE, BroadcastWindowSize, marshaller)

    /**
     * Privacy
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Privacy-48)
     */
    val privacy = Setting(SettingId.PRIVACY, Privacy, marshaller)

    /**
     * Quick Capture
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Quick-Capture-54)
     */
    val quickCapture = Setting(SettingId.QUICK_CAPTURE, QuickCapture, marshaller)

    /**
     * Auto Power Down
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Auto-Power-Down-59)
     */
    val autoPowerDown = Setting(SettingId.AUTO_POWER_DOWN, AutoPowerDown, marshaller)

    /**
     * Secondary Stream GOP Size
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Secondary-Stream-GOP-Size-60)
     */
    val secondaryStreamGopSize = Setting(SettingId.SECONDARY_STREAM_GOP_SIZE, SecondaryStreamGopSize, marshaller)

    /**
     * Secondary Stream IDR Interval
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Secondary-Stream-IDR-Interval-61)
     */
    val secondaryStreamIdrInterval = Setting(SettingId.SECONDARY_STREAM_IDR_INTERVAL, SecondaryStreamIdrInterval, marshaller)

    /**
     * Secondary Stream Bit Rate
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Secondary-Stream-Bit-Rate-62)
     */
    val secondaryStreamBitRate = Setting(SettingId.SECONDARY_STREAM_BIT_RATE, SecondaryStreamBitRate, marshaller)

    /**
     * Secondary Stream Window Size
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Secondary-Stream-Window-Size-64)
     */
    val secondaryStreamWindowSize = Setting(SettingId.SECONDARY_STREAM_WINDOW_SIZE, SecondaryStreamWindowSize, marshaller)

    /**
     * GOP Size
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#GOP-Size-65)
     */
    val gopSize = Setting(SettingId.GOP_SIZE, GopSize, marshaller)

    /**
     * IDR Interval
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#IDR-Interval-66)
     */
    val idrInterval = Setting(SettingId.IDR_INTERVAL, IdrInterval, marshaller)

    /**
     * Broadcast Bit Rate
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Broadcast-Bit-Rate-67)
     */
    val broadcastBitRate = Setting(SettingId.BROADCAST_BIT_RATE, BroadcastBitRate, marshaller)

    /**
     * Photo Protune ISO Min
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Protune-ISO-Min-75)
     */
    val photoProtuneIsoMin = Setting(SettingId.PHOTO_PROTUNE_ISO_MIN, PhotoProtuneIsoMin, marshaller)

    /**
     * Multi Shot Protune ISO Min
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Protune-ISO-Min-76)
     */
    val multiShotProtuneIsoMin = Setting(SettingId.MULTI_SHOT_PROTUNE_ISO_MIN, MultiShotProtuneIsoMin, marshaller)

    /**
     * Audio Protune
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Audio-Protune-79)
     */
    val audioProtune = Setting(SettingId.AUDIO_PROTUNE, AudioProtune, marshaller)

    /**
     * GPS
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#GPS-83)
     */
    val gps = Setting(SettingId.GPS, Gps, marshaller)

    /**
     * Language
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Language-84)
     */
    val language = Setting(SettingId.LANGUAGE, Language, marshaller)

    /**
     * Voice Control Language
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Voice-Control-Language-85)
     */
    val voiceControlLanguage = Setting(SettingId.VOICE_CONTROL_LANGUAGE, VoiceControlLanguage, marshaller)

    /**
     * Setup Beep Volume
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Beep-Volume-86)
     */
    val setupBeepVolume = Setting(SettingId.SETUP_BEEP_VOLUME, SetupBeepVolume, marshaller)

    /**
     * Beeps
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Beeps-87)
     */
    val beeps = Setting(SettingId.BEEPS, Beeps, marshaller)

    /**
     * LCD Brightness
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#LCD-Brightness-88)
     */
    val lcdBrightness = Setting(SettingId.LCD_BRIGHTNESS, LcdBrightness, marshaller)

    /**
     * LED
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#LED-91)
     */
    val led = Setting(SettingId.LED, Led, marshaller)

    /**
     * No Audio Track
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#No-Audio-Track-96)
     */
    val noAudioTrack = Setting(SettingId.NO_AUDIO_TRACK, NoAudioTrack, marshaller)

    /**
     * Video Protune ISO Min
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Protune-ISO-Min-102)
     */
    val videoProtuneIsoMin = Setting(SettingId.VIDEO_PROTUNE_ISO_MIN, VideoProtuneIsoMin, marshaller)

    /**
     * Auto Lock
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Auto-Lock-103)
     */
    val autoLock = Setting(SettingId.AUTO_LOCK, AutoLock, marshaller)

    /**
     * Wake On Voice
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Wake-On-Voice-104)
     */
    val wakeOnVoice = Setting(SettingId.WAKE_ON_VOICE, WakeOnVoice, marshaller)

    /**
     * Timer
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Timer-105)
     */
    val timer = Setting(SettingId.TIMER, Timer, marshaller)

    /**
     * Video Compression
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Compression-106)
     */
    val videoCompression = Setting(SettingId.VIDEO_COMPRESSION, VideoCompression, marshaller)

    /**
     * Video Aspect Ratio
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Aspect-Ratio-108)
     */
    val videoAspectRatio = Setting(SettingId.VIDEO_ASPECT_RATIO, VideoAspectRatio, marshaller)

    /**
     * Speed
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Speed-111)
     */
    val speed = Setting(SettingId.SPEED, Speed, marshaller)

    /**
     * Setup Landscape Lock
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Landscape-Lock-112)
     */
    val setupLandscapeLock = Setting(SettingId.SETUP_LANDSCAPE_LOCK, SetupLandscapeLock, marshaller)

    /**
     * Protune
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Protune-114)
     */
    val protune = Setting(SettingId.PROTUNE, Protune, marshaller)

    /**
     * White Balance
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#White-Balance-115)
     */
    val whiteBalance = Setting(SettingId.WHITE_BALANCE, WhiteBalance, marshaller)

    /**
     * Color
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Color-116)
     */
    val color = Setting(SettingId.COLOR, Color, marshaller)

    /**
     * Sharpness
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Sharpness-117)
     */
    val sharpness = Setting(SettingId.SHARPNESS, Sharpness, marshaller)

    /**
     * EV Comp
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#EV-Comp-118)
     */
    val evComp = Setting(SettingId.EV_COMP, EvComp, marshaller)

    /**
     * Video Lens
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Lens-121)
     */
    val videoLens = Setting(SettingId.VIDEO_LENS, VideoLens, marshaller)

    /**
     * Photo Lens
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Lens-122)
     */
    val photoLens = Setting(SettingId.PHOTO_LENS, PhotoLens, marshaller)

    /**
     * Time Lapse Digital Lenses
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Time-Lapse-Digital-Lenses-123)
     */
    val timeLapseDigitalLenses = Setting(SettingId.TIME_LAPSE_DIGITAL_LENSES, TimeLapseDigitalLenses, marshaller)

    /**
     * Video Bit Rate (Legacy)
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Bit-Rate-(Legacy)-124)
     */
    val videoBitRate_Legacy_ = Setting(SettingId.VIDEO_BIT_RATE_LEGACY_, VideoBitRate_Legacy_, marshaller)

    /**
     * Photo Output
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Output-125)
     */
    val photoOutput = Setting(SettingId.PHOTO_OUTPUT, PhotoOutput, marshaller)

    /**
     * Multi Shot Output
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Output-126)
     */
    val multiShotOutput = Setting(SettingId.MULTI_SHOT_OUTPUT, MultiShotOutput, marshaller)

    /**
     * Media Format
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Media-Format-128)
     */
    val mediaFormat = Setting(SettingId.MEDIA_FORMAT, MediaFormat, marshaller)

    /**
     * Lower Left
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Lower-Left-129)
     */
    val lowerLeft = Setting(SettingId.LOWER_LEFT, LowerLeft, marshaller)

    /**
     * Lower Right
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Lower-Right-130)
     */
    val lowerRight = Setting(SettingId.LOWER_RIGHT, LowerRight, marshaller)

    /**
     * Upper Left
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Upper-Left-131)
     */
    val upperLeft = Setting(SettingId.UPPER_LEFT, UpperLeft, marshaller)

    /**
     * Upper Right
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Upper-Right-132)
     */
    val upperRight = Setting(SettingId.UPPER_RIGHT, UpperRight, marshaller)

    /**
     * MegaPixels
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#MegaPixels-133)
     */
    val megapixels = Setting(SettingId.MEGAPIXELS, Megapixels, marshaller)

    /**
     * Anti-Flicker
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Anti-Flicker-134)
     */
    val anti_Flicker = Setting(SettingId.ANTI_FLICKER, Anti_Flicker, marshaller)

    /**
     * Hypersmooth
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Hypersmooth-135)
     */
    val hypersmooth = Setting(SettingId.HYPERSMOOTH, Hypersmooth, marshaller)

    /**
     * Mics
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Mics-137)
     */
    val mics = Setting(SettingId.MICS, Mics, marshaller)

    /**
     * 360 Audio
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#360-Audio-138)
     */
    val nUM360Audio = Setting(SettingId.NUM_360_AUDIO, NUM360Audio, marshaller)

    /**
     * RAW Audio
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#RAW-Audio-139)
     */
    val rawAudio = Setting(SettingId.RAW_AUDIO, RawAudio, marshaller)

    /**
     * QuikCapture Default
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#QuikCapture-Default-141)
     */
    val quikcaptureDefault = Setting(SettingId.QUIKCAPTURE_DEFAULT, QuikcaptureDefault, marshaller)

    /**
     * Spherical Lens
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Spherical-Lens-143)
     */
    val sphericalLens = Setting(SettingId.SPHERICAL_LENS, SphericalLens, marshaller)

    /**
     * Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Mode-144)
     */
    val mode = Setting(SettingId.MODE, Mode, marshaller)

    /**
     * Video Shutter
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Shutter-145)
     */
    val videoShutter = Setting(SettingId.VIDEO_SHUTTER, VideoShutter, marshaller)

    /**
     * Photo Shutter
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Shutter-146)
     */
    val photoShutter = Setting(SettingId.PHOTO_SHUTTER, PhotoShutter, marshaller)

    /**
     * Burst Rate
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Burst-Rate-147)
     */
    val burstRate = Setting(SettingId.BURST_RATE, BurstRate, marshaller)

    /**
     * Max HyperSmooth
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Max-HyperSmooth-148)
     */
    val maxHypersmooth = Setting(SettingId.MAX_HYPERSMOOTH, MaxHypersmooth, marshaller)

    /**
     * Wind
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Wind-149)
     */
    val wind = Setting(SettingId.WIND, Wind, marshaller)

    /**
     * Video Horizon Leveling
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Horizon-Leveling-150)
     */
    val videoHorizonLeveling = Setting(SettingId.VIDEO_HORIZON_LEVELING, VideoHorizonLeveling, marshaller)

    /**
     * Photo Horizon Leveling
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Horizon-Leveling-151)
     */
    val photoHorizonLeveling = Setting(SettingId.PHOTO_HORIZON_LEVELING, PhotoHorizonLeveling, marshaller)

    /**
     * Mode Button
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Mode-Button-153)
     */
    val modeButton = Setting(SettingId.MODE_BUTTON, ModeButton, marshaller)

    /**
     * Front LCD Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Front-LCD-Mode-154)
     */
    val frontLcdMode = Setting(SettingId.FRONT_LCD_MODE, FrontLcdMode, marshaller)

    /**
     * Speed Ramp
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Speed-Ramp-155)
     */
    val speedRamp = Setting(SettingId.SPEED_RAMP, SpeedRamp, marshaller)

    /**
     * Video Duration
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Duration-156)
     */
    val videoDuration = Setting(SettingId.VIDEO_DURATION, VideoDuration, marshaller)

    /**
     * Multi Shot Duration
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Duration-157)
     */
    val multiShotDuration = Setting(SettingId.MULTI_SHOT_DURATION, MultiShotDuration, marshaller)

    /**
     * Screen Saver Front
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Screen-Saver-Front-158)
     */
    val screenSaverFront = Setting(SettingId.SCREEN_SAVER_FRONT, ScreenSaverFront, marshaller)

    /**
     * Screen Saver Rear
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Screen-Saver-Rear-159)
     */
    val screenSaverRear = Setting(SettingId.SCREEN_SAVER_REAR, ScreenSaverRear, marshaller)

    /**
     * Multi Shot Bit Rate
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Bit-Rate-160)
     */
    val multiShotBitRate = Setting(SettingId.MULTI_SHOT_BIT_RATE, MultiShotBitRate, marshaller)

    /**
     * Default Preset
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Default-Preset-161)
     */
    val defaultPreset = Setting(SettingId.DEFAULT_PRESET, DefaultPreset, marshaller)

    /**
     * Max Lens
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Max-Lens-162)
     */
    val maxLens = Setting(SettingId.MAX_LENS, MaxLens, marshaller)

    /**
     * Setup Lens Dashboard Button
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Lens-Dashboard-Button-163)
     */
    val setupLensDashboardButton = Setting(SettingId.SETUP_LENS_DASHBOARD_BUTTON, SetupLensDashboardButton, marshaller)

    /**
     * Media Mod
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Media-Mod-164)
     */
    val mediaMod = Setting(SettingId.MEDIA_MOD, MediaMod, marshaller)

    /**
     * Video Horizon Lock
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Horizon-Lock-165)
     */
    val videoHorizonLock = Setting(SettingId.VIDEO_HORIZON_LOCK, VideoHorizonLock, marshaller)

    /**
     * Photo Horizon Lock
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Horizon-Lock-166)
     */
    val photoHorizonLock = Setting(SettingId.PHOTO_HORIZON_LOCK, PhotoHorizonLock, marshaller)

    /**
     * HindSight
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#HindSight-167)
     */
    val hindsight = Setting(SettingId.HINDSIGHT, Hindsight, marshaller)

    /**
     * Scheduled Capture
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Scheduled-Capture-168)
     */
    val scheduledCapture = Setting(SettingId.SCHEDULED_CAPTURE, ScheduledCapture, marshaller)

    /**
     * Mods
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Mods-169)
     */
    val mods = Setting(SettingId.MODS, Mods, marshaller)

    /**
     * Photo Single Interval
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Single-Interval-171)
     */
    val photoSingleInterval = Setting(SettingId.PHOTO_SINGLE_INTERVAL, PhotoSingleInterval, marshaller)

    /**
     * Photo Interval Duration
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Interval-Duration-172)
     */
    val photoIntervalDuration = Setting(SettingId.PHOTO_INTERVAL_DURATION, PhotoIntervalDuration, marshaller)

    /**
     * Video Performance Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Performance-Mode-173)
     */
    val videoPerformanceMode = Setting(SettingId.VIDEO_PERFORMANCE_MODE, VideoPerformanceMode, marshaller)

    /**
     * 10 Bit
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#10-Bit-174)
     */
    val nUM10Bit = Setting(SettingId.NUM_10_BIT, NUM10Bit, marshaller)

    /**
     * Controls
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Controls-175)
     */
    val controls = Setting(SettingId.CONTROLS, Controls, marshaller)

    /**
     * Easy Mode Speed
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Easy-Mode-Speed-176)
     */
    val easyModeSpeed = Setting(SettingId.EASY_MODE_SPEED, EasyModeSpeed, marshaller)

    /**
     * Enable Night Photo
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Enable-Night-Photo-177)
     */
    val enableNightPhoto = Setting(SettingId.ENABLE_NIGHT_PHOTO, EnableNightPhoto, marshaller)

    /**
     * Wireless Band
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Wireless-Band-178)
     */
    val wirelessBand = Setting(SettingId.WIRELESS_BAND, WirelessBand, marshaller)

    /**
     * Star Trails Length
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Star-Trails-Length-179)
     */
    val starTrailsLength = Setting(SettingId.STAR_TRAILS_LENGTH, StarTrailsLength, marshaller)

    /**
     * System Video Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#System-Video-Mode-180)
     */
    val systemVideoMode = Setting(SettingId.SYSTEM_VIDEO_MODE, SystemVideoMode, marshaller)

    /**
     * Night Photo
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Night-Photo-181)
     */
    val nightPhoto = Setting(SettingId.NIGHT_PHOTO, NightPhoto, marshaller)

    /**
     * Video Bit Rate
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Bit-Rate-182)
     */
    val videoBitRate = Setting(SettingId.VIDEO_BIT_RATE, VideoBitRate, marshaller)

    /**
     * Bit Depth
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Bit-Depth-183)
     */
    val bitDepth = Setting(SettingId.BIT_DEPTH, BitDepth, marshaller)

    /**
     * Profiles
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Profiles-184)
     */
    val profiles = Setting(SettingId.PROFILES, Profiles, marshaller)

    /**
     * Video Easy Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Easy-Mode-186)
     */
    val videoEasyMode = Setting(SettingId.VIDEO_EASY_MODE, VideoEasyMode, marshaller)

    /**
     * Lapse Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Lapse-Mode-187)
     */
    val lapseMode = Setting(SettingId.LAPSE_MODE, LapseMode, marshaller)

    /**
     * Max Lens Mod
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Max-Lens-Mod-189)
     */
    val maxLensMod = Setting(SettingId.MAX_LENS_MOD, MaxLensMod, marshaller)

    /**
     * Max Lens Mod Enable
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Max-Lens-Mod-Enable-190)
     */
    val maxLensModEnable = Setting(SettingId.MAX_LENS_MOD_ENABLE, MaxLensModEnable, marshaller)

    /**
     * Easy Night Photo
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Easy-Night-Photo-191)
     */
    val easyNightPhoto = Setting(SettingId.EASY_NIGHT_PHOTO, EasyNightPhoto, marshaller)

    /**
     * Multi Shot Aspect Ratio
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Aspect-Ratio-192)
     */
    val multiShotAspectRatio = Setting(SettingId.MULTI_SHOT_ASPECT_RATIO, MultiShotAspectRatio, marshaller)

    /**
     * Framing
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Framing-193)
     */
    val framing = Setting(SettingId.FRAMING, Framing, marshaller)

    /**
     * Camera Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Camera-Mode-194)
     */
    val cameraMode = Setting(SettingId.CAMERA_MODE, CameraMode, marshaller)

    /**
     * Regional Format
     *
     * Note that these can also be set via Setting 134
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Regional-Format-195)
     */
    val regionalFormat = Setting(SettingId.REGIONAL_FORMAT, RegionalFormat, marshaller)

    /**
     * 360 Photo Files Extension
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#360-Photo-Files-Extension-196)
     */
    val nUM360PhotoFilesExtension = Setting(SettingId.NUM_360_PHOTO_FILES_EXTENSION, NUM360PhotoFilesExtension, marshaller)

    /**
     * Single Lens Exposure
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Single-Lens-Exposure-197)
     */
    val singleLensExposure = Setting(SettingId.SINGLE_LENS_EXPOSURE, SingleLensExposure, marshaller)

    /**
     * Denoise
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Denoise-198)
     */
    val denoise = Setting(SettingId.DENOISE, Denoise, marshaller)

    /**
     * HLG HDR
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#HLG-HDR-199)
     */
    val hlgHdr = Setting(SettingId.HLG_HDR, HlgHdr, marshaller)

    /**
     * Focus Peaking
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Focus-Peaking-200)
     */
    val focusPeaking = Setting(SettingId.FOCUS_PEAKING, FocusPeaking, marshaller)

    /**
     * Quality Control
     *
     * Note that these can also be set via Setting 180
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Quality-Control-201)
     */
    val qualityControl = Setting(SettingId.QUALITY_CONTROL, QualityControl, marshaller)

    /**
     * Focus Peaking High Sensitivity
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Focus-Peaking-High-Sensitivity-202)
     */
    val focusPeakingHighSensitivity = Setting(SettingId.FOCUS_PEAKING_HIGH_SENSITIVITY, FocusPeakingHighSensitivity, marshaller)

    /**
     * Audio Tuning
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Audio-Tuning-203)
     */
    val audioTuning = Setting(SettingId.AUDIO_TUNING, AudioTuning, marshaller)

    /**
     * Battery Saver
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Battery-Saver-204)
     */
    val batterySaver = Setting(SettingId.BATTERY_SAVER, BatterySaver, marshaller)

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
     */
    val presetDashboardOverride = Setting(SettingId.PRESET_DASHBOARD_OVERRIDE, PresetDashboardOverride, marshaller)

    /**
     * Voice Commands
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Voice-Commands-206)
     */
    val voiceCommands = Setting(SettingId.VOICE_COMMANDS, VoiceCommands, marshaller)

    /**
     * Screen Saver
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Screen-Saver-207)
     */
    val screenSaver = Setting(SettingId.SCREEN_SAVER, ScreenSaver, marshaller)

    /**
     * General Beep Enable
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#General-Beep-Enable-208)
     */
    val generalBeepEnable = Setting(SettingId.GENERAL_BEEP_ENABLE, GeneralBeepEnable, marshaller)

    /**
     * General Locked Orientation
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#General-Locked-Orientation-209)
     */
    val generalLockedOrientation = Setting(SettingId.GENERAL_LOCKED_ORIENTATION, GeneralLockedOrientation, marshaller)

    /**
     * Front Display
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Front-Display-210)
     */
    val frontDisplay = Setting(SettingId.FRONT_DISPLAY, FrontDisplay, marshaller)

    /**
     * Screen Lock
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Screen-Lock-211)
     */
    val screenLock = Setting(SettingId.SCREEN_LOCK, ScreenLock, marshaller)

    /**
     * LEDs
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#LEDs-212)
     */
    val leds = Setting(SettingId.LEDS, Leds, marshaller)

    /**
     * Video Anti-Flicker
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Anti-Flicker-213)
     */
    val videoAnti_Flicker = Setting(SettingId.VIDEO_ANTI_FLICKER, VideoAnti_Flicker, marshaller)

    /**
     * Wind Suppression
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Wind-Suppression-214)
     */
    val windSuppression = Setting(SettingId.WIND_SUPPRESSION, WindSuppression, marshaller)

    /**
     * External Mics
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#External-Mics-215)
     */
    val externalMics = Setting(SettingId.EXTERNAL_MICS, ExternalMics, marshaller)

    /**
     * Camera Volume
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Camera-Volume-216)
     */
    val cameraVolume = Setting(SettingId.CAMERA_VOLUME, CameraVolume, marshaller)

    /**
     * Lens Attachment
     *
     * Note that these can also be set via Setting 189
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Lens-Attachment-217)
     */
    val lensAttachment = Setting(SettingId.LENS_ATTACHMENT, LensAttachment, marshaller)

    /**
     * Motion Blur
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Motion-Blur-218)
     */
    val motionBlur = Setting(SettingId.MOTION_BLUR, MotionBlur, marshaller)

    /**
     * Setup Screen Saver
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Screen-Saver-219)
     */
    val setupScreenSaver = Setting(SettingId.SETUP_SCREEN_SAVER, SetupScreenSaver, marshaller)

    /**
     * Dashboard Screen Saver
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Dashboard-Screen-Saver-220)
     */
    val dashboardScreenSaver = Setting(SettingId.DASHBOARD_SCREEN_SAVER, DashboardScreenSaver, marshaller)

    /**
     * Dashboard Beeps
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Dashboard-Beeps-221)
     */
    val dashboardBeeps = Setting(SettingId.DASHBOARD_BEEPS, DashboardBeeps, marshaller)

    /**
     * Dashboard LEDs
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Dashboard-LEDs-222)
     */
    val dashboardLeds = Setting(SettingId.DASHBOARD_LEDS, DashboardLeds, marshaller)

    /**
     * Setup Language
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Language-223)
     */
    val setupLanguage = Setting(SettingId.SETUP_LANGUAGE, SetupLanguage, marshaller)

    /**
     * Setup Brightness
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Brightness-224)
     */
    val setupBrightness = Setting(SettingId.SETUP_BRIGHTNESS, SetupBrightness, marshaller)

    /**
     * Auto Power Off
     *
     * Note that these can also be set via Setting 59
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Auto-Power-Off-225)
     */
    val autoPowerOff = Setting(SettingId.AUTO_POWER_OFF, AutoPowerOff, marshaller)

    /**
     * Setup Auto Lock
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Setup-Auto-Lock-226)
     */
    val setupAutoLock = Setting(SettingId.SETUP_AUTO_LOCK, SetupAutoLock, marshaller)

    /**
     * Photo Mode
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Mode-227)
     */
    val photoMode = Setting(SettingId.PHOTO_MODE, PhotoMode, marshaller)

    /**
     * Global Dashboard Front Display
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Global-Dashboard-Front-Display-228)
     */
    val globalDashboardFrontDisplay = Setting(SettingId.GLOBAL_DASHBOARD_FRONT_DISPLAY, GlobalDashboardFrontDisplay, marshaller)

    /**
     * Video Digital Lenses V2
     *
     * Note that these can also be set via Setting 121
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Digital-Lenses-V2-229)
     */
    val videoDigitalLensesV2 = Setting(SettingId.VIDEO_DIGITAL_LENSES_V2, VideoDigitalLensesV2, marshaller)

    /**
     * Photo Digital Lenses V2
     *
     * Note that these can also be set via Setting 122
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Photo-Digital-Lenses-V2-230)
     */
    val photoDigitalLensesV2 = Setting(SettingId.PHOTO_DIGITAL_LENSES_V2, PhotoDigitalLensesV2, marshaller)

    /**
     * Time Lapse Digital Lenses V2
     *
     * Note that these can also be set via Setting 123
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Time-Lapse-Digital-Lenses-V2-231)
     */
    val timeLapseDigitalLensesV2 = Setting(SettingId.TIME_LAPSE_DIGITAL_LENSES_V2, TimeLapseDigitalLensesV2, marshaller)

    /**
     * Video Framing
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Video-Framing-232)
     */
    val videoFraming = Setting(SettingId.VIDEO_FRAMING, VideoFraming, marshaller)

    /**
     * Multi Shot Framing
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Multi-Shot-Framing-233)
     */
    val multiShotFraming = Setting(SettingId.MULTI_SHOT_FRAMING, MultiShotFraming, marshaller)

    /**
     * Frame Rate
     *
     * @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#Frame-Rate-234)
     */
    val frameRate = Setting(SettingId.FRAME_RATE, FrameRate, marshaller);
}