/* request_get_preset_status.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal sealed class EnumRegisterPresetStatus(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumRegisterPresetStatus && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String =
      "EnumRegisterPresetStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object REGISTER_PRESET_STATUS_PRESET :
      EnumRegisterPresetStatus(1, "REGISTER_PRESET_STATUS_PRESET")

  internal object REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY :
      EnumRegisterPresetStatus(2, "REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY")

  internal class UNRECOGNIZED(value: Int) : EnumRegisterPresetStatus(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumRegisterPresetStatus> {
    internal val values: List<com.gopro.open_gopro.operations.EnumRegisterPresetStatus> by lazy {
      listOf(REGISTER_PRESET_STATUS_PRESET, REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumRegisterPresetStatus =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumRegisterPresetStatus =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumRegisterPresetStatus with name: $name")
  }
}

@pbandk.Export
internal data class RequestGetPresetStatus(
    val registerPresetStatus: List<com.gopro.open_gopro.operations.EnumRegisterPresetStatus> =
        emptyList(),
    val unregisterPresetStatus: List<com.gopro.open_gopro.operations.EnumRegisterPresetStatus> =
        emptyList(),
    val useConstantSettingIds: Boolean? = null,
    val includeHidden: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestGetPresetStatus = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetPresetStatus>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestGetPresetStatus> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestGetPresetStatus by lazy {
      com.gopro.open_gopro.operations.RequestGetPresetStatus()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestGetPresetStatus =
        com.gopro.open_gopro.operations.RequestGetPresetStatus.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetPresetStatus> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetPresetStatus",
            messageClass = com.gopro.open_gopro.operations.RequestGetPresetStatus::class,
            messageCompanion = this,
            fields =
                buildList(4) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "register_preset_status",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.EnumRegisterPresetStatus>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Enum(
                                          enumCompanion =
                                              com.gopro.open_gopro.operations
                                                  .EnumRegisterPresetStatus
                                                  .Companion)),
                          jsonName = "registerPresetStatus",
                          value =
                              com.gopro.open_gopro.operations.RequestGetPresetStatus::
                                  registerPresetStatus))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "unregister_preset_status",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.EnumRegisterPresetStatus>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Enum(
                                          enumCompanion =
                                              com.gopro.open_gopro.operations
                                                  .EnumRegisterPresetStatus
                                                  .Companion)),
                          jsonName = "unregisterPresetStatus",
                          value =
                              com.gopro.open_gopro.operations.RequestGetPresetStatus::
                                  unregisterPresetStatus))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "use_constant_setting_ids",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "useConstantSettingIds",
                          value =
                              com.gopro.open_gopro.operations.RequestGetPresetStatus::
                                  useConstantSettingIds))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "include_hidden",
                          number = 4,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "includeHidden",
                          value =
                              com.gopro.open_gopro.operations.RequestGetPresetStatus::
                                  includeHidden))
                })
  }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetPresetStatus")
internal fun RequestGetPresetStatus?.orDefault():
    com.gopro.open_gopro.operations.RequestGetPresetStatus =
    this ?: RequestGetPresetStatus.defaultInstance

private fun RequestGetPresetStatus.protoMergeImpl(plus: pbandk.Message?): RequestGetPresetStatus =
    (plus as? RequestGetPresetStatus)?.let {
      it.copy(
          registerPresetStatus = registerPresetStatus + plus.registerPresetStatus,
          unregisterPresetStatus = unregisterPresetStatus + plus.unregisterPresetStatus,
          useConstantSettingIds = plus.useConstantSettingIds ?: useConstantSettingIds,
          includeHidden = plus.includeHidden ?: includeHidden,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetPresetStatus.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestGetPresetStatus {
  var registerPresetStatus:
      pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.EnumRegisterPresetStatus>? =
      null
  var unregisterPresetStatus:
      pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.EnumRegisterPresetStatus>? =
      null
  var useConstantSettingIds: Boolean? = null
  var includeHidden: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 ->
              registerPresetStatus =
                  (registerPresetStatus ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<
                                com.gopro.open_gopro.operations.EnumRegisterPresetStatus>
                  }
          2 ->
              unregisterPresetStatus =
                  (unregisterPresetStatus ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<
                                com.gopro.open_gopro.operations.EnumRegisterPresetStatus>
                  }
          3 -> useConstantSettingIds = _fieldValue as Boolean
          4 -> includeHidden = _fieldValue as Boolean
        }
      }

  return RequestGetPresetStatus(
      pbandk.ListWithSize.Builder.fixed(registerPresetStatus),
      pbandk.ListWithSize.Builder.fixed(unregisterPresetStatus),
      useConstantSettingIds,
      includeHidden,
      unknownFields)
}
