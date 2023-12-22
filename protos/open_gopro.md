# open_gopro Protobuf Documentation


## EnumCOHNNetworkState




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| COHN_STATE_Init | 0 |  |
| COHN_STATE_Error | 1 |  |
| COHN_STATE_Exit | 2 |  |
| COHN_STATE_Idle | 5 |  |
| COHN_STATE_NetworkConnected | 27 |  |
| COHN_STATE_NetworkDisconnected | 28 |  |
| COHN_STATE_ConnectingToNetwork | 29 |  |
| COHN_STATE_Invalid | 30 |  |

## EnumCOHNStatus




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| COHN_UNPROVISIONED | 0 |  |
| COHN_PROVISIONED | 1 |  |

## EnumCameraControlStatus




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| CAMERA_IDLE | 0 |  |
| CAMERA_CONTROL | 1 | Can only be set by camera, not by app or third party |
| CAMERA_EXTERNAL_CONTROL | 2 |  |

## EnumFlatMode




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| FLAT_MODE_UNKNOWN | -1 |  |
| FLAT_MODE_PLAYBACK | 4 |  |
| FLAT_MODE_SETUP | 5 |  |
| FLAT_MODE_VIDEO | 12 |  |
| FLAT_MODE_TIME_LAPSE_VIDEO | 13 |  |
| FLAT_MODE_LOOPING | 15 |  |
| FLAT_MODE_PHOTO_SINGLE | 16 |  |
| FLAT_MODE_PHOTO | 17 |  |
| FLAT_MODE_PHOTO_NIGHT | 18 |  |
| FLAT_MODE_PHOTO_BURST | 19 |  |
| FLAT_MODE_TIME_LAPSE_PHOTO | 20 |  |
| FLAT_MODE_NIGHT_LAPSE_PHOTO | 21 |  |
| FLAT_MODE_BROADCAST_RECORD | 22 |  |
| FLAT_MODE_BROADCAST_BROADCAST | 23 |  |
| FLAT_MODE_TIME_WARP_VIDEO | 24 |  |
| FLAT_MODE_LIVE_BURST | 25 |  |
| FLAT_MODE_NIGHT_LAPSE_VIDEO | 26 |  |
| FLAT_MODE_SLOMO | 27 |  |
| FLAT_MODE_IDLE | 28 |  |
| FLAT_MODE_VIDEO_STAR_TRAIL | 29 |  |
| FLAT_MODE_VIDEO_LIGHT_PAINTING | 30 |  |
| FLAT_MODE_VIDEO_LIGHT_TRAIL | 31 |  |

## EnumLens




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| LENS_WIDE | 0 |  |
| LENS_LINEAR | 4 |  |
| LENS_SUPERVIEW | 3 |  |

## EnumLiveStreamError




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| LIVE_STREAM_ERROR_NONE | 0 | No error (success) |
| LIVE_STREAM_ERROR_NETWORK | 1 | General network error during the stream |
| LIVE_STREAM_ERROR_CREATESTREAM | 2 | Startup error: bad URL or valid with live stream server |
| LIVE_STREAM_ERROR_OUTOFMEMORY | 3 | Not enough memory on camera to complete task |
| LIVE_STREAM_ERROR_INPUTSTREAM | 4 | Failed to get stream from low level camera system |
| LIVE_STREAM_ERROR_INTERNET | 5 | No internet access detected on startup of streamer |
| LIVE_STREAM_ERROR_OSNETWORK | 6 | Error occured in linux networking stack. usually means the server closed the connection |
| LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT | 7 | Timed out attemping to connect to the wifi network when attemping live stream |
| LIVE_STREAM_ERROR_SSL_HANDSHAKE | 8 | SSL handshake failed (commonly caused due to incorrect time / time zone) |
| LIVE_STREAM_ERROR_CAMERA_BLOCKED | 9 | Low level camera system rejected attempt to start live stream |
| LIVE_STREAM_ERROR_UNKNOWN | 10 | Unknown |
| LIVE_STREAM_ERROR_SD_CARD_FULL | 40 | Can not perform livestream because sd card is full |
| LIVE_STREAM_ERROR_SD_CARD_REMOVED | 41 | Livestream stopped because sd card was removed |

