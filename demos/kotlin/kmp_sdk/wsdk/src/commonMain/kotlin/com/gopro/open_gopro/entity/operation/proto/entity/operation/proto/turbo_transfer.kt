@file:OptIn(pbandk.PublicForGeneratedCode::class)

package entity.operation.proto

@pbandk.Export
internal data class RequestSetTurboActive(
    val active: Boolean,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.RequestSetTurboActive = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestSetTurboActive> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.RequestSetTurboActive> {
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.RequestSetTurboActive = entity.operation.proto.RequestSetTurboActive.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestSetTurboActive> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetTurboActive",
            messageClass = entity.operation.proto.RequestSetTurboActive::class,
            messageCompanion = this,
            fields = buildList(1) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "active",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "active",
                        value = entity.operation.proto.RequestSetTurboActive::active
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
