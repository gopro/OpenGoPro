/* network_management.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Wed Sep 24 20:06:50 UTC 2025 */

@file:OptIn(pbandk.PublicForGeneratedCode::class)

package com.gopro.open_gopro.operations

@pbandk.Export
internal sealed class EnumProvisioning(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumProvisioning && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumProvisioning.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object PROVISIONING_UNKNOWN : EnumProvisioning(0, "PROVISIONING_UNKNOWN")

  internal object PROVISIONING_NEVER_STARTED : EnumProvisioning(1, "PROVISIONING_NEVER_STARTED")

  internal object PROVISIONING_STARTED : EnumProvisioning(2, "PROVISIONING_STARTED")

  internal object PROVISIONING_ABORTED_BY_SYSTEM :
      EnumProvisioning(3, "PROVISIONING_ABORTED_BY_SYSTEM")

  internal object PROVISIONING_CANCELLED_BY_USER :
      EnumProvisioning(4, "PROVISIONING_CANCELLED_BY_USER")

  internal object PROVISIONING_SUCCESS_NEW_AP : EnumProvisioning(5, "PROVISIONING_SUCCESS_NEW_AP")

  internal object PROVISIONING_SUCCESS_OLD_AP : EnumProvisioning(6, "PROVISIONING_SUCCESS_OLD_AP")

  internal object PROVISIONING_ERROR_FAILED_TO_ASSOCIATE :
      EnumProvisioning(7, "PROVISIONING_ERROR_FAILED_TO_ASSOCIATE")

  internal object PROVISIONING_ERROR_PASSWORD_AUTH :
      EnumProvisioning(8, "PROVISIONING_ERROR_PASSWORD_AUTH")

  internal object PROVISIONING_ERROR_EULA_BLOCKING :
      EnumProvisioning(9, "PROVISIONING_ERROR_EULA_BLOCKING")

  internal object PROVISIONING_ERROR_NO_INTERNET :
      EnumProvisioning(10, "PROVISIONING_ERROR_NO_INTERNET")

  internal object PROVISIONING_ERROR_UNSUPPORTED_TYPE :
      EnumProvisioning(11, "PROVISIONING_ERROR_UNSUPPORTED_TYPE")

  internal class UNRECOGNIZED(value: Int) : EnumProvisioning(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumProvisioning> {
    internal val values: List<com.gopro.open_gopro.operations.EnumProvisioning> by lazy {
      listOf(
          PROVISIONING_UNKNOWN,
          PROVISIONING_NEVER_STARTED,
          PROVISIONING_STARTED,
          PROVISIONING_ABORTED_BY_SYSTEM,
          PROVISIONING_CANCELLED_BY_USER,
          PROVISIONING_SUCCESS_NEW_AP,
          PROVISIONING_SUCCESS_OLD_AP,
          PROVISIONING_ERROR_FAILED_TO_ASSOCIATE,
          PROVISIONING_ERROR_PASSWORD_AUTH,
          PROVISIONING_ERROR_EULA_BLOCKING,
          PROVISIONING_ERROR_NO_INTERNET,
          PROVISIONING_ERROR_UNSUPPORTED_TYPE)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumProvisioning =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumProvisioning =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumProvisioning with name: $name")
  }
}

@pbandk.Export
internal sealed class EnumScanning(override val value: Int, override val name: String? = null) :
    pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumScanning && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumScanning.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object SCANNING_UNKNOWN : EnumScanning(0, "SCANNING_UNKNOWN")

  internal object SCANNING_NEVER_STARTED : EnumScanning(1, "SCANNING_NEVER_STARTED")

  internal object SCANNING_STARTED : EnumScanning(2, "SCANNING_STARTED")

  internal object SCANNING_ABORTED_BY_SYSTEM : EnumScanning(3, "SCANNING_ABORTED_BY_SYSTEM")

  internal object SCANNING_CANCELLED_BY_USER : EnumScanning(4, "SCANNING_CANCELLED_BY_USER")

  internal object SCANNING_SUCCESS : EnumScanning(5, "SCANNING_SUCCESS")

  internal class UNRECOGNIZED(value: Int) : EnumScanning(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumScanning> {
    internal val values: List<com.gopro.open_gopro.operations.EnumScanning> by lazy {
      listOf(
          SCANNING_UNKNOWN,
          SCANNING_NEVER_STARTED,
          SCANNING_STARTED,
          SCANNING_ABORTED_BY_SYSTEM,
          SCANNING_CANCELLED_BY_USER,
          SCANNING_SUCCESS)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumScanning =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumScanning =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumScanning with name: $name")
  }
}

@pbandk.Export
internal sealed class EnumScanEntryFlags(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumScanEntryFlags && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumScanEntryFlags.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object SCAN_FLAG_OPEN : EnumScanEntryFlags(0, "SCAN_FLAG_OPEN")

  internal object SCAN_FLAG_AUTHENTICATED : EnumScanEntryFlags(1, "SCAN_FLAG_AUTHENTICATED")

  internal object SCAN_FLAG_CONFIGURED : EnumScanEntryFlags(2, "SCAN_FLAG_CONFIGURED")

  internal object SCAN_FLAG_BEST_SSID : EnumScanEntryFlags(4, "SCAN_FLAG_BEST_SSID")

  internal object SCAN_FLAG_ASSOCIATED : EnumScanEntryFlags(8, "SCAN_FLAG_ASSOCIATED")

  internal object SCAN_FLAG_UNSUPPORTED_TYPE : EnumScanEntryFlags(16, "SCAN_FLAG_UNSUPPORTED_TYPE")

  internal class UNRECOGNIZED(value: Int) : EnumScanEntryFlags(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumScanEntryFlags> {
    internal val values: List<com.gopro.open_gopro.operations.EnumScanEntryFlags> by lazy {
      listOf(
          SCAN_FLAG_OPEN,
          SCAN_FLAG_AUTHENTICATED,
          SCAN_FLAG_CONFIGURED,
          SCAN_FLAG_BEST_SSID,
          SCAN_FLAG_ASSOCIATED,
          SCAN_FLAG_UNSUPPORTED_TYPE)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumScanEntryFlags =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumScanEntryFlags =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumScanEntryFlags with name: $name")
  }
}

@pbandk.Export
internal sealed class EnumPairingFinishState(
    override val value: Int,
    override val name: String? = null
) : pbandk.Message.Enum {
  override fun equals(other: kotlin.Any?): Boolean =
      other is com.gopro.open_gopro.operations.EnumPairingFinishState && other.value == value

  override fun hashCode(): Int = value.hashCode()

  override fun toString(): String = "EnumPairingFinishState.${name ?: "UNRECOGNIZED"}(value=$value)"

  internal object SUCCESS : EnumPairingFinishState(0, "SUCCESS")

  internal object FAILED : EnumPairingFinishState(1, "FAILED")

  internal class UNRECOGNIZED(value: Int) : EnumPairingFinishState(value)

  internal companion object :
      pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumPairingFinishState> {
    internal val values: List<com.gopro.open_gopro.operations.EnumPairingFinishState> by lazy {
      listOf(SUCCESS, FAILED)
    }

    override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumPairingFinishState =
        values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)

    override fun fromName(name: String): com.gopro.open_gopro.operations.EnumPairingFinishState =
        values.firstOrNull { it.name == name }
            ?: throw IllegalArgumentException("No EnumPairingFinishState with name: $name")
  }
}

@pbandk.Export
internal data class NotifProvisioningState(
    val provisioningState: com.gopro.open_gopro.operations.EnumProvisioning,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.NotifProvisioningState = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifProvisioningState>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.NotifProvisioningState> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.NotifProvisioningState =
        com.gopro.open_gopro.operations.NotifProvisioningState.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifProvisioningState> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifProvisioningState",
            messageClass = com.gopro.open_gopro.operations.NotifProvisioningState::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "provisioning_state",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumProvisioning.Companion,
                                  hasPresence = true),
                          jsonName = "provisioningState",
                          value =
                              com.gopro.open_gopro.operations.NotifProvisioningState::
                                  provisioningState))
                })
  }
}

