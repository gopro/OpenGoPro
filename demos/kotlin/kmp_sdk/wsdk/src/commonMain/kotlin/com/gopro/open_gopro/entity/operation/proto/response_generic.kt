/* response_generic.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal sealed class EnumResultGeneric(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumResultGeneric && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumResultGeneric.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object RESULT_UNKNOWN : EnumResultGeneric(0, "RESULT_UNKNOWN")

  internal object RESULT_SUCCESS : EnumResultGeneric(1, "RESULT_SUCCESS")

  internal object RESULT_ILL_FORMED : EnumResultGeneric(2, "RESULT_ILL_FORMED")

  internal object RESULT_NOT_SUPPORTED : EnumResultGeneric(3, "RESULT_NOT_SUPPORTED")

  internal object RESULT_ARGUMENT_OUT_OF_BOUNDS :
      EnumResultGeneric(4, "RESULT_ARGUMENT_OUT_OF_BOUNDS")

  internal object RESULT_ARGUMENT_INVALID : EnumResultGeneric(5, "RESULT_ARGUMENT_INVALID")

  internal object RESULT_RESOURCE_NOT_AVAILABLE :
      EnumResultGeneric(6, "RESULT_RESOURCE_NOT_AVAILABLE")

  internal class UNRECOGNIZED(value: Int) : EnumResultGeneric(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumResultGeneric> {
    internal val values: List<com.gopro.open_gopro.operations.EnumResultGeneric> by lazy {
      listOf(
          RESULT_UNKNOWN,
          RESULT_SUCCESS,
          RESULT_ILL_FORMED,
          RESULT_NOT_SUPPORTED,
          RESULT_ARGUMENT_OUT_OF_BOUNDS,
          RESULT_ARGUMENT_INVALID,
          RESULT_RESOURCE_NOT_AVAILABLE)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumResultGeneric =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumResultGeneric =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumResultGeneric with name: $name")
  }
}

@pbandk.Export
internal data class ResponseGeneric(
    val result: com.gopro.open_gopro.operations.EnumResultGeneric,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ResponseGeneric = protoMergeImpl(other)

  override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseGeneric>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseGeneric> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ResponseGeneric =
        com.gopro.open_gopro.operations.ResponseGeneric.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseGeneric> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseGeneric",
            messageClass = com.gopro.open_gopro.operations.ResponseGeneric::class,
            messageCompanion = this,
            fields =
                buildList(1) {
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
                          value = com.gopro.open_gopro.operations.ResponseGeneric::result))
                })
  }
}

@pbandk.Export
internal data class Media(
    val folder: String? = null,
    val file: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.operations.Media =
      protoMergeImpl(other)

  override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.Media>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.operations.Media> {
    internal val defaultInstance: com.gopro.open_gopro.operations.Media by lazy {
      com.gopro.open_gopro.operations.Media()
    }

    override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.operations.Media =
        com.gopro.open_gopro.operations.Media.decodeWithImpl(u)

    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.Media> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.Media",
            messageClass = com.gopro.open_gopro.operations.Media::class,
            messageCompanion = this,
            fields =
                buildList(2) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "folder",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "folder",
                          value = com.gopro.open_gopro.operations.Media::folder))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "file",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "file",
                          value = com.gopro.open_gopro.operations.Media::file))
                })
  }
}

private fun ResponseGeneric.protoMergeImpl(plus: pbandk.Message?): ResponseGeneric =
    (plus as? ResponseGeneric)?.let { it.copy(unknownFields = unknownFields + plus.unknownFields) }
        ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseGeneric.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseGeneric {
  var result: com.gopro.open_gopro.operations.EnumResultGeneric? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumResultGeneric
        }
      }

  if (result == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
  }
  return ResponseGeneric(result!!, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForMedia")
internal fun Media?.orDefault(): com.gopro.open_gopro.operations.Media =
    this ?: Media.defaultInstance

private fun Media.protoMergeImpl(plus: pbandk.Message?): Media =
    (plus as? Media)?.let {
      it.copy(
          folder = plus.folder ?: folder,
          file = plus.file ?: file,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun Media.Companion.decodeWithImpl(u: pbandk.MessageDecoder): Media {
  var folder: String? = null
  var file: String? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> folder = _fieldValue as String
          2 -> file = _fieldValue as String
        }
      }

  return Media(folder, file, unknownFields)
}
