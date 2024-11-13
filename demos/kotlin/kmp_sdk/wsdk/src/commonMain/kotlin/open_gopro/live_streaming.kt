@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public sealed class EnumLens(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumLens && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumLens.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object LENS_WIDE : EnumLens(0, "LENS_WIDE")
    public object LENS_LINEAR : EnumLens(4, "LENS_LINEAR")
    public object LENS_SUPERVIEW : EnumLens(3, "LENS_SUPERVIEW")
    public class UNRECOGNIZED(value: Int) : EnumLens(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumLens> {
        public val values: List<open_gopro.EnumLens> by lazy { listOf(LENS_WIDE, LENS_LINEAR, LENS_SUPERVIEW) }
        override fun fromValue(value: Int): open_gopro.EnumLens = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumLens = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumLens with name: $name")
    }
}

@pbandk.Export
public sealed class EnumLiveStreamError(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumLiveStreamError && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumLiveStreamError.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object LIVE_STREAM_ERROR_NONE : EnumLiveStreamError(0, "LIVE_STREAM_ERROR_NONE")
    public object LIVE_STREAM_ERROR_NETWORK : EnumLiveStreamError(1, "LIVE_STREAM_ERROR_NETWORK")
    public object LIVE_STREAM_ERROR_CREATESTREAM : EnumLiveStreamError(2, "LIVE_STREAM_ERROR_CREATESTREAM")
    public object LIVE_STREAM_ERROR_OUTOFMEMORY : EnumLiveStreamError(3, "LIVE_STREAM_ERROR_OUTOFMEMORY")
    public object LIVE_STREAM_ERROR_INPUTSTREAM : EnumLiveStreamError(4, "LIVE_STREAM_ERROR_INPUTSTREAM")
    public object LIVE_STREAM_ERROR_INTERNET : EnumLiveStreamError(5, "LIVE_STREAM_ERROR_INTERNET")
    public object LIVE_STREAM_ERROR_OSNETWORK : EnumLiveStreamError(6, "LIVE_STREAM_ERROR_OSNETWORK")
    public object LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT : EnumLiveStreamError(7, "LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT")
    public object LIVE_STREAM_ERROR_SSL_HANDSHAKE : EnumLiveStreamError(8, "LIVE_STREAM_ERROR_SSL_HANDSHAKE")
    public object LIVE_STREAM_ERROR_CAMERA_BLOCKED : EnumLiveStreamError(9, "LIVE_STREAM_ERROR_CAMERA_BLOCKED")
    public object LIVE_STREAM_ERROR_UNKNOWN : EnumLiveStreamError(10, "LIVE_STREAM_ERROR_UNKNOWN")
    public object LIVE_STREAM_ERROR_SD_CARD_FULL : EnumLiveStreamError(40, "LIVE_STREAM_ERROR_SD_CARD_FULL")
    public object LIVE_STREAM_ERROR_SD_CARD_REMOVED : EnumLiveStreamError(41, "LIVE_STREAM_ERROR_SD_CARD_REMOVED")
    public class UNRECOGNIZED(value: Int) : EnumLiveStreamError(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumLiveStreamError> {
        public val values: List<open_gopro.EnumLiveStreamError> by lazy { listOf(LIVE_STREAM_ERROR_NONE, LIVE_STREAM_ERROR_NETWORK, LIVE_STREAM_ERROR_CREATESTREAM, LIVE_STREAM_ERROR_OUTOFMEMORY, LIVE_STREAM_ERROR_INPUTSTREAM, LIVE_STREAM_ERROR_INTERNET, LIVE_STREAM_ERROR_OSNETWORK, LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT, LIVE_STREAM_ERROR_SSL_HANDSHAKE, LIVE_STREAM_ERROR_CAMERA_BLOCKED, LIVE_STREAM_ERROR_UNKNOWN, LIVE_STREAM_ERROR_SD_CARD_FULL, LIVE_STREAM_ERROR_SD_CARD_REMOVED) }
        override fun fromValue(value: Int): open_gopro.EnumLiveStreamError = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumLiveStreamError = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumLiveStreamError with name: $name")
    }
}

@pbandk.Export
public sealed class EnumLiveStreamStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumLiveStreamStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumLiveStreamStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object LIVE_STREAM_STATE_IDLE : EnumLiveStreamStatus(0, "LIVE_STREAM_STATE_IDLE")
    public object LIVE_STREAM_STATE_CONFIG : EnumLiveStreamStatus(1, "LIVE_STREAM_STATE_CONFIG")
    public object LIVE_STREAM_STATE_READY : EnumLiveStreamStatus(2, "LIVE_STREAM_STATE_READY")
    public object LIVE_STREAM_STATE_STREAMING : EnumLiveStreamStatus(3, "LIVE_STREAM_STATE_STREAMING")
    public object LIVE_STREAM_STATE_COMPLETE_STAY_ON : EnumLiveStreamStatus(4, "LIVE_STREAM_STATE_COMPLETE_STAY_ON")
    public object LIVE_STREAM_STATE_FAILED_STAY_ON : EnumLiveStreamStatus(5, "LIVE_STREAM_STATE_FAILED_STAY_ON")
    public object LIVE_STREAM_STATE_RECONNECTING : EnumLiveStreamStatus(6, "LIVE_STREAM_STATE_RECONNECTING")
    public object LIVE_STREAM_STATE_UNAVAILABLE : EnumLiveStreamStatus(7, "LIVE_STREAM_STATE_UNAVAILABLE")
    public class UNRECOGNIZED(value: Int) : EnumLiveStreamStatus(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumLiveStreamStatus> {
        public val values: List<open_gopro.EnumLiveStreamStatus> by lazy { listOf(LIVE_STREAM_STATE_IDLE, LIVE_STREAM_STATE_CONFIG, LIVE_STREAM_STATE_READY, LIVE_STREAM_STATE_STREAMING, LIVE_STREAM_STATE_COMPLETE_STAY_ON, LIVE_STREAM_STATE_FAILED_STAY_ON, LIVE_STREAM_STATE_RECONNECTING, LIVE_STREAM_STATE_UNAVAILABLE) }
        override fun fromValue(value: Int): open_gopro.EnumLiveStreamStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumLiveStreamStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumLiveStreamStatus with name: $name")
    }
}

@pbandk.Export
public sealed class EnumRegisterLiveStreamStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumRegisterLiveStreamStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumRegisterLiveStreamStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object REGISTER_LIVE_STREAM_STATUS_STATUS : EnumRegisterLiveStreamStatus(1, "REGISTER_LIVE_STREAM_STATUS_STATUS")
    public object REGISTER_LIVE_STREAM_STATUS_ERROR : EnumRegisterLiveStreamStatus(2, "REGISTER_LIVE_STREAM_STATUS_ERROR")
    public object REGISTER_LIVE_STREAM_STATUS_MODE : EnumRegisterLiveStreamStatus(3, "REGISTER_LIVE_STREAM_STATUS_MODE")
    public object REGISTER_LIVE_STREAM_STATUS_BITRATE : EnumRegisterLiveStreamStatus(4, "REGISTER_LIVE_STREAM_STATUS_BITRATE")
    public class UNRECOGNIZED(value: Int) : EnumRegisterLiveStreamStatus(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumRegisterLiveStreamStatus> {
        public val values: List<open_gopro.EnumRegisterLiveStreamStatus> by lazy { listOf(REGISTER_LIVE_STREAM_STATUS_STATUS, REGISTER_LIVE_STREAM_STATUS_ERROR, REGISTER_LIVE_STREAM_STATUS_MODE, REGISTER_LIVE_STREAM_STATUS_BITRATE) }
        override fun fromValue(value: Int): open_gopro.EnumRegisterLiveStreamStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumRegisterLiveStreamStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumRegisterLiveStreamStatus with name: $name")
    }
}

@pbandk.Export
public sealed class EnumWindowSize(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumWindowSize && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumWindowSize.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object WINDOW_SIZE_480 : EnumWindowSize(4, "WINDOW_SIZE_480")
    public object WINDOW_SIZE_720 : EnumWindowSize(7, "WINDOW_SIZE_720")
    public object WINDOW_SIZE_1080 : EnumWindowSize(12, "WINDOW_SIZE_1080")
    public class UNRECOGNIZED(value: Int) : EnumWindowSize(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumWindowSize> {
        public val values: List<open_gopro.EnumWindowSize> by lazy { listOf(WINDOW_SIZE_480, WINDOW_SIZE_720, WINDOW_SIZE_1080) }
        override fun fromValue(value: Int): open_gopro.EnumWindowSize = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumWindowSize = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumWindowSize with name: $name")
    }
}

@pbandk.Export
public data class NotifyLiveStreamStatus(
    val liveStreamStatus: open_gopro.EnumLiveStreamStatus? = null,
    val liveStreamError: open_gopro.EnumLiveStreamError? = null,
    val liveStreamEncode: Boolean? = null,
    val liveStreamBitrate: Int? = null,
    val liveStreamWindowSizeSupportedArray: List<open_gopro.EnumWindowSize> = emptyList(),
    val liveStreamEncodeSupported: Boolean? = null,
    val liveStreamMaxLensUnsupported: Boolean? = null,
    val liveStreamMinimumStreamBitrate: Int? = null,
    val liveStreamMaximumStreamBitrate: Int? = null,
    val liveStreamLensSupported: Boolean? = null,
    val liveStreamLensSupportedArray: List<open_gopro.EnumLens> = emptyList(),
    val liveStreamProtuneSupported: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.NotifyLiveStreamStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifyLiveStreamStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.NotifyLiveStreamStatus> {
        public val defaultInstance: open_gopro.NotifyLiveStreamStatus by lazy { open_gopro.NotifyLiveStreamStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.NotifyLiveStreamStatus = open_gopro.NotifyLiveStreamStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.NotifyLiveStreamStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifyLiveStreamStatus",
            messageClass = open_gopro.NotifyLiveStreamStatus::class,
            messageCompanion = this,
            fields = buildList(12) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumLiveStreamStatus.Companion, hasPresence = true),
                        jsonName = "liveStreamStatus",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamStatus
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_error",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumLiveStreamError.Companion, hasPresence = true),
                        jsonName = "liveStreamError",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamError
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_encode",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "liveStreamEncode",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamEncode
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_bitrate",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "liveStreamBitrate",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamBitrate
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_window_size_supported_array",
                        number = 5,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.EnumWindowSize>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumWindowSize.Companion)),
                        jsonName = "liveStreamWindowSizeSupportedArray",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamWindowSizeSupportedArray
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_encode_supported",
                        number = 6,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "liveStreamEncodeSupported",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamEncodeSupported
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_max_lens_unsupported",
                        number = 7,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "liveStreamMaxLensUnsupported",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamMaxLensUnsupported
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_minimum_stream_bitrate",
                        number = 8,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "liveStreamMinimumStreamBitrate",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamMinimumStreamBitrate
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_maximum_stream_bitrate",
                        number = 9,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "liveStreamMaximumStreamBitrate",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamMaximumStreamBitrate
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_lens_supported",
                        number = 10,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "liveStreamLensSupported",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamLensSupported
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_lens_supported_array",
                        number = 11,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.EnumLens>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumLens.Companion)),
                        jsonName = "liveStreamLensSupportedArray",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamLensSupportedArray
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "live_stream_protune_supported",
                        number = 13,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "liveStreamProtuneSupported",
                        value = open_gopro.NotifyLiveStreamStatus::liveStreamProtuneSupported
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestGetLiveStreamStatus(
    val registerLiveStreamStatus: List<open_gopro.EnumRegisterLiveStreamStatus> = emptyList(),
    val unregisterLiveStreamStatus: List<open_gopro.EnumRegisterLiveStreamStatus> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestGetLiveStreamStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetLiveStreamStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestGetLiveStreamStatus> {
        public val defaultInstance: open_gopro.RequestGetLiveStreamStatus by lazy { open_gopro.RequestGetLiveStreamStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestGetLiveStreamStatus = open_gopro.RequestGetLiveStreamStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetLiveStreamStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetLiveStreamStatus",
            messageClass = open_gopro.RequestGetLiveStreamStatus::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "register_live_stream_status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.EnumRegisterLiveStreamStatus>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumRegisterLiveStreamStatus.Companion)),
                        jsonName = "registerLiveStreamStatus",
                        value = open_gopro.RequestGetLiveStreamStatus::registerLiveStreamStatus
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "unregister_live_stream_status",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.EnumRegisterLiveStreamStatus>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumRegisterLiveStreamStatus.Companion)),
                        jsonName = "unregisterLiveStreamStatus",
                        value = open_gopro.RequestGetLiveStreamStatus::unregisterLiveStreamStatus
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class RequestSetLiveStreamMode(
    val url: String? = null,
    val encode: Boolean? = null,
    val windowSize: open_gopro.EnumWindowSize? = null,
    val cert: pbandk.ByteArr? = null,
    val minimumBitrate: Int? = null,
    val maximumBitrate: Int? = null,
    val startingBitrate: Int? = null,
    val lens: open_gopro.EnumLens? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestSetLiveStreamMode = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestSetLiveStreamMode> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestSetLiveStreamMode> {
        public val defaultInstance: open_gopro.RequestSetLiveStreamMode by lazy { open_gopro.RequestSetLiveStreamMode() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestSetLiveStreamMode = open_gopro.RequestSetLiveStreamMode.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestSetLiveStreamMode> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetLiveStreamMode",
            messageClass = open_gopro.RequestSetLiveStreamMode::class,
            messageCompanion = this,
            fields = buildList(8) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "url",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "url",
                        value = open_gopro.RequestSetLiveStreamMode::url
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "encode",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "encode",
                        value = open_gopro.RequestSetLiveStreamMode::encode
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "window_size",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumWindowSize.Companion, hasPresence = true),
                        jsonName = "windowSize",
                        value = open_gopro.RequestSetLiveStreamMode::windowSize
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "cert",
                        number = 6,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                        jsonName = "cert",
                        value = open_gopro.RequestSetLiveStreamMode::cert
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "minimum_bitrate",
                        number = 7,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "minimumBitrate",
                        value = open_gopro.RequestSetLiveStreamMode::minimumBitrate
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "maximum_bitrate",
                        number = 8,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "maximumBitrate",
                        value = open_gopro.RequestSetLiveStreamMode::maximumBitrate
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "starting_bitrate",
                        number = 9,
                        type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                        jsonName = "startingBitrate",
                        value = open_gopro.RequestSetLiveStreamMode::startingBitrate
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "lens",
                        number = 10,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumLens.Companion, hasPresence = true),
                        jsonName = "lens",
                        value = open_gopro.RequestSetLiveStreamMode::lens
                    )
                )
            }
        )
    }
}

