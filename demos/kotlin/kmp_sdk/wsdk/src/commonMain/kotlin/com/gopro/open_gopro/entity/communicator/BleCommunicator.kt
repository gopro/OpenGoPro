/* BleCommunicator.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.entity.communicator

internal enum class CommandId(val value: UByte) {
  SET_SHUTTER(0x01U),
  SLEEP(0x05U),
  SET_LOCAL_DATE_TIME(0x0DU),
  GET_LOCAL_DATE_TIME(0x0EU),
  REBOOT(0x11U),
  SET_DATE_TIME(0x0FU),
  GET_DATE_TIME(0x10U),
  SET_AP_MODE(0x17U),
  GET_HARDWARE_INFO(0x3CU),
  LOAD_PRESET_GROUP(0x3EU),
  LOAD_PRESET(0x40U),
  HILGIHT_MOMENT(0x18U),
  SET_THIRD_PARTY(0x50U),
  GET_OGP_VERSION(0x51U),
  KEEP_ALIVE(0x5BU);

  companion object {
    fun fromUByte(value: UByte) = entries.firstOrNull { it.value == value }
  }
}

internal enum class QueryId(val value: UByte) {
  GET_SETTING_VALUES(0X12U),
  GET_STATUS_VALUES(0X13U),
  GET_SETTING_CAPABILITIES(0X32U),
  REGISTER_SETTING_VALUE_UPDATES(0X52U),
  REGISTER_STATUS_VALUE_UPDATES(0X53U),
  REGISTER_SETTING_CAPABILITY_UPDATES(0X62U),
  UNREGISTER_SETTING_VALUE_UPDATES(0X72U),
  UNREGISTER_STATUS_VALUE_UPDATES(0X73U),
  UNREGISTER_SETTING_CAPABILITY_UPDATES(0X82U),
  ASYNC_SETTING_VALUE_NOTIFICATION(0X92U),
  ASYNC_STATUS_VALUE_NOTIFICATION(0X93U),
  ASYNC_SETTING_CAPABILITY_NOTIFICATION(0XA2U);

  companion object {
    fun fromUByte(value: UByte) = entries.first { it.value == value }
  }
}

internal enum class ActionId(val value: UByte) {
  REQUEST_PAIRING_STATE(0x01U),
  SCAN_WIFI_NETWORKS(0x02U),
  GET_AP_ENTRIES(0x03U),
  REQUEST_WIFI_CONNECT(0x04U),
  REQUEST_WIFI_CONNECT_NEW(0x05U),
  NOTIF_START_SCAN(0x0BU),
  NOTIF_PROVIS_STATE(0x0CU),
  REQUEST_PRESET_UPDATE_CUSTOM(0x64U),
  SET_CAMERA_CONTROL(0x69U),
  SET_TURBO_MODE(0x6BU),
  GET_PRESET_STATUS(0x72U),
  GET_LIVESTREAM_STATUS(0x74U),
  RELEASE_NETWORK(0x78U),
  SET_LIVESTREAM_MODE(0x79U),
  REQUEST_PAIRING_STATE_RSP(0x81U),
  SCAN_WIFI_NETWORKS_RSP(0x82U),
  GET_AP_ENTRIES_RSP(0x83U),
  REQUEST_WIFI_CONNECT_RSP(0x84U),
  REQUEST_WIFI_CONNECT_NEW_RSP(0x85U),
  REQUEST_COHN_SETTING(0x65U),
  REQUEST_CLEAR_COHN_CERT(0x66U),
  REQUEST_CREATE_COHN_CERT(0x67U),
  REQUEST_GET_LAST_MEDIA(0x6DU),
  REQUEST_GET_COHN_CERT(0x6EU),
  REQUEST_GET_COHN_STATUS(0x6FU),
  RESPONSE_PRESET_UPDATE_CUSTOM(0xE4U),
  RESPONSE_COHN_SETTING(0xE5U),
  RESPONSE_CLEAR_COHN_CERT(0xE6U),
  RESPONSE_CREATE_COHN_CERT(0xE7U),
  SET_CAMERA_CONTROL_RSP(0xE9U),
  SET_TURBO_MODE_RSP(0xEBU),
  RESPONSE_GET_LAST_MEDIA(0xEDU),
  RESPONSE_GET_COHN_CERT(0xEEU),
  RESPONSE_GET_COHN_STATUS(0xEFU),
  GET_PRESET_STATUS_RSP(0xF2U),
  PRESET_MODIFIED_NOTIFICATION(0xF3U),
  LIVESTREAM_STATUS_RSP(0xF4U),
  LIVESTREAM_STATUS_NOTIF(0xF5U),
  RELEASE_NETWORK_RSP(0xF8U),
  SET_LIVESTREAM_MODE_RSP(0xF9U),
  INTERNAL_FF(0xFFU);

  companion object {
    fun fromUByte(value: UByte) = entries.firstOrNull { it.value == value }
  }
}

internal enum class FeatureId(val value: UByte) {
  NETWORK_MANAGEMENT(0x02U),
  WIRELESS_MANAGEMENT(0x03U),
  COMMAND(0xF1U),
  SETTING(0xF3U),
  QUERY(0xF5U);

  companion object {
    fun fromUByte(value: UByte) = entries.firstOrNull { it.value == value }
  }
}

// TODO should we dynamically create this from operations? It's a pretty nasty foot gun currently
internal val responseProtobufIds: Set<Pair<FeatureId, ActionId>> =
    setOf(
        FeatureId.COMMAND to ActionId.SET_CAMERA_CONTROL_RSP,
        FeatureId.COMMAND to ActionId.SET_LIVESTREAM_MODE_RSP,
        FeatureId.COMMAND to ActionId.RESPONSE_PRESET_UPDATE_CUSTOM,
        FeatureId.COMMAND to ActionId.RESPONSE_CLEAR_COHN_CERT,
        FeatureId.COMMAND to ActionId.RESPONSE_CREATE_COHN_CERT,
        FeatureId.COMMAND to ActionId.RESPONSE_COHN_SETTING,
        FeatureId.NETWORK_MANAGEMENT to ActionId.SCAN_WIFI_NETWORKS_RSP,
        FeatureId.NETWORK_MANAGEMENT to ActionId.NOTIF_START_SCAN,
        FeatureId.NETWORK_MANAGEMENT to ActionId.GET_AP_ENTRIES_RSP,
        FeatureId.NETWORK_MANAGEMENT to ActionId.REQUEST_WIFI_CONNECT_NEW_RSP,
        FeatureId.NETWORK_MANAGEMENT to ActionId.REQUEST_WIFI_CONNECT_RSP,
        FeatureId.NETWORK_MANAGEMENT to ActionId.NOTIF_PROVIS_STATE,
        FeatureId.WIRELESS_MANAGEMENT to ActionId.REQUEST_PAIRING_STATE_RSP,
        FeatureId.QUERY to ActionId.LIVESTREAM_STATUS_RSP,
        FeatureId.QUERY to ActionId.LIVESTREAM_STATUS_NOTIF,
        FeatureId.QUERY to ActionId.GET_PRESET_STATUS_RSP,
        FeatureId.QUERY to ActionId.PRESET_MODIFIED_NOTIFICATION,
        FeatureId.QUERY to ActionId.RESPONSE_GET_COHN_STATUS,
        FeatureId.QUERY to ActionId.RESPONSE_GET_COHN_CERT,
    )

internal enum class GpStatus(val value: UByte) {
  SUCCESS(0U);

  companion object {
    fun fromUByte(value: UByte) = entries.firstOrNull() { it.value == value }

    fun isSuccess(value: UByte) = fromUByte(value) == SUCCESS
  }
}
