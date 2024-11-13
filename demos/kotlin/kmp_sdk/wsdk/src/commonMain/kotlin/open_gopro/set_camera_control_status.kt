@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public sealed class EnumCameraControlStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumCameraControlStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumCameraControlStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object CAMERA_IDLE : EnumCameraControlStatus(0, "CAMERA_IDLE")
    public object CAMERA_CONTROL : EnumCameraControlStatus(1, "CAMERA_CONTROL")
    public object CAMERA_EXTERNAL_CONTROL : EnumCameraControlStatus(2, "CAMERA_EXTERNAL_CONTROL")
    public object CAMERA_COF_SETUP : EnumCameraControlStatus(3, "CAMERA_COF_SETUP")
    public class UNRECOGNIZED(value: Int) : EnumCameraControlStatus(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumCameraControlStatus> {
        public val values: List<open_gopro.EnumCameraControlStatus> by lazy { listOf(CAMERA_IDLE, CAMERA_CONTROL, CAMERA_EXTERNAL_CONTROL, CAMERA_COF_SETUP) }
        override fun fromValue(value: Int): open_gopro.EnumCameraControlStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumCameraControlStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumCameraControlStatus with name: $name")
    }
}

@pbandk.Export
public data class RequestSetCameraControlStatus(
    val cameraControlStatus: open_gopro.EnumCameraControlStatus,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestSetCameraControlStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestSetCameraControlStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestSetCameraControlStatus> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestSetCameraControlStatus = open_gopro.RequestSetCameraControlStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestSetCameraControlStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetCameraControlStatus",
            messageClass = open_gopro.RequestSetCameraControlStatus::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "camera_control_status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumCameraControlStatus.Companion, hasPresence = true),
                        jsonName = "cameraControlStatus",
                        value = open_gopro.RequestSetCameraControlStatus::cameraControlStatus
                    )
                )
            }
        )
    }
}

private fun RequestSetCameraControlStatus.protoMergeImpl(plus: pbandk.Message?): RequestSetCameraControlStatus = (plus as? RequestSetCameraControlStatus)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetCameraControlStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestSetCameraControlStatus {
    var cameraControlStatus: open_gopro.EnumCameraControlStatus? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> cameraControlStatus = _fieldValue as open_gopro.EnumCameraControlStatus
        }
    }

    if (cameraControlStatus == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("camera_control_status")
    }
    return RequestSetCameraControlStatus(cameraControlStatus!!, unknownFields)
}
