@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal data class RequestGetCameraCapabilities(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestGetCameraCapabilities = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetCameraCapabilities>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestGetCameraCapabilities> {
    internal val defaultInstance:
        com.gopro.open_gopro.operations.RequestGetCameraCapabilities by lazy {
      com.gopro.open_gopro.operations.RequestGetCameraCapabilities()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestGetCameraCapabilities =
        com.gopro.open_gopro.operations.RequestGetCameraCapabilities.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetCameraCapabilities> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetCameraCapabilities",
            messageClass = com.gopro.open_gopro.operations.RequestGetCameraCapabilities::class,
            messageCompanion = this,
            fields = buildList(0) {})
  }
}

@pbandk.Export
internal data class ResponseGetCameraCapabilities(
    val result: com.gopro.open_gopro.operations.EnumResultGeneric,
    val schemaVersion: String,
    val protocol: com.gopro.open_gopro.operations.ProtocolCapabilities? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ResponseGetCameraCapabilities = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseGetCameraCapabilities>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseGetCameraCapabilities> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ResponseGetCameraCapabilities =
        com.gopro.open_gopro.operations.ResponseGetCameraCapabilities.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseGetCameraCapabilities> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseGetCameraCapabilities",
            messageClass = com.gopro.open_gopro.operations.ResponseGetCameraCapabilities::class,
            messageCompanion = this,
            fields =
                buildList(3) {
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
                              com.gopro.open_gopro.operations.ResponseGetCameraCapabilities::
                                  result))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "schema_version",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "schemaVersion",
                          value =
                              com.gopro.open_gopro.operations.ResponseGetCameraCapabilities::
                                  schemaVersion))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "protocol",
                          number = 3,
                          type =
                              pbandk.FieldDescriptor.Type.Message(
                                  messageCompanion =
                                      com.gopro.open_gopro.operations.ProtocolCapabilities
                                          .Companion),
                          jsonName = "protocol",
                          value =
                              com.gopro.open_gopro.operations.ResponseGetCameraCapabilities::
                                  protocol))
                })
  }
}

@pbandk.Export
internal data class ProtocolCapabilities(
    val supports2byteIds: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ProtocolCapabilities = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ProtocolCapabilities>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ProtocolCapabilities> {
    internal val defaultInstance: com.gopro.open_gopro.operations.ProtocolCapabilities by lazy {
      com.gopro.open_gopro.operations.ProtocolCapabilities()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ProtocolCapabilities =
        com.gopro.open_gopro.operations.ProtocolCapabilities.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ProtocolCapabilities> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ProtocolCapabilities",
            messageClass = com.gopro.open_gopro.operations.ProtocolCapabilities::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "supports_2byte_ids",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "supports2byteIds",
                          value =
                              com.gopro.open_gopro.operations.ProtocolCapabilities::
                                  supports2byteIds))
                })
  }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetCameraCapabilities")
internal fun RequestGetCameraCapabilities?.orDefault():
    com.gopro.open_gopro.operations.RequestGetCameraCapabilities =
    this ?: RequestGetCameraCapabilities.defaultInstance

private fun RequestGetCameraCapabilities.protoMergeImpl(
    plus: pbandk.Message?
): RequestGetCameraCapabilities =
    (plus as? RequestGetCameraCapabilities)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetCameraCapabilities.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestGetCameraCapabilities {

  val unknownFields = u.readMessage(this) { _, _ -> }

  return RequestGetCameraCapabilities(unknownFields)
}

private fun ResponseGetCameraCapabilities.protoMergeImpl(
    plus: pbandk.Message?
): ResponseGetCameraCapabilities =
    (plus as? ResponseGetCameraCapabilities)?.let {
      it.copy(
          protocol = protocol?.plus(plus.protocol) ?: plus.protocol,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseGetCameraCapabilities.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): ResponseGetCameraCapabilities {
  var result: com.gopro.open_gopro.operations.EnumResultGeneric? = null
  var schemaVersion: String? = null
  var protocol: com.gopro.open_gopro.operations.ProtocolCapabilities? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumResultGeneric
          2 -> schemaVersion = _fieldValue as String
          3 -> protocol = _fieldValue as com.gopro.open_gopro.operations.ProtocolCapabilities
        }
      }

  if (result == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
  }
  if (schemaVersion == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("schema_version")
  }
  return ResponseGetCameraCapabilities(result!!, schemaVersion!!, protocol, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForProtocolCapabilities")
internal fun ProtocolCapabilities?.orDefault():
    com.gopro.open_gopro.operations.ProtocolCapabilities =
    this ?: ProtocolCapabilities.defaultInstance

private fun ProtocolCapabilities.protoMergeImpl(plus: pbandk.Message?): ProtocolCapabilities =
    (plus as? ProtocolCapabilities)?.let {
      it.copy(
          supports2byteIds = plus.supports2byteIds ?: supports2byteIds,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun ProtocolCapabilities.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): ProtocolCapabilities {
  var supports2byteIds: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> supports2byteIds = _fieldValue as Boolean
        }
      }

  return ProtocolCapabilities(supports2byteIds, unknownFields)
}