## EnumLiveStreamStatus




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| LIVE_STREAM_STATE_IDLE | 0 | Initial status. Livestream has not yet been configured |
| LIVE_STREAM_STATE_CONFIG | 1 | Livestream is being configured |
| LIVE_STREAM_STATE_READY | 2 | Livestream has finished configuration and is ready to start streaming |
| LIVE_STREAM_STATE_STREAMING | 3 | Livestream is actively streaming |
| LIVE_STREAM_STATE_COMPLETE_STAY_ON | 4 | Live stream is exiting. No errors occured. |
| LIVE_STREAM_STATE_FAILED_STAY_ON | 5 | Live stream is exiting. An error occurred. |
| LIVE_STREAM_STATE_RECONNECTING | 6 | An error occurred during livestream and stream is attempting to reconnect. |

## EnumPresetGroup




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| PRESET_GROUP_ID_VIDEO | 1000 |  |
| PRESET_GROUP_ID_PHOTO | 1001 |  |
| PRESET_GROUP_ID_TIMELAPSE | 1002 |  |

## EnumPresetGroupIcon




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| PRESET_GROUP_VIDEO_ICON_ID | 0 |  |
| PRESET_GROUP_PHOTO_ICON_ID | 1 |  |
| PRESET_GROUP_TIMELAPSE_ICON_ID | 2 |  |
| PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID | 3 |  |
| PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID | 4 |  |
| PRESET_GROUP_MAX_VIDEO_ICON_ID | 5 |  |
| PRESET_GROUP_MAX_PHOTO_ICON_ID | 6 |  |
| PRESET_GROUP_MAX_TIMELAPSE_ICON_ID | 7 |  |

## EnumPresetIcon




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| PRESET_ICON_VIDEO | 0 |  |
| PRESET_ICON_ACTIVITY | 1 |  |
| PRESET_ICON_CINEMATIC | 2 |  |
| PRESET_ICON_PHOTO | 3 |  |
| PRESET_ICON_LIVE_BURST | 4 |  |
| PRESET_ICON_BURST | 5 |  |
| PRESET_ICON_PHOTO_NIGHT | 6 |  |
| PRESET_ICON_TIMEWARP | 7 |  |
| PRESET_ICON_TIMELAPSE | 8 |  |
| PRESET_ICON_NIGHTLAPSE | 9 |  |
| PRESET_ICON_SNAIL | 10 |  |
| PRESET_ICON_VIDEO_2 | 11 |  |
| PRESET_ICON_PHOTO_2 | 13 |  |
| PRESET_ICON_PANORAMA | 14 |  |
| PRESET_ICON_BURST_2 | 15 |  |
| PRESET_ICON_TIMEWARP_2 | 16 |  |
| PRESET_ICON_TIMELAPSE_2 | 17 |  |
| PRESET_ICON_CUSTOM | 18 |  |
| PRESET_ICON_AIR | 19 |  |
| PRESET_ICON_BIKE | 20 |  |
| PRESET_ICON_EPIC | 21 |  |
| PRESET_ICON_INDOOR | 22 |  |
| PRESET_ICON_MOTOR | 23 |  |
| PRESET_ICON_MOUNTED | 24 |  |
| PRESET_ICON_OUTDOOR | 25 |  |
| PRESET_ICON_POV | 26 |  |
| PRESET_ICON_SELFIE | 27 |  |
| PRESET_ICON_SKATE | 28 |  |
| PRESET_ICON_SNOW | 29 |  |
| PRESET_ICON_TRAIL | 30 |  |
| PRESET_ICON_TRAVEL | 31 |  |
| PRESET_ICON_WATER | 32 |  |
| PRESET_ICON_LOOPING | 33 |  |
| PRESET_ICON_BASIC | 58 |  |
| PRESET_ICON_ULTRA_SLO_MO | 59 |  |
| PRESET_ICON_STANDARD_ENDURANCE | 60 |  |
| PRESET_ICON_ACTIVITY_ENDURANCE | 61 |  |
| PRESET_ICON_CINEMATIC_ENDURANCE | 62 |  |
| PRESET_ICON_SLOMO_ENDURANCE | 63 |  |
| PRESET_ICON_STATIONARY_1 | 64 |  |
| PRESET_ICON_STATIONARY_2 | 65 |  |
| PRESET_ICON_STATIONARY_3 | 66 |  |
| PRESET_ICON_STATIONARY_4 | 67 |  |
| PRESET_ICON_SIMPLE_SUPER_PHOTO | 70 |  |
| PRESET_ICON_SIMPLE_NIGHT_PHOTO | 71 |  |
| PRESET_ICON_HIGHEST_QUALITY_VIDEO | 73 |  |
| PRESET_ICON_STANDARD_QUALITY_VIDEO | 74 |  |
| PRESET_ICON_BASIC_QUALITY_VIDEO | 75 |  |
| PRESET_ICON_STAR_TRAIL | 76 |  |
| PRESET_ICON_LIGHT_PAINTING | 77 |  |
| PRESET_ICON_LIGHT_TRAIL | 78 |  |
| PRESET_ICON_FULL_FRAME | 79 |  |
| PRESET_ICON_TIMELAPSE_PHOTO | 1000 |  |
| PRESET_ICON_NIGHTLAPSE_PHOTO | 1001 |  |

