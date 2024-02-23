---
permalink: /faq
read_time: false
---

# FAQ and Known Issues

# Frequently Asked Questions (FAQ)

If you have somehow stumbled here first, note that there are specifications, demos, and tutorials which
expand upon much of the information here. These can be found, among other places, from the [home page](/).

## Connectivity

{% accordion What is the distance from the camera that BLE will still work? %}
It is standard Bluetooth 4.0 range and it depends on external factors such as: Interference: anything
interfering with the signal will shorten the range. The type of device that the camera is connected to: BT
classification distinguishes 3 device classes based on their power levels. Depending on the class of the
connected device, the range varies from less than 10 meters to 100 meters.
{% endaccordion %}

{% accordion Can I connect using WiFi only? %}
Theoretically yes, if you already know the SSID, password, and the camera's WiFi AP has been enabled.
However, practically no because BLE is required in order to discover this information and configure the AP.
{% endaccordion %}

{% accordion Can I connect using BLE only? %}
Yes, however there is some functionality that is not possible over BLE such as accessing the media list
and downloading files.
{% endaccordion %}

{% accordion How to allow third-party devices to automatically discover close-by GoPro cameras? %}
Devices can only be discovered via BLE by scanning for advertising GoPro cameras
{% endaccordion %}

## Multi Camera Setups

{% accordion How many devices can connect to the camera? %}
Simultaneously, only one device can connect at a time. However, the camera stores BLE security keys and
other connection information so it is possible to connect multiple devices sequentially.
{% endaccordion %}

{% accordion Is there currently a way to connect multiple cameras on the same Wifi network?  %}
No. Cameras can only be connected through Wi-Fi by becoming an access point itself (generating its own Wi-Fi
network), not as a peripheral.
{% endaccordion %}

{% accordion What is the time offset between multiple cameras executing the same command? %}
In cases when camera sync is important, we recommend using the USB connection, which minimizes the variance
among devices. The time drift among cameras connected by USB cable to the same host will be up to ~35ms.
Using BLE for that purpose will further increase it.
{% endaccordion %}