@pbandk.Export
internal data class NotifStartScanning(
    val scanningState: com.gopro.open_gopro.operations.EnumScanning,
    val scanId: Int? = null,
    val totalEntries: Int? = null,
    val totalConfiguredSsid: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.NotifStartScanning = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifStartScanning>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.NotifStartScanning> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.NotifStartScanning =
        com.gopro.open_gopro.operations.NotifStartScanning.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.NotifStartScanning> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.NotifStartScanning",
            messageClass = com.gopro.open_gopro.operations.NotifStartScanning::class,
            messageCompanion = this,
            fields =
                buildList(4) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "scanning_state",
                          number = 1,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumScanning.Companion,
                                  hasPresence = true),
                          jsonName = "scanningState",
                          value =
                              com.gopro.open_gopro.operations.NotifStartScanning::scanningState))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "scan_id",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "scanId",
                          value = com.gopro.open_gopro.operations.NotifStartScanning::scanId))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "total_entries",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "totalEntries",
                          value = com.gopro.open_gopro.operations.NotifStartScanning::totalEntries))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "total_configured_ssid",
                          number = 4,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "totalConfiguredSsid",
                          value =
                              com.gopro.open_gopro.operations.NotifStartScanning::
                                  totalConfiguredSsid))
                })
  }
}

