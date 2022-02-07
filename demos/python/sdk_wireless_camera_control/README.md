# Open GoPro Python SDK

<img alt="GoPro Logo" src="https://raw.githubusercontent.com/gopro/OpenGoPro/main/docs/assets/images/logos/logo.png" width="50%" style="max-width: 500px;"/>

[![Build and Test](https://img.shields.io/github/workflow/status/gopro/OpenGoPro/Python%20SDK%20Testing?label=Build%20and%20Test)](https://github.com/gopro/OpenGoPro/actions/workflows/python_sdk_test.yml)
[![Build Docs](https://img.shields.io/github/workflow/status/gopro/OpenGoPro/Python%20SDK%20Docs%20Build%20and%20Deploy?label=Docs)](https://github.com/gopro/OpenGoPro/actions/workflows/python_sdk_deploy_docs.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/open-gopro)](https://pypi.org/project/open-gopro/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/gopro/OpenGoPro/blob/main/LICENSE)
![Coverage](https://raw.githubusercontent.com/gopro/OpenGoPro/main/demos/python/sdk_wireless_camera_control/docs/_static/coverage.svg)

This is a Python package that provides an interface for the user to exercise the Open GoPro Bluetooth Low
Energy (BLE) and Wi-Fi API's as well as install command line interfaces to take photos, videos, and view
the preview stream.

-   Free software: MIT license
-   Documentation: [View on Open GoPro](https://gopro.github.io/OpenGoPro/python_sdk/)
-   View on [Github](https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control)

## Documentation

> Note! This README is only an overview of the package.

Complete documentation can be found on [Open GoPro](https://gopro.github.io/OpenGoPro/python_sdk/)

## Features

-   Top-level GoPro class interface to use both BLE / WiFi
-   Cross-platform (tested on MacOS Big Sur, Windows 10, and Ubuntu 20.04)
    -   BLE implemented using [bleak](https://pypi.org/project/bleak/)
    -   Wi-Fi controller provided in the Open GoPro package (loosely based on the [Wireless Library](https://pypi.org/project/wireless/)
-   Supports all commands, settings, and statuses from the [Open GoPro API](https://gopro.github.io/OpenGoPro/)
-   Supports all versions of the Open GoPro API
-   Automatically handles connection maintenance:
    -   manage camera ready / encoding
    -   periodically sends keep alive signals
-   Includes detailed logging for each module
-   Includes demo scripts installed as command-line applications to show BLE and WiFi functionality
    -   Take a photo
    -   Take a video
    -   View the live stream
    -   Log the battery

## Installation

> Note! This package requires Python >= 3.8

```console
    $ pip install open-gopro
```

## Usage

To automatically connect to GoPro device via BLE and WiFI, set the preset, set video parameters, take a
video, and download all files:

```python
import time
from open_gopro import GoPro, Params

with GoPro() as gopro:
    gopro.ble_command.load_preset(Params.Preset.CINEMATIC)
    gopro.ble_setting.resolution.set(Params.Resolution.RES_4K)
    gopro.ble_setting.fps.set(Params.FPS.FPS_30)
    gopro.ble_command.set_shutter(Params.Shutter.ON)
    time.sleep(2) # Record for 2 seconds
    gopro.ble_command.set_shutter(Params.Shutter.OFF)

    # Download all of the files from the camera
    media_list = [x["n"] for x in gopro.wifi_command.get_media_list().flatten
    for file in media_list:
        gopro.wifi_command.download_file(camera_file=file)
```

And much more!

## Demos

> Note! These demos can be found on [Github](https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control/open_gopro/demos)

Demos can be found in the installed package in the "demos" folder. They are installed as a CLI entrypoint
and can be run via:

Capture a photo and download it to your computer:

```bash
$ gopro-photo
```

Capture a video and download it to your computer:

```bash
$ gopro-video
```

Start the preview stream and view it with [VLC](https://www.videolan.org/):

```bash
$ gopro-stream
```

Connect to the GoPro and log battery consumption in to a .csv:

```bash
$ gopro-log-battery
```

Connect to the GoPro's Wi-Fi AP and maintain the connection:

```bash
$ gopro-wifi
```

For more information on each, try running with help as such:

```bash
$ gopro-photo --help

usage: gopro-photo [-h] [-i IDENTIFIER] [-l LOG] [-o OUTPUT] [-w WIFI_INTERFACE]

Connect to a GoPro camera, take a photo, then download it.

optional arguments:
  -h, --help            show this help message and exit
  -i IDENTIFIER, --identifier IDENTIFIER
                        Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first
                        discovered GoPro will be connected to
  -l LOG, --log LOG     Location to store detailed log
  -o OUTPUT, --output OUTPUT
                        Where to write the photo to. If not set, write to 'photo.jpg'
  -w WIFI_INTERFACE, --wifi_interface WIFI_INTERFACE
                        System Wifi Interface. If not set, first discovered interface will be used.
```
