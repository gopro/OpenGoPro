/* live_streaming.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal sealed class EnumLens(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumLens && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumLens.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object LENS_WIDE : EnumLens(0, "LENS_WIDE")

  internal object LENS_LINEAR : EnumLens(4, "LENS_LINEAR")

  internal object LENS_SUPERVIEW : EnumLens(3, "LENS_SUPERVIEW")

  internal class UNRECOGNIZED(value: Int) : EnumLens(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumLens> {
    internal val values: List<com.gopro.open_gopro.operations.EnumLens> by lazy {
      listOf(LENS_WIDE, LENS_LINEAR, LENS_SUPERVIEW)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumLens =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumLens =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumLens with name: $name")
  }
}

@pbandk.Export
internal sealed class EnumLiveStreamError(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumLiveStreamError && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumLiveStreamError.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object LIVE_STREAM_ERROR_NONE : EnumLiveStreamError(0, "LIVE_STREAM_ERROR_NONE")

  internal object LIVE_STREAM_ERROR_NETWORK : EnumLiveStreamError(1, "LIVE_STREAM_ERROR_NETWORK")

  internal object LIVE_STREAM_ERROR_CREATESTREAM :
      EnumLiveStreamError(2, "LIVE_STREAM_ERROR_CREATESTREAM")

  internal object LIVE_STREAM_ERROR_OUTOFMEMORY :
      EnumLiveStreamError(3, "LIVE_STREAM_ERROR_OUTOFMEMORY")

  internal object LIVE_STREAM_ERROR_INPUTSTREAM :
      EnumLiveStreamError(4, "LIVE_STREAM_ERROR_INPUTSTREAM")

  internal object LIVE_STREAM_ERROR_INTERNET : EnumLiveStreamError(5, "LIVE_STREAM_ERROR_INTERNET")

  internal object LIVE_STREAM_ERROR_OSNETWORK :
      EnumLiveStreamError(6, "LIVE_STREAM_ERROR_OSNETWORK")

  internal object LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT :
      EnumLiveStreamError(7, "LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT")

  internal object LIVE_STREAM_ERROR_SSL_HANDSHAKE :
      EnumLiveStreamError(8, "LIVE_STREAM_ERROR_SSL_HANDSHAKE")

  internal object LIVE_STREAM_ERROR_CAMERA_BLOCKED :
      EnumLiveStreamError(9, "LIVE_STREAM_ERROR_CAMERA_BLOCKED")

  internal object LIVE_STREAM_ERROR_UNKNOWN : EnumLiveStreamError(10, "LIVE_STREAM_ERROR_UNKNOWN")

  internal object LIVE_STREAM_ERROR_SD_CARD_FULL :
      EnumLiveStreamError(40, "LIVE_STREAM_ERROR_SD_CARD_FULL")

  internal object LIVE_STREAM_ERROR_SD_CARD_REMOVED :
      EnumLiveStreamError(41, "LIVE_STREAM_ERROR_SD_CARD_REMOVED")

  internal class UNRECOGNIZED(value: Int) : EnumLiveStreamError(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumLiveStreamError> {
    internal val values: List<com.gopro.open_gopro.operations.EnumLiveStreamError> by lazy {
      listOf(
          LIVE_STREAM_ERROR_NONE,
          LIVE_STREAM_ERROR_NETWORK,
          LIVE_STREAM_ERROR_CREATESTREAM,
          LIVE_STREAM_ERROR_OUTOFMEMORY,
          LIVE_STREAM_ERROR_INPUTSTREAM,
          LIVE_STREAM_ERROR_INTERNET,
          LIVE_STREAM_ERROR_OSNETWORK,
          LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT,
          LIVE_STREAM_ERROR_SSL_HANDSHAKE,
          LIVE_STREAM_ERROR_CAMERA_BLOCKED,
          LIVE_STREAM_ERROR_UNKNOWN,
          LIVE_STREAM_ERROR_SD_CARD_FULL,
          LIVE_STREAM_ERROR_SD_CARD_REMOVED)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumLiveStreamError =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumLiveStreamError =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumLiveStreamError with name: $name")
  }
}

@pbandk.Export
internal sealed class EnumLiveStreamStatus(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumLiveStreamStatus && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumLiveStreamStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object LIVE_STREAM_STATE_IDLE : EnumLiveStreamStatus(0, "LIVE_STREAM_STATE_IDLE")

  internal object LIVE_STREAM_STATE_CONFIG : EnumLiveStreamStatus(1, "LIVE_STREAM_STATE_CONFIG")

  internal object LIVE_STREAM_STATE_READY : EnumLiveStreamStatus(2, "LIVE_STREAM_STATE_READY")

  internal object LIVE_STREAM_STATE_STREAMING :
      EnumLiveStreamStatus(3, "LIVE_STREAM_STATE_STREAMING")

  internal object LIVE_STREAM_STATE_COMPLETE_STAY_ON :
      EnumLiveStreamStatus(4, "LIVE_STREAM_STATE_COMPLETE_STAY_ON")

  internal object LIVE_STREAM_STATE_FAILED_STAY_ON :
      EnumLiveStreamStatus(5, "LIVE_STREAM_STATE_FAILED_STAY_ON")

  internal object LIVE_STREAM_STATE_RECONNECTING :
      EnumLiveStreamStatus(6, "LIVE_STREAM_STATE_RECONNECTING")

  internal object LIVE_STREAM_STATE_UNAVAILABLE :
      EnumLiveStreamStatus(7, "LIVE_STREAM_STATE_UNAVAILABLE")

  internal class UNRECOGNIZED(value: Int) : EnumLiveStreamStatus(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumLiveStreamStatus> {
    internal val values: List<com.gopro.open_gopro.operations.EnumLiveStreamStatus> by lazy {
      listOf(
          LIVE_STREAM_STATE_IDLE,
          LIVE_STREAM_STATE_CONFIG,
          LIVE_STREAM_STATE_READY,
          LIVE_STREAM_STATE_STREAMING,
          LIVE_STREAM_STATE_COMPLETE_STAY_ON,
          LIVE_STREAM_STATE_FAILED_STAY_ON,
          LIVE_STREAM_STATE_RECONNECTING,
          LIVE_STREAM_STATE_UNAVAILABLE)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumLiveStreamStatus =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumLiveStreamStatus =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumLiveStreamStatus with name: $name")
  }
}

@pbandk.Export
internal sealed class EnumRegisterLiveStreamStatus(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String =
      "EnumRegisterLiveStreamStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object REGISTER_LIVE_STREAM_STATUS_STATUS :
      EnumRegisterLiveStreamStatus(1, "REGISTER_LIVE_STREAM_STATUS_STATUS")

  internal object REGISTER_LIVE_STREAM_STATUS_ERROR :
      EnumRegisterLiveStreamStatus(2, "REGISTER_LIVE_STREAM_STATUS_ERROR")

  internal object REGISTER_LIVE_STREAM_STATUS_MODE :
      EnumRegisterLiveStreamStatus(3, "REGISTER_LIVE_STREAM_STATUS_MODE")

  internal object REGISTER_LIVE_STREAM_STATUS_BITRATE :
      EnumRegisterLiveStreamStatus(4, "REGISTER_LIVE_STREAM_STATUS_BITRATE")

  internal class UNRECOGNIZED(value: Int) : EnumRegisterLiveStreamStatus(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus> {
    internal val values:
        List<com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus> by lazy {
      listOf(
          REGISTER_LIVE_STREAM_STATUS_STATUS,
          REGISTER_LIVE_STREAM_STATUS_ERROR,
          REGISTER_LIVE_STREAM_STATUS_MODE,
          REGISTER_LIVE_STREAM_STATUS_BITRATE)
    }

    override fun fromValue(
        value: Int
    ): com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(
        name: String
    ): com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumRegisterLiveStreamStatus with name: $name")
  }
}

@pbandk.Export
internal sealed class EnumWindowSize(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumWindowSize && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumWindowSize.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object WINDOW_SIZE_480 : EnumWindowSize(4, "WINDOW_SIZE_480")

  internal object WINDOW_SIZE_720 : EnumWindowSize(7, "WINDOW_SIZE_720")

  internal object WINDOW_SIZE_1080 : EnumWindowSize(12, "WINDOW_SIZE_1080")

  internal class UNRECOGNIZED(value: Int) : EnumWindowSize(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumWindowSize> {
    internal val values: List<com.gopro.open_gopro.operations.EnumWindowSize> by lazy {
      listOf(WINDOW_SIZE_480, WINDOW_SIZE_720, WINDOW_SIZE_1080)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumWindowSize =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumWindowSize =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumWindowSize with name: $name")
  }
}

@pbandk.Export
internal data class NotifyLiveStreamStatus(
    val liveStreamStatus: com.gopro.open_gopro.operations.EnumLiveStreamStatus? = null,
    val liveStreamError: com.gopro.open_gopro.operations.EnumLiveStreamError? = null,
    val liveStreamEncode: Boolean? = null,
    val liveStreamBitrate: Int? = null,
    val liveStreamWindowSizeSupportedArray: List<com.gopro.open_gopro.operations.EnumWindowSize> =
        emptyList(),
    val liveStreamEncodeSupported: Boolean? = null,
    val liveStreamMaxLensUnsupported: Boolean? = null,
    val liveStreamMinimumStreamBitrate: Int? = null,
    val liveStreamMaximumStreamBitrate: Int? = null,
    val liveStreamLensSupported: Boolean? = null,
    val liveStreamLensSupportedArray: List<com.gopro.open_gopro.operations.EnumLens> = emptyList(),
    val liveStreamProtuneSupported: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.NotifyLiveStreamStatus = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifyLiveStreamStatus>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.NotifyLiveStreamStatus> {
    internal val defaultInstance: com.gopro.open_gopro.operations.NotifyLiveStreamStatus by lazy {
      com.gopro.open_gopro.operations.NotifyLiveStreamStatus()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.NotifyLiveStreamStatus =
        com.gopro.open_gopro.operations.NotifyLiveStreamStatus.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifyLiveStreamStatus> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifyLiveStreamStatus",
            messageClass = com.gopro.open_gopro.operations.NotifyLiveStreamStatus::class,
            messageCompanion = this,
            fields =
                buildList(12) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_status",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumLiveStreamStatus
                                          .Companion,
                                  hasPresence = true),
                          jsonName = "liveStreamStatus",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamStatus))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_error",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumLiveStreamError.Companion,
                                  hasPresence = true),
                          jsonName = "liveStreamError",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamError))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_encode",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "liveStreamEncode",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamEncode))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_bitrate",
                          number = 4,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "liveStreamBitrate",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamBitrate))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_window_size_supported_array",
                          number = 5,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.EnumWindowSize>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Enum(
                                          enumCompanion =
                                              com.gopro.open_gopro.operations.EnumWindowSize
                                                  .Companion)),
                          jsonName = "liveStreamWindowSizeSupportedArray",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamWindowSizeSupportedArray))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_encode_supported",
                          number = 6,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "liveStreamEncodeSupported",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamEncodeSupported))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_max_lens_unsupported",
                          number = 7,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "liveStreamMaxLensUnsupported",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamMaxLensUnsupported))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_minimum_stream_bitrate",
                          number = 8,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "liveStreamMinimumStreamBitrate",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamMinimumStreamBitrate))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_maximum_stream_bitrate",
                          number = 9,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "liveStreamMaximumStreamBitrate",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamMaximumStreamBitrate))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_lens_supported",
                          number = 10,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "liveStreamLensSupported",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamLensSupported))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_lens_supported_array",
                          number = 11,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.EnumLens>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Enum(
                                          enumCompanion =
                                              com.gopro.open_gopro.operations.EnumLens.Companion)),
                          jsonName = "liveStreamLensSupportedArray",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamLensSupportedArray))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "live_stream_protune_supported",
                          number = 13,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "liveStreamProtuneSupported",
                          value =
                              com.gopro.open_gopro.operations.NotifyLiveStreamStatus::
                                  liveStreamProtuneSupported))
                })
  }
}

@pbandk.Export
internal data class RequestGetLiveStreamStatus(
    val registerLiveStreamStatus:
        List<com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus> =
        emptyList(),
    val unregisterLiveStreamStatus:
        List<com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus> =
        emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestGetLiveStreamStatus = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetLiveStreamStatus>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestGetLiveStreamStatus> {
    internal val defaultInstance:
        com.gopro.open_gopro.operations.RequestGetLiveStreamStatus by lazy {
      com.gopro.open_gopro.operations.RequestGetLiveStreamStatus()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestGetLiveStreamStatus =
        com.gopro.open_gopro.operations.RequestGetLiveStreamStatus.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetLiveStreamStatus> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetLiveStreamStatus",
            messageClass = com.gopro.open_gopro.operations.RequestGetLiveStreamStatus::class,
            messageCompanion = this,
            fields =
                buildList(2) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "register_live_stream_status",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Enum(
                                          enumCompanion =
                                              com.gopro.open_gopro.operations
                                                  .EnumRegisterLiveStreamStatus
                                                  .Companion)),
                          jsonName = "registerLiveStreamStatus",
                          value =
                              com.gopro.open_gopro.operations.RequestGetLiveStreamStatus::
                                  registerLiveStreamStatus))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "unregister_live_stream_status",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Enum(
                                          enumCompanion =
                                              com.gopro.open_gopro.operations
                                                  .EnumRegisterLiveStreamStatus
                                                  .Companion)),
                          jsonName = "unregisterLiveStreamStatus",
                          value =
                              com.gopro.open_gopro.operations.RequestGetLiveStreamStatus::
                                  unregisterLiveStreamStatus))
                })
  }
}

@pbandk.Export
internal data class RequestSetLiveStreamMode(
    val url: String? = null,
    val encode: Boolean? = null,
    val windowSize: com.gopro.open_gopro.operations.EnumWindowSize? = null,
    val cert: pbandk.ByteArr? = null,
    val minimumBitrate: Int? = null,
    val maximumBitrate: Int? = null,
    val startingBitrate: Int? = null,
    val lens: com.gopro.open_gopro.operations.EnumLens? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestSetLiveStreamMode = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetLiveStreamMode>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestSetLiveStreamMode> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestSetLiveStreamMode by lazy {
      com.gopro.open_gopro.operations.RequestSetLiveStreamMode()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestSetLiveStreamMode =
        com.gopro.open_gopro.operations.RequestSetLiveStreamMode.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetLiveStreamMode> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetLiveStreamMode",
            messageClass = com.gopro.open_gopro.operations.RequestSetLiveStreamMode::class,
            messageCompanion = this,
            fields =
                buildList(8) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "url",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "url",
                          value = com.gopro.open_gopro.operations.RequestSetLiveStreamMode::url))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "encode",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "encode",
                          value = com.gopro.open_gopro.operations.RequestSetLiveStreamMode::encode))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "window_size",
                          number = 3,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumWindowSize.Companion,
                                  hasPresence = true),
                          jsonName = "windowSize",
                          value =
                              com.gopro.open_gopro.operations.RequestSetLiveStreamMode::windowSize))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "cert",
                          number = 6,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                          jsonName = "cert",
                          value = com.gopro.open_gopro.operations.RequestSetLiveStreamMode::cert))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "minimum_bitrate",
                          number = 7,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "minimumBitrate",
                          value =
                              com.gopro.open_gopro.operations.RequestSetLiveStreamMode::
                                  minimumBitrate))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "maximum_bitrate",
                          number = 8,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "maximumBitrate",
                          value =
                              com.gopro.open_gopro.operations.RequestSetLiveStreamMode::
                                  maximumBitrate))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "starting_bitrate",
                          number = 9,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "startingBitrate",
                          value =
                              com.gopro.open_gopro.operations.RequestSetLiveStreamMode::
                                  startingBitrate))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "lens",
                          number = 10,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumLens.Companion,
                                  hasPresence = true),
                          jsonName = "lens",
                          value = com.gopro.open_gopro.operations.RequestSetLiveStreamMode::lens))
                })
  }
}

@pbandk.Export
@pbandk.JsName("orDefaultForNotifyLiveStreamStatus")
internal fun NotifyLiveStreamStatus?.orDefault():
    com.gopro.open_gopro.operations.NotifyLiveStreamStatus =
    this ?: NotifyLiveStreamStatus.defaultInstance

private fun NotifyLiveStreamStatus.protoMergeImpl(plus: pbandk.Message?): NotifyLiveStreamStatus =
    (plus as? NotifyLiveStreamStatus)?.let {
      it.copy(
          liveStreamStatus = plus.liveStreamStatus ?: liveStreamStatus,
          liveStreamError = plus.liveStreamError ?: liveStreamError,
          liveStreamEncode = plus.liveStreamEncode ?: liveStreamEncode,
          liveStreamBitrate = plus.liveStreamBitrate ?: liveStreamBitrate,
          liveStreamWindowSizeSupportedArray =
              liveStreamWindowSizeSupportedArray + plus.liveStreamWindowSizeSupportedArray,
          liveStreamEncodeSupported = plus.liveStreamEncodeSupported ?: liveStreamEncodeSupported,
          liveStreamMaxLensUnsupported =
              plus.liveStreamMaxLensUnsupported ?: liveStreamMaxLensUnsupported,
          liveStreamMinimumStreamBitrate =
              plus.liveStreamMinimumStreamBitrate ?: liveStreamMinimumStreamBitrate,
          liveStreamMaximumStreamBitrate =
              plus.liveStreamMaximumStreamBitrate ?: liveStreamMaximumStreamBitrate,
          liveStreamLensSupported = plus.liveStreamLensSupported ?: liveStreamLensSupported,
          liveStreamLensSupportedArray =
              liveStreamLensSupportedArray + plus.liveStreamLensSupportedArray,
          liveStreamProtuneSupported =
              plus.liveStreamProtuneSupported ?: liveStreamProtuneSupported,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifyLiveStreamStatus.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): NotifyLiveStreamStatus {
  var liveStreamStatus: com.gopro.open_gopro.operations.EnumLiveStreamStatus? = null
  var liveStreamError: com.gopro.open_gopro.operations.EnumLiveStreamError? = null
  var liveStreamEncode: Boolean? = null
  var liveStreamBitrate: Int? = null
  var liveStreamWindowSizeSupportedArray:
      pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.EnumWindowSize>? =
      null
  var liveStreamEncodeSupported: Boolean? = null
  var liveStreamMaxLensUnsupported: Boolean? = null
  var liveStreamMinimumStreamBitrate: Int? = null
  var liveStreamMaximumStreamBitrate: Int? = null
  var liveStreamLensSupported: Boolean? = null
  var liveStreamLensSupportedArray:
      pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.EnumLens>? =
      null
  var liveStreamProtuneSupported: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 ->
              liveStreamStatus = _fieldValue as com.gopro.open_gopro.operations.EnumLiveStreamStatus
          2 -> liveStreamError = _fieldValue as com.gopro.open_gopro.operations.EnumLiveStreamError
          3 -> liveStreamEncode = _fieldValue as Boolean
          4 -> liveStreamBitrate = _fieldValue as Int
          5 ->
              liveStreamWindowSizeSupportedArray =
                  (liveStreamWindowSizeSupportedArray ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<
                                com.gopro.open_gopro.operations.EnumWindowSize>
                  }
          6 -> liveStreamEncodeSupported = _fieldValue as Boolean
          7 -> liveStreamMaxLensUnsupported = _fieldValue as Boolean
          8 -> liveStreamMinimumStreamBitrate = _fieldValue as Int
          9 -> liveStreamMaximumStreamBitrate = _fieldValue as Int
          10 -> liveStreamLensSupported = _fieldValue as Boolean
          11 ->
              liveStreamLensSupportedArray =
                  (liveStreamLensSupportedArray ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as kotlin.sequences.Sequence<com.gopro.open_gopro.operations.EnumLens>
                  }
          13 -> liveStreamProtuneSupported = _fieldValue as Boolean
        }
      }

  return NotifyLiveStreamStatus(
      liveStreamStatus,
      liveStreamError,
      liveStreamEncode,
      liveStreamBitrate,
      pbandk.ListWithSize.Builder.fixed(liveStreamWindowSizeSupportedArray),
      liveStreamEncodeSupported,
      liveStreamMaxLensUnsupported,
      liveStreamMinimumStreamBitrate,
      liveStreamMaximumStreamBitrate,
      liveStreamLensSupported,
      pbandk.ListWithSize.Builder.fixed(liveStreamLensSupportedArray),
      liveStreamProtuneSupported,
      unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetLiveStreamStatus")
internal fun RequestGetLiveStreamStatus?.orDefault():
    com.gopro.open_gopro.operations.RequestGetLiveStreamStatus =
    this ?: RequestGetLiveStreamStatus.defaultInstance

private fun RequestGetLiveStreamStatus.protoMergeImpl(
    plus: pbandk.Message?
): RequestGetLiveStreamStatus =
    (plus as? RequestGetLiveStreamStatus)?.let {
      it.copy(
          registerLiveStreamStatus = registerLiveStreamStatus + plus.registerLiveStreamStatus,
          unregisterLiveStreamStatus = unregisterLiveStreamStatus + plus.unregisterLiveStreamStatus,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetLiveStreamStatus.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestGetLiveStreamStatus {
  var registerLiveStreamStatus:
      pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus>? =
      null
  var unregisterLiveStreamStatus:
      pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus>? =
      null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 ->
              registerLiveStreamStatus =
                  (registerLiveStreamStatus ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<
                                com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus>
                  }
          2 ->
              unregisterLiveStreamStatus =
                  (unregisterLiveStreamStatus ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<
                                com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus>
                  }
        }
      }

  return RequestGetLiveStreamStatus(
      pbandk.ListWithSize.Builder.fixed(registerLiveStreamStatus),
      pbandk.ListWithSize.Builder.fixed(unregisterLiveStreamStatus),
      unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestSetLiveStreamMode")
internal fun RequestSetLiveStreamMode?.orDefault():
    com.gopro.open_gopro.operations.RequestSetLiveStreamMode =
    this ?: RequestSetLiveStreamMode.defaultInstance

private fun RequestSetLiveStreamMode.protoMergeImpl(
    plus: pbandk.Message?
): RequestSetLiveStreamMode =
    (plus as? RequestSetLiveStreamMode)?.let {
      it.copy(
          url = plus.url ?: url,
          encode = plus.encode ?: encode,
          windowSize = plus.windowSize ?: windowSize,
          cert = plus.cert ?: cert,
          minimumBitrate = plus.minimumBitrate ?: minimumBitrate,
          maximumBitrate = plus.maximumBitrate ?: maximumBitrate,
          startingBitrate = plus.startingBitrate ?: startingBitrate,
          lens = plus.lens ?: lens,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetLiveStreamMode.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestSetLiveStreamMode {
  var url: String? = null
  var encode: Boolean? = null
  var windowSize: com.gopro.open_gopro.operations.EnumWindowSize? = null
  var cert: pbandk.ByteArr? = null
  var minimumBitrate: Int? = null
  var maximumBitrate: Int? = null
  var startingBitrate: Int? = null
  var lens: com.gopro.open_gopro.operations.EnumLens? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> url = _fieldValue as String
          2 -> encode = _fieldValue as Boolean
          3 -> windowSize = _fieldValue as com.gopro.open_gopro.operations.EnumWindowSize
          6 -> cert = _fieldValue as pbandk.ByteArr
          7 -> minimumBitrate = _fieldValue as Int
          8 -> maximumBitrate = _fieldValue as Int
          9 -> startingBitrate = _fieldValue as Int
          10 -> lens = _fieldValue as com.gopro.open_gopro.operations.EnumLens
        }
      }

  return RequestSetLiveStreamMode(
      url,
      encode,
      windowSize,
      cert,
      minimumBitrate,
      maximumBitrate,
      startingBitrate,
      lens,
      unknownFields)
}
