# Over the Air Firmware Update Demo

- [Over the Air Firmware Update Demo](#over-the-air-firmware-update-demo)
  - [Assumptions](#assumptions)
  - [Prerequisites](#prerequisites)
  - [OTA Procedure](#ota-procedure)
  - [Usage](#usage)
  - [Testing](#testing)

This directory contains a bash script to perform an over-the-air (OTA) firmware (FW) update to the camera.

## Assumptions

-   The host PC is already connected via WiFi to the target camera
-   The target FW images are already provided from GoPro as a .zip file. These can be found on the
    [Update Page](https://gopro.com/en/us/update) or programmatically from the
    [Firmware Catalog](https://api.gopro.com/firmware/v2/catalog) JSON information.

## Prerequisites

Alternatively to satisfying these prerequisites, the script can be run with the Docker option (see [usage](#usage))

-   The script uses [open ssl](https://www.openssl.org/) to calculate the hash so `openssl` must be
    installed and available on the system path.
-   The script uses [curl](https://curl.se/) to send HTTP commands so `curl` must be installed and
    available on the system path.

## OTA Procedure

The OTA procedure requires the following steps:

1. Calculate the SHA1 hash of the target .zip file.
1. Delete any partially stored data.
1. Show the update UI
1. Upload the target firmware to the camera
1. Notify the camera that the upload is complete
1. Instruct the camera to load the new firmware

## Usage

Call the `send_ota.sh` script here with the `-h` option for a detailed usage:

```
Usage: ./send_ota.sh [-d] OTA_UPDATE_FILE

Given a target FW .zip file, calculate its SHA1 hash, then send it over-the-air to an already connected camera.
Required positional arguments:
    OTA_UPDATE_FILE  target .zip file to send over-the-air. If using docker, must be passed as relative path
                     from the directory of this script
Optional arguments:
    -d               Use docker for openssl and curl commands.
    -h               Print this Help.
```

## Testing

There is a test script that will use a Python script (contained in a Docker container) to:

-   get the FW catalog JSON
-   get the UPDATE.zip from the link in the JSON
-   exercise the send_ota.sh script to send this firmware to the camera (outside of the container)

The test script is located `./test/test.sh` and should be passed the camera that is connected, i.e.:

```
./test.sh "HERO_11"
```

> Note! The test script needs to be run from the `test` folder

You can also run with the `--help` parameter to get a list of cameras.
