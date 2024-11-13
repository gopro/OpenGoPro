@file:OptIn(pbandk.PublicForGeneratedCode::class)

package open_gopro

@pbandk.Export
public data class RequestGetLastCapturedMedia(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.RequestGetLastCapturedMedia = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetLastCapturedMedia> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.RequestGetLastCapturedMedia> {
        public val defaultInstance: open_gopro.RequestGetLastCapturedMedia by lazy { open_gopro.RequestGetLastCapturedMedia() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.RequestGetLastCapturedMedia = open_gopro.RequestGetLastCapturedMedia.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.RequestGetLastCapturedMedia> = pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetLastCapturedMedia",
            messageClass = open_gopro.RequestGetLastCapturedMedia::class,
            messageCompanion = this,
            fields = buildList(0) {
            }
        )
    }
}

@pbandk.Export
public data class ResponseLastCapturedMedia(
    val result: open_gopro.EnumResultGeneric? = null,
    val media: open_gopro.Media? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): open_gopro.ResponseLastCapturedMedia = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseLastCapturedMedia> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    public companion object : pbandk.Message.Companion<open_gopro.ResponseLastCapturedMedia> {
        public val defaultInstance: open_gopro.ResponseLastCapturedMedia by lazy { open_gopro.ResponseLastCapturedMedia() }
        override fun decodeWith(u: pbandk.MessageDecoder): open_gopro.ResponseLastCapturedMedia = open_gopro.ResponseLastCapturedMedia.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<open_gopro.ResponseLastCapturedMedia> = pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseLastCapturedMedia",
            messageClass = open_gopro.ResponseLastCapturedMedia::class,
            messageCompanion = this,
            fields = buildList(2) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "result",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = open_gopro.EnumResultGeneric.Companion, hasPresence = true),
                        jsonName = "result",
                        value = open_gopro.ResponseLastCapturedMedia::result
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "media",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Message(messageCompanion = open_gopro.Media.Companion),
                        jsonName = "media",
                        value = open_gopro.ResponseLastCapturedMedia::media
                    )
                )
            }
        )
    }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetLastCapturedMedia")
public fun RequestGetLastCapturedMedia?.orDefault(): open_gopro.RequestGetLastCapturedMedia = this ?: RequestGetLastCapturedMedia.defaultInstance

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
public fun ResponseLastCapturedMedia?.orDefault(): open_gopro.ResponseLastCapturedMedia = this ?: ResponseLastCapturedMedia.defaultInstance

private fun ResponseLastCapturedMedia.protoMergeImpl(plus: pbandk.Message?): ResponseLastCapturedMedia = (plus as? ResponseLastCapturedMedia)?.let {
    it.copy(
        result = plus.result ?: result,
        media = media?.plus(plus.media) ?: plus.media,
        unknownFields = unknownFields + plus.unknownFields
    )
} ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseLastCapturedMedia.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseLastCapturedMedia {
    var result: open_gopro.EnumResultGeneric? = null
    var media: open_gopro.Media? = null

    val unknownFields = u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
            1 -> result = _fieldValue as open_gopro.EnumResultGeneric
            2 -> media = _fieldValue as open_gopro.Media
        }
    }

    return ResponseLastCapturedMedia(result, media, unknownFields)
}
