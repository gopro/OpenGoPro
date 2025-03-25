# GoPro C/C++ Demos

- [GoPro C/C++ Demos](#gopro-cc-demos)
  - [Build](#build)
    - [Requirements](#requirements)
    - [Steps](#steps)
  - [Run](#run)
    - [Requirements](#requirements-1)
    - [Steps](#steps-1)
      - [Media Commands](#media-commands)
      - [Stream Commands](#stream-commands)

This folder contains C and C++ examples to perform some Open GoPro functionality. There are two examples,
each of which are detailed in a section below.

1. [**Media Commands**](#media-commands)
2. [**Stream Commands**](#stream-commands)

## Build

### Requirements

This demo depends on the following external libraries:

-   [libCurl](https://curl.se/download.html): a client-side URL transfer library used to make command requests to the camera over WiFi and get the JSON response
-   [cJSON](https://github.com/DaveGamble/cJSON): an ultra-light JSON parser that can be used to parse the JSON responses from the WiFi commands

To use the build system contained here, the following programs are required to be installed:

-   [Conan](https://docs.conan.io/en/latest/installation.html): a python-based C / C++ package manager
    -   If a local python 3 is found, this will be automatically installed
-   [CMake](https://cmake.org/install/): a project configuration and build tool

### Steps

1. Run the `build.sh` file. This will:
    - verify existence of requirements (and install Conan if applicable)
    - use Conan to download and install libCurl and cJson
    - use CMake to configure build system and build executables
1. The output binaries will then be available in `build/bin`

## Run

### Requirements

Before running the executables built here, you must first be connected to the camera's WiFi Access Point. This can be
done via:

1. Connect [BLE](https://gopro.github.io/OpenGoPro/ble) to turn on AP and get [WiFi](https://gopro.github.io/OpenGoPro/http) SSID/PASSPHRASE
2. Use retrieved WiFi SSID/PASSPHRASE to connect system to GoPro WiFi

A programmatic example of this process can be found in the Open GoPro Python SDK's
[Connect Wifi Demo](https://gopro.github.io/OpenGoPro/python_sdk/quickstart.html#wifi-demo). This can be run
(assuming a local Python 3.8.x installation exists) via:

```
pip install open-gopro
gopro-wifi
```

### Steps

#### Media Commands

This demo shows one way to get the media list and download the first media file. It also supports
requests to get the media list, media info and downloading specific media files.

For a list of possible commands, do:

```
$ ./build/bin/media_commands --help
```

Media List:

```bash
$ ./build/bin/media_commands <-l, --list_files>
```

Media List(Pretty Print):

```bash
$ ./build/bin/media_commands <-f, --list_files_pretty>
```

Media Info:

```bash
$ ./build/bin/media_commands <-i, --info> <camera_file_path>
```

Media Info(Pretty Print):

```bash
$ ./build/bin/media_commands <-p, --info_pretty> <camera_file_path>
```

Media Download:

```bash
$ ./build/bin/media_commands <-g, --download> <camera_file_path> <output_path/output_file_name>
```

Media Hilight Moment:

```bash
$ ./build/bin/media_commands --tag
```

Media Hilight File:

```bash
$ ./build/bin/media_commands --tag-video <video_file_path> <offset_ms>
```

```bash
$ ./build/bin/media_commands --tag-photo <photo_file_path>
```

Media Hilight Remove:

```bash
$ ./build/bin/media_commands --tag-video-remove <video_file_path> <offset_ms>
```

```bash
$ ./build/bin/media_commands --tag-photo-remove <photo_file_path>
```

Media Demo:

```bash
$ ./build/bin/media_commands <-d, --demo> <output_path>
```

#### Stream Commands

This demo demonstrates one way to start and stop the preview stream.

> Note: To run the Preview Stream demo. A media player (i.e: [VLC](https://www.videolan.org/)) that supports UDP is needed to view the preview stream.
> The UDP address is **_udp://0.0.0.0:8554_**

Start Stream:

```bash
$ ./build/bin/stream_commands <-s, --start>
```

Stop Stream:

```bash
$ ./build/bin/stream_commands <-e, --end>
```

Preview Stream Demo:

```bash
$ ./build/bin/stream_commands <-d, --demo>
```
