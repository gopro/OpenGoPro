/* bleByteData.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

@file:OptIn(ExperimentalUnsignedTypes::class)

package vectors

import com.gopro.open_gopro.entity.communicator.ActionId
import com.gopro.open_gopro.entity.communicator.CommandId
import com.gopro.open_gopro.entity.communicator.FeatureId
import com.gopro.open_gopro.entity.communicator.GpStatus
import com.gopro.open_gopro.operations.EnumFlatMode
import com.gopro.open_gopro.operations.EnumLens
import com.gopro.open_gopro.operations.EnumLiveStreamError
import com.gopro.open_gopro.operations.EnumLiveStreamStatus
import com.gopro.open_gopro.operations.EnumPresetGroup
import com.gopro.open_gopro.operations.EnumPresetGroupIcon
import com.gopro.open_gopro.operations.EnumPresetIcon
import com.gopro.open_gopro.operations.EnumPresetTitle
import com.gopro.open_gopro.operations.EnumProvisioning
import com.gopro.open_gopro.operations.EnumRegisterLiveStreamStatus
import com.gopro.open_gopro.operations.EnumRegisterPresetStatus
import com.gopro.open_gopro.operations.EnumResultGeneric
import com.gopro.open_gopro.operations.EnumScanning
import com.gopro.open_gopro.operations.EnumWindowSize
import com.gopro.open_gopro.operations.NotifProvisioningState
import com.gopro.open_gopro.operations.NotifStartScanning
import com.gopro.open_gopro.operations.NotifyLiveStreamStatus
import com.gopro.open_gopro.operations.NotifyPresetStatus
import com.gopro.open_gopro.operations.Preset
import com.gopro.open_gopro.operations.PresetGroup
import com.gopro.open_gopro.operations.PresetSetting
import com.gopro.open_gopro.operations.RequestGetLiveStreamStatus
import com.gopro.open_gopro.operations.RequestGetPresetStatus
import com.gopro.open_gopro.operations.ResponseConnectNew
import com.gopro.open_gopro.operations.ResponseGeneric
import com.gopro.open_gopro.operations.ResponseGetApEntries
import com.gopro.open_gopro.operations.ResponseStartScanning
import com.gopro.open_gopro.util.extensions.encodeToUByteArray
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.Month
import kotlinx.datetime.UtcOffset
import pbandk.encodeToByteArray

val utcOffsetVector = UtcOffset(hours = -2)
val utcOffsetBytes = ubyteArrayOf(0xFFU, 0x88U)
val localDateTimeVector =
    LocalDateTime(
        hour = 3,
        minute = 4,
        second = 5,
        year = 2023,
        month = Month(1),
        dayOfMonth = 31,
    )
val localDateTimeBytes = ubyteArrayOf(0x07U, 0xe7U, 0x01U, 0x1fU, 0x03U, 0x04U, 0x05U)

val setShutterRequestPayload = ubyteArrayOf(0x01U, 0x01U, 0x01U)
val setShutterRequestMessage = ubyteArrayOf(0x20U, 0x03U, 0x01U, 0x01U, 0x01U)
val setShutterResponsePayload = ubyteArrayOf(1U, 0U)
val setShutterResponseMessage = ubyteArrayOf(2U, 1U, 0U)
val keepAliveResponsePayload = ubyteArrayOf(0x5BU, 0x00U)
val dateTimeResponsePayload =
    ubyteArrayOf(
        // command ID
        0x10U,
        // status
        0x00U,
        // param size
        0x0AU) + localDateTimeBytes + utcOffsetBytes + ubyteArrayOf(0x01U)
val setSettingRequestPayload = ubyteArrayOf(2U, 1U, 9U)
val setSettingResponsePayload = ubyteArrayOf(2U, 0U)
val setSettingResponseMessage = ubyteArrayOf(2U, 2U, 0U)
val setSettingResponseMessageFailure = ubyteArrayOf(2U, 2U, 2U)
val setSettingsRequestPayload = ubyteArrayOf(32U, 3U, 2U, 1U, 9U)
val getSettingResponsePayload = ubyteArrayOf(0x12U, 0x00U, 0x02U, 0x01U, 0x09U)
val getSettingResponseMessage = ubyteArrayOf(0x05U, 0x12U, 0x00U, 0x02U, 0x01U, 0x09U)
val getSettingResponseMessage2 = ubyteArrayOf(0x05U, 0x12U, 0x00U, 0x02U, 0x01U, 12U)
val getSettingResponseMessage3 = ubyteArrayOf(0x05U, 0x12U, 0x00U, 0x02U, 0x01U, 18U)
val getScheduledCaptureResponseMessage =
    ubyteArrayOf(0x08U, 0x12U, 0x00U, 0xA8U, 0x04U, 0x00U, 0x00U, 0x0CU, 0x8BU)
val registerSettingValueResponseMessage = ubyteArrayOf(0x05U, 0x52U, 0x00U, 0x02U, 0x01U, 0x09U)
val asynchronousSettingValueUpdateMessage1 = ubyteArrayOf(0x05U, 0x92U, 0x00U, 0x02U, 0x01U, 0x09U)
val asynchronousSettingValueUpdateMessage2 = ubyteArrayOf(0x05U, 0x92U, 0x00U, 0x02U, 0x01U, 12U)
val getMultipleSettingsResponsePayload =
    ubyteArrayOf(0x12U, 0x00U, 0x02U, 0x01U, 0x09U, 0x03U, 0x01U, 0x00U, 0x79U, 0x01U, 0x00U)
val isEncodingNotificationMessage = ubyteArrayOf(0x05U, 0x93U, 0x00U, 0x0AU, 0x01U, 0x01U)
val isNotEncodingNotificationMessage = ubyteArrayOf(0x05U, 0x93U, 0x00U, 0x0AU, 0x01U, 0x00U)
val isBusyNotificationMessage = ubyteArrayOf(0x05U, 0x93U, 0x00U, 0x08U, 0x01U, 0x01U)
val isNotBusyNotificationMessage = ubyteArrayOf(0x05U, 0x93U, 0x00U, 0x08U, 0x01U, 0x00U)
val registerBusyResponseMessage = ubyteArrayOf(0x05U, 0x53U, 0x00U, 0x08U, 0x01U, 0x01U)
val registerEncodingResponseMessage = ubyteArrayOf(0x05U, 0x53U, 0x00U, 0x0AU, 0x01U, 0x01U)
val genericProtoResponseSuccessPayload =
    ResponseGeneric(EnumResultGeneric.RESULT_SUCCESS).encodeToByteArray().toUByteArray()
val initialApScanResponse =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.SCAN_WIFI_NETWORKS_RSP.value) +
        ResponseStartScanning(EnumResultGeneric.RESULT_SUCCESS, EnumScanning.SCANNING_STARTED)
            .encodeToByteArray()
            .toUByteArray()
val initialApScanResponseFailure =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.SCAN_WIFI_NETWORKS_RSP.value) +
        ResponseStartScanning(
                EnumResultGeneric.RESULT_ILL_FORMED, EnumScanning.SCANNING_NEVER_STARTED)
            .encodeToByteArray()
            .toUByteArray()
val intermediateApScanNotification =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.NOTIF_START_SCAN.value) +
        NotifStartScanning(
                scanningState = EnumScanning.SCANNING_STARTED,
                scanId = 1,
                totalEntries = 2,
                totalConfiguredSsid = 3)
            .encodeToByteArray()
            .toUByteArray()
val finalApScanNotification =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.NOTIF_START_SCAN.value) +
        NotifStartScanning(
                scanningState = EnumScanning.SCANNING_SUCCESS,
                scanId = 9,
                totalEntries = 9,
                totalConfiguredSsid = 9)
            .encodeToByteArray()
            .toUByteArray()
val getApScanResultsResponse =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.GET_AP_ENTRIES_RSP.value) +
        ResponseGetApEntries(
                scanId = 0,
                result = EnumResultGeneric.RESULT_SUCCESS,
                entries =
                    listOf(
                        ResponseGetApEntries.ScanEntry(
                            signalFrequencyMhz = 0,
                            signalStrengthBars = 0,
                            ssid = "zero",
                            scanEntryFlags = 0),
                        ResponseGetApEntries.ScanEntry(
                            signalFrequencyMhz = 1,
                            signalStrengthBars = 1,
                            ssid = "one",
                            scanEntryFlags = 1),
                        ResponseGetApEntries.ScanEntry(
                            signalFrequencyMhz = 2,
                            signalStrengthBars = 2,
                            ssid = "two",
                            scanEntryFlags = 0xF)))
            .encodeToByteArray()
            .toUByteArray()
val connectNewAccessPointResponseSuccess =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.REQUEST_WIFI_CONNECT_NEW_RSP.value) +
        ResponseConnectNew(
                result = EnumResultGeneric.RESULT_SUCCESS,
                provisioningState = EnumProvisioning.PROVISIONING_STARTED,
                timeoutSeconds = 100,
            )
            .encodeToByteArray()
            .toUByteArray()
val connectAccessPointOngoing =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.NOTIF_PROVIS_STATE.value) +
        NotifProvisioningState(provisioningState = EnumProvisioning.PROVISIONING_STARTED)
            .encodeToByteArray()
            .toUByteArray()
val connectAccessPointComplete =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.NOTIF_PROVIS_STATE.value) +
        NotifProvisioningState(provisioningState = EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP)
            .encodeToByteArray()
            .toUByteArray()
val connectAccessPointFailureSuccess =
    ubyteArrayOf(FeatureId.NETWORK_MANAGEMENT.value, ActionId.REQUEST_WIFI_CONNECT_RSP.value) +
        ResponseConnectNew(
                result = EnumResultGeneric.RESULT_SUCCESS,
                provisioningState = EnumProvisioning.PROVISIONING_ABORTED_BY_SYSTEM,
                timeoutSeconds = 100,
            )
            .encodeToByteArray()
            .toUByteArray()
val hardwareInfoResponsePayload =
    ubyteArrayOf(CommandId.GET_HARDWARE_INFO.value, GpStatus.SUCCESS.value) +
        ubyteArrayOf("modelNumber".length.toUByte()) +
        "modelNumber".encodeToUByteArray() +
        ubyteArrayOf("modelName".length.toUByte()) +
        "modelName".encodeToUByteArray() +
        ubyteArrayOf("deprecated".length.toUByte()) +
        "deprecated".encodeToUByteArray() +
        ubyteArrayOf("firmwareVersion".length.toUByte()) +
        "firmwareVersion".encodeToUByteArray() +
        ubyteArrayOf("serialNumber".length.toUByte()) +
        "serialNumber".encodeToUByteArray() +
        ubyteArrayOf("apSsid".length.toUByte()) +
        "apSsid".encodeToUByteArray() +
        ubyteArrayOf("apMacAddress".length.toUByte()) +
        "apMacAddress".encodeToUByteArray()
val getLivestreamStatusResponse1 =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.LIVESTREAM_STATUS_RSP.value) +
        NotifyLiveStreamStatus(
                liveStreamStatus = EnumLiveStreamStatus.LIVE_STREAM_STATE_CONFIG,
                liveStreamMaximumStreamBitrate = 100,
                liveStreamMinimumStreamBitrate = 0,
                liveStreamEncode = true,
                liveStreamBitrate = 1,
                liveStreamError = EnumLiveStreamError.LIVE_STREAM_ERROR_NONE,
                liveStreamLensSupported = true,
                liveStreamEncodeSupported = true,
                liveStreamProtuneSupported = true,
                liveStreamMaxLensUnsupported = true,
                liveStreamLensSupportedArray = listOf(EnumLens.LENS_WIDE),
                liveStreamWindowSizeSupportedArray = listOf(EnumWindowSize.WINDOW_SIZE_720))
            .encodeToByteArray()
            .toUByteArray()
val getLivestreamStatusNoti1 =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.LIVESTREAM_STATUS_NOTIF.value) +
        NotifyLiveStreamStatus(
                liveStreamStatus = EnumLiveStreamStatus.LIVE_STREAM_STATE_CONFIG,
                liveStreamMaximumStreamBitrate = 100,
                liveStreamMinimumStreamBitrate = 0,
                liveStreamEncode = true,
                liveStreamBitrate = 2,
                liveStreamError = EnumLiveStreamError.LIVE_STREAM_ERROR_NONE,
                liveStreamLensSupported = true,
                liveStreamEncodeSupported = true,
                liveStreamProtuneSupported = true,
                liveStreamMaxLensUnsupported = true,
                liveStreamLensSupportedArray = listOf(EnumLens.LENS_WIDE),
                liveStreamWindowSizeSupportedArray = listOf(EnumWindowSize.WINDOW_SIZE_720))
            .encodeToByteArray()
            .toUByteArray()
val getLivestreamStatusNoti2 =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.LIVESTREAM_STATUS_NOTIF.value) +
        NotifyLiveStreamStatus(
                liveStreamStatus = EnumLiveStreamStatus.LIVE_STREAM_STATE_CONFIG,
                liveStreamMaximumStreamBitrate = 100,
                liveStreamMinimumStreamBitrate = 0,
                liveStreamEncode = true,
                liveStreamBitrate = 3,
                liveStreamError = EnumLiveStreamError.LIVE_STREAM_ERROR_NONE,
                liveStreamLensSupported = true,
                liveStreamEncodeSupported = true,
                liveStreamProtuneSupported = true,
                liveStreamMaxLensUnsupported = true,
                liveStreamLensSupportedArray = listOf(EnumLens.LENS_WIDE),
                liveStreamWindowSizeSupportedArray = listOf(EnumWindowSize.WINDOW_SIZE_720))
            .encodeToByteArray()
            .toUByteArray()
val getLivestreamStatusNoti3 =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.LIVESTREAM_STATUS_NOTIF.value) +
        NotifyLiveStreamStatus(
                liveStreamStatus = EnumLiveStreamStatus.LIVE_STREAM_STATE_CONFIG,
                liveStreamMaximumStreamBitrate = 100,
                liveStreamMinimumStreamBitrate = 0,
                liveStreamEncode = true,
                liveStreamBitrate = 4,
                liveStreamError = EnumLiveStreamError.LIVE_STREAM_ERROR_NONE,
                liveStreamLensSupported = true,
                liveStreamEncodeSupported = true,
                liveStreamProtuneSupported = true,
                liveStreamMaxLensUnsupported = true,
                liveStreamLensSupportedArray = listOf(EnumLens.LENS_WIDE),
                liveStreamWindowSizeSupportedArray = listOf(EnumWindowSize.WINDOW_SIZE_720))
            .encodeToByteArray()
            .toUByteArray()
val unregisterLivestreamStatusRequest =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.GET_LIVESTREAM_STATUS.value) +
        RequestGetLiveStreamStatus(
                unregisterLiveStreamStatus =
                    listOf(EnumRegisterLiveStreamStatus.REGISTER_LIVE_STREAM_STATUS_STATUS))
            .encodeToByteArray()
            .toUByteArray()
val completeNotifyPresetStatus =
    NotifyPresetStatus(
        presetGroupArray =
            listOf(
                PresetGroup(
                    icon = EnumPresetGroupIcon.PRESET_GROUP_PHOTO_ICON_ID,
                    canAddPreset = true,
                    id = EnumPresetGroup.PRESET_GROUP_ID_PHOTO,
                    modeArray = listOf(EnumFlatMode.FLAT_MODE_IDLE, EnumFlatMode.FLAT_MODE_PHOTO),
                    presetArray =
                        listOf(
                            Preset(
                                id = 0,
                                icon = EnumPresetIcon.PRESET_ICON_BIKE,
                                titleNumber = 0,
                                mode = EnumFlatMode.FLAT_MODE_LOOPING,
                                isModified = true,
                                titleId = EnumPresetTitle.PRESET_TITLE_OUTDOOR,
                                isFixed = true,
                                customName = "cheese",
                                userDefined = true,
                                settingArray =
                                    listOf(PresetSetting(id = 0, value = 0, isCaption = false)))))),
    )
val getPresetStatusInitialResponse =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.GET_PRESET_STATUS_RSP.value) +
        completeNotifyPresetStatus.encodeToByteArray().toUByteArray()
val getPresetStatusPartialResponse1 =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.PRESET_MODIFIED_NOTIFICATION.value) +
        NotifyPresetStatus(
                presetGroupArray =
                    listOf(
                        PresetGroup(
                            icon = EnumPresetGroupIcon.PRESET_GROUP_TIMELAPSE_ICON_ID,
                            presetArray =
                                listOf(
                                    Preset(
                                        id = 0,
                                        icon = EnumPresetIcon.PRESET_ICON_BIKE,
                                        titleNumber = 0,
                                        settingArray = listOf(PresetSetting(isCaption = false)))))))
            .encodeToByteArray()
            .toUByteArray()
val getPresetStatusPartialResponse2 =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.PRESET_MODIFIED_NOTIFICATION.value) +
        NotifyPresetStatus(
                presetGroupArray =
                    listOf(
                        PresetGroup(
                            icon = EnumPresetGroupIcon.PRESET_GROUP_PHOTO_ICON_ID,
                            canAddPreset = true,
                            id = EnumPresetGroup.PRESET_GROUP_ID_PHOTO,
                            modeArray =
                                listOf(EnumFlatMode.FLAT_MODE_IDLE, EnumFlatMode.FLAT_MODE_PHOTO),
                        )))
            .encodeToByteArray()
            .toUByteArray()
val unregisterPresetInfoRequest =
    ubyteArrayOf(FeatureId.QUERY.value, ActionId.GET_PRESET_STATUS.value) +
        RequestGetPresetStatus(
                unregisterPresetStatus =
                    listOf(EnumRegisterPresetStatus.REGISTER_PRESET_STATUS_PRESET))
            .encodeToByteArray()
            .toUByteArray()

val complexBleWriteResponse =
    ubyteArrayOf(
        0x21U,
        0x72U,
        0x13U,
        0x00U,
        0x01U,
        0x01U,
        0x01U,
        0x02U,
        0x01U,
        0x04U,
        0x03U,
        0x01U,
        0x00U,
        0x04U,
        0x01U,
        0xFFU,
        0x06U,
        0x01U,
        0x00U,
        0x08U,
        0x80U,
        0x01U,
        0x00U,
        0x09U,
        0x01U,
        0x00U,
        0x0AU,
        0x01U,
        0x00U,
        0x0BU,
        0x01U,
        0x00U,
        0x0DU,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x00U,
        0x0EU,
        0x04U,
        0x81U,
        0x00U,
        0x00U,
        0x00U,
        0x00U,
        0x11U,
        0x01U,
        0x01U,
        0x13U,
        0x01U,
        0x03U,
        0x14U,
        0x01U,
        0x01U,
        0x15U,
        0x04U,
        0x00U,
        0x00U,
        0x3EU,
        0xA4U,
        0x82U,
        0x16U,
        0x01U,
        0x00U,
        0x17U,
        0x01U,
        0x00U,
        0x18U,
        0x01U,
        0x00U,
        0x1AU,
        0x01U,
        0x00U,
        0x1BU,
        0x01U,
        0x00U,
        0x1CU,
        0x01U,
        0x52U,
        0x1DU,
        0x83U,
        0x00U,
        0x1EU,
        0x0AU,
        0x47U,
        0x50U,
        0x32U,
        0x34U,
        0x35U,
        0x30U,
        0x30U,
        0x34U,
        0x35U,
        0x36U,
        0x1FU,
        0x01U,
        0x00U,
        0x20U,
        0x01U,
        0x01U,
        0x84U,
        0x21U,
        0x01U,
        0x00U,
        0x22U,
        0x04U,
        0x00U,
        0x00U,
        0x08U,
        0x73U,
        0x23U,
        0x04U,
        0x00U,
        0x00U,
        0x0FU,
        0xD6U,
        0x24U,
        0x04U,
        0x00U,
        0x00U,
        0x85U,
        0x00U,
        0x40U,
        0x25U,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x35U,
        0x26U,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x40U,
        0x27U,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x86U,
        0x35U,
        0x28U,
        0x12U,
        0x25U,
        0x31U,
        0x42U,
        0x25U,
        0x30U,
        0x34U,
        0x25U,
        0x30U,
        0x36U,
        0x25U,
        0x30U,
        0x37U,
        0x25U,
        0x33U,
        0x31U,
        0x25U,
        0x87U,
        0x30U,
        0x44U,
        0x29U,
        0x01U,
        0x00U,
        0x2AU,
        0x01U,
        0x00U,
        0x2DU,
        0x01U,
        0x00U,
        0x31U,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x00U,
        0x36U,
        0x08U,
        0x88U,
        0x00U,
        0x00U,
        0x00U,
        0x00U,
        0x01U,
        0x95U,
        0x82U,
        0x60U,
        0x37U,
        0x01U,
        0x01U,
        0x38U,
        0x01U,
        0x01U,
        0x39U,
        0x04U,
        0x00U,
        0x6EU,
        0x2FU,
        0x89U,
        0x81U,
        0x3AU,
        0x01U,
        0x00U,
        0x3BU,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x00U,
        0x3CU,
        0x04U,
        0x00U,
        0x00U,
        0x01U,
        0xF4U,
        0x3DU,
        0x01U,
        0x02U,
        0x8AU,
        0x3EU,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x00U,
        0x3FU,
        0x01U,
        0x00U,
        0x40U,
        0x04U,
        0x00U,
        0x00U,
        0x04U,
        0x39U,
        0x41U,
        0x01U,
        0x00U,
        0x42U,
        0x8BU,
        0x01U,
        0x64U,
        0x43U,
        0x01U,
        0x64U,
        0x44U,
        0x01U,
        0x00U,
        0x45U,
        0x01U,
        0x01U,
        0x46U,
        0x01U,
        0x35U,
        0x4AU,
        0x01U,
        0x00U,
        0x4BU,
        0x01U,
        0x8CU,
        0x00U,
        0x4CU,
        0x01U,
        0x01U,
        0x4DU,
        0x01U,
        0x01U,
        0x4EU,
        0x01U,
        0x00U,
        0x4FU,
        0x01U,
        0x00U,
        0x51U,
        0x01U,
        0x01U,
        0x52U,
        0x01U,
        0x01U,
        0x8DU,
        0x53U,
        0x01U,
        0x01U,
        0x55U,
        0x01U,
        0x00U,
        0x56U,
        0x01U,
        0x00U,
        0x58U,
        0x01U,
        0x00U,
        0x59U,
        0x01U,
        0x0CU,
        0x5AU,
        0x01U,
        0x01U,
        0x5BU,
        0x8EU,
        0x01U,
        0x00U,
        0x5DU,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x02U,
        0x5EU,
        0x04U,
        0x00U,
        0x01U,
        0x00U,
        0x00U,
        0x5FU,
        0x04U,
        0x00U,
        0x02U,
        0x00U,
        0x8FU,
        0x00U,
        0x60U,
        0x04U,
        0x00U,
        0x00U,
        0x03U,
        0xE8U,
        0x61U,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x02U,
        0x62U,
        0x04U,
        0x01U,
        0x00U,
        0x00U,
        0x02U,
        0x80U,
        0x63U,
        0x04U,
        0x00U,
        0x00U,
        0x05U,
        0x47U,
        0x64U,
        0x04U,
        0x00U,
        0x00U,
        0x00U,
        0x00U,
        0x65U,
        0x01U,
        0x00U,
        0x66U,
        0x01U,
        0x00U,
        0x67U,
        0x81U,
        0x01U,
        0x00U,
        0x68U,
        0x01U,
        0x01U,
        0x69U,
        0x01U,
        0x00U,
        0x6AU,
        0x01U,
        0x00U,
        0x6BU,
        0x04U,
        0xFFU,
        0xFFU,
        0xFFU,
        0xFFU,
        0x6CU,
        0x01U,
        0x82U,
        0x00U,
        0x6DU,
        0x01U,
        0x00U,
        0x6EU,
        0x01U,
        0x00U,
        0x71U,
        0x01U,
        0x00U)

val advertisementData =
    ubyteArrayOf(
        0x02U,
        0x01U,
        0x02U,
        0x03U,
        0x02U,
        0xA6U,
        0xFEU,
        0x0FU,
        0xFFU,
        0xF2U,
        0x02U,
        0x02U,
        0x01U,
        0x38U,
        0x33U,
        0x00U,
        0xB3U,
        0xFEU,
        0x2AU,
        0x79U,
        0xDCU,
        0xEBU,
        0x0FU,
    )

val scanResponseData =
    ubyteArrayOf(
        0x0BU,
        0x09U,
        0x47U,
        0x6FU,
        0x50U,
        0x72U,
        0x6FU,
        0x20U,
        0x31U,
        0x30U,
        0x35U,
        0x38U,
        0x0BU,
        0x16U,
        0xA6U,
        0xFEU,
        0xF7U,
        0xA9U,
        0x76U,
        0x88U,
        0x31U,
        0x30U,
        0x35U,
        0x38U)

val scanResponseFea6ServiceData =
    ubyteArrayOf(0x47U, 0x3BU, 0x28U, 0x2DU, 0x30U, 0x30U, 0x35U, 0x33U).toByteArray()
val advResponseManufData =
    ubyteArrayOf(0x02U, 0x01U, 0x41U, 0x23U, 0x00U, 0x99U, 0x64U, 0x26U, 0x61U, 0x21U, 0xE0U, 0x0FU)
        .toByteArray()