## EnumPresetTitle




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| PRESET_TITLE_ACTIVITY | 0 |  |
| PRESET_TITLE_STANDARD | 1 |  |
| PRESET_TITLE_CINEMATIC | 2 |  |
| PRESET_TITLE_PHOTO | 3 |  |
| PRESET_TITLE_LIVE_BURST | 4 |  |
| PRESET_TITLE_BURST | 5 |  |
| PRESET_TITLE_NIGHT | 6 |  |
| PRESET_TITLE_TIME_WARP | 7 |  |
| PRESET_TITLE_TIME_LAPSE | 8 |  |
| PRESET_TITLE_NIGHT_LAPSE | 9 |  |
| PRESET_TITLE_VIDEO | 10 |  |
| PRESET_TITLE_SLOMO | 11 |  |
| PRESET_TITLE_PHOTO_2 | 13 |  |
| PRESET_TITLE_PANORAMA | 14 |  |
| PRESET_TITLE_TIME_WARP_2 | 16 |  |
| PRESET_TITLE_CUSTOM | 18 |  |
| PRESET_TITLE_AIR | 19 |  |
| PRESET_TITLE_BIKE | 20 |  |
| PRESET_TITLE_EPIC | 21 |  |
| PRESET_TITLE_INDOOR | 22 |  |
| PRESET_TITLE_MOTOR | 23 |  |
| PRESET_TITLE_MOUNTED | 24 |  |
| PRESET_TITLE_OUTDOOR | 25 |  |
| PRESET_TITLE_POV | 26 |  |
| PRESET_TITLE_SELFIE | 27 |  |
| PRESET_TITLE_SKATE | 28 |  |
| PRESET_TITLE_SNOW | 29 |  |
| PRESET_TITLE_TRAIL | 30 |  |
| PRESET_TITLE_TRAVEL | 31 |  |
| PRESET_TITLE_WATER | 32 |  |
| PRESET_TITLE_LOOPING | 33 |  |
| PRESET_TITLE_BASIC | 58 |  |
| PRESET_TITLE_ULTRA_SLO_MO | 59 |  |
| PRESET_TITLE_STANDARD_ENDURANCE | 60 |  |
| PRESET_TITLE_ACTIVITY_ENDURANCE | 61 |  |
| PRESET_TITLE_CINEMATIC_ENDURANCE | 62 |  |
| PRESET_TITLE_SLOMO_ENDURANCE | 63 |  |
| PRESET_TITLE_STATIONARY_1 | 64 |  |
| PRESET_TITLE_STATIONARY_2 | 65 |  |
| PRESET_TITLE_STATIONARY_3 | 66 |  |
| PRESET_TITLE_STATIONARY_4 | 67 |  |
| PRESET_TITLE_SIMPLE_VIDEO | 68 |  |
| PRESET_TITLE_SIMPLE_TIME_WARP | 69 |  |
| PRESET_TITLE_SIMPLE_SUPER_PHOTO | 70 |  |
| PRESET_TITLE_SIMPLE_NIGHT_PHOTO | 71 |  |
| PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE | 72 |  |
| PRESET_TITLE_HIGHEST_QUALITY | 73 |  |
| PRESET_TITLE_EXTENDED_BATTERY | 74 |  |
| PRESET_TITLE_LONGEST_BATTERY | 75 |  |
| PRESET_TITLE_STAR_TRAIL | 76 |  |
| PRESET_TITLE_LIGHT_PAINTING | 77 |  |
| PRESET_TITLE_LIGHT_TRAIL | 78 |  |
| PRESET_TITLE_FULL_FRAME | 79 |  |
| PRESET_TITLE_STANDARD_QUALITY_VIDEO | 82 |  |
| PRESET_TITLE_BASIC_QUALITY_VIDEO | 83 |  |
| PRESET_TITLE_HIGHEST_QUALITY_VIDEO | 93 |  |
| PRESET_TITLE_USER_DEFINED_CUSTOM_NAME | 94 |  |

