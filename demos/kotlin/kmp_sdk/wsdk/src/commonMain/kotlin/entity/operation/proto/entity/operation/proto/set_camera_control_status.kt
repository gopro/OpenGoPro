@file:OptIn(pbandk.PublicForGeneratedCode::class)

package entity.operation.proto

@pbandk.Export
internal sealed class EnumCameraControlStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is entity.operation.proto.EnumCameraControlStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumCameraControlStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

    internal object CAMERA_IDLE : EnumCameraControlStatus(0, "CAMERA_IDLE")
    internal object CAMERA_CONTROL : EnumCameraControlStatus(1, "CAMERA_CONTROL")
    internal object CAMERA_EXTERNAL_CONTROL : EnumCameraControlStatus(2, "CAMERA_EXTERNAL_CONTROL")
    internal object CAMERA_COF_SETUP : EnumCameraControlStatus(3, "CAMERA_COF_SETUP")
    internal class UNRECOGNIZED(value: Int) : EnumCameraControlStatus(value)

    internal companion object : pbandk.Message.Enum.Companion<entity.operation.proto.EnumCameraControlStatus> {
        internal val values: List<entity.operation.proto.EnumCameraControlStatus> by lazy { listOf(CAMERA_IDLE, CAMERA_CONTROL, CAMERA_EXTERNAL_CONTROL, CAMERA_COF_SETUP) }
        override fun fromValue(value: Int): entity.operation.proto.EnumCameraControlStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): entity.operation.proto.EnumCameraControlStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumCameraControlStatus with name: $name")
    }
}

@pbandk.Export
internal data class RequestSetCameraControlStatus(
    val cameraControlStatus: entity.operation.proto.EnumCameraControlStatus,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.RequestSetCameraControlStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestSetCameraControlStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.RequestSetCameraControlStatus> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.RequestSetCameraControlStatus = entity.operation.proto.RequestSetCameraControlStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestSetCameraControlStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetCameraControlStatus",
            messageClass = entity.operation.proto.RequestSetCameraControlStatus::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "camera_control_status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumCameraControlStatus.Companion, hasPresence = true),
                        jsonName = "cameraControlStatus",
                        value = entity.operation.proto.RequestSetCameraControlStatus::cameraControlStatus
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
    var cameraControlStatus: entity.operation.proto.EnumCameraControlStatus? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> cameraControlStatus = _fieldValue as entity.operation.proto.EnumCameraControlStatus
        }
    }

    if (cameraControlStatus == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("camera_control_status")
    }
    return RequestSetCameraControlStatus(cameraControlStatus!!, unknownFields)
}
