This directory contains demos using the Open GoPro API with varying language and frameworks.

## Summary

The following table briefly describes each directory and its supported systems. See the individual subdirectory
for more information.

| Directory                          | Summary                                                                                                       | Windows | Mac | Linux | Mobile |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------- | --- | ----- | ------ |
| bash/ota_update                    | A bash script to perform an over-the-air (OTA) firmware update                                                | ✔️      | ✔️  | ✔️    | ❌     |
| c_c++/GoProC_C++Demo               | Two C / C++ demos to send media commands and start/stop the preview stream                                    | ✔️      | ✔️  | ✔️    | ❌     |
| c_c++/GoProStreamDemo              | Low latency webcam/preview stream demo                                                                        | ✔️      | ❌  | ❌    | ❌     |
| csharp/GoProCSharpSample           | A C# demo for discovering, pairing, connecting and controlling a camera                                       | ✔️      | ❌  | ❌    | ❌     |
| csharp/webcam                      | A C# demo to demonstrate webcam functionality                                                                 | ✔️      | ❌  | ❌    | ❌     |
| ionic/file_transfer                | Ionic demo for transfering files from GoPro to Mobile over Wi-Fi here are demos for iOS & Android             | ❌      | ❌  | ❌    | ✔️     |
| python/sdk_wireless_camera_control | A Python package to easily exercise the Open GoPro API's + CLI's for taking pictures, videos, etc             | ✔️      | ✔️  | ✔️    | ❌     |
| python/tutorial                    | Short Python scripts to accompany the [Python Tutorials](https://gopro.github.io/OpenGoPro/tutorials/#python) | ✔️      | ✔️  | ✔️    | ❌     |
| swift/EnableWiFiDemo               | A swift demo for discovering, connecting and enabling Wi-Fi on a GoPro camera                                 | ❌      | ❌  | ❌    | ✔️     |

## Contributing

1. Add your demo in the appropriate language subfolder of this directory. Create one if it does not exist.
1. Add a README.md in the demos directory describing what it does and how to use it
1. Update the chart above