## EnumProvisioning




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| PROVISIONING_UNKNOWN | 0 |  |
| PROVISIONING_NEVER_STARTED | 1 |  |
| PROVISIONING_STARTED | 2 |  |
| PROVISIONING_ABORTED_BY_SYSTEM | 3 |  |
| PROVISIONING_CANCELLED_BY_USER | 4 |  |
| PROVISIONING_SUCCESS_NEW_AP | 5 |  |
| PROVISIONING_SUCCESS_OLD_AP | 6 |  |
| PROVISIONING_ERROR_FAILED_TO_ASSOCIATE | 7 |  |
| PROVISIONING_ERROR_PASSWORD_AUTH | 8 |  |
| PROVISIONING_ERROR_EULA_BLOCKING | 9 |  |
| PROVISIONING_ERROR_NO_INTERNET | 10 |  |
| PROVISIONING_ERROR_UNSUPPORTED_TYPE | 11 |  |

## EnumRegisterLiveStreamStatus




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| REGISTER_LIVE_STREAM_STATUS_STATUS | 1 |  |
| REGISTER_LIVE_STREAM_STATUS_ERROR | 2 |  |
| REGISTER_LIVE_STREAM_STATUS_MODE | 3 |  |
| REGISTER_LIVE_STREAM_STATUS_BITRATE | 4 |  |

## EnumRegisterPresetStatus




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| REGISTER_PRESET_STATUS_PRESET | 1 | Send notification when properties of a preset change |
| REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY | 2 | Send notification when properties of a preset group change |

## EnumResultGeneric




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| RESULT_UNKNOWN | 0 |  |
| RESULT_SUCCESS | 1 |  |
| RESULT_ILL_FORMED | 2 |  |
| RESULT_NOT_SUPPORTED | 3 |  |
| RESULT_ARGUMENT_OUT_OF_BOUNDS | 4 |  |
| RESULT_ARGUMENT_INVALID | 5 |  |
| RESULT_RESOURCE_NOT_AVAILABLE | 6 |  |

## EnumScanEntryFlags




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| SCAN_FLAG_OPEN | 0x00 | This network does not require authentication |
| SCAN_FLAG_AUTHENTICATED | 0x01 | This network requires authentication |
| SCAN_FLAG_CONFIGURED | 0x02 | This network has been previously provisioned |
| SCAN_FLAG_BEST_SSID | 0x04 |  |
| SCAN_FLAG_ASSOCIATED | 0x08 | camera is connected to this AP |
| SCAN_FLAG_UNSUPPORTED_TYPE | 0x10 |  |

## EnumScanning




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| SCANNING_UNKNOWN | 0 |  |
| SCANNING_NEVER_STARTED | 1 |  |
| SCANNING_STARTED | 2 |  |
| SCANNING_ABORTED_BY_SYSTEM | 3 |  |
| SCANNING_CANCELLED_BY_USER | 4 |  |
| SCANNING_SUCCESS | 5 |  |

## EnumWindowSize




| Name |  Value | Summary |
| ---- |  ----- | ------- |
| WINDOW_SIZE_480 | 4 |  |
| WINDOW_SIZE_720 | 7 |  |
| WINDOW_SIZE_1080 | 12 |  |

## Media

A reusable model to represent a media file



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| folder |  optional | string  | 1  | Directory that the media is contained in |
| file |  optional | string  | 2  | Filename of media |

## NotifProvisioningState