@pbandk.Export
internal data class RequestConnect(
    val ssid: String,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestConnect = protoMergeImpl(other)

  override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestConnect>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestConnect> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestConnect =
        com.gopro.open_gopro.operations.RequestConnect.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestConnect> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestConnect",
            messageClass = com.gopro.open_gopro.operations.RequestConnect::class,
            messageCompanion = this,
            fields =
                buildList(1) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "ssid",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "ssid",
                          value = com.gopro.open_gopro.operations.RequestConnect::ssid))
                })
  }
}

@pbandk.Export
internal data class RequestConnectNew(
    val ssid: String,
    val password: String,
    val staticIp: pbandk.ByteArr? = null,
    val gateway: pbandk.ByteArr? = null,
    val subnet: pbandk.ByteArr? = null,
    val dnsPrimary: pbandk.ByteArr? = null,
    val dnsSecondary: pbandk.ByteArr? = null,
    val bypassEulaCheck: Boolean? = null,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestConnectNew = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestConnectNew>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestConnectNew> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestConnectNew =
        com.gopro.open_gopro.operations.RequestConnectNew.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestConnectNew> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestConnectNew",
            messageClass = com.gopro.open_gopro.operations.RequestConnectNew::class,
            messageCompanion = this,
            fields =
                buildList(8) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "ssid",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "ssid",
                          value = com.gopro.open_gopro.operations.RequestConnectNew::ssid))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "password",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "password",
                          value = com.gopro.open_gopro.operations.RequestConnectNew::password))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "static_ip",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                          jsonName = "staticIp",
                          value = com.gopro.open_gopro.operations.RequestConnectNew::staticIp))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "gateway",
                          number = 4,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                          jsonName = "gateway",
                          value = com.gopro.open_gopro.operations.RequestConnectNew::gateway))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "subnet",
                          number = 5,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                          jsonName = "subnet",
                          value = com.gopro.open_gopro.operations.RequestConnectNew::subnet))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "dns_primary",
                          number = 6,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                          jsonName = "dnsPrimary",
                          value = com.gopro.open_gopro.operations.RequestConnectNew::dnsPrimary))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "dns_secondary",
                          number = 7,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bytes(hasPresence = true),
                          jsonName = "dnsSecondary",
                          value = com.gopro.open_gopro.operations.RequestConnectNew::dnsSecondary))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "bypass_eula_check",
                          number = 10,
                          type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                          jsonName = "bypassEulaCheck",
                          value =
                              com.gopro.open_gopro.operations.RequestConnectNew::bypassEulaCheck))
                })
  }
}

@pbandk.Export
internal data class RequestGetApEntries(
    val startIndex: Int,
    val maxEntries: Int,
    val scanId: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestGetApEntries = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetApEntries>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestGetApEntries> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestGetApEntries =
        com.gopro.open_gopro.operations.RequestGetApEntries.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestGetApEntries> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestGetApEntries",
            messageClass = com.gopro.open_gopro.operations.RequestGetApEntries::class,
            messageCompanion = this,
            fields =
                buildList(3) {
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "start_index",
                          number = 1,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "startIndex",
                          value = com.gopro.open_gopro.operations.RequestGetApEntries::startIndex))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "max_entries",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "maxEntries",
                          value = com.gopro.open_gopro.operations.RequestGetApEntries::maxEntries))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "scan_id",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "scanId",
                          value = com.gopro.open_gopro.operations.RequestGetApEntries::scanId))
                })
  }
}