@pbandk.Export
@pbandk.JsName("orDefaultForNotifyLiveStreamStatus")
public fun NotifyLiveStreamStatus?.orDefault(): open_gopro.NotifyLiveStreamStatus = this ?: NotifyLiveStreamStatus.defaultInstance

private fun NotifyLiveStreamStatus.protoMergeImpl(plus: pbandk.Message?): NotifyLiveStreamStatus = (plus as? NotifyLiveStreamStatus)?.let {
    it.copy(
        liveStreamStatus = plus.liveStreamStatus ?: liveStreamStatus,
        liveStreamError = plus.liveStreamError ?: liveStreamError,
        liveStreamEncode = plus.liveStreamEncode ?: liveStreamEncode,
        liveStreamBitrate = plus.liveStreamBitrate ?: liveStreamBitrate,
        liveStreamWindowSizeSupportedArray = liveStreamWindowSizeSupportedArray + plus.liveStreamWindowSizeSupportedArray,
        liveStreamEncodeSupported = plus.liveStreamEncodeSupported ?: liveStreamEncodeSupported,
        liveStreamMaxLensUnsupported = plus.liveStreamMaxLensUnsupported ?: liveStreamMaxLensUnsupported,
        liveStreamMinimumStreamBitrate = plus.liveStreamMinimumStreamBitrate ?: liveStreamMinimumStreamBitrate,
        liveStreamMaximumStreamBitrate = plus.liveStreamMaximumStreamBitrate ?: liveStreamMaximumStreamBitrate,
        liveStreamLensSupported = plus.liveStreamLensSupported ?: liveStreamLensSupported,
        liveStreamLensSupportedArray = liveStreamLensSupportedArray + plus.liveStreamLensSupportedArray,
        liveStreamProtuneSupported = plus.liveStreamProtuneSupported ?: liveStreamProtuneSupported,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifyLiveStreamStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): NotifyLiveStreamStatus {
    var liveStreamStatus: open_gopro.EnumLiveStreamStatus? = null
    var liveStreamError: open_gopro.EnumLiveStreamError? = null
    var liveStreamEncode: Boolean? = null
    var liveStreamBitrate: Int? = null
    var liveStreamWindowSizeSupportedArray: pbandk.ListWithSize.Builder<open_gopro.EnumWindowSize>? = null
    var liveStreamEncodeSupported: Boolean? = null
    var liveStreamMaxLensUnsupported: Boolean? = null
    var liveStreamMinimumStreamBitrate: Int? = null
    var liveStreamMaximumStreamBitrate: Int? = null
    var liveStreamLensSupported: Boolean? = null
    var liveStreamLensSupportedArray: pbandk.ListWithSize.Builder<open_gopro.EnumLens>? = null
    var liveStreamProtuneSupported: Boolean? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> liveStreamStatus = _fieldValue as open_gopro.EnumLiveStreamStatus
            2 -> liveStreamError = _fieldValue as open_gopro.EnumLiveStreamError
            3 -> liveStreamEncode = _fieldValue as Boolean
            4 -> liveStreamBitrate = _fieldValue as Int
            5 -> liveStreamWindowSizeSupportedArray = (liveStreamWindowSizeSupportedArray ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.EnumWindowSize> }
            6 -> liveStreamEncodeSupported = _fieldValue as Boolean
            7 -> liveStreamMaxLensUnsupported = _fieldValue as Boolean
            8 -> liveStreamMinimumStreamBitrate = _fieldValue as Int
            9 -> liveStreamMaximumStreamBitrate = _fieldValue as Int
            10 -> liveStreamLensSupported = _fieldValue as Boolean
            11 -> liveStreamLensSupportedArray = (liveStreamLensSupportedArray ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.EnumLens> }
            13 -> liveStreamProtuneSupported = _fieldValue as Boolean
        }
    }

    return NotifyLiveStreamStatus(liveStreamStatus, liveStreamError, liveStreamEncode, liveStreamBitrate,
        pbandk.ListWithSize.Builder.fixed(liveStreamWindowSizeSupportedArray), liveStreamEncodeSupported, liveStreamMaxLensUnsupported, liveStreamMinimumStreamBitrate,
        liveStreamMaximumStreamBitrate, liveStreamLensSupported, pbandk.ListWithSize.Builder.fixed(liveStreamLensSupportedArray), liveStreamProtuneSupported, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetLiveStreamStatus")
public fun RequestGetLiveStreamStatus?.orDefault(): open_gopro.RequestGetLiveStreamStatus = this ?: RequestGetLiveStreamStatus.defaultInstance

private fun RequestGetLiveStreamStatus.protoMergeImpl(plus: pbandk.Message?): RequestGetLiveStreamStatus = (plus as? RequestGetLiveStreamStatus)?.let {
    it.copy(
        registerLiveStreamStatus = registerLiveStreamStatus + plus.registerLiveStreamStatus,
        unregisterLiveStreamStatus = unregisterLiveStreamStatus + plus.unregisterLiveStreamStatus,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetLiveStreamStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestGetLiveStreamStatus {
    var registerLiveStreamStatus: pbandk.ListWithSize.Builder<open_gopro.EnumRegisterLiveStreamStatus>? = null
    var unregisterLiveStreamStatus: pbandk.ListWithSize.Builder<open_gopro.EnumRegisterLiveStreamStatus>? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> registerLiveStreamStatus = (registerLiveStreamStatus ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.EnumRegisterLiveStreamStatus> }
            2 -> unregisterLiveStreamStatus = (unregisterLiveStreamStatus ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.EnumRegisterLiveStreamStatus> }
        }
    }

    return RequestGetLiveStreamStatus(pbandk.ListWithSize.Builder.fixed(registerLiveStreamStatus), pbandk.ListWithSize.Builder.fixed(unregisterLiveStreamStatus), unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestSetLiveStreamMode")
public fun RequestSetLiveStreamMode?.orDefault(): open_gopro.RequestSetLiveStreamMode = this ?: RequestSetLiveStreamMode.defaultInstance

private fun RequestSetLiveStreamMode.protoMergeImpl(plus: pbandk.Message?): RequestSetLiveStreamMode = (plus as? RequestSetLiveStreamMode)?.let {
    it.copy(
        url = plus.url ?: url,
        encode = plus.encode ?: encode,
        windowSize = plus.windowSize ?: windowSize,
        cert = plus.cert ?: cert,
        minimumBitrate = plus.minimumBitrate ?: minimumBitrate,
        maximumBitrate = plus.maximumBitrate ?: maximumBitrate,
        startingBitrate = plus.startingBitrate ?: startingBitrate,
        lens = plus.lens ?: lens,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetLiveStreamMode.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestSetLiveStreamMode {
    var url: String? = null
    var encode: Boolean? = null
    var windowSize: open_gopro.EnumWindowSize? = null
    var cert: pbandk.ByteArr? = null
    var minimumBitrate: Int? = null
    var maximumBitrate: Int? = null
    var startingBitrate: Int? = null
    var lens: open_gopro.EnumLens? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> url = _fieldValue as String
            2 -> encode = _fieldValue as Boolean
            3 -> windowSize = _fieldValue as open_gopro.EnumWindowSize
            6 -> cert = _fieldValue as pbandk.ByteArr
            7 -> minimumBitrate = _fieldValue as Int
            8 -> maximumBitrate = _fieldValue as Int
            9 -> startingBitrate = _fieldValue as Int
            10 -> lens = _fieldValue as open_gopro.EnumLens
        }
    }

    return RequestSetLiveStreamMode(url, encode, windowSize, cert,
        minimumBitrate, maximumBitrate, startingBitrate, lens, unknownFields)
}
