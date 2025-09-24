/* set_camera_control_status.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal sealed class EnumCameraControlStatus(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumCameraControlStatus && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String =
      "EnumCameraControlStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object CAMERA_IDLE : EnumCameraControlStatus(0, "CAMERA_IDLE")

  internal object CAMERA_CONTROL : EnumCameraControlStatus(1, "CAMERA_CONTROL")

  internal object CAMERA_EXTERNAL_CONTROL : EnumCameraControlStatus(2, "CAMERA_EXTERNAL_CONTROL")

  internal object CAMERA_COF_SETUP : EnumCameraControlStatus(3, "CAMERA_COF_SETUP")

  internal class UNRECOGNIZED(value: Int) : EnumCameraControlStatus(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumCameraControlStatus> {
    internal val values: List<com.gopro.open_gopro.operations.EnumCameraControlStatus> by lazy {
      listOf(CAMERA_IDLE, CAMERA_CONTROL, CAMERA_EXTERNAL_CONTROL, CAMERA_COF_SETUP)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumCameraControlStatus =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumCameraControlStatus =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumCameraControlStatus with name: $name")
  }
}

@pbandk.Export
internal data class RequestSetCameraControlStatus(
    val cameraControlStatus: com.gopro.open_gopro.operations.EnumCameraControlStatus,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestSetCameraControlStatus = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetCameraControlStatus>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestSetCameraControlStatus> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestSetCameraControlStatus =
        com.gopro.open_gopro.operations.RequestSetCameraControlStatus.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetCameraControlStatus> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetCameraControlStatus",
            messageClass = com.gopro.open_gopro.operations.RequestSetCameraControlStatus::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "camera_control_status",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumCameraControlStatus
                                          .Companion,
                                  hasPresence = true),
                          jsonName = "cameraControlStatus",
                          value =
                              com.gopro.open_gopro.operations.RequestSetCameraControlStatus::
                                  cameraControlStatus))
                })
  }
}

private fun RequestSetCameraControlStatus.protoMergeImpl(
    plus: pbandk.Message?
): RequestSetCameraControlStatus =
    (plus as? RequestSetCameraControlStatus)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetCameraControlStatus.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestSetCameraControlStatus {
  var cameraControlStatus: com.gopro.open_gopro.operations.EnumCameraControlStatus? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 ->
              cameraControlStatus =
                  _fieldValue as com.gopro.open_gopro.operations.EnumCameraControlStatus
        }
      }

  if (cameraControlStatus == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("camera_control_status")
  }
  return RequestSetCameraControlStatus(cameraControlStatus!!, unknownFields)
}