@pbandk.Export
internal data class RequestReleaseNetwork(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestReleaseNetwork = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestReleaseNetwork>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestReleaseNetwork> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestReleaseNetwork by lazy {
      com.gopro.open_gopro.operations.RequestReleaseNetwork()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestReleaseNetwork =
        com.gopro.open_gopro.operations.RequestReleaseNetwork.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestReleaseNetwork> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestReleaseNetwork",
            messageClass = com.gopro.open_gopro.operations.RequestReleaseNetwork::class,
            messageCompanion = this,
            fields = buildList(0) {})
  }
}

@pbandk.Export
internal data class RequestStartScan(
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestStartScan = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestStartScan>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestStartScan> {
    internal val defaultInstance: com.gopro.open_gopro.operations.RequestStartScan by lazy {
      com.gopro.open_gopro.operations.RequestStartScan()
    }

    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestStartScan =
        com.gopro.open_gopro.operations.RequestStartScan.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestStartScan> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestStartScan",
            messageClass = com.gopro.open_gopro.operations.RequestStartScan::class,
            messageCompanion = this,
            fields = buildList(0) {})
  }
}

@pbandk.Export
internal data class ResponseConnect(
    val result: com.gopro.open_gopro.operations.EnumResultGeneric,
    val provisioningState: com.gopro.open_gopro.operations.EnumProvisioning,
    val timeoutSeconds: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ResponseConnect = protoMergeImpl(other)

  override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseConnect>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseConnect> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ResponseConnect =
        com.gopro.open_gopro.operations.ResponseConnect.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseConnect> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseConnect",
            messageClass = com.gopro.open_gopro.operations.ResponseConnect::class,
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
                          value = com.gopro.open_gopro.operations.ResponseConnect::result))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "provisioning_state",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumProvisioning.Companion,
                                  hasPresence = true),
                          jsonName = "provisioningState",
                          value =
                              com.gopro.open_gopro.operations.ResponseConnect::provisioningState))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "timeout_seconds",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "timeoutSeconds",
                          value = com.gopro.open_gopro.operations.ResponseConnect::timeoutSeconds))
                })
  }
}

@pbandk.Export
internal data class ResponseConnectNew(
    val result: com.gopro.open_gopro.operations.EnumResultGeneric,
    val provisioningState: com.gopro.open_gopro.operations.EnumProvisioning,
    val timeoutSeconds: Int,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ResponseConnectNew = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseConnectNew>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseConnectNew> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ResponseConnectNew =
        com.gopro.open_gopro.operations.ResponseConnectNew.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseConnectNew> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseConnectNew",
            messageClass = com.gopro.open_gopro.operations.ResponseConnectNew::class,
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
                          value = com.gopro.open_gopro.operations.ResponseConnectNew::result))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "provisioning_state",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumProvisioning.Companion,
                                  hasPresence = true),
                          jsonName = "provisioningState",
                          value =
                              com.gopro.open_gopro.operations.ResponseConnectNew::
                                  provisioningState))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "timeout_seconds",
                          number = 3,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "timeoutSeconds",
                          value =
                              com.gopro.open_gopro.operations.ResponseConnectNew::timeoutSeconds))
                })
  }
}

