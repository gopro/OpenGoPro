var jekyllStore = [
        {
            "title": "FAQ and Known Issues: ",
            "excerpt": "Frequently Asked Questions (FAQ) If you have somehow stumbled here first, note that there are specifications, demos, and tutorials which expand upon much of the information here. These can be found, among other places, from the home page. Connectivity What is the distance from the camera that BLE will still work? It is standard Bluetooth 4.0 range and it depends on external factors such as: Interference: anything interfering with the signal will shorten the range. The type of device that the camera is connected to: BT classification distinguishes 3 device classes based on their power levels. Depending on the class of the connected device, the range varies from less than 10 meters to 100 meters. Can I connect using WiFi only? Theoretically yes, if you already know the SSID, password, and the camera’s WiFi AP has been enabled. However, practically no because BLE is required in order to discover this information and configure the AP. Can I connect using BLE only? Yes, however there is some functionality that is not possible over BLE such as accessing the media list and downloading files. How to allow third-party devices to automatically discover close-by GoPro cameras? Devices can only be discovered via BLE by scanning for advertising GoPro cameras Multi Camera Setups How many devices can connect to the camera? Simultaneously, only one device can connect at a time. However, the camera stores BLE security keys and other connection information so it is possible to connect multiple devices sequentially. Is there currently a way to connect multiple cameras on the same Wifi network? No. Cameras can only be connected through Wi-Fi by becoming an access point itself (generating its own Wi-Fi network), not as a peripheral. What is the time offset between multiple cameras executing the same command? In cases when camera sync is important, we recommend using the USB connection, which minimizes the variance among devices. The time drift among cameras connected by USB cable to the same host will be up to ~35ms. Using BLE for that purpose will further increase it. Is there a way to precisely time sync cameras so the footage can be aligned during post-processing? The cameras set their time via GPS. By default, the camera seeks GPS at the beginning of every session, but this can be hindered by typical limitations of GPS signals. Additionally, there are two advanced options that require GoPro Labs firmware installed on the camera. The best bet is multi-cam GPS sync. Another option is precise time calibration via a dynamic QR scan from a smartphone or PC. Streaming What are the differences between the streaming options for GoPros? There are currently 3 different options on how to stream out of GoPro cameras. They are available either via Wi-Fi, USB, or both.   : Wifi :   : USB :       ViewFinder Preview LiveStream ViewFinder Preview Webcam Preview Webcam Orientation Floating or Fixed Landscape facing up Floating or Fixed Landscape: Floating or Fixed Landscape: Floating or Fixed Streaming Protocols UDP (MPEG-TS) RTMP UDP (MPEG-TS) UDP (MPEG-TS) UDP (MPEG-TS) \\         RTSP RTSP Connection Protocol Wifi - AP Mode WiFi - STA Mode NCM NCM NCM Resolution 480p, 720p 480p, 720p, 1080p 480p, 720p 720p, 1080p 720p, 1080p Frame Rate 30 30 30 30 30 Bitrate 2.5 - 4 mbps 0.8 - 8 mbps 2.5 - 4 mbps 6 mbps 6 mbps \\   depending on model configurable depending on model     Stabilization Basic Stabilization HyperSmooth or none Basic Stabilization None None Image Quality Basic Same as recorded content Basic Basic Same as recorded content Minimum Latency 210 ms &gt; 100ms (un-stabilized) 210 ms 210 ms 210 ms \\     &gt; 1,100ms (stabilized)       Audio None Stereo None None None Max Stream Time 150 minutes (720p on fully 85 minutes (720p on fully Unlimited (with external Unlimited(with external Unlimited (with external\\   charged Enduro battery) charged Enduro battery) power via USB) power via USB) power via USB How to achieve low latency feed streaming onto displays? The stream has a minimum latency of about 210ms. If you are seeing latency higher than that, we often find that as a result of using off-the-shelf libraries like ffmpeg which adds its own buffering. For preview and framing use cases, we don’t recommend using the live streaming RTMP protocol because it adds unnecessary steps in the pipeline, and puts the camera in the streaming preset, which offers little other control. A low latency streaming demo is available in the demos. How do I minimize latency of video preview with FFPLAY? FFPLAY by default will buffer remote streams. You can minimize the buffer using: --no-cache (receiving side) `-fflags nobuffer” (sender). However, the best latency can be achieved by building your own pipeline or ffmpegs library for decoding the bytes. Users should be able to achieve about 200-300 ms latency on the desktop and possibly optimize lower than that. How to view the video stream in VLC? To view the stream in VLC, you need to open network stream udp://@0.0.0.0:8554. You will still see latency because VLC uses its own caching. Power What are the power requirements for GoPro if connected over USB? All cameras have minimum power requirements, as specified here. As long as the power is supplied, cameras will be fully functional with or without an internal battery. Removing the battery and running on USB power alone will improve thermal performance and runtime. If you are seeing issues with insufficient power and have a charger with correct specs, the problems likely stem from low quality cables or low-quality adapters that are not able to consistently provide advertised amperage. We have encountered USB-C cables manufactured with poor quality control that transfer enough power only when their connectors face one side up, but not the other. We recommend using only high-quality components that deliver the correct power output How to enable automatic power on and off in wired setups? Cameras cannot be switched on remotely over USB, or “woken up” remotely after they “go to sleep”. The best workaround for this is via the GoPro Labs firmware that forces the camera to automatically switch on as soon as it detects USB power and switch off when the powering stops. Refer to the WAKE command here. Metadata Can I use the GPS track from the camera in real time? No. The GPS track on the camera as well as other metadata is not available until the file is written and saved. If the objective is to add metadata to the stream, currently the only option is to pull GPS data from another device (phone, wearable,… ) and sync it to the video feed. What can be accessed in the metadata file? Metadata exists as a proprietary GPMF (GoPro Metadata Format) and can be extracted from the file via API commands separately for GPS, Telemetry data, or the entire metadata container. The following data points can be extracted: Camera settings (Exposure time, ISO, Sensor Gain, White balance) Date and Time IMU: GPS, gyroscope, and accelerometer Smile detection Audio levels Face detection in bounding boxes Scene Classifiers (water, urban, vegetation, snow, beach, indoor) Is there a way to change the file names or otherwise classify my video file? Currently there are two options to do that, and both require GoPro Labs firmware. The stock firmware doesn’t provide that option. With GoPro Labs installed, you can either inject metadata into the file (and extract it later with the GPMF parser) or use custom naming for the file. Is there a way to add time stamps to the video files and mark specific moments? Open GoPro users can add time stamped markers, called “Hilights”, to flag specific moments in the video. Hilights can be injected into the video in the real time and then extracted for analytics or other post-processing purposes. The same Hilights are used in GoPro’s auto-editing engine Quik to determine the most interesting moments in the video. General Which cameras are supported by Open GoPro? The answer at a high level is &gt;= Hero 9. However, there are also certain firmware requirements. For a complete answer, see the Specification. How to get the remaining timelapse capability? First check the value of Setting 128. Then depending on whether this is Photo or Video, use: Status 34 (Remaining photos) Status 35 (Remaining videos) Camera Logic Do commands operate as priority-wise or time-related? The cameras use first-in, first-out logic. Is there an option to send the commands in cyclic format instead of sending requests for each command? If you want to receive information asynchronously, it is possible via registering for BLE notifications. See an example (tracking battery) in the Python SDK. Troubleshooting If you are able to consistently reproduce a problem, please file a bug on Github Issues Why is the camera not advertising? If you have not yet paired to the camera with the desired device, then you need to first set the camera into pairing mode (Connections-&gt;Connect Device-&gt;Quick App). If you have already paired, then the camera should be advertising and ready to connect. If it is not advertising, it is possible you are already connected to it from a previous session. To be sure, power cycle both the camera and the peer device. Workaround for intermittent Wifi AP Connection failure On &gt;= Hero 11, try disabling and then re-enabling the camera’s Wifi AP using the AP Control BLE Command Known Issues Relevant to All Supported Cameras Webcam does not enter idle mode once plugged in The webcam status will be wrongly reported as IDLE instead of OFF after a new USB connection. The best workaround for this is to call Webcam Start followed by Webcam Stop after connecting USB in order to make the webcam truly IDLE and thus willing to accept setting changes. Intermittent failure to connect to the cameras Wifi Access Point On rare occasions, connections to the camera’s Wifi AP will continuously fail until the camera is reset. It is possible to workaround this as described in Troubleshooting Spurious Protobuf Notifications sent once camera is connected in Station mode Once the camera has been connected in station mode (STA), it will start sending protobuf notifications with action ID 0xFF. These should be ignored. Hero 11 (v01.10.00) Specific Wired Communication is broken after update mode This is fixed by Resetting Connections and then re-pairing. Hero 13 (v01.10.00) Specific Webcam endpoints are broken. The following endpoints will always return 500 error status: Start Webcam Exit Webcam Preview Webcam Camera is not discoverable via MDNS. The camera does not advertise the _gopro-web service.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/faq#"
        },
        {
            "title": "Open GoPro: ",
            "excerpt": "Getting Started Open GoPro is an API for interacting with GoPro cameras that is developed and managed directly by GoPro. It provides developers and companies with an easy-to-use programming interface and helps integrate the cameras into their ecosystems. The API works with off-the-shelf cameras with standard firmware, is free-to-use under MIT license, and publicly available online on GitHub. Docs Detailed Bluetooth Low Energy (BLE) and HTTP Interface Specifications. BLE Spec→ HTTP Spec → Tutorials Walk-through tutorials in different languages / frameworks for getting started. ✏️ Tutorials → Demos Complete runnable examples in different languages to use as base for your project. ⚙️ Demos → Compatibility Open GoPro API is supported on all camera models since Hero 9 with the following firmware version requirements: Camera Minimum FW Version HERO13 Black v01.10.00 HERO12 Black v01.10.00 HERO11 Black Mini v01.10.00 HERO11 Black v01.10.00 HERO10 Black v01.10.00 HERO9 Black v01.70.00 While we strive to provide the same API functionality and logic for all newly launched cameras, minor changes are sometimes necessary. These are typically a consequence of HW component upgrades or improving or optimizing FW architecture. Therefore support for some functions and commands might be model-specific. This is described in the compatibility tables in the documentation. Interfaces Users can interact with the camera over BLE, WiFi, or wired USB. Both Wifi and USB are operated through HTTP server with identical commands. It is important to note that due to hard constraints of power and the hardware design, some commands in Wi-Fi are not available in BLE, and vice-versa. Bluetooth Low Energy (BLE) BLE is the fastest way to control the cameras and allow command and control functionality. BLE advertising is used for initial camera pairing. BLE is a requirement for any type of Wireless control since camera WiFi must be enabled upon each connection via BLE. WiFi Wi-Fi needs to be switched on by a BLE command. Thanks to bigger data throughput than BLE, Wi-Fi allows not only for command &amp; control, but also for video streaming and media manipulation. Our newest cameras can act either as a Wi-Fi Access Point (creating its own Wi-fi network to which other devices connect) or as a Station (connecting as IP endpoint to any existing Wi-Fi network, similar to any other IP camera). API users can choose which mode to use. For more information, see the HTTP Specification. USB The USB connection can provide both data transfer and power to the camera. The power provided by the USB is sufficient for the camera to run indefinitely without the internal battery. However, the wired connection doesn’t allow for programmatic power on and off. Camera needs to be switched on manually or via BLE, and after the camera goes to sleep, it must be “woken up” again with a button press or via BLE. For monitoring and other use cases where the camera must be operated and switched on and off only via USB cable, there is a workaround with the Labs firmware - more detail in the FAQ. Control Camera and Record Remotely Here is a summary of currently supported per-interface features: Feature BLE WiFi USB Retrieve Camera State ✔️ ✔️ ✔️ Change Settings / Mode ✔️ ✔️ ✔️ Encode (Press shutter) ✔️ ✔️ ✔️ Stream Video   ✔️ ✔️ Media Management   ✔️ ✔️ Metadata Extraction   ✔️ ✔️ Camera Connect / Wake ✔️     BLE, WiFi, and USB can be used to change settings and modes, start and stop capture, query remaining battery life, SD card capacity, or camera status (such as “is it recording?”).  Most command-and-control functionality is disabled while the camera is recording video or is otherwise busy. There are 3 main recording modes for the cameras: photo, video, and timelapse. Within each mode, one can choose different frame rates, resolutions and FOV options. Note that not all cameras have all 3 recording modes, not all settings combinations are available for all camera models. The specification section links to json and xls files that show all available setting combinations per camera model. Stream Video Besides recording, the cameras can also stream video feed. The API provides 3 different ways to stream videos directly from the cameras, either via USB or wireless connection. Stream Type Description WiFi USB Record while Streaming Stream Initiation Wi-Fi Mode(s) Preview Moderate video quality, primarily for framing         \\ Stream Low latency stabilization ✔️ ✔️ Hero 12 [HTTP](https://gopro.github.io/OpenGoPro/httptag/Preview-Stream) AP, STA \\   Low power consumption     and later     Webcam Cinematic video quality         AP, STA \\ Mode Optional low latency stabilization ✔️ ✔️   [HTTP](https://gopro.github.io/OpenGoPro/httptag/Webcam)   Live Cinematic video quality         STA \\ Stream Optional hypersmooth stabilization ✔️   ✔️ [BLE Protobuf](https://gopro.github.io/OpenGoPro/ble/features/live_streaming.html)   Each of the streaming types has different resolutions, bit rates, imaging pipelines, and different levels of configurability. Refer to the FAQ. Manipulate and Transfer Media Files When the camera records video, time lapse, or photo, the media is saved on the SD card with filenames according to the GoPro File Naming Convention. The cameras always record two versions of each video file Full resolution based on the selected settings (.mp4) Low resolution video proxy (.lrv) that can be used for editing or other operations where file size matters. The lrv file type can be renamed to mp4 and used for playback or further editing. Both versions exist in the same folder on the SD card. In addition, the cameras generate a thumbnail image (.thm) for each media file. The thm file type can be changed to jpeg if required. All three file types can be accessed, deleted, or copied via API commands. Extract Metadata GoPro cameras write metadata in each file, using a proprietary GPMF format. The metadata contains information including gyroscope, accelerometer, GPS, imaging-specific metadata, and several computed metrics such as scene classification. The metadata file cannot be edited or read while the camera is recording but can be accessed after the file has been written either entirely or selectively for a specific metric such as GPS. Use Multiple Cameras Simultaneously Controlling multiple cameras from one client is supported via BLE, Wifi, and USB with varying functionality depending on the protocol used. Refer to the table below. Protocol Available Functionality Notes BLE Command and control of several cameras Each camera can connect only to one BLE-enabled device at a time WiFi Command and control in Wi-fi station mode (COHN) COHN is available only from HERO12 onwards \\   Webcam and Preview Stream in Wi-fi station mode (COHN) Live-streaming (RTMP) RTMP stream must be initiated via BLE USB Command and control and streaming via Webcam mode Available only from HERO11 onward Use GoPro Cloud and Editing Engine The GoPro ecosystem includes a multitude of ways to edit, store, and replay content which are currently available for end-users as a part of paid subscription programs. Even when integrated into your ecosystem, GoPro cameras can take advantage of cloud backup and editing tools provided by GoPro including auto-upload to the cloud, automatic editing, and native live streaming. The GoPro cloud interface has been tailored to the needs of individual consumers. If you are interested in commercial usage, reach out to our business development team.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/#"
        },
        {
            "title": "Tutorials: ",
            "excerpt": "This set of tutorials is a series of sample scripts / files and accompanying .html walk-throughs to implement basic functionality to interact with a GoPro device using the following languages: - Python - Kotlin - More to come! The tutorials only support Open GoPro Version 2.0 and must be run on a [supported camera]({{site.baseurl}}/ble/index.htmlsupported-cameras). They will provide walk-throughs and sample code to use the relevant language / framework to exercise the Open GoPro Interface using Bluetooth Low Energy (BLE) and HTTP over WiFi. {% warning %} The tutorials are only tested on the latest camera / firmware combination. This is only an issue in cases where capabilities change between cameras such as setting options. {% endwarning %} The tutorials are meant as an introduction to the Open GoPro specification. They are not a substitute for the complete [BLE]({{site.baseurl}}/ble/index.html) and [HTTP]({{site.baseurl}}/http) specifications which will be your main source of reference after completing the tutorials. {% for tutorial in site.tutorials %} - [{{ tutorial.title }}]({{ tutorial.permalink | prepend: site.baseurl }}) {% endfor %}",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/#"
        },
        {
            "title": "Tutorial 1: Connect BLE: ",
            "excerpt": "This tutorial will provide a walk-through to connect to the GoPro camera via Bluetooth Low Energy (BLE). Requirements Hardware A GoPro camera that is supported by Open GoPro python kotlin One of the following systems: Windows 10, version 16299 (Fall Creators Update) or greater Linux distribution with BlueZ &gt;= 5.43 OS X/macOS support via Core Bluetooth API, from at least OS X version 10.11 An Android Device supporting SDK &gt;= 33 Software python kotlin Python &gt;= 3.9 and &lt; 3.12 must be installed. See this Python installation guide. Android Studio &gt;= 2022.1.1 (Electric Eel) Overview / Assumptions python kotlin This tutorial will use bleak to control the OS’s Bluetooth Low Energy (BLE). The Bleak BLE controller does not currently support autonomous pairing for the BlueZ backend. So if you are using BlueZ (i.e. Ubuntu, RaspberryPi, etc.), you need to first pair the camera from the command line. One way to do this is to use bluetoothctl. The bleak module is based on asyncio which means that its awaitable functions need to be called from an async coroutine. In order to do this, all of the code below should be running in an async function. We accomplish this in the tutorial scripts by making main async as such: import asyncio async def main() -&gt; None: Put our code here if __name__ == \"__main__\": asyncio.run(main()) These are stripped down Python tutorials that are only meant to show the basics. For a complete Python SDK that uses bleak as the backend as well as a cross-platform WiFi backend to easily write Python apps that control the GoPro, see the Open GoPro Python SDK This tutorial will provide a set of Kotlin tutorials to demonstrate Open GoPro Functionality. The tutorials are provided as a single Android Studio project targeted to run on an Android device. The tutorials are only concerned with application-level demonstrations of the Open GoPro API and therefore do not prioritize the following: UI: The tutorial project only contains a minimal UI to select, implement, and view logs for each tutorial Android architecture / best practices: the project architecture is designed to encapsulate Kotlin functionality to easily display per-tutorial functionality Android-specific requirements: permission handling, adapter enabling, etc are implemented in the project but not documented in the tutorials BLE / Wifi (HTTP) functionality: A simple BLE API is included in the project and will be touched upon in the tutorials. However, the focus of the tutorials is not on how the BLE API is implemented as a real project would likely use a third-party library for this such as Kable See the Punchthrough tutorials for Android BLE-Specific tutorials These tutorials assume familiarity and a base level of competence with: Android Studio Bluetooth Low Energy JSON HTTP Setup python kotlin This set of tutorials is accompanied by a Python package consisting of scripts separated by tutorial module. These can be found on Github. Once the Github repo has been cloned or downloaded to your local machine, the package can be installed as follows: Enter the python tutorials directory at $INSTALL/demos/python/tutorial/ where $INSTALL is the top level of the Open GoPro repo where it exists on your local machine Use pip to install the package (in editable mode in case you want to test out some changes): pip install -e . While it is out of the scope of this tutorial to describe, it is recommended to install the package in to a virtual environment in order to isolate system dependencies. You can test that installation was successful by viewing the installed package’s information: $ pip show open-gopro-python-tutorials Name: open-gopro-python-tutorials Version: 0.0.3 Summary: Open GoPro Python Tutorials Home-page: https://github.com/gopro/OpenGoPro Author: Tim Camise Author-email: gopro.com License: MIT Location: c:\\users\\tim\\gopro\\opengopro\\demos\\python\\tutorial Requires: bleak, requests Required-by: This set of tutorials is accompanied by an Android Studio project consisting of, among other project infrastructure, Kotlin files separated by tutorial module. The project can be found on Github. Once the Github repo has been cloned or downloaded to your local machine, open the project in Android studio. At this point you should be able to build and load the project to your Android device. The project will not work on an emulated device since BLE can not be emulated. Just Show me the Demo!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 1 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements You can test connecting to your camera through BLE using the following script: python ble_connect.py See the help for parameter definitions: $ python ble_connect.py --help usage: ble_connect.py [-h] [-i IDENTIFIER] Connect to a GoPro camera, pair, then enable notifications. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to The Kotlin file for this tutorial can be found on Github. To perform the tutorial, run the Android Studio project, select “Tutorial 1” from the dropdown and click on “Perform.” Perform Tutorial 1 This will start the tutorial and log to the screen as it executes. When the tutorial is complete, click “Exit Tutorial” to return to the Tutorial selection screen. Basic BLE Tutorial This tutorial will walk through the process of connecting to a GoPro via BLE. This same connect functionality will be used as a foundation for all future BLE tutorials. Here is a summary of the sequence that will be described in detail in the following sections: GoProOpen GoPro user deviceGoProOpen GoPro user deviceScanningConnectedalt[If not Previously Paired]PairedReady to CommunicateAdvertisingAdvertisingConnectPair RequestPair ResponseEnable Notifications on Characteristic 1Enable Notifications on Characteristic 2Enable Notifications on Characteristic ..Enable Notifications on Characteristic N Advertise First, we need to ensure the camera is discoverable (i.e. it is advertising). Follow the per-camera steps here. The screen should appear as such: Camera is discoverable. Scan Next, we must scan to discover the advertising GoPro Camera. python kotlin We will do this using bleak. Let’s initialize an empty dict that will store discovered devices, indexed by name: Map of devices indexed by name devices: Dict[str, BleakDevice] = {} We’re then going to scan for all devices. We are passing a scan callback to bleak in order to also find non-connectable scan responses. We are keeping any devices that have a device name. Scan callback to also catch nonconnectable scan responses def _scan_callback(device: BleakDevice, _: Any) -&gt; None: Add to the dict if not unknown if device.name and device.name != \"Unknown\": devices[device.name] = device Now discover and add connectable advertisements for device in await BleakScanner.discover(timeout=5, detection_callback=_scan_callback): if device.name != \"Unknown\" and device.name is not None: devices[device.name] = device Now we can search through the discovered devices to see if we found a GoPro. Any GoPro device name will be structured as GoPro XXXX where XXXX is the last four digits of your camera’s serial number. If you have renamed your GoPro to something other than the default, you will need to update the below steps accordingly. First, we define a regex which is either “GoPro “ followed by any four alphanumeric characters if no identifier was passed, or the identifier if it exists. In the demo ble_connect.py, the identifier is taken from the command-line arguments. token = re.compile(identifier or r\"GoPro [A-Z0-9]{4}\") Now we build a list of matched devices by checking if each device’s name includes the token regex. matched_devices: List[BleakDevice] = [] Now look for our matching device(s) matched_devices = [device for name, device in devices.items() if token.match(name)] Due to potential RF interference and the asynchronous nature of BLE advertising / scanning, it is possible that the advertising GoPro will not be discovered by the scanning PC in one scan. Therefore, you may need to redo the scan (as ble_connect.py does) until a GoPro is found. That is, matched_device must contain at least one device. Similarly, connection establishment can fail for reasons out of our control. Therefore, the connection process is also wrapped in retry logic. Here is an example of the log from ble_connect.py of scanning for devices. Note that this includes several rescans until the devices was found. $ python ble_connect.py INFO:root:Scanning for bluetooth devices... INFO:root: Discovered: INFO:root: Discovered: TR8600 seri INFO:root:Found 0 matching devices. INFO:root: Discovered: INFO:root: Discovered: TR8600 seri INFO:root: Discovered: GoPro Cam INFO:root: Discovered: GoPro 0456 INFO:root:Found 1 matching devices. Among other devices, you should see GoPro XXXX where XXXX is the last four digits of your camera’s serial number. First let’s define a filter that will be used to find GoPro device advertisements. We do this by filtering on the GoPro Service UUID that is included in all GoPro advertisements: private val scanFilters = listOf&lt;ScanFilter&gt;( ScanFilter.Builder().setServiceUuid(ParcelUuid.fromString(GOPRO_UUID)).build() ) We then send this to the BLE API and collect events from the SharedFlow that it returns. We take the first event emitted from this SharedFlow and notify (via a Channel) that a GoPro advertiser has been found, store the GoPro’s BLE address, and stop the scan. ble.startScan(scanFilters).onSuccess { scanResults -&gt; val deviceChannel: Channel&lt;BluetoothDevice&gt; = Channel() // Collect scan results CoroutineScope(Dispatchers.IO).launch { scanResults.collect { scanResult -&gt; // We will take the first discovered gopro deviceChannel.send(scanResult.device) } } // Wait to receive the scan result goproAddress = deviceChannel.receive().address ble.stopScan(scanResults) } At this point, the GoPro’s BLE address is stored (as a string) in goproAddress. Here is an example log output from this process: Scanning for GoPro's Received scan result: GoPro 0992 Found GoPro: GoPro 0992 Connect Now that we have discovered at least one GoPro device to connect to, the next step is to establish a BLE connection to the camera. python kotlin We're just taking the first device if there are multiple. device = matched_devices[0] client = BleakClient(device) await client.connect(timeout=15) An example output of this is shown here where we can see that the connection has successfully been established as well as the GoPro’s BLE MAC address.: INFO:root:Establishing BLE connection to EF:5A:F6:13:E6:5A: GoPro 0456... INFO:bleak.backends.dotnet.client:Services resolved for BleakClientDotNet (EF:5A:F6:13:E6:5A) INFO:root:BLE Connected! ble.connect(goproAddress) At this point, the BLE connection is established but there is more setup to be done before we are ready to communicate. Pair The GoPro has encryption-protected characteristics which require us to pair before writing to them. Therefore now that we are connected, we need to attempt to pair. python kotlin try: await client.pair() except NotImplementedError: This is expected on Mac pass Not all OS’s allow pairing (at this time) but some require it. Rather than checking for the OS, we are just catching the exception when it fails. Rather than explicitly request pairing, we rely on the fact that Android will automatically start the pairing process if you try to read a characteristic that requires encryption. To do this, we read the Wifi AP Password characteristic. First we discover all characteristics (this will also be needed later when enabling notifications): ble.discoverCharacteristics(goproAddress) This API will discover the characteristics over-the-air but not return them here. They are stored to the ble object for later access via the servicesOf method. Then we read the relevant characteristic to trigger pairing: ble.readCharacteristic(goproAddress, GoProUUID.WIFI_AP_PASSWORD.uuid) At this point a pairing popup should occur on the Android Device. Select “Allow Pairing” to continue. Here is an example log output from this process: Discovering characteristics Discovered 9 services for F7:5B:5D:81:64:1B Service 00001801-0000-1000-8000-00805f9b34fb Characteristics: |-- Service 00001800-0000-1000-8000-00805f9b34fb Characteristics: |--00002a00-0000-1000-8000-00805f9b34fb: READABLE |--00002a01-0000-1000-8000-00805f9b34fb: READABLE |--00002a04-0000-1000-8000-00805f9b34fb: READABLE ... |------00002902-0000-1000-8000-00805f9b34fb: EMPTY |--b5f90082-aa8d-11e3-9046-0002a5d5c51b: WRITABLE |--b5f90083-aa8d-11e3-9046-0002a5d5c51b: NOTIFIABLE |------00002902-0000-1000-8000-00805f9b34fb: EMPTY |--b5f90084-aa8d-11e3-9046-0002a5d5c51b: NOTIFIABLE |------00002902-0000-1000-8000-00805f9b34fb: EMPTY Service 00001804-0000-1000-8000-00805f9b34fb Characteristics: |--00002a07-0000-1000-8000-00805f9b34fb: READABLE Pairing Read characteristic b5f90003-aa8d-11e3-9046-0002a5d5c51b : value: 66:3F:54:2D:38:35:72:2D:4E:35:63 Once paired, the camera should beep and display “Connection Successful”. This pairing process only needs to be done once. On subsequent connections, the devices will automatically re-establish encryption using stored keys. That is, they are “bonded.” Enable Notifications As specified in the Open GoPRo BLE Spec, we must enable notifications for a given characteristic to receive responses from it. To enable notifications, we loop over each characteristic in each service and enable the characteristic for notification if it has notify properties: python kotlin It is necessary to define a notification handler to pass to the bleak start_notify method. Since we only care about connecting to the device in this tutorial (and not actually receiving data), we are just passing an empty function. A future tutorial will demonstrate how to use this meaningfully. for service in client.services: for char in service.characteristics: if \"notify\" in char.properties: await client.start_notify(char, notification_handler) In the following example output, we can see that notifications are enabled for each characteristic that is notifiable. INFO:root:Enabling notifications... INFO:root:Enabling notification on char 00002a19-0000-1000-8000-00805f9b34fb INFO:root:Enabling notification on char b5f90073-aa8d-11e3-9046-0002a5d5c51b INFO:root:Enabling notification on char b5f90075-aa8d-11e3-9046-0002a5d5c51b INFO:root:Enabling notification on char b5f90077-aa8d-11e3-9046-0002a5d5c51b INFO:root:Enabling notification on char b5f90079-aa8d-11e3-9046-0002a5d5c51b INFO:root:Enabling notification on char b5f90092-aa8d-11e3-9046-0002a5d5c51b INFO:root:Enabling notification on char b5f90081-aa8d-11e3-9046-0002a5d5c51b INFO:root:Enabling notification on char b5f90083-aa8d-11e3-9046-0002a5d5c51b INFO:root:Enabling notification on char b5f90084-aa8d-11e3-9046-0002a5d5c51b INFO:root:Done enabling notifications INFO:root:BLE Connection is ready for communication. ble.servicesOf(goproAddress).onSuccess { services -&gt; services.forEach { service -&gt; service.characteristics.forEach { char -&gt; if (char.isNotifiable()) { ble.enableNotification(goproAddress, char.uuid) } } } } Here is an example log output from this process: Enabling notifications Enabling notifications for 00002a19-0000-1000-8000-00805f9b34fb Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Enabling notifications for b5f90073-aa8d-11e3-9046-0002a5d5c51b Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Enabling notifications for b5f90075-aa8d-11e3-9046-0002a5d5c51b Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Enabling notifications for b5f90077-aa8d-11e3-9046-0002a5d5c51b Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Enabling notifications for b5f90079-aa8d-11e3-9046-0002a5d5c51b Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Enabling notifications for b5f90092-aa8d-11e3-9046-0002a5d5c51b Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Enabling notifications for b5f90081-aa8d-11e3-9046-0002a5d5c51b Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Enabling notifications for b5f90083-aa8d-11e3-9046-0002a5d5c51b Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Enabling notifications for b5f90084-aa8d-11e3-9046-0002a5d5c51b Wrote to descriptor 00002902-0000-1000-8000-00805f9b34fb Bluetooth is ready for communication! The characteristics that correspond to each UUID listed in the log can be found in the Open GoPro API. These will be used in a future tutorial to send data. Once the notifications are enabled, the GoPro BLE initialization is complete and it is ready to communicate via BLE. Quiz time! 📚 ✏️ How often is it necessary to pair? A: Pairing must occur every time to ensure safe BLE communication. B: We never need to pair as the GoPro does not require it to communicate. C: Pairing only needs to occur once as the keys will be automatically re-used for future connections. Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is C. Pairing is only needed once (assuming neither side deletes the keys). If the GoPro deletes the keys (via Connections-&gt;Reset Connections), the devices will need to re-pair. Troubleshooting Device not connecting If the connection is not starting, it is likely because the camera is not advertising. This can be due to either: The camera is not in pairing mode. Ensure that this is achieved as done in the advertise section. The devices never disconnected from the previous session so are thus already connected. If this is the case, perform the “Complete System Reset” shown below. Complete System Reset BLE is a fickle beast. If at any point it is impossible to discover or connect to the camera, perform the following. Reset the camera by choosing Connections –&gt; Reset Connections Use your OS’s bluetooth settings GUI to remove / unpair the Gopro Restart the procedure detailed above Logs python kotlin The demo program has enabled bleak logs and is also using the default python logging module to write its own logs. To enable more bleak logs, follow bleak’s troubleshooting section. The demo program is using Timber. It is piping all log messages to the UI but they are also available in the logcat window and can be filtered using: package:mine tag:GP_. Good Job! Congratulations 🤙 You can now successfully connect to the GoPro via BLE and prepare it to receive / send data. To see how to send commands, you should advance to the next tutorial.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/connect-ble#"
        },
        {
            "title": "Tutorial 2: Send BLE TLV Commands: ",
            "excerpt": "This document will provide a walk-through tutorial to use the Open GoPro BLE Interface to send Type-Length-Value (TLV)commands and receive TLV responses. Commands in this sense are operations that are initiated by either: Writing to the Command Request UUID and receiving responses via the Command Response UUID. Writing to the Setting UUID and receiving responses via the Setting Response UUID A list of TLV commands can be found in the [Command ID Table]/OpenGoPro/ble/protocol/id_tables.htmlcommand-ids). This tutorial only considers sending these as one-off commands. That is, it does not consider state management / synchronization when sending multiple commands. This will be discussed in a future lab. Requirements It is assumed that the hardware and software requirements from the connecting BLE tutorial are present and configured correctly. It is suggested that you have first completed the connecting BLE tutorial before going through this tutorial. Just Show me the Demo(s)!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 2 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements Set Shutter You can test sending the Set Shutter command to your camera through BLE using the following script: $ python ble_command_set_shutter.py See the help for parameter definitions: $ python ble_command_set_shutter.py --help usage: ble_command_set_shutter.py [-h] [-i IDENTIFIER] Connect to a GoPro camera, set the shutter on, wait 2 seconds, then set the shutter off. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to Load Preset Group You can test sending the Load Preset Group command to your camera through BLE using the following script: $ python ble_command_load_group.py See the help for parameter definitions: $ python ble_command_load_group.py --help usage: ble_command_load_group.py [-h] [-i IDENTIFIER] Connect to a GoPro camera, then change the Preset Group to Video. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to Set the Video Resolution You can test sending the Set Video Resolution command to your camera through BLE using the following script: $ python ble_command_set_resolution.py See the help for parameter definitions: $ python ble_command_set_resolution.py --help usage: ble_command_set_resolution.py [-h] [-i IDENTIFIER] Connect to a GoPro camera, then change the resolution to 1080. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to Set the Frames Per Second (FPS) You can test sending the Set FPS command to your camera through BLE using the following script: $ python ble_command_set_fps.py See the help for parameter definitions: $ python ble_command_set_fps.py --help usage: ble_command_set_fps.py [-h] [-i IDENTIFIER] Connect to a GoPro camera, then attempt to change the fps to 240. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to The Kotlin file for this tutorial can be found on Github. To perform the tutorial, run the Android Studio project, select “Tutorial 2” from the dropdown and click on “Perform.” This requires that a GoPro is already connected via BLE, i.e. that Tutorial 1 was already run. You can check the BLE status at the top of the app. Perform Tutorial 2 This will start the tutorial and log to the screen as it executes. When the tutorial is complete, click “Exit Tutorial” to return to the Tutorial selection screen. Setup We must first connect as was discussed in the connecting BLE tutorial. In this case, however, we are defining a functional (albeit naive) notification handler that will: Log byte data and handle that the notification was received on Check if the response is what we expected Set an event to notify the writer that the response was received This is a very simple handler; response parsing will be expanded upon in the next tutorial. python kotlin async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -&gt; None: logger.info(f'Received response at handle {characteristic.handle}: {data.hex(\":\")}') If this is the correct handle and the status is success, the command was a success if client.services.characteristics[characteristic.handle].uuid == response_uuid and data[2] == 0x00: logger.info(\"Command sent successfully\") Anything else is unexpected. This shouldn't happen else: logger.error(\"Unexpected response\") Notify the writer event.set() The event used above is a simple synchronization event that is only alerting the writer that a notification was received. For now, we’re just checking that the handle matches what is expected and that the status (third byte) is success (0x00). private val receivedData: Channel&lt;UByteArray&gt; = Channel() private fun naiveNotificationHandler(characteristic: UUID, data: UByteArray) { if ((characteristic == GoProUUID.CQ_COMMAND_RSP.uuid)) { CoroutineScope(Dispatchers.IO).launch { receivedData.send(data) } } } private val bleListeners by lazy { BleEventListener().apply { onNotification = ::naiveNotificationHandler } } The handler is simply verifying that the response was received on the correct UIUD and then notifying the received data. We are registering this notification handler with the BLE API before sending any data requests as such: ble.registerListener(goproAddress, bleListeners) There is much more to the synchronization and data parsing than this but this will be discussed in future tutorials. Command Overview All commands follow the same procedure: Write to the relevant request UUID Receive confirmation from GoPro (via notification from relevant response UUID) that request was received. GoPro reacts to command The notification response only indicates that the request was received and whether it was accepted or rejected. The relevant behavior of the GoPro must be observed to verify when the command’s effects have been applied. Here is the procedure from power-on to finish: GoProOpen GoPro user deviceGoProOpen GoPro user devicedevices are connected as in Tutorial 1Command Request (Write to Request UUID)Command Response (via notification to Response UUID)Apply effects of command when able Sending Commands Now that we are are connected, paired, and have enabled notifications (registered to our defined callback), we can send some commands. First, we need to define the UUIDs to write to / receive responses from, which are: python kotlin We’ll define these and any others used throughout the tutorials and store them in a GoProUUID class: class GoProUuid: COMMAND_REQ_UUID = GOPRO_BASE_UUID.format(\"0072\") COMMAND_RSP_UUID = GOPRO_BASE_UUID.format(\"0073\") SETTINGS_REQ_UUID = GOPRO_BASE_UUID.format(\"0074\") SETTINGS_RSP_UUID = GOPRO_BASE_UUID.format(\"0075\") QUERY_REQ_UUID = GOPRO_BASE_UUID.format(\"0076\") QUERY_RSP_UUID = GOPRO_BASE_UUID.format(\"0077\") WIFI_AP_SSID_UUID = GOPRO_BASE_UUID.format(\"0002\") WIFI_AP_PASSWORD_UUID = GOPRO_BASE_UUID.format(\"0003\") NETWORK_MANAGEMENT_REQ_UUID = GOPRO_BASE_UUID.format(\"0091\") NETWORK_MANAGEMENT_RSP_UUID = GOPRO_BASE_UUID.format(\"0092\") We’re using the GOPRO_BASE_UUID string imported from the module’s __init__.py to build these. These are defined in the GoProUUID class: const val GOPRO_UUID = \"0000FEA6-0000-1000-8000-00805f9b34fb\" const val GOPRO_BASE_UUID = \"b5f9%s-aa8d-11e3-9046-0002a5d5c51b\" enum class GoProUUID(val uuid: UUID) { WIFI_AP_PASSWORD(UUID.fromString(GOPRO_BASE_UUID.format(\"0003\"))), WIFI_AP_SSID(UUID.fromString(GOPRO_BASE_UUID.format(\"0002\"))), CQ_COMMAND(UUID.fromString(GOPRO_BASE_UUID.format(\"0072\"))), CQ_COMMAND_RSP(UUID.fromString(GOPRO_BASE_UUID.format(\"0073\"))), CQ_SETTING(UUID.fromString(GOPRO_BASE_UUID.format(\"0074\"))), CQ_SETTING_RSP(UUID.fromString(GOPRO_BASE_UUID.format(\"0075\"))), CQ_QUERY(UUID.fromString(GOPRO_BASE_UUID.format(\"0076\"))), CQ_QUERY_RSP(UUID.fromString(GOPRO_BASE_UUID.format(\"0077\"))); } Set Shutter The first command we will be sending is Set Shutter, which at byte level is: Command Bytes Set Shutter Off 0x03 0x01 0x01 0x00 Set Shutter On 0x03 0x01 0x01 0x01 Now, let’s write the bytes to the “Command Request” UUID to turn the shutter on and start encoding! python kotlin request_uuid = GoProUuid.COMMAND_REQ_UUID event.clear() request = bytes([3, 1, 1, 1]) await client.write_gatt_char(request_uuid.value, request, response=True) await event.wait() Wait to receive the notification response We make sure to clear the synchronization event before writing, then pend on the event until it is set in the notification callback. val setShutterOnCmd = ubyteArrayOf(0x03U, 0x01U, 0x01U, 0x01U) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, setShutterOnCmd) // Wait to receive the notification response, then check its status checkStatus(receivedData.receive()) We’re waiting to receive the data from the queue that is posted to in the notification handler when the response is received. You should hear the camera beep and it will either take a picture or start recording depending on what mode it is in. Also note that we have received the “Command Status” notification response from the Command Response characteristic since we enabled its notifications in Enable Notifications. This can be seen in the demo log: python kotlin Setting the shutter on Writing to GoProUuid.COMMAND_REQ_UUID: 03:01:01:01 Received response at GoProUuid.COMMAND_RSP_UUID: 02:01:00 Command sent successfully Writing characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b ==&gt; 03:01:01:01 Wrote characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 02:01:00 Received response on b5f90073-aa8d-11e3-9046-0002a5d5c51b: 02:01:00 Command sent successfully As expected, the response was received on the correct UUID and the status was “success” (third byte == 0x00). If you are recording a video, continue reading to set the shutter off: We’re waiting 2 seconds in case you are in video mode so that we can capture a 2 second video. python kotlin await asyncio.sleep(2) request_uuid = GoProUuid.COMMAND_REQ_UUID request = bytes([3, 1, 1, 0]) event.clear() await client.write_gatt_char(request_uuid.value, request, response=True) await event.wait() Wait to receive the notification response This will log in the console as follows: Setting the shutter off Writing to GoProUuid.COMMAND_REQ_UUID: 03:01:01:00 Received response at GoProUuid.COMMAND_RSP_UUID: 02:01:00 Command sent successfully delay(2000) val setShutterOffCmd = ubyteArrayOf(0x03U, 0x01U, 0x01U, 0x00U) // Wait to receive the notification response, then check its status checkStatus(receivedData.receive()) We’re waiting to receive the data from the queue that is posted to in the notification handler when the response is received. This will log as such: Setting the shutter off Writing characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b ==&gt; 03:01:01:00 Wrote characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 02:01:00 Received response on b5f90073-aa8d-11e3-9046-0002a5d5c51b: 02:01:00 Command sent successfully Load Preset Group The next command we will be sending is Load Preset Group, which is used to toggle between the 3 groups of presets (video, photo, and timelapse). At byte level, the commands are: Command Bytes Load Video Preset Group 0x04 0x3E 0x02 0x03 0xE8 Load Photo Preset Group 0x04 0x3E 0x02 0x03 0xE9 Load Timelapse Preset Group 0x04 0x3E 0x02 0x03 0xEA Now, let’s write the bytes to the “Command Request” UUID to change the preset group to Video! python kotlin request_uuid = GoProUuid.COMMAND_REQ_UUID request = bytes([0x04, 0x3E, 0x02, 0x03, 0xE8]) event.clear() await client.write_gatt_char(request_uuid.value, request, response=True) await event.wait() Wait to receive the notification response We make sure to clear the synchronization event before writing, then pend on the event until it is set in the notification callback. val loadPreset = ubyteArrayOf(0x04U, 0x3EU, 0x02U, 0x03U, 0xE8U) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, loadPreset) // Wait to receive the notification response, then check its status checkStatus(receivedData.receive()) We’re waiting to receive the data from the queue that is posted to in the notification handler when the response is received. You should hear the camera beep and move to the Video Preset Group. You can tell this by the logo at the top middle of the screen: Load Preset Group Also note that we have received the “Command Status” notification response from the Command Response characteristic since we enabled its notifications in Enable Notifications. This can be seen in the demo log: python kotlin Loading the video preset group... Sending to GoProUuid.COMMAND_REQ_UUID: 04:3e:02:03:e8 Received response at GoProUuid.COMMAND_RSP_UUID: 02:3e:00 Command sent successfully Loading Video Preset Group Writing characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b ==&gt; 04:3E:02:03:E8 Wrote characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 02:3E:00 Received response on b5f90073-aa8d-11e3-9046-0002a5d5c51b: 02:3E:00 Command status received Command sent successfully As expected, the response was received on the correct UUID and the status was “success” (third byte == 0x00). Set the Video Resolution The next command we will be sending is Set Setting to set the Video Resolution. This is used to change the value of the Video Resolution setting. It is important to note that this only affects video resolution (not photo). Therefore, the Video Preset Group must be active in order for it to succeed. This can be done either manually through the camera UI or by sending Load Preset Group. This resolution only affects the current video preset. Each video preset can have its own independent values for video resolution. Here are some of the byte level commands for various video resolutions. Command Bytes Set Video Resolution to 1080 0x03 0x02 0x01 0x09 Set Video Resolution to 2.7K 0x03 0x02 0x01 0x04 Set Video Resolution to 5K 0x03 0x02 0x01 0x18 Now, let’s write the bytes to the “Setting Request” UUID to change the video resolution to 1080! python kotlin request_uuid = GoProUuid.COMMAND_REQ_UUID request = bytes([0x03, 0x02, 0x01, 0x09]) event.clear() await client.write_gatt_char(request_uuid.value, request, response=True) await event.wait() Wait to receive the notification response We make sure to clear the synchronization event before writing, then pend on the event until it is set in the notification callback. val setResolution = ubyteArrayOf(0x03U, 0x02U, 0x01U, 0x09U) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, setResolution) // Wait to receive the notification response, then check its status checkStatus(receivedData.receive()) We’re waiting to receive the data from the queue that is posted to in the notification handler when the response is received. You should see the video resolution change to 1080 in the pill in the bottom-middle of the screen: Set Video Resolution Also note that we have received the “Command Status” notification response from the Command Response characteristic since we enabled its notifications in Enable Notifications. This can be seen in the demo log: python kotlin Setting the video resolution to 1080 Writing to GoProUuid.SETTINGS_REQ_UUID: 03:02:01:09 Received response at GoProUuid.SETTINGS_RSP_UUID: 02:02:00 Command sent successfully Setting resolution to 1080 Writing characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b ==&gt; 03:02:01:09 Wrote characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 02:02:00 Received response on b5f90073-aa8d-11e3-9046-0002a5d5c51b: 02:02:00 Command status received Command sent successfully As expected, the response was received on the correct UUID and the status was “success” (third byte == 0x00). If the Preset Group was not Video, the status will not be success. Set the Frames Per Second (FPS) The next command we will be sending is Set Setting to set the FPS. This is used to change the value of the FPS setting. It is important to note that this setting is dependent on the video resolution. That is, certain FPS values are not valid with certain resolutions. In general, higher resolutions only allow lower FPS values. Other settings such as the current anti-flicker value may further limit possible FPS values. Futhermore, these capabilities all vary by camera. Check the camera capabilities to see which FPS values are valid for given use cases. Therefore, for this step of the tutorial, it is assumed that the resolution has been set to 1080 as in Set the Video Resolution. Here are some of the byte level commands for various FPS values. Command Bytes Set FPS to 24 0x03 0x03 0x01 0x0A Set FPS to 60 0x03 0x03 0x01 0x05 Set FPS to 240 0x03 0x03 0x01 0x00 Note that the possible FPS values can vary based on the Camera that is being operated on. Now, let’s write the bytes to the “Setting Request” UUID to change the FPS to 240! python kotlin request_uuid = GoProUuid.COMMAND_REQ_UUID request = bytes([0x03, 0x03, 0x01, 0x00]) event.clear() await client.write_gatt_char(request_uuid.value, request, response=True) await event.wait() Wait to receive the notification response We make sure to clear the synchronization event before writing, then pend on the event until it is set in the notification callback. val setFps = ubyteArrayOf(0x03U, 0x03U, 0x01U, 0x00U) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, setFps) // Wait to receive the notification response, then check its status checkStatus(receivedData.receive()) We’re waiting to receive the data from the queue that is posted to in the notification handler when the response is received. You should see the FPS change to 240 in the pill in the bottom-middle of the screen: Set FPS Also note that we have received the “Command Status” notification response from the Command Response characteristic since we enabled its notifications in Enable Notifications.. This can be seen in the demo log: python kotlin Setting the fps to 240 Writing to GoProUuid.SETTINGS_REQ_UUID: 03:03:01:00 Received response at GoProUuid.SETTINGS_RSP_UUID: 02:03:00 Command sent successfully Setting the FPS to 240 Writing characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b ==&gt; 03:03:01:00 Wrote characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 02:03:00 Received response on b5f90073-aa8d-11e3-9046-0002a5d5c51b: 02:03:00 Command status received Command sent successfully As expected, the response was received on the correct UUID and the status was “success” (third byte == 0x00). If the video resolution was higher, for example 5K, this would fail. Quiz time! 📚 ✏️ Which of the following is not a real preset group? A: Timelapse B: Photo C: Burst D: Video Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is C. There are 3 preset groups (Timelapse, Photo, and Video). These can be set via the Load Preset Group command. True or False: Every combination of resolution and FPS value is valid. A: True B: False Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is B. Each resolution can support all or only some FPS values. You can find out which resolutions support which FPS values by consulting the capabilities section of the spec. True or False: Every camera supports the same combination of resolution and FPS values. A: True B: False Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is B. The only way to know what values are supported is to first check the Open GoPro version. See the relevant version of the BLE or WiFi spec to see what is supported. Troubleshooting See the first tutorial’s troubleshooting section. Good Job! Congratulations 🤙 You can now send any of the other BLE commands detailed in the Open GoPro documentation in a similar manner. To see how to parse responses, proceed to the next tutorial.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/send-ble-commands#"
        },
        {
            "title": "Tutorial 3: Parse BLE TLV Responses: ",
            "excerpt": "This document will provide a walk-through tutorial to implement the Open GoPro Interface to parse BLE Type-Length-Value (TLV) Responses. Besides TLV, some BLE operations instead return protobuf responses. These are not considered here and will be discussed in a future tutorial This tutorial will provide an overview of how to handle responses of both single and multiple packets lengths, then give parsing examples for each case, and finally create Response and TlvResponse classes that will be reused in future tutorials. Requirements It is assumed that the hardware and software requirements from the connecting BLE tutorial are present and configured correctly. It is suggested that you have first completed the connect and sending commands tutorials before going through this tutorial. Just Show me the Demo(s)!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 3 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements Parsing a One Packet TLV Response You can test parsing a one packet TLV response with your camera through BLE using the following script: $ python ble_command_get_version.py See the help for parameter definitions: $ python ble_command_get_version.py --help usage: ble_command_get_version.py [-h] [-i IDENTIFIER] Connect to a GoPro camera via BLE, then get the Open GoPro version. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to Parsing Multiple Packet TLV Responses You can test parsing multiple packet TVL responses with your camera through BLE using the following script: $ python ble_command_get_hardware_info.py See the help for parameter definitions: $ python ble_command_get_hardware_info.py --help usage: ble_command_get_hardware_info.py [-h] [-i IDENTIFIER] Connect to a GoPro camera via BLE, then get its hardware info. options: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to The Kotlin file for this tutorial can be found on Github. To perform the tutorial, run the Android Studio project, select “Tutorial 3” from the dropdown and click on “Perform.” This requires that a GoPro is already connected via BLE, i.e. that Tutorial 1 was already run. You can check the BLE status at the top of the app. Perform Tutorial 3 This will start the tutorial and log to the screen as it executes. When the tutorial is complete, click “Exit Tutorial” to return to the Tutorial selection screen. Setup We must first connect as was discussed in the connecting BLE tutorial. When enabling notifications, one of the notification handlers described in the following sections will be used. Response Overview In the preceding tutorials, we have been using a very simple response handling procedure where the notification handler simply checks that the UUID is the expected UUID and that the status byte of the response is 0 (Success). This has been fine since we were only performing specific operations where this works and we know that the sequence always appears as such (connection sequence left out for brevity): GoProOpen GoPro user deviceGoProOpen GoPro user devicedevices are connected as in Tutorial 1Write to characteristicNotification Response (MSB == 0 (start)) In actuality, responses can be more complicated. As described in the BLE Spec, responses can be be comprised of multiple packets where each packet is &lt;= 20 bytes such as: GoProOpen GoPro user deviceGoProOpen GoPro user devicedevices are connected as in Tutorial 1Write to characteristicNotification Response (MSB == 0 (start))Notification Response (MSB == 1 (continuation))Notification Response (MSB == 1 (continuation))Notification Response (MSB == 1 (continuation)) This requires the implementation of accumulating and parsing algorithms which will be described below. Parsing a One Packet TLV Response This section will describe how to parse one packet (&lt;= 20 byte) responses. A one-packet response is formatted as such: Header (length) Operation ID Status Response 1 byte 1 byte 1 bytes Length - 2 bytes Responses with Payload Length 0 These are the only responses that we have seen thus far through the first 2 tutorials. They return a status but have a 0 length additional response. For example, consider Set Shutter. It returned a response of: 02:01:00 This equates to: Header (length) Command ID Status Response 1 byte 1 byte 1 bytes Length - 2 bytes 0x02 0x01 == Set Shutter 0x00 == Success (2 -2 = 0 bytes) We can see how this response includes the status but no additional response data. This type of response will be used for most Commands and Setting Responses as seen in the previous tutorial. Responses with Payload However, there are some operations that do return additional response data. These are identified by the presence of parameters in their Response documentation as shown in the red box here: Response With Payload In this tutorial, we will walk through creating a simple parser to parse the Open GoPro Get Version Command which is an example of such an operation. It is important to always query the version after connecting in order to know which API is supported. See the relevant version of the BLE and / or WiFi spec for more details about each version. First, we send the Get Version Command to the Command Request UUID in the same manner as commands were sent in the previous tutorial: python kotlin request_uuid = GoProUuid.COMMAND_REQ_UUID request = bytes([0x01, 0x51]) await client.write_gatt_char(request_uuid.value, request, response=True) await event.wait() Wait to receive the notification response We receive a response at the expected handle (as a TLV Response). This is logged as: Getting the Open GoPro version... Writing to GoProUuid.COMMAND_REQ_UUID: 01:51 Received response GoProUuid.COMMAND_RSP_UUID: 06:51:00:01:02:01:00 val versionRequest = ubyteArrayOf(0x01U, 0x51U) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, versionRequest) var tlvResponse = receivedResponses.receive() as Response.Tlv We then receive a response at the expected handle. This is logged as: This is logged as such: Getting the Open GoPro version Writing characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b ==&gt; 01:51 Wrote characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 06:51:00:01:02:01:00 Received response on CQ_COMMAND_RSP Received packet of length 6. 0 bytes remaining This response equates to: Header (length) Command ID Status Response 1 byte 1 byte 1 bytes Length - 2 bytes 0x06 0x51 == Get Version 0x00 == Success 0x01 0x02 0x01 0x00 We can see that this response payload contains 4 additional bytes that need to be parsed. Using the information from the Get Version Documentation, we know to parse this as: Byte Meaning 0x01 Length of Major Version Number 0x02 Major Version Number of length 1 byte 0x01 Length of Minor Version Number 0x00 Minor Version Number of length 1 byte We implement this as follows. First, we parse the length, command ID, and status from the first 3 bytes of the response. The remainder is stored as the payload. This is all of the common parsing across TLV Responses. Each individual response will document how to further parse the payload. python kotlin The snippets of code included in this section are taken from the notification handler First byte is the length of this response. length = data[0] Second byte is the ID command_id = data[1] Third byte is the status status = data[2] The remainder is the payload payload = data[3 : length + 1] The snippets of code included in this section are taken from the Response.Tlv.Parse method // Parse header bytes tlvResponse.parse() ... open fun parse() { require(isReceived) id = rawBytes[0].toInt() status = rawBytes[1].toInt() // Store remainder as payload payload = rawBytes.drop(2).toUByteArray() } From the response definition, we know these parameters are one byte each and equate to the major and the minor version so let’s print them (and all of the other response information) as such: python kotlin major_length = payload[0] payload.pop(0) major = payload[:major_length] payload.pop(major_length) minor_length = payload[0] payload.pop(0) minor = payload[:minor_length] logger.info(f\"The version is Open GoPro {major[0]}.{minor[0]}\") logger.info(f\"Received a response to {command_id=} with {status=}: version={major[0]}.{minor[0]}\") which shows on the log as: Received a response to command_id=81 with status=0, payload=01:02:01:00 The version is Open GoPro 2.0 The snippets of code included in this section are taken from the OpenGoProVersion from_bytes method. This class is a simple data class to contain the Get Version information. var buf = data.toUByteArray() val minorLen = buf[0].toInt() buf = buf.drop(1).toUByteArray() val minor = buf.take(minorLen).toInt() val majorLen = buf[0].toInt() buf = buf.drop(1).toUByteArray() val major = buf.take(majorLen).toInt() return OpenGoProVersion(minor, major) which shows on the log as such: Received response: ID: 81, Status: 0, Payload: 01:02:01:00 Got the Open GoPro version successfully: 2.0 Quiz time! 📚 ✏️ What is the maximum size of an individual notification response packet at the Open GoPro application layer? A: 20 bytes B: 256 bytes C: There is no maximum size Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is A. Responses can be composed of multiple packets where each packet is at maximum 20 bytes. What is the maximum amount of bytes that one response can be composed of? A: 20 bytes B: 256 bytes C: There is no maximum size Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is C. There is no limit on the amount of packets that can comprise a response. How many packets are command responses composed of? A: Always 1 packet B: Always multiple packets. C: A variable amount of packets depending on the payload size Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is C. Command responses are sometimes 1 packet (just returning the status). Other times, command responses also contain a payload and can thus be multiple packets if the payload is big enough (i.e. in the case of Get Hardware Info). This is described in the per-command documentation in the BLE spec. How many packets are setting responses comprised of? A: Always 1 packet B: Always multiple packets. C: A variable amount of packets depending on the payload size Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is A. Settings Responses only ever contain the response status. Parsing Multiple Packet TLV Responses This section will describe parsing TLV responses that contain more than one packet. It will first describe how to accumulate such responses and then provide a parsing example. We will be creating small Response and TlvResponse classes that will be re-used for future tutorials. Accumulating the Response The first step is to accumulate the multiple packets into one response. Whereas for all tutorials until now, we have just used the header bytes of the response as the length, we now must completely parse the headers as they are defined, reproduced for reference here: Byte 1 Byte 2 (optional) Byte 3 (optional) 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 0: Start 00: General Message Length: 5 bits 0: Start 01: Extended (13-bit) Message Length: 13 bits 0: Start 10: Extended (16-bit) Message Length: 16 bits 0: Start 11: Reserved 1: Continuation The basic accumulation algorithm (which is implemented in the Response.Accumulate method) is as follows: Is the continuation bit set? python kotlin The example script that will be walked through for this section is ble_command_get_hardware_info.py. if buf[0] &amp; CONT_MASK: buf.pop(0) else: ... if (data.first().and(Mask.Continuation.value) == Mask.Continuation.value) { buf = buf.drop(1).toUByteArray() // Pop the header byte } else { // This is a new packet ... No, the continuation bit was not set. Therefore create new response, then get its length. python kotlin This is a new packet so start with an empty byte array self.bytes = bytearray() hdr = Header((buf[0] &amp; HDR_MASK) &gt;&gt; 5) if hdr is Header.GENERAL: self.bytes_remaining = buf[0] &amp; GEN_LEN_MASK buf = buf[1:] elif hdr is Header.EXT_13: self.bytes_remaining = ((buf[0] &amp; EXT_13_BYTE0_MASK) &lt;&lt; 8) + buf[1] buf = buf[2:] elif hdr is Header.EXT_16: self.bytes_remaining = (buf[1] &lt;&lt; 8) + buf[2] buf = buf[3:] // This is a new packet so start with empty array packet = ubyteArrayOf() when (Header.fromValue((buf.first() and Mask.Header.value).toInt() shr 5)) { Header.GENERAL -&gt; { bytesRemaining = buf[0].and(Mask.GenLength.value).toInt() buf = buf.drop(1).toUByteArray() } Header.EXT_13 -&gt; { bytesRemaining = ((buf[0].and(Mask.Ext13Byte0.value) .toLong() shl 8) or buf[1].toLong()).toInt() buf = buf.drop(2).toUByteArray() } Header.EXT_16 -&gt; { bytesRemaining = ((buf[1].toLong() shl 8) or buf[2].toLong()).toInt() buf = buf.drop(3).toUByteArray() } Header.RESERVED -&gt; { throw Exception(\"Unexpected RESERVED header\") } } Append current packet to response and decrement bytes remaining. python kotlin Append payload to buffer and update remaining / complete self.bytes.extend(buf) self.bytes_remaining -= len(buf) // Accumulate the payload now that headers are handled and dropped packet += buf bytesRemaining -= buf.size In the notification handler, we are then enqueueing the received response if there are no bytes remaining. python kotlin if response.is_received: ... await received_responses.put(response) and finally parsing the payload back in the main task after it receives the accumulated response from the queue which, at the current TLV Response level, is just extracting the ID, status, and payload: class TlvResponse(Response): def parse(self) -&gt; None: self.id = self.raw_bytes[0] self.status = self.raw_bytes[1] self.payload = self.raw_bytes[2:] ... response = await received_responses.get() response.parse() if (response.isReceived) { if (uuid == GoProUUID.CQ_COMMAND_RSP) { CoroutineScope(Dispatchers.IO).launch { receivedResponses.send(response) } } ... No Yes Decrement bytes remaining Yes No Read Available Packet Continuation bit set? Create new empty response Get bytes remaining, i.e. length Append packet to accumulating response Bytes remaining == 0? Parse Received Packet We can see this in action when we send the Get Hardware Info Command: python kotlin request_uuid = GoProUuid.COMMAND_REQ_UUID request = bytearray([0x01, 0x3C]) await client.write_gatt_char(request_uuid.value, request, response=True) response = await received_responses.get() val hardwareInfoRequest = ubyteArrayOf(0x01U, 0x3CU) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, hardwareInfoRequest) Then, in the notification handler, we continuously receive and accumulate packets (per UUID) until we have received an entire response, at which point we perform common TLV parsing (via the TlvResponse’s parse method) to extract Command ID, Status, and payload. Then we enqueue the received response to notify the writer that the response is ready. Finally we reset the per-UUID response to prepare it to receive a new response. This notification handler is only designed to handle TlvResponses. This is fine for this tutorial since that is all we will be receiving. python kotlin request_uuid = GoProUuid.COMMAND_REQ_UUID response_uuid = GoProUuid.COMMAND_RSP_UUID responses_by_uuid = GoProUuid.dict_by_uuid(TlvResponse) received_responses: asyncio.Queue[TlvResponse] = asyncio.Queue() async def tlv_notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -&gt; None: uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid) response = responses_by_uuid[uuid] response.accumulate(data) if response.is_received: If this is the correct handle, enqueue it for processing if uuid is response_uuid: logger.info(\"Received the get hardware info response\") await received_responses.put(response) Anything else is unexpected. This shouldn't happen else: logger.error(\"Unexpected response\") Reset the per-UUID response responses_by_uuid[uuid] = TlvResponse(uuid) private fun notificationHandler(characteristic: UUID, data: UByteArray) { ... responsesByUuid[uuid]?.let { response -&gt; response.accumulate(data) if (response.isReceived) { if (uuid == GoProUUID.CQ_COMMAND_RSP) { CoroutineScope(Dispatchers.IO).launch { receivedResponses.send(response) } } ... responsesByUuid[uuid] = Response.muxByUuid(uuid) } } } We can see the individual packets being accumulated in the log: python kotlin Getting the camera's hardware info... Writing to GoProUuid.COMMAND_REQ_UUID: 01:3c Received response at handle 47: 20:62:3c:00:04:00:00:00:3e:0c:48:45:52:4f:31:32:20:42:6c:61 self.bytes_remaining=80 Received response at handle 47: 80:63:6b:04:30:78:30:35:0f:48:32:33:2e:30:31:2e:30:31:2e:39 self.bytes_remaining=61 Received response at handle 47: 81:39:2e:35:36:0e:43:33:35:30:31:33:32:34:35:30:30:37:30:32 self.bytes_remaining=42 Received response at handle 47: 82:11:48:45:52:4f:31:32:20:42:6c:61:63:6b:64:65:62:75:67:0c self.bytes_remaining=23 Received response at handle 47: 83:32:36:37:34:66:37:66:36:36:31:30:34:01:00:01:01:01:00:02 self.bytes_remaining=4 Received response at handle 47: 84:5b:5d:01:01 self.bytes_remaining=0 Received the get hardware info response Getting the Hardware Info Writing characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b ==&gt; 01:3C Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 20:5B:3C:00:04:00:00:00:3E:0C:48:45:52:4F:31:32:20:42:6C:61 Received response on CQ_COMMAND_RSP Received packet of length 18. 73 bytes remaining Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 80:63:6B:04:30:78:30:35:0F:48:32:33:2E:30:31:2E:30:31:2E:39 Received response on CQ_COMMAND_RSP Received packet of length 19. 54 bytes remaining Wrote characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 81:39:2E:35:36:0E:43:33:35:30:31:33:32:34:35:30:30:37:30:32 Received response on CQ_COMMAND_RSP Received packet of length 19. 35 bytes remaining Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 82:0A:47:50:32:34:35:30:30:37:30:32:0C:32:36:37:34:66:37:66 Received response on CQ_COMMAND_RSP Received packet of length 19. 16 bytes remaining Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 83:36:36:31:30:34:01:00:01:01:01:00:02:5B:5D:01:01 Received response on CQ_COMMAND_RSP Received packet of length 16. 0 bytes remaining At this point the response has been accumulated. We then parse and log the payload using the Get Hardware Info response documentation: python kotlin hardware_info = HardwareInfo.from_bytes(response.payload) logger.info(f\"Received hardware info: {hardware_info}\") where the parsing is done as such: @classmethod def from_bytes(cls, data: bytes) -&gt; HardwareInfo: buf = bytearray(data) Get model number model_num_length = buf.pop(0) model = int.from_bytes(buf[:model_num_length]) buf = buf[model_num_length:] Get model name model_name_length = buf.pop(0) model_name = (buf[:model_name_length]).decode() buf = buf[model_name_length:] Advance past deprecated bytes deprecated_length = buf.pop(0) buf = buf[deprecated_length:] Get firmware version firmware_length = buf.pop(0) firmware = (buf[:firmware_length]).decode() buf = buf[firmware_length:] Get serial number serial_length = buf.pop(0) serial = (buf[:serial_length]).decode() buf = buf[serial_length:] Get AP SSID ssid_length = buf.pop(0) ssid = (buf[:ssid_length]).decode() buf = buf[ssid_length:] Get MAC address mac_length = buf.pop(0) mac = (buf[:mac_length]).decode() buf = buf[mac_length:] return cls(model, model_name, firmware, serial, ssid, mac) This logs as: Parsed hardware info: { \"model_name\": \"HERO12 Black\", \"firmware_version\": \"H23.01.01.99.56\", \"serial_number\": \"C3501324500702\", \"ap_ssid\": \"HERO12 Blackdebug\", \"ap_mac_address\": \"2674f7f66104\" } tlvResponse.parse() val hardwareInfo = HardwareInfo.fromBytes(tlvResponse.payload) where the parsing is done as such: fun fromBytes(data: UByteArray): HardwareInfo { // Parse header bytes var buf = data.toUByteArray() // Get model number val modelNumLength = buf.first().toInt() buf = buf.drop(1).toUByteArray() val model = buf.take(modelNumLength).toInt() buf = buf.drop(modelNumLength).toUByteArray() // Get model name val modelNameLength = buf.first().toInt() buf = buf.drop(1).toUByteArray() val modelName = buf.take(modelNameLength).decodeToString() buf = buf.drop(modelNameLength).toUByteArray() // Advance past deprecated bytes val deprecatedLength = buf.first().toInt() buf = buf.drop(1).toUByteArray() buf = buf.drop(deprecatedLength).toUByteArray() // Get firmware version val firmwareLength = buf.first().toInt() buf = buf.drop(1).toUByteArray() val firmware = buf.take(firmwareLength).decodeToString() buf = buf.drop(firmwareLength).toUByteArray() // Get serial number val serialLength = buf.first().toInt() buf = buf.drop(1).toUByteArray() val serial = buf.take(serialLength).decodeToString() buf = buf.drop(serialLength).toUByteArray() // Get AP SSID val ssidLength = buf.first().toInt() buf = buf.drop(1).toUByteArray() val ssid = buf.take(ssidLength).decodeToString() buf = buf.drop(ssidLength).toUByteArray() // Get MAC Address val macLength = buf.first().toInt() buf = buf.drop(1).toUByteArray() val mac = buf.take(macLength).decodeToString() return HardwareInfo(model, modelName, firmware, serial, ssid, mac) } This logs as: Got the Hardware Info successfully: HardwareInfo( modelNumber=1040187392, modelName=HERO12 Black, firmwareVersion=H23.01.01.99.56, serialNumber=C3501324500702, apSsid=GP24500702, apMacAddress=2674f7f66104 ) Quiz time! 📚 ✏️ How can we know that a response has been completely received? A: The stop bit will be set in the header B: The response has accumulated length bytes C: By checking for the end of frame (EOF) sentinel character Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is B. The length of the entire response is parsed from the first packet. We then accumulate packets, keeping track of the received length, until all of the bytes have been received. A and C are just made up 😜. Troubleshooting See the first tutorial’s troubleshooting section. Good Job! Congratulations 🤙 You now know how to accumulate TLV responses that are received from the GoPro, at least if they are received uninterrupted. There is additional logic required for a complete solution such as checking the UUID the response is received on and storing a dict of response per UUID. At the current time, this endeavor is left for the reader. For a complete example of this, see the Open GoPro Python SDK. To learn about a different type of operation (Queries), go to the next tutorial.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/parse-ble-responses#"
        },
        {
            "title": "Tutorial 4: BLE TLV Queries: ",
            "excerpt": "This document will provide a walk-through tutorial to use the Open GoPro Interface to query the camera’s setting and status information via BLE. Queries in this sense are operations that are initiated by writing to the Query UUID and receiving responses via the Query Response UUID. A list of queries can be found in the Query ID Table. It is important to distinguish between queries and commands because they each have different request and response packet formats. This tutorial only considers sending these queries as one-off queries. That is, it does not consider state management / synchronization when sending multiple queries. This will be discussed in a future lab. Requirements It is assumed that the hardware and software requirements from the connecting BLE tutorial are present and configured correctly. It is suggested that you have first completed the connect, sending commands, and parsing responses tutorials before going through this tutorial. Just Show me the Demo(s)!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 4 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements Individual Query Poll You can test an individual query poll with your camera through BLE using the following script: $ python ble_query_poll_resolution_value.py See the help for parameter definitions: $ python ble_query_poll_resolution_value.py --help usage: ble_query_poll_resolution_value.py [-h] [-i IDENTIFIER] Connect to a GoPro camera, get the current resolution, modify the resolution, and confirm the change was successful. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to Multiple Simultaneous Query Polls You can test querying multiple queries simultaneously with your camera through BLE using the following script: $ python ble_query_poll_multiple_setting_values.py See the help for parameter definitions: $ python ble_query_poll_multiple_setting_values.py --help usage: ble_query_poll_multiple_setting_values.py [-h] [-i IDENTIFIER] Connect to a GoPro camera then get the current resolution, fps, and fov. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to Registering for Query Push Notifications You can test registering for querties and receiving push notifications with your camera through BLE using the following script: $ python ble_query_register_resolution_value_updates.py See the help for parameter definitions: $ python ble_query_register_resolution_value_updates.py --help usage: ble_query_register_resolution_value_updates.py [-h] [-i IDENTIFIER] Connect to a GoPro camera, register for updates to the resolution, receive the current resolution, modify the resolution, and confirm receipt of the change notification. optional arguments: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to The Kotlin file for this tutorial can be found on Github. To perform the tutorial, run the Android Studio project, select “Tutorial 4” from the dropdown and click on “Perform.” This requires that a GoPro is already connected via BLE, i.e. that Tutorial 1 was already run. You can check the BLE status at the top of the app. Perform Tutorial 4 This will start the tutorial and log to the screen as it executes. When the tutorial is complete, click “Exit Tutorial” to return to the Tutorial selection screen. Setup We must first connect as was discussed in the connecting BLE tutorial. python kotlin We have slightly updated the notification handler from the previous tutorial to handle a QueryResponse instead of a TlvResponse where QueryResponse is a subclass of TlvResponse that will be created in this tutorial. responses_by_uuid = GoProUuid.dict_by_uuid(QueryResponse) received_responses: asyncio.Queue[QueryResponse] = asyncio.Queue() query_request_uuid = GoProUuid.QUERY_REQ_UUID query_response_uuid = GoProUuid.QUERY_RSP_UUID setting_request_uuid = GoProUuid.SETTINGS_REQ_UUID setting_response_uuid = GoProUuid.SETTINGS_RSP_UUID async def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray) -&gt; None: uuid = GoProUuid(client.services.characteristics[characteristic.handle].uuid) response = responses_by_uuid[uuid] response.accumulate(data) Notify the writer if we have received the entire response if response.is_received: If this is query response, it must contain a resolution value if uuid is query_response_uuid: logger.info(\"Received a Query response\") await received_responses.put(response) If this is a setting response, it will just show the status elif uuid is setting_response_uuid: logger.info(\"Received Set Setting command response.\") await received_responses.put(response) Anything else is unexpected. This shouldn't happen else: logger.error(\"Unexpected response\") Reset per-uuid Response responses_by_uuid[uuid] = QueryResponse(uuid) The code above is taken from ble_query_poll_resolution_value.py We are defining a resolution enum that will be updated as we receive new resolutions: private enum class Resolution(val value: UByte) { RES_4K(1U), RES_2_7K(4U), RES_2_7K_4_3(6U), RES_1080(9U), RES_4K_4_3(18U), RES_5K(24U); companion object { private val valueMap: Map&lt;UByte, Resolution&gt; by lazy { values().associateBy { it.value } } fun fromValue(value: UByte) = valueMap.getValue(value) } } private lateinit var resolution: Resolution There are two methods to query status / setting information, each of which will be described in a following section: Polling Query Information Registering for query push notifications Parsing a Query Response Before sending queries, we must first describe how Query response parsing differs from the Command response parsing that was introduced in the previous tutorial. To recap, the generic response format for both Commands and Queries is: Header (length) Operation ID (Command / Query ID) Status Response 1-2 bytes 1 byte 1 bytes Length - 2 bytes Query Responses contain an array of additional TLV groups in the Response field as such: ID1 Length1 Value1 ID2 Length2 Value 2 … IDN LengthN ValueN 1 byte 1 byte Length1 bytes 1 byte 1 byte Length2 bytes … 1 byte 1 byte LengthN bytes We will be extending the TlvResponse class that was defined in the parsing responses tutorial to perform common parsing shared among all queries into a QueryResponse class as seen below: We have already parsed the length, Operation ID, and status, and extracted the payload in the TlvResponse class. The next step is to parse the payload. Therefore, we now continuously parse Type (ID) - Length - Value groups until we have consumed the response. We are storing each value in a hash map indexed by ID for later access. python kotlin class QueryResponse(TlvResponse): ... def parse(self) -&gt; None: super().parse() buf = bytearray(self.payload) while len(buf) &gt; 0: Get ID and Length of query parameter param_id = buf[0] param_len = buf[1] buf = buf[2:] Get the value value = buf[:param_len] Store in dict for later access self.data[param_id] = bytes(value) Advance the buffer buf = buf[param_len:] while (buf.isNotEmpty()) { // Get each parameter's ID and length val paramId = buf[0] val paramLen = buf[1].toInt() buf = buf.drop(2) // Get the parameter's value val paramVal = buf.take(paramLen) // Store in data dict for access later data[paramId] = paramVal.toUByteArray() // Advance the buffer for continued parsing buf = buf.drop(paramLen) } yes no Parse Query ID Parse Status More data? Get Value ID Get Value Length Get Value done How many packets are query responses? A: Always 1 packet B: Always multiple packets C: Can be 1 or multiple packets Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is C. Query responses can be one packet (if for example querying a specific setting) or multiple packets (when querying many or all settings as in the example here). Which field is not common to all TLV responses? A: length B: status C: ID D: None of the Above Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is D. All Commands and Query responses have a length, ID, and status. Polling Query Information It is possible to poll one or more setting / status values using the following queries: Query ID Request Query 0x12 [Get Setting value(s)](/OpenGoPro/ble/features/query.htmlget-setting-values) len:12:xx:xx 0x13 [Get Status value(s)](/OpenGoPro/ble/features/query.htmlget-status-values) len:13:xx:xx where xx are setting / status ID(s) and len is the length of the rest of the query (the number of query bytes plus one for the request ID byte). There will be specific examples below. Since they are two separate queries, combination of settings / statuses can not be polled simultaneously. Here is a generic sequence diagram (the same is true for statuses): GoProOpen GoPro user deviceGoProOpen GoPro user deviceConnected (steps from connect tutorial)Get Setting value(s) queries written to Query UUIDSetting values responded to Query Response UUIDMore setting values responded to Query Response UUID...More setting values responded to Query Response UUID The number of notification responses will vary depending on the amount of settings that have been queried. Note that setting values will be combined into one notification until it reaches the maximum notification size (20 bytes). At this point, a new response will be sent. Therefore, it is necessary to accumulate and then parse these responses as was described in parsing query responses Individual Query Poll Here we will walk through an example of polling one setting (Resolution). First we send the query: python kotlin The sample code can be found in in ble_query_poll_resolution_value.py. query_request_uuid = GoProUuid.QUERY_REQ_UUID request = bytes([0x02, 0x12, RESOLUTION_ID]) await client.write_gatt_char(query_request_uuid.value, request, response=True) val pollResolution = ubyteArrayOf(0x02U, 0x12U, RESOLUTION_ID) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_QUERY.uuid, pollResolution) Then when the response is received from the notification handler we parse it into individual query elements in the QueryResponse class and extract the new resolution value. python kotlin Wait to receive the notification response response = await received_responses.get() response.parse() resolution = Resolution(response.data[RESOLUTION_ID][0]) which logs as such: Getting the current resolution Writing to GoProUuid.QUERY_REQ_UUID: 02:12:02 Received response at handle=62: b'05:12:00:02:01:09' eceived the Resolution Query response Resolution is currently Resolution.RES_1080 // Wait to receive the response and then convert it to resolution val queryResponse = (receivedResponses.receive() as Response.Query).apply { parse() } resolution = Resolution.fromValue(queryResponse.data.getValue(RESOLUTION_ID).first()) which logs as such: Polling the current resolution Writing characteristic b5f90076-aa8d-11e3-9046-0002a5d5c51b ==&gt; 02:12:02 Wrote characteristic b5f90076-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90077-aa8d-11e3-9046-0002a5d5c51b changed | value: 05:12:00:02:01:09 Received response on CQ_QUERY_RSP Received packet of length 5. 0 bytes remaining Received Query Response Camera resolution is RES_1080 For verification purposes, we are then changing the resolution and polling again to verify that the setting has changed: python kotlin while resolution is not target_resolution: request = bytes([0x02, 0x12, RESOLUTION_ID]) await client.write_gatt_char(query_request_uuid.value, request, response=True) response = await received_responses.get() Wait to receive the notification response response.parse() resolution = Resolution(response.data[RESOLUTION_ID][0]) which logs as such: Changing the resolution to Resolution.RES_2_7K... Writing to GoProUuid.SETTINGS_REQ_UUID: 03:02:01:04 Writing to GoProUuid.SETTINGS_REQ_UUID: 03:02:01:04 Received response at GoProUuid.SETTINGS_RSP_UUID: 02:02:00 Received Set Setting command response. Polling the resolution to see if it has changed... Writing to GoProUuid.QUERY_REQ_UUID: 02:12:02 Received response at GoProUuid.QUERY_RSP_UUID: 05:12:00:02:01:04 Received the Resolution Query response Resolution is currently Resolution.RES_2_7K Resolution has changed as expected. Exiting... while (resolution != newResolution) { ble.writeCharacteristic(goproAddress, GoProUUID.CQ_QUERY.uuid, pollResolution) val queryNotification = (receivedResponses.receive() as Response.Query).apply { parse() } resolution = Resolution.fromValue(queryNotification.data.getValue(RESOLUTION_ID).first()) } which logs as such: Changing the resolution to RES_2_7K Writing characteristic b5f90074-aa8d-11e3-9046-0002a5d5c51b ==&gt; 03:02:01:04 Wrote characteristic b5f90074-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90075-aa8d-11e3-9046-0002a5d5c51b changed | value: 02:02:00 Received response on CQ_SETTING_RSP Received packet of length 2. 0 bytes remaining Received set setting response. Resolution successfully changed Polling the resolution until it changes Writing characteristic b5f90076-aa8d-11e3-9046-0002a5d5c51b ==&gt; 02:12:02 Characteristic b5f90077-aa8d-11e3-9046-0002a5d5c51b changed | value: 05:12:00:02:01:04 Received response on CQ_QUERY_RSP Received packet of length 5. 0 bytes remaining Received Query Response Wrote characteristic b5f90076-aa8d-11e3-9046-0002a5d5c51b Camera resolution is currently RES_2_7K Multiple Simultaneous Query Polls Rather than just polling one setting, it is also possible to poll multiple settings. An example of this is shown below. It is very similar to the previous example except that the query now includes 3 settings: Resolution, FPS, and FOV. python kotlin RESOLUTION_ID = 2 FPS_ID = 3 FOV_ID = 121 request = bytes([0x04, 0x12, RESOLUTION_ID, FPS_ID, FOV_ID]) await client.write_gatt_char(query_request_uuid.value, request, response=True) response = await received_responses.get() Wait to receive the notification response TODO The length (first byte of the query) has been increased to 4 to accommodate the extra settings We are also parsing the response to get all 3 values: python kotlin response.parse() logger.info(f\"Resolution is currently {Resolution(response.data[RESOLUTION_ID][0])}\") logger.info(f\"Video FOV is currently {VideoFOV(response.data[FOV_ID][0])}\") logger.info(f\"FPS is currently {FPS(response.data[FPS_ID][0])}\") TODO When we are storing the updated setting, we are just taking the first byte (i..e index 0). A real-world implementation would need to know the length (and type) of the setting / status response by the ID. For example, sometimes settings / statuses are bytes, words, strings, etc. They are then printed to the log which will look like the following: python kotlin Getting the current resolution, fps, and fov. Writing to GoProUuid.QUERY_REQ_UUID: 04:12:02:03:79 Received response at GoProUuid.QUERY_RSP_UUID: 0b:12:00:02:01:09:03:01:00:79:01:00 Received the Query Response Resolution is currently Resolution.RES_1080 Video FOV is currently VideoFOV.FOV_WIDE FPS is currently FPS.FPS_240 TODO In general, we can parse query values by looking at relevant documentation linked from the Setting or Status ID tables. For example (for settings): ID 2 == 9 equates to Resolution == 1080 ID 3 == 1 equates to FPS == 120 Query All It is also possible to query all settings / statuses by not passing any ID’s into the the query, i.e.: Query ID Request Query 0x12 Get All Settings 01:12 0x13 Get All Statuses 01:13 Quiz time! 📚 ✏️ How can we poll the encoding status and the resolution setting using one query? A: Concatenate a &8216;Get Setting Value&8217; query and a &8216;Get Status&8217; query with the relevant ID&8217;s B: Concatenate the &8216;Get All Setting&8217; and &8216;Get All Status&8217; queries. C: It is not possible Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is C. It is not possible to concatenate queries. This would result in an unknown sequence of bytes from the camera&8217;s perspective. So it is not possible to get a setting value and a status value in one query. The Get Setting Query (with resolution ID) and Get Status Query (with encoding ID) must be sent sequentially in order to get this information. Registering for Query Push Notifications Rather than polling the query information, it is also possible to use an interrupt scheme to register for push notifications when the relevant query information changes. The relevant queries are: Query ID Request Query 0x52 [Register updates for setting(s)](/OpenGoPro/ble/features/query.htmlregister-for-setting-value-updates) len:52:xx:xx 0x53 [Register updates for status(es)](/OpenGoPro/ble/features/query.htmlregister-for-status-value-updates) len:53:xx:xx 0x72 [Unregister updates for setting(s)](/OpenGoPro/ble/features/query.htmlunregister-for-setting-value-updates) len:72:xx:xx 0x73 [Unregister updates for status(es)](/OpenGoPro/ble/features/query.htmlunregister-for-status-value-updates) len:73:xx:xx where xx are setting / status ID(s) and len is the length of the rest of the query (the number of query bytes plus one for the request ID byte). The Query ID’s for push notification responses are as follows: Query ID Response 0x92 Setting Value Push Notification 0x93 Status Value Push Notification Here is a generic sequence diagram of how this looks (the same is true for statuses): GoProOpen GoPro user deviceGoProOpen GoPro user deviceConnected (steps from connect tutorial)loop[Setting changes]loop[Settingchanges]Register updates for settingNotification Response and Current Setting ValueSetting changesPush notification of new setting valueUnregister updates for settingNotification ResponseSetting changes That is, after registering for push notifications for a given query, notification responses will continuously be sent whenever the query changes until the client unregisters for push notifications for the given query. The initial response to the Register query also contains the current setting / status value. We will walk through an example of this below: First, let’s register for updates when the resolution setting changes: python kotlin query_request_uuid = GoProUuid.QUERY_REQ_UUID request = bytes([0x02, 0x52, RESOLUTION_ID]) await client.write_gatt_char(query_request_uuid.value, request, response=True) Wait to receive the notification response response = await received_responses.get() val registerResolutionUpdates = ubyteArrayOf(0x02U, 0x52U, RESOLUTION_ID) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_QUERY.uuid, registerResolutionUpdates) and parse its response (which includes the current resolution value). This is very similar to the polling example with the exception that the Query ID is now 0x52 (Register Updates for Settings). This can be seen in the raw byte data as well as by inspecting the response’s id property. python kotlin response.parse() resolution = Resolution(response.data[RESOLUTION_ID][0]) logger.info(f\"Resolution is currently {resolution}\") This will show in the log as such: Registering for resolution updates Writing to GoProUuid.QUERY_REQ_UUID: 02:52:02 Received response at GoProUuid.QUERY_RSP_UUID: 05:52:00:02:01:09 Received the Resolution Query response Successfully registered for resolution value updates Resolution is currently Resolution.RES_1080 val queryResponse = (receivedResponses.receive() as Response.Query).apply { parse() } resolution = Resolution.fromValue(queryResponse.data.getValue(RESOLUTION_ID).first()) This will show in the log as such: Registering for resolution value updates Writing characteristic b5f90076-aa8d-11e3-9046-0002a5d5c51b ==&gt; 02:52:02 Wrote characteristic b5f90076-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90077-aa8d-11e3-9046-0002a5d5c51b changed | value: 05:52:00:02:01:04 Received response on CQ_QUERY_RSP Received packet of length 5. 0 bytes remaining Received Query Response Camera resolution is RES_2_7K We are now successfully registered for resolution value updates and will receive push notifications whenever the resolution changes. We verify this in the demo by then changing the resolution and waiting to receive the update. notification.. python kotlin target_resolution = Resolution.RES_2_7K if resolution is Resolution.RES_1080 else Resolution.RES_1080 request = bytes([0x03, 0x02, 0x01, target_resolution.value]) await client.write_gatt_char(setting_request_uuid.value, request, response=True) response = await received_responses.get() response.parse() while resolution is not target_resolution: request = bytes([0x02, 0x12, RESOLUTION_ID]) await client.write_gatt_char(query_request_uuid.value, request, response=True) response = await received_responses.get() Wait to receive the notification response response.parse() resolution = Resolution(response.data[RESOLUTION_ID][0]) This will show in the log as such: Changing the resolution to Resolution.RES_2_7K... Writing to GoProUuid.SETTINGS_REQ_UUID: 03:02:01:04 Received response at GoProUuid.SETTINGS_RSP_UUID: 02:02:00 Received Set Setting command response. Waiting to receive new resolution Received response at GoProUuid.QUERY_RSP_UUID: 05:92:00:02:01:04 Received the Resolution Query response Resolution is currently Resolution.RES_2_7K Resolution has changed as expected. Exiting... val targetResolution = if (resolution == Resolution.RES_2_7K) Resolution.RES_1080 else Resolution.RES_2_7K val setResolution = ubyteArrayOf(0x03U, RESOLUTION_ID, 0x01U, targetResolution.value) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_SETTING.uuid, setResolution) val setResolutionResponse = (receivedResponses.receive() as Response.Tlv).apply { parse() } // Verify we receive the update from the camera when the resolution changes while (resolution != targetResolution) { val queryNotification = (receivedResponses.receive() as Response.Query).apply { parse() } resolution = Resolution.fromValue(queryNotification.data.getValue(RESOLUTION_ID).first()) } We can see change happen in the log: Changing the resolution to RES_2_7K Writing characteristic b5f90074-aa8d-11e3-9046-0002a5d5c51b ==&gt; 03:02:01:04 Wrote characteristic b5f90074-aa8d-11e3-9046-0002a5d5c51b Resolution successfully changed Waiting for camera to inform us about the resolution change Characteristic b5f90077-aa8d-11e3-9046-0002a5d5c51b changed | value: 05:92:00:02:01:04 Received response on b5f90077-aa8d-11e3-9046-0002a5d5c51b: 05:92:00:02:01:04 Received resolution query response Resolution is now RES_2_7K In this case, the Query ID is 0x92 (Setting Value Push Notification) as expected. Multiple push notifications can be registered / received in a similar manner that multiple queries were polled above Quiz time! 📚 ✏️ True or False: We can still poll a given query value while we are currently registered to receive push notifications for it. A: True B: False Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is A. While there is probably not a good reason to do so, there is nothing preventing polling in this manner. True or False: A push notification for a registered setting will only ever contain query information about one setting ID. A: True B: False Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is B. It is possible for push notifications to contain multiple setting ID&8217;s if both setting ID&8217;s have push notifications registered and both settings change at the same time. Troubleshooting See the first tutorial’s troubleshooting section. Good Job! Congratulations 🤙 You can now query any of the settings / statuses from the camera using one of the above patterns.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/ble-queries#"
        },
        {
            "title": "Tutorial 5: BLE Protobuf Operations: ",
            "excerpt": "This document will provide a walk-through tutorial to use the Open GoPro Interface to send and receive BLE Protobuf Data. Open GoPro uses Protocol Buffers Version 2 A list of Protobuf Operations can be found in the Protobuf ID Table. This tutorial only considers sending these as one-off operations. That is, it does not consider state management / synchronization when sending multiple operations. This will be discussed in a future lab. Requirements It is assumed that the hardware and software requirements from the connecting BLE tutorial are present and configured correctly. It is suggested that you have first completed the connect, sending commands, and parsing responses tutorials before going through this tutorial. Just Show me the Demo(s)!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 5 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements Protobuf Example You can see some basic Protobuf usage, independent of a BLE connection, in the following script: $ python protobuf_example.py Set Turbo Mode You can test sending Set Turbo Mode to your camera through BLE using the following script: $ python set_turbo_mode.py See the help for parameter definitions: $ python set_turbo_mode.py --help usage: set_turbo_mode.py [-h] [-i IDENTIFIER] Connect to a GoPro camera, send Set Turbo Mode and parse the response options: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to Decipher Response Type TODO TODO Compiling Protobuf Files The Protobuf files used to compile source code for the Open GoPro Interface exist in the top-level protobuf directory of the Open GoPro repository. It is mostly out of the scope of these tutorials to describe how to compile these since this process is clearly defined in the per-language Protobuf Tutorial. For the purposes of these tutorials (and shared with the Python SDK), the Protobuf files are compiled using the Docker image defined in tools/proto_build. This build process can be performed using make protos from the top level of this repo. This information is strictly explanatory. It is in no way necessary to (re)build the Protobuf files for these tutorials as the pre-compiled Protobuf source code already resides in the same directory as this tutorial’s example code. Working with Protobuf Messages Let’s first perform some basic serialization and deserialization of a Protobuf message. For this example, we are going to use the Set Turbo Transfer operation: Set Turbo Mode Documentation Per the documentation, this operation’s request payload should be serialized using the Protobuf message which can be found either in Documentation: RequestSetTurboActive documentation or source code: /** * Enable/disable display of \"Transferring Media\" UI * * Response: @ref ResponseGeneric */ message RequestSetTurboActive { required bool active = 1; // Enable or disable Turbo Transfer feature } This code can be found in protobuf_example.py Protobuf Message Example First let’s instantiate the request message by setting the active parameter and log the serialized bytes: Your IDE should show the Protobuf Message’s API signature since type stubs were generated when compiling the Protobuf files. python kotlin from tutorial_modules import proto request = proto.RequestSetTurboActive(active=False) logger.info(f\"Sending ==&gt; {request}\") logger.info(request.SerializeToString().hex(\":\")) which will log as such: Sending ==&gt; active: false 08:00 TODO We’re not going to analyze these bytes since it is the purpose of the Protobuf framework is to abstract this. However it is important to be able to generate the serialized bytes from the instantiated Protobuf Message object in order to send the bytes via BLE. Similarly, let’s now create a serialized response and show how to deserialize it into a ResponseGeneric object. python kotlin response_bytes = proto.ResponseGeneric(result=proto.EnumResultGeneric.RESULT_SUCCESS).SerializeToString() logger.info(f\"Received bytes ==&gt; {response_bytes.hex(':')}\") response = proto.ResponseGeneric.FromString(response_bytes) logger.info(f\"Received ==&gt; {response}\") which will log as such: Received bytes ==&gt; 08:01 Received ==&gt; result: RESULT_SUCCESS TODO We’re not hard-coding serialized bytes here since it may not be constant across Protobuf versions Performing a Protobuf Operation Now let’s actually perform a Protobuf Operation via BLE. First we need to discuss additional non-Protobuf-defined header bytes that are required for Protobuf Operations in the Open GoPro Interface. Protobuf Packet Format Besides having a compressed payload as defined per the Protobuf Specification, Open GoPro Protobuf operations also are identified by “Feature” and “Action” IDs. The top level message format (not including the standard headers) is as follows: Feature ID Action ID Serialized Protobuf Payload 1 Byte 1 Byte Variable Length This Feature / Action ID pair is used to identify the Protobuf Message that should be used to serialize / deserialize the payload. This mapping can be found in the Protobuf ID Table. Protobuf Response Parser Since the parsing of Protobuf messages is different than TLV Parsing, we need to create a ProtobufResponse class by extending the Response class from the TLV Parsing Tutorial. This ProtobufResponse parse method will: Extract Feature and Action ID’s Parse the Protobuf payload using the specified Protobuf Message python kotlin This code can be found in set_turbo_mode.py class ProtobufResponse(Response): ... def parse(self, proto: type[ProtobufMessage]) -&gt; None: self.feature_id = self.raw_bytes[0] self.action_id = self.raw_bytes[1] self.data = proto.FromString(bytes(self.raw_bytes[2:])) TODO The accumulation process is the same for TLV and Protobuf responses so have not overridden the base Response class’s accumulation method and we are using the same notification handler as previous labs. Set Turbo Transfer Now let’s perform the Set Turbo Transfer operation and receive the response. First, we build the serialized byte request in the same manner as above), then prepend the Feature ID, Action ID, and length bytes: python kotlin turbo_mode_request = bytearray( [ 0xF1, Feature ID 0x6B, Action ID *proto.RequestSetTurboActive(active=False).SerializeToString(), ] ) turbo_mode_request.insert(0, len(turbo_mode_request)) TODO We then send the message, wait to receive the response, and parse the response using the Protobuf Message specified from the Set Turbo Mode Documentation: ResponseGeneric. python kotlin await client.write_gatt_char(request_uuid.value, turbo_mode_request, response=True) response = await received_responses.get() response.parse(proto.ResponseGeneric) assert response.feature_id == 0xF1 assert response.action_id == 0xEB logger.info(response.data) which will log as such: Setting Turbo Mode Off Writing 04:f1:6b:08:00 to GoProUuid.COMMAND_REQ_UUID Received response at UUID GoProUuid.COMMAND_RSP_UUID: 04:f1:eb:08:01 Set Turbo Mode response complete received. Successfully set turbo mode result: RESULT_SUCCESS TODO Deciphering Response Type This same procedure is used for all Protobuf Operations. Coupled with the information from previous tutorials, you are now capable of parsing any response received from the GoPro. However we have not yet covered how to decipher the response type: Command, Query, Protobuf, etc. The algorithm to do so is defined in the GoPro BLE Spec and reproduced here for reference: Message Deciphering Algorithm Response Manager We’re now going to create a monolithic ResponseManager class to implement this algorithm to perform (at least initial) parsing of all response types: python kotlin The sample code below is taken from decipher_response.py The ResponseManager is a wrapper around a BleakClient to manage accumulating, parsing, and retrieving responses. First, let’s create a non-initialized response manager, connect to get a BleakClient and initialize the manager by setting the client: manager = ResponseManager() manager.set_client(await connect_ble(manager.notification_handler, identifier)) Then, in the notification handler, we “decipher” the response before enqueueing it to the received response queue: async def notification_handler(self, characteristic: BleakGATTCharacteristic, data: bytearray) -&gt; None: uuid = GoProUuid(self.client.services.characteristics[characteristic.handle].uuid) logger.debug(f'Received response at {uuid}: {data.hex(\":\")}') response = self._responses_by_uuid[uuid] response.accumulate(data) Enqueue if we have received the entire response if response.is_received: await self._q.put(self.decipher_response(response)) Reset the accumulating response self._responses_by_uuid[uuid] = Response(uuid) where “deciphering” is the implementation of the above algorithm: def decipher_response(self, undeciphered_response: Response) -&gt; ConcreteResponse: payload = undeciphered_response.raw_bytes Are the first two payload bytes a real Fetaure / Action ID pair? if (index := ProtobufId(payload[0], payload[1])) in ProtobufIdToMessage: if not (proto_message := ProtobufIdToMessage.get(index)): We've only added protobuf messages for operations used in this tutorial. raise RuntimeError( f\"{index} is a valid Protobuf identifier but does not currently have a defined message.\" ) else: Now use the protobuf messaged identified by the Feature / Action ID pair to parse the remaining payload response = ProtobufResponse.from_received_response(undeciphered_response) response.parse(proto_message) return response TLV. Should it be parsed as Command or Query? if undeciphered_response.uuid is GoProUuid.QUERY_RSP_UUID: It's a TLV query response = QueryResponse.from_received_response(undeciphered_response) else: It's a TLV command / setting. response = TlvResponse.from_received_response(undeciphered_response) Parse the TLV payload (query, command, or setting) response.parse() return response Only the minimal functionality needed for these tutorials have been added. For example, many Protobuf Feature / Action ID pairs do not have corresponding Protobuf Messages defined. TODO After deciphering, the parsed method is placed in the response queue as a either a TlvResponse, QueryResponse, or ProtobufResponse. Examples of Each Response Type Now let’s perform operations that will demonstrate each response type: python kotlin TLV Command (Setting) await set_resolution(manager) TLV Command await get_resolution(manager) TLV Query await set_shutter_off(manager) Protobuf await set_turbo_mode(manager) These four methods will perform the same functionality we’ve demonstrated in previous tutorials, now using our ResponseManager. We’ll walk through the get_resolution method here. First build the request and send it: request = bytes([0x03, 0x02, 0x01, 0x09]) request_uuid = GoProUuid.SETTINGS_REQ_UUID await manager.client.write_gatt_char(request_uuid.value, request, response=True) Then retrieve the response from the manager: tlv_response = await manager.get_next_response_as_tlv() logger.info(f\"Set resolution status: {tlv_response.status}\") This logs as such: Getting the current resolution Writing to GoProUuid.QUERY_REQ_UUID: 02:12:02 Received response at GoProUuid.QUERY_RSP_UUID: 05:12:00:02:01:09 Received current resolution: Resolution.RES_1080 Note that each example retrieves the parsed response from the manager via one of the following methods: get_next_response_as_tlv get_next_response_as_query get_next_response_as_response These are functionally the same as they just retrieve the next received response from the manager’s queue and only exist as helpers to simplify typing. TODO Troubleshooting See the first tutorial’s troubleshooting section. Good Job! Congratulations 🤙 You can now accumulate, decipher, and parse any BLE response received from the GoPro.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/ble-protobuf#"
        },
        {
            "title": "Tutorial 6: Connect WiFi: ",
            "excerpt": "This document will provide a walk-through tutorial to use the Open GoPro Interface to connect the GoPro to a Wifi network either in Access Point (AP) mode or Station (STA) Mode. It is recommended that you have first completed the connecting BLE, sending commands, parsing responses, and protobuf tutorials before proceeding. Requirements It is assumed that the hardware and software requirements from the connecting BLE tutorial are present and configured correctly. The scripts that will be used for this tutorial can be found in the Tutorial 6 Folder. Just Show me the Demo(s)!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 6 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements Enable WiFi AP You can enable the GoPro’s Access Point to allow it accept Wifi connections as an Access Point via: $ python wifi_enable.py See the help for parameter definitions: $ python wifi_enable.py --help usage: enable_wifi_ap.py [-h] [-i IDENTIFIER] [-t TIMEOUT] Connect to a GoPro camera via BLE, get its WiFi Access Point (AP) info, and enable its AP. options: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to -t TIMEOUT, --timeout TIMEOUT time in seconds to maintain connection before disconnecting. If not set, will maintain connection indefinitely Connect GoPro as STA You can connect the GoPro to a Wifi network where the GoPro is in Station Mode (STA) via: $ python connect_as_sta.py See the help for parameter definitions: $ python connect_as_sta.py --help Connect the GoPro to a Wifi network where the GoPro is in Station Mode (STA). positional arguments: ssid SSID of network to connect to password Password of network to connect to options: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to The Kotlin file for this tutorial can be found on Github. To perform the tutorial, run the Android Studio project, select “Tutorial 6” from the dropdown and click on “Perform.” This requires that a GoPro is already connected via BLE, i.e. that Tutorial 1 was already run. You can check the BLE status at the top of the app. Perform Tutorial 6 This will start the tutorial and log to the screen as it executes. When the tutorial is complete, click “Exit Tutorial” to return to the Tutorial selection screen. Setup For both cases, we must first connect to BLE as was discussed in the connecting BLE tutorial. Access Point Mode (AP) In AP mode, the GoPro operates as an Access Point, allowing wireless clients to connect and communicate using the Open GoPro HTTP API. The HTTP API provides much of the same functionality as the BLE API as well as some additional functionality. For more information on the HTTP API, see the next 2 tutorials. AccessPointGoProclientBLEWiFi In order to connect to the camera in AP mode, after connecting via BLE, pairing, and enabling notifications, we must: find the GoPro’s WiFi AP information (SSID and password) via BLE, enable the WiFi AP via BLE connect to the WiFi AP. Here is an outline of the steps to do so: GoProWiFiGoProBLEOpen GoPro user deviceGoProWiFiGoProBLEOpen GoPro user deviceScanningConnectedalt[If not Previously Paired]PairedReady to Communicateloop[Steps from Connect Tutorial]WiFi AP enabledAdvertisingAdvertisingConnectPair RequestPair ResponseEnable Notifications on Characteristic 1Enable Notifications on Characteristic 2Enable Notifications on Characteristic ..Enable Notifications on Characteristic NRead Wifi AP SSIDRead Wifi AP PasswordWrite to Enable WiFi APResponse sent as notificationConnect to WiFi AP The following subsections will detail this process. Find WiFi Information First we must find the target Wifi network’s SSID and password. The process to get this information is different than all other BLE operations described up to this point. Whereas the previous command, setting, and query operations all followed the Write Request-Notification Response pattern, the WiFi Information is retrieved via direct Read Requests to BLE characteristics. Get WiFi SSID The WiFi SSID can be found by reading from the WiFi AP SSID characteristic of the WiFi Access Point service. Let’s send the read request to get the SSID and decode it into a string. python kotlin ssid_uuid = GoProUuid.WIFI_AP_SSID_UUID logger.info(f\"Reading the WiFi AP SSID at {ssid_uuid}\") ssid = (await client.read_gatt_char(ssid_uuid.value)).decode() logger.info(f\"SSID is {ssid}\") There is no need for a synchronization event as the information is available when the read_gatt_char method returns. In the demo, this information is logged as such: Reading the WiFi AP SSID at GoProUuid.WIFI_AP_SSID_UUID SSID is GP24500702 ble.readCharacteristic(goproAddress, GoProUUID.WIFI_AP_SSID.uuid).onSuccess { ssid = it.decodeToString() } Timber.i(\"SSID is $ssid\") In the demo, this information is logged as such: Getting the SSID Read characteristic b5f90002-aa8d-11e3-9046-0002a5d5c51b : value: 64:65:62:75:67:68:65:72:6F:31:31 SSID is debughero11 Get WiFi Password The WiFi password can be found by reading from the WiFi AP password characteristic of the WiFi Access Point service. Let’s send the read request to get the password and decode it into a string. python kotlin password_uuid = GoProUuid.WIFI_AP_PASSWORD_UUID logger.info(f\"Reading the WiFi AP password at {password_uuid}\") password = (await client.read_gatt_char(password_uuid.value)).decode() logger.info(f\"Password is {password}\") There is no need for a synchronization event as the information is available when the read_gatt_char method returns. In the demo, this information is logged as such: Reading the WiFi AP password at GoProUuid.WIFI_AP_PASSWORD_UUID Password is p@d-NNc-2ts ble.readCharacteristic(goproAddress, GoProUUID.WIFI_AP_PASSWORD.uuid).onSuccess { password = it.decodeToString() } Timber.i(\"Password is $password\") In the demo, this information is logged as such: Getting the password Read characteristic b5f90003-aa8d-11e3-9046-0002a5d5c51b : value: 7A:33:79:2D:44:43:58:2D:50:68:6A Password is z3y-DCX-Phj Enable WiFi AP Before we can connect to the WiFi AP, we have to make sure the access point is enabled. This is accomplished via the AP Control command: Command Bytes Ap Control Enable 0x03 0x17 0x01 0x01 Ap Control Disable 0x03 0x17 0x01 0x00 We are using the same notification handler that was defined in the sending commands tutorial. Let’s write the bytes to the “Command Request UUID” to enable the WiFi AP! python kotlin event.clear() request = bytes([0x03, 0x17, 0x01, 0x01]) command_request_uuid = GoProUuid.COMMAND_REQ_UUID await client.write_gatt_char(command_request_uuid.value, request, response=True) await event.wait() Wait to receive the notification response We make sure to clear the synchronization event before writing, then pend on the event until it is set in the notification callback. val enableWifiCommand = ubyteArrayOf(0x03U, 0x17U, 0x01U, 0x01U) ble.writeCharacteristic(goproAddress, GoProUUID.CQ_COMMAND.uuid, enableWifiCommand) receivedData.receive() Note that we have received the “Command Status” notification response from the Command Response characteristic since we enabled it’s notifications in Enable Notifications. This can be seen in the demo log: python kotlin Enabling the WiFi AP Writing to GoProUuid.COMMAND_REQ_UUID: 03:17:01:01 Received response at GoProUuid.COMMAND_RSP_UUID: 02:17:00 Command sent successfully WiFi AP is enabled Enabling the camera's Wifi AP Writing characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b ==&gt; 03:17:01:01 Wrote characteristic b5f90072-aa8d-11e3-9046-0002a5d5c51b Characteristic b5f90073-aa8d-11e3-9046-0002a5d5c51b changed | value: 02:17:00 Received response on b5f90073-aa8d-11e3-9046-0002a5d5c51b: 02:17:00 Command sent successfully As expected, the response was received on the correct UUID and the status was “success”. Establish Connection to WiFi AP python kotlin If you have been following through the ble_enable_wifi.py script, you will notice that it ends here such that we know the WiFi SSID / password and the WiFi AP is enabled. This is because there are many different methods of connecting to the WiFi AP depending on your OS and the framework you are using to develop. You could, for example, simply use your OS’s WiFi GUI to connect. While out of the scope of these tutorials, there is a programmatic example of this in the cross-platform WiFi Demo from the Open GoPro Python SDK. Using the passwsord and SSID we discovered above, we will now connect to the camera’s network: wifi.connect(ssid, password) This should show a system popup on your Android device that eventually goes away once the Wifi is connected. This connection process appears to vary drastically in time. Quiz time! 📚 ✏️ How is the WiFi password response received? A: As a read response from the WiFi AP Password characteristic B: As write responses to the WiFi Request characteristic C: As notifications of the Command Response characteristic Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is A. This (and WiFi AP SSID) is an exception to the rule. Usually responses are received as notifications to a response characteristic. However, in this case, it is received as a direct read response (since we are reading from the characteristic and not writing to it). Which of the following statements about the GoPro WiFi AP is true? A: It only needs to be enabled once and it will then always remain on B: The WiFi password will never change C: The WiFi SSID will never change D: None of the Above Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is D. While the WiFi AP will remain on for some time, it can and will eventually turn off so it is always recommended to first connect via BLE and ensure that it is enabled. The password and SSID will almost never change. However, they will change if the connections are reset via Connections-&gt;Reset Connections. You are now connected to the GoPro’s Wifi AP and can send any of the HTTP commands defined in the HTTP Specification. Station (STA) Mode Station Mode is where the GoPro operates as a Station, allowing the camera to connect to and communicate with an Access Point such as a switch or a router. This is used, for example, in the livestreaming and camera on the home network (COHN) features. StationAccessPointGoProrouterclientBLEWifi When the GoPro is in Station Mode, there is no HTTP communication channel to the Open GoPro client. The GoPro can still be controlled via BLE. In order to configure the GoPro in Station mode, after connecting via BLE, pairing, and enabling notifications, we must: scan for available networks connect to a discovered network, using the correct API based on whether or not we have previously connected to this network The following subsections will detail these steps. All of the Protobuf operations are performed in the same manner as in the protobuf tutorial such as reusing the ResponseManager. Scan for Networks It is always necessary to scan for networks, regardless of whether you already have a network’s information and know it is available. Failure to do so follows an untested and unsupported path in the GoPro’s connection state machine. The process of scanning for networks requires several Protobuf Operations as summarized here: Scan For Networks First we must request the GoPro to Scan For Access Points: python kotlin The code here is taken from connect_as_sta.py Let’s send the scan request and then retrieve and parse notifications until we receive a notification where the scanning_state is set to SCANNING_SUCCESS. Then we store the scan id from the notification for later use in retrieving the scan results. start_scan_request = bytearray( [ 0x02, Feature ID 0x02, Action ID *proto.RequestStartScan().SerializePartialToString(), ] ) start_scan_request.insert(0, len(start_scan_request)) await manager.client.write_gatt_char(GoProUuid.NETWORK_MANAGEMENT_REQ_UUID.value, start_scan_request, response=True) while response := await manager.get_next_response_as_protobuf(): ... elif response.action_id == 0x0B: Scan Notifications scan_notification: proto.NotifStartScanning = response.data type: ignore logger.info(f\"Received scan notification: {scan_notification}\") if scan_notification.scanning_state == proto.EnumScanning.SCANNING_SUCCESS: return scan_notification.scan_id This will log as such: Scanning for available Wifi Networks Writing: 02:02:02 Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 06:02:82:08:01:10:02 Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 0a:02:0b:08:05:10:01:18:05:20:01 Received scan notification: scanning_state: SCANNING_SUCCESS scan_id: 1 total_entries: 5 total_configured_ssid: 1 TODO Next we must request the GoPro to return the Scan Results. Using the scan_id from above, let’s send the Get AP Scan Results request, then retrieve and parse the response: python kotlin results_request = bytearray( [ 0x02, Feature ID 0x03, Action ID *proto.RequestGetApEntries(start_index=0, max_entries=100, scan_id=scan_id).SerializePartialToString(), ] ) results_request.insert(0, len(results_request)) await manager.client.write_gatt_char(GoProUuid.NETWORK_MANAGEMENT_REQ_UUID.value, results_request, response=True) response := await manager.get_next_response_as_protobuf(): entries_response: proto.ResponseGetApEntries = response.data type: ignore logger.info(\"Found the following networks:\") for entry in entries_response.entries: logger.info(str(entry)) return list(entries_response.entries) This will log as such: Getting the scanned networks. Writing: 08:02:03:08:00:10:64:18:01 Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 20:76:02:83:08:01:10:01:1a:13:0a:0a:64:61:62:75:67:64:61:62 Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 80:75:67:10:03:20:e4:28:28:2f:1a:13:0a:0a:41:54:54:54:70:34 Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 81:72:36:46:69:10:02:20:f1:2c:28:01:1a:13:0a:0a:41:54:54:62 Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 82:37:4a:67:41:77:61:10:02:20:99:2d:28:01:1a:16:0a:0d:52:69 Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 83:6e:67:20:53:65:74:75:70:20:65:37:10:01:20:ec:12:28:00:1a Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 84:17:0a:0e:48:6f:6d:65:79:6e:65:74:5f:32:47:45:58:54:10:01 Received response at GoProUuid.NETWORK_MANAGEMENT_RSP_UUID: 85:20:85:13:28:01 Found the following networks: ssid: \"dabugdabug\" signal_strength_bars: 3 signal_frequency_mhz: 5220 scan_entry_flags: 47 ssid: \"ATTTp4r6Fi\" signal_strength_bars: 2 signal_frequency_mhz: 5745 scan_entry_flags: 1 ssid: \"ATTb7JgAwa\" signal_strength_bars: 2 signal_frequency_mhz: 5785 scan_entry_flags: 1 ssid: \"Ring Setup e7\" signal_strength_bars: 1 signal_frequency_mhz: 2412 scan_entry_flags: 0 ssid: \"Homeynet_2GEXT\" signal_strength_bars: 1 signal_frequency_mhz: 2437 scan_entry_flags: 1 TODO At this point we have all of the discovered networks. Continue on to see how to use this information. Connect to Network Depending on whether the GoPro has already connected to the desired network, we must next perform either the Connect or Connect New operation. This will be described below but first, a note on fragmentation: GATT Write Fragmentation Up to this point in the tutorials, all of the operations we have been performing have resulted in GATT write requests guaranteed to be less than maximum BLE packet size of 20 bytes. However, depending on the SSID and password used in the Connect New operation, this maximum size might be surpassed. Therefore, it is necessary to fragment the payload. This is essentially the inverse of the accumulation algorithm. We accomplish this as follows: python kotlin Let’s create a generator to yield fragmented packets (yield_fragmented_packets) from a monolithic payload. First, depending on the length of the payload, we create the header for the first packet that specifies the total payload length: if length &lt; (2**13 - 1): header = bytearray((length | 0x2000).to_bytes(2, \"big\", signed=False)) elif length &lt; (2**16 - 1): header = bytearray((length | 0x6400).to_bytes(2, \"big\", signed=False)) Then we chunk through the payload, prepending either the above header for the first packet or the continuation header for subsequent packets: byte_index = 0 while bytes_remaining := length - byte_index: If this is the first packet, use the appropriate header. Else use the continuation header if is_first_packet: packet = bytearray(header) is_first_packet = False else: packet = bytearray(CONTINUATION_HEADER) Build the current packet packet_size = min(MAX_PACKET_SIZE - len(packet), bytes_remaining) packet.extend(bytearray(payload[byte_index : byte_index + packet_size])) yield bytes(packet) Increment byte_index for continued processing byte_index += packet_size Finally we create a helper method that we can reuse throughout the tutorials to use this generator to send GATT Writes using a given Bleak client: async def fragment_and_write_gatt_char(client: BleakClient, char_specifier: str, data: bytes): for packet in yield_fragmented_packets(data): await client.write_gatt_char(char_specifier, packet, response=True) TODO The safest solution would be to always use the above fragmentation method. For the sake of simplicity in these tutorials, we are only using this where there is a possibility of exceeding the maximum BLE packet size. Connect Example In order to proceed, we must first inspect the scan result gathered from the previous section to see which connect operation to use. Specifically we are checking the scan_entry_flags to see if the SCAN_FLAG_CONFIGURED bit is set. If the bit is set (and thus we have already provisioned this network) then we must use Connect . Otherwise we must use Connect New: python kotlin if entry.scan_entry_flags &amp; proto.EnumScanEntryFlags.SCAN_FLAG_CONFIGURED: connect_request = bytearray( [ 0x02, Feature ID 0x04, Action ID *proto.RequestConnect(ssid=entry.ssid).SerializePartialToString(), ] ) else: connect_request = bytearray( [ 0x02, Feature ID 0x05, Action ID *proto.RequestConnectNew(ssid=entry.ssid, password=password).SerializePartialToString(), ] ) TODO Now that we have the correct request built, we can send it (using our newly created fragmentation method) we can send it. Then we will continuously receive Provisioning Notifications which should be checked until the provisioning_state is set to PROVISIONING_SUCCESS_NEW_AP. The final provisioning_state that we are looking for is always PROVISIONING_SUCCESS_NEW_AP both in the Connect and Connect New use cases. The procedure is summarized here: Connect to Already Configured Network python kotlin await fragment_and_write_gatt_char(manager.client, GoProUuid.NETWORK_MANAGEMENT_REQ_UUID.value, connect_request) while response := await manager.get_next_response_as_protobuf(): ... elif response.action_id == 0x0C: NotifProvisioningState Notifications provisioning_notification: proto.NotifProvisioningState = response.data type: ignore if provisioning_notification.provisioning_state == proto.EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP: return TODO At this point, the GoPro is connect to the desired network in Station Mode! Quiz time! 📚 ✏️ True or False: When the GoPro is in Station Mode, it can be communicated with via both BLE and HTTP. A: True B: False Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is B. When the GoPro is in station mode, it is connected via WiFi to another Access Point; not connected via Wifi to you (the client). However, it is possible to maintain the BLE connection in STA mode so that you can still control the GoPro. Troubleshooting See the first tutorial’s BLE troubleshooting section to troubleshoot BLE problems. Good Job! Congratulations 🤙 You have now connected the GoPro to a WiFi network in either AP or STA mode. To see how to make use of AP mode, continue to the next tutorial. To see how make use of STA mode, continue to the camera on the home network tutorial.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/connect-wifi#"
        },
        {
            "title": "Tutorial 7: Send WiFi Commands: ",
            "excerpt": "This document will provide a walk-through tutorial to perform Open GoPro HTTP Operations with the GoPro. It is suggested that you have first completed the Connecting to Wifi tutorial. This tutorial only considers sending these commands as one-off commands. That is, it does not consider state management / synchronization when sending multiple commands. This will be discussed in a future tutorial. There are two types of responses that can be received from the HTTP commands: JSON and binary. This section will deal with commands that return JSON responses. For commands with binary responses (as well as commands with JSON responses that work with the media list), see the next tutorial. Requirements It is assumed that the hardware and software requirements from the connecting BLE tutorial are present and configured correctly. The scripts that will be used for this tutorial can be found in the Tutorial 7 Folder. Just Show me the Demo(s)!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 7 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements You must be connected to the camera via WiFi as stated in Tutorial 6. Get Camera State You can test querying the state of your camera with HTTP over WiFi using the following script: $ python wifi_command_get_state.py See the help for parameter definitions: $ python wifi_command_get_state.py --help usage: wifi_command_get_state.py [-h] Get the state of the GoPro (status and settings). optional arguments: -h, --help show this help message and exit Preview Stream You can test enabling the UDP preview stream with HTTP over WiFi using the following script: $ python wifi_command_preview_stream.py See the help for parameter definitions: $ python wifi_command_preview_stream.py --help usage: wifi_command_preview_stream.py [-h] Enable the preview stream. optional arguments: -h, --help show this help message and exit Once enabled the stream can be viewed at udp://@:8554 (For more details see the View Stream tab in the Preview Stream section below. Load Preset Group You can test sending the load preset group command with HTTP over WiFi using the following script: $ python wifi_command_load_group.py See the help for parameter definitions: $ python wifi_command_load_group.py --help usage: wifi_command_load_group.py [-h] Load the video preset group. optional arguments: -h, --help show this help message and exit Set Shutter You can test sending the Set Shutter command with HTTP over WiFi using the following script: $ python wifi_command_set_shutter.py See the help for parameter definitions: $ python wifi_command_set_shutter.py --help usage: wifi_command_set_shutter.py [-h] Take a 3 second video. optional arguments: -h, --help show this help message and exit Set Setting You can test setting the resolution setting with HTTP over WiFi using the following script: $ python wifi_command_set_resolution.py See the help for parameter definitions: $ python wifi_command_set_resolution.py --help usage: wifi_command_set_resolution.py [-h] Set the video resolution to 1080. optional arguments: -h, --help show this help message and exit The Kotlin file for this tutorial can be found on Github. To perform the tutorial, run the Android Studio project, select “Tutorial 7” from the dropdown and click on “Perform.” This requires: a GoPro is already connected via BLE, i.e. that Tutorial 1 was already run. a GoPro is already connected via Wifi, i.e. that Tutorial 5 was already run. You can check the BLE and Wifi statuses at the top of the app. Perform Tutorial 7 This will start the tutorial and log to the screen as it executes. When the tutorial is complete, click “Exit Tutorial” to return to the Tutorial selection screen. Setup We must first connect to The GoPro’s WiFi Access Point (AP) as was discussed in the Connecting to Wifi tutorial. Sending HTTP Commands with JSON Responses Now that we are are connected via WiFi, we can communicate via HTTP commands. python kotlin We will use the requests package to send the various HTTP commands. We are building the endpoints using the GOPRO_BASE_URL defined in the tutorial package’s __init__.py We are using ktor for the HTTP client. We are using an abstracted get function from our Wifi class to send get requests as such: private val client by lazy { HttpClient(CIO) { install(HttpTimeout) } } suspend fun get(endpoint: String, timeoutMs: Long = 5000L): JsonObject { Timber.d(\"GET request to: $endpoint\") val response = client.request(endpoint) { timeout { requestTimeoutMillis = timeoutMs } } val bodyAsString: String = response.body() return prettyJson.parseToJsonElement(bodyAsString).jsonObject } Both Command Requests and Setting Requests follow the same procedure: Send HTTP GET command to appropriate endpoint Receive confirmation from GoPro (via HTTP response) that request was received. GoPro reacts to command The HTTP response only indicates that the request was received correctly. The relevant behavior of the GoPro must be observed to verify when the command’s effects have been applied. GoProOpen GoPro user deviceGoProOpen GoPro user devicePC connected to WiFi APCommand Request (GET)Command Response (HTTP 200 OK)Apply affects of command when able Get Camera State The first command we will be sending is Get Camera State. This command will return all of the current settings and values. It is basically a combination of the Get All Settings and Get All Statuses commands that were sent via BLE. Since there is no way to query individual settings / statuses via WiFi (or register for asynchronous notifications when they change), this is the only option to query setting / status information via WiFi. The command writes to the following endpoint: /gopro/camera/state Let’s build the endpoint then perform the GET operation and check the response for errors. Any errors will raise an exception. python kotlin url = GOPRO_BASE_URL + \"/gopro/camera/state\" response = requests.get(url) response.raise_for_status() var response = wifi.get(GOPRO_BASE_URL + \"gopro/camera/state\") Lastly, we print the response’s JSON data: python kotlin logger.info(f\"Response: {json.dumps(response.json(), indent=4)}\") The response will log as such (abbreviated for brevity): INFO:root:Getting GoPro's status and settings: sending http://10.5.5.9:8080/gopro/camera/state INFO:root:Command sent successfully INFO:root:Response: { \"status\": { \"1\": 1, \"2\": 2, \"3\": 0, \"4\": 255, \"6\": 0, \"8\": 0, \"9\": 0, \"10\": 0, \"11\": 0, \"13\": 0, \"14\": 0, \"17\": 1, ... \"settings\": { \"2\": 9, \"3\": 1, \"5\": 0, \"6\": 1, \"13\": 1, \"19\": 0, \"24\": 0, \"30\": 0, \"31\": 0, \"32\": 10, \"41\": 9, \"42\": 5, Timber.i(prettyJson.encodeToString(response)) The response will log as such (abbreviated for brevity): Getting camera state GET request to: http://10.5.5.9:8080/gopro/camera/state { \"status\": { \"1\": 1, \"2\": 4, \"3\": 0, \"4\": 255, \"6\": 0, \"8\": 0, \"9\": 0, \"10\": 0, \"11\": 0, \"13\": 0, ... \"113\": 0, \"114\": 0, \"115\": 0, \"116\": 0, \"117\": 31154688 }, \"settings\": { \"2\": 9, \"3\": 1, \"5\": 0, \"6\": 1, \"13\": 1, ... \"177\": 0, \"178\": 1, \"179\": 3, \"180\": 0, \"181\": 0 } } We can see what each of these values mean by looking at relevant documentation in the settings or status object of the State schema. For example (for settings): ID 2 == 9 equates to Resolution == 1080 ID 3 == 1 equates to FPS == 120 Load Preset Group The next command we will be sending is Load Preset Group, which is used to toggle between the 3 groups of presets (video, photo, and timelapse). The preset groups ID’s are: Command Bytes Load Video Preset Group 1000 Load Photo Preset Group 1001 Load Timelapse Preset Group 1002 python kotlin url = GOPRO_BASE_URL + \"/gopro/camera/presets/set_group?id=1000\" response = requests.get(url) response.raise_for_status() response = wifi.get(GOPRO_BASE_URL + \"gopro/camera/presets/load?id=1000\") Lastly, we print the response’s JSON data: python kotlin logger.info(f\"Response: {json.dumps(response.json(), indent=4)}\") This will log as such: INFO:root:Loading the video preset group: sending http://10.5.5.9:8080/gopro/camera/presets/set_group?id=1000 INFO:root:Command sent successfully INFO:root:Response: {} Timber.i(prettyJson.encodeToString(response)) The response will log as such: Loading Video Preset Group GET request to: http://10.5.5.9:8080/gopro/camera/presets/load?id=1000 { } Lastly, we print the response’s JSON data: The response JSON is empty. This is expected in the case of a success. You should hear the camera beep and switch to the Cinematic Preset (assuming it wasn’t already set). You can verify this by seeing the preset name in the pill at bottom middle of the screen. Load Preset Set Shutter The next command we will be sending is Set Shutter. which is used to start and stop encoding. python kotlin url = GOPRO_BASE_URL + f\"/gopro/camera/shutter/start\" response = requests.get(url) response.raise_for_status() response = wifi.get(GOPRO_BASE_URL + \"gopro/camera/shutter/start\") Lastly, we print the response’s JSON data: This command does not return a JSON response so we don’t print the response This will log as such: python kotlin INFO:root:Turning the shutter on: sending http://10.5.5.9:8080/gopro/camera/shutter/start INFO:root:Command sent successfully Timber.i(prettyJson.encodeToString(response)) The response will log as such: Setting Shutter On GET request to: http://10.5.5.9:8080/gopro/camera/shutter/start { } We can then wait a few seconds and repeat the above procedure to set the shutter off using gopro/camera/shutter/stop. The shutter can not be set on if the camera is encoding or set off if the camera is not encoding. An attempt to do so will result in an error response. Set Setting The next command will be sending is Set Setting. This end point is used to update all of the settings on the camera. It is analogous to BLE commands like Set Video Resolution. It is important to note that many settings are dependent on the video resolution (and other settings). For example, certain FPS values are not valid with certain resolutions. In general, higher resolutions only allow lower FPS values. Check the camera capabilities to see which settings are valid for given use cases. Let’s build the endpoint first to set the Video Resolution to 1080 (the setting_id and option value comes from the command table linked above). python kotlin url = GOPRO_BASE_URL + f\"/gopro/camera/setting?setting=2&amp;option=9\" response = requests.get(url) response.raise_for_status() response = wifi.get(GOPRO_BASE_URL + \"gopro/camera/setting?setting=2&amp;option=9\") Lastly, we print the response’s JSON data: python kotlin logger.info(f\"Response: {json.dumps(response.json(), indent=4)}\") This will log as such: INFO:root:Setting the video resolution to 1080: sending http://10.5.5.9:8080/gopro/camera/setting?setting_id=2&amp;opt_value=9 INFO:root:Command sent successfully INFO:root:Response: {} Timber.i(prettyJson.encodeToString(response)) The response will log as such: Setting Resolution to 1080 GET request to: http://10.5.5.9:8080/gopro/camera/setting?setting=2&amp;option=9 { } The response JSON is empty. This is expected in the case of a success. You should hear the camera beep and see the video resolution change to 1080 in the pill in the bottom-middle of the screen: Video Resolution As a reader exercise, try using the Get Camera State command to verify that the resolution has changed. Preview Stream The next command we will be sending is Start Preview Stream. This command will enable (or disable) the preview stream . It is then possible to view the preview stream from a media player. The commands write to the following endpoints: Command Endpoint start preview stream /gopro/camera/stream/start stop preview stream /gopro/camera/stream/stop Let’s build the endpoint then send the GET request and check the response for errors. Any errors will raise an exception. python kotlin url = GOPRO_BASE_URL + \"/gopro/camera/stream/start\" response = requests.get(url) response.raise_for_status() TODO Lastly, we print the response’s JSON data: python kotlin logger.info(f\"Response: {json.dumps(response.json(), indent=4)}\") This will log as such: INFO:root:Starting the preview stream: sending http://10.5.5.9:8080/gopro/camera/stream/start INFO:root:Command sent successfully INFO:root:Response: {} TODO The response JSON is empty. This is expected in the case of a success. Once enabled, the stream can be viewed at udp://@:8554. Here is an example of viewing this using VLC: The screen may slightly vary depending on your OS Select Media–&gt;Open Network Stream Enter the path as such: Configure Preview Stream Select play The preview stream should now be visible. Quiz time! 📚 ✏️ What is the significance of empty JSON in an HTTP response? A: Always an error! The command was not received correctly. B: If the status is ok (200), this is expected. C: This is expected for errors (code other than 200) but not expected for ok (200). Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is B. It is common for the JSON response to be empty if the command was received successfully but there is no additional information to return at the current time. Which of the of the following is not a real preset group? A: Timelapse B: Photo C: Burst D: Video Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is C. There are 3 preset groups (Timelapse, Photo, and Video). These can be set via the Load Preset Group command. How do you query the current video resolution setting (id = 2) via WiFi? A: Send GET to /gopro/camera/state?setting_id=2 B: Send GET to /gopro/camera/state?get_setting=2 C: Send POST to /gopro/camera/state with request &8216;setting_id=2&8217; D: None of the Above Submit Answer Correct!! 😃 Incorrect!! 😭 The correct answer is D. You can&8217;t query individual settings or statuses with the HTTP API. In order to get the value of a specific setting you&8217;ll need to send a GET to /gopro/camera/state and parse the value of the desired setting from the JSON response. Troubleshooting HTTP Logging Wireshark can be used to view the HTTP commands and responses between the PC and the GoPro. Start a Wireshark capture on the WiFi adapter that is used to connect to the GoPro Filter for the GoPro IP address (10.5.5.9) Wireshark Good Job! Congratulations 🤙 You can now send any of the HTTP commands defined in the Open GoPro Interface that return JSON responses. You may have noted that we did not discuss one of these (Get Media List) in this tutorial. Proceed to the next tutorial to see how to get and perform operations using the media list.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/send-wifi-commands#"
        },
        {
            "title": "Tutorial 8: Camera Media List: ",
            "excerpt": "This document will provide a walk-through tutorial to send Open GoPro HTTP commands to the GoPro, specifically to get the media list and perform operations on it (downloading pictures, videos, etc.) It is suggested that you have first completed the Connecting to Wifi and Sending WiFi Commands tutorials. This tutorial only considers sending these commands as one-off commands. That is, it does not consider state management / synchronization when sending multiple commands. This will be discussed in a future tutorial. Requirements It is assumed that the hardware and software requirements from the connecting BLE tutorial are present and configured correctly. The scripts that will be used for this tutorial can be found in the Tutorial 8 Folder. Just Show me the Demo(s)!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 8 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements You must be connected to the camera via WiFi in order to run these scripts. You can do this by manually to the SSID and password listed on your camera or by leaving the Establish Connection to WiFi AP script from Tutorial 5 running in the background. Download Media File You can downloading a file from your camera with HTTP over WiFi using the following script: $ python wifi_media_download_file.py See the help for parameter definitions: $ python wifi_media_download_file.py --help usage: wifi_media_download_file.py [-h] Find a photo on the camera and download it to the computer. optional arguments: -h, --help show this help message and exit Get Media Thumbnail You can downloading the thumbnail for a media file from your camera with HTTP over WiFi using the following script: $ python wifi_media_get_thumbnail.py See the help for parameter definitions: $ python wifi_media_get_thumbnail.py --help usage: wifi_media_get_thumbnail.py [-h] Get the thumbnail for a media file. optional arguments: -h, --help show this help message and exit The Kotlin file for this tutorial can be found on Github. To perform the tutorial, run the Android Studio project, select “Tutorial 8” from the dropdown and click on “Perform.” This requires: a GoPro is already connected via BLE, i.e. that Tutorial 1 was already run. a GoPro is already connected via Wifi, i.e. that Tutorial 5 was already run. You can check the BLE and Wifi statuses at the top of the app. Perform Tutorial 8 This will start the tutorial and log to the screen as it executes. When the tutorial is complete, click “Exit Tutorial” to return to the Tutorial selection screen. Setup We must first connect to The GoPro’s WiFi Access Point (AP) as was discussed in the Connecting to Wifi tutorial. Get Media List Now that we are are connected via WiFi, we will get the media list using the same procedure to send HTTP commands as in the previous tutorial. We get the media list via Get Media List. This will return a JSON structure of all of the media files (pictures, videos) on the camera with corresponding information about each media file. Let’s build the endpoint, send the GET request, and check the response for errors. Any errors will raise an exception. python kotlin url = GOPRO_BASE_URL + \"/gopro/media/list\" response = requests.get(url) response.raise_for_status() val response = wifi.get(GOPRO_BASE_URL + \"gopro/media/list\") Lastly, we print the response’s JSON data: python kotlin logger.info(f\"Response: {json.dumps(response.json(), indent=4)}\") The response will log as such (abbreviated for brevity): INFO:root:Getting the media list: sending http://10.5.5.9:8080/gopro/media/list INFO:root:Command sent successfully INFO:root:Response: { \"id\": \"2510746051348624995\", \"media\": [ { \"d\": \"100GOPRO\", \"fs\": [ { \"n\": \"GOPR0987.JPG\", \"cre\": \"1618583762\", \"mod\": \"1618583762\", \"s\": \"5013927\" }, { \"n\": \"GOPR0988.JPG\", \"cre\": \"1618583764\", \"mod\": \"1618583764\", \"s\": \"5009491\" }, { \"n\": \"GOPR0989.JPG\", \"cre\": \"1618583766\", \"mod\": \"1618583766\", \"s\": \"5031861\" }, { \"n\": \"GX010990.MP4\", \"cre\": \"1451608343\", \"mod\": \"1451608343\", \"glrv\": \"806586\", \"ls\": \"-1\", \"s\": \"10725219\" }, Timber.i(\"Files in media list: ${prettyJson.encodeToString(fileList)}\") The response will log as such (abbreviated for brevity): GET request to: http://10.5.5.9:8080/gopro/media/list Complete media list: { \"id\": \"4386457835676877283\", \"media\": [ { \"d\": \"100GOPRO\", \"fs\": [ { \"n\": \"GOPR0232.JPG\", \"cre\": \"1748997965\", \"mod\": \"1748997965\", \"s\": \"7618898\" }, { \"n\": \"GOPR0233.JPG\", \"cre\": \"1748998273\", \"mod\": \"1748998273\", \"s\": \"7653472\" }, ... { \"n\": \"GX010259.MP4\", \"cre\": \"1677828860\", \"mod\": \"1677828860\", \"glrv\": \"943295\", \"ls\": \"-1\", \"s\": \"9788009\" } ] } ] } The media list format is defined in the Media Model. We won’t be rehashing that here but will provide examples below of using the media list. One common functionality is to get the list of media file names, which can be done as such: python kotlin print([x[\"n\"] for x in media_list[\"media\"][0][\"fs\"]]) That is, access the list at the fs tag at the first element of the media tag, then make a list of all of the names (n tag of each element) in the fs list. val fileList = response[\"media\"]?.jsonArray?.first()?.jsonObject?.get(\"fs\")?.jsonArray?.map { mediaEntry -&gt; mediaEntry.jsonObject[\"n\"] }?.map { it.toString().replace(\"\\\"\", \"\") } That is: Access the JSON array at the fs tag at the first element of the media tag Make a list of all of the names (n tag of each element) in the fs list. Map this list to string and remove backslashes Media List Operations Whereas all of the WiFi commands described until now have returned JSON responses, most of the media list operations return binary data. From an HTTP perspective, the behavior is the same. However, the GET response will contain a large binary chunk of information so we will loop through it with the requests library as such, writing up to 8 kB at a time: GoProOpen GoPro user devicediskGoProOpen GoPro user devicediskPC connected to WiFi APloop[write until complete]Get Media List (GET)Media List (HTTP 200 OK)Command Request (GET)Binary Response (HTTP 200 OK)write &lt;= 8K Download Media File TODO Handle directory in media list. The next command we will be sending is Download Media. Specifically, we will be downloading a photo. The camera must have at least one photo in its media list in order for this to work. First, we get the media list as in Get Media List . Then we search through the list of file names in the media list looking for a photo (i.e. a file whose name ends in .jpg). Once we find a photo, we proceed: python kotlin media_list = get_media_list() photo: Optional[str] = None for media_file in [x[\"n\"] for x in media_list[\"media\"][0][\"fs\"]]: if media_file.lower().endswith(\".jpg\"): logger.info(f\"found a photo: {media_file}\") photo = media_file break val photo = fileList?.firstOrNull { it.endsWith(ignoreCase = true, suffix = \"jpg\") } ?: throw Exception(\"Not able to find a .jpg in the media list\") Timber.i(\"Found a photo: $photo\") Now let’s build the endpoint, send the GET request, and check the response for errors. Any errors will raise an exception. The endpoint will start with “videos” for both photos and videos python kotlin url = GOPRO_BASE_URL + f\"videos/DCIM/100GOPRO/{photo}\" with requests.get(url, stream=True) as request: request.raise_for_status() Lastly, we iterate through the binary content in 8 kB chunks, writing to a local file: file = photo.split(\".\")[0] + \".jpg\" with open(file, \"wb\") as f: logger.info(f\"receiving binary stream to {file}...\") for chunk in request.iter_content(chunk_size=8192): f.write(chunk) return wifi.getFile( GOPRO_BASE_URL + \"videos/DCIM/100GOPRO/$photo\", appContainer.applicationContext ) TODO FIX THIS This will log as such: python kotlin INFO:root:found a photo: GOPR0987.JPG INFO:root:Downloading GOPR0987.JPG INFO:root:Sending: http://10.5.5.9:8080/videos/DCIM/100GOPRO/GOPR0987.JPG INFO:root:receiving binary stream to GOPR0987.jpg... Once complete, the GOPR0987_thumbnail.jpg file will be available from where the demo script was called. Found a photo: GOPR0232.JPG Downloading photo: GOPR0232.JPG... Once complete, the photo will display in the tutorial window. Get Media Thumbnail The next command we will be sending is Get Media thumbnail . Specifically, we will be getting the thumbnail for a photo. The camera must have at least one photo in its media list in order for this to work. There is a separate commandto get a media “screennail” First, we get the media list as in Get Media List . Then we search through the list of file names in the media list looking for a photo (i.e. a file whose name ends in .jpg). Once we find a photo, we proceed: python kotlin media_list = get_media_list() photo: Optional[str] = None for media_file in [x[\"n\"] for x in media_list[\"media\"][0][\"fs\"]]: if media_file.lower().endswith(\".jpg\"): logger.info(f\"found a photo: {media_file}\") photo = media_file break TODO Now let’s build the endpoint, send the GET request, and check the response for errors. Any errors will raise an exception. python kotlin url = GOPRO_BASE_URL + f\"/gopro/media/thumbnail?path=100GOPRO/{photo}\" with requests.get(url, stream=True) as request: request.raise_for_status() Lastly, we iterate through the binary content in 8 kB chunks, writing to a local file: file = photo.split(\".\")[0] + \".jpg\" with open(file, \"wb\") as f: logger.info(f\"receiving binary stream to {file}...\") for chunk in request.iter_content(chunk_size=8192): f.write(chunk) TODO This will log as such: python kotlin INFO:root:found a photo: GOPR0987.JPG INFO:root:Getting the thumbnail for GOPR0987.JPG INFO:root:Sending: http://10.5.5.9:8080/gopro/media/thumbnail?path=100GOPRO/GOPR0987.JPG INFO:root:receiving binary stream to GOPR0987_thumbnail.jpg... TODO Troubleshooting See the previous tutorial’s troubleshooting section. Good Job! Congratulations 🤙 You can now query the GoPro’s media list and retrieve binary information for media file. This is currently last tutorial. Stay tuned for more 👍 At this point you should be able to start creating a useful example using the Open GoPro Interface. For some inspiration check out some of the demos.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/camera-media-list#"
        },
        {
            "title": "Tutorial 9: Camera on the Home Network: ",
            "excerpt": "This document will provide a walk-through tutorial to use the Open GoPro Interface to configure and demonstrate the Camera on the Home Network (COHN) feature. It is recommended that you have first completed the connecting BLE, sending commands, parsing responses, protobuf, and connecting WiFi tutorials before proceeding. Requirements It is assumed that the hardware and software requirements from the connecting BLE tutorial are present and configured correctly. The scripts that will be used for this tutorial can be found in the Tutorial 9 Folder. Just Show me the Demo(s)!! python kotlin Each of the scripts for this tutorial can be found in the Tutorial 9 directory. Python &gt;= 3.9 and &lt; 3.12 must be used as specified in the requirements Provision COHN You can provision the GoPro for COHN to communicate via a network via: $ python provision_cohn.py See the help for parameter definitions: $ python provision_cohn.py --help usage: provision_cohn.py [-h] [-i IDENTIFIER] [-c CERTIFICATE] ssid password Provision COHN via BLE to be ready for communication. positional arguments: ssid SSID of network to connect to password Password of network to connect to options: -h, --help show this help message and exit -i IDENTIFIER, --identifier IDENTIFIER Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to -c CERTIFICATE, --certificate CERTIFICATE Path to write retrieved COHN certificate. Communicate via COHN You can see an example of communicating HTTPS via COHN (assuming it has already been provisioned) via: $ python communicate_via_cohn.py See the help for parameter definitions: $ python communicate_via_cohn.py --help usage: communicate_via_cohn.py [-h] ip_address username password certificate Demonstrate HTTPS communication via COHN. positional arguments: ip_address IP Address of camera on the home network username COHN username password COHN password certificate Path to read COHN cert from. options: -h, --help show this help message and exit TODO Setup We must first connect to BLE as was discussed in the connecting BLE tutorial. The GoPro must then be connected to an access point as was discussed in the Connecting WiFi Tutorial. For all of the BLE operations, we are using the same ResponseManager class that was defined in the Protobuf tutorial. COHN Overview The Camera on the Home Network feature allows the GoPro to connect (in Station Mode) to an Access Point (AP) such as a router in order to be controlled over a local network via the HTTP API. In order to protect users who connect to a network that includes Bad Actors, COHN uses SSL/TLS so that command and responses are sent securely encrypted via https:// rather than http://. Once COHN is provisioned it is possible to control the GoPro without a BLE connection by communicating via HTTPS over the provisioned network. Provisioning In order to use the COHN capability, the GoPro must first be provisioned for COHN via BLE. At a high level, the provisioning process is as follows: Connect the GoPro to an access point Instruct the GoPro to create a COHN Certificate Get the created COHN certificate Get the COHN status to retrieve and store COHN credentials for future use A summary of this process is shown here and will be expanded upon in the following sections: Provision COHN Set Date Time While not explicitly part of of the provisioning process, it is important that the GoPro’s date and time are correct so that it generates a valid SSL certificate. This can be done manually through the camera UI or programatically using the Set Local Datetime command. For the provisioning demo discussed in this tutorial, this is done programatically: python kotlin The code shown here can be found in provision_cohn.py We’re using the pytz and tzlocal libraries to find the timezone offset and daylight savings time status. In the set_date_time method, we send the request and wait to receive the successful response: datetime_request = bytearray( [ 0x0F, Command ID 10, Length of following datetime parameter *now.year.to_bytes(2, \"big\", signed=False), uint16 year now.month, now.day, now.hour, now.minute, now.second, *offset.to_bytes(2, \"big\", signed=True), int16 offset in minutes is_dst, ] ) datetime_request.insert(0, len(datetime_request)) await manager.client.write_gatt_char(GoProUuid.COMMAND_REQ_UUID.value, datetime_request, response=True) response = await manager.get_next_response_as_tlv() which logs as: Setting the camera's date and time to 2024-04-04 13:00:05.097305-07:00:-420 is_dst=True Writing: 0c:0f:0a:07:e8:04:04:0d:00:05:fe:5c:01 Received response at GoProUuid.COMMAND_RSP_UUID: 02:0f:00 Successfully set the date time. TODO Create the COHN Certificate Now that the GoPro’s date and time are valid and it has been connected to an Access Point, we can continue to provision COHN. Let’s instruct the GoPro to Create a COHN certificate. python kotlin create_request = bytearray( [ 0xF1, Feature ID 0x67, Action ID *proto.RequestCreateCOHNCert().SerializePartialToString(), ] ) create_request.insert(0, len(create_request)) await manager.client.write_gatt_char(GoProUuid.COMMAND_REQ_UUID.value, create_request, response=True) response := await manager.get_next_response_as_protobuf() which logs as: Creating a new COHN certificate. Writing: 02:f1:67 Received response at GoProUuid.COMMAND_RSP_UUID: 04:f1:e7:08:01 COHN certificate successfully created TODO You may notice that the provisioning demo first Clears the COHN Certificate. This is is only to ensure a consistent starting state in the case that COHN has already been provisioned. It is not necessary to clear the certificate if COHN has not yet been provisioned. Get the COHN Credentials At this point the GoPro has created the certificate and is in the process of provisioning COHN. We now need to get the COHN credentials that will be used for HTTPS communication. These are: COHN certificate Basic auth username Baisc auth password IP Address of COHN network We can immediately get the COHN certificate as such: python kotlin cert_request = bytearray( [ 0xF5, Feature ID 0x6E, Action ID *proto.RequestCOHNCert().SerializePartialToString(), ] ) cert_request.insert(0, len(cert_request)) await manager.client.write_gatt_char(GoProUuid.QUERY_REQ_UUID.value, cert_request, response=True) response := await manager.get_next_response_as_protobuf(): cert_response: proto.ResponseCOHNCert = response.data type: ignore return cert_response.cert TODO For the remaining credentials, we need to wait until the COHN network is connected. That is, we need to Get COHN Status until we receive a status where the state is set to COHN_STATE_NetworkConnected. This final status contains the remaining credentials: username, password, and IP Address. To do this, we first register to receive asynchronous COHN status updates: python kotlin status_request = bytearray( [ 0xF5, Feature ID 0x6F, Action ID *proto.RequestGetCOHNStatus(register_cohn_status=True).SerializePartialToString(), ] ) status_request.insert(0, len(status_request)) await manager.client.write_gatt_char(GoProUuid.QUERY_REQ_UUID.value, status_request, response=True) TODO Then we continuously receive and check the updates until we receive the desired status: python kotlin while response := await manager.get_next_response_as_protobuf(): cohn_status: proto.NotifyCOHNStatus = response.data type: ignore if cohn_status.state == proto.EnumCOHNNetworkState.COHN_STATE_NetworkConnected: return cohn_status This will all display in the log as such: Checking COHN status until provisioning is complete Writing: 04:f5:6f:08:01 ... Received response at GoProUuid.QUERY_RSP_UUID: 20:47:f5:ef:08:01:10:1b:1a:05:67:6f:70:72:6f:22:0c:47:7a:74 Received response at GoProUuid.QUERY_RSP_UUID: 80:32:6d:36:59:4d:76:4c:41:6f:2a:0e:31:39:32:2e:31:36:38:2e Received response at GoProUuid.QUERY_RSP_UUID: 81:35:30:2e:31:30:33:30:01:3a:0a:64:61:62:75:67:64:61:62:75 Received response at GoProUuid.QUERY_RSP_UUID: 82:67:42:0c:32:34:37:34:66:37:66:36:36:31:30:34 Received COHN Status: status: COHN_PROVISIONED state: COHN_STATE_NetworkConnected username: \"gopro\" password: \"Gzt2m6YMvLAo\" ipaddress: \"192.168.50.103\" enabled: true ssid: \"dabugdabug\" macaddress: \"2474f7f66104\" Successfully provisioned COHN. TODO Finally we accumulate all of the credentials and log them, also storing the certificate to a cohn.crt file: python kotlin credentials = await provision_cohn(manager) with open(certificate, \"w\") as fp: fp.write(credentials.certificate) logger.info(f\"Certificate written to {certificate.resolve()}\") { \"certificate\": \"-----BEGIN CERTIFICATE-----\\nMIIDnzCCAoegAwIBAgIUC7DGLtJJ61TzRY/mYQyhOegnz6cwDQYJKoZIhvcNAQ EL\\nBQAwaTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMRIwEAYDVQQHDAlTYW4gTWF0\\nZW8xDjAMBg NVBAoMBUdvUHJvMQ0wCwYDVQQLDARIZXJvMRowGAYDVQQDDBFHb1By\\nbyBDYW1lcmEgUm9vdDAeFw0y NDA0MDQyMDAwMTJaFw0zNDA0MDIyMDAwMTJaMGkx\\nCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJDQTESMB AGA1UEBwwJU2FuIE1hdGVvMQ4w\\nDAYDVQQKDAVHb1BybzENMAsGA1UECwwESGVybzEaMBgGA1UEAwwR R29Qcm8gQ2Ft\\nZXJhIFJvb3QwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC05o1QIN5r\\n PmtTntzpzBQvfq64OM1j/tjdNCJsyB9/ipPrPcKdItOy+5gZZF8iOFiw8cG8O2nA\\nvLSIJkpQ6d3cuE 48nAQpc1+jJzskM7Vgqc/i43OqnB8iTKjtNJgj+lJtreQBNJw7\\nf00a0GbbUJMo6DhaW58ZIsOJKu3i +w8w+LNEZECfDN6RMSmkYoLXaHeKAlvhlRYv\\nxkNO7pB2OwhbD9awgzKVTiKvZ8Hrxl6lGlH5SHHimU uo2O1yiNKDWv+MhirCVnup\\nVvP/N5S+230KpXreEnHmo65fsHmdM11qYu8WJXGzOViCnQi24wgCuoMx np9hAeKs\\nVj4vxhyCu8gZAgMBAAGjPzA9MA8GA1UdEwQIMAYBAf8CAQAwCwYDVR0PBAQDAgGG\\nMB0G A1UdDgQWBBTYDT4QXVDsi23ukLr2ohJk5+8+gDANBgkqhkiG9w0BAQsFAAOC\\nAQEAU4Z9120CGtRGo3 QfWEy66BGdqI6ohdudmb/3qag0viXag2FyWar18lRFiEWc\\nZcsqw6i0CM6lKNVUluEsSBiGGVAbAHKu +fcpId5NLEI7G1XY5MFRHMIMi4PNKbJr\\nVi0ks/biMy7u9++FOBgmCXGAdbMJBfe2gxEJNdyU6wjgGs 2o402/parrWN8x9J+k\\ndBgYqiKpZK0Fad/qM4ivbgkMijXhGFODhWs/GlQWnPeaLusRnn3T/w2CsFzM kf0i\\n6fFT3FAQBU5LCZs1Fp/XFRrnFMp+sNhbmdfnI9EDyZOXzlRS4O48k/AW/nSkCozk\\nugYW+61H /RYPVEgF4VNxRqn+uA==\\n-----END CERTIFICATE-----\\n\", \"username\": \"gopro\", \"password\": \"Gzt2m6YMvLAo\", \"ip_address\": \"192.168.50.103\" } Certificate written to C:\\Users\\user\\gopro\\OpenGoPro\\demos\\python\\tutorial\\tutorial_modules\\tutorial_9_cohn\\cohn.crt TODO Make sure to keep these credentials for use in the next section. Communicating via COHN Once the GoPro has provisioned for COHN, we can use the stored credentials for HTTPS communication. For the setup of this demo, there is no pre-existing BLE or WiFi connection to the GoPro. We are only going to be using HTTPS over the provisioned home network for communication. In order to demonstrate COHN communication we are going to Get the Camera State. python kotlin The code shown below is taken from communicate_via_cohn.py. The credentials logged and stored from the previous demo must be passed in as command line arguments to this script. Run python communicate_via_cohn.py --help for usage. We’re going to use the requests library to perform the HTTPS request. First let’s build the url using the ip_address CLI argument: url = f\"https://{ip_address}\" + \"/gopro/camera/state\" Then let’s build the basic auth token from the username and password CLI arguments: token = b64encode(f\"{username}:{password}\".encode(\"utf-8\")).decode(\"ascii\") Lastly we build and send the request using the above endpoint and token combined with the path to the certificate from the CLI certificate argument: response = requests.get( url, timeout=10, headers={\"Authorization\": f\"Basic {token}\"}, verify=str(certificate), ) logger.info(f\"Response: {json.dumps(response.json(), indent=4)}\") TODO This should result in logging the complete cameras state, truncated here for brevity: Sending: https://192.168.50.103/gopro/camera/state Command sent successfully Response: { \"status\": { \"1\": 1, \"2\": 4, \"3\": 0, \"4\": 255, \"6\": 0, \"8\": 0, \"9\": 0, ... \"settings\": { \"2\": 1, \"3\": 0, \"5\": 0, \"6\": 0, \"13\": 0, ... See the sending Wifi commands tutorial for more information on this and other HTTP(S) functionality. Quiz time! 📚 ✏️ Troubleshooting See the first tutorial’s troubleshooting section to troubleshoot any BLE problems. See the Sending Wifi Command tutorial’s troubleshooting section to troubleshoot HTTP communication. Good Job! Congratulations 🤙 You have now provisioned COHN and performed an HTTPS operation. In the future, you can now communicate with the GoPro over your home network without needing a direct BLE or WiFi connection.",
            "categories": [],
            "tags": [],
            "url": "/OpenGoPro/tutorials/cohn#"
        },]

