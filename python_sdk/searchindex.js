Search.setIndex({docnames:["api","authors","changelog","contributing","future_work","index","installation","quickstart","troubleshooting","usage"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":5,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["api.rst","authors.rst","changelog.rst","contributing.rst","future_work.rst","index.rst","installation.rst","quickstart.rst","troubleshooting.rst","usage.rst"],objects:{"open_gopro.api":[[0,1,1,"","params"]],"open_gopro.api.ble_commands":[[0,0,1,"","BleCommands"],[0,0,1,"","BleSettings"],[0,0,1,"","BleStatuses"]],"open_gopro.api.ble_commands.BleCommands":[[0,1,1,"","enable_wifi_ap"],[0,1,1,"","get_camera_settings"],[0,1,1,"","get_camera_statuses"],[0,1,1,"","get_date_time"],[0,1,1,"","get_hardware_info"],[0,1,1,"","get_open_gopro_api_version"],[0,1,1,"","get_preset_status"],[0,1,1,"","get_wifi_password"],[0,1,1,"","get_wifi_ssid"],[0,1,1,"","load_preset"],[0,1,1,"","load_preset_group"],[0,1,1,"","power_down"],[0,1,1,"","register_for_all_settings"],[0,1,1,"","register_for_all_statuses"],[0,1,1,"","set_camera_control"],[0,1,1,"","set_date_time"],[0,1,1,"","set_shutter"],[0,1,1,"","set_third_party_client_info"],[0,1,1,"","set_turbo_mode"],[0,1,1,"","sleep"],[0,1,1,"","tag_hilight"],[0,1,1,"","unregister_for_all_settings"],[0,1,1,"","unregister_for_all_statuses"]],"open_gopro.api.ble_commands.BleSettings":[[0,0,1,"","Iterator"],[0,1,1,"","anti_flicker"],[0,1,1,"","auto_off"],[0,1,1,"","fps"],[0,1,1,"","hypersmooth"],[0,1,1,"","led"],[0,1,1,"","max_lens_mode"],[0,1,1,"","multi_shot_field_of_view"],[0,1,1,"","photo_field_of_view"],[0,1,1,"","resolution"],[0,1,1,"","video_field_of_view"],[0,1,1,"","video_performance_mode"]],"open_gopro.api.ble_commands.BleStatuses":[[0,0,1,"","Iterator"],[0,1,1,"","acc_mic_stat"],[0,1,1,"","active_preset"],[0,1,1,"","analytics_rdy"],[0,1,1,"","analytics_size"],[0,1,1,"","ap_ssid"],[0,1,1,"","ap_state"],[0,1,1,"","app_count"],[0,1,1,"","band_5ghz_avail"],[0,1,1,"","batt_level"],[0,1,1,"","batt_ok_ota"],[0,1,1,"","batt_present"],[0,1,1,"","camera_control"],[0,1,1,"","camera_lens_type"],[0,1,1,"","capt_delay_active"],[0,1,1,"","control_allowed_over_usb"],[0,1,1,"","creating_preset"],[0,1,1,"","current_time_ms"],[0,1,1,"","deprecated_40"],[0,1,1,"","deprecated_92"],[0,1,1,"","dig_zoom_active"],[0,1,1,"","digital_zoom"],[0,1,1,"","download_cancel_pend"],[0,1,1,"","encoding_active"],[0,1,1,"","exposure_type"],[0,1,1,"","exposure_x"],[0,1,1,"","exposure_y"],[0,1,1,"","ext_batt_level"],[0,1,1,"","ext_batt_present"],[0,1,1,"","first_time"],[0,1,1,"","flatmode_id"],[0,1,1,"","gps_stat"],[0,1,1,"","in_context_menu"],[0,1,1,"","int_batt_per"],[0,1,1,"","last_hilight"],[0,1,1,"","lcd_lock_active"],[0,1,1,"","linux_core_active"],[0,1,1,"","live_burst_rem"],[0,1,1,"","live_burst_total"],[0,1,1,"","locate_active"],[0,1,1,"","logs_ready"],[0,1,1,"","media_mod_mic_stat"],[0,1,1,"","media_mod_stat"],[0,1,1,"","mobile_video"],[0,1,1,"","mode_group"],[0,1,1,"","multi_count_down"],[0,1,1,"","next_poll"],[0,1,1,"","num_group_photo"],[0,1,1,"","num_group_video"],[0,1,1,"","num_hilights"],[0,1,1,"","num_total_photo"],[0,1,1,"","num_total_video"],[0,1,1,"","orientation"],[0,1,1,"","ota_stat"],[0,1,1,"","pair_state"],[0,1,1,"","pair_state2"],[0,1,1,"","pair_time"],[0,1,1,"","pair_type"],[0,1,1,"","photo_presets"],[0,1,1,"","photos_rem"],[0,1,1,"","preset_modified"],[0,1,1,"","presets_group"],[0,1,1,"","preview_enabled"],[0,1,1,"","quick_capture"],[0,1,1,"","remote_ctrl_conn"],[0,1,1,"","remote_ctrl_ver"],[0,1,1,"","scheduled_capture"],[0,1,1,"","scheduled_preset"],[0,1,1,"","sd_rating_check_error"],[0,1,1,"","sd_status"],[0,1,1,"","sd_write_speed_error"],[0,1,1,"","sec_sd_stat"],[0,1,1,"","space_rem"],[0,1,1,"","streaming_supp"],[0,1,1,"","system_busy"],[0,1,1,"","system_hot"],[0,1,1,"","system_ready"],[0,1,1,"","thermal_mit_mode"],[0,1,1,"","timelapse_presets"],[0,1,1,"","timelapse_rem"],[0,1,1,"","timewarp_speed_ramp"],[0,1,1,"","turbo_mode"],[0,1,1,"","usb_connected"],[0,1,1,"","video_hindsight"],[0,1,1,"","video_low_temp"],[0,1,1,"","video_presets"],[0,1,1,"","video_progress"],[0,1,1,"","video_rem"],[0,1,1,"","wap_prov_stat"],[0,1,1,"","wap_scan_state"],[0,1,1,"","wap_scan_time"],[0,1,1,"","wifi_bars"],[0,1,1,"","wireless_band"],[0,1,1,"","wireless_enabled"],[0,1,1,"","wlan_ssid"],[0,1,1,"","zoom_encoding"]],"open_gopro.api.builders":[[0,0,1,"","BleSetting"],[0,0,1,"","BleStatus"],[0,0,1,"","WifiSetting"]],"open_gopro.api.builders.BleSetting":[[0,2,1,"","get_capabilities_names"],[0,2,1,"","get_capabilities_values"],[0,2,1,"","get_name"],[0,2,1,"","get_value"],[0,2,1,"","register_capability_update"],[0,2,1,"","register_value_update"],[0,2,1,"","set"],[0,2,1,"","unregister_capability_update"],[0,2,1,"","unregister_value_update"]],"open_gopro.api.builders.BleStatus":[[0,2,1,"","get_value"],[0,2,1,"","register_value_update"],[0,2,1,"","unregister_value_update"]],"open_gopro.api.builders.WifiSetting":[[0,2,1,"","set"]],"open_gopro.api.wifi_commands":[[0,0,1,"","WifiCommands"],[0,0,1,"","WifiSettings"]],"open_gopro.api.wifi_commands.WifiCommands":[[0,1,1,"","add_photo_hilight"],[0,1,1,"","add_video_hilight"],[0,1,1,"","download_file"],[0,1,1,"","get_camera_state"],[0,1,1,"","get_date_time"],[0,1,1,"","get_gpmf_data"],[0,1,1,"","get_media_info"],[0,1,1,"","get_media_list"],[0,1,1,"","get_open_gopro_api_version"],[0,1,1,"","get_preset_status"],[0,1,1,"","get_screennail"],[0,1,1,"","get_telemetry"],[0,1,1,"","get_thumbnail"],[0,1,1,"","get_webcam_status"],[0,1,1,"","get_webcam_version"],[0,1,1,"","remove_photo_hilight"],[0,1,1,"","remove_video_hilight"],[0,1,1,"","set_camera_control"],[0,1,1,"","set_date_time"],[0,1,1,"","set_digital_zoom"],[0,1,1,"","set_keep_alive"],[0,1,1,"","set_preset"],[0,1,1,"","set_preset_group"],[0,1,1,"","set_shutter_off"],[0,1,1,"","set_shutter_on"],[0,1,1,"","set_third_party_client_info"],[0,1,1,"","set_turbo_mode"],[0,1,1,"","start_preview_stream"],[0,1,1,"","stop_preview_stream"]],"open_gopro.api.wifi_commands.WifiSettings":[[0,0,1,"","Iterator"],[0,1,1,"","auto_off"],[0,1,1,"","fps"],[0,1,1,"","hypersmooth"],[0,1,1,"","max_lens_mode"],[0,1,1,"","media_format"],[0,1,1,"","multi_shot_field_of_view"],[0,1,1,"","photo_field_of_view"],[0,1,1,"","resolution"],[0,1,1,"","video_field_of_view"],[0,1,1,"","video_performance_mode"]],"open_gopro.constants":[[0,0,1,"","ActionId"],[0,0,1,"","CmdId"],[0,4,1,"","CmdType"],[0,0,1,"","ErrorCode"],[0,0,1,"","FeatureId"],[0,0,1,"","GoProEnum"],[0,0,1,"","GoProEnumMeta"],[0,0,1,"","GoProUUIDs"],[0,4,1,"","ProducerType"],[0,0,1,"","QueryCmdId"],[0,4,1,"","ResponseType"],[0,0,1,"","SettingId"],[0,0,1,"","StatusId"]],"open_gopro.constants.ActionId":[[0,1,1,"","GET_PRESET_STATUS"],[0,1,1,"","PRESET_MODIFIED_NOTIFICATION"],[0,1,1,"","SET_CAMERA_CONTROL"],[0,1,1,"","SET_TURBO_MODE"]],"open_gopro.constants.CmdId":[[0,1,1,"","GET_CAMERA_SETTINGS"],[0,1,1,"","GET_CAMERA_STATUSES"],[0,1,1,"","GET_DATE_TIME"],[0,1,1,"","GET_HW_INFO"],[0,1,1,"","GET_SETTINGS_JSON"],[0,1,1,"","GET_THIRD_PARTY_API_VERSION"],[0,1,1,"","LOAD_PRESET"],[0,1,1,"","LOAD_PRESET_GROUP"],[0,1,1,"","POWER_DOWN"],[0,1,1,"","PROTOBUF_COMMAND"],[0,1,1,"","REGISTER_ALL_SETTINGS"],[0,1,1,"","REGISTER_ALL_STATUSES"],[0,1,1,"","SET_DATE_TIME"],[0,1,1,"","SET_PAIRING_COMPLETE"],[0,1,1,"","SET_SHUTTER"],[0,1,1,"","SET_THIRD_PARTY_CLIENT_INFO"],[0,1,1,"","SET_WIFI"],[0,1,1,"","SLEEP"],[0,1,1,"","TAG_HILIGHT"],[0,1,1,"","UNREGISTER_ALL_SETTINGS"],[0,1,1,"","UNREGISTER_ALL_STATUSES"]],"open_gopro.constants.ErrorCode":[[0,1,1,"","ERROR"],[0,1,1,"","INVALID_PARAM"],[0,1,1,"","SUCCESS"],[0,1,1,"","UNKNOWN"]],"open_gopro.constants.FeatureId":[[0,1,1,"","COMMAND"],[0,1,1,"","QUERY"],[0,1,1,"","SETTING"]],"open_gopro.constants.GoProUUIDs":[[0,1,1,"","CM_NET_MGMT_COMM"],[0,1,1,"","CN_NET_MGMT_RESP"],[0,1,1,"","CQ_COMMAND"],[0,1,1,"","CQ_COMMAND_RESP"],[0,1,1,"","CQ_QUERY"],[0,1,1,"","CQ_QUERY_RESP"],[0,1,1,"","CQ_SENSOR"],[0,1,1,"","CQ_SENSOR_RESP"],[0,1,1,"","CQ_SETTINGS"],[0,1,1,"","CQ_SETTINGS_RESP"],[0,1,1,"","INTERNAL_81"],[0,1,1,"","INTERNAL_82"],[0,1,1,"","INTERNAL_83"],[0,1,1,"","INTERNAL_84"],[0,1,1,"","S_CAMERA_MANAGEMENT"],[0,1,1,"","S_CONTROL_QUERY"],[0,1,1,"","S_UNKNOWN"],[0,1,1,"","S_WIFI_ACCESS_POINT"],[0,1,1,"","WAP_CSI_PASSWORD"],[0,1,1,"","WAP_PASSWORD"],[0,1,1,"","WAP_POWER"],[0,1,1,"","WAP_SSID"],[0,1,1,"","WAP_STATE"]],"open_gopro.constants.QueryCmdId":[[0,1,1,"","GET_CAPABILITIES_NAME"],[0,1,1,"","GET_CAPABILITIES_VAL"],[0,1,1,"","GET_SETTING_NAME"],[0,1,1,"","GET_SETTING_VAL"],[0,1,1,"","GET_STATUS_VAL"],[0,1,1,"","INVALID_FOR_TESTING"],[0,1,1,"","PROTOBUF_QUERY"],[0,1,1,"","REG_CAPABILITIES_UPDATE"],[0,1,1,"","REG_SETTING_VAL_UPDATE"],[0,1,1,"","REG_STATUS_VAL_UPDATE"],[0,1,1,"","SETTING_CAPABILITY_PUSH"],[0,1,1,"","SETTING_VAL_PUSH"],[0,1,1,"","STATUS_VAL_PUSH"],[0,1,1,"","UNREG_CAPABILITIES_UPDATE"],[0,1,1,"","UNREG_SETTING_VAL_UPDATE"],[0,1,1,"","UNREG_STATUS_VAL_UPDATE"]],"open_gopro.constants.SettingId":[[0,1,1,"","ANTI_FLICKER"],[0,1,1,"","AUTO_OFF"],[0,1,1,"","FPS"],[0,1,1,"","HYPERSMOOTH"],[0,1,1,"","INTERNAL_102"],[0,1,1,"","INTERNAL_103"],[0,1,1,"","INTERNAL_104"],[0,1,1,"","INTERNAL_105"],[0,1,1,"","INTERNAL_106"],[0,1,1,"","INTERNAL_111"],[0,1,1,"","INTERNAL_112"],[0,1,1,"","INTERNAL_114"],[0,1,1,"","INTERNAL_115"],[0,1,1,"","INTERNAL_116"],[0,1,1,"","INTERNAL_117"],[0,1,1,"","INTERNAL_118"],[0,1,1,"","INTERNAL_124"],[0,1,1,"","INTERNAL_125"],[0,1,1,"","INTERNAL_126"],[0,1,1,"","INTERNAL_129"],[0,1,1,"","INTERNAL_13"],[0,1,1,"","INTERNAL_130"],[0,1,1,"","INTERNAL_131"],[0,1,1,"","INTERNAL_132"],[0,1,1,"","INTERNAL_133"],[0,1,1,"","INTERNAL_139"],[0,1,1,"","INTERNAL_142"],[0,1,1,"","INTERNAL_144"],[0,1,1,"","INTERNAL_145"],[0,1,1,"","INTERNAL_146"],[0,1,1,"","INTERNAL_147"],[0,1,1,"","INTERNAL_148"],[0,1,1,"","INTERNAL_149"],[0,1,1,"","INTERNAL_153"],[0,1,1,"","INTERNAL_154"],[0,1,1,"","INTERNAL_155"],[0,1,1,"","INTERNAL_156"],[0,1,1,"","INTERNAL_157"],[0,1,1,"","INTERNAL_158"],[0,1,1,"","INTERNAL_159"],[0,1,1,"","INTERNAL_160"],[0,1,1,"","INTERNAL_161"],[0,1,1,"","INTERNAL_163"],[0,1,1,"","INTERNAL_164"],[0,1,1,"","INTERNAL_165"],[0,1,1,"","INTERNAL_166"],[0,1,1,"","INTERNAL_167"],[0,1,1,"","INTERNAL_168"],[0,1,1,"","INTERNAL_169"],[0,1,1,"","INTERNAL_19"],[0,1,1,"","INTERNAL_24"],[0,1,1,"","INTERNAL_30"],[0,1,1,"","INTERNAL_31"],[0,1,1,"","INTERNAL_32"],[0,1,1,"","INTERNAL_37"],[0,1,1,"","INTERNAL_41"],[0,1,1,"","INTERNAL_42"],[0,1,1,"","INTERNAL_43"],[0,1,1,"","INTERNAL_44"],[0,1,1,"","INTERNAL_45"],[0,1,1,"","INTERNAL_47"],[0,1,1,"","INTERNAL_48"],[0,1,1,"","INTERNAL_5"],[0,1,1,"","INTERNAL_54"],[0,1,1,"","INTERNAL_6"],[0,1,1,"","INTERNAL_60"],[0,1,1,"","INTERNAL_61"],[0,1,1,"","INTERNAL_62"],[0,1,1,"","INTERNAL_64"],[0,1,1,"","INTERNAL_65"],[0,1,1,"","INTERNAL_66"],[0,1,1,"","INTERNAL_67"],[0,1,1,"","INTERNAL_68"],[0,1,1,"","INTERNAL_69"],[0,1,1,"","INTERNAL_75"],[0,1,1,"","INTERNAL_76"],[0,1,1,"","INTERNAL_79"],[0,1,1,"","INTERNAL_83"],[0,1,1,"","INTERNAL_84"],[0,1,1,"","INTERNAL_85"],[0,1,1,"","INTERNAL_86"],[0,1,1,"","INTERNAL_87"],[0,1,1,"","INTERNAL_88"],[0,1,1,"","INTERNAL_96"],[0,1,1,"","INVALID_FOR_TESTING"],[0,1,1,"","LED"],[0,1,1,"","MAX_LENS_MOD"],[0,1,1,"","MEDIA_FORMAT"],[0,1,1,"","MULTI_SHOT_FOV"],[0,1,1,"","PHOTO_FOV"],[0,1,1,"","PROTOBUF_SETTING"],[0,1,1,"","RESOLUTION"],[0,1,1,"","VIDEO_FOV"],[0,1,1,"","VIDEO_PERFORMANCE_MODE"]],"open_gopro.constants.StatusId":[[0,1,1,"","ACC_MIC_STAT"],[0,1,1,"","ACTIVE_PRESET"],[0,1,1,"","ANALYTICS_RDY"],[0,1,1,"","ANALYTICS_SIZE"],[0,1,1,"","APP_COUNT"],[0,1,1,"","AP_SSID"],[0,1,1,"","AP_STATE"],[0,1,1,"","BAND_5GHZ_AVAIL"],[0,1,1,"","BATT_LEVEL"],[0,1,1,"","BATT_OK_OTA"],[0,1,1,"","BATT_PRESENT"],[0,1,1,"","CAMERA_CONTROL"],[0,1,1,"","CAMERA_LENS_TYPE"],[0,1,1,"","CAPTURE_DELAY"],[0,1,1,"","CAPT_DELAY_ACTIVE"],[0,1,1,"","CONTROL_OVER_USB"],[0,1,1,"","CREATING_PRESET"],[0,1,1,"","CURRENT_TIME_MS"],[0,1,1,"","DEPRECATED_40"],[0,1,1,"","DEPRECATED_92"],[0,1,1,"","DIGITAL_ZOOM"],[0,1,1,"","DIG_ZOOM_ACTIVE"],[0,1,1,"","DOWNLAD_CANCEL_PEND"],[0,1,1,"","ENCODING"],[0,1,1,"","EXPOSURE_TYPE"],[0,1,1,"","EXPOSURE_X"],[0,1,1,"","EXPOSURE_Y"],[0,1,1,"","EXT_BATT_LEVEL"],[0,1,1,"","EXT_BATT_PRESENT"],[0,1,1,"","FIRST_TIME"],[0,1,1,"","FLATMODE_ID"],[0,1,1,"","GPS_STAT"],[0,1,1,"","INTERNAL_14"],[0,1,1,"","INTERNAL_46"],[0,1,1,"","INTERNAL_47"],[0,1,1,"","INTERNAL_48"],[0,1,1,"","INTERNAL_90"],[0,1,1,"","INT_BATT_PER"],[0,1,1,"","IN_CONTEXT_MENU"],[0,1,1,"","LAST_HILIGHT"],[0,1,1,"","LCD_LOCK_ACTIVE"],[0,1,1,"","LINUX_CORE_ACTIVE"],[0,1,1,"","LIVE_BURST_REM"],[0,1,1,"","LIVE_BURST_TOTAL"],[0,1,1,"","LOCATE_ACTIVE"],[0,1,1,"","LOGS_READY"],[0,1,1,"","MEDIA_MOD_MIC_STAT"],[0,1,1,"","MEDIA_MOD_STAT"],[0,1,1,"","MOBILE_VIDEO"],[0,1,1,"","MODE_GROUP"],[0,1,1,"","MULTI_COUNT_DOWN"],[0,1,1,"","NEXT_POLL"],[0,1,1,"","NUM_GROUP_PHOTO"],[0,1,1,"","NUM_GROUP_VIDEO"],[0,1,1,"","NUM_HILIGHTS"],[0,1,1,"","NUM_TOTAL_PHOTO"],[0,1,1,"","NUM_TOTAL_VIDEO"],[0,1,1,"","ORIENTATION"],[0,1,1,"","OTA_STAT"],[0,1,1,"","PAIR_STATE"],[0,1,1,"","PAIR_STATE2"],[0,1,1,"","PAIR_TIME"],[0,1,1,"","PAIR_TYPE"],[0,1,1,"","PHOTOS_REM"],[0,1,1,"","PHOTO_PRESETS"],[0,1,1,"","PRESETS_GROUP"],[0,1,1,"","PRESET_MODIFIED"],[0,1,1,"","PREVIEW_ENABLED"],[0,1,1,"","QUICK_CAPTURE"],[0,1,1,"","REMOTE_CTRL_CONN"],[0,1,1,"","REMOTE_CTRL_VER"],[0,1,1,"","SCHEDULED_CAPTURE"],[0,1,1,"","SCHEDULED_PRESET"],[0,1,1,"","SD_RATING_CHECK_ERROR"],[0,1,1,"","SD_STATUS"],[0,1,1,"","SD_WRITE_SPEED_ERROR"],[0,1,1,"","SEC_SD_STAT"],[0,1,1,"","SPACE_REM"],[0,1,1,"","STREAMING_SUPP"],[0,1,1,"","SYSTEM_BUSY"],[0,1,1,"","SYSTEM_HOT"],[0,1,1,"","SYSTEM_READY"],[0,1,1,"","THERMAL_MIT_MODE"],[0,1,1,"","TIMELAPSE_PRESETS"],[0,1,1,"","TIMELAPSE_REM"],[0,1,1,"","TIMEWARP_SPEED_RAMP"],[0,1,1,"","TURBO_MODE"],[0,1,1,"","USB_CONNECTED"],[0,1,1,"","VIDEO_HINDSIGHT"],[0,1,1,"","VIDEO_LOW_TEMP"],[0,1,1,"","VIDEO_PRESETS"],[0,1,1,"","VIDEO_PROGRESS"],[0,1,1,"","VIDEO_REM"],[0,1,1,"","WAP_PROV_STAT"],[0,1,1,"","WAP_SCAN_STATE"],[0,1,1,"","WAP_SCAN_TIME"],[0,1,1,"","WIFI_BARS"],[0,1,1,"","WIRELESS_BAND"],[0,1,1,"","WIRELESS_ENABLED"],[0,1,1,"","WLAN_SSID"],[0,1,1,"","ZOOM_ENCODING"]],"open_gopro.gopro":[[0,0,1,"","GoPro"],[0,0,1,"","Interface"],[0,6,1,"","acquire_ready_lock"],[0,6,1,"","ensure_initialized"]],"open_gopro.gopro.GoPro":[[0,5,1,"","ble_command"],[0,5,1,"","ble_setting"],[0,5,1,"","ble_status"],[0,2,1,"","close"],[0,2,1,"","get_update"],[0,5,1,"","identifier"],[0,5,1,"","is_ble_connected"],[0,5,1,"","is_busy"],[0,5,1,"","is_encoding"],[0,5,1,"","is_wifi_connected"],[0,2,1,"","keep_alive"],[0,2,1,"","open"],[0,5,1,"","version"],[0,5,1,"","wifi_command"],[0,5,1,"","wifi_setting"]],"open_gopro.responses":[[0,0,1,"","GoProResp"]],"open_gopro.responses.GoProResp":[[0,5,1,"","cmd"],[0,1,1,"","data"],[0,5,1,"","endpoint"],[0,5,1,"","flatten"],[0,5,1,"","id"],[0,5,1,"","is_ok"],[0,5,1,"","is_parsed"],[0,5,1,"","is_received"],[0,2,1,"","items"],[0,2,1,"","keys"],[0,1,1,"","status"],[0,5,1,"","uuid"],[0,2,1,"","values"]],open_gopro:[[0,3,0,"-","constants"],[0,3,0,"-","gopro"]]},objnames:{"0":["py","class","Python class"],"1":["py","attribute","Python attribute"],"2":["py","method","Python method"],"3":["py","module","Python module"],"4":["py","data","Python data"],"5":["py","property","Python property"],"6":["py","function","Python function"]},objtypes:{"0":"py:class","1":"py:attribute","2":"py:method","3":"py:module","4":"py:data","5":"py:property","6":"py:function"},terms:{"0":[0,5,9],"04":[2,5],"0456":0,"1":[0,5],"10":[0,3,5],"100":0,"101":0,"102":0,"103":0,"104":0,"105":0,"106":0,"107":0,"108":0,"109":0,"11":[0,3,5],"110":0,"111":0,"112":0,"113":0,"114":0,"115":0,"116":0,"117":0,"118":0,"12":5,"121":0,"122":0,"123":0,"124":0,"125":0,"126":0,"128":0,"129":0,"13":0,"130":0,"131":0,"132":0,"133":0,"134":0,"135":0,"139":0,"14":0,"142":0,"144":0,"145":0,"146":0,"147":0,"148":0,"149":0,"15":5,"153":0,"154":0,"155":0,"156":0,"157":0,"158":0,"159":0,"16":5,"160":0,"161":0,"162":0,"16299":3,"163":0,"164":0,"165":0,"166":0,"167":0,"168":0,"169":0,"17":0,"173":0,"18":0,"19":0,"2":[0,5,7,9],"20":[0,5],"2021":5,"2022":5,"21":0,"22":[0,5],"23":0,"24":0,"241":0,"243":0,"245":0,"25":5,"255":0,"26":[0,5],"27":[0,5],"28":[0,5],"29":[0,5],"3":[0,3,5,9],"30":[0,5],"31":0,"32":0,"33":0,"34":0,"35":0,"36":0,"37":0,"38":0,"39":0,"4":[0,5,7,9],"40":0,"41":0,"42":0,"43":[0,3],"44":0,"45":0,"46":0,"47":0,"48":0,"49":0,"5":[0,3,5],"50":0,"54":0,"55":0,"56":0,"57":0,"58":0,"59":0,"5ghz":0,"6":[0,5],"60":0,"61":0,"62":0,"63":0,"64":0,"65":0,"66":0,"67":0,"68":0,"69":0,"7":5,"70":0,"74":0,"75":0,"76":0,"77":0,"78":0,"79":0,"8":[0,3,5],"80":0,"81":0,"82":0,"83":0,"84":0,"85":0,"86":0,"87":0,"88":0,"89":0,"9":[0,5],"90":0,"91":0,"92":0,"93":0,"94":0,"95":0,"96":0,"97":0,"98":0,"99":0,"boolean":9,"break":[8,9],"byte":[0,8],"case":[2,9],"catch":2,"class":[0,2,5,8,9],"default":[0,7,8,9],"do":[0,7,9],"enum":[0,2,9],"float":0,"function":[2,3,5,8,9],"import":[0,8,9],"int":0,"long":[0,7],"new":9,"public":6,"return":[0,2,9],"short":9,"static":0,"true":[0,9],"try":5,"while":[0,9],A:[0,5,9],As:9,But:9,For:[0,3,5,7,9],If:[0,3,5,6,7,9],In:9,Is:0,It:[0,7,9],Not:[0,8],ON:[0,9],On:0,One:9,Or:[0,6],That:[0,9],The:[0,2,3,6,7,9],Their:9,Then:[6,9],There:[7,8,9],These:[0,9],To:[0,6,7],Will:0,__contains__:9,__getitem__:9,__iter__:9,__name__:8,_ble:8,about:[0,3,9],abov:[6,9],acc_mic_stat:0,accept:0,access:[0,5,7],accesstori:0,accumul:2,acquaint:5,acquir:0,acquire_ready_lock:0,across:[0,3],action:[0,2,3],actionid:0,activ:[0,2,9],active_preset:0,actual:2,ad:[2,9],adapt:[0,2],add:[0,2,3,7],add_photo_hilight:0,add_video_hilight:0,addit:0,adher:2,after:[0,9],agnost:2,air:0,alia:0,aliv:[0,2,5,9],all:[0,2,3,5,7,8,9],allow:[0,2],alreadi:[0,9],also:[0,7,9],alwai:[3,6,9],amount:[7,8],an:[0,3,5,8,9],analyt:0,analytics_rdi:0,analytics_s:0,ani:[0,3,9],anti:0,anti_flick:0,antiflick:0,anymor:9,anyth:[3,8,9],ap:[0,7,9],ap_ssid:0,ap_stat:0,api:[2,5],app:0,app_count:0,appear:0,append:9,applic:[0,5,9],appreci:3,approxim:0,april:5,ar:[0,3,7,9],archiv:6,arg:[0,2],argument:[0,2,5,7],around:0,articl:3,assum:7,asynchron:[0,5],asyncio:2,attempt:[0,7,9],attribut:[0,9],august:5,author:3,auto:0,auto_off:0,automat:[0,2,5,7,9],autonom:7,autooff:0,avail:[0,2],b:3,backend:7,bad:8,band:0,band_5ghz_avail:0,bar:0,base:[2,5,9],basic:9,batt_level:0,batt_ok_ota:0,batt_pres:0,batteri:[0,2,5],becaus:0,been:[0,9],befor:[0,3,9],behavior:[0,2],being:2,below:9,besid:[0,9],best:3,beta:2,between:0,big:[0,5],bitmask:0,ble:[2,5,7,8,9],ble_command:[0,9],ble_set:[0,9],ble_statu:[0,9],bleak:[2,5,7],blecommand:[0,9],bledevic:0,bleset:[0,9],blestatu:[0,9],blestatus:0,bleuuid:0,block:[0,9],blog:3,bluetooth:5,bluez:[3,5],bool:0,boot:0,both:[0,5,9],branch:3,bug:[2,4,5],bugfix:3,build:[0,3],builder:[0,9],bump:2,burst:0,busi:[0,9],bytearrai:0,cah:0,call:[0,9],callabl:[0,9],callback:0,camera:[0,2,5,7],camera_control:0,camera_fil:0,camera_lens_typ:0,cameracontrol:0,camis:1,can:[0,2,3,6,7,8,9],cancel:0,capabl:[0,9],capt_delay_act:0,captur:0,capture_delai:0,care:[0,9],caus:[2,9],cd:[2,3,6],chang:[0,2,3,9],changelog:[3,5],characterist:[0,5,9],charg:0,check:[2,3,9],checkout:3,ci:2,cl:0,clariti:9,classdict:0,clean:2,cli:2,clone:[3,6],close:[0,5],cm_net_mgmt_comm:0,cmd:[0,9],cmdid:[0,9],cmdtype:0,cn_net_mgmt_resp:0,code:[0,6,7],coexist:2,cold:0,collect:0,com:[1,3,6],command:[2,5,6,7],commit:3,common:2,commun:[0,2,9],communication_cli:0,complet:[0,9],complex:9,complic:2,compress:0,comput:0,configur:[0,7],connect:[0,2,5,7,9],consid:0,consider:5,consist:0,consol:7,constant:[5,9],construct:[0,2],consum:0,contain:[0,9],context:[0,9],contextu:0,continu:[0,7,9],contribut:5,contributor:[3,5],control:[0,2,5,7],control_allowed_over_usb:0,control_over_usb:0,coordin:0,copi:[3,6],core:0,corner:2,correct:0,correctli:9,correspond:9,could:[2,3],count:0,countdown:0,coverag:2,cq_command:0,cq_command_resp:0,cq_queri:0,cq_query_resp:[0,9],cq_sensor:0,cq_sensor_resp:0,cq_set:0,cq_settings_resp:0,creat:[0,2,3],creating_preset:0,creator:3,credit:[3,5],critic:8,cross:5,csi:0,csv:[7,8],curl:[6,7],current:[0,7,9],current_fov:9,current_time_m:0,custom:[0,8],data:[0,5],date:[0,2],datetim:0,debug:8,decemb:5,decim:0,decoupl:2,defin:[5,9],definit:9,delai:0,deleg:0,demo:[0,2,3,5,6,8,9],demonstr:7,depend:[0,3,9],deprec:[0,2],deprecated_40:0,deprecated_92:0,describ:9,desir:[0,9],detail:[3,5,7,9],dev:6,develop:[0,2,3],devic:[0,9],diagnos:7,dict:[0,2,9],dictionari:0,did:2,differ:[2,9],dig_zoom_act:0,digit:[0,7,9],digital_zoom:0,direct:[0,9],directli:[0,9],directori:[3,6],disabl:[0,9],disconnect:[0,2,9],discov:[0,7,8,9],distribut:3,doc:[0,2,3],docstr:[2,3],document:[0,2,5,9],doe:[0,7],don:[6,9],done:[0,3,8,9],down:0,downlad_cancel_pend:0,download:[0,6,7],download_cancel_pend:0,download_fil:0,driver:2,drop:0,dump:8,durat:0,dure:[0,9],dynam:0,e:[0,2,7,9],each:[0,3,5,9],easier:3,edit:6,either:[6,7,9],els:[0,9],enabl:[0,7,8,9],enable_wifi:[0,9],enable_wifi_ap:0,encapsul:0,encod:[0,2,5,9],encoding_act:[0,9],end:[0,2,9],endian:0,endpoint:[0,9],energi:5,engag:0,enhanc:[3,4],enqueu:9,ensur:[0,2],ensure_initi:0,enter:[3,6],entir:9,entri:[0,2],entrypoint:2,enumresultgener:0,environ:[2,3,5],error:[0,2,8],errorcod:[0,9],establish:0,etc:[0,7],even:[3,8],event:0,everyth:0,exampl:[0,2,5,7,8,9],except:[0,2,9],exception_cb:0,exceptionhandl:0,exclus:0,execut:7,exercis:5,exhaust:0,exist:6,exit:[0,7,9],expand:9,explain:3,expos:[0,2],exposur:0,exposure_i:0,exposure_typ:0,exposure_x:0,ext_batt_level:0,ext_batt_pres:0,extend:0,extern:[0,7],extract:0,f:9,fail:0,failur:2,fall:3,fals:[0,9],far:0,featur:[0,7],featureid:0,februari:5,feedback:5,feel:3,fi:[0,2,5,7],field:0,fieldofview:0,fifo:0,file:[0,2,3,7,8],filenam:0,fill:0,find:0,finish:9,firmwar:0,first:[0,2,6,7,9],first_tim:0,firstli:9,fix:[2,5],flag:0,flake8:2,flatmod:0,flatmode_id:0,flatten:[0,5],flexibl:0,flicker:0,flow:0,follow:[3,9],forev:0,fork:3,form:0,format:[0,2,3],found:[0,7,9],fov:[0,9],fp:[0,9],fps_30:9,frame:0,framework:2,free:3,frequenc:0,friendli:0,fro:7,from:[0,2,3,5,7,8,9],fs:9,ftu:0,full:[0,9],functionwrapp:0,furthermor:8,futur:[5,9],g:0,gatt:0,get:[0,2,9],get_camera_set:[0,9],get_camera_st:[0,9],get_camera_status:[0,9],get_capabilities_nam:0,get_capabilities_v:0,get_capabilities_valu:[0,9],get_date_tim:0,get_gpmf_data:0,get_hardware_info:0,get_hw_info:0,get_media_info:0,get_media_list:[0,9],get_nam:0,get_open_gopro_api_vers:0,get_preset_statu:0,get_screennail:0,get_setting_nam:0,get_setting_v:[0,9],get_settings_json:0,get_status_v:0,get_telemetri:0,get_third_party_api_vers:0,get_thumbnail:0,get_upd:[0,9],get_valu:[0,9],get_webcam_statu:0,get_webcam_vers:0,get_wifi_password:0,get_wifi_ssid:0,getlogg:8,git:[3,6],github:[2,3,4,6,7],given:[0,3,7,9],global:[0,2],gopro0456:0,gopro:[1,2,3,6,7,8,9],goprobl:0,goproenum:0,goproenummeta:0,goproresp:[0,9],goprouuid:0,goprowifi:0,gp:0,gpmf:0,gps_stat:0,gracefulli:9,greater:3,greatli:3,group:0,guid:[5,6,8,9],guidelin:5,h:7,ha:[0,2,9],handl:[0,2,5],happen:8,hardwar:[0,9],have:[0,6,7,8,9],head:6,heartbeat:0,help:[3,7,8],helper:9,here:[0,3,4,5,8,9],hero8:0,high:[0,9],higher:[0,3],highlight:0,hilight:[0,2],hindsight:0,hint:9,home:0,hopefulli:1,housekeep:9,how:[0,3,7,8,9],howev:9,http:[0,2,3,6,7,9],hypersmooth:0,hypersmoothmod:0,i:[0,2,7,8,9],id:[0,2,9],ident:2,identif:9,identifi:[0,7,9],idl:0,implement:[0,2,5],importlib:2,improv:2,in_context_menu:0,includ:[0,3,5],inconsist:[2,7],increment:2,index:2,individu:[0,3,9],info:[0,8,9],inform:[0,3,5,7,8,9],infrastructur:2,initi:[0,9],inspect:[0,9],instal:[2,3,5,7],instanc:[0,9],instanti:[0,2],instead:[0,7,9],int_batt_p:[0,9],interact:[0,9],interfac:[2,5,7,9],intern:[0,9],internal_102:0,internal_103:0,internal_104:0,internal_105:0,internal_106:0,internal_111:0,internal_112:0,internal_114:0,internal_115:0,internal_116:0,internal_117:0,internal_118:0,internal_124:0,internal_125:0,internal_126:0,internal_129:0,internal_130:0,internal_131:0,internal_132:0,internal_133:0,internal_139:0,internal_13:0,internal_142:0,internal_144:0,internal_145:0,internal_146:0,internal_147:0,internal_148:0,internal_149:0,internal_14:0,internal_153:0,internal_154:0,internal_155:0,internal_156:0,internal_157:0,internal_158:0,internal_159:0,internal_160:0,internal_161:0,internal_163:0,internal_164:0,internal_165:0,internal_166:0,internal_167:0,internal_168:0,internal_169:0,internal_19:0,internal_24:0,internal_30:0,internal_31:0,internal_32:0,internal_37:0,internal_41:0,internal_42:0,internal_43:0,internal_44:0,internal_45:0,internal_46:0,internal_47:0,internal_48:0,internal_54:0,internal_5:0,internal_60:0,internal_61:0,internal_62:0,internal_64:0,internal_65:0,internal_66:0,internal_67:0,internal_68:0,internal_69:0,internal_6:0,internal_75:0,internal_76:0,internal_79:0,internal_81:0,internal_82:0,internal_83:0,internal_84:0,internal_85:0,internal_86:0,internal_87:0,internal_88:0,internal_90:0,internal_96:0,interrupt:7,interv:[0,7],invalid:2,invalid_for_test:0,invalid_param:0,invalidconfigur:0,invalidopengoprovers:0,is_ble_connect:[0,9],is_ble_initi:9,is_busi:[0,9],is_encod:[0,9],is_ok:[0,9],is_pars:0,is_readi:9,is_receiv:0,is_wifi_connect:[0,9],isn:0,issu:[0,3,5,7,9],item:0,itemsview:0,iter:0,its:[0,9],januari:5,jekyl:2,join:9,jpg:[0,7],json:[0,9],june:5,just:[0,9],keep:[0,2,3,5,9],keep_al:0,kei:0,keyboard:7,keysview:0,keyword:0,kilobyt:0,know:0,known:5,kwarg:0,kwd:0,l:7,last:[0,7,9],last_hilight:0,launch:7,lcd:0,lcd_lock_act:0,lead:5,least:9,led:0,len:[0,2],length:2,let:[0,9],level:[0,5,7,8,9],lib:0,librari:5,like:[0,9],line:[2,5,7,9],link:[0,2],lint:3,linux:[0,3],linux_core_act:0,list:[0,9],listen:0,live:[0,5],live_burst_rem:0,live_burst_tot:0,liveview:0,load:0,load_preset:0,load_preset_group:0,local:[0,3,7],local_fil:0,locat:[0,7],locate_act:0,lock:0,log:[0,2,5,7,9],log_batteri:7,logger:8,logs_readi:0,look:[3,9],loos:5,lot:[2,8,9],low:5,m:[8,9],mac:2,machin:[0,7],maco:[3,5],made:3,mai:5,main:[0,2,3,6],maintain:[0,7,9],maintain_bl:[0,9],maintain_st:0,mainten:[0,5],major:[0,2],make:[2,3],manag:[0,5,9],mandatori:0,mani:[0,9],manual:9,march:5,max:[0,2],max_lens_mod:0,maximum:8,maxlensmod:0,media:[0,9],media_format:0,media_list:9,media_mod_mic_stat:0,media_mod_stat:0,meet:[0,3],mention:9,menu:0,merg:2,messag:7,meta:0,metaclass:0,metadata:2,method:[0,6,9],microphon:0,might:3,millisecond:0,min:0,minimum:0,minor:[0,2],minut:0,miss:2,mobil:0,mobile_video:0,mod:0,mode:[0,2,6],mode_group:0,model:0,modifi:[0,3,6],modul:[0,5,8,9],more:[0,3,5,7,8,9],most:[0,6,9],mostli:[0,9],move:2,mp4:[0,7],ms:0,msec:0,multi:0,multi_count_down:0,multi_shot_field_of_view:0,multi_shot_fov:0,multipl:[2,3],multishot:0,must:9,my_log:8,mypi:2,naiv:9,name:[0,3,9],narrow:3,need:[0,3,5,7,8,9],never:0,next_pol:0,nice:9,non:2,none:[0,9],not_applic:0,notabl:2,note:[3,7,9],notif:[0,5,7],notifi:[0,7],notimplementederror:0,now:[0,9],nox:0,num_group_photo:0,num_group_video:0,num_hilight:0,num_total_photo:0,num_total_video:0,number:[0,7],o:7,object:[0,9],occur:[0,9],octob:5,off:[0,9],offici:3,offset:0,often:0,ok:0,ol:6,onc:[0,3,6,9],one:[0,2,9],onli:[0,2,7,9],open:[0,2,3,6,7,8],open_gopro:[0,2,8,9],opengopro:[0,3,6],oper:[0,3,5],option:[0,2,7,9],order:[0,2,5],orient:0,origin:3,os:[0,3,9],ota:0,ota_stat:0,other:[2,9],otherwis:[0,9],our:9,out:0,output:[0,7],over:0,overh:0,overridden:9,overview:5,own:[0,5],p:7,packag:[0,2,5,6,7,8,9],page:[2,4],pair:[0,7,9],pair_stat:0,pair_state2:0,pair_tim:0,pair_typ:0,param:[0,9],paramet:[2,5,7],pars:[0,2,9],parser:[0,2],parser_build:0,part:[0,3],parti:0,pass:[0,3,7,9],password:[0,2],path:[0,8],pathlib:8,pattern:[0,9],pc:0,peer:0,pend:0,per:[0,7],percent:0,percentag:0,perform:[0,2,9],performancemod:0,perhap:5,period:[0,2,5],photo:[0,2,5],photo_field_of_view:0,photo_fov:0,photo_preset:0,photofov:0,photos_rem:0,pip:[6,7],platform:[3,5],pleas:3,poe:3,poetri:[2,3],point:[0,2,7],poll:[0,7],posit:[0,7],possibl:[3,9],post:3,potenti:9,power:0,power_down:0,prefer:[0,6,9],present:0,preset:[0,9],preset_modifi:0,preset_modified_notif:0,presetgroup:0,presets_group:0,prevent:0,preview:[0,7],preview_en:0,previou:0,previous:9,primari:0,print:[0,9],probabl:9,problem:9,procedur:5,process:[0,6],producertyp:0,program:[0,2,9],progress:7,project:2,propag:0,properti:[0,9],propos:3,proprietari:0,protobuf:[0,2],protobuf_command:0,protobuf_queri:0,protobuf_set:0,provid:[0,5,8,9],provis:0,proxi:0,pull:5,push:[0,3,5],put:0,py:[0,2,7,8],pydocstyl:2,pyinstal:2,pylint:2,pypi:[2,6],python3:0,python:[0,3,4,6,8,9],queri:[0,9],querycmdid:[0,9],queue:9,quick:0,quick_captur:0,quickstart:[5,9],r:6,radio:0,rais:[0,9],raspberrypi:7,rate:0,rather:9,raw_packet:0,re:[3,9],read:[0,5,7,9],readabl:8,readi:[0,2,3,5],realli:0,receiv:[0,9],recent:[0,6],recommend:9,reconnect:[0,9],record:[0,7],record_tim:7,ref:6,refactor:2,refer:[0,5,9],referenc:9,reflect:0,reg_capabilities_upd:0,reg_setting_val_upd:0,reg_status_val_upd:0,regard:9,regist:[0,2,7,9],register_all_set:0,register_all_status:0,register_capability_upd:[0,9],register_for_all_set:[0,9],register_for_all_status:[0,9],register_preset_statu:0,register_value_upd:[0,9],register_xxx_upd:9,registerpresetstatu:0,reiter:9,relat:0,releas:[0,5],relev:[0,5,9],remain:[0,2],remot:0,remote_ctrl_conn:0,remote_ctrl_v:0,remov:[0,2],remove_photo_hilight:0,remove_video_hilight:0,repo:[2,3,6],report:5,repositori:6,reproduc:3,request:[0,5],requir:[2,5,6,9],res_1080:[0,9],res_2_7k:9,res_2_7k_4_3:9,res_4k:9,res_4k_4_3:9,res_5_3_k:9,res_5_k_4_3:9,resolut:[0,9],resourc:9,respect:0,respond:9,respons:[2,5],responsetyp:0,result:[0,7],retri:0,retriev:9,robust:2,rotat:0,rough:0,rst:3,run:[2,3,6,7,9],runner:0,rx:8,s:[0,2,3,5,7,9],s_camera_manag:0,s_control_queri:0,s_unknown:0,s_wifi_access_point:0,safe:0,same:[0,5],sampl:4,scan:[0,2,9],schedul:0,scheduled_captur:0,scheduled_preset:0,scope:3,screennail:0,script:5,sd_rating_check_error:0,sd_statu:0,sd_write_speed_error:0,sdcard:0,sdk:[4,9],sdk_wireless_camera_control:[0,3,6],search:4,sec_sd_stat:0,second:0,secondari:0,section:[0,7,8,9],see:[0,3,4,5,9],select:[0,5],semant:2,send:[0,2,3,5,7],sensor:0,sent:[0,2,9],separ:[0,9],septemb:5,sequenc:9,serial:[0,7,9],serializ:9,servic:0,services_as_csv:8,session:0,set:[2,3,5,7],set_camera_control:0,set_date_tim:0,set_digital_zoom:0,set_keep_al:0,set_pairing_complet:0,set_preset:[0,9],set_preset_group:0,set_shutt:[0,9],set_shutter_off:0,set_shutter_on:0,set_third_party_client_info:0,set_turbo_mod:0,set_wifi:0,setting_capability_push:0,setting_val_push:0,settingid:[0,9],settingvaluetyp:0,setup:[2,3],setup_log:8,sever:[7,9],share:0,shot:0,should:[0,2,3,6,8,9],shouldn:8,show:[0,5,7],shown:7,shutter:[0,9],signal:[0,5,9],similarli:9,simplifi:0,simultan:[0,2],sinc:[0,9],singl:[0,9],site:0,size:0,sleep:0,so:[0,2,7,9],some:[0,2,5,7,8,9],someon:1,sourc:[0,5,7],space:0,space_rem:0,spec:0,special:[0,5],specif:[0,2,5,9],specifi:[0,2,9],speed:0,sprinkl:8,ssid:[0,2,7],stabl:5,standard:8,standbi:0,start:[0,2],start_preview_stream:0,state:[0,9],statu:[2,5,9],status:[2,5],status_val_push:0,statusid:0,stdin:2,step:[5,9],stop:[0,9],stop_preview_stream:0,storag:0,store:[0,7,9],str:[0,9],stream:[0,2,5],streaming_supp:0,strength:0,string:[0,8,9],structur:5,submit:5,substitut:0,succeed:0,success:[0,9],successfulli:[0,7,9],succinct:9,sudo:2,sudo_password:0,suffici:0,suggest:[2,5],summari:0,superbank:0,support:[0,2,5,7,9],sur:5,sync:2,synchron:[0,5],system:[0,2,3,7],system_busi:0,system_hot:0,system_readi:0,t:[0,2,6,8,9],tag:[0,3,4],tag_hilight:0,take:[5,7,9],taken:0,target:[0,9],task:[0,3],tcamis:1,telemetri:0,temperatur:0,termin:6,test:[0,2,3,5,9],tf:0,than:[0,2,9],thei:[7,9],them:[0,9],themselv:0,therefor:9,thermal_mit_mod:0,thi:[0,2,5,6,7,8,9],thing:[8,9],third:0,thread:[0,2,9],through:[0,2,3,5,6,9],throughout:[8,9],thu:[7,9],thumbnail:0,ticket:4,tim:1,time:[0,2,7],timelaps:0,timelapse_preset:0,timelapse_rem:0,timeout:0,timewarp_speed_ramp:0,todo:0,toggl:0,too:0,top:[0,5,9],total:0,trace:8,track:[7,9],transfer:0,tripod:0,troubleshoot:[3,5,9],tupl:0,turbo:0,turbo_mod:0,turn:9,tutori:7,two:9,tx:8,txt:6,type:[2,5,9],ubuntu:[2,5,7],ugli:9,ui:0,union:0,uniqu:0,unit:[0,3],unknown:0,unless:9,unrecover:8,unreg_capabilities_upd:0,unreg_setting_val_upd:0,unreg_status_val_upd:0,unregist:[0,2,9],unregister_all_set:0,unregister_all_status:0,unregister_capability_upd:[0,9],unregister_for_all_set:[0,9],unregister_for_all_status:[0,9],unregister_preset_statu:0,unregister_value_upd:[0,9],unreleas:5,until:[0,2,7,9],unwieldi:9,up:[2,3,5],updat:[0,2,3,9],upgrad:2,upon:9,us:[0,2,3,5,7,8,9],usabl:2,usag:[0,5,7],usb:0,usb_connect:0,user:[0,5,9],util:8,uuid:[0,2,9],v:7,valid:9,valu:[0,5],valuesview:0,vari:[0,9],variou:[0,9],veri:[7,8],verif:[0,2],verifi:0,version:[0,2,3,5],via:[0,2,3,7,9],video:[0,2,5],video_field_of_view:[0,9],video_fov:[0,9],video_hindsight:0,video_low_temp:0,video_performance_mod:0,video_preset:0,video_progress:0,video_rem:0,videofov:0,view:[5,7],virtual:3,vlc:[2,7],w:7,wa:[0,2,9],wai:[0,3,9],wait:[0,2],want:[3,6,7],wap_csi_password:0,wap_password:0,wap_pow:0,wap_prov_stat:0,wap_scan_st:0,wap_scan_tim:0,wap_ssid:0,wap_stat:0,warn:8,warp:0,we:[0,9],web:3,webcam:0,welcom:[3,5],well:[7,9],were:2,weren:2,what:[0,9],when:[0,3,9],whenev:9,where:[0,2,6,7,9],whether:3,which:[0,7,9],whoever:3,why:9,wi:[0,2,5,7],wif:7,wifi:[2,5,9],wifi_bar:0,wifi_command:[0,9],wifi_interfac:[0,7,9],wifi_set:[0,9],wificommand:[0,9],wifiset:[0,9],window:[2,3,5],wireless:[0,5],wireless_band:0,wireless_en:0,without:[0,2,9],wlan_ssid:0,won:[0,8,9],work:[0,2,3,5,7,9],worri:9,would:3,wrap:0,wrapper:0,write:[0,5,7],written:0,wrote:2,x:[3,5,9],y:0,yai:9,ye:0,yet:[0,2,9],you:[3,5,6,7,8,9],your:[3,5,6,7,9],your_name_her:3,zip:6,zoom:0,zoom_encod:0},titles:["Interfaces","Credits","Changelog","Contributing","Future Work","Open GoPro Python SDK","Installation","QuickStart Guide","Troubleshooting","Usage"],titleterms:{"0":2,"1":2,"10":2,"11":2,"12":2,"15":2,"16":2,"2":2,"20":2,"2021":2,"2022":2,"22":2,"25":2,"26":2,"27":2,"28":2,"29":2,"3":2,"30":2,"4":2,"5":2,"6":2,"7":2,"8":2,"9":2,A:7,For:6,access:9,api:[0,9],april:2,argument:9,asynchron:9,august:2,base:0,batteri:7,ble:0,bluetooth:8,bluez:7,bug:3,camera:9,changelog:2,characterist:8,close:9,command:[0,9],consider:7,constant:0,content:5,contribut:3,contributor:1,credit:1,data:9,decemb:2,demo:7,develop:[1,5,6],document:3,featur:[3,5],februari:2,feedback:3,fix:3,flatten:9,from:6,futur:4,get:[3,5],gopro:[0,5],guid:7,guidelin:3,handl:9,implement:3,instal:6,interfac:0,issu:4,januari:2,june:2,known:4,lead:1,log:8,mai:2,march:2,notif:9,octob:2,open:[5,9],oper:9,overview:9,paramet:[0,9],photo:7,pull:3,push:9,python:5,quickstart:7,readi:9,releas:6,report:3,request:3,requir:3,respons:[0,9],sdk:5,select:9,send:9,septemb:2,set:[0,9],sourc:6,special:7,stabl:6,start:[3,5],statu:0,status:[0,9],step:3,stream:7,structur:9,submit:3,summari:5,synchron:9,troubleshoot:8,type:[0,3],unreleas:2,usag:9,valu:9,version:9,video:7,wifi:[0,7],work:4,write:3,x:2}})