Provision state notification

 TODO refernce where this is triggered



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| provisioning_state |  required | [EnumProvisioning]({% link protos/open_gopro.md %}#enumprovisioning)  | 1  | Provisioning / connection state |

## NotifStartScanning

Scanning state notification

 Triggered via [RequestStartScan]( {% link protos/open_gopro.md %}#requeststartscan )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| scanning_state |  required | [EnumScanning]({% link protos/open_gopro.md %}#enumscanning)  | 1  | Scanning state |
| scan_id |  optional | int32  | 2  | ID associated with scan results (included if scan was successful) |
| total_entries |  optional | int32  | 3  | Number of APs found during scan (included if scan was successful) |
| total_configured_ssid |  required | int32  | 4  | Total count of camera's provisioned SSIDs |

## NotifyCOHNStatus

Current COHN status triggered by a RequestGetCOHNStatus



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| status |  optional | [EnumCOHNStatus]({% link protos/open_gopro.md %}#enumcohnstatus)  | 1  | Current COHN status |
| state |  optional | [EnumCOHNNetworkState]({% link protos/open_gopro.md %}#enumcohnnetworkstate)  | 2  | Current COHN network state |
| username |  optional | string  | 3  | Username used for http basic auth header |
| password |  optional | string  | 4  | Password used for http basic auth header |
| ipaddress |  optional | string  | 5  | Camera's IP address on the local network |
| enabled |  optional | bool  | 6  | Is COHN currently enabled |
| ssid |  optional | string  | 7  | Currently connected SSID |
| macaddress |  optional | string  | 8  | MAC address of the wifi adapter |

## NotifyLiveStreamStatus

Live Stream status

 Sent either:
   - as a syncrhonous response to initial [RequestGetLiveStreamStatus]( {% link protos/open_gopro.md %}#requestgetlivestreamstatus )
   - as asynchronous notifications registered for via [RequestGetLiveStreamStatus]( {% link protos/open_gopro.md %}#requestgetlivestreamstatus )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| live_stream_status |  optional | [EnumLiveStreamStatus]({% link protos/open_gopro.md %}#enumlivestreamstatus)  | 1  | Live stream status |
| live_stream_error |  optional | [EnumLiveStreamError]({% link protos/open_gopro.md %}#enumlivestreamerror)  | 2  | Live stream error |
| live_stream_encode |  optional | bool  | 3  | Is live stream encoding? |
| live_stream_bitrate |  optional | int32  | 4  | Live stream bitrate (Kbps) |
| live_stream_window_size_supported_array |  repeated | [EnumWindowSize]({% link protos/open_gopro.md %}#enumwindowsize)  | 5  | Set of currently supported resolutions |
| live_stream_encode_supported |  optional | bool  | 6  | Does the camera support encoding while live streaming? |
| live_stream_max_lens_unsupported |  optional | bool  | 7  | Is the Max Lens feature NOT supported? |
| live_stream_minimum_stream_bitrate |  optional | int32  | 8  | Camera-defined minimum bitrate (static) (Kbps) |
| live_stream_maximum_stream_bitrate |  optional | int32  | 9  | Camera-defined maximum bitrate (static) (Kbps) |
| live_stream_lens_supported |  optional | bool  | 10  | Does camera support setting lens for live streaming? |
| live_stream_lens_supported_array |  repeated | [EnumLens]({% link protos/open_gopro.md %}#enumlens)  | 11  | Set of currently supported FOV options |

## NotifyPresetStatus

Current Preset status

 Sent either:
 - synchronously via initial response to [RequestGetPresetStatus]( {% link protos/open_gopro.md %}#requestgetpresetstatus )
 - asynchronously when Preset change if registered in @rev RequestGetPresetStatus



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| preset_group_array |  repeated | [PresetGroup]({% link protos/open_gopro.md %}#presetgroup)  | 1  | Array of currently available Preset Groups |

## Preset

An individual preset.



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| id |  optional | int32  | 1  | Preset ID |
| mode |  optional | [EnumFlatMode]({% link protos/open_gopro.md %}#enumflatmode)  | 2  | Preset flatmode ID |
| title_id |  optional | [EnumPresetTitle]({% link protos/open_gopro.md %}#enumpresettitle)  | 3  | Preset Title ID |
| title_number |  optional | int32  | 4  | Preset Title Number (e.g. 1/2/3 in Custom1, Custom2, Custom3) |
| user_defined |  optional | bool  | 5  | Is the Preset custom/user-defined? |
| icon |  optional | [EnumPresetIcon]({% link protos/open_gopro.md %}#enumpreseticon)  | 6  | Preset Icon ID |
| setting_array |  repeated | [PresetSetting]({% link protos/open_gopro.md %}#presetsetting)  | 7  | Array of settings associated with this Preset |
| is_modified |  optional | bool  | 8  | Has Preset been modified from factory defaults? (False for user-defined Presets) |
| is_fixed |  optional | bool  | 9  | Is this Preset mutable? |
| custom_name |  optional | string  | 10  | Custom string name given to this preset via [RequestCustomPresetUpdate]( {% link protos/open_gopro.md %}#requestcustompresetupdate ) |

## PresetGroup

Preset Group meta information and contained Presets



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| id |  optional | [EnumPresetGroup]({% link protos/open_gopro.md %}#enumpresetgroup)  | 1  | Preset Group ID |
| preset_array |  repeated | [Preset]({% link protos/open_gopro.md %}#preset)  | 2  | Array of Presets contained in this Preset Group |
| can_add_preset |  optional | bool  | 3  | Is there room in the group to add additional Presets? |
| icon |  optional | [EnumPresetGroupIcon]({% link protos/open_gopro.md %}#enumpresetgroupicon)  | 4  | The icon to display for this preset group |

## PresetSetting

Setting representation that comprises a  [Preset]( {% link protos/open_gopro.md %}#preset )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| id |  optional | int32  | 1  | Setting ID |
| value |  optional | int32  | 2  | Setting value |
| is_caption |  optional | bool  | 3  | Does this setting appear on the Preset "pill" in the camera UI? |

## RequestCOHNCert

Get the COHN certificate.

 Returns a [ResponseCOHNCert]( {% link protos/open_gopro.md %}#responsecohncert )


## RequestClearCOHNCert

Clear the COHN certificate.

 Returns a [ResponseGeneric]( {% link protos/open_gopro.md %}#responsegeneric ) with the status of the clear


## RequestConnect

Connect to (but do not authenticate with) an Access Point

 This is intended to be used to connect to a previously-connected Access Point

 Response: [ResponseConnect]( {% link protos/open_gopro.md %}#responseconnect )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| ssid |  required | string  | 1  | AP SSID |

## RequestConnectNew

Connect to and authenticate with an Access Point

 This is only intended to be used if the AP is not previously provisioned.

 Response: [ResponseConnectNew]( {% link protos/open_gopro.md %}#responseconnectnew ) sent immediately

 Notification: [NotifProvisioningState]( {% link protos/open_gopro.md %}#notifprovisioningstate ) sent periodically as provisioning state changes



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| ssid |  required | string  | 1  | AP SSID |
| password |  required | string  | 2  | AP password |
| static_ip |  optional | bytes  | 3  | Static IP address |
| gateway |  optional | bytes  | 4  | Gateway IP address |
| subnet |  optional | bytes  | 5  | Subnet mask |
| dns_primary |  optional | bytes  | 6  | Primary DNS |
| dns_secondary |  optional | bytes  | 7  | Secondary DNS |

## RequestCreateCOHNCert

Create the COHN certificate.

 Returns a [ResponseGeneric]( {% link protos/open_gopro.md %}#responsegeneric ) with the status of the creation



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| override |  optional | bool  | 1  | Override current provisioning and create new cert |

## RequestCustomPresetUpdate

Request to update the active custom preset

 This only operates on the currently active Preset and will fail  if the current
 Preset is not custom.

 The use cases are:

 1. Update the Custom Preset Icon
     - `icon_id` is always optional and can always be passed

 and / or

 2. Update the Custom Preset Title to a...
      - **Factory Preset Title**: Set `title_id` to a non-94 value
      - **Custom Preset Name**: Set `title_id` to 94 and specify a `custom_name`

 Returns a [ResponseGeneric]( {% link protos/open_gopro.md %}#responsegeneric ) with the status of the preset update request.



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| title_id |  optional | [EnumPresetTitle]({% link protos/open_gopro.md %}#enumpresettitle)  | 1  | Preset Title ID   The range of acceptable custom title ID's can be found in the initial [NotifyPresetStatus]( {% link protos/open_gopro.md %}#notifypresetstatus ) response  to [RequestGetPresetStatus]( {% link protos/open_gopro.md %}#requestgetpresetstatus ) |
| custom_name |  optional | string  | 2  | utf-8 encoded target custom preset name |
| icon_id |  optional | [EnumPresetIcon]({% link protos/open_gopro.md %}#enumpreseticon)  | 3  | Preset Icon ID   The range of acceptable custom icon ID's can be found in the initial [NotifyPresetStatus]( {% link protos/open_gopro.md %}#notifypresetstatus ) response to  [RequestGetPresetStatus]( {% link protos/open_gopro.md %}#requestgetpresetstatus ) |

## RequestGetApEntries

Get a list of Access Points found during a [RequestStartScan]( {% link protos/open_gopro.md %}#requeststartscan )

 Response: [ResponseGetApEntries]( {% link protos/open_gopro.md %}#responsegetapentries )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| start_index |  required | int32  | 1  | Used for paging. 0 <= start_index < [ResponseGetApEntries]( {% link protos/open_gopro.md %}#responsegetapentries ) .total_entries |
| max_entries |  required | int32  | 2  | Used for paging. Value must be < [ResponseGetApEntries]( {% link protos/open_gopro.md %}#responsegetapentries ) .total_entries |
| scan_id |  required | int32  | 3  | ID corresponding to a set of scan results (i.e. [ResponseGetApEntries]( {% link protos/open_gopro.md %}#responsegetapentries ) .scan_id) |

## RequestGetCOHNStatus

Get the current COHN status.

 This always returns a [NotifyCOHNStatus]( {% link protos/open_gopro.md %}#notifycohnstatus )

 Additionally, asynchronous updates can also be registerd to return more [NotifyCOHNStatus]( {% link protos/open_gopro.md %}#notifycohnstatus ) when a value
 changes.



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| register_cohn_status |  optional | bool  | 1  | 1 to register, 0 to unregister |

## RequestGetLastCapturedMedia

Get the last captured media filename

 Returns a [ResponseLastCapturedMedia]( {% link protos/open_gopro.md %}#responselastcapturedmedia )


## RequestGetLiveStreamStatus

Get the current livestream status (and optionally register for future status changes)

 Both current status and future status changes are sent via [NotifyLiveStreamStatus]( {% link protos/open_gopro.md %}#notifylivestreamstatus )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| register_live_stream_status |  repeated | [EnumRegisterLiveStreamStatus]({% link protos/open_gopro.md %}#enumregisterlivestreamstatus)  | 1  | Array of live stream statuses to be notified about |
| unregister_live_stream_status |  repeated | [EnumRegisterLiveStreamStatus]({% link protos/open_gopro.md %}#enumregisterlivestreamstatus)  | 2  | Array of live stream statuses to stop being notified about |

## RequestGetPresetStatus

Get preset status (and optionally register to be notified when it changes)

 Response: [NotifyPresetStatus]( {% link protos/open_gopro.md %}#notifypresetstatus ) sent immediately

 Notification: [NotifyPresetStatus]( {% link protos/open_gopro.md %}#notifypresetstatus ) sent periodically as preset status changes, if registered.



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| register_preset_status |  repeated | [EnumRegisterPresetStatus]({% link protos/open_gopro.md %}#enumregisterpresetstatus)  | 1  | Array of Preset statuses to be notified about |
| unregister_preset_status |  repeated | [EnumRegisterPresetStatus]({% link protos/open_gopro.md %}#enumregisterpresetstatus)  | 2  | Array of Preset statuses to stop being notified about |

## RequestReleaseNetwork

Request to disconnect from current AP network

 Response: [ResponseGeneric]( {% link protos/open_gopro.md %}#responsegeneric )


## RequestSetCOHNSetting

Enable and disable COHN if provisioned

 Returns a [ResponseGeneric]( {% link protos/open_gopro.md %}#responsegeneric )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| cohn_active |  optional | bool  | 1  | 1 to enable, 0 to disable |

## RequestSetCameraControlStatus

Set Camera Control Status (as part of Global Behaviors feature)

 Response: [ResponseGeneric]( {% link protos/open_gopro.md %}#responsegeneric )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| camera_control_status |  required | [EnumCameraControlStatus]({% link protos/open_gopro.md %}#enumcameracontrolstatus)  | 1  | Declare who is taking control of the camera |

## RequestSetLiveStreamMode

Configure lives streaming

 The current livestream status can be queried via [RequestGetLiveStreamStatus]( {% link protos/open_gopro.md %}#requestgetlivestreamstatus )

 Response: [ResponseGeneric]( {% link protos/open_gopro.md %}#responsegeneric )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| url |  optional | string  | 1  | RTMP(S) URL used for live stream |
| encode |  optional | bool  | 2  | Save media to sdcard while streaming? |
| window_size |  optional | [EnumWindowSize]({% link protos/open_gopro.md %}#enumwindowsize)  | 3  | Resolution to use for live stream   The set of supported lenses is only available from the `live_stream_window_size_supported_array` in [NotifyLiveStreamStatus]( {% link protos/open_gopro.md %}#notifylivestreamstatus )) |
| cert |  optional | bytes  | 6  | Certificate for servers that require it |
| minimum_bitrate |  optional | int32  | 7  | Minimum desired bitrate (may or may not be honored) |
| maximum_bitrate |  optional | int32  | 8  | Maximum desired bitrate (may or may not be honored) |
| starting_bitrate |  optional | int32  | 9  | Starting bitrate |
| lens |  optional | [EnumLens]({% link protos/open_gopro.md %}#enumlens)  | 10  | Lens to use for live stream   The set of supported lenses is only available from the  `live_stream_lens_supported_array` in [NotifyLiveStreamStatus]( {% link protos/open_gopro.md %}#notifylivestreamstatus )) |

## RequestSetTurboActive

Enable/disable display of "Transferring Media" UI

 Response: [ResponseGeneric]( {% link protos/open_gopro.md %}#responsegeneric )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| active |  required | bool  | 1  | Enable or disable Turbo Transfer feature |

## RequestStartScan

Start scanning for Access Points

 > Serialization of this object is zero bytes.

 Response: [ResponseStartScanning]( {% link protos/open_gopro.md %}#responsestartscanning )  are sent immediately after the camera receives this command

 Notifications: [NotifStartScanning]( {% link protos/open_gopro.md %}#notifstartscanning ) are sent periodically as scanning state changes. Use to detect scan complete.


## ResponseCOHNCert

COHN Certificate response triggered by RequestCOHNCert



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| result |  optional | [EnumResultGeneric]({% link protos/open_gopro.md %}#enumresultgeneric)  | 1  | Was request successful? |
| cert |  optional | string  | 2  | Root CA cert (ASCII text) |

## ResponseConnect

The status of an attempt to connect to an Access Point

 Sent as the initial response to [RequestConnect]( {% link protos/open_gopro.md %}#requestconnect )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| result |  required | [EnumResultGeneric]({% link protos/open_gopro.md %}#enumresultgeneric)  | 1  | Generic pass/fail/error info |
| provisioning_state |  required | [EnumProvisioning]({% link protos/open_gopro.md %}#enumprovisioning)  | 2  | Provisioning/connection state |
| timeout_seconds |  required | int32  | 3  | Network connection timeout (seconds) |

## ResponseConnectNew

The status of an attempt to connect to an Access Point

 Sent as the initial response to [RequestConnectNew]( {% link protos/open_gopro.md %}#requestconnectnew )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| result |  required | [EnumResultGeneric]({% link protos/open_gopro.md %}#enumresultgeneric)  | 1  | Status of Connect New request |
| provisioning_state |  required | [EnumProvisioning]({% link protos/open_gopro.md %}#enumprovisioning)  | 2  | Current provisioning state of the network |
| timeout_seconds |  required | int32  | 3  | number of seconds camera will wait before declaring a network connection attempt failed. |

## ResponseGeneric

Generic Response used across most response / notification messages

 [EnumResultGeneric]( {% link protos/open_gopro.md %}#enumresultgeneric )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| result |  required | [EnumResultGeneric]({% link protos/open_gopro.md %}#enumresultgeneric)  | 1  | Generic pass/fail/error info |

## ResponseGetApEntries

A list of scan entries describing a scanned Access Point

 This is sent in response to a [RequestGetApEntries]( {% link protos/open_gopro.md %}#requestgetapentries )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| result |  required | [EnumResultGeneric]({% link protos/open_gopro.md %}#enumresultgeneric)  | 1  | Generic pass/fail/error info |
| scan_id |  required | int32  | 2  | ID associated with this batch of results |
| entries |  repeated | [ScanEntry]({% link protos/open_gopro.md %}#scanentry)  | 3  | Array containing details about discovered APs |

## ResponseLastCapturedMedia

Message sent in response to a [RequestGetLastCapturedMedia]( {% link protos/open_gopro.md %}#requestgetlastcapturedmedia )

 This contains the complete path of the last captured media. Depending on the type of media captured, it will return:

 - Single photo / video: The single media path
 - Any grouped media: The path to the first captured media in the group



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| result |  optional | [EnumResultGeneric]({% link protos/open_gopro.md %}#enumresultgeneric)  | 1  | Was the request successful? |
| media |  optional | [Media]({% link protos/open_gopro.md %}#media)  | 2  | Last captured media if result is RESULT_SUCCESS. Invalid if result is RESULT_RESOURCE_NOT_AVAILBLE. |

## ResponseStartScanning

The current scanning state.

 This is the initial response to a [RequestStartScan]( {% link protos/open_gopro.md %}#requeststartscan )



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| result |  required | [EnumResultGeneric]({% link protos/open_gopro.md %}#enumresultgeneric)  | 1  | Generic pass/fail/error info |
| scanning_state |  required | [EnumScanning]({% link protos/open_gopro.md %}#enumscanning)  | 2  | Scanning state |

## ScanEntry

The individual Scan Entry model



| Field | Typespec | Value Type | Value | Summary |
| ----- | -------- | ---------- | ----- | ------- |
| ssid |  required | string  | 1  | AP SSID |
| signal_strength_bars |  required | int32  | 2  | Signal strength (3 bars: >-70 dBm; 2 bars: >-85 dBm; 1 bar: <=-85 dBm) |
| signal_frequency_mhz |  required | int32  | 4  | Signal frequency (MHz) |
| scan_entry_flags |  required | int32  | 5  | Bitmasked value from [EnumScanEntryFlags]( {% link protos/open_gopro.md %}#enumscanentryflags ) |
