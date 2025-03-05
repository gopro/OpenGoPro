# Demos

This directory contains demos using the Open GoPro API with varying language and frameworks.

This file will also provide a summary of each demo.

## Demos Summary

| Language | Name                                                                   | Supported Platforms   | Notes                                                                                             |
| -------- | ---------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------- |
| bash     | [Over the Air Firmware Update](./bash/ota_update/README.md)            | Windows, Mac, Linux   |                                                                                                   |
| C++      | [Basic Media and Stream](./c_c++/GoProC_C++Demo/README.md)             | Windows, Mac, Linux   | Unoptimized Preview Stream                                                                        |
| C++      | [Low Latency Stream](./c_c++/GoProStreamDemo/README.md)                | Windows, Mac, Linux   | Low Latency Preview and Webcam Streams                                                            |
| C#       | [BLE and Wifi Connect / Control](./csharp/GoProCSharpSample/README.md) | Windows               |                                                                                                   |
| C#       | [Webcam Stream](./csharp/webcam/README.md)                             | Windows               | Unoptimized webcam streaming using VLC                                                            |
| Ionic JS | [BLE and WiFi Connect / Control](./ionic/file_transfer/readme.md)      | iOS, Android          |                                                                                                   |
| Kotlin   | [Kotlin SDK](./kotlin/kmp_sdk/README.md)                               | iOS (partly), Android | This is a fully featured SDK. See its [home page](https://gopro.github.io/OpenGoPro/kotlin_sdk/). |
| Python   | [Multi Webcam](./python/multi_webcam/README.md)                        | Windows, Mac, Linux   | Unoptimized streaming using OpenCV                                                                |
| Python   | [Python SDK](./python/sdk_wireless_camera_control/README.md)           | Windows, Mac, Linux   | This is a fully featured SDK. See its [home page](https://gopro.github.io/OpenGoPro/python_sdk/). |
| Swift    | [BLE and WiFi Connect / Control](./swift/EnableWiFiDemo/README.md)     | iOS                   |                                                                                                   |

## Contributing

To add a new demo:

1. Add your demo in the appropriate language subfolder of this directory. Create one if it does not exist.
1. Add a README.md in the demos directory describing what it does and how to use it
1. Add a summary row to the [summary table](#demos-summary) above.
