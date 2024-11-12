@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public data class RequestSetTurboActive(
    val active: Boolean,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestSetTurboActive = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestSetTurboActive> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestSetTurboActive> {
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestSetTurboActive = open_gopro.RequestSetTurboActive.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestSetTurboActive> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetTurboActive",
            messageClass = open_gopro.RequestSetTurboActive::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "active",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "active",
                        value = open_gopro.RequestSetTurboActive::active
                    )
                )
            }
        )
    }
}

private fun RequestSetTurboActive.protoMergeImpl(plus: pbandk.Message?): RequestSetTurboActive = (plus as? RequestSetTurboActive)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetTurboActive.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestSetTurboActive {
    var active: Boolean? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> active = _fieldValue as Boolean
        }
    }

    if (active == null) {
        throw pbandk.InvalidProtocolBufferException.missingRequiredField("active")
    }
    return RequestSetTurboActive(active!!, unknownFields)
}
