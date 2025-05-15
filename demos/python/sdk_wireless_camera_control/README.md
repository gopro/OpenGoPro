# Open GoPro Python SDK

<img alt="GoPro Logo" src="https://raw.githubusercontent.com/gopro/OpenGoPro/gh-pages/assets/images/logos/logo.png" width="50%" style="max-width: 500px;"/>

[![Build and Test](https://img.shields.io/github/actions/workflow/status/gopro/OpenGoPro/python_sdk_test.yml)](https://github.com/gopro/OpenGoPro/actions/workflows/python_sdk_test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/open-gopro)](https://pypi.org/project/open-gopro/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/gopro/OpenGoPro/blob/main/LICENSE)
![Coverage](https://raw.githubusercontent.com/gopro/OpenGoPro/main/demos/python/sdk_wireless_camera_control/docs/_static/coverage.svg)

This is a Python package that provides an
interface for the user to exercise the Open GoPro Bluetooth Low Energy (BLE) and Wi-Fi / USB HTTP API's as well as install command line interfaces to take photos, videos, and view video streams.

-   Free software: MIT license
-   Documentation: [View on Open GoPro](https://gopro.github.io/OpenGoPro/python_sdk/)
-   View on [Github](https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control)

## Documentation

> Note! This README is only an overview of the package.

Complete documentation can be  found on [Open GoPro](https://gopro.github.io/OpenGoPro/python_sdk/)

## Features

-   Top-level GoPro class interface to use BLE, WiFi, and / or USB
-   Cross-platform (tested on MacOS Big Sur, Windows 10, and Ubuntu 20.04)
    -   BLE implemented using [bleak](https://pypi.org/project/bleak/)
    -   Wi-Fi controller provided in the Open GoPro package (loosely based on the [Wireless Library](https://pypi.org/project/wireless/)
-   Supports all commands, settings, and statuses from the [Open GoPro API](https://gopro.github.io/OpenGoPro/)
-   [Asyncio](https://docs.python.org/3/library/asyncio.html) based
-   Automatically handles connection maintenance:
    -   manage camera ready / encoding
    -   periodically sends keep alive signals
-   Includes detailed logging for each module
-   Includes demo scripts installed as command-line applications to show BLE, WiFi, and USB functionality such as:
    -   Take a photo
    -   Take a video
    -   Configure and view a GoPro webcam stream
    -   GUI to send all commands and view the live / preview stream
    -   Log the battery

## Installation

> Note! This package requires Python >= 3.11 and < 3.14 and only supports GoPros that
> [implement the OGP API](https://gopro.github.io/OpenGoPro/ble/#supported-cameras)

The minimal install to use the Open GoPro library and the CLI demos is:

```console
$ pip install open-gopro
```

To also install the extra dependencies to run the GUI demos, do:

```console
$ pip install open-gopro[gui]
```

## Usage

To automatically connect to GoPro device via BLE and WiFI, set the preset, set video parameters, take a
video, and download all files:

```python
import asyncio
from open_gopro import WirelessGoPro, Params

async def main():
    async with WirelessGoPro() as gopro:
        await gopro.ble_setting.video_resolution.set(constants.settings.VideoResolution.NUM_4K)
        await gopro.ble_setting.video_lens.set(constants.settings.VideoLens.LINEAR)
        await gopro.ble_command.set_shutter(shutter=constants.Toggle.ENABLE)
        await asyncio.sleep(2)  # Record for 2 seconds
        await gopro.ble_command.set_shutter(shutter=constants.Toggle.DISABLE)

        # Download all of the files from the camera
        media_list = (await gopro.http_command.get_media_list()).data.files
        for item in media_list:
            await gopro.http_command.download_file(camera_file=item.filename)

asyncio.run(main())
```

And much more!

## Demos

> Note! These demos can be found on [Github](https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control/open_gopro/demos)

Demos can be found in the installed package in the "demos" folder. They are installed as a CLI entrypoint
and can be run as shown below.

## Command Line Interface (CLI) Demos

All of these demos are CLI only and can thus be run with the minimal (non-GUI) install.

Capture a photo and download it to your computer:

```bash
$ gopro-photo
```

Capture a video and download it to your computer:

```bash
$ gopro-video
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


## GUI Demos

These demos require the additional GUI installation.

Start the preview stream and view it:

```bash
$ gopro-preview-stream
```

Start the live stream and view it:

```bash
$ gopro-live-stream
```