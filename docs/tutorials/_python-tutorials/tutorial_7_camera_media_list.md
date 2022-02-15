---
permalink: '/tutorials/python/camera-media-list'
sidebar:
    nav: 'python-tutorials'
lesson: 7
---

# Python Tutorial 7: Camera Media List

This document will provide a walk-through tutorial to use the Python [requests](https://docs.python-requests.org/en/master/)
package to send Open GoPro [HTTP commands]({% link specs/http.md %}) to the GoPro,
specifically to get the media list and perform operations on it (downloading pictures, videos, etc.)

> Note! It is required that you have first completed the [Connecting to Wifi]({% link _python-tutorials/tutorial_5_connect_wifi.md %}) and [Sending WiFi Commands]({% link _python-tutorials/tutorial_6_send_wifi_commands.md %}) tutorials.

This tutorial only considers sending these commands as one-off commands. That is, it does not consider state management /
synchronization when sending multiple commands. This will be discussed in a future lab.

# Requirements

It is assumed that the hardware and software requirements from the [connect tutorial]({% link _python-tutorials/tutorial_1_connect_ble.md %}#requirements)
are present and configured correctly.

The scripts that will be used for this tutorial can be found in the
[Tutorial 7 Folder](https://github.com/gopro/OpenGoPro/tree/main/demos/python/tutorial/tutorial_modules/tutorial_7_camera_media_list).

# Just Show me the Demo(s)!!

Each of the operations detailed below has a corresponding script to demo it. If you don't want
to read this tutorial and just want to see the demo, for example, run:

```console
$ python wifi_media_download_file.py
```

> Note! Python 3.8.x must be used as specified in [the requirements]({% link _python-tutorials/tutorial_1_connect_ble.md %}#requirements)

Note that each script has a command-line help which can be found via:

```console
$ python wifi_media_download_file.py --help
usage: wifi_media_download_file.py [-h]

Find a photo on the camera and download it to the computer.

optional arguments:
  -h, --help  show this help message and exit
```

# Setup

We must first connect to The GoPro's WiFi Access Point (AP) as was discussed in the
[Connecting to Wifi]({% link _python-tutorials/tutorial_5_connect_wifi.md %}) tutorial.

# Get Media List

Now that we are are connected via WiFi, we will get the media list using the same procedure
to send HTTP commands as in the [previous tutorial]({% link _python-tutorials/tutorial_6_send_wifi_commands.md %}).

{% tabs media %}
{% tab media Send Request %}

We get the media list via the
[Get Media List command]({% link specs/http.md %}#commands-quick-reference).
This command will return a JSON structure of all of the media files (pictures, videos) on the camera with corresponding information about each media file.

Let's first build the endpoint:

```python
url = GOPRO_BASE_URL + "/gopro/media/list"
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
{% tab media Parse Response %}

The response will log as such (abbreviated for brevity):

```console
INFO:root:Getting the media list: sending http://10.5.5.9:8080/gopro/media/list
INFO:root:Command sent successfully
INFO:root:Response: {
    "id": "2510746051348624995",
    "media": [
        {
            "d": "100GOPRO",
            "fs": [
                {
                    "n": "GOPR0987.JPG",
                    "cre": "1618583762",
                    "mod": "1618583762",
                    "s": "5013927"
                },
                {
                    "n": "GOPR0988.JPG",
                    "cre": "1618583764",
                    "mod": "1618583764",
                    "s": "5009491"
                },
                {
                    "n": "GOPR0989.JPG",
                    "cre": "1618583766",
                    "mod": "1618583766",
                    "s": "5031861"
                },
                {
                    "n": "GX010990.MP4",
                    "cre": "1451608343",
                    "mod": "1451608343",
                    "glrv": "806586",
                    "ls": "-1",
                    "s": "10725219"
                },
```

The media list format is defined in the
[Open GoPro Specification]({% link specs/http.md %}#media-list-format).
We won't be rehashing that here but will provide examples below of using the media list.

One common functionality is to get the list of media file names, which can be done as such:

```python
print([x["n"] for x in media_list["media"][0]["fs"]])
```

That is, access the list at the **fs** tag at the first element of the **media** tag, then
make a list
of all of the names (**n** tag of each element) in the **fs** list.

{% endtab %}
{% endtabs %}

# Media List Operations

Whereas all of the WiFi commands described until now have returned JSON responses, most of
the media list operations return binary data. From an HTTP perspective, the behavior is the same. However,
the GET response will contain a large binary chunk of information so we will loop through it with the
`requests` library as such, writing up to 8 kB at a time:

```mermaid!
sequenceDiagram
  participant disk
  participant PC as Open GoPro user device
  participant GoPro
  note over GoPro, PC: PC connected to WiFi AP
  PC ->> GoPro: Get Media List (GET)
  GoPro ->> PC: Media List (HTTP 200 OK)
  PC ->> GoPro: Command Request (GET)
  activate GoPro
    GoPro ->> PC: Binary Response (HTTP 200 OK)
  deactivate GoPro
  activate PC
    loop write until complete
        PC ->> disk: write <= 8K
    end
  deactivate PC
```

## Download Media File

The next command we will be sending is
[Download Media]({% link specs/http.md %}#downloading-media). Specifically, we
will be downloading a photo. The camera must have at least one photo in its media list in order for this to
work.

First, we get the media list as in [Get Media List]({% link _python-tutorials/tutorial_7_camera_media_list.md %}#get-media-list) . Then we search through the list of file names in
the media list looking for a photo (i.e. a file whose name ends in **.jpg**). Once we find a photo, we
proceed:

```python
media_list = get_media_list()

photo: Optional[str] = None
for media_file in [x["n"] for x in media_list["media"][0]["fs"]]:
    if media_file.lower().endswith(".jpg"):
        logger.info(f"found a photo: {media_file}")
        photo = media_file
        break
```

Now let's build the endpoint to download the photo whose name we just found:

```python
url = GOPRO_BASE_URL + f"videos/DCIM/100GOPRO/{photo}"
```

{% tip %}
The endpoint will start with "videos" for both photos and videos
{% endtip %}

Next we send the GET request and check the response for errors. Any errors will raise an exception.

```python
with requests.get(url, stream=True) as request:
    request.raise_for_status()
```

Lastly, we iterate through the binary content in 8 kB chunks, writing to a local file:

```python
file = photo.split(".")[0] + ".jpg"
with open(file, "wb") as f:
    logger.info(f"receiving binary stream to {file}...")
    for chunk in request.iter_content(chunk_size=8192):
        f.write(chunk)
```

This will log as such:

```console
INFO:root:found a photo: GOPR0987.JPG
INFO:root:Downloading GOPR0987.JPG
INFO:root:Sending: http://10.5.5.9:8080/videos/DCIM/100GOPRO/GOPR0987.JPG
INFO:root:receiving binary stream to GOPR0987.jpg...
```

Once complete, the `GOPR0987.jpg` file will be available from where the demo script was called.

## Get Media GPMF

The next command we will be sending is
[Get Media GPMF]({% link specs/http.md %}#commands-quick-reference). More
information about GPMF can be found [here](https://github.com/gopro/gpmf-parser). Specifically, we will be
downloading the GPMF for a photo. The camera must have at least one photo in its media list in order for this to
work.

First, we get the media list as in [Get Media List]({% link _python-tutorials/tutorial_7_camera_media_list.md %}#get-media-list) . Then we search through the list of file names in
the media list looking for a photo (i.e. a file whose name ends in **.jpg**). Once we find a photo, we
proceed:

```python
media_list = get_media_list()

photo: Optional[str] = None
for media_file in [x["n"] for x in media_list["media"][0]["fs"]]:
    if media_file.lower().endswith(".jpg"):
        logger.info(f"found a photo: {media_file}")
        photo = media_file
        break
```

Now let's build the endpoint to download the GPMF for the photo whose name we just found:

```python
url = GOPRO_BASE_URL + f"/gopro/media/gpmf?path=100GOPRO/{photo}"
```

Next we send the GET request and check the response for errors. Any errors will raise an exception.

```python
with requests.get(url, stream=True) as request:
    request.raise_for_status()
```

Lastly, we iterate through the binary content in 8 kB chunks, writing to a local file:

```python
file = photo.split(".")[0] + ".jpg"
with open(file, "wb") as f:
    logger.info(f"receiving binary stream to {file}...")
    for chunk in request.iter_content(chunk_size=8192):
        f.write(chunk)
```

This will log as such:

```console
INFO:root:found a photo: GOPR0987.JPG
INFO:root:Getting the GPMF for GOPR0987.JPG
INFO:root:Sending: http://10.5.5.9:8080/gopro/media/gpmf?path=100GOPRO/GOPR0987.JPG
INFO:root:receiving binary stream to GOPR0987.gpmf...
```

Once complete, the `GOPR0987.gpm`f file will be available from where the demo script was called.

## Get Media Screennail

The next command we will be sending is
[Get Media Screennail ]({% link specs/http.md %}#downloading-media).
Specifically, we will be getting the screennail for a photo. The camera must have at least one photo in its
media list in order for this to work.

{% note %}
There is a separate command (shown below) to get a media "thumbnbail"
{% endnote %}

First, we get the media list as in [Get Media List]({% link _python-tutorials/tutorial_7_camera_media_list.md %}#get-media-list) . Then we search through the list of file names in
the media list looking for a photo (i.e. a file whose name ends in **.jpg**). Once we find a photo, we
proceed:

```python
media_list = get_media_list()

photo: Optional[str] = None
for media_file in [x["n"] for x in media_list["media"][0]["fs"]]:
    if media_file.lower().endswith(".jpg"):
        logger.info(f"found a photo: {media_file}")
        photo = media_file
        break
```

Now let's build the endpoint to download the screennail for the photo whose name we just found:

```python
url = GOPRO_BASE_URL + f"/gopro/media/screennail?path=100GOPRO/{photo}"
```

Next we send the GET request and check the response for errors. Any errors will raise an exception.

```python
with requests.get(url, stream=True) as request:
    request.raise_for_status()
```

Lastly, we iterate through the binary content in 8 kB chunks, writing to a local file:

```python
file = photo.split(".")[0] + ".jpg"
with open(file, "wb") as f:
    logger.info(f"receiving binary stream to {file}...")
    for chunk in request.iter_content(chunk_size=8192):
        f.write(chunk)
```

This will log as such:

```console
INFO:root:found a photo: GOPR0987.JPG
INFO:root:Getting the screennail for GOPR0987.JPG
INFO:root:Sending: http://10.5.5.9:8080/gopro/media/screennail?path=100GOPRO/GOPR0987.JPG
INFO:root:receiving binary stream to GOPR0987_screennail.jpg...
```

Once complete, the `GOPR0987_screennail.jpg` file will be available from where the demo script was called.

## Get Media Thumbnail

The next command we will be sending is
[Get Media thumbnail ]({% link specs/http.md %}#downloading-media).
Specifically, we will be getting the thumbnail for a photo. The camera must have at least one photo in its
media list in order for this to work.

{% note %}
There is a separate command (shown above) to get a media "screennail"
{% endnote %}

First, we get the media list as in [Get Media List]({% link _python-tutorials/tutorial_7_camera_media_list.md %}#get-media-list) . Then we search through the list of file names in
the media list looking for a photo (i.e. a file whose name ends in **.jpg**). Once we find a photo, we
proceed:

```python
media_list = get_media_list()

photo: Optional[str] = None
for media_file in [x["n"] for x in media_list["media"][0]["fs"]]:
    if media_file.lower().endswith(".jpg"):
        logger.info(f"found a photo: {media_file}")
        photo = media_file
        break
```

Now let's build the endpoint to download the thumbnail for the photo whose name we just found:

```python
url = GOPRO_BASE_URL + f"/gopro/media/thumbnail?path=100GOPRO/{photo}"
```

Next we send the GET request and check the response for errors. Any errors will raise an exception.

```python
with requests.get(url, stream=True) as request:
    request.raise_for_status()
```

Lastly, we iterate through the binary content in 8 kB chunks, writing to a local file:

```python
file = photo.split(".")[0] + ".jpg"
with open(file, "wb") as f:
    logger.info(f"receiving binary stream to {file}...")
    for chunk in request.iter_content(chunk_size=8192):
        f.write(chunk)
```

This will log as such:

```console
INFO:root:found a photo: GOPR0987.JPG
INFO:root:Getting the thumbnail for GOPR0987.JPG
INFO:root:Sending: http://10.5.5.9:8080/gopro/media/thumbnail?path=100GOPRO/GOPR0987.JPG
INFO:root:receiving binary stream to GOPR0987_thumbnail.jpg...
```

Once complete, the `GOPR0987_thumbnail.jpg` file will be available from where the demo script was called.

# Troubleshooting

See the previous tutorial's [troubleshooting section]({% link _python-tutorials/tutorial_6_send_wifi_commands.md %}#troubleshooting).

# Good Job!

{% success %}
Congratulations 🤙
{% endsuccess %}

You can now query the GoPro's media list and retrieve binary information for media file. This is currently
last tutorial. Stay tuned for more 👍

At this point you should be able to start creating a useful example using the Open GoPro Interface. For some
inspiration check out some of the [demos]({% link demos.md %}).