@pbandk.Export
internal data class ResponseGetApEntries(
    val result: com.gopro.open_gopro.operations.EnumResultGeneric,
    val scanId: Int,
    val entries: List<com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ResponseGetApEntries = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseGetApEntries>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseGetApEntries> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ResponseGetApEntries =
        com.gopro.open_gopro.operations.ResponseGetApEntries.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseGetApEntries> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseGetApEntries",
            messageClass = com.gopro.open_gopro.operations.ResponseGetApEntries::class,
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
                          value = com.gopro.open_gopro.operations.ResponseGetApEntries::result))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "scan_id",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                          jsonName = "scanId",
                          value = com.gopro.open_gopro.operations.ResponseGetApEntries::scanId))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "entries",
                          number = 3,
                          type =
                              pbandk.FieldDescriptor.Type.Repeated<
                                  com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry>(
                                  valueType =
                                      pbandk.FieldDescriptor.Type.Message(
                                          messageCompanion =
                                              com.gopro.open_gopro.operations.ResponseGetApEntries
                                                  .ScanEntry
                                                  .Companion)),
                          jsonName = "entries",
                          value = com.gopro.open_gopro.operations.ResponseGetApEntries::entries))
                })
  }

  internal data class ScanEntry(
      val ssid: String,
      val signalStrengthBars: Int,
      val signalFrequencyMhz: Int,
      val scanEntryFlags: Int,
      override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
  ) : pbandk.Message {
    override operator fun plus(
        other: pbandk.Message?
    ): com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry = protoMergeImpl(other)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry>
      get() = Companion.descriptor

    override val protoSize: Int by lazy { super.protoSize }

    internal companion object :
        pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry> {
      override fun decodeWith(
          u: pbandk.MessageDecoder
      ): com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry =
          com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry.decodeWithImpl(u)

      override val descriptor:
          pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry> =
          pbandk.MessageDescriptor(
              fullName = "open_gopro.ResponseGetApEntries.ScanEntry",
              messageClass = com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry::class,
              messageCompanion = this,
              fields =
                  buildList(4) {
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "ssid",
                            number = 1,
                            type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                            jsonName = "ssid",
                            value =
                                com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry::
                                    ssid))
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "signal_strength_bars",
                            number = 2,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "signalStrengthBars",
                            value =
                                com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry::
                                    signalStrengthBars))
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "signal_frequency_mhz",
                            number = 4,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "signalFrequencyMhz",
                            value =
                                com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry::
                                    signalFrequencyMhz))
                    add(
                        pbandk.FieldDescriptor(
                            messageDescriptor = this@Companion::descriptor,
                            name = "scan_entry_flags",
                            number = 5,
                            type = pbandk.FieldDescriptor.Type.Primitive.Int32(hasPresence = true),
                            jsonName = "scanEntryFlags",
                            value =
                                com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry::
                                    scanEntryFlags))
                  })
    }
  }
}

@pbandk.Export
internal data class ResponseStartScanning(
    val result: com.gopro.open_gopro.operations.EnumResultGeneric,
    val scanningState: com.gopro.open_gopro.operations.EnumScanning,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.ResponseStartScanning = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseStartScanning>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.ResponseStartScanning> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.ResponseStartScanning =
        com.gopro.open_gopro.operations.ResponseStartScanning.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.ResponseStartScanning> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.ResponseStartScanning",
            messageClass = com.gopro.open_gopro.operations.ResponseStartScanning::class,
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
                          value = com.gopro.open_gopro.operations.ResponseStartScanning::result))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "scanning_state",
                          number = 2,
                          type =
                              pbandk.FieldDescriptor.Type.Enum(
                                  enumCompanion =
                                      com.gopro.open_gopro.operations.EnumScanning.Companion,
                                  hasPresence = true),
                          jsonName = "scanningState",
                          value =
                              com.gopro.open_gopro.operations.ResponseStartScanning::scanningState))
                })
  }
}

