/* turbo_transfer.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal data class RequestSetTurboActive(
    val active: Boolean,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestSetTurboActive = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetTurboActive>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestSetTurboActive> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestSetTurboActive =
        com.gopro.open_gopro.operations.RequestSetTurboActive.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetTurboActive> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetTurboActive",
            messageClass = com.gopro.open_gopro.operations.RequestSetTurboActive::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "active",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "active",
                          value = com.gopro.open_gopro.operations.RequestSetTurboActive::active))
                })
  }
}

private fun RequestSetTurboActive.protoMergeImpl(plus: pbandk.Message?): RequestSetTurboActive =
    (plus as? RequestSetTurboActive)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetTurboActive.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestSetTurboActive {
  var active: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> active = _fieldValue as Boolean
        }
      }

  if (active == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("active")
  }
  return RequestSetTurboActive(active!!, unknownFields)
}
