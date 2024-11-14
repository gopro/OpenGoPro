@file:OptIn(pbandk.PublicForGeneratedCode::class)

package entity.operation.proto

@pbandk.Export
internal data class RequestGetLastCapturedMedia(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.RequestGetLastCapturedMedia = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestGetLastCapturedMedia> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.RequestGetLastCapturedMedia> {
        internal val defaultInstance: entity.operation.proto.RequestGetLastCapturedMedia by lazy { entity.operation.proto.RequestGetLastCapturedMedia() }
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.RequestGetLastCapturedMedia = entity.operation.proto.RequestGetLastCapturedMedia.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.RequestGetLastCapturedMedia> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetLastCapturedMedia",
            messageClass = entity.operation.proto.RequestGetLastCapturedMedia::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
internal data class ResponseLastCapturedMedia(
    val result: entity.operation.proto.EnumResultGeneric? = null,
    val media: entity.operation.proto.Media? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): entity.operation.proto.ResponseLastCapturedMedia = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseLastCapturedMedia> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<entity.operation.proto.ResponseLastCapturedMedia> {
        internal val defaultInstance: entity.operation.proto.ResponseLastCapturedMedia by lazy { entity.operation.proto.ResponseLastCapturedMedia() }
        override fun decodeWith(u: pbandk.MessageDecoder): entity.operation.proto.ResponseLastCapturedMedia = entity.operation.proto.ResponseLastCapturedMedia.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<entity.operation.proto.ResponseLastCapturedMedia> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseLastCapturedMedia",
            messageClass = entity.operation.proto.ResponseLastCapturedMedia::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = entity.operation.proto.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = entity.operation.proto.ResponseLastCapturedMedia::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "media",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Message(messageCompanion = entity.operation.proto.Media.Companion),
                        jsonName = "media",
                        value = entity.operation.proto.ResponseLastCapturedMedia::media
                    )
                )
            }
        )
    }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetLastCapturedMedia")
internal fun RequestGetLastCapturedMedia?.orDefault(): entity.operation.proto.RequestGetLastCapturedMedia = this ?: RequestGetLastCapturedMedia.defaultInstance

private fun RequestGetLastCapturedMedia.protoMergeImpl(plus: pbandk.Message?): RequestGetLastCapturedMedia = (plus as? RequestGetLastCapturedMedia)?.let {
    it.copy(
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetLastCapturedMedia.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestGetLastCapturedMedia {

    val unknownFields = u.readMessage(this) { _, _ -> }

    return RequestGetLastCapturedMedia(unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForResponseLastCapturedMedia")
internal fun ResponseLastCapturedMedia?.orDefault(): entity.operation.proto.ResponseLastCapturedMedia = this ?: ResponseLastCapturedMedia.defaultInstance

private fun ResponseLastCapturedMedia.protoMergeImpl(plus: pbandk.Message?): ResponseLastCapturedMedia = (plus as? ResponseLastCapturedMedia)?.let {
    it.copy(
        result = plus.result ?: result,
        media = media?.plus(plus.media) ?: plus.media,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseLastCapturedMedia.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseLastCapturedMedia {
    var result: entity.operation.proto.EnumResultGeneric? = null
    var media: entity.operation.proto.Media? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as entity.operation.proto.EnumResultGeneric
            2 -> media = _fieldValue as entity.operation.proto.Media
        }
    }

    return ResponseLastCapturedMedia(result, media, unknownFields)
}
