/* media.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal data class RequestGetLastCapturedMedia(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestGetLastCapturedMedia = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetLastCapturedMedia>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestGetLastCapturedMedia> {
    internal val defaultInstance:
        com.gopro.open_gopro.operations.RequestGetLastCapturedMedia by lazy {
      com.gopro.open_gopro.operations.RequestGetLastCapturedMedia()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestGetLastCapturedMedia =
        com.gopro.open_gopro.operations.RequestGetLastCapturedMedia.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetLastCapturedMedia> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetLastCapturedMedia",
            messageClass = com.gopro.open_gopro.operations.RequestGetLastCapturedMedia::class,
            messageCompanion = this,
            fields = buildList(0) {})
  }
}

@pbandk.Export
internal data class ResponseLastCapturedMedia(
    val result: com.gopro.open_gopro.operations.EnumResultGeneric? = null,
    val media: com.gopro.open_gopro.operations.Media? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ResponseLastCapturedMedia = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseLastCapturedMedia>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseLastCapturedMedia> {
    internal val defaultInstance:
        com.gopro.open_gopro.operations.ResponseLastCapturedMedia by lazy {
      com.gopro.open_gopro.operations.ResponseLastCapturedMedia()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ResponseLastCapturedMedia =
        com.gopro.open_gopro.operations.ResponseLastCapturedMedia.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseLastCapturedMedia> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseLastCapturedMedia",
            messageClass = com.gopro.open_gopro.operations.ResponseLastCapturedMedia::class,
            messageCompanion = this,
            fields =
                buildList(2) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "result",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumResultGeneric.Companion,
                                  hasPresence = true),
                          jsonName = "result",
                          value =
                              com.gopro.open_gopro.operations.ResponseLastCapturedMedia::result))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "media",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Message(
                                  messageCompanion =
                                      com.gopro.open_gopro.operations.Media.Companion),
                          jsonName = "media",
                          value = com.gopro.open_gopro.operations.ResponseLastCapturedMedia::media))
                })
  }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetLastCapturedMedia")
internal fun RequestGetLastCapturedMedia?.orDefault():
    com.gopro.open_gopro.operations.RequestGetLastCapturedMedia =
    this ?: RequestGetLastCapturedMedia.defaultInstance

private fun RequestGetLastCapturedMedia.protoMergeImpl(
    plus: pbandk.Message?
): RequestGetLastCapturedMedia =
    (plus as? RequestGetLastCapturedMedia)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetLastCapturedMedia.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestGetLastCapturedMedia {

  val unknownFields = u.readMessage(this) { _, _ -> }

  return RequestGetLastCapturedMedia(unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForResponseLastCapturedMedia")
internal fun ResponseLastCapturedMedia?.orDefault():
    com.gopro.open_gopro.operations.ResponseLastCapturedMedia =
    this ?: ResponseLastCapturedMedia.defaultInstance

private fun ResponseLastCapturedMedia.protoMergeImpl(
    plus: pbandk.Message?
): ResponseLastCapturedMedia =
    (plus as? ResponseLastCapturedMedia)?.let {
      it.copy(
          result = plus.result ?: result,
          media = media?.plus(plus.media) ?: plus.media,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseLastCapturedMedia.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): ResponseLastCapturedMedia {
  var result: com.gopro.open_gopro.operations.EnumResultGeneric? = null
  var media: com.gopro.open_gopro.operations.Media? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumResultGeneric
          2 -> media = _fieldValue as com.gopro.open_gopro.operations.Media
        }
      }

  return ResponseLastCapturedMedia(result, media, unknownFields)
}
