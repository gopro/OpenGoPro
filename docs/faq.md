---
permalink: /faq
read_time: false
---

# Frequently Asked Questions

If you have somehow stumbled here first, note that there are specifications, demos, and tutorials which expand upon
much of the information here. These can be found, among other places, from the [home page](/).

## Connectivity

{% accordion
  question="What is the distance from the camera that BLE will still work?"
  answer="It is standard Bluetooth 4.0 range and it depends on external factors such as: Interference: anything
  interfering with the signal will shorten the range. The type of device that the camera is connected to: BT
  classification distinguishes 3 device classes based on their power levels. Depending on the class of the
  connected device, the range varies from less than 10 meters to 100 meters."
%}

{% accordion
  question="Can I connect using WiFi only?"
  answer="Theoretically yes, if you already know the SSID, password, and the camera's WiFi AP has been enabled.
  However, practically no because BLE is required in order to discover this information and configure the AP."
%}

{% accordion
  question="Can I connect using BLE only?"
  answer="Yes, however there is some functionality that is not possible over BLE such as accessing the media list
  and downloading files."
%}

{% accordion
  question="How many devices can connect to the camera?"
  answer="Simultaneously, only one device can connect at a time. However, the camera stores BLE security keys and
  other connection information so it is possible to connect multiple devices sequentially."
%}

## General

{% accordion
  question="Is preview turned off during record for all video settings?"
  answer="Yes, preview is disabled during record on all video settings."
%}
{% accordion
  question="How can I view the live stream?"
  answer="In VLC, for example, you need to open network stream udp://@0.0.0.0:8554. You may see some latency due
  to VLC caching. See the Preview Stream tutorial for more information."
%}

## Troubleshooting

If you are able to consistently reproduce a problem, please file a bug on [Github Issues](https://github.com/gopro/OpenGoPro/issues)

{% accordion
  question="Why isn't the camera advertising?"
  answer="If you have not yet paired to the camera with the desired device, then you need to first set the
  camera into pairing mode (Connections->Connect Device->Quick App). If you have already
  paired, then the camera should be advertising and ready to connect. If it is not advertising, it is possible
  you are already connected to it from a previous session. To be sure, power cycle both the camera and the peer device."
%}