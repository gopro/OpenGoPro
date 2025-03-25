# Multi Webcam

- [Multi Webcam](#multi-webcam)
  - [Assumptions](#assumptions)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
    - [Start Webcam](#start-webcam)
      - [Example](#example)
    - [Single Webcam](#single-webcam)
  - [Multiple Webcams](#multiple-webcams)
  - [Module Usage](#module-usage)

This is a small Python module to demonstrate GoPro Webcam usage, including how to use multiple webcams
simultaneously from the same PC.

## Assumptions

It is assumed that the GoPro's are using firmware versions that support the port parameter to the Start Webcam
endpoint. See the Open GoPro Command [Quick Reference](https://gopro.github.io/OpenGoPro/http#tag/Webcam/operation/OGP_WEBCAM_START)
for more information.

## Installation

This module requires Python >= 3.10 and < 3.13.

It should be installed locally, either with pip via:

```
pip install .
```

## Quick Start

Once installed, the following CLI programs are available:

> Each CLI has useful help available by calling it with the `--help` argument

### Start Webcam

Configure and start a single webcam. Its stream can then be viewed using, for example [VLC](https://www.videolan.org/vlc/).

```
usage: start-webcam [-h] [-p PORT] [-r RESOLUTION] [-f FOV] serial

Enable and start the webcam.

positional arguments:
  serial                Last 3 digits of camera serial number.

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to use. If not set, port will not be specified to camera.
  -r RESOLUTION, --resolution RESOLUTION
                        Resolution to use. If set, fov must also be set.
  -f FOV, --fov FOV     FOV to use. If set, resolution must also be set
```

#### Example

```
start-webcam 992 -p 9000
```

The stream can than be viewed at `udp://@0.0.0.0:9001`

### Single Webcam

Configure and start a single webcam. Then display its stream. This is different than the previous program
in that it also handles displaying the stream (using [OpenCV](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)).

```
usage: single-webcam [-h] [-p PORT] [-r RESOLUTION] [-f FOV] serial

Enable and start the webcam and a player to view it.

positional arguments:
  serial                Last 3 digits of camera serial number.

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to use. If not set, port will not be specified to camera.
  -r RESOLUTION, --resolution RESOLUTION
                        Resolution to use. If set, fov must also be set.
  -f FOV, --fov FOV     FOV to use. If set, resolution must also be set
```

## Multiple Webcams

Using a `.json` configuraton file, configure, start, and view multiple webcams.

```
usage: multi-webcam [-h] config

Configure, enable and start webcams with players to view them.

positional arguments:
  config      Location of config json file.

options:
  -h, --help  show this help message and exit
```

where an example config file could look like this:

```
{
    "992": {
        "port": 9000,
        "resolution": 12,
        "fov": 0
    },
    "149": {
        "resolution": 12,
        "fov": 0
    }
}

```

If port is not set, an available port will be discovered automatically starting at 8554.
If resolution or fov are not set, they will be set to defaults by the GoPro.

## Module Usage

For detailed module usage, see the docstrings in `./multi_webcam/webcam.py`.
