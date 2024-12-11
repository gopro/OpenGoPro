@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.entity.operation.proto

@pbandk.Export
internal sealed class EnumRegisterPresetStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumRegisterPresetStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

    internal object REGISTER_PRESET_STATUS_PRESET : EnumRegisterPresetStatus(1, "REGISTER_PRESET_STATUS_PRESET")
    internal object REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY : EnumRegisterPresetStatus(2, "REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY")
    internal class UNRECOGNIZED(value: Int) : EnumRegisterPresetStatus(value)

    internal companion object : pbandk.Message.Enum.Companion<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus> {
        internal val values: List<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus> by lazy { listOf(REGISTER_PRESET_STATUS_PRESET, REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY) }
        override fun fromValue(value: Int): com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumRegisterPresetStatus with name: $name")
    }
}

@pbandk.Export
internal data class RequestGetPresetStatus(
    val registerPresetStatus: List<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus> = emptyList(),
    val unregisterPresetStatus: List<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus> {
        internal val defaultInstance: com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus by lazy { com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus = com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetPresetStatus",
            messageClass = com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "register_preset_status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Repeated<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus.Companion)),
                        jsonName = "registerPresetStatus",
                        value = com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus::registerPresetStatus
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "unregister_preset_status",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Repeated<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus.Companion)),
                        jsonName = "unregisterPresetStatus",
                        value = com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus::unregisterPresetStatus
                    )
                )
            }
        )
    }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetPresetStatus")
internal fun RequestGetPresetStatus?.orDefault(): com.gopro.open_gopro.entity.operation.proto.RequestGetPresetStatus = this ?: RequestGetPresetStatus.defaultInstance

private fun RequestGetPresetStatus.protoMergeImpl(plus: pbandk.Message?): RequestGetPresetStatus = (plus as? RequestGetPresetStatus)?.let {
    it.copy(
        registerPresetStatus = registerPresetStatus + plus.registerPresetStatus,
        unregisterPresetStatus = unregisterPresetStatus + plus.unregisterPresetStatus,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetPresetStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestGetPresetStatus {
    var registerPresetStatus: pbandk.ListWithSize.Builder<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus>? = null
    var unregisterPresetStatus: pbandk.ListWithSize.Builder<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus>? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> registerPresetStatus = (registerPresetStatus ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus> }
            2 -> unregisterPresetStatus = (unregisterPresetStatus ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<com.gopro.open_gopro.entity.operation.proto.EnumRegisterPresetStatus> }
        }
    }

    return RequestGetPresetStatus(pbandk.ListWithSize.Builder.fixed(registerPresetStatus), pbandk.ListWithSize.Builder.fixed(unregisterPresetStatus), unknownFields)
}
