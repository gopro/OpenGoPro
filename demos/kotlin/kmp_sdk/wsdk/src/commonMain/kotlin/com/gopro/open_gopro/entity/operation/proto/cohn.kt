/* cohn.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
public sealed class EnumCOHNStatus(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumCOHNStatus && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumCOHNStatus.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object COHN_UNPROVISIONED : EnumCOHNStatus(0, "COHN_UNPROVISIONED")

  internal object COHN_PROVISIONED : EnumCOHNStatus(1, "COHN_PROVISIONED")

  internal class UNRECOGNIZED(value: Int) : EnumCOHNStatus(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumCOHNStatus> {
    internal val values: List<com.gopro.open_gopro.operations.EnumCOHNStatus> by lazy {
      listOf(COHN_UNPROVISIONED, COHN_PROVISIONED)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumCOHNStatus =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumCOHNStatus =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumCOHNStatus with name: $name")
  }
}

@pbandk.Export
public sealed class EnumCOHNNetworkState(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumCOHNNetworkState && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumCOHNNetworkState.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object COHN_STATE_INIT : EnumCOHNNetworkState(0, "COHN_STATE_Init")

  internal object COHN_STATE_ERROR : EnumCOHNNetworkState(1, "COHN_STATE_Error")

  internal object COHN_STATE_EXIT : EnumCOHNNetworkState(2, "COHN_STATE_Exit")

  internal object COHN_STATE_IDLE : EnumCOHNNetworkState(5, "COHN_STATE_Idle")

  internal object COHN_STATE_NETWORK_CONNECTED :
      EnumCOHNNetworkState(27, "COHN_STATE_NetworkConnected")

  internal object COHN_STATE_NETWORK_DISCONNECTED :
      EnumCOHNNetworkState(28, "COHN_STATE_NetworkDisconnected")

  internal object COHN_STATE_CONNECTING_TO_NETWORK :
      EnumCOHNNetworkState(29, "COHN_STATE_ConnectingToNetwork")

  internal object COHN_STATE_INVALID : EnumCOHNNetworkState(30, "COHN_STATE_Invalid")

  internal class UNRECOGNIZED(value: Int) : EnumCOHNNetworkState(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumCOHNNetworkState> {
    internal val values: List<com.gopro.open_gopro.operations.EnumCOHNNetworkState> by lazy {
      listOf(
          COHN_STATE_INIT,
          COHN_STATE_ERROR,
          COHN_STATE_EXIT,
          COHN_STATE_IDLE,
          COHN_STATE_NETWORK_CONNECTED,
          COHN_STATE_NETWORK_DISCONNECTED,
          COHN_STATE_CONNECTING_TO_NETWORK,
          COHN_STATE_INVALID)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumCOHNNetworkState =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumCOHNNetworkState =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumCOHNNetworkState with name: $name")
  }
}

@pbandk.Export
internal data class RequestGetCOHNStatus(
    val registerCohnStatus: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestGetCOHNStatus = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetCOHNStatus>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestGetCOHNStatus> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestGetCOHNStatus by lazy {
      com.gopro.open_gopro.operations.RequestGetCOHNStatus()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestGetCOHNStatus =
        com.gopro.open_gopro.operations.RequestGetCOHNStatus.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetCOHNStatus> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetCOHNStatus",
            messageClass = com.gopro.open_gopro.operations.RequestGetCOHNStatus::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "register_cohn_status",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "registerCohnStatus",
                          value =
                              com.gopro.open_gopro.operations.RequestGetCOHNStatus::
                                  registerCohnStatus))
                })
  }
}

@pbandk.Export
internal data class NotifyCOHNStatus(
    val status: com.gopro.open_gopro.operations.EnumCOHNStatus? = null,
    val state: com.gopro.open_gopro.operations.EnumCOHNNetworkState? = null,
    val username: String? = null,
    val password: String? = null,
    val ipaddress: String? = null,
    val enabled: Boolean? = null,
    val ssid: String? = null,
    val macaddress: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.NotifyCOHNStatus = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifyCOHNStatus>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.NotifyCOHNStatus> {
    internal val defaultInstance: com.gopro.open_gopro.operations.NotifyCOHNStatus by lazy {
      com.gopro.open_gopro.operations.NotifyCOHNStatus()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.NotifyCOHNStatus =
        com.gopro.open_gopro.operations.NotifyCOHNStatus.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifyCOHNStatus> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifyCOHNStatus",
            messageClass = com.gopro.open_gopro.operations.NotifyCOHNStatus::class,
            messageCompanion = this,
            fields =
                buildList(8) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "status",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumCOHNStatus.Companion,
                                  hasPresence = true),
                          jsonName = "status",
                          value = com.gopro.open_gopro.operations.NotifyCOHNStatus::status))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "state",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumCOHNNetworkState
                                          .Companion,
                                  hasPresence = true),
                          jsonName = "state",
                          value = com.gopro.open_gopro.operations.NotifyCOHNStatus::state))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "username",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "username",
                          value = com.gopro.open_gopro.operations.NotifyCOHNStatus::username))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "password",
                          number = 4,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "password",
                          value = com.gopro.open_gopro.operations.NotifyCOHNStatus::password))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "ipaddress",
                          number = 5,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "ipaddress",
                          value = com.gopro.open_gopro.operations.NotifyCOHNStatus::ipaddress))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "enabled",
                          number = 6,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "enabled",
                          value = com.gopro.open_gopro.operations.NotifyCOHNStatus::enabled))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "ssid",
                          number = 7,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "ssid",
                          value = com.gopro.open_gopro.operations.NotifyCOHNStatus::ssid))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "macaddress",
                          number = 8,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "macaddress",
                          value = com.gopro.open_gopro.operations.NotifyCOHNStatus::macaddress))
                })
  }
}

@pbandk.Export
internal data class RequestCreateCOHNCert(
    val override: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestCreateCOHNCert = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestCreateCOHNCert>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestCreateCOHNCert> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestCreateCOHNCert by lazy {
      com.gopro.open_gopro.operations.RequestCreateCOHNCert()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestCreateCOHNCert =
        com.gopro.open_gopro.operations.RequestCreateCOHNCert.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestCreateCOHNCert> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestCreateCOHNCert",
            messageClass = com.gopro.open_gopro.operations.RequestCreateCOHNCert::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "override",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "override",
                          value = com.gopro.open_gopro.operations.RequestCreateCOHNCert::override))
                })
  }
}

@pbandk.Export
internal data class RequestClearCOHNCert(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestClearCOHNCert = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestClearCOHNCert>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestClearCOHNCert> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestClearCOHNCert by lazy {
      com.gopro.open_gopro.operations.RequestClearCOHNCert()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestClearCOHNCert =
        com.gopro.open_gopro.operations.RequestClearCOHNCert.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestClearCOHNCert> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestClearCOHNCert",
            messageClass = com.gopro.open_gopro.operations.RequestClearCOHNCert::class,
            messageCompanion = this,
            fields = buildList(0) {})
  }
}

@pbandk.Export
internal data class RequestCOHNCert(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestCOHNCert = protoMergeImpl(other)

  override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestCOHNCert>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestCOHNCert> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestCOHNCert by lazy {
      com.gopro.open_gopro.operations.RequestCOHNCert()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestCOHNCert =
        com.gopro.open_gopro.operations.RequestCOHNCert.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestCOHNCert> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestCOHNCert",
            messageClass = com.gopro.open_gopro.operations.RequestCOHNCert::class,
            messageCompanion = this,
            fields = buildList(0) {})
  }
}

@pbandk.Export
internal data class ResponseCOHNCert(
    val result: com.gopro.open_gopro.operations.EnumResultGeneric? = null,
    val cert: String? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ResponseCOHNCert = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseCOHNCert>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseCOHNCert> {
    internal val defaultInstance: com.gopro.open_gopro.operations.ResponseCOHNCert by lazy {
      com.gopro.open_gopro.operations.ResponseCOHNCert()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ResponseCOHNCert =
        com.gopro.open_gopro.operations.ResponseCOHNCert.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseCOHNCert> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseCOHNCert",
            messageClass = com.gopro.open_gopro.operations.ResponseCOHNCert::class,
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
                          value = com.gopro.open_gopro.operations.ResponseCOHNCert::result))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "cert",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "cert",
                          value = com.gopro.open_gopro.operations.ResponseCOHNCert::cert))
                })
  }
}

@pbandk.Export
internal data class RequestSetCOHNSetting(
    val cohnActive: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestSetCOHNSetting = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetCOHNSetting>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestSetCOHNSetting> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestSetCOHNSetting by lazy {
      com.gopro.open_gopro.operations.RequestSetCOHNSetting()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestSetCOHNSetting =
        com.gopro.open_gopro.operations.RequestSetCOHNSetting.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestSetCOHNSetting> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestSetCOHNSetting",
            messageClass = com.gopro.open_gopro.operations.RequestSetCOHNSetting::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "cohn_active",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "cohnActive",
                          value =
                              com.gopro.open_gopro.operations.RequestSetCOHNSetting::cohnActive))
                })
  }
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestGetCOHNStatus")
internal fun RequestGetCOHNStatus?.orDefault():
    com.gopro.open_gopro.operations.RequestGetCOHNStatus =
    this ?: RequestGetCOHNStatus.defaultInstance

private fun RequestGetCOHNStatus.protoMergeImpl(plus: pbandk.Message?): RequestGetCOHNStatus =
    (plus as? RequestGetCOHNStatus)?.let {
      it.copy(
          registerCohnStatus = plus.registerCohnStatus ?: registerCohnStatus,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetCOHNStatus.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestGetCOHNStatus {
  var registerCohnStatus: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> registerCohnStatus = _fieldValue as Boolean
        }
      }

  return RequestGetCOHNStatus(registerCohnStatus, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForNotifyCOHNStatus")
internal fun NotifyCOHNStatus?.orDefault(): com.gopro.open_gopro.operations.NotifyCOHNStatus =
    this ?: NotifyCOHNStatus.defaultInstance

private fun NotifyCOHNStatus.protoMergeImpl(plus: pbandk.Message?): NotifyCOHNStatus =
    (plus as? NotifyCOHNStatus)?.let {
      it.copy(
          status = plus.status ?: status,
          state = plus.state ?: state,
          username = plus.username ?: username,
          password = plus.password ?: password,
          ipaddress = plus.ipaddress ?: ipaddress,
          enabled = plus.enabled ?: enabled,
          ssid = plus.ssid ?: ssid,
          macaddress = plus.macaddress ?: macaddress,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifyCOHNStatus.Companion.decodeWithImpl(u: pbandk.MessageDecoder): NotifyCOHNStatus {
  var status: com.gopro.open_gopro.operations.EnumCOHNStatus? = null
  var state: com.gopro.open_gopro.operations.EnumCOHNNetworkState? = null
  var username: String? = null
  var password: String? = null
  var ipaddress: String? = null
  var enabled: Boolean? = null
  var ssid: String? = null
  var macaddress: String? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> status = _fieldValue as com.gopro.open_gopro.operations.EnumCOHNStatus
          2 -> state = _fieldValue as com.gopro.open_gopro.operations.EnumCOHNNetworkState
          3 -> username = _fieldValue as String
          4 -> password = _fieldValue as String
          5 -> ipaddress = _fieldValue as String
          6 -> enabled = _fieldValue as Boolean
          7 -> ssid = _fieldValue as String
          8 -> macaddress = _fieldValue as String
        }
      }

  return NotifyCOHNStatus(
      status, state, username, password, ipaddress, enabled, ssid, macaddress, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestCreateCOHNCert")
internal fun RequestCreateCOHNCert?.orDefault():
    com.gopro.open_gopro.operations.RequestCreateCOHNCert =
    this ?: RequestCreateCOHNCert.defaultInstance

private fun RequestCreateCOHNCert.protoMergeImpl(plus: pbandk.Message?): RequestCreateCOHNCert =
    (plus as? RequestCreateCOHNCert)?.let {
      it.copy(
          override = plus.override ?: override, unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestCreateCOHNCert.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestCreateCOHNCert {
  var override: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> override = _fieldValue as Boolean
        }
      }

  return RequestCreateCOHNCert(override, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestClearCOHNCert")
internal fun RequestClearCOHNCert?.orDefault():
    com.gopro.open_gopro.operations.RequestClearCOHNCert =
    this ?: RequestClearCOHNCert.defaultInstance

private fun RequestClearCOHNCert.protoMergeImpl(plus: pbandk.Message?): RequestClearCOHNCert =
    (plus as? RequestClearCOHNCert)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestClearCOHNCert.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestClearCOHNCert {

  val unknownFields = u.readMessage(this) { _, _ -> }

  return RequestClearCOHNCert(unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestCOHNCert")
internal fun RequestCOHNCert?.orDefault(): com.gopro.open_gopro.operations.RequestCOHNCert =
    this ?: RequestCOHNCert.defaultInstance

private fun RequestCOHNCert.protoMergeImpl(plus: pbandk.Message?): RequestCOHNCert =
    (plus as? RequestCOHNCert)?.let { it.copy(unknownFields = unknownFields + plus.unknownFields) }
        ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestCOHNCert.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestCOHNCert {

  val unknownFields = u.readMessage(this) { _, _ -> }

  return RequestCOHNCert(unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForResponseCOHNCert")
internal fun ResponseCOHNCert?.orDefault(): com.gopro.open_gopro.operations.ResponseCOHNCert =
    this ?: ResponseCOHNCert.defaultInstance

private fun ResponseCOHNCert.protoMergeImpl(plus: pbandk.Message?): ResponseCOHNCert =
    (plus as? ResponseCOHNCert)?.let {
      it.copy(
          result = plus.result ?: result,
          cert = plus.cert ?: cert,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseCOHNCert.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseCOHNCert {
  var result: com.gopro.open_gopro.operations.EnumResultGeneric? = null
  var cert: String? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumResultGeneric
          2 -> cert = _fieldValue as String
        }
      }

  return ResponseCOHNCert(result, cert, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestSetCOHNSetting")
internal fun RequestSetCOHNSetting?.orDefault():
    com.gopro.open_gopro.operations.RequestSetCOHNSetting =
    this ?: RequestSetCOHNSetting.defaultInstance

private fun RequestSetCOHNSetting.protoMergeImpl(plus: pbandk.Message?): RequestSetCOHNSetting =
    (plus as? RequestSetCOHNSetting)?.let {
      it.copy(
          cohnActive = plus.cohnActive ?: cohnActive,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestSetCOHNSetting.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestSetCOHNSetting {
  var cohnActive: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> cohnActive = _fieldValue as Boolean
        }
      }

  return RequestSetCOHNSetting(cohnActive, unknownFields)
}
