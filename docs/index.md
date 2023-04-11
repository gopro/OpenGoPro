---
title: Open GoPro
layout: splash
header:
    overlay_color: '#000'
    overlay_filter: '0.5'
    overlay_image: /assets/images/splash.jpg
    actions:
        - label: 'View on Github'
          url: 'https://github.com/gopro/OpenGoPro'
excerpt: 'An open source interface specification to communicate with a GoPro camera with accompanying demos and tutorials.'
read_time: false
classes: main__splash
toc: true
toc_sticky: true
---

Open GoPro is an API for interacting with GoPro cameras that is developed and managed directly by GoPro.
It provides developers and companies with an easy-to-use programming interface and helps integrate the cameras
into their ecosystems. The API works with off-the-shelf cameras with standard firmware, is free-to-use under
MIT license, and publicly available online on GitHub.

## Compatibility

Open GoPro API is supported on all camera models since Hero 9 with the following firmware version requirements:

| Camera             | Minimum FW Version |
| ------------------ | ------------------ |
| Hero 9 Black       | v01.70.00          |
| Hero 10 Black      | v01.10.00          |
| Hero 11 Black      | v01.10.00          |
| Hero 11 Black Mini | v01.10.00          |

While we strive to provide the same API functionality and logic for all newly launched cameras, minor changes
are sometimes necessary. These are typically a consequence of HW component upgrades or improving or optimizing
FW architecture. Therefore support for some functions and commands might be model-specific. This is
described in the compatibility tables in the documentation.

## Interfaces

Users can interact with the camera over BLE, WiFi, or wired USB. Both Wifi and USB are operated through HTTP
server with identical commands. It is important to note that due to hard constraints of power and the hardware
design, some commands in Wi-Fi are not available in BLE, and vice-versa.

### Bluetooth Low Energy (BLE)

BLE is the fastest way to control the cameras and a requirement for any type of Wireless control since camera
WiFi must be enabled upon each connection via BLE. Some functionality such as livestreaming is only possible
via BLE. For more information, see the [BLE Specification]({% link specs/ble_versions/ble_2_0.md %})

### WiFi

WiFi needs to be switched on by a BLE command. Besides command & control, Wi-Fi also allows for video streaming
and media manipulation. With the exception of live-streaming, the camera always acts as an Wi-Fi access point
that other devices need to connect to. For more information, see the
[Wifi Specification]({% link specs/http_versions/http_2_0.md %})

### USB

The USB connection can provide both data transfer and power to the camera. The power provided by the USB is
sufficient for the camera to run indefinitely without the internal battery. However, the wired connection
doesn't allow for programmatic power on and off. Camera needs to be switched on manually or via BLE, and
after the camera goes to sleep, it must be “woken up” again with a button press or via BLE. For monitoring
and other use cases where the camera must be operated and switched on and off only via USB cable, there is a
workaround with the Labs firmware - more detail in our FAQ. TODO read this

## Features

Here is a summary of currently supported per-interface features:

| Feature                | BLE | WiFi | USB |
| ---------------------- | --- | ---- | --- |
| Retrieve Camera State  | ✔️  | ✔️   | ✔️  |
| Change Settings / Mode | ✔️  | ✔️   | ✔️  |
| Encode (Press shutter) | ✔️  | ✔️   | ✔️  |
| Stream Video           |     | ✔️   | ✔️  |
| Media Management       |     | ✔️   | ✔️  |
| Metadata Extraction    |     | ✔️   | ✔️  |
| Camera Connect / Wake  | ✔️  |      |     |

### Control Camera and Record Remotely

BLE, WiFi, and USB can be used to change settings and modes, start and stop capture, query remaining battery
life, SD card capacity, or camera status (such as "is it recording?"). Most command-and-control functionality is
disabled while the camera is recording video or is otherwise busy.

There are 3 main recording modes for the cameras:

-   photo
-   video
-   timelapse

Within each mode, one can choose different frame rates, resolutions and FOV options. Note that not all cameras
have all 3 recording modes, not all settings combinations are available for all camera models. The specification
section links to json and xls files that show all available setting combinations per camera model.

### Stream Video

Besides recording, the cameras can also stream video feed. The API provides 3 different ways to stream videos
directly from the cameras, either via USB or wireless connection.

| Stream Type | Description                                   | WiFi | USB | Record while Streaming |
| ----------- | --------------------------------------------- | ---- | --- | ---------------------- |
| : Preview : | Moderate video quality, primarily for framing |      |     | \                      |
| Stream      | Low latency stabilization                     | ✔️   | ✔️  | \                      |
|             | Low power consumption                         |      |     |                        |
| : Webcam :  | Cinematic video quality                       |      |     | \                      |
| Mode        | Optional low latency stabilization            | ✔️   | ✔️  |                        |
| : Live :    | Cinematic video quality                       |      |     | \                      |
| Stream      | Optional hypersmooth stabilization            |      | ✔️  | ✔️                     |

Each of the streaming types has different resolutions, bit rates, imaging pipelines, and different levels of
configurability. Refer to the FAQ section for details. TODO add links.

### Manipulate and Transfer Media Files

When the camera records video, time lapse, or photo, the media is saved on the SD card with filenames according
to the GoPro [File Naming Convention](https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention). 

The cameras always record two versions of each video file: Full resolution based on your selected settings (MP4), and low resolution video proxy (LRV file) that can be used for editing or other operations where file size matters. “LRV” file ending can be simply renamed to “MP4” and used for playback or further editing. Both versions live in the same folder on the SD card. In addition, cameras generate a thumbnail image for each media file (THM). The THM ending can be changed to JPEG if required. 



You can access, delete, or copy all three file types to the desired connected location via API commands.