let specStore = [
    {
        "title": "Keep Alive (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#keep-alive",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Analytics (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#set-analytics",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Ap Control (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#set-ap-control",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Camera Control (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#set-camera-control",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Date Time (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#set-date-time",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Local Date Time (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#set-local-date-time",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Shutter (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#set-shutter",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Turbo Transfer (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#set-turbo-transfer",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Sleep (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#sleep",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Scan For Access Points (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/access_points.html#scan-for-access-points",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Ap Scan Results (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/access_points.html#get-ap-scan-results",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Connect To Provisioned Access Point (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/access_points.html#connect-to-provisioned-access-point",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Connect To A New Access Point (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/access_points.html#connect-to-a-new-access-point",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Clear Cohn Certificate (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#clear-cohn-certificate",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Create Cohn Certificate (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#create-cohn-certificate",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Cohn Certificate (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#get-cohn-certificate",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Cohn Status (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#get-cohn-status",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Cohn Setting (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#set-cohn-setting",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Hilight Moment (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/hilights.html#hilight-moment",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Date Time (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#get-date-time",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Hardware Info (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#get-hardware-info",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Local Date Time (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#get-local-date-time",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Last Captured Media (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#get-last-captured-media",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Open Gopro Version (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#get-open-gopro-version",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Setting Values (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#get-setting-values",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Status Values (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#get-status-values",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Setting Capabilities (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#get-setting-capabilities",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Register For Setting Value Updates (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#register-for-setting-value-updates",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Register For Status Value Updates (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#register-for-status-value-updates",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Register For Setting Capability Updates (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#register-for-setting-capability-updates",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Unregister For Setting Value Updates (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#unregister-for-setting-value-updates",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Unregister For Status Value Updates (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#unregister-for-status-value-updates",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Unregister For Setting Capability Updates (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#unregister-for-setting-capability-updates",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Available Presets (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/presets.html#get-available-presets",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Load Preset (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/presets.html#load-preset",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Load Preset Group (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/presets.html#load-preset-group",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Update Custom Preset (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/presets.html#update-custom-preset",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Setting (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#set-setting",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Set Livestream Mode (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/live_streaming.html#set-livestream-mode",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "Get Livestream Status (BLE Operation)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/live_streaming.html#get-livestream-status",
        "tags": [
            "bleOperation"
        ]
    },
    {
        "title": "State Management (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/state_management.html#state-management",
        "tags": []
    },
    {
        "title": "Camera Readiness (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/state_management.html#camera-readiness",
        "tags": []
    },
    {
        "title": "Keep Alive (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/state_management.html#keep-alive",
        "tags": []
    },
    {
        "title": "Camera Control (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/state_management.html#camera-control",
        "tags": []
    },
    {
        "title": "Id Tables (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/id_tables.html#id-tables",
        "tags": []
    },
    {
        "title": "Command Ids (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/id_tables.html#command-ids",
        "tags": []
    },
    {
        "title": "Query Ids (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/id_tables.html#query-ids",
        "tags": []
    },
    {
        "title": "Protobuf Ids (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/id_tables.html#protobuf-ids",
        "tags": []
    },
    {
        "title": "Setting Ids (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/id_tables.html#setting-ids",
        "tags": []
    },
    {
        "title": "Status Ids (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/id_tables.html#status-ids",
        "tags": []
    },
    {
        "title": "Ble Setup (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/ble_setup.html#ble-setup",
        "tags": []
    },
    {
        "title": "Pairing Mode (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/ble_setup.html#pairing-mode",
        "tags": []
    },
    {
        "title": "Advertisements (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/ble_setup.html#advertisements",
        "tags": []
    },
    {
        "title": "Finish Pairing (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/ble_setup.html#finish-pairing",
        "tags": []
    },
    {
        "title": "Configure Gatt Characteristics (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/ble_setup.html#configure-gatt-characteristics",
        "tags": []
    },
    {
        "title": "Ble Characteristics (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/ble_setup.html#ble-characteristics",
        "tags": []
    },
    {
        "title": "Send Messages (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/ble_setup.html#send-messages",
        "tags": []
    },
    {
        "title": "Protobuf Documentation (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#protobuf-documentation",
        "tags": []
    },
    {
        "title": "Enums (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enums",
        "tags": []
    },
    {
        "title": "Enumcohnnetworkstate (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumcohnnetworkstate",
        "tags": []
    },
    {
        "title": "Enumcohnstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumcohnstatus",
        "tags": []
    },
    {
        "title": "Enumcameracontrolstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumcameracontrolstatus",
        "tags": []
    },
    {
        "title": "Enumflatmode (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumflatmode",
        "tags": []
    },
    {
        "title": "Enumlens (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumlens",
        "tags": []
    },
    {
        "title": "Enumlivestreamerror (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumlivestreamerror",
        "tags": []
    },
    {
        "title": "Enumlivestreamstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumlivestreamstatus",
        "tags": []
    },
    {
        "title": "Enumpresetgroup (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumpresetgroup",
        "tags": []
    },
    {
        "title": "Enumpresetgroupicon (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumpresetgroupicon",
        "tags": []
    },
    {
        "title": "Enumpreseticon (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumpreseticon",
        "tags": []
    },
    {
        "title": "Enumpresettitle (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumpresettitle",
        "tags": []
    },
    {
        "title": "Enumprovisioning (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumprovisioning",
        "tags": []
    },
    {
        "title": "Enumregisterlivestreamstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumregisterlivestreamstatus",
        "tags": []
    },
    {
        "title": "Enumregisterpresetstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumregisterpresetstatus",
        "tags": []
    },
    {
        "title": "Enumresultgeneric (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumresultgeneric",
        "tags": []
    },
    {
        "title": "Enumscanentryflags (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumscanentryflags",
        "tags": []
    },
    {
        "title": "Enumscanning (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumscanning",
        "tags": []
    },
    {
        "title": "Enumwindowsize (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#enumwindowsize",
        "tags": []
    },
    {
        "title": "Media (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#media",
        "tags": []
    },
    {
        "title": "Notifprovisioningstate (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#notifprovisioningstate",
        "tags": []
    },
    {
        "title": "Notifstartscanning (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#notifstartscanning",
        "tags": []
    },
    {
        "title": "Notifycohnstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#notifycohnstatus",
        "tags": []
    },
    {
        "title": "Notifylivestreamstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#notifylivestreamstatus",
        "tags": []
    },
    {
        "title": "Notifypresetstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#notifypresetstatus",
        "tags": []
    },
    {
        "title": "Preset (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#preset",
        "tags": []
    },
    {
        "title": "Presetgroup (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#presetgroup",
        "tags": []
    },
    {
        "title": "Presetsetting (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#presetsetting",
        "tags": []
    },
    {
        "title": "Requestcohncert (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestcohncert",
        "tags": []
    },
    {
        "title": "Requestclearcohncert (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestclearcohncert",
        "tags": []
    },
    {
        "title": "Requestconnect (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestconnect",
        "tags": []
    },
    {
        "title": "Requestconnectnew (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestconnectnew",
        "tags": []
    },
    {
        "title": "Requestcreatecohncert (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestcreatecohncert",
        "tags": []
    },
    {
        "title": "Requestcustompresetupdate (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestcustompresetupdate",
        "tags": []
    },
    {
        "title": "Requestgetapentries (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestgetapentries",
        "tags": []
    },
    {
        "title": "Requestgetcohnstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestgetcohnstatus",
        "tags": []
    },
    {
        "title": "Requestgetlastcapturedmedia (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestgetlastcapturedmedia",
        "tags": []
    },
    {
        "title": "Requestgetlivestreamstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestgetlivestreamstatus",
        "tags": []
    },
    {
        "title": "Requestgetpresetstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestgetpresetstatus",
        "tags": []
    },
    {
        "title": "Requestreleasenetwork (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestreleasenetwork",
        "tags": []
    },
    {
        "title": "Requestsetcohnsetting (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestsetcohnsetting",
        "tags": []
    },
    {
        "title": "Requestsetcameracontrolstatus (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestsetcameracontrolstatus",
        "tags": []
    },
    {
        "title": "Requestsetlivestreammode (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestsetlivestreammode",
        "tags": []
    },
    {
        "title": "Requestsetturboactive (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requestsetturboactive",
        "tags": []
    },
    {
        "title": "Requeststartscan (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#requeststartscan",
        "tags": []
    },
    {
        "title": "Responsecohncert (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#responsecohncert",
        "tags": []
    },
    {
        "title": "Responseconnect (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#responseconnect",
        "tags": []
    },
    {
        "title": "Responseconnectnew (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#responseconnectnew",
        "tags": []
    },
    {
        "title": "Responsegeneric (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#responsegeneric",
        "tags": []
    },
    {
        "title": "Responsegetapentries (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#responsegetapentries",
        "tags": []
    },
    {
        "title": "Responselastcapturedmedia (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#responselastcapturedmedia",
        "tags": []
    },
    {
        "title": "Responsestartscanning (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#responsestartscanning",
        "tags": []
    },
    {
        "title": "Responsegetapentries::Scanentry (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/protobuf.html#responsegetapentries::scanentry",
        "tags": []
    },
    {
        "title": "Data Protocol (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#data-protocol",
        "tags": []
    },
    {
        "title": "Packetization (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#packetization",
        "tags": []
    },
    {
        "title": "Packet Headers (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#packet-headers",
        "tags": []
    },
    {
        "title": "General 5 Bit Packets (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#general-5-bit-packets",
        "tags": []
    },
    {
        "title": "Extended 13 Bit Packets (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#extended-13-bit-packets",
        "tags": []
    },
    {
        "title": "Extended 16 Bit Packets (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#extended-16-bit-packets",
        "tags": []
    },
    {
        "title": "Continuation Packets (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#continuation-packets",
        "tags": []
    },
    {
        "title": "Decipher Message Payload Type (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#decipher-message-payload-type",
        "tags": []
    },
    {
        "title": "Message Payload (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#message-payload",
        "tags": []
    },
    {
        "title": "Type Length Value (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#type-length-value",
        "tags": []
    },
    {
        "title": "Commands (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#commands",
        "tags": []
    },
    {
        "title": "Queries (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#queries",
        "tags": []
    },
    {
        "title": "Protobuf (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#protobuf",
        "tags": []
    },
    {
        "title": "Backwards Compatibility (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/protocol/data_protocol.html#backwards-compatibility",
        "tags": []
    },
    {
        "title": "Control (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#control",
        "tags": []
    },
    {
        "title": "Operations (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/control.html#operations",
        "tags": []
    },
    {
        "title": "Access Point (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/access_points.html#access-point",
        "tags": []
    },
    {
        "title": "Operations (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/access_points.html#operations",
        "tags": []
    },
    {
        "title": "Disconnect From Access Point (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/access_points.html#disconnect-from-access-point",
        "tags": []
    },
    {
        "title": "Camera On The Home Network (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#camera-on-the-home-network",
        "tags": []
    },
    {
        "title": "Certificates (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#certificates",
        "tags": []
    },
    {
        "title": "Verifying Certificate (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#verifying-certificate",
        "tags": []
    },
    {
        "title": "View Certificate Details (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#view-certificate-details",
        "tags": []
    },
    {
        "title": "Provisioning Procedure (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#provisioning-procedure",
        "tags": []
    },
    {
        "title": "Operations (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/cohn.html#operations",
        "tags": []
    },
    {
        "title": "Hilights (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/hilights.html#hilights",
        "tags": []
    },
    {
        "title": "Operations (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/hilights.html#operations",
        "tags": []
    },
    {
        "title": "Query (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#query",
        "tags": []
    },
    {
        "title": "Operations (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/query.html#operations",
        "tags": []
    },
    {
        "title": "Presets (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/presets.html#presets",
        "tags": []
    },
    {
        "title": "Preset Groups (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/presets.html#preset-groups",
        "tags": []
    },
    {
        "title": "Preset Modified Status (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/presets.html#preset-modified-status",
        "tags": []
    },
    {
        "title": "Operations (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/presets.html#operations",
        "tags": []
    },
    {
        "title": "Statuses (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#statuses",
        "tags": []
    },
    {
        "title": "Status Ids (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#status-ids",
        "tags": []
    },
    {
        "title": "Battery Present 1 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#battery-present-1",
        "tags": []
    },
    {
        "title": "Internal Battery Bars 2 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#internal-battery-bars-2",
        "tags": []
    },
    {
        "title": "Overheating 6 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#overheating-6",
        "tags": []
    },
    {
        "title": "Busy 8 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#busy-8",
        "tags": []
    },
    {
        "title": "Quick Capture 9 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#quick-capture-9",
        "tags": []
    },
    {
        "title": "Encoding 10 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#encoding-10",
        "tags": []
    },
    {
        "title": "Lcd Lock 11 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#lcd-lock-11",
        "tags": []
    },
    {
        "title": "Video Encoding Duration 13 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#video-encoding-duration-13",
        "tags": []
    },
    {
        "title": "Wireless Connections Enabled 17 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wireless-connections-enabled-17",
        "tags": []
    },
    {
        "title": "Pairing State 19 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pairing-state-19",
        "tags": []
    },
    {
        "title": "Last Pairing Type 20 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-pairing-type-20",
        "tags": []
    },
    {
        "title": "Last Pairing Success 21 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-pairing-success-21",
        "tags": []
    },
    {
        "title": "Wifi Scan State 22 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-scan-state-22",
        "tags": []
    },
    {
        "title": "Last Wifi Scan Success 23 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#last-wifi-scan-success-23",
        "tags": []
    },
    {
        "title": "Wifi Provisioning State 24 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-provisioning-state-24",
        "tags": []
    },
    {
        "title": "Remote Version 26 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remote-version-26",
        "tags": []
    },
    {
        "title": "Remote Connected 27 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remote-connected-27",
        "tags": []
    },
    {
        "title": "Pairing State Legacy 28 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pairing-state-legacy-28",
        "tags": []
    },
    {
        "title": "Ap Ssid 29 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ap-ssid-29",
        "tags": []
    },
    {
        "title": "Wifi Ssid 30 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-ssid-30",
        "tags": []
    },
    {
        "title": "Connected Devices 31 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#connected-devices-31",
        "tags": []
    },
    {
        "title": "Preview Stream 32 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preview-stream-32",
        "tags": []
    },
    {
        "title": "Primary Storage 33 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#primary-storage-33",
        "tags": []
    },
    {
        "title": "Remaining Photos 34 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-photos-34",
        "tags": []
    },
    {
        "title": "Remaining Video Time 35 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-video-time-35",
        "tags": []
    },
    {
        "title": "Photos 38 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photos-38",
        "tags": []
    },
    {
        "title": "Videos 39 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#videos-39",
        "tags": []
    },
    {
        "title": "Ota 41 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ota-41",
        "tags": []
    },
    {
        "title": "Pending Fw Update Cancel 42 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#pending-fw-update-cancel-42",
        "tags": []
    },
    {
        "title": "Locate 45 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#locate-45",
        "tags": []
    },
    {
        "title": "Timelapse Interval Countdown 49 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#timelapse-interval-countdown-49",
        "tags": []
    },
    {
        "title": "Sd Card Remaining 54 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-remaining-54",
        "tags": []
    },
    {
        "title": "Preview Stream Available 55 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preview-stream-available-55",
        "tags": []
    },
    {
        "title": "Wifi Bars 56 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wifi-bars-56",
        "tags": []
    },
    {
        "title": "Active Hilights 58 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#active-hilights-58",
        "tags": []
    },
    {
        "title": "Time Since Last Hilight 59 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#time-since-last-hilight-59",
        "tags": []
    },
    {
        "title": "Minimum Status Poll Period 60 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#minimum-status-poll-period-60",
        "tags": []
    },
    {
        "title": "Liveview Exposure Select Mode 65 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-exposure-select-mode-65",
        "tags": []
    },
    {
        "title": "Liveview Y 66 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-y-66",
        "tags": []
    },
    {
        "title": "Liveview X 67 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#liveview-x-67",
        "tags": []
    },
    {
        "title": "Gps Lock 68 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#gps-lock-68",
        "tags": []
    },
    {
        "title": "Ap Mode 69 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ap-mode-69",
        "tags": []
    },
    {
        "title": "Internal Battery Percentage 70 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#internal-battery-percentage-70",
        "tags": []
    },
    {
        "title": "Microphone Accessory 74 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#microphone-accessory-74",
        "tags": []
    },
    {
        "title": "Zoom Level 75 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-level-75",
        "tags": []
    },
    {
        "title": "Wireless Band 76 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#wireless-band-76",
        "tags": []
    },
    {
        "title": "Zoom Available 77 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-available-77",
        "tags": []
    },
    {
        "title": "Mobile Friendly 78 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#mobile-friendly-78",
        "tags": []
    },
    {
        "title": "Ftu 79 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ftu-79",
        "tags": []
    },
    {
        "title": "5Ghz Available 81 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#5ghz-available-81",
        "tags": []
    },
    {
        "title": "Ready 82 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ready-82",
        "tags": []
    },
    {
        "title": "Ota Charged 83 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#ota-charged-83",
        "tags": []
    },
    {
        "title": "Cold 85 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#cold-85",
        "tags": []
    },
    {
        "title": "Rotation 86 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#rotation-86",
        "tags": []
    },
    {
        "title": "Zoom While Encoding 88 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#zoom-while-encoding-88",
        "tags": []
    },
    {
        "title": "Flatmode 89 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#flatmode-89",
        "tags": []
    },
    {
        "title": "Video Preset 93 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#video-preset-93",
        "tags": []
    },
    {
        "title": "Photo Preset 94 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photo-preset-94",
        "tags": []
    },
    {
        "title": "Timelapse Preset 95 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#timelapse-preset-95",
        "tags": []
    },
    {
        "title": "Preset Group 96 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-group-96",
        "tags": []
    },
    {
        "title": "Preset 97 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-97",
        "tags": []
    },
    {
        "title": "Preset Modified 98 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#preset-modified-98",
        "tags": []
    },
    {
        "title": "Remaining Live Bursts 99 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#remaining-live-bursts-99",
        "tags": []
    },
    {
        "title": "Live Bursts 100 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#live-bursts-100",
        "tags": []
    },
    {
        "title": "Capture Delay Active 101 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#capture-delay-active-101",
        "tags": []
    },
    {
        "title": "Media Mod State 102 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#media-mod-state-102",
        "tags": []
    },
    {
        "title": "Time Warp Speed 103 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#time-warp-speed-103",
        "tags": []
    },
    {
        "title": "Linux Core 104 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#linux-core-104",
        "tags": []
    },
    {
        "title": "Lens Type 105 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#lens-type-105",
        "tags": []
    },
    {
        "title": "Hindsight 106 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#hindsight-106",
        "tags": []
    },
    {
        "title": "Scheduled Capture Preset Id 107 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#scheduled-capture-preset-id-107",
        "tags": []
    },
    {
        "title": "Scheduled Capture 108 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#scheduled-capture-108",
        "tags": []
    },
    {
        "title": "Display Mod Status 110 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#display-mod-status-110",
        "tags": []
    },
    {
        "title": "Sd Card Write Speed Error 111 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-write-speed-error-111",
        "tags": []
    },
    {
        "title": "Sd Card Errors 112 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-errors-112",
        "tags": []
    },
    {
        "title": "Turbo Transfer 113 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#turbo-transfer-113",
        "tags": []
    },
    {
        "title": "Camera Control Id 114 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#camera-control-id-114",
        "tags": []
    },
    {
        "title": "Usb Connected 115 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#usb-connected-115",
        "tags": []
    },
    {
        "title": "Usb Controlled 116 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#usb-controlled-116",
        "tags": []
    },
    {
        "title": "Sd Card Capacity 117 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#sd-card-capacity-117",
        "tags": []
    },
    {
        "title": "Photo Interval Capture Count 118 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/statuses.html#photo-interval-capture-count-118",
        "tags": []
    },
    {
        "title": "Settings (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#settings",
        "tags": []
    },
    {
        "title": "Operations (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#operations",
        "tags": []
    },
    {
        "title": "Setting Ids (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#setting-ids",
        "tags": []
    },
    {
        "title": "Video Resolution 2 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-resolution-2",
        "tags": []
    },
    {
        "title": "Frames Per Second 3 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#frames-per-second-3",
        "tags": []
    },
    {
        "title": "Video Timelapse Rate 5 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-timelapse-rate-5",
        "tags": []
    },
    {
        "title": "Photo Timelapse Rate 30 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-timelapse-rate-30",
        "tags": []
    },
    {
        "title": "Nightlapse Rate 32 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#nightlapse-rate-32",
        "tags": []
    },
    {
        "title": "Webcam Digital Lenses 43 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#webcam-digital-lenses-43",
        "tags": []
    },
    {
        "title": "Auto Power Down 59 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#auto-power-down-59",
        "tags": []
    },
    {
        "title": "Gps 83 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#gps-83",
        "tags": []
    },
    {
        "title": "Video Aspect Ratio 108 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-aspect-ratio-108",
        "tags": []
    },
    {
        "title": "Video Lens 121 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-lens-121",
        "tags": []
    },
    {
        "title": "Photo Lens 122 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-lens-122",
        "tags": []
    },
    {
        "title": "Time Lapse Digital Lenses 123 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#time-lapse-digital-lenses-123",
        "tags": []
    },
    {
        "title": "Photo Output 125 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-output-125",
        "tags": []
    },
    {
        "title": "Media Format 128 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#media-format-128",
        "tags": []
    },
    {
        "title": "Anti Flicker 134 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#anti-flicker-134",
        "tags": []
    },
    {
        "title": "Hypersmooth 135 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#hypersmooth-135",
        "tags": []
    },
    {
        "title": "Video Horizon Leveling 150 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-horizon-leveling-150",
        "tags": []
    },
    {
        "title": "Photo Horizon Leveling 151 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-horizon-leveling-151",
        "tags": []
    },
    {
        "title": "Max Lens 162 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-162",
        "tags": []
    },
    {
        "title": "Hindsight 167 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#hindsight-167",
        "tags": []
    },
    {
        "title": "Photo Single Interval 171 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-single-interval-171",
        "tags": []
    },
    {
        "title": "Photo Interval Duration 172 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-interval-duration-172",
        "tags": []
    },
    {
        "title": "Video Performance Mode 173 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-performance-mode-173",
        "tags": []
    },
    {
        "title": "Controls 175 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#controls-175",
        "tags": []
    },
    {
        "title": "Easy Mode Speed 176 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-mode-speed-176",
        "tags": []
    },
    {
        "title": "Enable Night Photo 177 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#enable-night-photo-177",
        "tags": []
    },
    {
        "title": "Wireless Band 178 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#wireless-band-178",
        "tags": []
    },
    {
        "title": "Star Trails Length 179 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#star-trails-length-179",
        "tags": []
    },
    {
        "title": "System Video Mode 180 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#system-video-mode-180",
        "tags": []
    },
    {
        "title": "Video Bit Rate 182 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-bit-rate-182",
        "tags": []
    },
    {
        "title": "Bit Depth 183 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#bit-depth-183",
        "tags": []
    },
    {
        "title": "Profiles 184 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#profiles-184",
        "tags": []
    },
    {
        "title": "Video Easy Mode 186 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-easy-mode-186",
        "tags": []
    },
    {
        "title": "Lapse Mode 187 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#lapse-mode-187",
        "tags": []
    },
    {
        "title": "Max Lens Mod 189 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-189",
        "tags": []
    },
    {
        "title": "Max Lens Mod Enable 190 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-enable-190",
        "tags": []
    },
    {
        "title": "Easy Night Photo 191 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-night-photo-191",
        "tags": []
    },
    {
        "title": "Multi Shot Aspect Ratio 192 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-aspect-ratio-192",
        "tags": []
    },
    {
        "title": "Framing 193 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#framing-193",
        "tags": []
    },
    {
        "title": "Camera Volume 216 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#camera-volume-216",
        "tags": []
    },
    {
        "title": "Setup Screen Saver 219 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-screen-saver-219",
        "tags": []
    },
    {
        "title": "Setup Language 223 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-language-223",
        "tags": []
    },
    {
        "title": "Photo Mode 227 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-mode-227",
        "tags": []
    },
    {
        "title": "Video Framing 232 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-framing-232",
        "tags": []
    },
    {
        "title": "Multi Shot Framing 233 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-framing-233",
        "tags": []
    },
    {
        "title": "Frame Rate 234 (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/settings.html#frame-rate-234",
        "tags": []
    },
    {
        "title": "Live Streaming (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/live_streaming.html#live-streaming",
        "tags": []
    },
    {
        "title": "Operations (BLE Spec)",
        "excerpt": "",
        "url": "https://gopro.github.io/OpenGoPro/ble/features/live_streaming.html#operations",
        "tags": []
    },
    {
        "title": "Control (HTTP Section)",
        "excerpt": "Command and control of the camera",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Control",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Query (HTTP Section)",
        "excerpt": "Get information about the camera",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Query",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Media (HTTP Section)",
        "excerpt": "This section describes the operations to query basic details about media captured on the sdcard.\n\n## Chapters\n\nAll GoPro cameras break longer videos into chapters.\nGoPro cameras currently limit file sizes on sdcards to 4GB for both FAT32 and exFAT file systems.\nThis limitation is most commonly seen when recording longer (10+ minute) videos.\nIn practice, the camera will split video media into chapters named Gqccmmmm.MP4 (and ones for THM/LRV) such that:\n\n-   q: Quality Level (X: Extreme, H: High, M: Medium, L: Low)\n-   cc: Chapter Number (01-99)\n-   mmmm: Media ID (0001-9999)\n\nWhen media becomes chaptered, the camera increments subsequent Chapter Numbers while leaving the Media ID unchanged.\nFor example, if the user records a long High-quality video that results in 4 chapters, the files on the sdcard may\nlook like the following:\n\n```\n-rwxrwxrwx@ 1 gopro  123456789  4006413091 Jan  1 00:00 GH010078.MP4\n-rwxrwxrwx@ 1 gopro  123456789       17663 Jan  1 00:00 GH010078.THM\n-rwxrwxrwx@ 1 gopro  123456789  4006001541 Jan  1 00:00 GH020078.MP4\n-rwxrwxrwx@ 1 gopro  123456789       17357 Jan  1 00:00 GH020078.THM\n-rwxrwxrwx@ 1 gopro  123456789  4006041985 Jan  1 00:00 GH030078.MP4\n-rwxrwxrwx@ 1 gopro  123456789       17204 Jan  1 00:00 GH030078.THM\n-rwxrwxrwx@ 1 gopro  123456789   756706872 Jan  1 00:00 GH040078.MP4\n-rwxrwxrwx@ 1 gopro  123456789       17420 Jan  1 00:00 GH040078.THM\n-rwxrwxrwx@ 1 gopro  123456789   184526939 Jan  1 00:00 GL010078.LRV\n-rwxrwxrwx@ 1 gopro  123456789   184519787 Jan  1 00:00 GL020078.LRV\n-rwxrwxrwx@ 1 gopro  123456789   184517614 Jan  1 00:00 GL030078.LRV\n-rwxrwxrwx@ 1 gopro  123456789    34877660 Jan  1 00:00 GL040078.LRV\n```",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Media",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Webcam (HTTP Section)",
        "excerpt": "The webcam feature enables developers who are interested in writing custom drivers to broadcast the camera's video\npreview with a limited set of resolution, field of view, port, and protocol options.\n\nWhile active, the webcam feature sends raw data to the connected client using a supported protocol. To enable\nmulti-cam support, some cameras support running on a user-specified port. Protocol and port details are provided in a\ntable below.\n\nTo test basic functionality, start the webcam, and use an application such as VLC to open a network stream:\n\n| Protocol | Port                        |\n| -------- | --------------------------- |\n| TS       | udp://@:{PORT}              |\n| RTSP     | rtsp://{CAMERA_IP}:554/live |\n\nFor readers interested in using a GoPro camera as a webcam with preexisting tools, please see\n[How to use GoPro as a Webcam](https://community.gopro.com/s/article/GoPro-Webcam?language=en_US).\n\n### Webcam via USB\n\nFor USB connections, prior to issuing webcam commands, [Wired USB Control](#operation/OGP_SET_WIRED_USB_CONTROL) should\nbe disabled.\n\n### Webcam State Diagram\n\n![webcam state diagram](assets/images/webcam.png)\n\n### Webcam Stabilization\n\nShould the client require stabilization, the\n[Hypersmooth setting](#operation/GPCAMERA_CHANGE_SETTING::135)\ncan be used while in the state: `READY (Status: OFF)`. This setting can only be set while webcam is disabled, which\nrequires either sending the [Webcam Exit](#operation/OGP_WEBCAM_EXIT) command or reseating the USB-C connection to the camera.\n\n> Note! The Low Hypersmooth option provides lower/lighter stabilization when used in Webcam mode vs other camera modes.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Webcam",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Preview Stream (HTTP Section)",
        "excerpt": "When the preview stream is started, the camera starts up a UDP client and begins writing MPEG Transport\nStream data to the client on port 8554. In order to stream this data, the client must implement a UDP\nconnection that binds to the same port and decode the data.",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Preview Stream",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Ota (HTTP Section)",
        "excerpt": "The Over The Air (OTA) update feature allows the user to update the camera's firmware via HTTP connection. There are\ntwo ways to perform OTA updates: Simple OTA Update and Resumable OTA Update.\n\nFirmware update files can be obtained from GoPro's [update page](https://gopro.com/en/us/update) or programmatically\nusing the [firmware catalog](https://api.gopro.com/firmware/v2/catalog).\n\n> In order to complete the firmware update process, the camera will reboot one or more times. This will cause any\n> existing HTTP connections to be lost.\n\n## Simple OTA Update\n\nThe simple OTA update process is done by sending an entire update file to the camera in a single HTTP/POST. Details can\nbe found in the diagram below.\n\n![simple ota state diagram](assets/images/simple_ota.png)\n\n## Resumable OTA Update\n\nThe resumable OTA update process involves uploading chunks (or all) of a file, marking the file complete and then telling\nthe camera to begin the update process. Chunks are stored until they are explicitly deleted, allowing the client to stop\nand resume as needed. Details can be found in the diagram below.\n\n![simple ota state diagram](assets/images/resumeable_ota.png)\n",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/OTA",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Cohn (HTTP Section)",
        "excerpt": "The Camera On the Home Network (COHN) capability allows the client to perform command and control with the camera\nindirectly through an access point such as a router at home.\n\nFor security purposes, all communications are performed over HTTPS.\n\n## Provisioning COHN\n\nIn order to use the COHN capability, the camera must first be provisioned for COHN.\nFor instructions on how to do this, see the [Open GoPro BLE spec](ble/features/cohn.html).\n\n## Send Messages via HTTPS\n\nOnce the camera is provisioned, the client can issue commands and set settings\nvia HTTPS using the COHN certificate and Basic authorization (username/password) credentials obtained during\nprovisioning or subsequently by querying for COHN status.\n\n## HTTPS Headers\n\nAll HTTPS messages must contain [Basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)\nheaders, using the username and password from the COHN status obtained during or after provisioning.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/COHN",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Analytics (HTTP Section)",
        "excerpt": "Query / Configure Analytics",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Analytics",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Presets (HTTP Section)",
        "excerpt": "## Presets\n\nThe camera organizes modes of operation into [Presets](#schema/Preset).\n\nDepending on the camera's state, different collections of presets will be available for immediate loading and use.\n\nTo find the currently available Presets, use [Get Preset Status](#operation/OGP_PRESETS_GET).\n\n## Preset Groups\n\nPresets are organized into [Preset Groups](#schema/PresetGroup).\n\nTo find the currently available Preset Groups, use [Get Preset Status](#operation/OGP_PRESETS_GET).\n",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Presets",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Settings (HTTP Section)",
        "excerpt": "GoPro cameras have hundreds of setting options to choose from. Since these options have a complex tree of dependencies\non camera state, current Preset, etc, there is no mechanism to set a desired setting option from any camera state.\n\nTo find the currently available options for a given setting, attempt to set it to an invalid option using its relevant\noperation below and view the [currently available options](#schema/SettingCapabilities) returned in the 403 error response.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/settings",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Hilights (HTTP Section)",
        "excerpt": "The [HiLight Tags](https://community.gopro.com/t5/en/What-Is-HiLight-Tagging-amp-How-Does-It-Work/ta-p/390286)\nfeature allows the user to tag moments of interest either during video capture or on existing media.\n\nOnce HiLight tags have been added, they can be queried via [Media Info](#operation/OGP_MEDIA_INFO)\n",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Hilights",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Models (HTTP Section)",
        "excerpt": "Common data models used across operations",
        "url": "https://gopro.github.io/OpenGoPro/http#tag/Models",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Groupedmedialistitem (HTTP Schema)",
        "excerpt": "A grouped (i.e. burst, lapse, etc.) media item\n\nNote that each property actually comes as a string but is specified here using its functional value.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/GroupedMediaListItem",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Medialist (HTTP Schema)",
        "excerpt": "list of media file systems",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/MediaList",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Otastatus (HTTP Schema)",
        "excerpt": "OTA Status\n\n| ID | Status | Description |\n| -- | ------ | ----------- |\n| 0 | OK | No errors occurred |\n| 1 | Unknown Request | Server did not recognize the request |\n| 2 | Bad Params | Parameter values not recognized |\n| 3 | SHA1 Send Mismatch | SHA1 for chunk did not match SHA1 of previous chunk(s) |\n| 4 | SHA1 Calculated Mismatch | Calculated SHA1 did not match user-specified SHA1 |\n| 5 | HTTP Boundary Error | HTTP Post was malformed |\n| 6 | HTTP Post Error | Unexpected HTTP / Post Content Type |\n| 7 | Server Busy | HTTP server is busy |\n| 8 | Offset Mismatch | Attempt to upload chunk with offset that did not align with previous chunk |\n| 9 | Bad Post Data | Server failed to parse POST data |\n| 10 | File Incomplete | Tried to start update before server finished validating .zip file |\n| 11 | Update in progress | Firmware update is in progress |\n| 12 | Insufficient Space | Insufficient space on the sdcard to hold decompressed update file |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/OtaStatus",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Photometadata (HTTP Schema)",
        "excerpt": "Metadata for a photo media file\n\nNote that each property actually comes as a string but is specified here using its functional value.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/PhotoMetadata",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Preset (HTTP Schema)",
        "excerpt": "A logical wrapper around a specific camera mode, title, icon, and a set of settings that enhance different\n styles of capturing media.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/Preset",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Presetgroup (HTTP Schema)",
        "excerpt": "A collection of Presets",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/PresetGroup",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Presetsetting (HTTP Schema)",
        "excerpt": "An individual preset setting that forms the preset's setting array",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/PresetSetting",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Settingcapabilities (HTTP Schema)",
        "excerpt": "The currently available options for the requested setting.",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/SettingCapabilities",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Singlemedialistitem (HTTP Schema)",
        "excerpt": "A single (non-grouped) media item\n\nNote that each property actually comes as a string but is specified here using its functional value.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/SingleMediaListItem",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "State (HTTP Schema)",
        "excerpt": "All settings and statuses",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/State",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Videometadata (HTTP Schema)",
        "excerpt": "Metadata for a video media file\n\nNote that each property actually comes as a string but is specified here using its functional value.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/VideoMetadata",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enumcameracontrolstatus (HTTP Schema)",
        "excerpt": "\n\n| ID | Name | Summary |\n| -- | ---- | ------- |\n| 0 | CAMERA_IDLE |  |\n| 1 | CAMERA_CONTROL | Can only be set by camera, not by app or third party |\n| 2 | CAMERA_EXTERNAL_CONTROL |  |\n| 3 | CAMERA_COF_SETUP | Set by the camera when it is on the CAH (Camera As a Hub) / COF (Cloud Offload) setup screen |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/EnumCameraControlStatus",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enumpresetgroupicon (HTTP Schema)",
        "excerpt": "\n\n| ID | Name | Summary |\n| -- | ---- | ------- |\n| 0 | PRESET_GROUP_VIDEO_ICON_ID |  |\n| 1 | PRESET_GROUP_PHOTO_ICON_ID |  |\n| 2 | PRESET_GROUP_TIMELAPSE_ICON_ID |  |\n| 3 | PRESET_GROUP_LONG_BAT_VIDEO_ICON_ID |  |\n| 4 | PRESET_GROUP_ENDURANCE_VIDEO_ICON_ID |  |\n| 5 | PRESET_GROUP_MAX_VIDEO_ICON_ID |  |\n| 6 | PRESET_GROUP_MAX_PHOTO_ICON_ID |  |\n| 7 | PRESET_GROUP_MAX_TIMELAPSE_ICON_ID |  |\n| 8 | PRESET_GROUP_ND_MOD_VIDEO_ICON_ID |  |\n| 9 | PRESET_GROUP_ND_MOD_PHOTO_ICON_ID |  |\n| 10 | PRESET_GROUP_ND_MOD_TIMELAPSE_ICON_ID |  |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/EnumPresetGroupIcon",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enumpresetgroup (HTTP Schema)",
        "excerpt": "\n\n| ID | Name | Summary |\n| -- | ---- | ------- |\n| 1000 | PRESET_GROUP_ID_VIDEO |  |\n| 1001 | PRESET_GROUP_ID_PHOTO |  |\n| 1002 | PRESET_GROUP_ID_TIMELAPSE |  |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/EnumPresetGroup",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enumflatmode (HTTP Schema)",
        "excerpt": "\n\n| ID | Name | Summary |\n| -- | ---- | ------- |\n| -1 | FLAT_MODE_UNKNOWN |  |\n| 4 | FLAT_MODE_PLAYBACK |  |\n| 5 | FLAT_MODE_SETUP |  |\n| 12 | FLAT_MODE_VIDEO |  |\n| 13 | FLAT_MODE_TIME_LAPSE_VIDEO |  |\n| 15 | FLAT_MODE_LOOPING |  |\n| 16 | FLAT_MODE_PHOTO_SINGLE |  |\n| 17 | FLAT_MODE_PHOTO |  |\n| 18 | FLAT_MODE_PHOTO_NIGHT |  |\n| 19 | FLAT_MODE_PHOTO_BURST |  |\n| 20 | FLAT_MODE_TIME_LAPSE_PHOTO |  |\n| 21 | FLAT_MODE_NIGHT_LAPSE_PHOTO |  |\n| 22 | FLAT_MODE_BROADCAST_RECORD |  |\n| 23 | FLAT_MODE_BROADCAST_BROADCAST |  |\n| 24 | FLAT_MODE_TIME_WARP_VIDEO |  |\n| 25 | FLAT_MODE_LIVE_BURST |  |\n| 26 | FLAT_MODE_NIGHT_LAPSE_VIDEO |  |\n| 27 | FLAT_MODE_SLOMO |  |\n| 28 | FLAT_MODE_IDLE |  |\n| 29 | FLAT_MODE_VIDEO_STAR_TRAIL |  |\n| 30 | FLAT_MODE_VIDEO_LIGHT_PAINTING |  |\n| 31 | FLAT_MODE_VIDEO_LIGHT_TRAIL |  |\n| 32 | FLAT_MODE_VIDEO_BURST_SLOMO |  |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/EnumFlatMode",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enumpreseticon (HTTP Schema)",
        "excerpt": "\n\n| ID | Name | Summary |\n| -- | ---- | ------- |\n| 0 | PRESET_ICON_VIDEO |  |\n| 1 | PRESET_ICON_ACTIVITY |  |\n| 2 | PRESET_ICON_CINEMATIC |  |\n| 3 | PRESET_ICON_PHOTO |  |\n| 4 | PRESET_ICON_LIVE_BURST |  |\n| 5 | PRESET_ICON_BURST |  |\n| 6 | PRESET_ICON_PHOTO_NIGHT |  |\n| 7 | PRESET_ICON_TIMEWARP |  |\n| 8 | PRESET_ICON_TIMELAPSE |  |\n| 9 | PRESET_ICON_NIGHTLAPSE |  |\n| 10 | PRESET_ICON_SNAIL |  |\n| 11 | PRESET_ICON_VIDEO_2 |  |\n| 13 | PRESET_ICON_PHOTO_2 |  |\n| 14 | PRESET_ICON_PANORAMA |  |\n| 15 | PRESET_ICON_BURST_2 |  |\n| 16 | PRESET_ICON_TIMEWARP_2 |  |\n| 17 | PRESET_ICON_TIMELAPSE_2 |  |\n| 18 | PRESET_ICON_CUSTOM |  |\n| 19 | PRESET_ICON_AIR |  |\n| 20 | PRESET_ICON_BIKE |  |\n| 21 | PRESET_ICON_EPIC |  |\n| 22 | PRESET_ICON_INDOOR |  |\n| 23 | PRESET_ICON_MOTOR |  |\n| 24 | PRESET_ICON_MOUNTED |  |\n| 25 | PRESET_ICON_OUTDOOR |  |\n| 26 | PRESET_ICON_POV |  |\n| 27 | PRESET_ICON_SELFIE |  |\n| 28 | PRESET_ICON_SKATE |  |\n| 29 | PRESET_ICON_SNOW |  |\n| 30 | PRESET_ICON_TRAIL |  |\n| 31 | PRESET_ICON_TRAVEL |  |\n| 32 | PRESET_ICON_WATER |  |\n| 33 | PRESET_ICON_LOOPING |  |\n| 34 | PRESET_ICON_STARS |  |\n| 35 | PRESET_ICON_ACTION |  |\n| 36 | PRESET_ICON_FOLLOW_CAM |  |\n| 37 | PRESET_ICON_SURF |  |\n| 38 | PRESET_ICON_CITY |  |\n| 39 | PRESET_ICON_SHAKY |  |\n| 40 | PRESET_ICON_CHESTY |  |\n| 41 | PRESET_ICON_HELMET |  |\n| 42 | PRESET_ICON_BITE |  |\n| 43 | PRESET_ICON_CUSTOM_CINEMATIC |  |\n| 44 | PRESET_ICON_VLOG |  |\n| 45 | PRESET_ICON_FPV |  |\n| 46 | PRESET_ICON_HDR |  |\n| 47 | PRESET_ICON_LANDSCAPE |  |\n| 48 | PRESET_ICON_LOG |  |\n| 49 | PRESET_ICON_CUSTOM_SLOMO |  |\n| 50 | PRESET_ICON_TRIPOD |  |\n| 55 | PRESET_ICON_MAX_VIDEO |  |\n| 56 | PRESET_ICON_MAX_PHOTO |  |\n| 57 | PRESET_ICON_MAX_TIMEWARP |  |\n| 58 | PRESET_ICON_BASIC |  |\n| 59 | PRESET_ICON_ULTRA_SLO_MO |  |\n| 60 | PRESET_ICON_STANDARD_ENDURANCE |  |\n| 61 | PRESET_ICON_ACTIVITY_ENDURANCE |  |\n| 62 | PRESET_ICON_CINEMATIC_ENDURANCE |  |\n| 63 | PRESET_ICON_SLOMO_ENDURANCE |  |\n| 64 | PRESET_ICON_STATIONARY_1 |  |\n| 65 | PRESET_ICON_STATIONARY_2 |  |\n| 66 | PRESET_ICON_STATIONARY_3 |  |\n| 67 | PRESET_ICON_STATIONARY_4 |  |\n| 70 | PRESET_ICON_SIMPLE_SUPER_PHOTO |  |\n| 71 | PRESET_ICON_SIMPLE_NIGHT_PHOTO |  |\n| 73 | PRESET_ICON_HIGHEST_QUALITY_VIDEO |  |\n| 74 | PRESET_ICON_STANDARD_QUALITY_VIDEO |  |\n| 75 | PRESET_ICON_BASIC_QUALITY_VIDEO |  |\n| 76 | PRESET_ICON_STAR_TRAIL |  |\n| 77 | PRESET_ICON_LIGHT_PAINTING |  |\n| 78 | PRESET_ICON_LIGHT_TRAIL |  |\n| 79 | PRESET_ICON_FULL_FRAME |  |\n| 80 | PRESET_ICON_EASY_MAX_VIDEO |  |\n| 81 | PRESET_ICON_EASY_MAX_PHOTO |  |\n| 82 | PRESET_ICON_EASY_MAX_TIMEWARP |  |\n| 83 | PRESET_ICON_EASY_MAX_STAR_TRAIL |  |\n| 84 | PRESET_ICON_EASY_MAX_LIGHT_PAINTING |  |\n| 85 | PRESET_ICON_EASY_MAX_LIGHT_TRAIL |  |\n| 89 | PRESET_ICON_MAX_STAR_TRAIL |  |\n| 90 | PRESET_ICON_MAX_LIGHT_PAINTING |  |\n| 91 | PRESET_ICON_MAX_LIGHT_TRAIL |  |\n| 100 | PRESET_ICON_EASY_STANDARD_PROFILE |  |\n| 101 | PRESET_ICON_EASY_HDR_PROFILE |  |\n| 102 | PRESET_ICON_BURST_SLOMO |  |\n| 1000 | PRESET_ICON_TIMELAPSE_PHOTO |  |\n| 1001 | PRESET_ICON_NIGHTLAPSE_PHOTO |  |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/EnumPresetIcon",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enumpresettitle (HTTP Schema)",
        "excerpt": "\n\n| ID | Name | Summary |\n| -- | ---- | ------- |\n| 0 | PRESET_TITLE_ACTIVITY |  |\n| 1 | PRESET_TITLE_STANDARD |  |\n| 2 | PRESET_TITLE_CINEMATIC |  |\n| 3 | PRESET_TITLE_PHOTO |  |\n| 4 | PRESET_TITLE_LIVE_BURST |  |\n| 5 | PRESET_TITLE_BURST |  |\n| 6 | PRESET_TITLE_NIGHT |  |\n| 7 | PRESET_TITLE_TIME_WARP |  |\n| 8 | PRESET_TITLE_TIME_LAPSE |  |\n| 9 | PRESET_TITLE_NIGHT_LAPSE |  |\n| 10 | PRESET_TITLE_VIDEO |  |\n| 11 | PRESET_TITLE_SLOMO |  |\n| 13 | PRESET_TITLE_PHOTO_2 |  |\n| 14 | PRESET_TITLE_PANORAMA |  |\n| 16 | PRESET_TITLE_TIME_WARP_2 |  |\n| 18 | PRESET_TITLE_CUSTOM |  |\n| 19 | PRESET_TITLE_AIR |  |\n| 20 | PRESET_TITLE_BIKE |  |\n| 21 | PRESET_TITLE_EPIC |  |\n| 22 | PRESET_TITLE_INDOOR |  |\n| 23 | PRESET_TITLE_MOTOR |  |\n| 24 | PRESET_TITLE_MOUNTED |  |\n| 25 | PRESET_TITLE_OUTDOOR |  |\n| 26 | PRESET_TITLE_POV |  |\n| 27 | PRESET_TITLE_SELFIE |  |\n| 28 | PRESET_TITLE_SKATE |  |\n| 29 | PRESET_TITLE_SNOW |  |\n| 30 | PRESET_TITLE_TRAIL |  |\n| 31 | PRESET_TITLE_TRAVEL |  |\n| 32 | PRESET_TITLE_WATER |  |\n| 33 | PRESET_TITLE_LOOPING |  |\n| 34 | PRESET_TITLE_STARS |  |\n| 35 | PRESET_TITLE_ACTION |  |\n| 36 | PRESET_TITLE_FOLLOW_CAM |  |\n| 37 | PRESET_TITLE_SURF |  |\n| 38 | PRESET_TITLE_CITY |  |\n| 39 | PRESET_TITLE_SHAKY |  |\n| 40 | PRESET_TITLE_CHESTY |  |\n| 41 | PRESET_TITLE_HELMET |  |\n| 42 | PRESET_TITLE_BITE |  |\n| 43 | PRESET_TITLE_CUSTOM_CINEMATIC |  |\n| 44 | PRESET_TITLE_VLOG |  |\n| 45 | PRESET_TITLE_FPV |  |\n| 46 | PRESET_TITLE_HDR |  |\n| 47 | PRESET_TITLE_LANDSCAPE |  |\n| 48 | PRESET_TITLE_LOG |  |\n| 49 | PRESET_TITLE_CUSTOM_SLOMO |  |\n| 50 | PRESET_TITLE_TRIPOD |  |\n| 58 | PRESET_TITLE_BASIC |  |\n| 59 | PRESET_TITLE_ULTRA_SLO_MO |  |\n| 60 | PRESET_TITLE_STANDARD_ENDURANCE |  |\n| 61 | PRESET_TITLE_ACTIVITY_ENDURANCE |  |\n| 62 | PRESET_TITLE_CINEMATIC_ENDURANCE |  |\n| 63 | PRESET_TITLE_SLOMO_ENDURANCE |  |\n| 64 | PRESET_TITLE_STATIONARY_1 |  |\n| 65 | PRESET_TITLE_STATIONARY_2 |  |\n| 66 | PRESET_TITLE_STATIONARY_3 |  |\n| 67 | PRESET_TITLE_STATIONARY_4 |  |\n| 68 | PRESET_TITLE_SIMPLE_VIDEO |  |\n| 69 | PRESET_TITLE_SIMPLE_TIME_WARP |  |\n| 70 | PRESET_TITLE_SIMPLE_SUPER_PHOTO |  |\n| 71 | PRESET_TITLE_SIMPLE_NIGHT_PHOTO |  |\n| 72 | PRESET_TITLE_SIMPLE_VIDEO_ENDURANCE |  |\n| 73 | PRESET_TITLE_HIGHEST_QUALITY |  |\n| 74 | PRESET_TITLE_EXTENDED_BATTERY |  |\n| 75 | PRESET_TITLE_LONGEST_BATTERY |  |\n| 76 | PRESET_TITLE_STAR_TRAIL |  |\n| 77 | PRESET_TITLE_LIGHT_PAINTING |  |\n| 78 | PRESET_TITLE_LIGHT_TRAIL |  |\n| 79 | PRESET_TITLE_FULL_FRAME |  |\n| 82 | PRESET_TITLE_STANDARD_QUALITY_VIDEO |  |\n| 83 | PRESET_TITLE_BASIC_QUALITY_VIDEO |  |\n| 93 | PRESET_TITLE_HIGHEST_QUALITY_VIDEO |  |\n| 94 | PRESET_TITLE_USER_DEFINED_CUSTOM_NAME |  |\n| 99 | PRESET_TITLE_EASY_STANDARD_PROFILE |  |\n| 100 | PRESET_TITLE_EASY_HDR_PROFILE |  |\n| 106 | PRESET_TITLE_BURST_SLOMO |  |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/EnumPresetTitle",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enumcohnnetworkstate (HTTP Schema)",
        "excerpt": "\n\n| ID | Name | Summary |\n| -- | ---- | ------- |\n| 0 | COHN_STATE_Init |  |\n| 1 | COHN_STATE_Error |  |\n| 2 | COHN_STATE_Exit |  |\n| 5 | COHN_STATE_Idle |  |\n| 27 | COHN_STATE_NetworkConnected |  |\n| 28 | COHN_STATE_NetworkDisconnected |  |\n| 29 | COHN_STATE_ConnectingToNetwork |  |\n| 30 | COHN_STATE_Invalid |  |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/EnumCOHNNetworkState",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enumcohnstatus (HTTP Schema)",
        "excerpt": "\n\n| ID | Name | Summary |\n| -- | ---- | ------- |\n| 0 | COHN_UNPROVISIONED |  |\n| 1 | COHN_PROVISIONED |  |\n",
        "url": "https://gopro.github.io/OpenGoPro/http#schema/EnumCOHNStatus",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Cohn Certificate (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_GET_HOME_NETWORK_CERT",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Set Client As Third Party (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_SET_ANALYTICS",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Set Camera Control Status (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n \n---\nThis command is used to tell the camera that a client (i.e. External Control) wishes to claim control of the camera.\nThis causes the camera to immediately exit most contextual menus and return to the idle screen. Any interaction with the\ncamera's physical buttons will cause the camera to reclaim control and update control status accordingly. If the user\nreturns the camera UI to the idle screen, the camera updates control status to Idle.\n\nNote:\n\n- The entity currently claiming control of the camera is advertised in camera status 114\n- Information about whether the camera is in a contextual menu or not is advertised in camera status 63.\n\nSee the below diagram for a state diagram of Camera Control:\n\n![global behaviors state diagram](assets/images/global_behaviors.png)\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_SET_CAMERA_CONTROL_STATUS",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enable Wired Camera Control Over Usb (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_SET_WIRED_USB_CONTROL",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Set Digital Zoom (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_DIGITAL_ZOOM_SET",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Date / Time (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_GET_DATE_AND_TIME_DST",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Hardware Info (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_CAMERA_INFO",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Keep Alive (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nIn order to maximize battery life, GoPro cameras automatically go to sleep after some time.\nThis logic is handled by a combination of the **Auto Power Down** setting which most (but not all) cameras support\nand a **Keep Alive** message that the user can regularly send to the camera.\n\nThe camera will automatically go to sleep if both timers reach zero.\n\nThe Auto Power Down timer is reset when the user taps the LCD screen, presses a button on the camera,\nprogrammatically (un)sets the shutter, sets a setting, or loads a Preset.\n\nThe Keep Alive timer is reset when the user sends a keep alive message.\n\nThe best practice to prevent the camera from inadvertently going to sleep is to start sending Keep Alive messages\nevery **3.0** seconds after a connection is established.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_KEEP_ALIVE",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Available Presets (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nGet the currently available Preset Groups and Presets, the set of which\n[depends](#tag/Presets/Presets) on the current camera settings.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_PRESETS_GET",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Load Preset By Id (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nA preset can only be loaded if it is currently available where available preset IDs can be found\nfrom  [Get Preset Status](#operation/OGP_PRESETS_GET)\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_PRESET_LOAD",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Load Preset Group By Id (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_PRESET_SET_GROUP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Update Custom Preset (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nThis only operates on the currently active Preset and will fail if the current\nPreset is not custom.\n\nThe use cases are:\n\n1. Update the Custom Preset Icon\n\n    - `icon_id` is always optional and can always be passed\n\nand / or\n\n2. Update the Custom Preset Title to a...\n\n    - **Factory Preset Title**: Set `title_id` to a non-`PRESET_TITLE_USER_DEFINED_CUSTOM_NAME` (94) value\n    - **Custom Preset Name**: Set `title_id` to `PRESET_TITLE_USER_DEFINED_CUSTOM_NAME` (94) and\n      specify a `custom_name`\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CUSTOM_PRESET_UPDATE",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Set Date / Time (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_SET_DATE_AND_TIME_DST",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Aspect Ratio (108) (HTTP Operation)",
        "excerpt": "\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::108",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Lens (121) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::121",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Photo Lens (122) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::122",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Time Lapse Digital Lenses (123) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::123",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Photo Output (125) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::125",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Media Format (128) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::128",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Anti Flicker (134) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::134",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Hypersmooth (135) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::135",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Horizon Leveling (150) (HTTP Operation)",
        "excerpt": "\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::150",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Photo Horizon Leveling (151) (HTTP Operation)",
        "excerpt": "\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::151",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Max Lens (162) (HTTP Operation)",
        "excerpt": "\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::162",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Hindsight (167) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::167",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Photo Single Interval (171) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::171",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Photo Interval Duration (172) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::172",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Performance Mode (173) (HTTP Operation)",
        "excerpt": "\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::173",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Controls (175) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::175",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Easy Mode Speed (176) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::176",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enable Night Photo (177) (HTTP Operation)",
        "excerpt": "\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::177",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Wireless Band (178) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::178",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Star Trails Length (179) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::179",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "System Video Mode (180) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::180",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Bit Rate (182) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::182",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Bit Depth (183) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::183",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Profiles (184) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::184",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Easy Mode (186) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::186",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Lapse Mode (187) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::187",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Max Lens Mod (189) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::189",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Max Lens Mod Enable (190) (HTTP Operation)",
        "excerpt": "\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::190",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Easy Night Photo (191) (HTTP Operation)",
        "excerpt": "\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::191",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Multi Shot Aspect Ratio (192) (HTTP Operation)",
        "excerpt": "\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::192",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Framing (193) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::193",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Resolution (2) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::2",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Camera Volume (216) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::216",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Setup Screen Saver (219) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::219",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Setup Language (223) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::223",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Photo Mode (227) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::227",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Framing (232) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::232",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Multi Shot Framing (233) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::233",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Frame Rate (234) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::234",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Frames Per Second (3) (HTTP Operation)",
        "excerpt": "\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::3",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Photo Timelapse Rate (30) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\nHow frequently to take a photo when performing a Photo Timelapse.",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::30",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Nightlapse Rate (32) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \nHow frequently to take a video or photo when performing a Nightlapse.\n\nThis controls the Video or Photo Nightlapse rate if Setting 128 is set to 21 or 26 respectively.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::32",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Webcam Digital Lenses (43) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::43",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Video Timelapse Rate (5) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \nHow frequently to take a video when performing a Video Timelapse",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::5",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Auto Power Down (59) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::59",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Gps (83) (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CHANGE_SETTING::83",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Set Shutter (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_SHUTTER",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Camera State (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nGet all camera settings and statuses.",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_GET_STATE",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Start Preview Stream (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_PREVIEW_STREAM_START",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Stop Preview Stream (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_PREVIEW_STREAM_STOP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Delete Cohn Certificates (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CLEAR_HOME_NETWORK_CERT",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Create The Cohn Ssl/Tls Certificates (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nThis creates the Camera On the Home Network SSL/TLS certs certs.\n The created certificate(s) can be obtained via [Get COHN Certificate](#operation/GPCAMERA_GET_HOME_NETWORK_CERT) and\n used for SSL/TLS communications\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_CREATE_HOME_NETWORK_CERT",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Configure Cohn Settings (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_SET_HOME_NETWORK_SETTING",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Cohn Status (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_GET_HOME_NETWORK_STATUS",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Delete Single Media File (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nWhen operating on a file that is part of a group, only the individual file will be deleted. To delete\nthe entire group, use [Delete Grouped Media Item](#tag/Media/operation/GPCAMERA_DELETE_FILE_GROUP)\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_DELETE_SINGLE_FILE",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Media File Gpmf (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nNone",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_MEDIA_GPMF",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Hilight A Media File (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nAdd a hilight / tag to an existing photo or media file.",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_ADD_HILIGHT",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Hilight While Recording (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n \n---\nAdd hilight at current time while recording video\n\nThis can only be used during recording.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_TAG_MOMENT",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Remove Hilight (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nRemove an existing hilight from a photo or video file.",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_REMOVE_HILIGHT",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Media File Info (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_MEDIA_INFO",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Last Captured Media (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nThis will return the complete path of the last captured media. Depending on the type of media captured, it will return:\n\n- single photo / video: The single media path\n- any grouped media: The path to the first captured media in the group\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_GET_LAST_MEDIA",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Media List (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nTo minimize the size of the JSON transmitted by the camera, grouped media items such as Burst Photos,\nTime Lapse Photos, Night Lapse Photos, etc are represented with a single item in the media list with additional keys\nthat allow the user to extrapolate individual filenames for each member of the group.\n\nFilenames for group media items have the form \"GXXXYYYY.ZZZ\"\nwhere XXX is the group ID, YYY is the group member ID and ZZZ is the file extension.\n\nFor example, take the media list below, which contains a Time Lapse Photo group media item:\n\n```json\n{\n    \"id\": \"2530266050123724003\",\n    \"media\": [\n        {\n            \"d\": \"100GOPRO\",\n            \"fs\": [\n                {\n                    \"b\": \"8\",\n                    \"cre\": \"1613669353\",\n                    \"g\": \"1\",\n                    \"l\": \"396\",\n                    \"m\": [\"75\", \"139\"],\n                    \"mod\": \"1613669353\",\n                    \"n\": \"G0010008.JPG\",\n                    \"s\": \"773977407\",\n                    \"t\": \"t\"\n                }\n            ]\n        }\n    ]\n}\n```\n\nThe first filename in the group is `G0010008.JP` (key: `n`).\n\nThe ID of the first group member in this case is `008` (key: `b`).\n\nThe ID of the last group member in this case is `396` (key: `l`).\n\nThe IDs of deleted members in this case are `75` and `139` (key: `m`)\n\nGiven this information, the user can extrapolate that the group currently contains\n\n```\nG0010008.JPG, G0010009.JPG, G0010010.JPG,\n...,\nG0010074.JPG, G0010076.JPG,\n...,\nG0010138.JPG, G0010140.JPG,\n...,\nG0010394.JPG, G0010395.JPG. G0010396.JPG\n```\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_MEDIA_LIST",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Media File Screennail (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nA screennail is a low-res preview image that is higher resolution than a thumbnail.",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_MEDIA_SCREENNAIL",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Media File Telemetry (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nGet Media File Telemetry track data",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_MEDIA_TELEMETRY",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Media File Thumbnail (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_MEDIA_THUMBNAIL",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Configure Turbo Transfer (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nSome cameras support Turbo Transfer mode, which allows media to be downloaded over WiFi more rapidly.\n\nThis special mode should only be used during media offload.\n\nIt is recommended that the user check for and, if necessary, disable Turbo Transfer on connection.\n\nNote that Disabling / enabling turbo mode will also enable / disable the transferring media camera UI.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_TURBO_MODE_ENABLE",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Open Gopro Version (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_OPENGOPRO_VERSION",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Exit Webcam Mode (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n ---\nNot supported on **WiFi** for:\n\n- Hero 11 Black Mini\n- Hero 11 Black\n- Hero 10 Black\n- Hero 9 Black\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_WEBCAM_EXIT_OGP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Enter Webcam Preview (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n ---\nNot supported on **WiFi** for:\n\n- Hero 11 Black Mini\n- Hero 11 Black\n- Hero 10 Black\n- Hero 9 Black\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_WEBCAM_PREVIEW_OGP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Start Webcam (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n ---\nNot supported on **WiFi** for:\n\n- Hero 11 Black Mini\n- Hero 11 Black\n- Hero 10 Black\n- Hero 9 Black\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_WEBCAM_START_OGP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Webcam Status (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_WEBCAM_STATUS_OGP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Stop Webcam (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n ---\nNot supported on **WiFi** for:\n\n- Hero 11 Black Mini\n- Hero 11 Black\n- Hero 10 Black\n- Hero 9 Black\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_WEBCAM_STOP_OGP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Get Webcam Version (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n ![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n\n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_WEBCAM_VERSION_OGP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Delete Grouped Media Item (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nDelete an entire group of media files such as in a burst, timelapse, or chaptered video. This API should\nnot be used to delete single files. Instead use [Delete Single File](#tag/Media/operation/OGP_DELETE_SINGLE_FILE)\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_DELETE_FILE_GROUP",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Resumable Ota Update (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nPerform Resumable OTA Update\n\nTo send a portion of the OTA image as per the requestBody specification, do not use the `request` parameter.\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_FIRMWARE_UPDATE_V2",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Simple Ota Update (HTTP Operation)",
        "excerpt": "\n![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/GPCAMERA_FWUPDATE_DOWNLOAD_FILE",
        "tags": [
            "httpOperation"
        ]
    },
    {
        "title": "Download A Media File (HTTP Operation)",
        "excerpt": "\n![HERO13 Black](https://img.shields.io/badge/HERO13%20Black-ffe119)\n![HERO12 Black](https://img.shields.io/badge/HERO12%20Black-f58231)\n ![HERO11 Black Mini](https://img.shields.io/badge/HERO11%20Black%20Mini-911eb4)\n![HERO11 Black](https://img.shields.io/badge/HERO11%20Black-f032e6)\n ![HERO10 Black](https://img.shields.io/badge/HERO10%20Black-bcf60c)\n![HERO9 Black](https://img.shields.io/badge/HERO9%20Black-fabebe)\n \n\nSupported Protocols:\n\n\n- usb\n- wifi\n\n---\nNote that this is the same endpoint for all media (photos, video, etc.).\n",
        "url": "https://gopro.github.io/OpenGoPro/http#operation/OGP_DOWNLOAD_MEDIA",
        "tags": [
            "httpOperation"
        ]
    }
]