# GoPro C/C++ Demos

<img alt="GoPro Logo" src="https://raw.githubusercontent.com/gopro/OpenGoPro/main/docs/assets/images/logos/logo.png" width="50%" style="max-width: 500px;"/>

This folder contains C and C++ examples to perform some Open GoPro functionality. There are two examples,
each of which are detailed in a section below.

1. [**Media Commands**](#media-commands)
2. [**Stream Commands**](#stream-commands)

## Requirements

To build these demos as is, [libCurl](https://curl.se/download.html) and [cJSON](https://github.com/DaveGamble/cJSON) are necessary.
libCurl is a client-side URL transfer library. This is used to make command requests to the camera over WiFi and get the JSON response.
cJSON is an ultra-light JSON parser that can be used to parse the JSON responses from the WiFi commands. Both can be used in either
C or C++ and work for MacOS, Linux and Windows.

To connect to the camera:

1. Connect [BLE](https://gopro.github.io/OpenGoPro/ble) to turn on AP and get [WiFi](https://gopro.github.io/OpenGoPro/wifi) SSID/PASSPHRASE
2. Use retrieved WiFi SSID/PASSPHRASE to connect system to GoPro WiFi

<h2 id="media-commands">Media Commands</h2>

This demo demonstrates one way to get the media list and download the first media file. It also supports
requests to get the media list, media info and downloading specific media files.

Media List:

```bash
$ ./bin/media_commands <-l, --list_files>
```

Media List(Pretty Print):

```bash
$ ./bin/media_commands <-f, --list_files_pretty>
```

Media Info:

```bash
$ ./bin/media_commands <-i, --info> <camera_file_path>
```

Media Info(Pretty Print):

```bash
$ ./bin/media_commands <-p, --info_pretty> <camera_file_path>
```

Media Download:

```bash
$ ./bin/media_commands <-g, --download <camera_file_path> <output_path/output_file_name>>
```

Media Demo:

```bash
$ ./bin/media_commands <-d, --demo> <output_path>
```

<h2 id="stream-commands">Stream Commands</h2>

This demo demonstrates one way to start and stop the preview stream.

> Note: To run the Preview Stream demo. A media player (i.e: [VLC](https://www.videolan.org/)) that supports UDP is needed to view the preview stream.
> The UDP address is **_udp://0.0.0.0:8554_**

Start Stream:

```bash
$ ./bin/stream_commands <-s, --start>
```

Stop Stream:

```bash
$ ./bin/stream_commands <-e, --end>
```

Preview Stream Demo:

```bash
$ ./bin/stream_commands <-d, --demo>
```