@pbandk.Export
internal data class RequestPairingFinish(
    val result: com.gopro.open_gopro.operations.EnumPairingFinishState,
    val phoneName: String,
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
  override operator fun plus(
      other: pbandk.Message?
  ): com.gopro.open_gopro.operations.RequestPairingFinish = protoMergeImpl(other)

  override val descriptor:
      pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestPairingFinish>
    get() = Companion.descriptor

  override val protoSize: Int by lazy { super.protoSize }

  internal companion object :
      pbandk.Message.Companion<com.gopro.open_gopro.operations.RequestPairingFinish> {
    override fun decodeWith(
        u: pbandk.MessageDecoder
    ): com.gopro.open_gopro.operations.RequestPairingFinish =
        com.gopro.open_gopro.operations.RequestPairingFinish.decodeWithImpl(u)

    override val descriptor:
        pbandk.MessageDescriptor<com.gopro.open_gopro.operations.RequestPairingFinish> =
        pbandk.MessageDescriptor(
            fullName = "open_gopro.RequestPairingFinish",
            messageClass = com.gopro.open_gopro.operations.RequestPairingFinish::class,
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
                                      com.gopro.open_gopro.operations.EnumPairingFinishState
                                          .Companion,
                                  hasPresence = true),
                          jsonName = "result",
                          value = com.gopro.open_gopro.operations.RequestPairingFinish::result))
                  add(
                      pbandk.FieldDescriptor(
                          messageDescriptor = this@Companion::descriptor,
                          name = "phoneName",
                          number = 2,
                          type = pbandk.FieldDescriptor.Type.Primitive.String(hasPresence = true),
                          jsonName = "phoneName",
                          value = com.gopro.open_gopro.operations.RequestPairingFinish::phoneName))
                })
  }
}

private fun NotifProvisioningState.protoMergeImpl(plus: pbandk.Message?): NotifProvisioningState =
    (plus as? NotifProvisioningState)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifProvisioningState.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): NotifProvisioningState {
  var provisioningState: com.gopro.open_gopro.operations.EnumProvisioning? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> provisioningState = _fieldValue as com.gopro.open_gopro.operations.EnumProvisioning
        }
      }

  if (provisioningState == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("provisioning_state")
  }
  return NotifProvisioningState(provisioningState!!, unknownFields)
}

private fun NotifStartScanning.protoMergeImpl(plus: pbandk.Message?): NotifStartScanning =
    (plus as? NotifStartScanning)?.let {
      it.copy(
          scanId = plus.scanId ?: scanId,
          totalEntries = plus.totalEntries ?: totalEntries,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun NotifStartScanning.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): NotifStartScanning {
  var scanningState: com.gopro.open_gopro.operations.EnumScanning? = null
  var scanId: Int? = null
  var totalEntries: Int? = null
  var totalConfiguredSsid: Int? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> scanningState = _fieldValue as com.gopro.open_gopro.operations.EnumScanning
          2 -> scanId = _fieldValue as Int
          3 -> totalEntries = _fieldValue as Int
          4 -> totalConfiguredSsid = _fieldValue as Int
        }
      }

  if (scanningState == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("scanning_state")
  }
  if (totalConfiguredSsid == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("total_configured_ssid")
  }
  return NotifStartScanning(
      scanningState!!, scanId, totalEntries, totalConfiguredSsid!!, unknownFields)
}

private fun RequestConnect.protoMergeImpl(plus: pbandk.Message?): RequestConnect =
    (plus as? RequestConnect)?.let { it.copy(unknownFields = unknownFields + plus.unknownFields) }
        ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestConnect.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestConnect {
  var ssid: String? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> ssid = _fieldValue as String
        }
      }

  if (ssid == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("ssid")
  }
  return RequestConnect(ssid!!, unknownFields)
}

private fun RequestConnectNew.protoMergeImpl(plus: pbandk.Message?): RequestConnectNew =
    (plus as? RequestConnectNew)?.let {
      it.copy(
          staticIp = plus.staticIp ?: staticIp,
          gateway = plus.gateway ?: gateway,
          subnet = plus.subnet ?: subnet,
          dnsPrimary = plus.dnsPrimary ?: dnsPrimary,
          dnsSecondary = plus.dnsSecondary ?: dnsSecondary,
          bypassEulaCheck = plus.bypassEulaCheck ?: bypassEulaCheck,
          unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestConnectNew.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestConnectNew {
  var ssid: String? = null
  var password: String? = null
  var staticIp: pbandk.ByteArr? = null
  var gateway: pbandk.ByteArr? = null
  var subnet: pbandk.ByteArr? = null
  var dnsPrimary: pbandk.ByteArr? = null
  var dnsSecondary: pbandk.ByteArr? = null
  var bypassEulaCheck: Boolean? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> ssid = _fieldValue as String
          2 -> password = _fieldValue as String
          3 -> staticIp = _fieldValue as pbandk.ByteArr
          4 -> gateway = _fieldValue as pbandk.ByteArr
          5 -> subnet = _fieldValue as pbandk.ByteArr
          6 -> dnsPrimary = _fieldValue as pbandk.ByteArr
          7 -> dnsSecondary = _fieldValue as pbandk.ByteArr
          10 -> bypassEulaCheck = _fieldValue as Boolean
        }
      }

  if (ssid == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("ssid")
  }
  if (password == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("password")
  }
  return RequestConnectNew(
      ssid!!,
      password!!,
      staticIp,
      gateway,
      subnet,
      dnsPrimary,
      dnsSecondary,
      bypassEulaCheck,
      unknownFields)
}