{% accordion Is there a way to precisely time sync cameras so the footage can be aligned during post-processing? %}
The cameras set their time via GPS. By default, the camera seeks GPS at the beginning of every session, but
this can be hindered by typical limitations of GPS signals. Additionally, there are two advanced options
that require GoPro Labs firmware installed on the camera. The best bet is
[multi-cam GPS sync](https://gopro.github.io/labs/control/gpssync/). Another option is
[precise time calibration](https://gopro.github.io/labs/control/precisiontime/) via a dynamic QR scan from a
smartphone or PC.
{% endaccordion %}

## Streaming

{% accordion What are the differences between the streaming options for GoPros? %}
There are currently 3 different options on how to stream out of GoPro cameras. They are available either via
Wi-Fi, USB, or both.

|                     | : Wifi :                   |                           | : USB :                  |                              |                              |
| ------------------- | -------------------------- | ------------------------- | ------------------------ | ---------------------------- | ---------------------------- |
|                     | ViewFinder Preview         | LiveStream                | ViewFinder Preview       | Webcam Preview               | Webcam                       |
| Orientation         | Floating or Fixed          | Landscape facing up       | Floating or Fixed        | Landscape: Floating or Fixed | Landscape: Floating or Fixed |
| Streaming Protocols | UDP (MPEG-TS)              | RTMP                      | UDP (MPEG-TS)            | UDP (MPEG-TS)                | UDP (MPEG-TS) \              |
|                     |                            |                           |                          | RTSP                         | RTSP                         |
| Connection Protocol | Wifi - AP Mode             | WiFi - STA Mode           | NCM                      | NCM                          | NCM                          |
| Resolution          | 480p, 720p                 | 480p, 720p, 1080p         | 480p, 720p               | 720p, 1080p                  | 720p, 1080p                  |
| Frame Rate          | 30                         | 30                        | 30                       | 30                           | 30                           |
| Bitrate             | 2.5 - 4 mbps               | 0.8 - 8 mbps              | 2.5 - 4 mbps             | 6 mbps                       | 6 mbps \                     |
|                     | depending on model         | configurable              | depending on model       |                              |                              |
| Stabilization       | Basic Stabilization        | HyperSmooth or none       | Basic Stabilization      | None                         | None                         |
| Image Quality       | Basic                      | Same as recorded content  | Basic                    | Basic                        | Same as recorded content     |
| Minimum Latency     | 210 ms                     | `>` 100ms (un-stabilized) | 210 ms                   | 210 ms                       | 210 ms \                     |
|                     |                            | `>` 1,100ms (stabilized)  |                          |                              |                              |
| Audio               | None                       | Stereo                    | None                     | None                         | None                         |
| Max Stream Time     | 150 minutes (720p on fully | 85 minutes (720p on fully | Unlimited (with external | Unlimited(with external      | Unlimited (with external\    |
|                     | charged Enduro battery)    | charged Enduro battery)   | power via USB)           | power via USB)               | power via USB                |

{% endaccordion %}

{% accordion How to achieve low latency feed streaming onto displays?  %}
The stream has a minimum latency of about 210ms. If you are seeing latency higher than that, we often find
that as a result of using off-the-shelf libraries like ffmpeg which adds its own buffering. For preview and
framing use cases, we don't recommend using the live streaming RTMP protocol because it adds unnecessary
steps in the pipeline, and puts the camera in the streaming preset, which offers little other control.
A low latency streaming demo is available in the [demos](https://github.com/gopro/OpenGoPro/tree/main/demos).
{% endaccordion %}

{% accordion How do I minimize latency of video preview with FFPLAY?  %}
FFPLAY by default will buffer remote streams. You can minimize the buffer using:

-   `--no-cache` (receiving side)
-   `-fflags nobuffer" (sender).

However, the best latency can be achieved by building your own pipeline or ffmpegs library for decoding the
bytes. Users should be able to achieve about 200-300 ms latency on the desktop and possibly optimize lower
than that.
{% endaccordion %}

{% accordion How to view the video stream in VLC? %}
To view the stream in VLC, you need to open network stream `udp://@0.0.0.0:8554`. You will still see latency
because VLC uses its own caching.
{% endaccordion %}

## Power

{% accordion What are the power requirements for GoPro if connected over USB? %}
All cameras have minimum power requirements, as specified
[here](https://community.gopro.com/s/article/Recommended-Chargers?language=en_US). As long as the power is
supplied, cameras will be fully functional with or without an internal battery. Removing the battery and
running on USB power alone will improve thermal performance and runtime.

If you are seeing issues with insufficient power and have a charger with correct specs, the problems likely
stem from low quality cables or low-quality adapters that are not able to consistently provide advertised
amperage. We have encountered USB-C cables manufactured with poor quality control that transfer enough power
only when their connectors face one side up, but not the other. We recommend using only high-quality
components that deliver the correct power output
{% endaccordion %}

{% accordion How to enable automatic power on and off in wired setups? %}
Cameras cannot be switched on remotely over USB, or "woken up" remotely after they "go to sleep". The best
workaround for this is via the GoPro Labs firmware that forces the camera to automatically switch on as soon
as it detects USB power and switch off when the powering stops. Refer to the WAKE command
[here](https://gopro.github.io/labs/control/extensions/).
{% endaccordion %}

## Metadata

{% accordion Can I use the GPS track from the camera in real time? %}
No. The GPS track on the camera as well as other metadata is not available until the file is written and
saved. If the objective is to add metadata to the stream, currently the only option is to pull GPS data from
another device (phone, wearable,... ) and sync it to the video feed.
{% endaccordion %}

{% accordion What can be accessed in the metadata file?  %}
Metadata exists as a proprietary GPMF (GoPro Metadata Format) and can be extracted from the file via
API commands separately for GPS, Telemetry data, or the entire metadata container. The following data points
can be extracted:

-   Camera settings (Exposure time, ISO, Sensor Gain, White balance)
-   Date and Time
-   IMU: GPS, gyroscope, and accelerometer
-   Smile detection
-   Audio levels
-   Face detection in bounding boxes
-   Scene Classifiers (water, urban, vegetation, snow, beach, indoor)

{% endaccordion %}

{% accordion Is there a way to change the file names or otherwise classify my video file? %}
Currently there are two options to do that, and both require GoPro Labs firmware. The stock firmware doesn’t
provide that option. With GoPro Labs installed, you can either
[inject metadata](https://gopro.github.io/labs/control/extensions/) into the file (and extract it later
with the [GPMF](https://github.com/gopro/gpmf-parser) parser) or use
[custom naming](https://gopro.github.io/labs/control/basename/) for the file.
{% endaccordion %}

{% accordion Is there a way to add time stamps to the video files and mark specific moments? %}
Open GoPro users can add time stamped markers, called “Hilights”, to flag specific moments in the video.
Hilights can be injected into the video in the real time and then extracted for analytics or other
post-processing purposes. The same Hilights are used in GoPro’s auto-editing engine Quik to determine the
most interesting moments in the video.
{% endaccordion %}

## General

{% accordion Which cameras are supported by Open GoPro? %}
The answer at a high level is >= Hero 9. However, there are also certain firmware requirements. For a complete
answer, see the [Specification](/ble/index.html#supported-cameras).
{% endaccordion %}

## Camera Logic

{% accordion Do commands operate as priority-wise or time-related? %}
The cameras use first-in, first-out logic.
{% endaccordion %}

{% accordion Is there an option to send the commands in cyclic format instead of sending requests for each command? %}
If you want to receive information asynchronously, it is possible via registering for BLE notifications.
See an example (tracking battery) in the Python SDK.
{% endaccordion %}

## Troubleshooting

If you are able to consistently reproduce a problem, please file a bug on [Github Issues](https://github.com/gopro/OpenGoPro/issues)

{% accordion Why is the camera not advertising? %}
If you have not yet paired to the camera with the desired device, then you need to first set the
camera into pairing mode (Connections->Connect Device->Quick App). If you have already
paired, then the camera should be advertising and ready to connect. If it is not advertising, it is possible
you are already connected to it from a previous session. To be sure, power cycle both the camera and the peer device.
{% endaccordion %}

{% accordion Workaround for intermittent Wifi AP Connection failure %}
On >= Hero 11, try disabling and then re-enabling the camera's Wifi AP using the
[AP Control BLE Command](/ble/index.html#commands)
{% endaccordion %}

# Known Issues

## Relevant to All Supported Cameras

{% accordion Webcam does not enter idle mode once plugged in %}
The webcam status will be wrongly reported as IDLE instead of OFF after a new USB connection.
The best workaround for this is to call `Webcam Start` followed by `Webcam Stop` after connecting USB in
order to make the webcam truly IDLE and thus willing to accept setting changes.
{% endaccordion %}

{% accordion Intermittent failure to connect to the cameras Wifi Access Point %}
On rare occasions, connections to the camera's Wifi AP will continuously fail until the camera is reset.
It is possible to workaround this as described in [Troubleshooting](#troubleshooting)
{% endaccordion %}

{% accordion Spurious Protobuf Notifications sent once camera is connected in Station mode %}
Once the camera has been connected in station mode (STA), it will start sending protobuf notifications with
action ID 0xFF. These should be ignored.
{% endaccordion %}

## Hero 11 (v01.10.00) Specific

{% accordion Wired Communication is broken after update mode %}
This is fixed by Resetting Connections and then re-pairing.
{% endaccordion %}
