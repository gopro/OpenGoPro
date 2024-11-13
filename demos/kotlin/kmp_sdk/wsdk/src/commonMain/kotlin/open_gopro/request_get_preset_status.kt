@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public sealed class EnumRegisterPresetStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumRegisterPresetStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumRegisterPresetStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object REGISTER_PRESET_STATUS_PRESET : EnumRegisterPresetStatus(1, "REGISTER_PRESET_STATUS_PRESET")
    public object REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY : EnumRegisterPresetStatus(2, "REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY")
    public class UNRECOGNIZED(value: Int) : EnumRegisterPresetStatus(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumRegisterPresetStatus> {
        public val values: List<open_gopro.EnumRegisterPresetStatus> by lazy { listOf(REGISTER_PRESET_STATUS_PRESET, REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY) }
        override fun fromValue(value: Int): open_gopro.EnumRegisterPresetStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumRegisterPresetStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumRegisterPresetStatus with name: $name")
    }
}

@pbandk.Export
public data class RequestGetPresetStatus(
    val registerPresetStatus: List<open_gopro.EnumRegisterPresetStatus> = emptyList(),
    val unregisterPresetStatus: List<open_gopro.EnumRegisterPresetStatus> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestGetPresetStatus = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetPresetStatus> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestGetPresetStatus> {
        public val defaultInstance: open_gopro.RequestGetPresetStatus by lazy { open_gopro.RequestGetPresetStatus() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestGetPresetStatus = open_gopro.RequestGetPresetStatus.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetPresetStatus> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetPresetStatus",
            messageClass = open_gopro.RequestGetPresetStatus::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "register_preset_status",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.EnumRegisterPresetStatus>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumRegisterPresetStatus.Companion)),
                        jsonName = "registerPresetStatus",
                        value = open_gopro.RequestGetPresetStatus::registerPresetStatus
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "unregister_preset_status",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Repeated<open_gopro.EnumRegisterPresetStatus>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumRegisterPresetStatus.Companion)),
                        jsonName = "unregisterPresetStatus",
                        value = open_gopro.RequestGetPresetStatus::unregisterPresetStatus
                    )
                )
            }
        )
    }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetPresetStatus")
public fun RequestGetPresetStatus?.orDefault(): open_gopro.RequestGetPresetStatus = this ?: RequestGetPresetStatus.defaultInstance

private fun RequestGetPresetStatus.protoMergeImpl(plus: pbandk.Message?): RequestGetPresetStatus = (plus as? RequestGetPresetStatus)?.let {
    it.copy(
        registerPresetStatus = registerPresetStatus + plus.registerPresetStatus,
        unregisterPresetStatus = unregisterPresetStatus + plus.unregisterPresetStatus,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetPresetStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestGetPresetStatus {
    var registerPresetStatus: pbandk.ListWithSize.Builder<open_gopro.EnumRegisterPresetStatus>? = null
    var unregisterPresetStatus: pbandk.ListWithSize.Builder<open_gopro.EnumRegisterPresetStatus>? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> registerPresetStatus = (registerPresetStatus ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.EnumRegisterPresetStatus> }
            2 -> unregisterPresetStatus = (unregisterPresetStatus ?: pbandk.ListWithSize.Builder()).apply { this += _fieldValue as kotlin.sequences.Sequence<open_gopro.EnumRegisterPresetStatus> }
        }
    }

    return RequestGetPresetStatus(pbandk.ListWithSize.Builder.fixed(registerPresetStatus), pbandk.ListWithSize.Builder.fixed(unregisterPresetStatus), unknownFields)
}
