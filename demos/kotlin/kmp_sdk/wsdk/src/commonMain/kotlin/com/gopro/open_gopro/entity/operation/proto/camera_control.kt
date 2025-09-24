/* camera_control.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal data class RequestSetCameraName(
    val name: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestSetCameraName = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetCameraName>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestSetCameraName> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestSetCameraName by lazy {
      com.gopro.open_gopro.operations.RequestSetCameraName()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestSetCameraName =
        com.gopro.open_gopro.operations.RequestSetCameraName.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetCameraName> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetCameraName",
            messageClass = com.gopro.open_gopro.operations.RequestSetCameraName::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "name",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "name",
                          value = com.gopro.open_gopro.operations.RequestSetCameraName::name))
                })
  }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestSetCameraName")
internal fun RequestSetCameraName?.orDefault():
    com.gopro.open_gopro.operations.RequestSetCameraName =
    this ?: RequestSetCameraName.defaultInstance

private fun RequestSetCameraName.protoMergeImpl(plus: pbandk.Message?): RequestSetCameraName =
    (plus as? RequestSetCameraName)?.let {
      it.copy(name = plus.name ?: name, unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetCameraName.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestSetCameraName {
  var name: String? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> name = _fieldValue as String
        }
      }

  return RequestSetCameraName(name, unknownFields)
}
