@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public sealed class EnumResultGeneric(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is open_gopro.EnumResultGeneric && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumResultGeneric.${name ?: "UNRECOGNIZED"}(value=$value)"

    public object RESULT_UNKNOWN : EnumResultGeneric(0, "RESULT_UNKNOWN")
    public object RESULT_SUCCESS : EnumResultGeneric(1, "RESULT_SUCCESS")
    public object RESULT_ILL_FORMED : EnumResultGeneric(2, "RESULT_ILL_FORMED")
    public object RESULT_NOT_SUPPORTED : EnumResultGeneric(3, "RESULT_NOT_SUPPORTED")
    public object RESULT_ARGUMENT_OUT_OF_BOUNDS : EnumResultGeneric(4, "RESULT_ARGUMENT_OUT_OF_BOUNDS")
    public object RESULT_ARGUMENT_INVALID : EnumResultGeneric(5, "RESULT_ARGUMENT_INVALID")
    public object RESULT_RESOURCE_NOT_AVAILABLE : EnumResultGeneric(6, "RESULT_RESOURCE_NOT_AVAILABLE")
    public class UNRECOGNIZED(value: Int) : EnumResultGeneric(value)

    public companion object : pbandk.Message.Enum.Companion<open_gopro.EnumResultGeneric> {
        public val values: List<open_gopro.EnumResultGeneric> by lazy { listOf(RESULT_UNKNOWN, RESULT_SUCCESS, RESULT_ILL_FORMED, RESULT_NOT_SUPPORTED, RESULT_ARGUMENT_OUT_OF_BOUNDS, RESULT_ARGUMENT_INVALID, RESULT_RESOURCE_NOT_AVAILABLE) }
        override fun fromValue(value: Int): open_gopro.EnumResultGeneric = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): open_gopro.EnumResultGeneric = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumResultGeneric with name: $name")
    }
}

@pbandk.Export
public data class ResponseGeneric(
    val result: open_gopro.EnumResultGeneric,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.ResponseGeneric = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseGeneric> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.ResponseGeneric> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.ResponseGeneric = open_gopro.ResponseGeneric.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseGeneric> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseGeneric",
            messageClass = open_gopro.ResponseGeneric::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = open_gopro.ResponseGeneric::result
                    )
                )
            }
        )
    }
}

@pbandk.Export
public data class Media(
    val folder: String? = null,
    val file: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.Media = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.Media> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.Media> {
        public val defaultInstance: open_gopro.Media by lazy { open_gopro.Media() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.Media = open_gopro.Media.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.Media> = pbandk.MessageDescriptor(
            fullName = "open_gopro.Media",
            messageClass = open_gopro.Media::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "folder",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "folder",
                        value = open_gopro.Media::folder
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "file",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                        jsonName = "file",
                        value = open_gopro.Media::file
                    )
                )
            }
        )
    }
}

private fun ResponseGeneric.protoMergeImpl(plus: pbandk.Message?): ResponseGeneric = (plus as? ResponseGeneric)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseGeneric.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseGeneric {
    var result: open_gopro.EnumResultGeneric? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as open_gopro.EnumResultGeneric
        }
    }

    if (result == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
    }
    return ResponseGeneric(result!!, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForMedia")
public fun Media?.orDefault(): open_gopro.Media = this ?: Media.defaultInstance

private fun Media.protoMergeImpl(plus: pbandk.Message?): Media = (plus as? Media)?.let {
    it.copy(
        folder = plus.folder ?: folder,
        file = plus.file ?: file,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun Media.Companion.decodeWithImpl(u: pbandk.MessageDecoder): Media {
    var folder: String? = null
    var file: String? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> folder = _fieldValue as String
            2 -> file = _fieldValue as String
        }
    }

    return Media(folder, file, unknownFields)
}