private fun RequestGetApEntries.protoMergeImpl(plus: pbandk.Message?): RequestGetApEntries =
    (plus as? RequestGetApEntries)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestGetApEntries.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestGetApEntries {
  var startIndex: Int? = null
  var maxEntries: Int? = null
  var scanId: Int? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> startIndex = _fieldValue as Int
          2 -> maxEntries = _fieldValue as Int
          3 -> scanId = _fieldValue as Int
        }
      }

  if (startIndex == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("start_index")
  }
  if (maxEntries == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("max_entries")
  }
  if (scanId == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("scan_id")
  }
  return RequestGetApEntries(startIndex!!, maxEntries!!, scanId!!, unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestReleaseNetwork")
internal fun RequestReleaseNetwork?.orDefault():
    com.gopro.open_gopro.operations.RequestReleaseNetwork =
    this ?: RequestReleaseNetwork.defaultInstance

private fun RequestReleaseNetwork.protoMergeImpl(plus: pbandk.Message?): RequestReleaseNetwork =
    (plus as? RequestReleaseNetwork)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestReleaseNetwork.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestReleaseNetwork {

  val unknownFields = u.readMessage(this) { _, _ -> }

  return RequestReleaseNetwork(unknownFields)
}

@pbandk.Export
@pbandk.JsName("orDefaultForRequestStartScan")
internal fun RequestStartScan?.orDefault(): com.gopro.open_gopro.operations.RequestStartScan =
    this ?: RequestStartScan.defaultInstance

private fun RequestStartScan.protoMergeImpl(plus: pbandk.Message?): RequestStartScan =
    (plus as? RequestStartScan)?.let { it.copy(unknownFields = unknownFields + plus.unknownFields) }
        ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestStartScan.Companion.decodeWithImpl(u: pbandk.MessageDecoder): RequestStartScan {

  val unknownFields = u.readMessage(this) { _, _ -> }

  return RequestStartScan(unknownFields)
}

private fun ResponseConnect.protoMergeImpl(plus: pbandk.Message?): ResponseConnect =
    (plus as? ResponseConnect)?.let { it.copy(unknownFields = unknownFields + plus.unknownFields) }
        ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseConnect.Companion.decodeWithImpl(u: pbandk.MessageDecoder): ResponseConnect {
  var result: com.gopro.open_gopro.operations.EnumResultGeneric? = null
  var provisioningState: com.gopro.open_gopro.operations.EnumProvisioning? = null
  var timeoutSeconds: Int? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumResultGeneric
          2 -> provisioningState = _fieldValue as com.gopro.open_gopro.operations.EnumProvisioning
          3 -> timeoutSeconds = _fieldValue as Int
        }
      }

  if (result == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
  }
  if (provisioningState == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("provisioning_state")
  }
  if (timeoutSeconds == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("timeout_seconds")
  }
  return ResponseConnect(result!!, provisioningState!!, timeoutSeconds!!, unknownFields)
}

private fun ResponseConnectNew.protoMergeImpl(plus: pbandk.Message?): ResponseConnectNew =
    (plus as? ResponseConnectNew)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseConnectNew.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): ResponseConnectNew {
  var result: com.gopro.open_gopro.operations.EnumResultGeneric? = null
  var provisioningState: com.gopro.open_gopro.operations.EnumProvisioning? = null
  var timeoutSeconds: Int? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumResultGeneric
          2 -> provisioningState = _fieldValue as com.gopro.open_gopro.operations.EnumProvisioning
          3 -> timeoutSeconds = _fieldValue as Int
        }
      }

  if (result == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
  }
  if (provisioningState == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("provisioning_state")
  }
  if (timeoutSeconds == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("timeout_seconds")
  }
  return ResponseConnectNew(result!!, provisioningState!!, timeoutSeconds!!, unknownFields)
}

