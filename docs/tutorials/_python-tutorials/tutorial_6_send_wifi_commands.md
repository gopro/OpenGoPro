---
permalink: '/tutorials/python/send-wifi-commands'
sidebar:
    nav: 'python-tutorials'
lesson: 6
---

# Python Tutorial 6: Send WiFi Commands

This document will provide a walk-through tutorial to use the Python [requests](https://pypi.org/project/requests/)
package to send Open GoPro [HTTP commands]({% link specs/http_versions/http_2_0.md %}) to the GoPro.

{% warning %}
It is required that you have first completed the
[Connecting to Wifi]({% link _python-tutorials/tutorial_5_connect_wifi.md %}) tutorial.
{% endwarning %}

This tutorial only considers sending these commands as one-off commands. That is, it does not consider state management /
synchronization when sending multiple commands. This will be discussed in a future tutorial.

There are two types of responses that can be received from the HTTP commands: JSON and binary. This section
will deal with commands that return JSON responses. For commands with binary responses (as well as commands with
JSON responses that work with the media list), see the [next tutorial]({% link _python-tutorials/tutorial_7_camera_media_list.md %}).

# Requirements

It is assumed that the hardware and software requirements from the [connect tutorial]({% link _python-tutorials/tutorial_1_connect_ble.md %}#requirements)
are present and configured correctly.

The scripts that will be used for this tutorial can be found in the
[Tutorial 6 Folder](https://github.com/gopro/OpenGoPro/tree/main/demos/python/tutorial/tutorial_modules/tutorial_6_send_wifi_commands).

# Just Show me the Demo(s)!!

If you just want to run the demo, you can find Python scripts for each of the concepts in this tutorial in the [Open GoPro GitHub repo]( https://github.com/gopro/OpenGoPro).

{% warning %}
Python >= 3.8.x must be used as specified in the requirements
{% endwarning %}

{% note %}
Each of the scripts for this tutorial can be found in this directory of the repo: 
`demos/python/tutorial/tutorial_modules/tutorial_6_send_wifi_commands/`
{% endnote %}

{% warning %}
You must be connected to the camera via WiFi in order to run these scripts. You can do this by manually to the SSID and password listed on your camera or by leaving the `Establish Connection to WiFi AP` script from [Tutorial 5]({% link _python-tutorials/tutorial_5_connect_wifi.md %}#just-show-me-the-demos) running in the background.
{% endwarning %}

{% accordion Get Open GoPro Version %}

You can test querying the Open GoPro version on your camera with HTTP over WiFi using the following script:
```console
$ python wifi_command_get_version.py
```

See the help for parameter definitions:

```console
$ python wifi_command_get_version.py --help
usage: wifi_command_get_version.py [-h]

Get the camera's supported Open GoPro version.

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}


{% accordion Digital Zoom %}

You can test setting the digital zoom level on your camera with HTTP over WiFi using the following script:
```console
$ python wifi_command_zoom.py
```

See the help for parameter definitions:

```console
$ python wifi_command_zoom.py --help
usage: wifi_command_zoom.py [-h] [-z ZOOM]

Set the digital zoom level.

optional arguments:
  -h, --help            show this help message and exit
  -z ZOOM, --zoom ZOOM  Zoom percentage (0-100)
```
{% endaccordion %}


{% accordion Get State %}

You can test querying the state of your camera with HTTP over WiFi using the following script:
```console
$ python wifi_command_get_state.py
```

See the help for parameter definitions:

```console
$ python wifi_command_get_state.py --help
usage: wifi_command_get_state.py [-h]

Get the state of the GoPro (status and settings).

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}


{% accordion Preview Stream %}

You can test enabling the UDP preview stream with HTTP over WiFi using the following script:
```console
$ python wifi_command_preview_stream.py
```

See the help for parameter definitions:

```console
$ python wifi_command_preview_stream.py --help
usage: wifi_command_preview_stream.py [-h]

Enable the preview stream.

optional arguments:
  -h, --help  show this help message and exit
```

Once enabled the stream can be viewed at `udp://@:8554` (For more details see the View Stream tab in the [Preview Stream]({% link _python-tutorials/tutorial_6_send_wifi_commands.md %}#preview-stream) section below.
{% endaccordion %}


{% accordion Load Preset Group %}

You can test sending the load preset group command with HTTP over WiFi using the following script:
```console
$ python wifi_command_load_group.py
```

See the help for parameter definitions:

```console
$ python wifi_command_load_group.py --help
usage: wifi_command_load_group.py [-h]

Load the video preset group.

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}


{% accordion Load Preset %}

You can test sending the load preset command with HTTP over WiFi using the following script:
```console
$ python wifi_command_load_preset.py
```

See the help for parameter definitions:

```console
$ python wifi_command_load_preset.py --help
usage: wifi_command_load_preset.py [-h]

Load a preset by ID.

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}


{% accordion Get Preset Status %}

You can test querying the preset status with HTTP over WiFi using the following script:
```console
$ python wifi_command_get_preset_status.py
```

See the help for parameter definitions:

```console
$ python wifi_command_get_preset_status.py --help
usage: wifi_command_get_preset_status.py [-h]

Get the current preset status.

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}


{% accordion Keep Alive %}

You can test sending the Keep Alive command with HTTP over WiFi using the following script:
```console
$ python wifi_command_keep_alive.py
```

See the help for parameter definitions:

```console
$ python wifi_command_keep_alive.py --help
usage: wifi_command_keep_alive.py [-h]

Send the keep alive signal.

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}


{% accordion Set Shutter %}

You can test sending the Set Shutter command with HTTP over WiFi using the following script:
```console
$ python wifi_command_set_shutter.py
```

See the help for parameter definitions:

```console
$ python wifi_command_set_shutter.py --help
usage: wifi_command_set_shutter.py [-h]

Take a 3 second video.

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}


{% accordion Set Setting %}

You can test setting the resolution setting with HTTP over WiFi using the following script:
```console
$ python wifi_command_set_resolution.py
```

See the help for parameter definitions:

```console
$ python wifi_command_set_resolution.py --help
usage: wifi_command_set_resolution.py [-h]

Set the video resolution to 1080.

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}


{% accordion Get Media List %}

You can test the Get Media List command with HTTP over WiFi using the following script:
```console
$ python wifi_command_get_media_list.py
```

See the help for parameter definitions:

```console
$ python wifi_command_get_media_list.py --help
usage: wifi_command_get_media_list.py [-h]

Get the media list.

optional arguments:
  -h, --help  show this help message and exit
```
{% endaccordion %}

# Setup

We must first connect to The GoPro's WiFi Access Point (AP) as was discussed in the
[Connecting to Wifi]({% link _python-tutorials/tutorial_5_connect_wifi.md %}) tutorial.

# Sending HTTP Commands with JSON Responses

Now that we are are connected via WiFi, we will use the `requests` module to send the various HTTP commands.

Both Command Requests and Setting Requests follow the same procedure:

1. Send HTTP GET command to appropriate endpoint
1. Receive confirmation from GoPro (via HTTP response) that request was received.
1. GoPro reacts to command

{% note %}
The HTTP response only indicates that the request was received correctly. The relevant behavior of the
GoPro must be observed to verify when the command's effects have been applied.
{% endnote %}

```mermaid!
sequenceDiagram
  participant PC as Open GoPro user device
  participant GoPro
  note over GoPro, PC: PC connected to WiFi AP
  PC ->> GoPro: Command Request (GET)
  activate GoPro
    GoPro ->> PC: Command Response (HTTP 200 OK)
    GoPro ->> GoPro: Apply affects of command when able
  deactivate GoPro
```

{% tip %}
We are building the endpoints using the GOPRO_BASE_URL defined in the tutorial package's `__init__.py`
{% endtip %}

## Get Open GoPro Version

The first command we will be sending is
[Get Version]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). This should be the first command you send
after connecting.

{% warning %}
It is imperative to know the Open GoPro version that the connected camera supports as setting values,
endpoints, and more differ between versions
{% endwarning %}

Let's build the endpoint first send the Keep Alive signal:

```python
url = GOPRO_BASE_URL + f"/gopro/version
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

This will log as such:

```console
INFO:root:Getting the Open GoPro version: sending http://10.5.5.9:8080/gopro/version
INFO:root:Command sent successfully
INFO:root:Response: {
    "version": "2.0"
}
```

In this case, this camera supports version 2.0 of the Open GoPro spec. We will an example of why this is important in the Set Setting section
[below](#set-setting).

## Digital Zoom

The next command we will be sending is
[Digital Zoom]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). The camera
must be in the [Photo Preset Group]({% link _python-tutorials/tutorial_2_send_ble_commands.md %}#load-preset-group)
for this command to succeed. The commands writes to the following endpoint:

`/gopro/camera/digital_zoom?percent=50`

Let's build the endpoint (in this example from the script, **zoom** is a command line argument that defaults to 50):

```python
url = GOPRO_BASE_URL + f"gopro/camera/digital_zoom?percent={zoom}"
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

This will log as such:

```console
INFO:root:Setting digital zoom to 50%: sending http://10.5.5.9:8080/gopro/camera/digital_zoom?percent=50
INFO:root:Command sent successfully
INFO:root:Response: {}
```

{% success %}
The response JSON is empty. This is expected in the case of a success.
{% endsuccess %}

## Get State

{% tabs state %}
{% tab state Send Request %}

The next command we will be sending is
[Get State]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). This command will
return all of the current settings and values. It is basically a combination of the
[Get All Settings]({% link _python-tutorials/tutorial_4_ble_queries.md %}#query-all) and
[Get All Statuses]({% link _python-tutorials/tutorial_4_ble_queries.md %}#query-all)
commands that were sent via BLE. Since there is no way to query individual settings / statuses
via WiFi (or register for asynchronous notifications when they change), this is the only option to query
setting / status information via WiFi.

The command writes to the following endpoint:

`/gopro/camera/state`

Let's first build the endpoint:

```python
url = GOPRO_BASE_URL + "/gopro/camera/state"
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

Go to the next tab for examples of viewing and parsing the response.

{% endtab %}
{% tab state Parse Response %}

The response will log as such (abbreviated for brevity):

```console
INFO:root:Getting GoPro's status and settings: sending http://10.5.5.9:8080/gopro/camera/state
INFO:root:Command sent successfully
INFO:root:Response: {
    "status": {
        "1": 1,
        "2": 2,
        "3": 0,
        "4": 255,
        "6": 0,
        "8": 0,
        "9": 0,
        "10": 0,
        "11": 0,
        "13": 0,
        "14": 0,
        "17": 1,

  ...

  "settings": {
      "2": 9,
      "3": 1,
      "5": 0,
      "6": 1,
      "13": 1,
      "19": 0,
      "24": 0,
      "30": 0,
      "31": 0,
      "32": 10,
      "41": 9,
      "42": 5,
```

We can see what each of these values mean by looking at the
[Open GoPro Interface]({% link specs/ble_versions/ble_2_0.md %}#settings-quick-reference).

For example (for settings):

-   ID 2 == 9 equates to Resolution == 1080
-   ID 3 == 1 equates to FPS == 120

{% endtab %}
{% endtabs %}

## Preview Stream

{% tabs stream %}
{% tab stream Send Request %}

The next command we will be sending is
[Preview Stream]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). This command will
enable (or disable) the preview stream . It is then possible to view the preview stream from a media player.

The commands write to the following endpoints:

| Command              | Endpoint                   |
| -------------------- | -------------------------- |
| start preview stream | /gopro/camera/stream/start |
| stop preview stream  | /gopro/camera/stream/stop  |

Let's first build the endpoint:

```python
url = GOPRO_BASE_URL + "/gopro/camera/stream/start"
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

This will log as such:

```console
INFO:root:Starting the preview stream: sending http://10.5.5.9:8080/gopro/camera/stream/start
INFO:root:Command sent successfully
INFO:root:Response: {}
```

{% success %}
The response JSON is empty. This is expected in the case of a success.
{% endsuccess %}

Go to the next tab for an example of viewing the stream.

{% endtab %}
{% tab stream View Stream %}

Once enabled, the stream can be viewed at `udp://@:8554`.

Here is an example of viewing this using [VLC](https://www.videolan.org/):

{% note %}
The screen may slightly vary depending on your OS
{% endnote %}

1. Select **Media-->Open Network Stream**
1. Enter the path as such:

{% include figure image_path="/assets/images/tutorials/python/preview_stream.png" alt="Preview Stream" size="70%" caption="Configure Preview Stream" %}

1. Select play
1. The preview stream should now be visible.

{% endtab %}
{% endtabs %}

## Load Preset Group

The next command we will be sending is
[Load Preset Group]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). which is
used to toggle between the 3 groups of presets (video, photo, and timelapse).

Let's build the endpoint first to load the video preset group (the id comes from the command table linked above):

```python
url = GOPRO_BASE_URL + "/gopro/camera/presets/set_group?id=1000"
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

This will log as such:

```console
INFO:root:Loading the video preset group: sending http://10.5.5.9:8080/gopro/camera/presets/set_group?id=1000
INFO:root:Command sent successfully
INFO:root:Response: {}
```

{% success %}
The response JSON is empty. This is expected in the case of a success.
{% endsuccess %}

You should hear the camera beep and move to the Video Preset Group. You can tell this by the logo at the top
middle of the screen:

{% include figure image_path="/assets/images/tutorials/python/preset_group.png" alt="Preset Group" size="50%" caption="Preset Group" %}

## Load Preset

The next command we will be sending is
[Load Preset]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). which is
used to select a specific preset that is part of a Preset Group.

Let's build the endpoint first to load the Cinematic Preset (the id comes from the command table linked above):

```python
url = GOPRO_BASE_URL + "/gopro/camera/presets/load?id=2"
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

This will log as such:

```console
INFO:root:Loading the cinematic preset: sending http://10.5.5.9:8080/gopro/camera/presets/load?id=2
INFO:root:Command sent successfully
INFO:root:Response: {}
```

{% success %}
The response JSON is empty. This is expected in the case of a success.
{% endsuccess %}

You should hear the camera beep and switch to the Cinematic Preset (assuming it wasn't already set). You can verify
this by seeing the preset name in the pill at bottom middle of the screen.

{% include figure image_path="/assets/images/tutorials/python/preset.png" alt="Load Preset" size="50%" caption="Load Preset" %}

## Get Preset Status

{% tabs preset %}
{% tab preset Send Request %}

The next command we will be sending is
[Get Presets Status]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). This
command is used to get the list of all currently available presets as well as the settings that comprise
each preset. This includes both default and user-defined presets.

Let's first build the endpoint:

```python
url = GOPRO_BASE_URL + "/gopro/camera/presets/get"
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

Go to the next tab for examples of viewing and parsing the response.

{% endtab %}
{% tab preset Parse Response %}

The response will log as such (abbreviated for brevity):

```console
INFO:root:Getting the current preset status: sending http://10.5.5.9:8080/gopro/camera/presets/get
INFO:root:Command sent successfully
INFO:root:Response: {
    "presetGroupArray": [
        {
            "id": "PRESET_GROUP_ID_VIDEO",
            "presetArray": [
                {
                    "id": 6,
                    "mode": "FLAT_MODE_LOOPING",
                    "titleId": "PRESET_TITLE_LOOPING",
                    "userDefined": true,
                    "icon": "PRESET_ICON_LOOPING",
                    "settingArray": [
                        {
                            "id": 2,
                            "value": 9,
                            "isCaption": true
                        },
                        {
                            "id": 3,
                            "value": 5,
                            "isCaption": true
                        },
                        {
                            "id": 6,
                            "value": 1,
                            "isCaption": true
                        },
                        {
                            "id": 121,
                            "value": 0,
                            "isCaption": true
                        }
                    ],
                    "isModified": false
                },
                {
                    "id": 0,
                    "mode": "FLAT_MODE_VIDEO",
                    "titleId": "PRESET_TITLE_STANDARD",
                    "userDefined": false,
                    "icon": "PRESET_ICON_VIDEO",
                    "settingArray": [
                        {
                            "id": 2,
                            "value": 24,
                            "isCaption": true
                        },
                        {
                            "id": 3,
                            "value": 8,
                            "isCaption": true
                        },
                        {
                            "id": 121,
                            "value": 0,
                            "isCaption": true
                        }
                    ],
                    "isModified": true
                },
```

The JSON **presetGroupArray** tag is a list of presets where each preset is comprised of
an ID, array of settings, and other descriptive information. In the example above, we can
see that there is a user-defined looping preset and a default video preset. For more
information on creating / using custom presets, see the
[GoPro Community Article](https://community.gopro.com/s/article/GoPro-Webcam?language=en_US).
A future tutorial may be created to demonstrate parsing this JSON directly into a protobuf-compiled object.

{% note %}
The settings shown above are parsed the same as they were in the Get State command above
{% endnote %}

As a reader exercise, try creating a custom preset on the camera and then using this command to view its
information.

{% endtab %}
{% endtabs %}

## Keep Alive

The next command we will be sending is
[Keep Alive]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). which is
used to prevent the camera from powering down. Unless changed by the user, GoPro cameras will automatically
power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by
periodically sending this message.

Let's build the endpoint first send the Keep Alive signal:

```python
url = GOPRO_BASE_URL + f"/gopro/camera/keep_alive"
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

This will log as such:

```console
INFO:root:Sending the keep alive signal: sending http://10.5.5.9:8080/gopro/camera/keep_alive
INFO:root:Command sent successfully
INFO:root:Response: {}
```

{% tip %}
It is recommended to send a keep-alive at least once every 120 seconds.
{% endtip %}

## Set Shutter

The next command we will be sending is
[Set Shutter]({% link specs/http_versions/http_2_0.md %}#commands-quick-reference). which is
used to start and stop encoding.

Let's build the endpoint first send the Set Shutter signal:

```python
url = GOPRO_BASE_URL + f"/gopro/camera/shutter/start"
```

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

{% note %}
This command does not return a JSON response so we don't print the response
{% endnote %}

This will log as such:

```console
INFO:root:Turning the shutter on: sending http://10.5.5.9:8080/gopro/camera/shutter/start
INFO:root:Command sent successfully
```

We then wait a few seconds and repeat the above procedure to set the shutter off. This time we use the
following URL:

```python
url = GOPRO_BASE_URL + f"/gopro/camera/shutter/stop"
```

{% warning %}
The shutter can not be set on if the camera is encoding or set off if the camera is not encoding. An
attempt to do so will result in an error response.
{% endwarning %}

## Set Setting

The next command will be sending is [Set Setting]({% link specs/http_versions/http_2_0.md %}#settings-quick-reference).
This end point is used to update all of the settings on the camera. It is analogous to BLE commands like
[Set Video Resolution]({% link _python-tutorials/tutorial_2_send_ble_commands.md %}#set-the-video-resolution).

It is important to note that many settings are dependent on the video resolution (and other settings).
For example, certain FPS values are not valid with certain resolutions. In general, higher resolutions
only allow lower FPS values. Check the [camera capabilities]({% link specs/ble_versions/ble_2_0.md %}#camera-capabilities)
to see which settings are valid for given use cases.

{% tip %}
The following endpoint is different between Open GoPro 1.0 and 2.0.
{% endtip %}

Let's build the endpoint first to set the Video Resolution to 1080 (the setting_id and opt_value comes from
the command table linked above). Click the relevant tab for the desired Open GoPro Version.

{% tabs endpoint %}
{% tab endpoint Version 1.0 %}

```python
url = GOPRO_BASE_URL + f"/gopro/camera/setting?setting_id=2&opt_value=9"
```

{% endtab %}
{% tab endpoint Version 2.0 %}

```python
url = GOPRO_BASE_URL + f"/gopro/camera/setting?setting=2&option=9"
```

{% endtab %}
{% endtabs %}

Now we send the GET request and check the response for errors. Any errors will raise an exception.

```python
response = requests.get(url)
response.raise_for_status()
```

Lastly, we print the response's JSON data (nicely formatted with indent 4 using the `json` module):

```python
logger.info(f"Response: {json.dumps(response.json(), indent=4)}")
```

This will log as such:

```console
INFO:root:Setting the video resolution to 1080: sending http://10.5.5.9:8080/gopro/camera/setting?setting_id=2&opt_value=9
INFO:root:Command sent successfully
INFO:root:Response: {}
```

{% success %}
The response JSON is empty. This is expected in the case of a success.
{% endsuccess %}

You should hear the camera beep and see the video resolution change to 1080 in the pill in the bottom-middle of the
screen:

{% include figure image_path="/assets/images/tutorials/python/video_resolution.png" alt="Video Resolution" size="50%" caption="Video Resolution" %}

As a reader exercise, try using the [Get State] command to verify that the resolution has changed.

**Quiz time! 📚 ✏️**

{% quiz
    question="What is the significance of empty JSON in an HTTP response?"
    option="A:::Always an error! The command was not received correctly."
    option="B:::If the status is ok (200), this is expected."
    option="C:::This is expected for errors (code other than 200) but not expected for ok (200)."
    correct="B"
    info="It is common for the JSON response to be empty if the command was received successfully
    but there is no additional information to return at the current time."
%}

{% quiz
    question="Which of the of the following is not a real preset group?"
    option="A:::Timelapse"
    option="B:::Photo"
    option="C:::Burst"
    option="D:::Video"
    correct="C"
    info="There are 3 preset groups (Timelapse, Photo, and Video). These can be
    set via the Load Preset Group command."
%}

{% quiz
    question="How do you query the current video resolution setting (id = 2) via WiFi?"
    option="A:::Send GET to `/gopro/camera/state?setting_id=2`"
    option="B:::Send GET to `/gopro/camera/state?get_setting=2`"
    option="C:::Send POST to `/gopro/camera/state` with request 'setting_id=2'"
    option="D:::None of the Above"
    correct="D"
    info="You can't query individual settings or statuses with the HTTP API. In order to get the value of a specific setting you'll need to send a GET to `/gopro/camera/state` and parse the value of the desired setting from the JSON response."
%}

# Troubleshooting

## HTTP Logging

[Wireshark](https://www.wireshark.org/) can be used to view the HTTP commands and responses
between the PC and the GoPro.

1. Start a Wireshark capture on the WiFi adapter that is used to connect to the GoPro
2. Filter for the GoPro IP address (10.5.5.9)

{% include figure image_path="/assets/images/tutorials/python/wireshark.png" alt="Wireshark" size="100%" caption="Wireshark" %}

# Good Job!

{% success %}
Congratulations 🤙
{% endsuccess %}

You can now send any of the HTTP commands defined in the
[Open GoPro Interface]({% link specs/http_versions/http_2_0.md %}) that return JSON responses. You
may have noted that we did not discuss one of these (Get Media List) in this tutorial. Proceed to the
next tutorial to see how to get and perform operations using the media list.
