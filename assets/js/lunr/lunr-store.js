var store = [
        {
            "title": "Bluetooth Low Energy (BLE) Specifications: ",
            "excerpt": "This page will provide links to each version of the Open GoPro Bluetooth Low Energy (BLE) specification, as well as an overview of the changes from the previous version. Click on an individual spec to see it's complete information including possible commands, settings, etc.  {% note Since the Open GoPro API varies based on the version, it is necessary to query the Open GoPro version using the Get Version command upon connection %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble#",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specifications: [Bluetooth Low Energy (BLE) Specification 2.0](ble_versions/ble_2_0.md)",
            "excerpt": "-   Hilights:     -   Capture media     -   Track camera state     -   Get media list and download files / metadata     -   Load / edit presets     -   Configure and use as webcam     -   Add / remove hilights -   Breaking changes:     -   Video Digital Lens setting parameter changes:         -   Narrow changed from 6 to 2     -   Photo Digital Lens setting parameter changes:         -   Wide changed from 22 to 101         -   Linear changed from 23 to 102         -   Narrow changed from 24 to 19         -   Max Superview changed from 25 to 100     -   Multishot Digital Lens parameter changes:         -   Wide changed from 2 to 101         -   Narrow changed from 24 to 19",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble#bluetooth-low-energy-ble-specification-2-0-ble-versions-ble-2-0-md",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specifications: [Bluetooth Low Energy (BLE) Specification 1.0](ble_versions/ble_1_0.md)",
            "excerpt": "-   Initial API",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble#bluetooth-low-energy-ble-specification-1-0-ble-versions-ble-1-0-md",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: ",
            "excerpt": "About This Page  This page describes the format, capabilities, and use of Bluetooth Low Energy (BLE) as it pertains to communicating with GoPro cameras. Messages are sent using either TLV or Protobuf format.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: General",
            "excerpt": "Communicating with a GoPro camera via Bluetooth Low Energy involves writing to Bluetooth characteristics and, typically, waiting for a response notification from a corresponding characteristic.  The camera organizes its Generic Attribute Profile (GATT) table by broad features: AP control, network management,  control & query, etc.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#general",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Supported Cameras",
            "excerpt": "Below is a table of cameras that support GoPro's public BLE API:                   ID       Model       Marketing Name       Minimal Firmware Version                 55       HD9.01       HERO9 Black       v1.60",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#supported-cameras",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Services and Characteristics",
            "excerpt": "Note: GP-XXXX is shorthand for GoPro's 128-bit UUIDs: b5f9xxxx-aa8d-11e3-9046-0002a5d5c51b                   Service UUID       Service       Characteristic UUID       Description       Permissions                 GP-0001       GoPro WiFi Access Point       GP-0002       WiFi AP SSID       Read / Write                 GP-0003       WiFi AP Password       Read / Write                 GP-0004       WiFi AP Power       Write                 GP-0005       WiFi AP State       Read / Notify                 FEA6       Control & Query       GP-0072       Command       Write                 GP-0073       Command Response       Notify                 GP-0074       Settings       Write                 GP-0075       Settings Response       Notify                 GP-0076       Query       Write                 GP-0077       Query Response       Notify",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#services-and-characteristics",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Packet Headers",
            "excerpt": "The Bluetooth Low Energy protocol limits messages to 20 Bytes per packet. To accommodate this limitation, the packet header rules below are used. All lengths are in bytes. The packet count starts at 0 for the first continuation packet.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#packet-headers",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Packet Header Format",
            "excerpt": "Byte 1         Byte 2 (optional)         Byte 3 (optional)                   7         6         5         4         3         2         1         0         7         6         5         4         3         2         1         0         7         6         5         4         3         2         1         0                   0: Start         00: General         Message Length: 5 bits                            0: Start         01: Extended (13-bit)         Message Length: 13 bits                            0: Start         10: Extended (16-bit)                  Message Length: 16 bits                   0: Start         11: Reserved                            1: Continuation",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#packet-header-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Advertisements",
            "excerpt": "The camera will send BLE advertisements while it is ON and for the first 8 hours after the camera is put to sleep. During this time, the camera is discoverable and can be connected to. If the camera is in sleep mode, connecting to it will cause the camera to wake and boot up.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#advertisements",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Pairing",
            "excerpt": "In order to communicate with a GoPro camera via BLE, a client must first be paired with the camera. The pairing procedure must be done once for each new client. If the camera is factory reset, all clients will need to pair again. To pair with the camera, use the UI to put it into pairing mode, connect via BLE and then initiate pairing. The camera will whitelist the client so subsequent connections do not require pairing.                   Camera       To Enter Pairing Mode                 HERO9 Black       Swipe down, swipe left >> Connections >> Connect Device >> GoPro App",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#pairing",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Steps",
            "excerpt": "Discovery of and connection to the GoPro camera can be done as follows:     Put the camera into pairing mode Scan to discover peripherals (which can be narrowed by limiting to peripherals that advertise service FEA6) Connect to the peripheral Finish pairing with the peripheral Discover all advertised services and characteristics Subscribe to notifications from all characteristics that have the notify flag set",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#steps",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Sending and Receiving Messages",
            "excerpt": "In order to enable two-way communication with a GoPro camera, clients must connect to the camera and subscribe to characteristics that have the notify flag set. Messages are sent to the camera by writing to a write-enabled UUID and then waiting for a notification from the corresponding response UUID. Response notifications indicate whether the message was valid and will be (asynchronously) processed. For example, to send a camera control command, a client should write to GP-0072 and then wait for a response notification from GP-0073.     Depending on the camera's state, it may not be ready to accept some commands. This ready state is dependent on the System Busy and the Encoding Active status flags. For example:     System Busy flag is set while loading presets, changing settings, formatting sdcard, ... Encoding Active flag is set while capturing photo/video media    If the system is not ready, it should reject an incoming command; however, best practice is to always wait for the System Busy and Encode Active flags to go down before sending messages other than get status/setting queries.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#sending-and-receiving-messages",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Keep Alive",
            "excerpt": "Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera, as below. It is recommended to send a keep-alive at least once every 120 seconds.                   UUID       Write       Response UUID       Response                 GP-0074       03:5B:01:42       GP-0075       02:5B:00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#keep-alive",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Turbo Transfer",
            "excerpt": "Some cameras support Turbo Transfer mode, which allows media to be downloaded over WiFi more rapidly. This special mode should only be used during media offload. It is recommended that the user check for and--if necessary--disable Turbo Transfer on connect. For details on which cameras are supported and how to enable and disable Turbo Transfer, see Protobuf Commands.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#turbo-transfer",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: HERO9 Black",
            "excerpt": "The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#hero9-black",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: General",
            "excerpt": "Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera. It is recommended to send a keep-alive at least once every 120 seconds. In general, querying the value for a setting that is not associated with the current preset/flatmode results in an undefined value. For example, the user should not try to query the current Photo Digital Lenses (FOV) value while in Standard preset (Video flatmode).",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#general",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: TLV",
            "excerpt": "GoPro's BLE protocol comes in two flavors: TLV (Type Length Value) and Protobuf. This section describes TLV style messaging.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#tlv",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Commands",
            "excerpt": "The table below contains command IDs supported by Open GoPro. Command messages are sent to GP-0072 and responses/notifications are received on GP-0073.                   Command ID       Description                 0x01       Set shutter                 0x05       Sleep                 0x17       AP Control                 0x3C       Get Hardware Info                 0x3E       Presets: Load Group                 0x40       Presets: Load                 0x50       Analytics                 0x51       Open GoPro",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#commands",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Command Format",
            "excerpt": "Header/Length       Command ID       Parameter Length       Parameter Value                 1-2 bytes       1 byte       1 byte       Variable length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#command-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Command Response",
            "excerpt": "The GoPro camera sends responses to most commands received, indicating whether the command was valid and will be  processed or not.     Unless indicated otherwise in the Quick Reference table below, command responses use the format below.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#command-response",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Command Response Format",
            "excerpt": "Header/Length       Command ID       Response Code       Response                 1-2 bytes       1 byte       1 byte       Variable length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#command-response-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Command Response Error Codes",
            "excerpt": "Error Code       Description                 0       Success                 1       Error                 2       Invalid Parameter                 3..255       Reserved",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#command-response-error-codes",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Commands Quick Reference",
            "excerpt": "Below is a table of commands that can be sent to the camera and how to send them.                    ID       Command       Description       Request       Response       HERO9 Black                 0x01       Set shutter       Shutter: on       03:01:01:01       02:01:00       Y                 0x01       Set shutter       Shutter: off       03:01:01:00       02:01:00       Y                 0x05       Sleep       Put camera to sleep       01:05       02:05:00       Y                 0x17       AP Control       WiFi AP: on       03:17:01:01       02:17:00       Y                 0x17       AP Control       WiFi AP: off       03:17:01:00       02:17:00       Y                 0x3C       Get Hardware Info       Get camera hardware info       01:3C       Complex       Y                 0x3E       Presets: Load Group       Video       04:3E:02:03:E8       02:3E:00       Y                 0x3E       Presets: Load Group       Photo       04:3E:02:03:E9       02:3E:00       Y                 0x3E       Presets: Load Group       Timelapse       04:3E:02:03:EA       02:3E:00       Y                 0x40       Presets: Load       Activity       06:40:04:00:00:00:01       02:40:00       Y                 0x40       Presets: Load       Burst Photo       06:40:04:00:01:00:02       02:40:00       Y                 0x40       Presets: Load       Cinematic       06:40:04:00:00:00:02       02:40:00       Y                 0x40       Presets: Load       Live Burst       06:40:04:00:01:00:01       02:40:00       Y                 0x40       Presets: Load       Night Photo       06:40:04:00:01:00:03       02:40:00       Y                 0x40       Presets: Load       Night Lapse       06:40:04:00:02:00:02       02:40:00       Y                 0x40       Presets: Load       Photo       06:40:04:00:01:00:00       02:40:00       Y                 0x40       Presets: Load       Slo-Mo       06:40:04:00:00:00:03       02:40:00       Y                 0x40       Presets: Load       Standard       06:40:04:00:00:00:00       02:40:00       Y                 0x40       Presets: Load       Time Lapse       06:40:04:00:02:00:01       02:40:00       Y                 0x40       Presets: Load       Time Warp       06:40:04:00:02:00:00       02:40:00       Y                 0x40       Presets: Load       Max Photo       06:40:04:00:04:00:00       02:40:00       Y                 0x40       Presets: Load       Max Timewarp       06:40:04:00:05:00:00       02:40:00       Y                 0x40       Presets: Load       Max Video       06:40:04:00:03:00:00       02:40:00       Y                 0x50       Analytics       Set third party client       01:50       02:50:00       Y                 0x51       Open GoPro       Get version       01:51       Complex       Y",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#commands-quick-reference",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Complex Command Responses",
            "excerpt": "Below are clarifications for complex camera responses",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#complex-command-responses",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Get Hardware Info",
            "excerpt": "Response Packet       Response Byte(s)       Description                 1       20       Start packet                 51       Packet length                 3C:00       Command 3C sent successfully                 04       Length of model number                 00:00:00:13       Model number                 0B       Length of model name                 48:45:52:4F:58:20:42:6C:61:63       \"HEROX Blac\"                 2       80       Continuation packet                 6B       \"k\"                 04       Length of board type                 30:78:30:35       \"0x05\"                 0F       Length of firmware version                 48:44:58:2E:58:58:2E:58:58:2E:58:58       \"HDX.XX.XX.XX\"                 3       81       Continuation packet (1)                 2E:58:58       \".XX\"                 0E       Length of serial number                 58:58:58:58:58:58:58:58:58:58:58:58:58:58       \"XXXXXXXXXXXXXX\"                 0A       Length of AP SSID                 4       82       Continuation packet (2)                 47:50:32:34:35:30:58:58:58:58       \"GP2450XXXX\"                 0C       AP MAC Address length                 58:58:58:58:58:58:58:58       \"XXXXXXXX\"                 5       83       Continuation packet (3)                 58:58:58:58       \"XXXX\"",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#get-hardware-info",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Open GoPro Version",
            "excerpt": "Given the response 06:51:00:01:01:01:00, the Open GoPro version is v1.0.                  Response Byte(s)       Description                 06       Packet length                 51       Command ID                 00       Status (OK)                 01       Length of major version                 01       Major version: 1                 01       Length of minor version                 00       Minor version: 0",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#open-gopro-version",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Settings",
            "excerpt": "GoPro settings can be configured using the GP-Settings (GP-0074) UUID. Setting status is returned on GP-Settings-Status (GP-0075) UUID.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#settings",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Settings Request Format",
            "excerpt": "This will configure a setting on the camera. Only one setting may be sent on a packet (GATT notify or write-no-response), although multiple packets may be sent back-to-back.                  Request Length       Setting ID       Setting Value Length       Setting Value                 1-2 bytes       1 byte       1 byte       (variable length)",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#settings-request-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Settings Response Format",
            "excerpt": "Response Length       Setting ID       Response Code                 1 byte       1 byte       1 byte",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#settings-response-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Settings Quick Reference",
            "excerpt": "All settings are sent to UUID GP-0074. All values are hexadecimal and length are in bytes.                   Setting ID       Setting       Option       Request       Response       HERO9 Black                 2       Resolution       Set video resolution (id: 2) to 4k (value: 1)       03:02:01:01       02:02:00       Y                 2       Resolution       Set video resolution (id: 2) to 2.7k (value: 4)       03:02:01:04       02:02:00       Y                 2       Resolution       Set video resolution (id: 2) to 2.7k 4:3 (value: 6)       03:02:01:06       02:02:00       Y                 2       Resolution       Set video resolution (id: 2) to 1440 (value: 7)       03:02:01:07       02:02:00       Y                 2       Resolution       Set video resolution (id: 2) to 1080 (value: 9)       03:02:01:09       02:02:00       Y                 2       Resolution       Set video resolution (id: 2) to 4k 4:3 (value: 18)       03:02:01:12       02:02:00       Y                 2       Resolution       Set video resolution (id: 2) to 5k (value: 24)       03:02:01:18       02:02:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 240 (value: 0)       03:03:01:00       02:03:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 120 (value: 1)       03:03:01:01       02:03:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 100 (value: 2)       03:03:01:02       02:03:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 60 (value: 5)       03:03:01:05       02:03:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 50 (value: 6)       03:03:01:06       02:03:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 30 (value: 8)       03:03:01:08       02:03:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 25 (value: 9)       03:03:01:09       02:03:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 24 (value: 10)       03:03:01:0A       02:03:00       Y                 3       Frames Per Second       Set video fps (id: 3) to 200 (value: 13)       03:03:01:0D       02:03:00       Y                 59       Auto Off       Set setup auto power down (id: 59) to never (value: 0)       03:3B:01:00       01:3B:00       Y                 59       Auto Off       Set setup auto power down (id: 59) to 5 min (value: 4)       03:3B:01:04       01:3B:00       Y                 59       Auto Off       Set setup auto power down (id: 59) to 15 min (value: 6)       03:3B:01:06       01:3B:00       Y                 59       Auto Off       Set setup auto power down (id: 59) to 30 min (value: 7)       03:3B:01:07       01:3B:00       Y                 121       Lens       Set video digital lenses (id: 121) to wide (value: 0)       03:79:01:00       02:79:00       Y                 121       Lens       Set video digital lenses (id: 121) to narrow (value: 6)       03:79:01:06       02:79:00       Y                 121       Lens       Set video digital lenses (id: 121) to superview (value: 3)       03:79:01:03       02:79:00       Y                 121       Lens       Set video digital lenses (id: 121) to linear (value: 4)       03:79:01:04       02:79:00       Y                 121       Lens       Set video digital lenses (id: 121) to max superview (value: 7)       03:79:01:07       02:79:00       Y                 121       Lens       Set video digital lenses (id: 121) to linear + horizon leveling (value: 8)       03:79:01:08       02:79:00       Y                 122       Lens       Set photo digital lenses (id: 122) to narrow (value: 24)       03:7A:01:18       02:7A:00       Y                 122       Lens       Set photo digital lenses (id: 122) to max superview (value: 25)       03:7A:01:19       02:7A:00       Y                 122       Lens       Set photo digital lenses (id: 122) to wide (value: 22)       03:7A:01:16       02:7A:00       Y                 122       Lens       Set photo digital lenses (id: 122) to linear (value: 23)       03:7A:01:17       02:7A:00       Y                 123       Lens       Set multi shot digital lenses (id: 123) to narrow (value: 24)       03:7B:01:18       02:7B:00       Y                 123       Lens       Set multi shot digital lenses (id: 123) to wide (value: 22)       03:7B:01:16       02:7B:00       Y                 123       Lens       Set multi shot digital lenses (id: 123) to linear (value: 23)       03:7B:01:17       02:7B:00       Y                 162       Max Lens Mod Enable       Set mods max lens enable (id: 162) to off (value: 0)       03:A2:01:00       02:A2:00       Y                 162       Max Lens Mod Enable       Set mods max lens enable (id: 162) to on (value: 1)       03:A2:01:01       02:A2:00       Y",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#settings-quick-reference",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Camera Capabilities",
            "excerpt": "Below are tables detailing supported features for Open GoPro cameras.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#camera-capabilities",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: HERO9 Black",
            "excerpt": "Resolution       Anti-Flicker       Frames Per Second       Lens                 1080       50Hz       24       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 50       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 100       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 200       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 60       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 120       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 240       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 1440       50Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 50       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 100       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 120       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 2.7K       50Hz       50       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 100       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       60       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 120       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 2.7K 4:3       50Hz       50       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       60       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 4K       50Hz       24       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 50       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 60       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 4K 4:3       50Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 5K       50Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Linear                 Narrow                 Linear + Horizon Leveling",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#hero9-black",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Query",
            "excerpt": "The camera provides two basic types of state information: Camera status and settings. Camera status info includes information such as the current preset/mode, whether the system is encoding, remaining sdcard space, the date, etc. Settings info gives the currently selected option for each setting; for example, this includes the current video resolution, frame rate, digital lens (FOV), etc.     Queries are sent to to GP-0076 and responses are received on GP-0077. All packets sent and received are in Big Endian.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#query",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Query Format",
            "excerpt": "Header/Length       Query Command ID       Array of IDs                 1-2 bytes       1 byte       Variable Length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#query-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Query Commands",
            "excerpt": "All query commands are sent to GP-0076. Responses are received on GP-0077.    Note: omitting :xx:... from (un)register query commands will result in being (un)registered for all possible updates                  Query ID       Query       Request       Notes                 0x12       Get setting value       02:12:xx       xx -> Setting ID                 0x12       Get all setting values       01:12                        0x13       Get status value       02:13:xx       xx -> status code                 0x13       Get all status values       01:13                        0x52       Register for setting updates       nn:52:xx:...       nn -> message lengthxx -> setting id                 0x53       Register for status updates       nn:53:xx:...       nn -> message lengthxx -> status code                 0x72       Unregister for setting updates       nn:72:xx:...       nn -> message lengthxx -> setting id                 0x73       Unregister for status updates       nn:73:xx:...       nn -> message lengthxx -> status code",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#query-commands",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Query Response Format",
            "excerpt": "Query responses are pushed asynchronously in the following scenarios:     The user queries for current status/settings The user registers for settings/status updates The user is registered to receive updates for a status/setting and the value changes                  Message Length       Query ID       Command Status       Status ID       Status Value Length       Status Value                 1-2 bytes       1 byte       1 byte       1 byte       1 byte       1-255 bytes",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#query-response-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Multi-Value Responses",
            "excerpt": "When querying for or receiving a push notifications about more than one setting/status, the Status ID, Status Value Length, and Status Value fields become collectively repeatable.     Example:      [MESSAGE LENGTH]:[QUERY ID]:[COMMAND STATUS]:[ID1]:[LENGTH1]:[VALUE1]:[ID2]:[LENGTH2]:[VALUE2]:...",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#multi-value-responses",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Push Notification Responses",
            "excerpt": "The Query ID for settings/status push notifications replaces the upper 4 bits with 1001 (nine).    For example, if the original query comand ID was 0x52, the query ID of the push notification will be 0x92.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#push-notification-responses",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Status Codes",
            "excerpt": "Below is a table of all possible camera status codes.                  Status ID       Name       Description       Type       Values                 1       Internal battery present       Is the system's internal battery present?       boolean       0: False 1: True                  2       Internal battery level       Rough approximation of internal battery level in bars       integer       0: Zero 1: One 2: Two 3: Three                  3       External battery present       Is an external battery connected?       boolean       0: False 1: True                  4       External battery level       External battery power level in percent       percent       0-100                 5       Unused       Unused       None                        6       System hot       Is the system currently overheating?       boolean       0: False 1: True                  7       Unused       Unused       None                        8       System busy       Is the camera busy?       boolean       0: False 1: True                  9       Quick capture active       Is Quick Capture feature enabled?       boolean       0: False 1: True                  10       Encoding active       Is the system encoding right now?       boolean       0: False 1: True                  11       Lcd lock active       Is LCD lock active?       boolean       0: False 1: True                  12       Unused       Unused       None                        13       Video progress counter       When encoding video, this is the duration (seconds) of the video so far; 0 otherwise       integer       *                 17       Enable       Are Wireless Connections enabled?       boolean       0: False 1: True                  18       Unused       Unused              *                 19       State       The pairing state of the camera       integer       0: Success 1: In Progress 2: Failed 3: Stopped                  20       Type       The last type of pairing that the camera was engaged in       integer       0: Not Pairing 1: Pairing App 2: Pairing Remote Control 3: Pairing Bluetooth Device                  21       Pair time       Time (milliseconds) since boot of last successful pairing complete action       integer       *                 22       State       State of current scan for WiFi Access Points. Appears to only change for CAH-related scans       integer       0: Never started 1: Started 2: Aborted 3: Canceled 4: Completed                  23       Scan time msec       The time, in milliseconds since boot that the WiFi Access Point scan completed       integer       *                 24       Provision status       WiFi AP provisioning state       integer       0: Never started 1: Started 2: Aborted 3: Canceled 4: Completed                  25       Unused       Unused       None                        26       Remote control version       Wireless remote control version       integer       *                 27       Remote control connected       Is a wireless remote control connected?       boolean       0: False 1: True                  28       Pairing       Wireless Pairing State       integer       *                 29       Wlan ssid       Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int       string       *                 30       Ap ssid       Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int       string       *                 31       App count       The number of wireless devices connected to the camera       integer       *                 32       Enable       Is Preview Stream enabled?       boolean       0: False 1: True                  33       Sd status       Primary Storage Status       integer       -1: Unknown 0: OK 1: SD Card Full 2: SD Card Removed 3: SD Card Format Error 4: SD Card Busy 8: SD Card Swapped                  34       Remaining photos       How many photos can be taken before sdcard is full       integer       *                 35       Remaining video time       How many minutes of video can be captured with current settings before sdcard is full       integer       *                 36       Num group photos       How many group photos can be taken with current settings before sdcard is full       integer       *                 37       Num group videos       Total number of group videos on sdcard       integer       *                 38       Num total photos       Total number of photos on sdcard       integer       *                 39       Num total videos       Total number of videos on sdcard       integer       *                 40       Date time       Current date/time (format: %YY%MM%DD%HH%MM%SS, all values in hex)       string       *                 41       Ota status       The current status of Over The Air (OTA) update       integer       0: Idle 1: Downloading 2: Verifying 3: Download Failed 4: Verify Failed 5: Ready 6: GoPro App: Downloading 7: GoPro App: Verifying 8: GoPro App: Download Failed 9: GoPro App: Verify Failed 10: GoPro App: Ready                  42       Download cancel request pending       Is there a pending request to cancel a firmware update download?       boolean       0: False 1: True                  45       Camera locate active       Is locate camera feature active?       boolean       0: False 1: True                  49       Multi shot count down       The current timelapse interval countdown value (e.g. 5...4...3...2...1...)       integer       *                 50       Unused       Unused       None                        51       Unused       Unused       None                        52       Unused       Unused       None                        53       Unused       Unused       None                        54       Remaining space       Remaining space on the sdcard in Kilobytes       integer       *                 55       Supported       Is preview stream supported in current recording/flatmode/secondary-stream?       boolean       0: False 1: True                  56       Wifi bars       WiFi signal strength in bars       integer       *                 57       Current time msec       System time in milliseconds since system was booted       integer       *                 58       Num hilights       The number of hilights in encoding video (set to 0 when encoding stops)       integer       *                 59       Last hilight time msec       Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)       integer       *                 60       Next poll msec       The min time between camera status updates (msec). Do not poll for status more often than this       integer       *                 63       In contextual menu       Is the camera currently in a contextual menu (e.g. Preferences)?       boolean       0: False 1: True                  64       Remaining timelapse time       How many min of Timelapse video can be captured with current settings before sdcard is full       integer       *                 65       Exposure select type       Liveview Exposure Select Mode       integer       0: Disabled 1: Auto 2: ISO Lock 3: Hemisphere                  66       Exposure select x       Liveview Exposure Select: y-coordinate (percent)       percent       0-100                 67       Exposure select y       Liveview Exposure Select: y-coordinate (percent)       percent       0-100                 68       Gps status       Does the camera currently have a GPS lock?       boolean       0: False 1: True                  69       Ap state       Is the WiFi radio enabled?       boolean       0: False 1: True                  70       Internal battery percentage       Internal battery level (percent)       percent       0-100                 74       Acc mic status       Microphone Accesstory status       integer       0: Microphone mod not connected 1: Microphone mod connected 2: Microphone mod connected and microphone plugged into Microphone mod                  75       Digital zoom       Digital Zoom level (percent)       percent       0-100                 76       Wireless band       Wireless Band       integer       0: 2.4 GHz 1: 5 GHz 2: Max                  77       Digital zoom active       Is Digital Zoom feature available?       boolean       0: False 1: True                  78       Mobile friendly video       Are current video settings mobile friendly? (related to video compression and frame rate)       boolean       0: False 1: True                  79       First time use       Is the camera currently in First Time Use (FTU) UI flow?       boolean       0: False 1: True                  81       Band 5ghz avail       Is 5GHz wireless band available?       boolean       0: False 1: True                  82       System ready       Is the system ready to accept commands?       boolean       0: False 1: True                  83       Batt okay for ota       Is the internal battery charged sufficiently to start Over The Air (OTA) update?       boolean       0: False 1: True                  85       Video low temp alert       Is the camera getting too cold to continue recording?       boolean       0: False 1: True                  86       Actual orientation       The rotational orientation of the camera       integer       0: 0 degrees (upright) 1: 180 degrees (upside down) 2: 90 degrees (laying on right side) 3: 270 degrees (laying on left side)                  87       Thermal mitigation mode       Can camera use high resolution/fps (based on temperature)? (HERO7 Silver/White only)       boolean       0: False 1: True                  88       Zoom while encoding       Is this camera capable of zooming while encoding (static value based on model, not settings)       boolean       0: False 1: True                  89       Current mode       Current flatmode ID       integer       *                 91       Logs ready       Are system logs ready to be downloaded?       boolean       0: False 1: True                  92       Timewarp 1x active       Is Timewarp 1x active?       boolean       0: False 1: True                  93       Active video presets       Current Video Preset (ID)       integer       *                 94       Active photo presets       Current Photo Preset (ID)       integer       *                 95       Active timelapse presets       Current Timelapse Preset (ID)       integer       *                 96       Active presets group       Current Preset Group (ID)       integer       *                 97       Active preset       Current Preset (ID)       integer       *                 98       Preset modified       Preset Modified Status, which contains an event ID and a preset (group) ID       integer       *                 99       Remaining live bursts       How many Live Bursts can be captured before sdcard is full       integer       *                 100       Num total live bursts       Total number of Live Bursts on sdcard       integer       *                 101       Capture delay active       Is Capture Delay currently active (i.e. counting down)?       boolean       0: False 1: True                  102       Media mod mic status       Media mod State       integer       0: Media mod microphone removed 2: Media mod microphone only 3: Media mod microphone with external microphone                  103       Timewarp speed ramp active       Time Warp Speed       integer       0: 15x 1: 30x 2: 60x 3: 150x 4: 300x 5: 900x 6: 1800x 7: 2x 8: 5x 9: 10x 10: Auto 11: 1x (realtime) 12: 1/2x (slow-motion)                  104       Linux core active       Is the system's Linux core active?       boolean       0: False 1: True                  105       Camera lens type       Camera lens type (reflects changes to setting 162)       integer       0: Default 1: Max Lens                  106       Video hindsight capture active       Is Video Hindsight Capture Active?       boolean       0: False 1: True                  107       Scheduled preset       Scheduled Capture Preset ID       integer       *                 108       Scheduled enabled       Is Scheduled Capture set?       boolean       0: False 1: True                  109       Creating preset       Is the camera in the process of creating a custom preset?       boolean       0: False 1: True                  110       Media mod status       Media Mode Status (bitmasked)       integer       0: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: False 1: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: True 2: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: False 3: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: True 4: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: False 5: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: True 6: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: False 7: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: True                  113       Turbo transfer       Is Turbo Transfer active?       boolean       0: False 1: True",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#status-codes",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Protobuf",
            "excerpt": "In order to maximize BLE bandwidth, some complex messages are sent using Google Protobuf (Protocol Buffers).",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#protobuf",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Protobuf Message Format",
            "excerpt": "Protobuf communications with the camera differ from TLV-style communications. Rather than having a Type, Length, and Value, protobuf messages sent to a GoPro device have a Command Type (called a Feature), a Sub-command Type (called an Action) and a Value (serialization of a protobuf object).     Note: For commands that do not require any protobuf inputs, Value would be empty (0 bytes).                   Message Length       Feature ID       Action ID       Protobuf Bytestream                 1-2 bytes       1 byte       1 byte       Variable Length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#protobuf-message-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Protobuf Commands",
            "excerpt": "Open GoPro supports the following protobuf commands:                 Feature ID       Action ID       Description       Request       Response                 0xF1       0x6B       Request set turbo active       RequestSetTurboActive       ResponseGeneric                 0xF5       0x72       Request get preset status       RequestGetPresetStatus       NotifyPresetStatus",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#protobuf-commands",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: Protobuf Command Details",
            "excerpt": "Below are additional details about specific protobuf commands:",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#protobuf-command-details",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: RequestSetTurboActive",
            "excerpt": "Turbo Transfer Mode is a special feature that serves two purposes:  Temporarily modify low-level settings in the OS to prioritize WiFi offload speeds Put up a UI on the camera indicating that media is being transferred and preventing the user from inadvertently changing settings or capturing new media      Developers can query whether the camera is currently in Turbo Transfer Mode from camera status 113.     While in Turbo Transfer Mode, if the user presses the Mode/Power or Shutter buttons on the camera, Turbo Transfer Mode will be deactivated.     Some cameras are already optimized for WiFi transfer and do not gain additional speed from this feature.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#requestsetturboactive",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v1.0: RequestGetPresetStatus",
            "excerpt": "This command is used to get information about what Preset Groups and Presets the camera supports in its current state. Each Preset Group contains an ID, whether additional presets can be added, and an array of existing Presets. Each Preset contains information about its ID, associated flatmode, title, icon, whether it's a user-defined preset, whether the preset has been modified from its factory-default state (for factory-default presets only) and a list of  settings associated with the Preset.     Preset Status should not be confused with camera status, which contains hundreds of camera/setting statuses on a system level.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_1_0#requestgetpresetstatus",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: ",
            "excerpt": "About This Page  This page describes the format, capabilities, and use of Bluetooth Low Energy (BLE) as it pertains to communicating with GoPro cameras. Messages are sent using either TLV or Protobuf format.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: General",
            "excerpt": "Communicating with a GoPro camera via Bluetooth Low Energy involves writing to Bluetooth characteristics and, typically, waiting for a response notification from a corresponding characteristic.  The camera organizes its Generic Attribute Profile (GATT) table by broad features: AP control, control & query, etc.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#general",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Supported Cameras",
            "excerpt": "Below is a table of cameras that support GoPro's public BLE API:                   ID       Model       Marketing Name       Minimal Firmware Version                 57       H21.01       HERO10 Black       v01.10.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#supported-cameras",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Services and Characteristics",
            "excerpt": "Note: GP-XXXX is shorthand for GoPro's 128-bit UUIDs: b5f9xxxx-aa8d-11e3-9046-0002a5d5c51b                   Service UUID       Service       Characteristic UUID       Description       Permissions                 GP-0001       GoPro WiFi Access Point       GP-0002       WiFi AP SSID       Read / Write                 GP-0003       WiFi AP Password       Read / Write                 GP-0004       WiFi AP Power       Write                 GP-0005       WiFi AP State       Read / Indicate                 FEA6       Control & Query       GP-0072       Command       Write                 GP-0073       Command Response       Notify                 GP-0074       Settings       Write                 GP-0075       Settings Response       Notify                 GP-0076       Query       Write                 GP-0077       Query Response       Notify",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#services-and-characteristics",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Packet Headers",
            "excerpt": "The Bluetooth Low Energy protocol limits messages to 20 Bytes per packet. To accommodate this limitation, the packet header rules below are used. All lengths are in bytes. The packet count starts at 0 for the first continuation packet.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#packet-headers",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Packet Header Format",
            "excerpt": "Byte 1         Byte 2 (optional)         Byte 3 (optional)                   7         6         5         4         3         2         1         0         7         6         5         4         3         2         1         0         7         6         5         4         3         2         1         0                   0: Start         00: General         Message Length: 5 bits                            0: Start         01: Extended (13-bit)         Message Length: 13 bits                            0: Start         10: Extended (16-bit)                  Message Length: 16 bits                   0: Start         11: Reserved                            1: Continuation",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#packet-header-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Advertisements",
            "excerpt": "The camera will send BLE advertisements while it is ON and for the first 8 hours after the camera is put to sleep. During this time, the camera is discoverable and can be connected to. If the camera is in sleep mode, connecting to it will cause the camera to wake and boot up.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#advertisements",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Pairing",
            "excerpt": "In order to communicate with a GoPro camera via BLE, a client must first be paired with the camera. The pairing procedure must be done once for each new client. If the camera is factory reset, all clients will need to pair again. To pair with the camera, use the UI to put it into pairing mode, connect via BLE and then initiate pairing. The camera will whitelist the client so subsequent connections do not require pairing.                   Camera       To Enter Pairing Mode                 HERO10 Black       Swipe down, swipe left >> Connections >> Connect Device >> GoPro Quik App",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#pairing",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Steps",
            "excerpt": "Discovery of and connection to the GoPro camera can be done as follows:     Put the camera into pairing mode Scan to discover peripherals (which can be narrowed by limiting to peripherals that advertise service FEA6) Connect to the peripheral Finish pairing with the peripheral Discover all advertised services and characteristics Subscribe to notifications from all characteristics that have the notify flag set",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#steps",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Sending and Receiving Messages",
            "excerpt": "In order to enable two-way communication with a GoPro camera, clients must connect to the camera and subscribe to characteristics that have the notify flag set. Messages are sent to the camera by writing to a write-enabled UUID and then waiting for a notification from the corresponding response UUID. Response notifications indicate whether the message was valid and will be (asynchronously) processed. For example, to send a camera control command, a client should write to GP-0072 and then wait for a response notification from GP-0073.     Depending on the camera's state, it may not be ready to accept specific commands. This ready state is dependent on the System Busy and the Encoding Active status flags. For example:     System Busy flag is set while loading presets, changing settings, formatting sdcard, ... Encoding Active flag is set while capturing photo/video media    If the system is not ready, it should reject an incoming command; however, best practice is to always wait for the System Busy and Encode Active flags to be unset before sending messages other than get status/setting queries.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#sending-and-receiving-messages",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Presets",
            "excerpt": "The camera organizes modes of operation into presets. A preset is a logical wrapper around a specific camera flatmode and a collection of settings that target different ways of capturing media.     The set of presets available to load at any moment depends on the value of certain camera settings, which are outlined in the table below.     For per-preset firmware compatibility information, see Commands Quick Reference.                   Setting       Preset       Preset ID                 Max Lens: OFF       Standard       0x00000000                           Activity       0x00000001                           Cinematic       0x00000002                           Ultra Slo-Mo       0x00000004                           Basic       0x00000005                           Photo       0x00010000                           Live Burst       0x00010001                           Burst Photo       0x00010002                           Night Photo       0x00010003                           Time Warp       0x00020000                           Time Lapse       0x00020001                           Night Lapse       0x00020002                           Max Lens: ON       Max Video       0x00030000                           Max Photo       0x00040000                           Max Timewarp       0x00050000                           Video Performance Mode: Maximum Video Performance       Standard       0x00000000                                     Activity       0x00000001                                     Cinematic       0x00000002                                     Ultra Slo-Mo       0x00000004                                     Basic       0x00000005                                     Photo       0x00010000                                     Live Burst       0x00010001                                     Burst Photo       0x00010002                                     Night Photo       0x00010003                                     Time Warp       0x00020000                                     Time Lapse       0x00020001                                     Night Lapse       0x00020002                                     Video Performance Mode: Extended Battery       Photo       0x00010000                                     Live Burst       0x00010001                                     Burst Photo       0x00010002                                     Night Photo       0x00010003                                     Time Warp       0x00020000                                     Time Lapse       0x00020001                                     Night Lapse       0x00020002                                     Standard [EB]       0x00080000                                     Activity [EB]       0x00080001                                     Cinematic [EB]       0x00080002                                     Slo-Mo [EB]       0x00080003                                     Video Performance Mode: Tripod / Stationary Video       Photo       0x00010000                                     Live Burst       0x00010001                                     Burst Photo       0x00010002                                     Night Photo       0x00010003                                     Time Warp       0x00020000                                     Time Lapse       0x00020001                                     Night Lapse       0x00020002                                     4K Tripod       0x00090000                                     5.3K Tripod       0x00090001",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#presets",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Keep Alive",
            "excerpt": "Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera, as below. It is recommended to send a keep-alive at least once every 120 seconds.                   UUID       Write       Response UUID       Response                 GP-0074       03:5B:01:42       GP-0075       02:5B:00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#keep-alive",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Turbo Transfer",
            "excerpt": "Some cameras support Turbo Transfer mode, which allows media to be downloaded over WiFi more rapidly. This special mode should only be used during media offload. It is recommended that the user check for and--if necessary--disable Turbo Transfer on connect. For details on which cameras are supported and how to enable and disable Turbo Transfer, see Protobuf Commands.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#turbo-transfer",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Global Behaviors",
            "excerpt": "In order to prevent undefined behavior between the camera and a connected app, simultaneous use of the camera and a connected app is discouraged.     Best practice for synchronizing user/app control is to use the Set Camera Control Status command and corresponding Camera Control Status (CCS) camera statuses in alignment with the finite state machine below:    ```plantuml!   ' Define states IDLE: Control Status: Idle CAMERA_CONTROL: Control Status: Camera Control EXTERNAL_CONTROL: Control Status: External Control  ' Define transitions [*]              ->      IDLE  IDLE             ->      IDLE: App sets CCS: Idle IDLE             -up->   CAMERA_CONTROL: User interacts with camera IDLE             -down-> EXTERNAL_CONTROL: App sets CCS: External Control  CAMERA_CONTROL   ->      CAMERA_CONTROL: User interacts with camera CAMERA_CONTROL   -down-> IDLE: User returns camera to idle screen\\nApp sets CCS: Idle  EXTERNAL_CONTROL ->    EXTERNAL_CONTROL: App sets CCS: External Control EXTERNAL_CONTROL -up-> IDLE: App sets CCS: Idle\\nUser interacts with camera EXTERNAL_CONTROL -up-> CAMERA_CONTROL: User interacts with camera     ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#global-behaviors",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: HERO10 Black",
            "excerpt": "The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#hero10-black",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: General",
            "excerpt": "Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera. It is recommended to send a keep-alive at least once every 120 seconds. In general, querying the value for a setting that is not associated with the current preset/flatmode results in an undefined value. For example, the user should not try to query the current Photo Digital Lenses (FOV) value while in Standard preset (Video flatmode). USB command and control is not supported on HERO9 Black.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#general",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: TLV",
            "excerpt": "GoPro's BLE protocol comes in two flavors: TLV (Type Length Value) and Protobuf. This section describes TLV style messaging.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#tlv",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Commands",
            "excerpt": "The table below contains command IDs supported by Open GoPro. Command messages are sent to GP-0072 and responses/notifications are received on GP-0073.                   Command ID       Description                 0x01       Set shutter                 0x05       Sleep                 0x0D       Set Date/Time                 0x0E       Get Date/Time                 0x17       AP Control                 0x3C       Get Hardware Info                 0x3E       Presets: Load Group                 0x40       Presets: Load                 0x50       Analytics                 0x51       Open GoPro",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#commands",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Command Format",
            "excerpt": "Header/Length       Command ID       Parameter Length       Parameter Value                 1-2 bytes       1 byte       1 byte       Variable length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#command-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Command Response",
            "excerpt": "The GoPro camera sends responses to most commands received, indicating whether the command was valid and will be  processed or not.     Unless indicated otherwise in the Quick Reference table below, command responses use the format below.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#command-response",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Command Response Format",
            "excerpt": "Header/Length       Command ID       Response Code       Response                 1-2 bytes       1 byte       1 byte       Variable length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#command-response-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Command Response Error Codes",
            "excerpt": "Error Code       Description                 0       Success                 1       Error                 2       Invalid Parameter                 3..255       Reserved",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#command-response-error-codes",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Commands Quick Reference",
            "excerpt": "Below is a table of commands that can be sent to the camera and how to send them.  ✔ Indicates support for all Open GoPro firmware versions.  ❌ Indicates a lack of support for all Open GoPro firmware versions.  >= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ                    ID       Command       Description       Request       Response       HERO10 Black                 0x01       Set shutter       Shutter: off       03:01:01:00       02:01:00       ✔                 0x01       Set shutter       Shutter: on       03:01:01:01       02:01:00       ✔                 0x05       Sleep       Put camera to sleep       01:05       02:05:00       ✔                 0x0D       Set Date/Time       Set date/time to 2022-01-02 03:04:05       09:0D:07:07:E6:01:02:03:04:05       02:0D:00       ✔                 0x0E       Get Date/Time       Get date/time       01:0E       Complex       ✔                 0x17       AP Control       WiFi AP: off       03:17:01:00       02:17:00       ✔                 0x17       AP Control       WiFi AP: on       03:17:01:01       02:17:00       ✔                 0x3C       Get Hardware Info       Get camera hardware info       01:3C       Complex       ✔                 0x3E       Presets: Load Group       Video       04:3E:02:03:E8       02:3E:00       ✔                 0x3E       Presets: Load Group       Photo       04:3E:02:03:E9       02:3E:00       ✔                 0x3E       Presets: Load Group       Timelapse       04:3E:02:03:EA       02:3E:00       ✔                 0x40       Presets: Load       Standard       06:40:04:00:00:00:00       02:40:00       ✔                 0x40       Presets: Load       Activity       06:40:04:00:00:00:01       02:40:00       ✔                 0x40       Presets: Load       Cinematic       06:40:04:00:00:00:02       02:40:00       ✔                 0x40       Presets: Load       Ultra Slo-Mo       06:40:04:00:00:00:04       02:40:00       \\&gt;= v01.16.00                 0x40       Presets: Load       Basic       06:40:04:00:00:00:05       02:40:00       \\&gt;= v01.16.00                 0x40       Presets: Load       Photo       06:40:04:00:01:00:00       02:40:00       ✔                 0x40       Presets: Load       Live Burst       06:40:04:00:01:00:01       02:40:00       ✔                 0x40       Presets: Load       Burst Photo       06:40:04:00:01:00:02       02:40:00       ✔                 0x40       Presets: Load       Night Photo       06:40:04:00:01:00:03       02:40:00       ✔                 0x40       Presets: Load       Time Warp       06:40:04:00:02:00:00       02:40:00       ✔                 0x40       Presets: Load       Time Lapse       06:40:04:00:02:00:01       02:40:00       ✔                 0x40       Presets: Load       Night Lapse       06:40:04:00:02:00:02       02:40:00       ✔                 0x40       Presets: Load       Max Video       06:40:04:00:03:00:00       02:40:00       \\&gt;= v01.20.00                 0x40       Presets: Load       Max Photo       06:40:04:00:04:00:00       02:40:00       \\&gt;= v01.20.00                 0x40       Presets: Load       Max Timewarp       06:40:04:00:05:00:00       02:40:00       \\&gt;= v01.20.00                 0x40       Presets: Load       Standard [EB]       06:40:04:00:08:00:00       02:40:00       \\&gt;= v01.16.00                 0x40       Presets: Load       Activity [EB]       06:40:04:00:08:00:01       02:40:00       \\&gt;= v01.16.00                 0x40       Presets: Load       Cinematic [EB]       06:40:04:00:08:00:02       02:40:00       \\&gt;= v01.16.00                 0x40       Presets: Load       Slo-Mo [EB]       06:40:04:00:08:00:03       02:40:00       \\&gt;= v01.16.00                 0x40       Presets: Load       4K Tripod       06:40:04:00:09:00:00       02:40:00       \\&gt;= v01.16.00                 0x40       Presets: Load       5.3K Tripod       06:40:04:00:09:00:01       02:40:00       \\&gt;= v01.16.00                 0x50       Analytics       Set third party client       01:50       02:50:00       ✔                 0x51       Open GoPro       Get version       01:51       Complex       ✔",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#commands-quick-reference",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Complex Command Responses",
            "excerpt": "Below are clarifications for complex camera responses",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#complex-command-responses",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Get Hardware Info",
            "excerpt": "Response Packet       Response Byte(s)       Description                 1       20       Start packet                 51       Packet length                 3C:00       Command 3C sent successfully                 04       Length of model number                 00:00:00:13       Model number                 0B       Length of model name                 48:45:52:4F:58:20:42:6C:61:63       \"HEROX Blac\"                 2       80       Continuation packet                 6B       \"k\"                 04       Length of board type                 30:78:30:35       \"0x05\"                 0F       Length of firmware version                 48:44:58:2E:58:58:2E:58:58:2E:58:58       \"HDX.XX.XX.XX\"                 3       81       Continuation packet (1)                 2E:58:58       \".XX\"                 0E       Length of serial number                 58:58:58:58:58:58:58:58:58:58:58:58:58:58       \"XXXXXXXXXXXXXX\"                 0A       Length of AP SSID                 4       82       Continuation packet (2)                 47:50:32:34:35:30:58:58:58:58       \"GP2450XXXX\"                 0C       AP MAC Address length                 58:58:58:58:58:58:58:58       \"XXXXXXXX\"                 5       83       Continuation packet (3)                 58:58:58:58       \"XXXX\"",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#get-hardware-info",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Open GoPro Version",
            "excerpt": "Given the response 06:51:00:01:01:01:00, the Open GoPro version would be vXX.YY.                  Response Byte(s)       Description                 06       Packet length                 51       Command ID                 00       Status (OK)                 01       Length of major version                 01       Major version: 1                 01       Length of minor version                 00       Minor version: 0",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#open-gopro-version",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Get Date/Time",
            "excerpt": "Given the response 0b:0e:00:08:07:e5:01:02:03:04:05:06, the date/time would be 2021-01-02 03:04:05 (Saturday).                  Response Byte(s)       Description                 0B       Packet length                 0E       Command ID                 00       Status (OK)                 08       Date length (bytes)                 07:E5       Year (big endian)                 01       Month                 02       Day                 03       Hour                 04       Minute                 05       Second                 06       Day of the week (Sun=0, Sat=6)",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#get-date-time",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Settings",
            "excerpt": "GoPro settings can be configured using the GP-Settings (GP-0074) UUID. Setting status is returned on GP-Settings-Status (GP-0075) UUID.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#settings",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Settings Request Format",
            "excerpt": "This will configure a setting on the camera. Only one setting may be sent on a packet (GATT notify or write-no-response), although multiple packets may be sent back-to-back.                  Request Length       Setting ID       Setting Value Length       Setting Value                 1-2 bytes       1 byte       1 byte       (variable length)",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#settings-request-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Settings Response Format",
            "excerpt": "Response Length       Setting ID       Response Code                 1 byte       1 byte       1 byte",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#settings-response-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Settings Quick Reference",
            "excerpt": "All settings are sent to UUID GP-0074. All values are hexadecimal and length are in bytes.  ✔ Indicates support for all Open GoPro firmware versions.  ❌ Indicates a lack of support for all Open GoPro firmware versions.  >= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ                   Setting ID       Setting       Option       Request       Response       HERO10 Black                 2       Resolution       Set video resolution (id: 2) to 4k (id: 1)       03:02:01:01       02:02:00       ✔                 2       Resolution       Set video resolution (id: 2) to 2.7k (id: 4)       03:02:01:04       02:02:00       ✔                 2       Resolution       Set video resolution (id: 2) to 2.7k 4:3 (id: 6)       03:02:01:06       02:02:00       ✔                 2       Resolution       Set video resolution (id: 2) to 1080 (id: 9)       03:02:01:09       02:02:00       ✔                 2       Resolution       Set video resolution (id: 2) to 4k 4:3 (id: 18)       03:02:01:12       02:02:00       ✔                 2       Resolution       Set video resolution (id: 2) to 5k 4:3 (id: 25)       03:02:01:19       02:02:00       ✔                 2       Resolution       Set video resolution (id: 2) to 5.3k (id: 100)       03:02:01:64       02:02:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 240 (id: 0)       03:03:01:00       02:03:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 120 (id: 1)       03:03:01:01       02:03:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 100 (id: 2)       03:03:01:02       02:03:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 60 (id: 5)       03:03:01:05       02:03:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 50 (id: 6)       03:03:01:06       02:03:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 30 (id: 8)       03:03:01:08       02:03:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 25 (id: 9)       03:03:01:09       02:03:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 24 (id: 10)       03:03:01:0A       02:03:00       ✔                 3       Frames Per Second       Set video fps (id: 3) to 200 (id: 13)       03:03:01:0D       02:03:00       ✔                 59       Auto Power Down       Set auto power down (id: 59) to never (id: 0)       03:3B:01:00       01:3B:00       ✔                 59       Auto Power Down       Set auto power down (id: 59) to 5 min (id: 4)       03:3B:01:04       01:3B:00       ✔                 59       Auto Power Down       Set auto power down (id: 59) to 15 min (id: 6)       03:3B:01:06       01:3B:00       ✔                 59       Auto Power Down       Set auto power down (id: 59) to 30 min (id: 7)       03:3B:01:07       01:3B:00       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to wide (id: 0)       03:79:01:00       02:79:00       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to narrow (id: 2)       03:79:01:02       02:79:00       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to superview (id: 3)       03:79:01:03       02:79:00       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to linear (id: 4)       03:79:01:04       02:79:00       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to max superview (id: 7)       03:79:01:07       02:79:00       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to linear + horizon leveling (id: 8)       03:79:01:08       02:79:00       ✔                 122       Photo Digital Lenses       Set photo digital lenses (id: 122) to narrow (id: 19)       03:7A:01:13       02:7A:00       ✔                 122       Photo Digital Lenses       Set photo digital lenses (id: 122) to max superview (id: 100)       03:7A:01:64       02:7A:00       ✔                 122       Photo Digital Lenses       Set photo digital lenses (id: 122) to wide (id: 101)       03:7A:01:65       02:7A:00       ✔                 122       Photo Digital Lenses       Set photo digital lenses (id: 122) to linear (id: 102)       03:7A:01:66       02:7A:00       ✔                 123       Time Lapse Digital Lenses       Set time lapse digital lenses (id: 123) to narrow (id: 19)       03:7B:01:13       02:7B:00       ✔                 123       Time Lapse Digital Lenses       Set time lapse digital lenses (id: 123) to max superview (id: 100)       03:7B:01:64       02:7B:00       ✔                 123       Time Lapse Digital Lenses       Set time lapse digital lenses (id: 123) to wide (id: 101)       03:7B:01:65       02:7B:00       ✔                 123       Time Lapse Digital Lenses       Set time lapse digital lenses (id: 123) to linear (id: 102)       03:7B:01:66       02:7B:00       ✔                 128       Media Format       Set media format (id: 128) to time lapse video (id: 13)       03:80:01:0D       02:80:00       ✔                 128       Media Format       Set media format (id: 128) to time lapse photo (id: 20)       03:80:01:14       02:80:00       ✔                 128       Media Format       Set media format (id: 128) to night lapse photo (id: 21)       03:80:01:15       02:80:00       ✔                 128       Media Format       Set media format (id: 128) to night lapse video (id: 26)       03:80:01:1A       02:80:00       ✔                 134       Anti-Flicker       Set setup anti flicker (id: 134) to 60hz (id: 2)       03:86:01:02       02:86:00       ✔                 134       Anti-Flicker       Set setup anti flicker (id: 134) to 50hz (id: 3)       03:86:01:03       02:86:00       ✔                 135       Hypersmooth       Set video hypersmooth (id: 135) to off (id: 0)       03:87:01:00       02:87:00       ✔                 135       Hypersmooth       Set video hypersmooth (id: 135) to high (id: 2)       03:87:01:02       02:87:00       ✔                 135       Hypersmooth       Set video hypersmooth (id: 135) to boost (id: 3)       03:87:01:03       02:87:00       ✔                 135       Hypersmooth       Set video hypersmooth (id: 135) to standard (id: 100)       03:87:01:64       02:87:00       ✔                 162       Max Lens       Set max lens (id: 162) to off (id: 0)       03:A2:01:00       02:A2:00       \\&gt;= v01.20.00                 162       Max Lens       Set max lens (id: 162) to on (id: 1)       03:A2:01:01       02:A2:00       \\&gt;= v01.20.00                 173       Video Performance Mode       Set video performance mode (id: 173) to maximum video performance (id: 0)       03:AD:01:00       02:AD:00       \\&gt;= v01.16.00                 173       Video Performance Mode       Set video performance mode (id: 173) to extended battery (id: 1)       03:AD:01:01       02:AD:00       \\&gt;= v01.16.00                 173       Video Performance Mode       Set video performance mode (id: 173) to tripod / stationary video (id: 2)       03:AD:01:02       02:AD:00       \\&gt;= v01.16.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#settings-quick-reference",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Camera Capabilities",
            "excerpt": "Camera capabilities usually change from one camera to another and often change from one release to the next. Below are documents that detail whitelists for basic video settings for every supported camera release.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#camera-capabilities",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Note about Dependency Ordering and Blacklisting",
            "excerpt": "Capability documents define supported camera states. Each state is comprised of a set of setting options that are presented in dependency order. This means each state is guaranteed to be attainable if and only if the setting options are set in the order presented. Failure to adhere to dependency ordering may result in the camera's blacklist rules rejecting a set-setting command.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#note-about-dependency-ordering-and-blacklisting",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Example",
            "excerpt": "Camera       Command 1       Command 2       Command 3       Command 4       Command 5       Guaranteed Valid?                 HERO10 Black       Res: 1080       Anti-Flicker: 60Hz (NTSC)       FPS: 240       FOV: Wide       Hypersmooth: OFF       ✔                 HERO10 Black       FPS: 240       Anti-Flicker: 60Hz (NTSC)       Res: 1080       FOV: Wide       Hypersmooth: OFF       ❌           In the example above, the first set of commands will always work for basic video presets such as Standard.     In the second example, suppose the camera's Video Resolution was previously set to 4K. If the user tries to set Video FPS to 240, it will fail because 4K/240fps is not supported.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#example",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Capability Documents",
            "excerpt": "Documents       Product       Release                 capabilities.xlsx capabilities.json       HERO10 Black       v01.30.00                 v01.20.00                 v01.16.00                 v01.10.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#capability-documents",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Spreadsheet Format",
            "excerpt": "The capabilities spreadsheet contains worksheets for every supported release. Each row in a worksheet represents a whitelisted state and is presented in dependency order as outlined above.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#spreadsheet-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: JSON Format",
            "excerpt": "The capabilities JSON contains a set of whitelist states for every supported release. Each state is comprised of a list of objects that contain setting and option IDs necessary to construct set-setting commands and are given in dependency order as outlined above.     Below is a simplified example of the capabilities JSON file; a formal schema is also available here: capabilities_schema.json    ``` {     \"(PRODUCT_NAME)\": {         \"(RELEASE_VERSION)\": {             \"states\": [                 [                     {\"setting_name\": \"(str)\", \"setting_id\": (int), \"option_name\": \"(str)\", \"option_id\": (int)},                     ...                 ],                 ...             ],         },         ...     },     ... } ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#json-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Query",
            "excerpt": "The camera provides two basic types of state information: Camera status and settings. Camera status info includes information such as the current preset/mode, whether the system is encoding, remaining sdcard space, etc. Settings info gives the currently selected option for each setting; for example, this includes the current video resolution, frame rate, digital lens (FOV), etc.     Queries are sent to to GP-0076 and responses are received on GP-0077. All packets sent and received are in Big Endian.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#query",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Query Format",
            "excerpt": "Header/Length       Query Command ID       Array of IDs                 1-2 bytes       1 byte       Variable Length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#query-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Query Commands",
            "excerpt": "All query commands are sent to GP-0076. Responses are received on GP-0077.    Note: omitting :xx:... from (un)register query commands will result in being (un)registered for all possible updates                  Query ID       Query       Request       Notes                 0x12       Get setting value       02:12:xx       xx -> Setting ID                 0x12       Get all setting values       01:12                        0x13       Get status value       02:13:xx       xx -> status code                 0x13       Get all status values       01:13                        0x52       Register for setting updates       nn:52:xx:...       nn -> message lengthxx -> setting id                 0x53       Register for status updates       nn:53:xx:...       nn -> message lengthxx -> status code                 0x72       Unregister for setting updates       nn:72:xx:...       nn -> message lengthxx -> setting id                 0x73       Unregister for status updates       nn:73:xx:...       nn -> message lengthxx -> status code",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#query-commands",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Query Response Format",
            "excerpt": "Query responses are pushed asynchronously in the following scenarios:     The user queries for current status/settings The user registers for settings/status updates The user is registered to receive updates for a status/setting and the value changes                  Message Length       Query ID       Command Status       Status ID       Status Value Length       Status Value                 1-2 bytes       1 byte       1 byte       1 byte       1 byte       1-255 bytes",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#query-response-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Multi-Value Responses",
            "excerpt": "When querying for or receiving a push notifications about more than one setting/status, the Status ID, Status Value Length, and Status Value fields become collectively repeatable.     Example:      [MESSAGE LENGTH]:[QUERY ID]:[COMMAND STATUS]:[ID1]:[LENGTH1]:[VALUE1]:[ID2]:[LENGTH2]:[VALUE2]:...",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#multi-value-responses",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Push Notification Responses",
            "excerpt": "The Query ID for settings/status push notifications replaces the upper 4 bits with 1001 (nine).    For example, if the original query comand ID was 0x52, the query ID of the push notification will be 0x92.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#push-notification-responses",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Status Codes",
            "excerpt": "Below is a table of supported status codes.  ✔ Indicates support for all Open GoPro firmware versions.  ❌ Indicates a lack of support for all Open GoPro firmware versions.  >= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ                  Status ID       Name       Description       Type       Values       HERO10 Black                 1       Internal battery present       Is the system's internal battery present?       boolean       0: False 1: True        ✔                 2       Internal battery level       Rough approximation of internal battery level in bars       integer       0: Zero 1: One 2: Two 3: Three        ✔                 3       External battery present       Is an external battery connected?       boolean       0: False 1: True        ✔                 4       External battery level       External battery power level in percent       percent       0-100       ✔                 6       System hot       Is the system currently overheating?       boolean       0: False 1: True        ✔                 8       System busy       Is the camera busy?       boolean       0: False 1: True        ✔                 9       Quick capture active       Is Quick Capture feature enabled?       boolean       0: False 1: True        ✔                 10       Encoding active       Is the system encoding right now?       boolean       0: False 1: True        ✔                 11       Lcd lock active       Is LCD lock active?       boolean       0: False 1: True        ✔                 13       Video progress counter       When encoding video, this is the duration (seconds) of the video so far; 0 otherwise       integer       *       ✔                 17       Enable       Are Wireless Connections enabled?       boolean       0: False 1: True        ✔                 19       State       The pairing state of the camera       integer       0: Success 1: In Progress 2: Failed 3: Stopped        ✔                 20       Type       The last type of pairing that the camera was engaged in       integer       0: Not Pairing 1: Pairing App 2: Pairing Remote Control 3: Pairing Bluetooth Device        ✔                 21       Pair time       Time (milliseconds) since boot of last successful pairing complete action       integer       *       ✔                 22       State       State of current scan for WiFi Access Points. Appears to only change for CAH-related scans       integer       0: Never started 1: Started 2: Aborted 3: Canceled 4: Completed        ✔                 23       Scan time msec       The time, in milliseconds since boot that the WiFi Access Point scan completed       integer       *       ✔                 24       Provision status       WiFi AP provisioning state       integer       0: Never started 1: Started 2: Aborted 3: Canceled 4: Completed        ✔                 26       Remote control version       Wireless remote control version       integer       *       ✔                 27       Remote control connected       Is a wireless remote control connected?       boolean       0: False 1: True        ✔                 28       Pairing       Wireless Pairing State       integer       *       ✔                 29       Wlan ssid       Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int       string       *       ✔                 30       Ap ssid       Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int       string       *       ✔                 31       App count       The number of wireless devices connected to the camera       integer       *       ✔                 32       Enable       Is Preview Stream enabled?       boolean       0: False 1: True        ✔                 33       Sd status       Primary Storage Status       integer       -1: Unknown 0: OK 1: SD Card Full 2: SD Card Removed 3: SD Card Format Error 4: SD Card Busy 8: SD Card Swapped        ✔                 34       Remaining photos       How many photos can be taken before sdcard is full       integer       *       ✔                 35       Remaining video time       How many minutes of video can be captured with current settings before sdcard is full       integer       *       ✔                 36       Num group photos       How many group photos can be taken with current settings before sdcard is full       integer       *       ✔                 37       Num group videos       Total number of group videos on sdcard       integer       *       ✔                 38       Num total photos       Total number of photos on sdcard       integer       *       ✔                 39       Num total videos       Total number of videos on sdcard       integer       *       ✔                 41       Ota status       The current status of Over The Air (OTA) update       integer       0: Idle 1: Downloading 2: Verifying 3: Download Failed 4: Verify Failed 5: Ready 6: GoPro App: Downloading 7: GoPro App: Verifying 8: GoPro App: Download Failed 9: GoPro App: Verify Failed 10: GoPro App: Ready        ✔                 42       Download cancel request pending       Is there a pending request to cancel a firmware update download?       boolean       0: False 1: True        ✔                 45       Camera locate active       Is locate camera feature active?       boolean       0: False 1: True        ✔                 49       Multi shot count down       The current timelapse interval countdown value (e.g. 5...4...3...2...1...)       integer       *       ✔                 54       Remaining space       Remaining space on the sdcard in Kilobytes       integer       *       ✔                 55       Supported       Is preview stream supported in current recording/flatmode/secondary-stream?       boolean       0: False 1: True        ✔                 56       Wifi bars       WiFi signal strength in bars       integer       *       ✔                 58       Num hilights       The number of hilights in encoding video (set to 0 when encoding stops)       integer       *       ✔                 59       Last hilight time msec       Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)       integer       *       ✔                 60       Next poll msec       The min time between camera status updates (msec). Do not poll for status more often than this       integer       *       ✔                 64       Remaining timelapse time       How many min of Timelapse video can be captured with current settings before sdcard is full       integer       *       ✔                 65       Exposure select type       Liveview Exposure Select Mode       integer       0: Disabled 1: Auto 2: ISO Lock 3: Hemisphere        ✔                 66       Exposure select x       Liveview Exposure Select: y-coordinate (percent)       percent       0-100       ✔                 67       Exposure select y       Liveview Exposure Select: y-coordinate (percent)       percent       0-100       ✔                 68       Gps status       Does the camera currently have a GPS lock?       boolean       0: False 1: True        ✔                 69       Ap state       Is the WiFi radio enabled?       boolean       0: False 1: True        ✔                 70       Internal battery percentage       Internal battery level (percent)       percent       0-100       ✔                 74       Acc mic status       Microphone Accesstory status       integer       0: Microphone mod not connected 1: Microphone mod connected 2: Microphone mod connected and microphone plugged into Microphone mod        ✔                 75       Digital zoom       Digital Zoom level (percent)       percent       0-100       ✔                 76       Wireless band       Wireless Band       integer       0: 2.4 GHz 1: 5 GHz 2: Max        ✔                 77       Digital zoom active       Is Digital Zoom feature available?       boolean       0: False 1: True        ✔                 78       Mobile friendly video       Are current video settings mobile friendly? (related to video compression and frame rate)       boolean       0: False 1: True        ✔                 79       First time use       Is the camera currently in First Time Use (FTU) UI flow?       boolean       0: False 1: True        ✔                 81       Band 5ghz avail       Is 5GHz wireless band available?       boolean       0: False 1: True        ✔                 82       System ready       Is the system ready to accept commands?       boolean       0: False 1: True        ✔                 83       Batt okay for ota       Is the internal battery charged sufficiently to start Over The Air (OTA) update?       boolean       0: False 1: True        ✔                 85       Video low temp alert       Is the camera getting too cold to continue recording?       boolean       0: False 1: True        ✔                 86       Actual orientation       The rotational orientation of the camera       integer       0: 0 degrees (upright) 1: 180 degrees (upside down) 2: 90 degrees (laying on right side) 3: 270 degrees (laying on left side)        ✔                 88       Zoom while encoding       Is this camera capable of zooming while encoding (static value based on model, not settings)       boolean       0: False 1: True        ✔                 89       Current mode       Current flatmode ID       integer       *       ✔                 91       Logs ready       Are system logs ready to be downloaded?       boolean       0: False 1: True        ✔                 93       Active video presets       Current Video Preset (ID)       integer       *       ✔                 94       Active photo presets       Current Photo Preset (ID)       integer       *       ✔                 95       Active timelapse presets       Current Timelapse Preset (ID)       integer       *       ✔                 96       Active presets group       Current Preset Group (ID)       integer       *       ✔                 97       Active preset       Current Preset (ID)       integer       *       ✔                 98       Preset modified       Preset Modified Status, which contains an event ID and a preset (group) ID       integer       *       ✔                 99       Remaining live bursts       How many Live Bursts can be captured before sdcard is full       integer       *       ✔                 100       Num total live bursts       Total number of Live Bursts on sdcard       integer       *       ✔                 101       Capture delay active       Is Capture Delay currently active (i.e. counting down)?       boolean       0: False 1: True        ✔                 102       Media mod mic status       Media mod State       integer       0: Media mod microphone removed 2: Media mod microphone only 3: Media mod microphone with external microphone        ✔                 103       Timewarp speed ramp active       Time Warp Speed       integer       0: 15x 1: 30x 2: 60x 3: 150x 4: 300x 5: 900x 6: 1800x 7: 2x 8: 5x 9: 10x 10: Auto 11: 1x (realtime) 12: 1/2x (slow-motion)        ✔                 104       Linux core active       Is the system's Linux core active?       boolean       0: False 1: True        ✔                 105       Camera lens type       Camera lens type (reflects changes to setting 162)       integer       0: Default 1: Max Lens        ✔                 106       Video hindsight capture active       Is Video Hindsight Capture Active?       boolean       0: False 1: True        ✔                 107       Scheduled preset       Scheduled Capture Preset ID       integer       *       ✔                 108       Scheduled enabled       Is Scheduled Capture set?       boolean       0: False 1: True        ✔                 109       Creating preset       Is the camera in the process of creating a custom preset?       boolean       0: False 1: True        ✔                 110       Media mod status       Media Mode Status (bitmasked)       integer       0: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: False 1: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: True 2: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: False 3: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: True 4: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: False 5: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: True 6: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: False 7: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: True        ✔                 111       Sd rating check error       Does sdcard meet specified minimum write speed?       boolean       0: False 1: True        ✔                 112       Sd write speed error       Number of sdcard write speed errors since device booted       integer       *       ✔                 113       Turbo transfer       Is Turbo Transfer active?       boolean       0: False 1: True        ✔                 114       Camera control status       Camera control status ID       integer       0: Camera Idle: No one is attempting to change camera settings 1: Camera Control: Camera is in a menu or changing settings. To intervene, app must request control 2: Camera External Control: An outside entity (app) has control and is in a menu or modifying settings        ✔                 115       Usb connected       Is the camera connected to a PC via USB?       boolean       0: False 1: True        ✔                 116       Allow control over usb       Camera control over USB state       integer       0: Disabled 1: Enabled        \\&gt;= v01.30.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#status-codes",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Protobuf",
            "excerpt": "In order to maximize BLE bandwidth, some messages and their corresponding notifications utilize Google Protobuf (Protocol Buffers).",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#protobuf",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Protobuf Message Format",
            "excerpt": "Protobuf communications with the camera differ from TLV-style communications. Rather than having a Type, Length, and Value, GoPro protobuf messages utilize the following:  Feature: Indicates command type (e.g. command, setting, query) Action: Specific camera action; value indicates whether message was sent or an (aync) notification was received Value: Serialized protobuf object",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#protobuf-message-format",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Requests Sent",
            "excerpt": "Message Length       Feature ID       Action ID       Protobuf Bytestream                 1-2 bytes       1 byte       1 byte       Variable Length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#requests-sent",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Notifications Received",
            "excerpt": "Message Length       Feature ID       Response Action ID       Protobuf Bytestream                 1-2 bytes       1 byte       1 byte       Variable Length",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#notifications-received",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Protobuf UUIDs",
            "excerpt": "Below is a map of Protobuf Feature IDs and the characteristics used to write/notify. For additional details, see Services and Characteristics.                  Feature       Feature ID       UUID       Response UUID                 Command       0xF1       GP-0072       GP-0073                 Settings       0xF3       GP-0074       GP-0075                 Query       0xF5       GP-0076       GP-0077",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#protobuf-uuids",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Protobuf Commands",
            "excerpt": "Below is a table of protobuf commands that can be sent to the camera and their expected response.  ✔ Indicates support for all Open GoPro firmware versions.  ❌ Indicates a lack of support for all Open GoPro firmware versions.  >= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ                   Feature ID       Action ID       Response Action ID       Description       Request       Response       HERO10 Black                 0xF1       0x69       0xE9       Request set camera control status       RequestSetCameraControlStatus       ResponseGeneric       \\&gt;= v01.20.00                 0x6B       0xEB       Request set turbo active       RequestSetTurboActive       ResponseGeneric       ✔                 0xF5       0x72       0xF2       Request get preset status       RequestGetPresetStatus       NotifyPresetStatus       ✔                        0xF3       Async status update              NotifyPresetStatus       ✔",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#protobuf-commands",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: Protobuf Command Details",
            "excerpt": "Below are additional details about specific protobuf commands:",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#protobuf-command-details",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: RequestSetCameraControlStatus",
            "excerpt": "As part of the Global Behaviors feature, this command is used to tell the camera that the app (i.e. External Control) wants to be in control, which causes the camera to immediately exit any contextual menus and return to the idle screen.     Developers can query who is currently claiming control of the camera from camera status 114.     Developers can query whether the camera is currently in a contextual menu from camera status 63.     When the user interacts with the camera UI, the camera reclaims control and updates camera status to Control. When the user returns the camera UI to the idle screen, the camera updates camera status to Idle.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#requestsetcameracontrolstatus",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: RequestSetTurboActive",
            "excerpt": "Turbo Transfer Mode is a special feature that serves two purposes:  Temporarily modify low-level settings in the OS to prioritize WiFi offload speeds Put up a UI on the camera indicating that media is being transferred and preventing the user from inadvertently changing settings or capturing new media      Developers can query whether the camera is currently in Turbo Transfer Mode from camera status 113.     While in Turbo Transfer Mode, if the user presses the Mode/Power or Shutter buttons on the camera, Turbo Transfer Mode will be deactivated.     Some cameras are already optimized for WiFi transfer and do not gain additional speed from this feature.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#requestsetturboactive",
            "teaser": ''
        },
        {
            "title": "Bluetooth Low Energy (BLE) Specification v2.0: RequestGetPresetStatus",
            "excerpt": "This command serves two purposes:  Describe which Preset Groups and Presets the camera supports in its current state (Un)register to be notified when a Preset is modified (e.g. resolution changes from 1080p to 4K) or a Preset Group is modified (e.g. presets are reordered/create/deleted)      Each Preset Group contains an ID, whether additional presets can be added, and an array of existing Presets.     Each Preset contains information about its ID, associated flatmode, title, icon, whether it's a user-defined preset, whether the preset has been modified from its factory-default state (for factory-default presets only) and a list of  settings associated with the Preset.     Preset Status should not be confused with camera status, which contains hundreds of camera/setting statuses on a system level.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/ble_2_0#requestgetpresetstatus",
            "teaser": ''
        },
        {
            "title": "Demos: ",
            "excerpt": "Demos  {% assign languages = \"\" | split: \" \" %} {% for demo in site.demos %}     {% assign parts = demo.path | split: \"/\" %}     {% assign language = parts[1] | split: \" \" %}     {% assign languages = languages | concat: language %} {% endfor %}  {% assign unique_languages = languages | uniq %} {% for language in unique_languages %}     {% assign words = language | split: '_' %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/demos#",
            "teaser": ''
        },
        {
            "title": "Demos: {% for word in words %}{{ word | capitalize }} {% endfor %}",
            "excerpt": "{% for demo in site.demos %}         {% assign parts = demo.path | split: \"/\" %}         {% assign target_language = parts[1] %}         {% if target_language == language %} [{{ demo.title }}]({{ demo.permalink | prepend: site.baseurl }})  - {{ demo.snippet }}          {% endif %}     {% endfor %} {% endfor %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/demos#for-word-in-words-word-capitalize-endfor",
            "teaser": ''
        },
        {
            "title": "Frequently Asked Questions: ",
            "excerpt": "Frequently Asked Questions  If you have somehow stumbled here first, note that there are specifications, demos, and tutorials which expand upon much of the information here. These can be found, among other places, from the [home page](/).",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/faq#",
            "teaser": ''
        },
        {
            "title": "Frequently Asked Questions: Connectivity",
            "excerpt": "{% accordion   question=\"What is the distance from the camera that BLE will still work?\"   answer=\"It is standard Bluetooth 4.0 range and it depends on external factors such as: Interference: anything   interfering with the signal will shorten the range. The type of device that the camera is connected to: BT   classification distinguishes 3 device classes based on their power levels. Depending on the class of the   connected device, the range varies from less than 10 meters to 100 meters.\" %}  {% accordion   question=\"Can I connect using WiFi only?\"   answer=\"Theoretically yes, if you already know the SSID, password, and the camera's WiFi AP has been enabled.   However, practically no because BLE is required in order to discover this information and configure the AP.\" %}  {% accordion   question=\"Can I connect using BLE only?\"   answer=\"Yes, however there is some functionality that is not possible over BLE such as accessing the media list   and downloading files.\" %}  {% accordion   question=\"How many devices can connect to the camera?\"   answer=\"Simultaneously, only one device can connect at a time. However, the camera stores BLE security keys and   other connection information so it is possible to connect multiple devices sequentially.\" %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/faq#connectivity",
            "teaser": ''
        },
        {
            "title": "Frequently Asked Questions: General",
            "excerpt": "{% accordion   question=\"Is preview turned off during record for all video settings?\"   answer=\"Yes, preview is disabled during record on all video settings.\" %} {% accordion   question=\"How can I view the live stream?\"   answer=\"In VLC, for example, you need to open network stream udp://@0.0.0.0:8554. You may see some latency due   to VLC caching. See the Preview Stream tutorial for more information.\" %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/faq#general",
            "teaser": ''
        },
        {
            "title": "Frequently Asked Questions: Troubleshooting",
            "excerpt": "If you are able to consistently reproduce a problem, please file a bug on [Github Issues](https://github.com/gopro/OpenGoPro/issues)  {% accordion   question=\"Why isn't the camera advertising?\"   answer=\"If you have not yet paired to the camera with the desired device, then you need to first set the   camera into pairing mode (Connections->Connect Device->Quick App). If you have already   paired, then the camera should be advertising and ready to connect. If it is not advertising, it is possible   you are already connected to it from a previous session. To be sure, power cycle both the camera and the peer device.\" %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/faq#troubleshooting",
            "teaser": ''
        },
        {
            "title": "HTTP Specifications: ",
            "excerpt": "This page will provide links to each version of the Open GoPro HTTP specification, as well as an overview of the changes from the previous version. Click on an individual spec to see its complete information including possible commands, settings, etc.  {% note Since the Open GoPro API varies based on the version, it is necessary to query the Open GoPro version using the Get Version command upon connection %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http#",
            "teaser": ''
        },
        {
            "title": "HTTP Specifications: [HTTP Specification 2.0](http_versions/http_2_0.md)",
            "excerpt": "-   Hilights:     -   Capture media     -   Track camera state     -   Get media list and download files / metadata     -   Load / edit presets     -   Configure and use as webcam     -   Add / remove hilights -   Breaking changes:     -   Settings endpoint has changed to: `gopro/camera/setting?setting={setting}&option={option}`         See the [quick reference]({% link specs/http_versions/http_2_0.md %}settings-quick-reference) for more information     -   Video Digital Lens setting parameter changes:         -   Narrow changed from 6 to 2     -   Photo Digital Lens setting parameter changes:         -   Wide changed from 22 to 101         -   Linear changed from 23 to 102         -   Narrow changed from 24 to 19         -   Max Superview changed from 25 to 100     -   Multishot Digital Lens parameter changes:         -   Wide changed from 2 to 101         -   Narrow changed from 24 to 19",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http#http-specification-2-0-http-versions-http-2-0-md",
            "teaser": ''
        },
        {
            "title": "HTTP Specifications: [HTTP Specification 1.0](http_versions/http_1_0.md)",
            "excerpt": "-   Initial API",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http#http-specification-1-0-http-versions-http-1-0-md",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: ",
            "excerpt": "Overview   The GoPro API allows developers to create apps and utilities that interact with and control a GoPro camera.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: What can you do with GoPro API?",
            "excerpt": "The GoPro API allows you to control and query the camera:  Capture photo/video media Get media list Change settings Set date/time Get camera status Get media metadata (file size, width, height, duration, tags, etc) and more!",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#what-can-you-do-with-gopro-api",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Supported Cameras",
            "excerpt": "Below is a table of cameras that support GoPro's public REST API:                   ID       Model       Marketing Name       Minimal Firmware Version                 55       HD9.01       HERO9 Black       v1.60",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#supported-cameras",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Turning on Camera WiFi Access Point",
            "excerpt": "In order to maximize the battery life of the camera, the camera's WiFi AP is turned off by default. Turning on the WiFi AP requires connecting to the camera via Bluetooth Low Energy (BLE) and sending an AP Control command.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#turning-on-camera-wifi-access-point",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Authentication",
            "excerpt": "Once the WiFi Access Point has been turned on, authentication with the camera simply requries connecting with the correct SSID and password. This information is available in the camera UI by putting the camera into pairing mode and tapping the \"i\" in the top-right corner of the screen.     Additionally, when the camera is in pairing mode, the SSID and password can be read directly via Bluetooth Low Energy. See Services and Characteristics in BLE documentation for details.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#authentication",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Request and Response Formats",
            "excerpt": "The camera will respond to REST commands and queries according to the table below. Most commands are sent via HTTP/GET and require no special HTTP headers. Responses come in two parts: The standard HTTP return codes and JSON containing any additional information. Typically, when the camera accepts a command and begins to (asynchronously) work on it, it will return HTTP 200 (OK) and empty JSON (i.e. { }) to indicate success. If an error occurs, the camera will return a standard HTTP error code and JSON with helpful error/debug information.                   Protocol       Address       Port       Base URL                 WiFi       10.5.5.9       8080       http://10.5.5.9:8080             Depending on the command sent, the camera can return JSON, binary, or Protobuf data.  Get Camera State -> JSON Get Media Info -> JSON Get Media GPMF -> Binary Get Media List -> JSON Get Media Screennail (JPEG) -> Binary Get Media Thumbnail (JPEG) -> Binary Get Presets -> JSON",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#request-and-response-formats",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Sending Commands",
            "excerpt": "Depending on the camera's state, it may not be ready to accept some commands. This ready state is dependent on the System Busy and the Encoding Active status flags. For example:   System Busy flag is set while loading presets, changing settings, formatting sdcard, ... Encoding Active flag is set while capturing photo/video media      If the system is not ready, it should reject an incoming command; however, best practice is to always wait for the System Busy and Encode Active flags to go down before sending messages other than queries to get camera status. For details regarding camera state, see Camera Status Codes.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#sending-commands",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Presets",
            "excerpt": "Presets were first added to the GoPro product line with the release of HERO8 Black. A preset represents a targeted camera state; for example, the built-in \"Activity\" preset is useful for capturing video with lots of quick motion while \"Cinematic\" is good for third-person and follow style shots.     Each preset is associated with:     A preset group (i.e. Video, Photo, Time Lapse) A camera mode (e.g. Video, Photo, Time Warp, ...) An icon A title A collection of settings specific to the preset (e.g. Resolution, Frame Rate and Digital Lens for video presets)    Different collections of presets will be available depending on the current camera state. For example:     Cameras that support Max Lens have special presets that are only available to load when Max Lens Mod is enabled (see Settings Quick Reference for details)",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#presets",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: HERO9 Black",
            "excerpt": "The HTTP server is not available while the camera is encoding, which means shutter controls are not supported over WiFi. This limitation can be overcome by using  Bluetooth Low Energy for command and control and HTTP/REST for quering media content such as media list, media info, preview stream, etc.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#hero9-black",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: General",
            "excerpt": "Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera. It is recommended to send a keep-alive at least once every 120 seconds. In general, querying the value for a setting that is not associated with the current preset/flatmode results in an undefined value. For example, the user should not try to query the current Photo Digital Lenses (FOV) value while in Standard preset (Video flatmode).",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#general",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Commands",
            "excerpt": "Using the Open GoPro API, a client can perform various command, control, and query operations!",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#commands",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Commands Quick Reference",
            "excerpt": "Below is a table of commands that can be sent to the camera and how to send them.                 Command       Description       HTTP Method       Endpoint       HERO9 Black                 Camera: Digital Zoom       Digital zoom 50%       GET       /gopro/camera/digital_zoom?percent=50       Y                 Camera: Get State       Get camera state (status + settings)       GET       /gopro/camera/state       Y                 Keep-alive       Send keep-alive       GET       /gopro/camera/keep_alive       Y                 Media: GPMF       Get GPMF data (MP4)       GET       /gopro/media/gpmf?path=100GOPRO/XXX.MP4       Y                 Media: GPMF       Get GPMF data (JPG)       GET       /gopro/media/gpmf?path=100GOPRO/XXX.JPG       Y                 Media: Info       Get media info (MP4)       GET       /gopro/media/info?path=100GOPRO/XXX.MP4       Y                 Media: Info       Get media info (JPG)       GET       /gopro/media/info?path=100GOPRO/XXX.JPG       Y                 Media: List       Get media list       GET       /gopro/media/list       Y                 Media: Screennail       Get screennail for \"100GOPRO/xxx.MP4\"       GET       /gopro/media/screennail?path=100GOPRO/XXX.MP4       Y                 Media: Screennail       Get screennail for \"100GOPRO/xxx.JPG\"       GET       /gopro/media/screennail?path=100GOPRO/XXX.JPG       Y                 Media: Telemetry       Get telemetry track data (MP4)       GET       /gopro/media/telemetry?path=100GOPRO/XXX.MP4       Y                 Media: Telemetry       Get telemetry track data (JPG)       GET       /gopro/media/telemetry?path=100GOPRO/XXX.JPG       Y                 Media: Thumbnail       Get thumbnail for \"100GOPRO/xxx.MP4\"       GET       /gopro/media/thumbnail?path=100GOPRO/XXX.MP4       Y                 Media: Thumbnail       Get thumbnail for \"100GOPRO/xxx.JPG\"       GET       /gopro/media/thumbnail?path=100GOPRO/XXX.JPG       Y                 Media: Turbo Transfer       Turbo transfer: on       GET       /gopro/media/turbo_transfer?p=1       Y                 Media: Turbo Transfer       Turbo transfer: off       GET       /gopro/media/turbo_transfer?p=0       Y                 Open GoPro       Get version       GET       /gopro/version       Y                 Presets: Get Status       Get preset status       GET       /gopro/camera/presets/get       Y                 Presets: Load       Activity       GET       /gopro/camera/presets/load?id=1       Y                 Presets: Load       Burst Photo       GET       /gopro/camera/presets/load?id=65538       Y                 Presets: Load       Cinematic       GET       /gopro/camera/presets/load?id=2       Y                 Presets: Load       Live Burst       GET       /gopro/camera/presets/load?id=65537       Y                 Presets: Load       Night Photo       GET       /gopro/camera/presets/load?id=65539       Y                 Presets: Load       Night Lapse       GET       /gopro/camera/presets/load?id=131074       Y                 Presets: Load       Photo       GET       /gopro/camera/presets/load?id=65536       Y                 Presets: Load       Slo-Mo       GET       /gopro/camera/presets/load?id=3       Y                 Presets: Load       Standard       GET       /gopro/camera/presets/load?id=0       Y                 Presets: Load       Time Lapse       GET       /gopro/camera/presets/load?id=131073       Y                 Presets: Load       Time Warp       GET       /gopro/camera/presets/load?id=131072       Y                 Presets: Load       Max Photo       GET       /gopro/camera/presets/load?id=262144       Y                 Presets: Load       Max Timewarp       GET       /gopro/camera/presets/load?id=327680       Y                 Presets: Load       Max Video       GET       /gopro/camera/presets/load?id=196608       Y                 Presets: Load Group       Video       GET       /gopro/camera/presets/set_group?id=1000       Y                 Presets: Load Group       Photo       GET       /gopro/camera/presets/set_group?id=1001       Y                 Presets: Load Group       Timelapse       GET       /gopro/camera/presets/set_group?id=1002       Y                 Stream: Start       Start preview stream       GET       /gopro/camera/stream/start       Y                 Stream: Stop       Stop preview stream       GET       /gopro/camera/stream/stop       Y",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#commands-quick-reference",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Settings",
            "excerpt": "GoPro cameras have hundreds of setting options to choose from, all of which can be set using a single endpoint. The endpoint is configured with a setting id and an option value. Note that setting option values are not globally unique. While most option values are enumerated values, some are complex bitmasked values.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#settings",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Settings Quick Reference",
            "excerpt": "Below is a table of setting options detailing how to set every option supported by Open GoPro cameras.                 Setting ID       Setting       Option       HTTP Method       Endpoint       HERO9 Black                 2       Resolution       Set video resolution (id: 2) to 4k (value: 1)       GET       /gopro/camera/setting?setting_id=2&opt_value=1       Y                 2       Resolution       Set video resolution (id: 2) to 2.7k (value: 4)       GET       /gopro/camera/setting?setting_id=2&opt_value=4       Y                 2       Resolution       Set video resolution (id: 2) to 2.7k 4:3 (value: 6)       GET       /gopro/camera/setting?setting_id=2&opt_value=6       Y                 2       Resolution       Set video resolution (id: 2) to 1440 (value: 7)       GET       /gopro/camera/setting?setting_id=2&opt_value=7       Y                 2       Resolution       Set video resolution (id: 2) to 1080 (value: 9)       GET       /gopro/camera/setting?setting_id=2&opt_value=9       Y                 2       Resolution       Set video resolution (id: 2) to 4k 4:3 (value: 18)       GET       /gopro/camera/setting?setting_id=2&opt_value=18       Y                 2       Resolution       Set video resolution (id: 2) to 5k (value: 24)       GET       /gopro/camera/setting?setting_id=2&opt_value=24       Y                 3       Frames Per Second       Set video fps (id: 3) to 240 (value: 0)       GET       /gopro/camera/setting?setting_id=3&opt_value=0       Y                 3       Frames Per Second       Set video fps (id: 3) to 120 (value: 1)       GET       /gopro/camera/setting?setting_id=3&opt_value=1       Y                 3       Frames Per Second       Set video fps (id: 3) to 100 (value: 2)       GET       /gopro/camera/setting?setting_id=3&opt_value=2       Y                 3       Frames Per Second       Set video fps (id: 3) to 60 (value: 5)       GET       /gopro/camera/setting?setting_id=3&opt_value=5       Y                 3       Frames Per Second       Set video fps (id: 3) to 50 (value: 6)       GET       /gopro/camera/setting?setting_id=3&opt_value=6       Y                 3       Frames Per Second       Set video fps (id: 3) to 30 (value: 8)       GET       /gopro/camera/setting?setting_id=3&opt_value=8       Y                 3       Frames Per Second       Set video fps (id: 3) to 25 (value: 9)       GET       /gopro/camera/setting?setting_id=3&opt_value=9       Y                 3       Frames Per Second       Set video fps (id: 3) to 24 (value: 10)       GET       /gopro/camera/setting?setting_id=3&opt_value=10       Y                 3       Frames Per Second       Set video fps (id: 3) to 200 (value: 13)       GET       /gopro/camera/setting?setting_id=3&opt_value=13       Y                 59       Auto Off       Set setup auto power down (id: 59) to never (value: 0)       GET       /gopro/camera/setting?setting_id=59&opt_value=0       Y                 59       Auto Off       Set setup auto power down (id: 59) to 5 min (value: 4)       GET       /gopro/camera/setting?setting_id=59&opt_value=4       Y                 59       Auto Off       Set setup auto power down (id: 59) to 15 min (value: 6)       GET       /gopro/camera/setting?setting_id=59&opt_value=6       Y                 59       Auto Off       Set setup auto power down (id: 59) to 30 min (value: 7)       GET       /gopro/camera/setting?setting_id=59&opt_value=7       Y                 121       Lens       Set video digital lenses (id: 121) to wide (value: 0)       GET       /gopro/camera/setting?setting_id=121&opt_value=0       Y                 121       Lens       Set video digital lenses (id: 121) to narrow (value: 6)       GET       /gopro/camera/setting?setting_id=121&opt_value=6       Y                 121       Lens       Set video digital lenses (id: 121) to superview (value: 3)       GET       /gopro/camera/setting?setting_id=121&opt_value=3       Y                 121       Lens       Set video digital lenses (id: 121) to linear (value: 4)       GET       /gopro/camera/setting?setting_id=121&opt_value=4       Y                 121       Lens       Set video digital lenses (id: 121) to max superview (value: 7)       GET       /gopro/camera/setting?setting_id=121&opt_value=7       Y                 121       Lens       Set video digital lenses (id: 121) to linear + horizon leveling (value: 8)       GET       /gopro/camera/setting?setting_id=121&opt_value=8       Y                 122       Lens       Set photo digital lenses (id: 122) to narrow (value: 24)       GET       /gopro/camera/setting?setting_id=122&opt_value=24       Y                 122       Lens       Set photo digital lenses (id: 122) to max superview (value: 25)       GET       /gopro/camera/setting?setting_id=122&opt_value=25       Y                 122       Lens       Set photo digital lenses (id: 122) to wide (value: 22)       GET       /gopro/camera/setting?setting_id=122&opt_value=22       Y                 122       Lens       Set photo digital lenses (id: 122) to linear (value: 23)       GET       /gopro/camera/setting?setting_id=122&opt_value=23       Y                 123       Lens       Set multi shot digital lenses (id: 123) to narrow (value: 24)       GET       /gopro/camera/setting?setting_id=123&opt_value=24       Y                 123       Lens       Set multi shot digital lenses (id: 123) to wide (value: 22)       GET       /gopro/camera/setting?setting_id=123&opt_value=22       Y                 123       Lens       Set multi shot digital lenses (id: 123) to linear (value: 23)       GET       /gopro/camera/setting?setting_id=123&opt_value=23       Y                 162       Max Lens Mod Enable       Set mods max lens enable (id: 162) to off (value: 0)       GET       /gopro/camera/setting?setting_id=162&opt_value=0       Y                 162       Max Lens Mod Enable       Set mods max lens enable (id: 162) to on (value: 1)       GET       /gopro/camera/setting?setting_id=162&opt_value=1       Y",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#settings-quick-reference",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Camera Capabilities",
            "excerpt": "Below are tables detailing supported features for Open GoPro cameras.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#camera-capabilities",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: HERO9 Black",
            "excerpt": "Resolution       Anti-Flicker       Frames Per Second       Lens                 1080       50Hz       24       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 50       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 100       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 200       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 60       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 120       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 240       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 1440       50Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 50       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 100       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 120       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 2.7K       50Hz       50       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 100       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       60       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 120       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 2.7K 4:3       50Hz       50       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       60       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 4K       50Hz       24       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 50       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Superview                 Linear                 Narrow                 Linear + Horizon Leveling                 60       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 4K 4:3       50Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 5K       50Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 25       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 60Hz       24       Wide                 Linear                 Narrow                 Linear + Horizon Leveling                 30       Wide                 Linear                 Narrow                 Linear + Horizon Leveling",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#hero9-black",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Media",
            "excerpt": "The camera provides an endpoint to query basic details about media captured on the sdcard.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#media",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Chapters",
            "excerpt": "All GoPro cameras break longer videos into chapters. GoPro cameras currently limit file sizes on sdcards to 4GB for both FAT32 and exFAT file systems. This limitation is most commonly seen when recording longer (10+ minute) videos. In practice, the camera will split video media into chapters named Gqccmmmm.MP4 (and ones for THM/LRV) such that:     q: Quality Level (X: Extreme, H: High, M: Medium, L: Low) cc: Chapter Number (01-99) mmmm: Media ID (0001-9999)    When media becomes chaptered, the camera increments subsequent Chapter Numbers while leaving the Media ID unchanged. For example, if the user records a long High-quality video that results in 4 chapters, the files on the sdcard may look like the following:    ``` -rwxrwxrwx@ 1 gopro  123456789  4006413091 Jan  1 00:00 GH010078.MP4 -rwxrwxrwx@ 1 gopro  123456789       17663 Jan  1 00:00 GH010078.THM -rwxrwxrwx@ 1 gopro  123456789  4006001541 Jan  1 00:00 GH020078.MP4 -rwxrwxrwx@ 1 gopro  123456789       17357 Jan  1 00:00 GH020078.THM -rwxrwxrwx@ 1 gopro  123456789  4006041985 Jan  1 00:00 GH030078.MP4 -rwxrwxrwx@ 1 gopro  123456789       17204 Jan  1 00:00 GH030078.THM -rwxrwxrwx@ 1 gopro  123456789   756706872 Jan  1 00:00 GH040078.MP4 -rwxrwxrwx@ 1 gopro  123456789       17420 Jan  1 00:00 GH040078.THM -rwxrwxrwx@ 1 gopro  123456789   184526939 Jan  1 00:00 GL010078.LRV -rwxrwxrwx@ 1 gopro  123456789   184519787 Jan  1 00:00 GL020078.LRV -rwxrwxrwx@ 1 gopro  123456789   184517614 Jan  1 00:00 GL030078.LRV -rwxrwxrwx@ 1 gopro  123456789    34877660 Jan  1 00:00 GL040078.LRV ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#chapters",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Media List Format",
            "excerpt": "The format of the media list is given below.    ``` {     \"id\": \"\",     \"media\": [         {             \"d\": \"\",             \"fs\": [                 {},                 ...             ]         },         ...     ] } ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#media-list-format",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Media List Keys",
            "excerpt": "The outer structure of the media list and the inner structure of individual media items use the keys in the table below.                Key       Description                 b       ID of first member of a group (for grouped media items)                 d       Directory name                 fs       File system. Contains listing of media items in directory                 g       Group ID (if grouped media item)                 id       Media list session identifier                 l       ID of last member of a group (for grouped media items)                 ls       Low resolution video file size                 m       List of missing/deleted group member IDs (for grouped media items)                 media       Contains media info for for each directory (e.g. 100GOPRO/, 101GOPRO/, ...)                 mod       Last modified time (seconds since epoch)                 n       Media filename                 s       Size of (group) media in bytes                 t       Group type (for grouped media items) (b -> burst, c -> continuous shot, n -> night lapse, t -> time lapse)",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#media-list-keys",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Grouped Media Items",
            "excerpt": "In order to minimize the size of the JSON transmitted by the camera, grouped media items such as Burst Photos, Time Lapse Photos, Night Lapse Photos, etc are represented with a single item in the media list with additional keys that allow the user to extrapolate individual filenames for each member of the group.     Filenames for group media items have the form \"GXXXYYYY.ZZZ\" where XXX is the group ID, YYY is the group member ID and ZZZ is the file extension.     For example, take the media list below, which contains a Time Lapse Photo group media item:    ``` {     \"id\": \"2530266050123724003\",     \"media\": [         {             \"d\": \"100GOPRO\",             \"fs\": [                 {                     \"b\": \"8\",                     \"cre\": \"1613669353\",                     \"g\": \"1\",                     \"l\": \"396\",                     \"m\": ['75', '139'],                     \"mod\": \"1613669353\",                     \"n\": \"G0010008.JPG\",                     \"s\": \"773977407\",                     \"t\": \"t\"                 }             ]         }     ] } ```   The first filename in the group is \"G0010008.JPG\" (key: \"n\"). The ID of the first group member in this case is \"008\" (key: \"b\"). The ID of the last group member in this case is \"396\" (key: \"l\"). The IDs of deleted members in this case are \"75\" and \"139\" (key: \"m\") Given this information, the user can extrapolate that the group currently contains     G0010008.JPG, G0010009.JPG, G0010010.JPG, ..., G0010074.JPG, G0010076.JPG, ..., G0010138.JPG, G0010140.JPG, ..., G0010394.JPG, G0010395.JPG. G0010396.JPG",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#grouped-media-items",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Downloading Media",
            "excerpt": "The URL to download/stream media from the DCIM/ directory on the sdcard is the Base URL plus /videos/DCIM/XXX/YYY where XXX is the directory name within DCIM/ given by the media list and YYY is the target media filename.     For example: Given the following media list:    ``` {     \"id\": \"3586667939918700960\",     \"media\": [         {             \"d\": \"100GOPRO\",             \"fs\": [                 {                     \"n\": \"GH010397.MP4\",                     \"cre\": \"1613672729\",                     \"mod\": \"1613672729\",                     \"glrv\": \"1895626\",                     \"ls\": \"-1\",                     \"s\": \"19917136\"                 },                 {                     \"cre\": \"1614340213\",                     \"mod\": \"1614340213\",                     \"n\": \"GOPR0001.JPG\",                     \"s\": \"6961371\"                 }             ]         }     ] } ```   The URL to download GH010397.MP4 over WiFi would be http://10.5.5.9:8080/videos/DCIM/100GOPRO/GH010397.MP4     The URL to download GOPR0001.JPG over WiFi would be http://10.5.5.9:8080/videos/DCIM/100GOPRO/GOPR0001.JPG",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#downloading-media",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Turbo Transfer",
            "excerpt": "Some cameras support Turbo Transfer mode, which allows media to be downloaded over WiFi more rapidly. This special mode should only be used during media offload. It is recommended that the user check for and--if necessary--disable Turbo Transfer on connect. For details on which cameras are supported and how to enable and disable Turbo Transfer, see Commands Quick Reference.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#turbo-transfer",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Downloading Preview Stream",
            "excerpt": "When the preview stream is started, the camera starts up a UDP client and begins writing MPEG Transport Stream data to the connected client on port 8554. In order to stream and save this data, the user can implement a UDP server that binds to the same port and appends datagrams to a file when they are received.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#downloading-preview-stream",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Camera State",
            "excerpt": "The camera provides multiple types of state, all of which can be queried:     Camera state: Contains information about camera status (photos taken, date, is-camera-encoding, etc) and settings (current video resolution, current frame rate, etc) Preset State: How presets are arranged into preset groups, their titles, icons, settings closely associated with each preset, etc",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#camera-state",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Camera State Format",
            "excerpt": "Camera state is given in the following form:  ``` {     \"status\": {         \"1\": ,         \"2\": ,         ...     },     \"settings: {         \"2\": ,         \"3\": ,         ...     } } ```   Where status X value and setting X value are almost always integer values. See Status Codes table in this document for exceptions.     For status, keys are status codes and values are status values.     For settings, keys are setting IDs, and values are option values",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#camera-state-format",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Camera Status Codes",
            "excerpt": "Below is a table of supported camera status codes.                 Status ID       Name       Description       Type       Values                 1       Internal battery present       Is the system's internal battery present?       boolean       0: False 1: True                  2       Internal battery level       Rough approximation of internal battery level in bars       integer       0: Zero 1: One 2: Two 3: Three                  3       External battery present       Is an external battery connected?       boolean       0: False 1: True                  4       External battery level       External battery power level in percent       percent       0-100                 5       Unused       Unused       None                        6       System hot       Is the system currently overheating?       boolean       0: False 1: True                  7       Unused       Unused       None                        8       System busy       Is the camera busy?       boolean       0: False 1: True                  9       Quick capture active       Is Quick Capture feature enabled?       boolean       0: False 1: True                  10       Encoding active       Is the system encoding right now?       boolean       0: False 1: True                  11       Lcd lock active       Is LCD lock active?       boolean       0: False 1: True                  12       Unused       Unused       None                        13       Video progress counter       When encoding video, this is the duration (seconds) of the video so far; 0 otherwise       integer       *                 17       Enable       Are Wireless Connections enabled?       boolean       0: False 1: True                  18       Unused       Unused              *                 19       State       The pairing state of the camera       integer       0: Success 1: In Progress 2: Failed 3: Stopped                  20       Type       The last type of pairing that the camera was engaged in       integer       0: Not Pairing 1: Pairing App 2: Pairing Remote Control 3: Pairing Bluetooth Device                  21       Pair time       Time (milliseconds) since boot of last successful pairing complete action       integer       *                 22       State       State of current scan for WiFi Access Points. Appears to only change for CAH-related scans       integer       0: Never started 1: Started 2: Aborted 3: Canceled 4: Completed                  23       Scan time msec       The time, in milliseconds since boot that the WiFi Access Point scan completed       integer       *                 24       Provision status       WiFi AP provisioning state       integer       0: Never started 1: Started 2: Aborted 3: Canceled 4: Completed                  25       Unused       Unused       None                        26       Remote control version       Wireless remote control version       integer       *                 27       Remote control connected       Is a wireless remote control connected?       boolean       0: False 1: True                  28       Pairing       Wireless Pairing State       integer       *                 29       Wlan ssid       Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int       string       *                 30       Ap ssid       Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int       string       *                 31       App count       The number of wireless devices connected to the camera       integer       *                 32       Enable       Is Preview Stream enabled?       boolean       0: False 1: True                  33       Sd status       Primary Storage Status       integer       -1: Unknown 0: OK 1: SD Card Full 2: SD Card Removed 3: SD Card Format Error 4: SD Card Busy 8: SD Card Swapped                  34       Remaining photos       How many photos can be taken before sdcard is full       integer       *                 35       Remaining video time       How many minutes of video can be captured with current settings before sdcard is full       integer       *                 36       Num group photos       How many group photos can be taken with current settings before sdcard is full       integer       *                 37       Num group videos       Total number of group videos on sdcard       integer       *                 38       Num total photos       Total number of photos on sdcard       integer       *                 39       Num total videos       Total number of videos on sdcard       integer       *                 40       Date time       Current date/time (format: %YY%MM%DD%HH%MM%SS, all values in hex)       string       *                 41       Ota status       The current status of Over The Air (OTA) update       integer       0: Idle 1: Downloading 2: Verifying 3: Download Failed 4: Verify Failed 5: Ready 6: GoPro App: Downloading 7: GoPro App: Verifying 8: GoPro App: Download Failed 9: GoPro App: Verify Failed 10: GoPro App: Ready                  42       Download cancel request pending       Is there a pending request to cancel a firmware update download?       boolean       0: False 1: True                  45       Camera locate active       Is locate camera feature active?       boolean       0: False 1: True                  49       Multi shot count down       The current timelapse interval countdown value (e.g. 5...4...3...2...1...)       integer       *                 50       Unused       Unused       None                        51       Unused       Unused       None                        52       Unused       Unused       None                        53       Unused       Unused       None                        54       Remaining space       Remaining space on the sdcard in Kilobytes       integer       *                 55       Supported       Is preview stream supported in current recording/flatmode/secondary-stream?       boolean       0: False 1: True                  56       Wifi bars       WiFi signal strength in bars       integer       *                 57       Current time msec       System time in milliseconds since system was booted       integer       *                 58       Num hilights       The number of hilights in encoding video (set to 0 when encoding stops)       integer       *                 59       Last hilight time msec       Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)       integer       *                 60       Next poll msec       The min time between camera status updates (msec). Do not poll for status more often than this       integer       *                 63       In contextual menu       Is the camera currently in a contextual menu (e.g. Preferences)?       boolean       0: False 1: True                  64       Remaining timelapse time       How many min of Timelapse video can be captured with current settings before sdcard is full       integer       *                 65       Exposure select type       Liveview Exposure Select Mode       integer       0: Disabled 1: Auto 2: ISO Lock 3: Hemisphere                  66       Exposure select x       Liveview Exposure Select: y-coordinate (percent)       percent       0-100                 67       Exposure select y       Liveview Exposure Select: y-coordinate (percent)       percent       0-100                 68       Gps status       Does the camera currently have a GPS lock?       boolean       0: False 1: True                  69       Ap state       Is the WiFi radio enabled?       boolean       0: False 1: True                  70       Internal battery percentage       Internal battery level (percent)       percent       0-100                 74       Acc mic status       Microphone Accesstory status       integer       0: Microphone mod not connected 1: Microphone mod connected 2: Microphone mod connected and microphone plugged into Microphone mod                  75       Digital zoom       Digital Zoom level (percent)       percent       0-100                 76       Wireless band       Wireless Band       integer       0: 2.4 GHz 1: 5 GHz 2: Max                  77       Digital zoom active       Is Digital Zoom feature available?       boolean       0: False 1: True                  78       Mobile friendly video       Are current video settings mobile friendly? (related to video compression and frame rate)       boolean       0: False 1: True                  79       First time use       Is the camera currently in First Time Use (FTU) UI flow?       boolean       0: False 1: True                  81       Band 5ghz avail       Is 5GHz wireless band available?       boolean       0: False 1: True                  82       System ready       Is the system ready to accept commands?       boolean       0: False 1: True                  83       Batt okay for ota       Is the internal battery charged sufficiently to start Over The Air (OTA) update?       boolean       0: False 1: True                  85       Video low temp alert       Is the camera getting too cold to continue recording?       boolean       0: False 1: True                  86       Actual orientation       The rotational orientation of the camera       integer       0: 0 degrees (upright) 1: 180 degrees (upside down) 2: 90 degrees (laying on right side) 3: 270 degrees (laying on left side)                  87       Thermal mitigation mode       Can camera use high resolution/fps (based on temperature)? (HERO7 Silver/White only)       boolean       0: False 1: True                  88       Zoom while encoding       Is this camera capable of zooming while encoding (static value based on model, not settings)       boolean       0: False 1: True                  89       Current mode       Current flatmode ID       integer       *                 91       Logs ready       Are system logs ready to be downloaded?       boolean       0: False 1: True                  92       Timewarp 1x active       Is Timewarp 1x active?       boolean       0: False 1: True                  93       Active video presets       Current Video Preset (ID)       integer       *                 94       Active photo presets       Current Photo Preset (ID)       integer       *                 95       Active timelapse presets       Current Timelapse Preset (ID)       integer       *                 96       Active presets group       Current Preset Group (ID)       integer       *                 97       Active preset       Current Preset (ID)       integer       *                 98       Preset modified       Preset Modified Status, which contains an event ID and a preset (group) ID       integer       *                 99       Remaining live bursts       How many Live Bursts can be captured before sdcard is full       integer       *                 100       Num total live bursts       Total number of Live Bursts on sdcard       integer       *                 101       Capture delay active       Is Capture Delay currently active (i.e. counting down)?       boolean       0: False 1: True                  102       Media mod mic status       Media mod State       integer       0: Media mod microphone removed 2: Media mod microphone only 3: Media mod microphone with external microphone                  103       Timewarp speed ramp active       Time Warp Speed       integer       0: 15x 1: 30x 2: 60x 3: 150x 4: 300x 5: 900x 6: 1800x 7: 2x 8: 5x 9: 10x 10: Auto 11: 1x (realtime) 12: 1/2x (slow-motion)                  104       Linux core active       Is the system's Linux core active?       boolean       0: False 1: True                  105       Camera lens type       Camera lens type (reflects changes to setting 162)       integer       0: Default 1: Max Lens                  106       Video hindsight capture active       Is Video Hindsight Capture Active?       boolean       0: False 1: True                  107       Scheduled preset       Scheduled Capture Preset ID       integer       *                 108       Scheduled enabled       Is Scheduled Capture set?       boolean       0: False 1: True                  109       Creating preset       Is the camera in the process of creating a custom preset?       boolean       0: False 1: True                  110       Media mod status       Media Mode Status (bitmasked)       integer       0: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: False 1: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: True 2: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: False 3: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: True 4: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: False 5: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: True 6: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: False 7: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: True                  113       Turbo transfer       Is Turbo Transfer active?       boolean       0: False 1: True",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#camera-status-codes",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v1.0: Preset Status Format",
            "excerpt": "Preset Status is returned as JSON, whose content is the serialization of the protobuf message: NotifyPresetStatus. Using Google protobuf APIs, the JSON can be converted back into a programmatic object in the user's language of choice.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_1_0#preset-status-format",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: ",
            "excerpt": "Overview   The GoPro API allows developers to create apps and utilities that interact with and control a GoPro camera.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: What can you do with the GoPro API?",
            "excerpt": "The GoPro API allows you to control and query the camera:  Capture photo/video media Get media list Change settings Get and set the date/time Get camera status Get media metadata (file size, width, height, duration, tags, etc) and more!",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#what-can-you-do-with-the-gopro-api",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Supported Cameras",
            "excerpt": "Below is a table of cameras that support GoPro's public HTTP API:                   ID       Model       Marketing Name       Minimal Firmware Version                 57       H21.01       HERO10 Black       v01.10.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#supported-cameras",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: WiFi",
            "excerpt": "Connection to the camera via WiFi requires that the camera's WiFi Access Point be enabled. This can be done by connecting to the camera via Bluetooth Low Energy (BLE) and sending the AP Control command: WIFI AP ON.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#wifi",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: USB",
            "excerpt": "OpenGoPro systems that utilize USB must support the Network Control Model (NCM) protocol. Connecting via USB requires the following steps:  Physically connect the camera's USB-C port to your system Send HTTP command to enable wired USB control",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#usb",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: WiFi",
            "excerpt": "Once the WiFi Access Point has been turned on, authentication with the camera simply requries connecting with the correct SSID and password. This information can be obtained in two ways:   Put the camera into pairing mode and tap the info button in the top-right corner of the screen. Read the SSID/password directly via Bluetooth Low Energy. See Services and Characteristics seciton in BLE Specification for details.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#wifi",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: USB",
            "excerpt": "No authentication is necessary.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#usb",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: WiFi",
            "excerpt": "The socket address for WiFi connections is 10.5.5.9:8080.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#wifi",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: USB",
            "excerpt": "The socket address for USB connections is 172.2X.1YZ.51:8080 where:   X is the 100's digit from the camera serial number Y is the 10's digit from the camera serial number Z is the 1's digit from the camera serial number      The camera's serial number can be obtained in any of the following ways:  Reading the sticker inside the camera's battery enclosure Camera UI: Preferences >> About >> Camera Info Bluetooth Low Energy by reading directly from Hardware Info . See Commands in BLE Specification for details.      For example, if the camera's serial number is C0000123456789, the IP address for USB connections would be 172.27.189.51.     Alternatively, the IP address can be discovered via mDNS as the camera registers the _gopro-web service.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#usb",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Request and Response Formats",
            "excerpt": "Most commands are sent via HTTP/GET and require no special headers. Responses come in two parts: The standard HTTP return codes and JSON containing any additional information.     The typical use case is that the camera accepts a valid command, returns HTTP/200 (OK) and empty JSON (i.e. { }) and begins asynchronously working on the command. If an error occurs, the camera will return a standard HTTP error code and JSON with helpful error/debug information.     Depending on the command sent, the camera can return JSON, binary, or Protobuf data. Some examples are listed below:                   Command       Return Type                 Get Camera State       JSON                 Get Media Info       JSON                 Get Media GPMF       Binary                 Get Media List       JSON                 Get Media Screennail (JPEG)       Binary                 Get Media Thumbnail (JPEG)       Binary                 Get Presets       JSON",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#request-and-response-formats",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Sending Commands",
            "excerpt": "Depending on the camera's state, it may not be ready to accept specific commands. This ready state is dependent on the System Busy and the Encoding Active status flags. For example:   System Busy flag is set while loading presets, changing settings, formatting sdcard, ... Encoding Active flag is set while capturing photo/video media      If the system is not ready, it should reject an incoming command; however, best practice is to always wait for the System Busy and Encode Active flags to be unset before sending messages other than camera status queries. For details regarding camera state, see Status Codes.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#sending-commands",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Presets",
            "excerpt": "The camera organizes modes of operation into presets. A preset is a logical wrapper around a specific camera flatmode and a collection of settings that target different ways of capturing media.     The set of presets available to load at any moment depends on the value of certain camera settings, which are outlined in the table below.     For per-preset firmware compatibility information, see Commands Quick Reference.                   Setting       Preset       Preset ID                 Max Lens: OFF       Standard       0x00000000                           Activity       0x00000001                           Cinematic       0x00000002                           Ultra Slo-Mo       0x00000004                           Basic       0x00000005                           Photo       0x00010000                           Live Burst       0x00010001                           Burst Photo       0x00010002                           Night Photo       0x00010003                           Time Warp       0x00020000                           Time Lapse       0x00020001                           Night Lapse       0x00020002                           Max Lens: ON       Max Video       0x00030000                           Max Photo       0x00040000                           Max Timewarp       0x00050000                           Video Performance Mode: Maximum Video Performance       Standard       0x00000000                                     Activity       0x00000001                                     Cinematic       0x00000002                                     Ultra Slo-Mo       0x00000004                                     Basic       0x00000005                                     Photo       0x00010000                                     Live Burst       0x00010001                                     Burst Photo       0x00010002                                     Night Photo       0x00010003                                     Time Warp       0x00020000                                     Time Lapse       0x00020001                                     Night Lapse       0x00020002                                     Video Performance Mode: Extended Battery       Photo       0x00010000                                     Live Burst       0x00010001                                     Burst Photo       0x00010002                                     Night Photo       0x00010003                                     Time Warp       0x00020000                                     Time Lapse       0x00020001                                     Night Lapse       0x00020002                                     Standard [EB]       0x00080000                                     Activity [EB]       0x00080001                                     Cinematic [EB]       0x00080002                                     Slo-Mo [EB]       0x00080003                                     Video Performance Mode: Tripod / Stationary Video       Photo       0x00010000                                     Live Burst       0x00010001                                     Burst Photo       0x00010002                                     Night Photo       0x00010003                                     Time Warp       0x00020000                                     Time Lapse       0x00020001                                     Night Lapse       0x00020002                                     4K Tripod       0x00090000                                     5.3K Tripod       0x00090001",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#presets",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Global Behaviors",
            "excerpt": "In order to prevent undefined behavior between the camera and a connected app, simultaneous use of the camera and a connected app is discouraged.     Best practice for synchronizing user/app control is to use the Set Camera Control Status command and corresponding Camera Control Status (CCS) camera statuses in alignment with the finite state machine below:    ```plantuml!   ' Define states IDLE: Control Status: Idle CAMERA_CONTROL: Control Status: Camera Control EXTERNAL_CONTROL: Control Status: External Control  ' Define transitions [*]              ->      IDLE  IDLE             ->      IDLE: App sets CCS: Idle IDLE             -up->   CAMERA_CONTROL: User interacts with camera IDLE             -down-> EXTERNAL_CONTROL: App sets CCS: External Control  CAMERA_CONTROL   ->      CAMERA_CONTROL: User interacts with camera CAMERA_CONTROL   -down-> IDLE: User returns camera to idle screen\\nApp sets CCS: Idle  EXTERNAL_CONTROL ->    EXTERNAL_CONTROL: App sets CCS: External Control EXTERNAL_CONTROL -up-> IDLE: App sets CCS: Idle\\nUser interacts with camera EXTERNAL_CONTROL -up-> CAMERA_CONTROL: User interacts with camera     ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#global-behaviors",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: HERO10 Black",
            "excerpt": "The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#hero10-black",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: General",
            "excerpt": "Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera. It is recommended to send a keep-alive at least once every 120 seconds. In general, querying the value for a setting that is not associated with the current preset/flatmode results in an undefined value. For example, the user should not try to query the current Photo Digital Lenses (FOV) value while in Standard preset (Video flatmode). USB command and control is not supported on HERO9 Black.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#general",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Webcam",
            "excerpt": "The webcam feature enables developers who are interested in writing custom drivers to make the camera broadcast its video preview with a limited set of resolution and field of view options.     While active, the webcam feature runs a UDP client that sends raw Transport Stream data to the connected client on port 8554. To test basic functionality, connect the camera to your system, start the webcam, and use an application such as VLC to start a network stream on udp://@0.0.0.0:8554.     For readers interested in using a GoPro camera as a webcam with preexisting tools, please see How to use GoPro as a Webcam.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#webcam",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Webcam Finite State Machine",
            "excerpt": "```plantuml!   ' Source: '    https://wiki-dev.gopro.com/pages/viewpage.action?spaceKey=SBO&title=Webcam+Http+Endpoint+API  ' Define states OFF:    Webcam disabled IDLE:   Webcam ready HPP:    High power preview LPP:    Low power preview  ' Actions: '   Connect camera to system via USB '   Start '   Preview '   Stop '   Exit  ' Define transitions [*]  --> OFF  OFF  --> IDLE: Connect USB  IDLE --> IDLE: Stop\\nExit IDLE --> HPP:  Start IDLE --> LPP:  Preview  HPP  --> HPP:  Start HPP  --> LPP:  Preview HPP  --> IDLE: Stop\\nExit  LPP  --> LPP:  Preview LPP  --> HPP:  Start LPP  --> IDLE: Stop\\nExit     ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#webcam-finite-state-machine",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Webcam Commands",
            "excerpt": "For details about how to send webcam commands, see Commands Quick Reference.                Command       Connections       Description                 Webcam: Start       USB       Enters webcam mode, uses default resolution and last-used fov, starts high-res stream to the IP address of caller                 Webcam: Start (with args)       USB       Enters webcam mode, uses specified resolution and/or fov, starts streaming to the IP address of caller                 Webcam: Preview       USB       Enters webcam mode, sets stream resolution and bitrate, starts low-res stream to the IP address of caller. Can set Webcam Digital Lenses and Digital Zoom levels while streaming                 Webcam: Stop       USB       Stops the webcam stream                 Webcam: Exit       USB       Stops the webcam stream and exits webcam mode                 Webcam: Status       WIFI, USB       Returns the current state of the webcam endpoint, including status and error codes (see tables below)                 Webcam: Version       WIFI, USB       Provides version information about webcam implementation in JSON format",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#webcam-commands",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Status Codes",
            "excerpt": "Status       Code                 OFF       0                 IDLE       1                 HIGH_POWER_PREVIEW       2                 LOW_POWER_PREVIEW       3",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#status-codes",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Error Codes",
            "excerpt": "Status       Code                 NONE       0                 SET_PRESET       1                 SET_WINDOW_SIZE       2                 EXEC_STREAM       3                 SHUTTER       4                 COM_TIMEOUT       5                 INVALID_PARAM       6                 UNAVAILABLE       7                 EXIT       8",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#error-codes",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Resolutions",
            "excerpt": "Note: If resolution is not set, 1080p will be used by default                  Resolution       ID                 480       4                 720       7                 1080       12",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#resolutions",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Webcam Digital Lenses (FOV)",
            "excerpt": "Note: If fov is not set, camera will default to the last-set fov or Wide if fov has never been set.                  Webcam Digital Lens (FOV)       ID                 WIDE       0                 NARROW       2                 SUPERVIEW       3                 LINEAR       4",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#webcam-digital-lenses-fov",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Commands",
            "excerpt": "Using the Open GoPro API, a client can perform various command, control, and query operations!",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#commands",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Commands Quick Reference",
            "excerpt": "Below is a table of commands that can be sent to the camera and how to send them.  ✔ Indicates support for all Open GoPro firmware versions.  ❌ Indicates a lack of support for all Open GoPro firmware versions.  >= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ                   Command       Description       HTTP Method       Endpoint       HERO10 Black                 Camera: Get State       Get camera state (status + settings)       GET       /gopro/camera/state       ✔                 Digital Zoom       Digital zoom 50%       GET       /gopro/camera/digital_zoom?percent=50       ✔                 Get Date/Time       Get date/time       GET       /gopro/camera/get_date_time       \\&gt;= v01.30.00                 Keep-alive       Send keep-alive       GET       /gopro/camera/keep_alive       ✔                 Media: GPMF       Get GPMF data (JPG)       GET       /gopro/media/gpmf?path=100GOPRO/XXX.JPG       ✔                 Media: GPMF       Get GPMF data (MP4)       GET       /gopro/media/gpmf?path=100GOPRO/XXX.MP4       ✔                 Media: HiLight (Add)       Add hilight to 100GOPRO/xxx.JPG       GET       /gopro/media/hilight/file?path=100GOPRO/XXX.JPG       \\&gt;= v01.30.00                 Media: HiLight (Add)       Add hilight to 100GOPRO/xxx.MP4 at offset 2500 ms       GET       /gopro/media/hilight/file?path=100GOPRO/XXX.MP4&ms=2500       \\&gt;= v01.30.00                 Media: HiLight (Remove)       Remove hilight from 100GOPRO/xxx.JPG       GET       /gopro/media/hilight/remove?path=100GOPRO/XXX.JPG       \\&gt;= v01.30.00                 Media: HiLight (Remove)       Remove hilight from 100GOPRO/xxx.MP4 at offset 2500ms       GET       /gopro/media/hilight/remove?path=100GOPRO/XXX.MP4&ms=2500       \\&gt;= v01.30.00                 Media: HiLight moment       Hilight moment during encoding       GET       /gopro/media/hilight/moment       \\&gt;= v01.30.00                 Media: Info       Get media info (JPG)       GET       /gopro/media/info?path=100GOPRO/XXX.JPG       ✔                 Media: Info       Get media info (MP4)       GET       /gopro/media/info?path=100GOPRO/XXX.MP4       ✔                 Media: List       Get media list       GET       /gopro/media/list       ✔                 Media: Screennail       Get screennail for \"100GOPRO/xxx.JPG\"       GET       /gopro/media/screennail?path=100GOPRO/XXX.JPG       ✔                 Media: Screennail       Get screennail for \"100GOPRO/xxx.MP4\"       GET       /gopro/media/screennail?path=100GOPRO/XXX.MP4       ✔                 Media: Telemetry       Get telemetry track data (JPG)       GET       /gopro/media/telemetry?path=100GOPRO/XXX.JPG       ✔                 Media: Telemetry       Get telemetry track data (MP4)       GET       /gopro/media/telemetry?path=100GOPRO/XXX.MP4       ✔                 Media: Thumbnail       Get thumbnail for \"100GOPRO/xxx.JPG\"       GET       /gopro/media/thumbnail?path=100GOPRO/XXX.JPG       ✔                 Media: Thumbnail       Get thumbnail for \"100GOPRO/xxx.MP4\"       GET       /gopro/media/thumbnail?path=100GOPRO/XXX.MP4       ✔                 Media: Turbo Transfer       Turbo transfer: off       GET       /gopro/media/turbo_transfer?p=0       ✔                 Media: Turbo Transfer       Turbo transfer: on       GET       /gopro/media/turbo_transfer?p=1       ✔                 Open GoPro       Get version       GET       /gopro/version       ✔                 Presets: Get Status       Get preset status       GET       /gopro/camera/presets/get       ✔                 Presets: Load       Standard       GET       /gopro/camera/presets/load?id=0       ✔                 Presets: Load       Activity       GET       /gopro/camera/presets/load?id=1       ✔                 Presets: Load       Cinematic       GET       /gopro/camera/presets/load?id=2       ✔                 Presets: Load       Ultra Slo-Mo       GET       /gopro/camera/presets/load?id=4       \\&gt;= v01.16.00                 Presets: Load       Basic       GET       /gopro/camera/presets/load?id=5       \\&gt;= v01.16.00                 Presets: Load       Photo       GET       /gopro/camera/presets/load?id=65536       ✔                 Presets: Load       Live Burst       GET       /gopro/camera/presets/load?id=65537       ✔                 Presets: Load       Burst Photo       GET       /gopro/camera/presets/load?id=65538       ✔                 Presets: Load       Night Photo       GET       /gopro/camera/presets/load?id=65539       ✔                 Presets: Load       Time Warp       GET       /gopro/camera/presets/load?id=131072       ✔                 Presets: Load       Time Lapse       GET       /gopro/camera/presets/load?id=131073       ✔                 Presets: Load       Night Lapse       GET       /gopro/camera/presets/load?id=131074       ✔                 Presets: Load       Max Video       GET       /gopro/camera/presets/load?id=196608       \\&gt;= v01.20.00                 Presets: Load       Max Photo       GET       /gopro/camera/presets/load?id=262144       \\&gt;= v01.20.00                 Presets: Load       Max Timewarp       GET       /gopro/camera/presets/load?id=327680       \\&gt;= v01.20.00                 Presets: Load       Standard [EB]       GET       /gopro/camera/presets/load?id=524288       \\&gt;= v01.16.00                 Presets: Load       Activity [EB]       GET       /gopro/camera/presets/load?id=524289       \\&gt;= v01.16.00                 Presets: Load       Cinematic [EB]       GET       /gopro/camera/presets/load?id=524290       \\&gt;= v01.16.00                 Presets: Load       Slo-Mo [EB]       GET       /gopro/camera/presets/load?id=524291       \\&gt;= v01.16.00                 Presets: Load       4K Tripod       GET       /gopro/camera/presets/load?id=589824       \\&gt;= v01.16.00                 Presets: Load       5.3K Tripod       GET       /gopro/camera/presets/load?id=589825       \\&gt;= v01.16.00                 Presets: Load Group       Video       GET       /gopro/camera/presets/set_group?id=1000       ✔                 Presets: Load Group       Photo       GET       /gopro/camera/presets/set_group?id=1001       ✔                 Presets: Load Group       Timelapse       GET       /gopro/camera/presets/set_group?id=1002       ✔                 Set Camera Control Status       Set camera control status to idle       GET       /gopro/camera/control/set_ui_controller?p=0       \\&gt;= v01.20.00                 Set Camera Control Status       Set camera control status to external_control       GET       /gopro/camera/control/set_ui_controller?p=2       \\&gt;= v01.20.00                 Set Date/Time       Set date/time to 2022-01-02 03:04:05       GET       /gopro/camera/set_date_time?date=2022_1_2&time=3_4_5       \\&gt;= v01.30.00                 Set shutter       Shutter: on       GET       /gopro/camera/shutter/start       ✔                 Set shutter       Shutter: off       GET       /gopro/camera/shutter/stop       ✔                 Stream: Start       Start preview stream       GET       /gopro/camera/stream/start       ✔                 Stream: Stop       Stop preview stream       GET       /gopro/camera/stream/stop       ✔                 Webcam: Exit       Exit webcam mode       GET       /gopro/webcam/exit       ✔                 Webcam: Preview       Start preview stream       GET       /gopro/webcam/preview       ✔                 Webcam: Start       Start webcam       GET       /gopro/webcam/start       ✔                 Webcam: Start       Start webcam (res: 1080, fov: wide)       GET       /gopro/webcam/start?res=12&fov=0       ✔                 Webcam: Status       Get webcam status       GET       /gopro/webcam/status       ✔                 Webcam: Stop       Stop webcam       GET       /gopro/webcam/stop       ✔                 Webcam: Version       Get webcam api version       GET       /gopro/webcam/version       ✔                 Wired USB       Disable wired usb control       GET       /gopro/camera/control/wired_usb?p=0       \\&gt;= v01.30.00                 Wired USB       Enable wired usb control       GET       /gopro/camera/control/wired_usb?p=1       \\&gt;= v01.30.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#commands-quick-reference",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Settings",
            "excerpt": "GoPro cameras have hundreds of setting options to choose from, all of which can be set using a single endpoint. The endpoint is configured with a setting id and an option value. Note that setting option values are not globally unique. While most option values are enumerated values, some are complex bitmasked values.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#settings",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Settings Quick Reference",
            "excerpt": "Below is a table of setting options detailing how to set every option supported by Open GoPro cameras.  ✔ Indicates support for all Open GoPro firmware versions.  ❌ Indicates a lack of support for all Open GoPro firmware versions.  >= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ                   Setting ID       Setting       Option       HTTP Method       Endpoint       HERO10 Black                 2       Resolution       Set video resolution (id: 2) to 4k (id: 1)       GET       /gopro/camera/setting?setting=2&amp;option=1       ✔                 2       Resolution       Set video resolution (id: 2) to 2.7k (id: 4)       GET       /gopro/camera/setting?setting=2&amp;option=4       ✔                 2       Resolution       Set video resolution (id: 2) to 2.7k 4:3 (id: 6)       GET       /gopro/camera/setting?setting=2&amp;option=6       ✔                 2       Resolution       Set video resolution (id: 2) to 1080 (id: 9)       GET       /gopro/camera/setting?setting=2&amp;option=9       ✔                 2       Resolution       Set video resolution (id: 2) to 4k 4:3 (id: 18)       GET       /gopro/camera/setting?setting=2&amp;option=18       ✔                 2       Resolution       Set video resolution (id: 2) to 5k 4:3 (id: 25)       GET       /gopro/camera/setting?setting=2&amp;option=25       ✔                 2       Resolution       Set video resolution (id: 2) to 5.3k (id: 100)       GET       /gopro/camera/setting?setting=2&amp;option=100       ✔                 3       Frames Per Second       Set video fps (id: 3) to 240 (id: 0)       GET       /gopro/camera/setting?setting=3&amp;option=0       ✔                 3       Frames Per Second       Set video fps (id: 3) to 120 (id: 1)       GET       /gopro/camera/setting?setting=3&amp;option=1       ✔                 3       Frames Per Second       Set video fps (id: 3) to 100 (id: 2)       GET       /gopro/camera/setting?setting=3&amp;option=2       ✔                 3       Frames Per Second       Set video fps (id: 3) to 60 (id: 5)       GET       /gopro/camera/setting?setting=3&amp;option=5       ✔                 3       Frames Per Second       Set video fps (id: 3) to 50 (id: 6)       GET       /gopro/camera/setting?setting=3&amp;option=6       ✔                 3       Frames Per Second       Set video fps (id: 3) to 30 (id: 8)       GET       /gopro/camera/setting?setting=3&amp;option=8       ✔                 3       Frames Per Second       Set video fps (id: 3) to 25 (id: 9)       GET       /gopro/camera/setting?setting=3&amp;option=9       ✔                 3       Frames Per Second       Set video fps (id: 3) to 24 (id: 10)       GET       /gopro/camera/setting?setting=3&amp;option=10       ✔                 3       Frames Per Second       Set video fps (id: 3) to 200 (id: 13)       GET       /gopro/camera/setting?setting=3&amp;option=13       ✔                 43       Webcam Digital Lenses       Set webcam digital lenses (id: 43) to wide (id: 0)       GET       /gopro/camera/setting?setting=43&amp;option=0       ✔                 43       Webcam Digital Lenses       Set webcam digital lenses (id: 43) to narrow (id: 2)       GET       /gopro/camera/setting?setting=43&amp;option=2       ✔                 43       Webcam Digital Lenses       Set webcam digital lenses (id: 43) to superview (id: 3)       GET       /gopro/camera/setting?setting=43&amp;option=3       ✔                 43       Webcam Digital Lenses       Set webcam digital lenses (id: 43) to linear (id: 4)       GET       /gopro/camera/setting?setting=43&amp;option=4       ✔                 59       Auto Power Down       Set auto power down (id: 59) to never (id: 0)       GET       /gopro/camera/setting?setting=59&amp;option=0       ✔                 59       Auto Power Down       Set auto power down (id: 59) to 5 min (id: 4)       GET       /gopro/camera/setting?setting=59&amp;option=4       ✔                 59       Auto Power Down       Set auto power down (id: 59) to 15 min (id: 6)       GET       /gopro/camera/setting?setting=59&amp;option=6       ✔                 59       Auto Power Down       Set auto power down (id: 59) to 30 min (id: 7)       GET       /gopro/camera/setting?setting=59&amp;option=7       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to wide (id: 0)       GET       /gopro/camera/setting?setting=121&amp;option=0       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to narrow (id: 2)       GET       /gopro/camera/setting?setting=121&amp;option=2       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to superview (id: 3)       GET       /gopro/camera/setting?setting=121&amp;option=3       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to linear (id: 4)       GET       /gopro/camera/setting?setting=121&amp;option=4       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to max superview (id: 7)       GET       /gopro/camera/setting?setting=121&amp;option=7       ✔                 121       Video Digital Lenses       Set video digital lenses (id: 121) to linear + horizon leveling (id: 8)       GET       /gopro/camera/setting?setting=121&amp;option=8       ✔                 122       Photo Digital Lenses       Set photo digital lenses (id: 122) to narrow (id: 19)       GET       /gopro/camera/setting?setting=122&amp;option=19       ✔                 122       Photo Digital Lenses       Set photo digital lenses (id: 122) to max superview (id: 100)       GET       /gopro/camera/setting?setting=122&amp;option=100       ✔                 122       Photo Digital Lenses       Set photo digital lenses (id: 122) to wide (id: 101)       GET       /gopro/camera/setting?setting=122&amp;option=101       ✔                 122       Photo Digital Lenses       Set photo digital lenses (id: 122) to linear (id: 102)       GET       /gopro/camera/setting?setting=122&amp;option=102       ✔                 123       Time Lapse Digital Lenses       Set time lapse digital lenses (id: 123) to narrow (id: 19)       GET       /gopro/camera/setting?setting=123&amp;option=19       ✔                 123       Time Lapse Digital Lenses       Set time lapse digital lenses (id: 123) to max superview (id: 100)       GET       /gopro/camera/setting?setting=123&amp;option=100       ✔                 123       Time Lapse Digital Lenses       Set time lapse digital lenses (id: 123) to wide (id: 101)       GET       /gopro/camera/setting?setting=123&amp;option=101       ✔                 123       Time Lapse Digital Lenses       Set time lapse digital lenses (id: 123) to linear (id: 102)       GET       /gopro/camera/setting?setting=123&amp;option=102       ✔                 128       Media Format       Set media format (id: 128) to time lapse video (id: 13)       GET       /gopro/camera/setting?setting=128&amp;option=13       ✔                 128       Media Format       Set media format (id: 128) to time lapse photo (id: 20)       GET       /gopro/camera/setting?setting=128&amp;option=20       ✔                 128       Media Format       Set media format (id: 128) to night lapse photo (id: 21)       GET       /gopro/camera/setting?setting=128&amp;option=21       ✔                 128       Media Format       Set media format (id: 128) to night lapse video (id: 26)       GET       /gopro/camera/setting?setting=128&amp;option=26       ✔                 134       Anti-Flicker       Set setup anti flicker (id: 134) to 60hz (id: 2)       GET       /gopro/camera/setting?setting=134&amp;option=2       ✔                 134       Anti-Flicker       Set setup anti flicker (id: 134) to 50hz (id: 3)       GET       /gopro/camera/setting?setting=134&amp;option=3       ✔                 162       Max Lens       Set max lens (id: 162) to off (id: 0)       GET       /gopro/camera/setting?setting=162&amp;option=0       \\&gt;= v01.20.00                 162       Max Lens       Set max lens (id: 162) to on (id: 1)       GET       /gopro/camera/setting?setting=162&amp;option=1       \\&gt;= v01.20.00                 173       Video Performance Mode       Set video performance mode (id: 173) to maximum video performance (id: 0)       GET       /gopro/camera/setting?setting=173&amp;option=0       \\&gt;= v01.16.00                 173       Video Performance Mode       Set video performance mode (id: 173) to extended battery (id: 1)       GET       /gopro/camera/setting?setting=173&amp;option=1       \\&gt;= v01.16.00                 173       Video Performance Mode       Set video performance mode (id: 173) to tripod / stationary video (id: 2)       GET       /gopro/camera/setting?setting=173&amp;option=2       \\&gt;= v01.16.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#settings-quick-reference",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Camera Capabilities",
            "excerpt": "Camera capabilities usually change from one camera to another and often change from one release to the next. Below are documents that detail whitelists for basic video settings for every supported camera release.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#camera-capabilities",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Note about Dependency Ordering and Blacklisting",
            "excerpt": "Capability documents define supported camera states. Each state is comprised of a set of setting options that are presented in dependency order. This means each state is guaranteed to be attainable if and only if the setting options are set in the order presented. Failure to adhere to dependency ordering may result in the camera's blacklist rules rejecting a set-setting command.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#note-about-dependency-ordering-and-blacklisting",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Example",
            "excerpt": "Camera       Command 1       Command 2       Command 3       Command 4       Command 5       Guaranteed Valid?                 HERO10 Black       Res: 1080       Anti-Flicker: 60Hz (NTSC)       FPS: 240       FOV: Wide       Hypersmooth: OFF       ✔                 HERO10 Black       FPS: 240       Anti-Flicker: 60Hz (NTSC)       Res: 1080       FOV: Wide       Hypersmooth: OFF       ❌           In the example above, the first set of commands will always work for basic video presets such as Standard.     In the second example, suppose the camera's Video Resolution was previously set to 4K. If the user tries to set Video FPS to 240, it will fail because 4K/240fps is not supported.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#example",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Capability Documents",
            "excerpt": "Documents       Product       Release                 capabilities.xlsx capabilities.json       HERO10 Black       v01.30.00                 v01.20.00                 v01.16.00                 v01.10.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#capability-documents",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Spreadsheet Format",
            "excerpt": "The capabilities spreadsheet contains worksheets for every supported release. Each row in a worksheet represents a whitelisted state and is presented in dependency order as outlined above.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#spreadsheet-format",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: JSON Format",
            "excerpt": "The capabilities JSON contains a set of whitelist states for every supported release. Each state is comprised of a list of objects that contain setting and option IDs necessary to construct set-setting commands and are given in dependency order as outlined above.     Below is a simplified example of the capabilities JSON file; a formal schema is also available here: capabilities_schema.json    ``` {     \"(PRODUCT_NAME)\": {         \"(RELEASE_VERSION)\": {             \"states\": [                 [                     {\"setting_name\": \"(str)\", \"setting_id\": (int), \"option_name\": \"(str)\", \"option_id\": (int)},                     ...                 ],                 ...             ],         },         ...     },     ... } ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#json-format",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Media",
            "excerpt": "The camera provides an endpoint to query basic details about media captured on the sdcard.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#media",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Chapters",
            "excerpt": "All GoPro cameras break longer videos into chapters. GoPro cameras currently limit file sizes on sdcards to 4GB for both FAT32 and exFAT file systems. This limitation is most commonly seen when recording longer (10+ minute) videos. In practice, the camera will split video media into chapters named Gqccmmmm.MP4 (and ones for THM/LRV) such that:     q: Quality Level (X: Extreme, H: High, M: Medium, L: Low) cc: Chapter Number (01-99) mmmm: Media ID (0001-9999)    When media becomes chaptered, the camera increments subsequent Chapter Numbers while leaving the Media ID unchanged. For example, if the user records a long High-quality video that results in 4 chapters, the files on the sdcard may look like the following:    ``` -rwxrwxrwx@ 1 gopro  123456789  4006413091 Jan  1 00:00 GH010078.MP4 -rwxrwxrwx@ 1 gopro  123456789       17663 Jan  1 00:00 GH010078.THM -rwxrwxrwx@ 1 gopro  123456789  4006001541 Jan  1 00:00 GH020078.MP4 -rwxrwxrwx@ 1 gopro  123456789       17357 Jan  1 00:00 GH020078.THM -rwxrwxrwx@ 1 gopro  123456789  4006041985 Jan  1 00:00 GH030078.MP4 -rwxrwxrwx@ 1 gopro  123456789       17204 Jan  1 00:00 GH030078.THM -rwxrwxrwx@ 1 gopro  123456789   756706872 Jan  1 00:00 GH040078.MP4 -rwxrwxrwx@ 1 gopro  123456789       17420 Jan  1 00:00 GH040078.THM -rwxrwxrwx@ 1 gopro  123456789   184526939 Jan  1 00:00 GL010078.LRV -rwxrwxrwx@ 1 gopro  123456789   184519787 Jan  1 00:00 GL020078.LRV -rwxrwxrwx@ 1 gopro  123456789   184517614 Jan  1 00:00 GL030078.LRV -rwxrwxrwx@ 1 gopro  123456789    34877660 Jan  1 00:00 GL040078.LRV ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#chapters",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Media List Format",
            "excerpt": "The format of the media list is given below.    ``` {     \"id\": \"\",     \"media\": [         {             \"d\": \"\",             \"fs\": [                 {},                 ...             ]         },         ...     ] } ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#media-list-format",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Media List Keys",
            "excerpt": "The outer structure of the media list and the inner structure of individual media items use the keys in the table below.                Key       Description                 b       ID of first member of a group (for grouped media items)                 d       Directory name                 fs       File system. Contains listing of media items in directory                 g       Group ID (if grouped media item)                 id       Media list session identifier                 l       ID of last member of a group (for grouped media items)                 ls       Low resolution video file size                 m       List of missing/deleted group member IDs (for grouped media items)                 media       Contains media info for for each directory (e.g. 100GOPRO/, 101GOPRO/, ...)                 mod       Last modified time (seconds since epoch)                 n       Media filename                 s       Size of (group) media in bytes                 t       Group type (for grouped media items) (b -> burst, c -> continuous shot, n -> night lapse, t -> time lapse)",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#media-list-keys",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Grouped Media Items",
            "excerpt": "In order to minimize the size of the JSON transmitted by the camera, grouped media items such as Burst Photos, Time Lapse Photos, Night Lapse Photos, etc are represented with a single item in the media list with additional keys that allow the user to extrapolate individual filenames for each member of the group.     Filenames for group media items have the form \"GXXXYYYY.ZZZ\" where XXX is the group ID, YYY is the group member ID and ZZZ is the file extension.     For example, take the media list below, which contains a Time Lapse Photo group media item:    ``` {     \"id\": \"2530266050123724003\",     \"media\": [         {             \"d\": \"100GOPRO\",             \"fs\": [                 {                     \"b\": \"8\",                     \"cre\": \"1613669353\",                     \"g\": \"1\",                     \"l\": \"396\",                     \"m\": ['75', '139'],                     \"mod\": \"1613669353\",                     \"n\": \"G0010008.JPG\",                     \"s\": \"773977407\",                     \"t\": \"t\"                 }             ]         }     ] } ```   The first filename in the group is \"G0010008.JPG\" (key: \"n\"). The ID of the first group member in this case is \"008\" (key: \"b\"). The ID of the last group member in this case is \"396\" (key: \"l\"). The IDs of deleted members in this case are \"75\" and \"139\" (key: \"m\") Given this information, the user can extrapolate that the group currently contains     G0010008.JPG, G0010009.JPG, G0010010.JPG, ..., G0010074.JPG, G0010076.JPG, ..., G0010138.JPG, G0010140.JPG, ..., G0010394.JPG, G0010395.JPG. G0010396.JPG",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#grouped-media-items",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Media HiLights",
            "excerpt": "The HiLight Tags feature allows the user to tag moments of interest either during video capture or on existing media.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#media-hilights",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Add/Remove HiLights",
            "excerpt": "Below is a table of all HiLight commands. For details on how to send HiLight commands, see Commands Quick Reference.                   Command       Description                 Media: HiLight (Add)       Video: Add a tag at a specific time offset (ms)Photo: Add a tag                 Media: HiLight (Remove)       Video: Remove a tag at a specific time offset (ms)Photo: Remove tag                 Media: HiLight Moment       Add a tag to the current time offset (ms) while encoding video            Note: Attempting to add a HiLight tag at a time offset that exceeds the duration of the video or removing a non-existent HiLight tag will result in an HTTP/500 error.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#add-remove-hilights",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Get HiLights",
            "excerpt": "Once HiLight tags have been added, they can be queried by calling the Media: Info command; the response content will be JSON that contains HiLight information:                  Media Type       Key       Value                 Photo       hc       HiLight Count                 Video       hc       HiLight Count                 Video       hi       HiLights (list of time offsets in ms)",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#get-hilights",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Example",
            "excerpt": "The JSON sample below shows media that contains three HiLights at time offsets 2502ms, 5839ms, and 11478ms. Note: Photo info will not have an \"hi\":[...] key-value pair.    ``` {   ...,   \"hc\":\"3\",   \"hi\":[2502,5839,11478],   ..., } ```",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#example",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Downloading Media",
            "excerpt": "The URL to download/stream media from the DCIM/ directory on the sdcard is the Base URL plus /videos/DCIM/XXX/YYY where XXX is the directory name within DCIM/ given by the media list and YYY is the target media filename.     For example: Given the following media list:    ``` {     \"id\": \"3586667939918700960\",     \"media\": [         {             \"d\": \"100GOPRO\",             \"fs\": [                 {                     \"n\": \"GH010397.MP4\",                     \"cre\": \"1613672729\",                     \"mod\": \"1613672729\",                     \"glrv\": \"1895626\",                     \"ls\": \"-1\",                     \"s\": \"19917136\"                 },                 {                     \"cre\": \"1614340213\",                     \"mod\": \"1614340213\",                     \"n\": \"GOPR0001.JPG\",                     \"s\": \"6961371\"                 }             ]         }     ] } ```   The URL to download GH010397.MP4 over WiFi would be http://10.5.5.9:8080/videos/DCIM/100GOPRO/GH010397.MP4     The URL to download GOPR0001.JPG over WiFi would be http://10.5.5.9:8080/videos/DCIM/100GOPRO/GOPR0001.JPG",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#downloading-media",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Turbo Transfer",
            "excerpt": "Some cameras support Turbo Transfer mode, which allows media to be downloaded over WiFi more rapidly. This special mode should only be used during media offload. It is recommended that the user check for and--if necessary--disable Turbo Transfer on connect. For details on which cameras are supported and how to enable and disable Turbo Transfer, see Commands Quick Reference.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#turbo-transfer",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Downloading Preview Stream",
            "excerpt": "When the preview stream is started, the camera starts up a UDP client and begins writing MPEG Transport Stream data to the connected client on port 8554. In order to stream and save this data, the user can implement a UDP server that binds to the same port and appends datagrams to a file when they are received.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#downloading-preview-stream",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Camera State",
            "excerpt": "The camera provides multiple types of state, all of which can be queried:     Camera state: Contains information about camera status (photos taken, date, is-camera-encoding, etc) and settings (current video resolution, current frame rate, etc) Preset State: How presets are arranged into preset groups, their titles, icons, settings closely associated with each preset, etc",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#camera-state",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Camera State Format",
            "excerpt": "Camera state is given in the following form:  ``` {     \"status\": {         \"1\": ,         \"2\": ,         ...     },     \"settings: {         \"2\": ,         \"3\": ,         ...     } } ```   Where status X value and setting X value are almost always integer values. See Status Codes table in this document for exceptions.     For status, keys are status codes and values are status values.     For settings, keys are setting IDs, and values are option values",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#camera-state-format",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Status Codes",
            "excerpt": "Below is a table of supported status codes.  ✔ Indicates support for all Open GoPro firmware versions.  ❌ Indicates a lack of support for all Open GoPro firmware versions.  >= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ                   Status ID       Name       Description       Type       Values       HERO10 Black                 1       Internal battery present       Is the system's internal battery present?       boolean       0: False 1: True        ✔                 2       Internal battery level       Rough approximation of internal battery level in bars       integer       0: Zero 1: One 2: Two 3: Three        ✔                 3       External battery present       Is an external battery connected?       boolean       0: False 1: True        ✔                 4       External battery level       External battery power level in percent       percent       0-100       ✔                 6       System hot       Is the system currently overheating?       boolean       0: False 1: True        ✔                 8       System busy       Is the camera busy?       boolean       0: False 1: True        ✔                 9       Quick capture active       Is Quick Capture feature enabled?       boolean       0: False 1: True        ✔                 10       Encoding active       Is the system encoding right now?       boolean       0: False 1: True        ✔                 11       Lcd lock active       Is LCD lock active?       boolean       0: False 1: True        ✔                 13       Video progress counter       When encoding video, this is the duration (seconds) of the video so far; 0 otherwise       integer       *       ✔                 17       Enable       Are Wireless Connections enabled?       boolean       0: False 1: True        ✔                 19       State       The pairing state of the camera       integer       0: Success 1: In Progress 2: Failed 3: Stopped        ✔                 20       Type       The last type of pairing that the camera was engaged in       integer       0: Not Pairing 1: Pairing App 2: Pairing Remote Control 3: Pairing Bluetooth Device        ✔                 21       Pair time       Time (milliseconds) since boot of last successful pairing complete action       integer       *       ✔                 22       State       State of current scan for WiFi Access Points. Appears to only change for CAH-related scans       integer       0: Never started 1: Started 2: Aborted 3: Canceled 4: Completed        ✔                 23       Scan time msec       The time, in milliseconds since boot that the WiFi Access Point scan completed       integer       *       ✔                 24       Provision status       WiFi AP provisioning state       integer       0: Never started 1: Started 2: Aborted 3: Canceled 4: Completed        ✔                 26       Remote control version       Wireless remote control version       integer       *       ✔                 27       Remote control connected       Is a wireless remote control connected?       boolean       0: False 1: True        ✔                 28       Pairing       Wireless Pairing State       integer       *       ✔                 29       Wlan ssid       Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int       string       *       ✔                 30       Ap ssid       Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int       string       *       ✔                 31       App count       The number of wireless devices connected to the camera       integer       *       ✔                 32       Enable       Is Preview Stream enabled?       boolean       0: False 1: True        ✔                 33       Sd status       Primary Storage Status       integer       -1: Unknown 0: OK 1: SD Card Full 2: SD Card Removed 3: SD Card Format Error 4: SD Card Busy 8: SD Card Swapped        ✔                 34       Remaining photos       How many photos can be taken before sdcard is full       integer       *       ✔                 35       Remaining video time       How many minutes of video can be captured with current settings before sdcard is full       integer       *       ✔                 36       Num group photos       How many group photos can be taken with current settings before sdcard is full       integer       *       ✔                 37       Num group videos       Total number of group videos on sdcard       integer       *       ✔                 38       Num total photos       Total number of photos on sdcard       integer       *       ✔                 39       Num total videos       Total number of videos on sdcard       integer       *       ✔                 41       Ota status       The current status of Over The Air (OTA) update       integer       0: Idle 1: Downloading 2: Verifying 3: Download Failed 4: Verify Failed 5: Ready 6: GoPro App: Downloading 7: GoPro App: Verifying 8: GoPro App: Download Failed 9: GoPro App: Verify Failed 10: GoPro App: Ready        ✔                 42       Download cancel request pending       Is there a pending request to cancel a firmware update download?       boolean       0: False 1: True        ✔                 45       Camera locate active       Is locate camera feature active?       boolean       0: False 1: True        ✔                 49       Multi shot count down       The current timelapse interval countdown value (e.g. 5...4...3...2...1...)       integer       *       ✔                 54       Remaining space       Remaining space on the sdcard in Kilobytes       integer       *       ✔                 55       Supported       Is preview stream supported in current recording/flatmode/secondary-stream?       boolean       0: False 1: True        ✔                 56       Wifi bars       WiFi signal strength in bars       integer       *       ✔                 58       Num hilights       The number of hilights in encoding video (set to 0 when encoding stops)       integer       *       ✔                 59       Last hilight time msec       Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)       integer       *       ✔                 60       Next poll msec       The min time between camera status updates (msec). Do not poll for status more often than this       integer       *       ✔                 64       Remaining timelapse time       How many min of Timelapse video can be captured with current settings before sdcard is full       integer       *       ✔                 65       Exposure select type       Liveview Exposure Select Mode       integer       0: Disabled 1: Auto 2: ISO Lock 3: Hemisphere        ✔                 66       Exposure select x       Liveview Exposure Select: y-coordinate (percent)       percent       0-100       ✔                 67       Exposure select y       Liveview Exposure Select: y-coordinate (percent)       percent       0-100       ✔                 68       Gps status       Does the camera currently have a GPS lock?       boolean       0: False 1: True        ✔                 69       Ap state       Is the WiFi radio enabled?       boolean       0: False 1: True        ✔                 70       Internal battery percentage       Internal battery level (percent)       percent       0-100       ✔                 74       Acc mic status       Microphone Accesstory status       integer       0: Microphone mod not connected 1: Microphone mod connected 2: Microphone mod connected and microphone plugged into Microphone mod        ✔                 75       Digital zoom       Digital Zoom level (percent)       percent       0-100       ✔                 76       Wireless band       Wireless Band       integer       0: 2.4 GHz 1: 5 GHz 2: Max        ✔                 77       Digital zoom active       Is Digital Zoom feature available?       boolean       0: False 1: True        ✔                 78       Mobile friendly video       Are current video settings mobile friendly? (related to video compression and frame rate)       boolean       0: False 1: True        ✔                 79       First time use       Is the camera currently in First Time Use (FTU) UI flow?       boolean       0: False 1: True        ✔                 81       Band 5ghz avail       Is 5GHz wireless band available?       boolean       0: False 1: True        ✔                 82       System ready       Is the system ready to accept commands?       boolean       0: False 1: True        ✔                 83       Batt okay for ota       Is the internal battery charged sufficiently to start Over The Air (OTA) update?       boolean       0: False 1: True        ✔                 85       Video low temp alert       Is the camera getting too cold to continue recording?       boolean       0: False 1: True        ✔                 86       Actual orientation       The rotational orientation of the camera       integer       0: 0 degrees (upright) 1: 180 degrees (upside down) 2: 90 degrees (laying on right side) 3: 270 degrees (laying on left side)        ✔                 88       Zoom while encoding       Is this camera capable of zooming while encoding (static value based on model, not settings)       boolean       0: False 1: True        ✔                 89       Current mode       Current flatmode ID       integer       *       ✔                 91       Logs ready       Are system logs ready to be downloaded?       boolean       0: False 1: True        ✔                 93       Active video presets       Current Video Preset (ID)       integer       *       ✔                 94       Active photo presets       Current Photo Preset (ID)       integer       *       ✔                 95       Active timelapse presets       Current Timelapse Preset (ID)       integer       *       ✔                 96       Active presets group       Current Preset Group (ID)       integer       *       ✔                 97       Active preset       Current Preset (ID)       integer       *       ✔                 98       Preset modified       Preset Modified Status, which contains an event ID and a preset (group) ID       integer       *       ✔                 99       Remaining live bursts       How many Live Bursts can be captured before sdcard is full       integer       *       ✔                 100       Num total live bursts       Total number of Live Bursts on sdcard       integer       *       ✔                 101       Capture delay active       Is Capture Delay currently active (i.e. counting down)?       boolean       0: False 1: True        ✔                 102       Media mod mic status       Media mod State       integer       0: Media mod microphone removed 2: Media mod microphone only 3: Media mod microphone with external microphone        ✔                 103       Timewarp speed ramp active       Time Warp Speed       integer       0: 15x 1: 30x 2: 60x 3: 150x 4: 300x 5: 900x 6: 1800x 7: 2x 8: 5x 9: 10x 10: Auto 11: 1x (realtime) 12: 1/2x (slow-motion)        ✔                 104       Linux core active       Is the system's Linux core active?       boolean       0: False 1: True        ✔                 105       Camera lens type       Camera lens type (reflects changes to setting 162)       integer       0: Default 1: Max Lens        ✔                 106       Video hindsight capture active       Is Video Hindsight Capture Active?       boolean       0: False 1: True        ✔                 107       Scheduled preset       Scheduled Capture Preset ID       integer       *       ✔                 108       Scheduled enabled       Is Scheduled Capture set?       boolean       0: False 1: True        ✔                 109       Creating preset       Is the camera in the process of creating a custom preset?       boolean       0: False 1: True        ✔                 110       Media mod status       Media Mode Status (bitmasked)       integer       0: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: False 1: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: True 2: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: False 3: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: True 4: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: False 5: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: True 6: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: False 7: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: True        ✔                 111       Sd rating check error       Does sdcard meet specified minimum write speed?       boolean       0: False 1: True        ✔                 112       Sd write speed error       Number of sdcard write speed errors since device booted       integer       *       ✔                 113       Turbo transfer       Is Turbo Transfer active?       boolean       0: False 1: True        ✔                 114       Camera control status       Camera control status ID       integer       0: Camera Idle: No one is attempting to change camera settings 1: Camera Control: Camera is in a menu or changing settings. To intervene, app must request control 2: Camera External Control: An outside entity (app) has control and is in a menu or modifying settings        ✔                 115       Usb connected       Is the camera connected to a PC via USB?       boolean       0: False 1: True        ✔                 116       Allow control over usb       Camera control over USB state       integer       0: Disabled 1: Enabled        \\&gt;= v01.30.00",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#status-codes",
            "teaser": ''
        },
        {
            "title": "HTTP Specification v2.0: Preset Status Format",
            "excerpt": "Preset Status is returned as JSON, whose content is the serialization of the protobuf message: NotifyPresetStatus. Using Google protobuf APIs, the JSON can be converted back into a programmatic object in the user's language of choice.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/http_2_0#preset-status-format",
            "teaser": ''
        },
        {
            "title": "Open GoPro: ",
            "excerpt": "The Open GoPro API is the primary way for users to interact with a GoPro             camera. The camera provides interfaces to HTTP (wired and wireless) and Bluetooth Low Energy that             allow users to perform command, control, and query actions including, but not             limited to:                                Capture media             Track camera state             Get media list and download files / metadata              Load / edit presets             Configure and use as webcam             Add / remove hilights                                                           Docs                                       Detailed Bluetooth Low Energy (BLE) and HTTP Interface Specifications.                                                    BLE Specs →                                                    HTTP Specs →                                            Tutorials                                       Walk-through tutorials in different languages / frameworks for getting                     started.                                   ✏️ Tutorials →                                            Demos                                       Complete runnable examples in different languages to use as base for                     your project.                                   ⚙️ Demos →",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/#",
            "teaser": ''
        },
        {
            "title": "Tutorials: ",
            "excerpt": "Tutorials  Several walk-through tutorials in different languages / frameworks exist for getting started with Open GoPro.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/#",
            "teaser": ''
        },
        {
            "title": "Tutorials: Python",
            "excerpt": "This set of tutorials is a series of sample python scripts and accompanying .html walk-throughs to implement basic functionality to interact with a GoPro device using Python.  The tutorials support Open GoPro Versions 1.0 and 2.0. They will provide a walk-through to use Python to exercise the Open GoPro Interface using [bleak](https://bleak.readthedocs.io/en/latest/api.html) for Bluetooth Low Energy (BLE) and [requests](https://docs.python-requests.org/en/master/) for HTTP.  These tutorials are meant as an introduction to the Open GoPro specification. There is complete documentation available for [BLE]({% link specs/ble.md %}) and [HTTP]({% link specs/http.md %}) which will be the main source of reference after completing the tutorials.  {% for tutorial in site.python-tutorials %} -   [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }}) {% endfor %}  {% note These are stripped down Python tutorials that are only meant to show the basics. %} For a complete Python SDK that uses [bleak](https://bleak.readthedocs.io/en/latest/) as the backend as well as a cross-platform WiFi backend to easily write Python apps that control the GoPro, see the [Open GoPro Python SDK](https://gopro.github.io/OpenGoPro/python_sdk/)",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/#python",
            "teaser": ''
        },
        {
            "title": "Tutorials: Bash",
            "excerpt": "BlueZ tutorial for Ubuntu using the command line:  {% for tutorial in site.bash-tutorials %} -   [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }}) {% endfor %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/#bash",
            "teaser": ''
        },]