private fun ResponseGetApEntries.protoMergeImpl(plus: pbandk.Message?): ResponseGetApEntries =
    (plus as? ResponseGetApEntries)?.let {
      it.copy(entries = entries + plus.entries, unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseGetApEntries.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): ResponseGetApEntries {
  var result: com.gopro.open_gopro.operations.EnumResultGeneric? = null
  var scanId: Int? = null
  var entries:
      pbandk.ListWithSize.Builder<com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry>? =
      null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumResultGeneric
          2 -> scanId = _fieldValue as Int
          3 ->
              entries =
                  (entries ?: pbandk.ListWithSize.Builder()).apply {
                    this +=
                        _fieldValue
                            as
                            kotlin.sequences.Sequence<
                                com.gopro.open_gopro.operations.ResponseGetApEntries.ScanEntry>
                  }
        }
      }

  if (result == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
  }
  if (scanId == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("scan_id")
  }
  return ResponseGetApEntries(
      result!!, scanId!!, pbandk.ListWithSize.Builder.fixed(entries), unknownFields)
}

private fun ResponseGetApEntries.ScanEntry.protoMergeImpl(
    plus: pbandk.Message?
): ResponseGetApEntries.ScanEntry =
    (plus as? ResponseGetApEntries.ScanEntry)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseGetApEntries.ScanEntry.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): ResponseGetApEntries.ScanEntry {
  var ssid: String? = null
  var signalStrengthBars: Int? = null
  var signalFrequencyMhz: Int? = null
  var scanEntryFlags: Int? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> ssid = _fieldValue as String
          2 -> signalStrengthBars = _fieldValue as Int
          4 -> signalFrequencyMhz = _fieldValue as Int
          5 -> scanEntryFlags = _fieldValue as Int
        }
      }

  if (ssid == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("ssid")
  }
  if (signalStrengthBars == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("signal_strength_bars")
  }
  if (signalFrequencyMhz == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("signal_frequency_mhz")
  }
  if (scanEntryFlags == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("scan_entry_flags")
  }
  return ResponseGetApEntries.ScanEntry(
      ssid!!, signalStrengthBars!!, signalFrequencyMhz!!, scanEntryFlags!!, unknownFields)
}

private fun ResponseStartScanning.protoMergeImpl(plus: pbandk.Message?): ResponseStartScanning =
    (plus as? ResponseStartScanning)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun ResponseStartScanning.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): ResponseStartScanning {
  var result: com.gopro.open_gopro.operations.EnumResultGeneric? = null
  var scanningState: com.gopro.open_gopro.operations.EnumScanning? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumResultGeneric
          2 -> scanningState = _fieldValue as com.gopro.open_gopro.operations.EnumScanning
        }
      }

  if (result == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
  }
  if (scanningState == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("scanning_state")
  }
  return ResponseStartScanning(result!!, scanningState!!, unknownFields)
}

private fun RequestPairingFinish.protoMergeImpl(plus: pbandk.Message?): RequestPairingFinish =
    (plus as? RequestPairingFinish)?.let {
      it.copy(unknownFields = unknownFields + plus.unknownFields)
    } ?: this

@Suppress("UNCHECKED_CAST")
private fun RequestPairingFinish.Companion.decodeWithImpl(
    u: pbandk.MessageDecoder
): RequestPairingFinish {
  var result: com.gopro.open_gopro.operations.EnumPairingFinishState? = null
  var phoneName: String? = null

  val unknownFields =
      u.readMessage(this) { _fieldNumber, _fieldValue ->
        when (_fieldNumber) {
          1 -> result = _fieldValue as com.gopro.open_gopro.operations.EnumPairingFinishState
          2 -> phoneName = _fieldValue as String
        }
      }

  if (result == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("result")
  }
  if (phoneName == null) {
    throw pbandk.InvalidProtocolBufferException.missingRequiredField("phoneName")
  }
  return RequestPairingFinish(result!!, phoneName!!, unknownFields)
}
