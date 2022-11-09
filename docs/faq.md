---
permalink: /faq
read_time: false
---

# FAQ and Known Issues

# Frequently Asked Questions (FAQ)

If you have somehow stumbled here first, note that there are specifications, demos, and tutorials which expand upon
much of the information here. These can be found, among other places, from the [home page](/).

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

{% accordion How many devices can connect to the camera? %}
Simultaneously, only one device can connect at a time. However, the camera stores BLE security keys and
other connection information so it is possible to connect multiple devices sequentially.
{% endaccordion %}

## General

{% accordion Is preview turned off during record for all video settings? %}
Yes, preview is disabled during record on all video settings.
{% endaccordion %}

{% accordion How can I view the live stream? %}
In VLC, for example, you need to open network stream udp://@0.0.0.0:8554. You may see some latency due
to VLC caching. See the Preview Stream tutorial for more information.
{% endaccordion %}

{% accordion Which cameras are supported by Open GoPro? %}
The answer at a high level is >= Hero 9. However, there are also certain firmware requirements. For a complete
answer, see the [Specification]({% link specs/ble_versions/ble_2_0.md %}#supported-cameras).
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
[AP Control BLE Command]({% link specs/ble_versions/ble_2_0.md %}#commands)
{% endaccordion %}

# Known Issues

## Relevant to All Supported Cameras

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