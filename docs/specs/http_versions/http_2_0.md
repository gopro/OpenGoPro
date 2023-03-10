---
title: 'HTTP Specification v2.0'
permalink: /http_2_0
classes: spec
redirect_from:
    - /http
---


# Overview

<p>
The GoPro API allows developers to create apps and utilities that interact with and control a GoPro camera.
</p>

## What can you do with the GoPro API?

<p>
The GoPro API allows you to control and query the camera:
<ul>
<li>Capture photo/video media</li>
<li>Get media list</li>
<li>Change settings</li>
<li>Get and set the date/time</li>
<li>Get camera status</li>
<li>Get media metadata (file size, width, height, duration, tags, etc)</li>
<li>and more!</li>
</ul>
</p>


# Supported Cameras

<p>
Below is a table of cameras that support GoPro's public HTTP API:
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Model ID</td>
      <td>Model Code</td>
      <td>Marketing Name</td>
      <td>Minimal Firmware Version</td>
    </tr>
    <tr>
      <td>60</td>
      <td>H22.03</td>
      <td>HERO11 Black Mini</td>
      <td><a href="https://gopro.com/en/us/update/hero11-black-mini">v01.10.00</a></td>
    </tr>
    <tr>
      <td>58</td>
      <td>H22.01</td>
      <td>HERO11 Black</td>
      <td><a href="https://gopro.com/en/us/update/hero11-black">v01.10.00</a></td>
    </tr>
    <tr>
      <td>57</td>
      <td>H21.01</td>
      <td>HERO10 Black</td>
      <td><a href="https://gopro.com/en/us/update/hero10-black">v01.10.00</a></td>
    </tr>
    <tr>
      <td>55</td>
      <td>HD9.01</td>
      <td>HERO9 Black</td>
      <td><a href="https://gopro.com/en/us/update/hero9-black">v01.70.00</a></td>
    </tr>
  </tbody>
</table>


# The Basics


## Connection
### WiFi
<p>
Connection to the camera via WiFi requires that the camera's WiFi Access Point be enabled.
This can be done by connecting to the camera via
<a href="https://gopro.github.io/OpenGoPro/ble">Bluetooth Low Energy (BLE)</a>
and sending the AP Control command: WIFI AP ON.
</p>

### USB
<p>
OpenGoPro systems that utilize USB must support the Network Control Model (NCM) protocol.
Connecting via USB requires the following steps:
<ol>
<li>Physically connect the camera's USB-C port to your system</li>
<li>Send HTTP command to enable wired USB control</li>
</ol>
</p>


## Authentication

### WiFi

<p>
Once the WiFi Access Point has been turned on, authentication with the camera simply requries connecting with the
correct SSID and password. This information can be obtained in two ways:

<ul>
<li>Put the camera into <a href="https://community.gopro.com/s/article/GoPro-Quik-How-To-Pair-Your-Camera?language=en_US">pairing mode</a> and tap the info button in the top-right corner of the screen.</li>
<li>Read the SSID/password directly via Bluetooth Low Energy. See <i>Services and Characteristics</i> seciton in <a href="https://gopro.github.io/OpenGoPro/ble">BLE Specification</a> for details.</li>
</ul>
</p>

### USB
<p>
No authentication is necessary.
</p>


## Socket Address

### WiFi
<p>
The socket address for WiFi connections is <b>10.5.5.9:8080</b>.
</p>

### USB
<p>
The socket address for USB connections is <b>172.2X.1YZ.51:8080</b> where:

<ul>
<li>X is the 100's digit from the camera serial number</li>
<li>Y is the 10's digit from the camera serial number</li>
<li>Z is the 1's digit from the camera serial number</li>
</ul>
</p>

<p>
The camera's serial number can be obtained in any of the following ways:
<ul>
<li>Reading the sticker inside the camera's battery enclosure</li>
<li>Camera UI: Preferences >> About >> Camera Info</li>
<li>Bluetooth Low Energy by reading directly from Hardware Info . See <i>Commands</i> in <a href="https://gopro.github.io/OpenGoPro/ble">BLE Specification</a> for details.</li>
</ul>
</p>

<p>
For example, if the camera's serial number is C0000123456<b>789</b>, the IP address for USB connections would be 172.2<b>7</b>.1<b>89</b>.51.
</p>

<p>
Alternatively, the IP address can be discovered via mDNS as the camera registers the <b>_gopro-web</b> service.
</p>


## Request and Response Formats
<p>
Most commands are sent via HTTP/GET and require no special headers.
Responses come in two parts: The standard HTTP return codes and JSON containing any additional information.
</p>

<p>
The typical use case is that the camera accepts a valid command, returns HTTP/200 (OK) and empty JSON 
(i.e. { }) and begins asynchronously working on the command.
If an error occurs, the camera will return a standard HTTP error code and JSON with helpful error/debug information.
</p>

<p>
Depending on the command sent, the camera can return JSON, binary, or Protobuf data. Some examples are listed below:
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Command</td>
      <td>Return Type</td>
    </tr>
    <tr>
      <td>Get Camera State</td>
      <td>JSON</td>
    </tr>
    <tr>
      <td>Get Media Info</td>
      <td>JSON</td>
    </tr>
    <tr>
      <td>Get Media <a href="https://gopro.github.io/gpmf-parser">GPMF</a></td>
      <td>Binary</td>
    </tr>
    <tr>
      <td>Get Media List</td>
      <td>JSON</td>
    </tr>
    <tr>
      <td>Get Media Screennail (JPEG)</td>
      <td>Binary</td>
    </tr>
    <tr>
      <td>Get Media Thumbnail (JPEG)</td>
      <td>Binary</td>
    </tr>
    <tr>
      <td>Get Presets</td>
      <td>JSON</td>
    </tr>
  </tbody>
</table>


## Sending Commands

<p>
Depending on the camera's state, it may not be ready to accept specific commands.
This ready state is dependent on the <b>System Busy</b> and the <b>Encoding Active</b> status flags. For example:

<ul>
<li>System Busy flag is set while loading presets, changing settings, formatting sdcard, ...</li>
<li>Encoding Active flag is set while capturing photo/video media</li>
</ul>
</p>

<p>
If the system is not ready, it should reject an incoming command; however, best practice is to always wait for the
System Busy and Encode Active flags to be unset before sending messages other than camera status queries.
For details regarding camera state, see <a href="#status-codes">Status Codes</a>.
</p>


## Keep Alive
<p>
In order to maximize battery life, GoPro cameras automatically go to sleep after some time.
This logic is handled by a combination of an <b>Auto Power Down</b> setting which most (but not all) cameras support
and a <b>Keep Alive</b> message that the user can regularly send to the camera.
The camera will automatically go to sleep if both timers reach zero.
</p>

<p>
The Auto Power Down timer is reset when the user taps the LCD screen, presses a button on the camera or 
programmatically (un)sets the shutter, sets a setting, or loads a Preset.
</p>

<p>
The Keep Alive timer is reset when the user sends a keep alive message.
</p>

<p>
The best practice to prevent the camera from inadvertently going to sleep is to start sending Keep Alive messages
every <b>3.0</b> seconds after a connection is established.
</p>

### Command
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>HTTP/GET</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>/gopro/camera/keep_alive</td>
      <td>Send keep-alive</td>
    </tr>
  </tbody>
</table>


# Commands
Using the Open GoPro API, a client can perform various command, control, and query operations!

## Commands Quick Reference
<p>
Below is a table of commands that can be sent to the camera and how to send them.<br />
<span style="color:green">✔</span> Indicates support for all Open GoPro firmware versions.<br />
<span style="color:red">❌</span> Indicates a lack of support for all Open GoPro firmware versions.<br />
>= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Command</td>
      <td>Description</td>
      <td>HTTP Method</td>
      <td>Endpoint</td>
      <td>HERO11 Black Mini</td>
      <td>HERO11 Black</td>
      <td>HERO10 Black</td>
      <td>HERO9 Black</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Analytics</td>
      <td>Set third party client</td>
      <td>GET</td>
      <td>/gopro/camera/analytics/set_client_info</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td>\&gt;= v01.70.00</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Camera: Get State</td>
      <td>Get camera state (status + settings)</td>
      <td>GET</td>
      <td>/gopro/camera/state</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Digital Zoom</td>
      <td>Digital zoom 50%</td>
      <td>GET</td>
      <td>/gopro/camera/digital_zoom?percent=50</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Get Date/Time</td>
      <td>Get date/time</td>
      <td>GET</td>
      <td>/gopro/camera/get_date_time</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td>\&gt;= v01.70.00</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Keep-alive</td>
      <td>Send keep-alive</td>
      <td>GET</td>
      <td>/gopro/camera/keep_alive</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: GPMF</td>
      <td>Get GPMF data (JPG)</td>
      <td>GET</td>
      <td>/gopro/media/gpmf?path=100GOPRO/XXX.JPG</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: GPMF</td>
      <td>Get GPMF data (MP4)</td>
      <td>GET</td>
      <td>/gopro/media/gpmf?path=100GOPRO/XXX.MP4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Media: HiLight (Add)</td>
      <td>Add hilight to 100GOPRO/xxx.JPG</td>
      <td>GET</td>
      <td>/gopro/media/hilight/file?path=100GOPRO/XXX.JPG</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td>\&gt;= v01.70.00</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Media: HiLight (Add)</td>
      <td>Add hilight to 100GOPRO/xxx.MP4 at offset 2500 ms</td>
      <td>GET</td>
      <td>/gopro/media/hilight/file?path=100GOPRO/XXX.MP4&ms=2500</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td>\&gt;= v01.70.00</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: HiLight (Remove)</td>
      <td>Remove hilight from 100GOPRO/xxx.JPG</td>
      <td>GET</td>
      <td>/gopro/media/hilight/remove?path=100GOPRO/XXX.JPG</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td>\&gt;= v01.70.00</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: HiLight (Remove)</td>
      <td>Remove hilight from 100GOPRO/xxx.MP4 at offset 2500ms</td>
      <td>GET</td>
      <td>/gopro/media/hilight/remove?path=100GOPRO/XXX.MP4&ms=2500</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td>\&gt;= v01.70.00</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Media: HiLight Moment</td>
      <td>Hilight moment during encoding</td>
      <td>GET</td>
      <td>/gopro/media/hilight/moment</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: Info</td>
      <td>Get media info (JPG)</td>
      <td>GET</td>
      <td>/gopro/media/info?path=100GOPRO/XXX.JPG</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: Info</td>
      <td>Get media info (MP4)</td>
      <td>GET</td>
      <td>/gopro/media/info?path=100GOPRO/XXX.MP4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Media: List</td>
      <td>Get media list</td>
      <td>GET</td>
      <td>/gopro/media/list</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: Screennail</td>
      <td>Get screennail for "100GOPRO/xxx.JPG"</td>
      <td>GET</td>
      <td>/gopro/media/screennail?path=100GOPRO/XXX.JPG</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: Screennail</td>
      <td>Get screennail for "100GOPRO/xxx.MP4"</td>
      <td>GET</td>
      <td>/gopro/media/screennail?path=100GOPRO/XXX.MP4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Media: Telemetry</td>
      <td>Get telemetry track data (JPG)</td>
      <td>GET</td>
      <td>/gopro/media/telemetry?path=100GOPRO/XXX.JPG</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Media: Telemetry</td>
      <td>Get telemetry track data (MP4)</td>
      <td>GET</td>
      <td>/gopro/media/telemetry?path=100GOPRO/XXX.MP4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: Thumbnail</td>
      <td>Get thumbnail for "100GOPRO/xxx.JPG"</td>
      <td>GET</td>
      <td>/gopro/media/thumbnail?path=100GOPRO/XXX.JPG</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Media: Thumbnail</td>
      <td>Get thumbnail for "100GOPRO/xxx.MP4"</td>
      <td>GET</td>
      <td>/gopro/media/thumbnail?path=100GOPRO/XXX.MP4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Media: Turbo Transfer</td>
      <td>Turbo transfer: off</td>
      <td>GET</td>
      <td>/gopro/media/turbo_transfer?p=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Media: Turbo Transfer</td>
      <td>Turbo transfer: on</td>
      <td>GET</td>
      <td>/gopro/media/turbo_transfer?p=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>OTA Update</td>
      <td>Soft update: upload 12345 bytes starting at offset 67890</td>
      <td>POST</td>
      <td>/gp/gpSoftUpdate (plus data)</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>OTA Update</td>
      <td>Soft update: mark upload complete</td>
      <td>POST</td>
      <td>/gp/gpSoftUpdate (plus data)</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>OTA Update</td>
      <td>Ota update: show canceled/failed ui on the camera</td>
      <td>GET</td>
      <td>/gp/gpSoftUpdate?request=canceled</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>OTA Update</td>
      <td>Ota update: delete cached update files</td>
      <td>GET</td>
      <td>/gp/gpSoftUpdate?request=delete</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>OTA Update</td>
      <td>Ota update: get current update state</td>
      <td>GET</td>
      <td>/gp/gpSoftUpdate?request=progress</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>OTA Update</td>
      <td>Ota update: display update ui on camera</td>
      <td>GET</td>
      <td>/gp/gpSoftUpdate?request=showui</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>OTA Update</td>
      <td>Ota update: initiate firmware update</td>
      <td>GET</td>
      <td>/gp/gpSoftUpdate?request=start</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Open GoPro</td>
      <td>Get version</td>
      <td>GET</td>
      <td>/gopro/version</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Presets: Get Status</td>
      <td>Get preset status</td>
      <td>GET</td>
      <td>/gopro/camera/presets/get</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Presets: Load</td>
      <td>Example <a href="#presets">preset id</a>: 0x1234ABCD</td>
      <td>GET</td>
      <td>/gopro/camera/presets/load?id=305441741</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Presets: Load Group</td>
      <td>Video</td>
      <td>GET</td>
      <td>/gopro/camera/presets/set_group?id=1000</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Presets: Load Group</td>
      <td>Photo</td>
      <td>GET</td>
      <td>/gopro/camera/presets/set_group?id=1001</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Presets: Load Group</td>
      <td>Timelapse</td>
      <td>GET</td>
      <td>/gopro/camera/presets/set_group?id=1002</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Set Camera Control Status</td>
      <td>Set camera control status to idle</td>
      <td>GET</td>
      <td>/gopro/camera/control/set_ui_controller?p=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.20.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Set Camera Control Status</td>
      <td>Set camera control status to external_control</td>
      <td>GET</td>
      <td>/gopro/camera/control/set_ui_controller?p=2</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.20.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Set Date/Time</td>
      <td>Set date/time to 2023-01-31 03:04:05</td>
      <td>GET</td>
      <td>/gopro/camera/set_date_time?date=2023_1_31&time=3_4_5</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td>\&gt;= v01.70.00</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Set Local Date/Time</td>
      <td>Set local date/time to: 2023-01-31 03:04:05 (utc-02:00)  (dst: on)</td>
      <td>GET</td>
      <td>/gopro/camera/set_date_time?date=2023_1_31&time=3_4_5&tzone=-120&dst=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Set shutter</td>
      <td>Shutter: on</td>
      <td>GET</td>
      <td>/gopro/camera/shutter/start</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Set shutter</td>
      <td>Shutter: off</td>
      <td>GET</td>
      <td>/gopro/camera/shutter/stop</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Stream: Start</td>
      <td>Start preview stream</td>
      <td>GET</td>
      <td>/gopro/camera/stream/start</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Stream: Stop</td>
      <td>Stop preview stream</td>
      <td>GET</td>
      <td>/gopro/camera/stream/stop</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Webcam: Exit</td>
      <td>Exit webcam mode</td>
      <td>GET</td>
      <td>/gopro/webcam/exit</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Webcam: Preview</td>
      <td>Start preview stream</td>
      <td>GET</td>
      <td>/gopro/webcam/preview</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Webcam: Start</td>
      <td>Start webcam</td>
      <td>GET</td>
      <td>/gopro/webcam/start</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.40.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Webcam: Start</td>
      <td>Start webcam</td>
      <td>GET</td>
      <td>/gopro/webcam/start?port=12345</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Webcam: Start</td>
      <td>Start webcam (res: resolution_1080, fov: wide)</td>
      <td>GET</td>
      <td>/gopro/webcam/start?res=12&fov=0</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Webcam: Status</td>
      <td>Get webcam status</td>
      <td>GET</td>
      <td>/gopro/webcam/status</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Webcam: Stop</td>
      <td>Stop webcam</td>
      <td>GET</td>
      <td>/gopro/webcam/stop</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>Webcam: Version</td>
      <td>Get webcam api version</td>
      <td>GET</td>
      <td>/gopro/webcam/version</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Wired USB Control</td>
      <td>Disable wired usb control</td>
      <td>GET</td>
      <td>/gopro/camera/control/wired_usb?p=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>Wired USB Control</td>
      <td>Enable wired usb control</td>
      <td>GET</td>
      <td>/gopro/camera/control/wired_usb?p=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
  </tbody>
</table>


# Settings
<p>
GoPro cameras have hundreds of setting options to choose from, all of which can be set using a single endpoint.
The endpoint is configured with a <b>setting id</b> and an <b>option value</b>.
Note that setting option values are not globally unique.
While most option values are enumerated values, some are complex bitmasked values.
</p>

## Settings Quick Reference
<p>
Below is a table of setting options detailing how to set every option supported by Open GoPro cameras.<br />
<span style="color:green">✔</span> Indicates support for all Open GoPro firmware versions.<br />
<span style="color:red">❌</span> Indicates a lack of support for all Open GoPro firmware versions.<br />
>= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Setting ID</td>
      <td>Setting</td>
      <td>Option</td>
      <td>HTTP Method</td>
      <td>Endpoint</td>
      <td>HERO11 Black Mini</td>
      <td>HERO11 Black</td>
      <td>HERO10 Black</td>
      <td>HERO9 Black</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 4k (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 2.7k (id: 4)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 2.7k 4:3 (id: 6)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=6</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 1440 (id: 7)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=7</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 1080 (id: 9)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=9</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 4k 4:3 (id: 18)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=18</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5k (id: 24)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=24</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5k 4:3 (id: 25)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=25</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5.3k 8:7 (id: 26)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=26</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5.3k 4:3 (id: 27)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=27</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 4k 8:7 (id: 28)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=28</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5.3k (id: 100)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=2&option=100</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 240 (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 120 (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 100 (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=2</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 60 (id: 5)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=5</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 50 (id: 6)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=6</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 30 (id: 8)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=8</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 25 (id: 9)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=9</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 24 (id: 10)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=10</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 200 (id: 13)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=3&option=13</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>43</td>
      <td>Webcam Digital Lenses</td>
      <td>Set webcam digital lenses (id: 43) to wide (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=43&option=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>43</td>
      <td>Webcam Digital Lenses</td>
      <td>Set webcam digital lenses (id: 43) to narrow (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=43&option=2</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>43</td>
      <td>Webcam Digital Lenses</td>
      <td>Set webcam digital lenses (id: 43) to superview (id: 3)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=43&option=3</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>43</td>
      <td>Webcam Digital Lenses</td>
      <td>Set webcam digital lenses (id: 43) to linear (id: 4)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=43&option=4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to never (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=59&option=0</td>
      <td>\&gt;= v02.10.00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 1 min (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=59&option=1</td>
      <td>\&gt;= v02.10.00</td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 5 min (id: 4)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=59&option=4</td>
      <td>\&gt;= v02.10.00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 15 min (id: 6)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=59&option=6</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 30 min (id: 7)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=59&option=7</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 8 seconds (id: 11)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=59&option=11</td>
      <td>\&gt;= v02.10.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 30 seconds (id: 12)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=59&option=12</td>
      <td>\&gt;= v02.10.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to wide (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=121&option=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to narrow (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=121&option=2</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to superview (id: 3)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=121&option=3</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to linear (id: 4)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=121&option=4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to max superview (id: 7)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=121&option=7</td>
      <td>\&gt;= v02.00.00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to linear + horizon leveling (id: 8)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=121&option=8</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to hyperview (id: 9)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=121&option=9</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to linear + horizon lock (id: 10)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=121&option=10</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>122</td>
      <td>Photo Digital Lenses</td>
      <td>Set photo digital lenses (id: 122) to narrow (id: 19)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=122&option=19</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>122</td>
      <td>Photo Digital Lenses</td>
      <td>Set photo digital lenses (id: 122) to max superview (id: 100)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=122&option=100</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>122</td>
      <td>Photo Digital Lenses</td>
      <td>Set photo digital lenses (id: 122) to wide (id: 101)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=122&option=101</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>122</td>
      <td>Photo Digital Lenses</td>
      <td>Set photo digital lenses (id: 122) to linear (id: 102)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=122&option=102</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>123</td>
      <td>Time Lapse Digital Lenses</td>
      <td>Set time lapse digital lenses (id: 123) to narrow (id: 19)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=123&option=19</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>123</td>
      <td>Time Lapse Digital Lenses</td>
      <td>Set time lapse digital lenses (id: 123) to max superview (id: 100)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=123&option=100</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>123</td>
      <td>Time Lapse Digital Lenses</td>
      <td>Set time lapse digital lenses (id: 123) to wide (id: 101)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=123&option=101</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>123</td>
      <td>Time Lapse Digital Lenses</td>
      <td>Set time lapse digital lenses (id: 123) to linear (id: 102)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=123&option=102</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>128</td>
      <td>Media Format</td>
      <td>Set media format (id: 128) to time lapse video (id: 13)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=128&option=13</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>128</td>
      <td>Media Format</td>
      <td>Set media format (id: 128) to time lapse photo (id: 20)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=128&option=20</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>128</td>
      <td>Media Format</td>
      <td>Set media format (id: 128) to night lapse photo (id: 21)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=128&option=21</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>128</td>
      <td>Media Format</td>
      <td>Set media format (id: 128) to night lapse video (id: 26)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=128&option=26</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>134</td>
      <td>Anti-Flicker</td>
      <td>Set setup anti flicker (id: 134) to 60hz (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=134&option=2</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>134</td>
      <td>Anti-Flicker</td>
      <td>Set setup anti flicker (id: 134) to 50hz (id: 3)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=134&option=3</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to off (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=135&option=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to on (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=135&option=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to high (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=135&option=2</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to boost (id: 3)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=135&option=3</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to auto boost (id: 4)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=135&option=4</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to standard (id: 100)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=135&option=100</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>150</td>
      <td>Horizon Leveling</td>
      <td>Set video horizon levelling (id: 150) to off (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=150&option=0</td>
      <td>\&gt;= v02.00.00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>150</td>
      <td>Horizon Leveling</td>
      <td>Set video horizon levelling (id: 150) to on (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=150&option=1</td>
      <td>\&gt;= v02.00.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>150</td>
      <td>Horizon Leveling</td>
      <td>Set video horizon levelling (id: 150) to locked (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=150&option=2</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>151</td>
      <td>Horizon Leveling</td>
      <td>Set photo horizon levelling (id: 151) to off (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=151&option=0</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>151</td>
      <td>Horizon Leveling</td>
      <td>Set photo horizon levelling (id: 151) to locked (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=151&option=2</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>162</td>
      <td>Max Lens</td>
      <td>Set max lens (id: 162) to off (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=162&option=0</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.20.00</td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>162</td>
      <td>Max Lens</td>
      <td>Set max lens (id: 162) to on (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=162&option=1</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.20.00</td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>173</td>
      <td>Video Performance Mode</td>
      <td>Set video performance mode (id: 173) to maximum video performance (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=173&option=0</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v01.16.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>173</td>
      <td>Video Performance Mode</td>
      <td>Set video performance mode (id: 173) to extended battery (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=173&option=1</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v01.16.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>173</td>
      <td>Video Performance Mode</td>
      <td>Set video performance mode (id: 173) to tripod / stationary video (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=173&option=2</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v01.16.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>175</td>
      <td>Controls</td>
      <td>Set controls (id: 175) to easy (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=175&option=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>175</td>
      <td>Controls</td>
      <td>Set controls (id: 175) to pro (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=175&option=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=0</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=1</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=2</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (low light) (id: 3)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=3</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (ext. batt) (id: 4)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=4</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (ext. batt) (id: 5)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=5</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (ext. batt, low light) (id: 6)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=6</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (50hz) (id: 7)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=7</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (50hz) (id: 8)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=8</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (50hz) (id: 9)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=9</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (low light, 50hz) (id: 10)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=10</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (ext. batt, 50hz) (id: 11)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=11</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (ext. batt, 50hz) (id: 12)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=12</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (ext. batt, low light, 50hz) (id: 13)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=13</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (ext. batt) (id: 14)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=14</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (ext. batt, 50hz) (id: 15)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=15</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (long. batt) (id: 16)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=16</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (long. batt) (id: 17)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=17</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (long. batt) (id: 18)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=18</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (long. batt, low light) (id: 19)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=19</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (long. batt, 50hz) (id: 20)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=20</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (long. batt, 50hz) (id: 21)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=21</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (long. batt, 50hz) (id: 22)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=22</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (long. batt, low light, 50hz) (id: 23)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=23</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (4k) (id: 24)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=24</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (2.7k) (id: 25)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=25</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (4k, 50hz) (id: 26)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=26</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (2.7k, 50hz) (id: 27)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=176&option=27</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>177</td>
      <td>Enable Night Photo</td>
      <td>Set enable night photo (id: 177) to off (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=177&option=0</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>177</td>
      <td>Enable Night Photo</td>
      <td>Set enable night photo (id: 177) to on (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=177&option=1</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>178</td>
      <td>Wireless Band</td>
      <td>Set wireless band (id: 178) to 2.4ghz (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=178&option=0</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>178</td>
      <td>Wireless Band</td>
      <td>Set wireless band (id: 178) to 5ghz (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=178&option=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>179</td>
      <td>Trail Length</td>
      <td>Set trail length (id: 179) to short (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=179&option=1</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>179</td>
      <td>Trail Length</td>
      <td>Set trail length (id: 179) to long (id: 2)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=179&option=2</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>179</td>
      <td>Trail Length</td>
      <td>Set trail length (id: 179) to max (id: 3)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=179&option=3</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>180</td>
      <td>Video Mode</td>
      <td>Set video mode (id: 180) to highest quality (id: 0)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=180&option=0</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>180</td>
      <td>Video Mode</td>
      <td>Set video mode (id: 180) to extended battery (id: 1)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=180&option=1</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>180</td>
      <td>Video Mode</td>
      <td>Set video mode (id: 180) to extended battery (green icon) (id: 101)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=180&option=101</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>180</td>
      <td>Video Mode</td>
      <td>Set video mode (id: 180) to longest battery (green icon) (id: 102)</td>
      <td>GET</td>
      <td>/gopro/camera/setting?setting=180&option=102</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
  </tbody>
</table>


## Camera Capabilities
<p>
Camera capabilities usually change from one camera to another and often change from one release to the next.
Below are documents that detail whitelists for basic video settings for every supported camera release.
</p>

### Note about Dependency Ordering and Blacklisting
<p>
Capability documents define supported camera states.
Each state is comprised of a set of setting options that are presented in <b>dependency order</b>.
This means each state is guaranteed to be attainable if and only if the setting options are set in the order presented.
Failure to adhere to dependency ordering may result in the camera's blacklist rules rejecting a set-setting command.
</p>

### Example
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Camera</td>
      <td>Command 1</td>
      <td>Command 2</td>
      <td>Command 3</td>
      <td>Command 4</td>
      <td>Command 5</td>
      <td>Guaranteed Valid?</td>
    </tr>
    <tr>
      <td>HERO10 Black</td>
      <td>Res: 1080</td>
      <td>Anti-Flicker: 60Hz (NTSC)</td>
      <td>FPS: 240</td>
      <td>FOV: Wide</td>
      <td>Hypersmooth: OFF</td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>HERO10 Black</td>
      <td>FPS: 240</td>
      <td>Anti-Flicker: 60Hz (NTSC)</td>
      <td>Res: 1080</td>
      <td>FOV: Wide</td>
      <td>Hypersmooth: OFF</td>
      <td><span style="color:red">❌</span></td>
    </tr>
  </tbody>
</table>
<p>
In the example above, the first set of commands will always work for basic video presets such as Standard.
</p>

<p>
In the second example, suppose the camera's Video Resolution was previously set to 4K.
If the user tries to set Video FPS to 240, it will fail because 4K/240fps is not supported.
</p>

### Capability Documents
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Documents</td>
      <td>Product</td>
      <td>Release</td>
    </tr>
    <tr>
      <td rowspan="17"><a href="https://github.com/gopro/OpenGoPro/blob/main/docs/specs/capabilities.xlsx">capabilities.xlsx</a><br /><a href="https://github.com/gopro/OpenGoPro/blob/main/docs/specs/capabilities.json">capabilities.json</a></td>
      <td rowspan="3">HERO11 Black Mini</td>
      <td>v02.10.00</td>
    </tr>
    <tr>
      <td>v02.00.00</td>
    </tr>
    <tr>
      <td>v01.10.00</td>
    </tr>
    <tr>
      <td rowspan="4">HERO11 Black</td>
      <td>v02.01.00</td>
    </tr>
    <tr>
      <td>v01.20.00</td>
    </tr>
    <tr>
      <td>v01.12.00</td>
    </tr>
    <tr>
      <td>v01.10.00</td>
    </tr>
    <tr>
      <td rowspan="8">HERO10 Black</td>
      <td>v01.50.00</td>
    </tr>
    <tr>
      <td>v01.46.00</td>
    </tr>
    <tr>
      <td>v01.42.00</td>
    </tr>
    <tr>
      <td>v01.40.00</td>
    </tr>
    <tr>
      <td>v01.30.00</td>
    </tr>
    <tr>
      <td>v01.20.00</td>
    </tr>
    <tr>
      <td>v01.16.00</td>
    </tr>
    <tr>
      <td>v01.10.00</td>
    </tr>
    <tr>
      <td rowspan="2">HERO9 Black</td>
      <td>v01.72.00</td>
    </tr>
    <tr>
      <td>v01.70.00</td>
    </tr>
  </tbody>
</table>

### Spreadsheet Format
<p>
The capabilities spreadsheet contains worksheets for every supported release.
Each row in a worksheet represents a whitelisted state and is presented in dependency order as outlined above.
</p>

### JSON Format
<p>
The capabilities JSON contains a set of whitelist states for every supported release.
Each state is comprised of a list of objects that contain setting and option IDs necessary to construct set-setting
commands and are given in dependency order as outlined above.
</p>

<p>
Below is a simplified example of the capabilities JSON file; a formal schema is also available here:
<a href="https://github.com/gopro/OpenGoPro/blob/main/docs/specs/capabilities_schema.json">capabilities_schema.json</a>
</p>

```
{
    "(PRODUCT_NAME)": {
        "(RELEASE_VERSION)": {
            "states": [
                [
                    {"setting_name": "(str)", "setting_id": (int), "option_name": "(str)", "option_id": (int)},
                    ...
                ],
                ...
            ],
        },
        ...
    },
    ...
}
```


# Media
<p>
The camera provides an endpoint to query basic details about media captured on the sdcard.
</p>


## Chapters
<p>
All GoPro cameras break longer videos into chapters.
GoPro cameras currently limit file sizes on sdcards to 4GB for both FAT32 and exFAT file systems.
This limitation is most commonly seen when recording longer (10+ minute) videos.
In practice, the camera will split video media into chapters named Gqccmmmm.MP4 (and ones for THM/LRV) such that:
</p>

<ul>
<li>q: Quality Level (X: Extreme, H: High, M: Medium, L: Low)</li>
<li>cc: Chapter Number (01-99)</li>
<li>mmmm: Media ID (0001-9999)</li>
</ul>

<p>
When media becomes chaptered, the camera increments subsequent Chapter Numbers while leaving the Media ID unchanged.
For example, if the user records a long High-quality video that results in 4 chapters, the files on the sdcard may
look like the following:
</p>

```
-rwxrwxrwx@ 1 gopro  123456789  4006413091 Jan  1 00:00 GH010078.MP4
-rwxrwxrwx@ 1 gopro  123456789       17663 Jan  1 00:00 GH010078.THM
-rwxrwxrwx@ 1 gopro  123456789  4006001541 Jan  1 00:00 GH020078.MP4
-rwxrwxrwx@ 1 gopro  123456789       17357 Jan  1 00:00 GH020078.THM
-rwxrwxrwx@ 1 gopro  123456789  4006041985 Jan  1 00:00 GH030078.MP4
-rwxrwxrwx@ 1 gopro  123456789       17204 Jan  1 00:00 GH030078.THM
-rwxrwxrwx@ 1 gopro  123456789   756706872 Jan  1 00:00 GH040078.MP4
-rwxrwxrwx@ 1 gopro  123456789       17420 Jan  1 00:00 GH040078.THM
-rwxrwxrwx@ 1 gopro  123456789   184526939 Jan  1 00:00 GL010078.LRV
-rwxrwxrwx@ 1 gopro  123456789   184519787 Jan  1 00:00 GL020078.LRV
-rwxrwxrwx@ 1 gopro  123456789   184517614 Jan  1 00:00 GL030078.LRV
-rwxrwxrwx@ 1 gopro  123456789    34877660 Jan  1 00:00 GL040078.LRV
```


## Media List Format
<p>
The format of the media list is given below.
</p>

```
{
    "id": "<MEDIA SESSION ID>",
    "media": [
        {
            "d": "<DIRECTORY NAME>",
            "fs": [
                {<MEDIA ITEM INFO>},
                ...
            ]
        },
        ...
    ]
}
```

### Media List Keys
The outer structure of the media list and the inner structure of individual media items use the keys in the table below.
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Key</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>b</td>
      <td>ID of first member of a group (for grouped media items)</td>
    </tr>
    <tr>
      <td>d</td>
      <td>Directory name</td>
    </tr>
    <tr>
      <td>fs</td>
      <td>File system. Contains listing of media items in directory</td>
    </tr>
    <tr>
      <td>g</td>
      <td>Group ID (if grouped media item)</td>
    </tr>
    <tr>
      <td>glrv</td>
      <td>Low resolution video file size</td>
    </tr>
    <tr>
      <td>id</td>
      <td>Media list session identifier</td>
    </tr>
    <tr>
      <td>l</td>
      <td>ID of last member of a group (for grouped media items)</td>
    </tr>
    <tr>
      <td>m</td>
      <td>List of missing/deleted group member IDs (for grouped media items)</td>
    </tr>
    <tr>
      <td>media</td>
      <td>Contains media info for for each directory (e.g. 100GOPRO/, 101GOPRO/, ...)</td>
    </tr>
    <tr>
      <td>mod</td>
      <td>Last modified time (seconds since epoch)</td>
    </tr>
    <tr>
      <td>n</td>
      <td>Media filename</td>
    </tr>
    <tr>
      <td>s</td>
      <td>Size of (group) media in bytes</td>
    </tr>
    <tr>
      <td>t</td>
      <td>Group type (for grouped media items) (b -> burst, c -> continuous shot, n -> night lapse, t -> time lapse)</td>
    </tr>
  </tbody>
</table>

### Grouped Media Items
<p>
In order to minimize the size of the JSON transmitted by the camera, grouped media items such as Burst Photos,
Time Lapse Photos, Night Lapse Photos, etc are represented with a single item in the media list with additional keys
that allow the user to extrapolate individual filenames for each member of the group.
</p>

<p>
Filenames for group media items have the form "GXXXYYYY.ZZZ"
where XXX is the group ID, YYY is the group member ID and ZZZ is the file extension.
</p>

<p>
For example, take the media list below, which contains a Time Lapse Photo group media item:
</p>

```
{
    "id": "2530266050123724003",
    "media": [
        {
            "d": "100GOPRO",
            "fs": [
                {
                    "b": "8",
                    "cre": "1613669353",
                    "g": "1",
                    "l": "396",
                    "m": ['75', '139'],
                    "mod": "1613669353",
                    "n": "G0010008.JPG",
                    "s": "773977407",
                    "t": "t"
                }
            ]
        }
    ]
}
```

<p>
The first filename in the group is "G0010008.JPG" (key: "n").<br/>
The ID of the first group member in this case is "008" (key: "b").<br/>
The ID of the last group member in this case is "396" (key: "l").<br/>
The IDs of deleted members in this case are "75" and "139" (key: "m")<br/>
Given this information, the user can extrapolate that the group currently contains
</p>

<p>
G0010008.JPG, G0010009.JPG, G0010010.JPG,<br/>
...,<br/>
G0010074.JPG, G0010076.JPG,<br/>
...,<br/>
G0010138.JPG, G0010140.JPG,<br/>
...,<br/>
G0010394.JPG, G0010395.JPG. G0010396.JPG<br/>
</p>



## Media HiLights
<p>
The <a href="https://community.gopro.com/t5/en/What-Is-HiLight-Tagging-amp-How-Does-It-Work/ta-p/390286">HiLight Tags</a> feature allows the user to tag moments of interest either during video
capture or on existing media.
</p>

### Add/Remove HiLights
<p>
Below is a table of all HiLight commands.
For details on how to send HiLight commands, see <a href="#commands-quick-reference">Commands Quick Reference</a>.

</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Command</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>Media: HiLight (Add)</td>
      <td>Video: Add a tag at a specific time offset (ms)<br/>Photo: Add a tag</td>
    </tr>
    <tr>
      <td>Media: HiLight (Remove)</td>
      <td>Video: Remove a tag at a specific time offset (ms)<br/>Photo: Remove tag</td>
    </tr>
    <tr>
      <td>Media: HiLight Moment</td>
      <td>Add a tag to the current time offset (ms) while encoding video</td>
    </tr>
  </tbody>
</table>

<p>
Note: Attempting to add a HiLight tag at a time offset that exceeds the duration of the video
or removing a non-existent HiLight tag will result in an HTTP/500 error.
</p>

### Get HiLights
<p>
Once HiLight tags have been added, they can be queried by calling the <a href="#commands-quick-reference">Media: Info</a> command;
the response content will be JSON that contains HiLight information:
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Media Type</td>
      <td>Key</td>
      <td>Value</td>
    </tr>
    <tr>
      <td>Photo</td>
      <td>hc</td>
      <td>HiLight Count</td>
    </tr>
    <tr>
      <td>Video</td>
      <td>hc</td>
      <td>HiLight Count</td>
    </tr>
    <tr>
      <td>Video</td>
      <td>hi</td>
      <td>HiLights (list of time offsets in ms)</td>
    </tr>
  </tbody>
</table>

#### Example
<p>
The JSON sample below shows media that contains three HiLights at time offsets 2502ms, 5839ms, and 11478ms.
Note: Photo info will not have an "hi":[...] key-value pair.
</p>

```
{
  ...,
  "hc":"3",
  "hi":[2502,5839,11478],
  ...,
}
```


## Downloading Media
<p>
The URL to download/stream media from the DCIM/ directory on the sdcard is the Base URL plus <i>/videos/DCIM/XXX/YYY</i>
where XXX is the directory name within DCIM/ given by the media list and YYY is the target media filename.
</p>

<p>
For example: Given the following media list:
</p>

```
{
    "id": "3586667939918700960",
    "media": [
        {
            "d": "100GOPRO",
            "fs": [
                {
                    "n": "GH010397.MP4",
                    "cre": "1613672729",
                    "mod": "1613672729",
                    "glrv": "1895626",
                    "ls": "-1",
                    "s": "19917136"
                },
                {
                    "cre": "1614340213",
                    "mod": "1614340213",
                    "n": "GOPR0001.JPG",
                    "s": "6961371"
                }
            ]
        }
    ]
}
```

<p>
The URL to download GH010397.MP4 over WiFi would be
<a href="http://10.5.5.9:8080/videos/DCIM/100GOPRO/GH010397.MP4">http://10.5.5.9:8080/videos/DCIM/100GOPRO/GH010397.MP4</a>
</p>

<p>
The URL to download GOPR0001.JPG over WiFi would be
<a href="http://10.5.5.9:8080/videos/DCIM/100GOPRO/GOPR0001.JPG">http://10.5.5.9:8080/videos/DCIM/100GOPRO/GOPR0001.JPG</a>
</p>


## Turbo Transfer
<p>
Some cameras support Turbo Transfer mode, which allows media to be downloaded over WiFi more rapidly.
This special mode should only be used during media offload.
It is recommended that the user check for and--if necessary--disable Turbo Transfer on connect.
For details on which cameras are supported and how to enable and disable Turbo Transfer, see
<a href="#commands-quick-reference">Commands Quick Reference</a>.
</p>


## Downloading Preview Stream
<p>
When the preview stream is started, the camera starts up a UDP client and begins writing MPEG Transport Stream
data to the connected client on port 8554.
In order to stream and save this data, the user can implement a UDP server that binds to the same port and appends
datagrams to a file when they are received.
</p>


# Camera State
<p>
The camera provides multiple types of state, all of which can be queried:
</p>

<ul>
<li>Camera state: Contains information about camera status (photos taken, date, is-camera-encoding, etc) and settings (current video resolution, current frame rate, etc)</li>
<li>Preset State: How presets are arranged into preset groups, their titles, icons, settings closely associated with each preset, etc</li>
</ul>


## Camera State Format
Camera state is given in the following form:

```
{
    "status": {
        "1": <status 1 value>,
        "2": <status 2 value>,
        ...
    },
    "settings: {
        "2": <setting 2 value>,
        "3": <setting 3 value>,
        ...
    }
}
```

<p>
Where <b>status X value</b> and <b>setting X value</b> are almost always integer values.
See Status Codes table in this document for exceptions.
</p>

<p>
For status, keys are status codes and values are status values.
</p>

<p>
For settings, keys are setting IDs, and values are option values
</p>


## Status IDs
<p>
Below is a table of supported status IDs.<br />
<span style="color:green">✔</span> Indicates support for all Open GoPro firmware versions.<br />
<span style="color:red">❌</span> Indicates a lack of support for all Open GoPro firmware versions.<br />
>= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Status ID</td>
      <td>Name</td>
      <td>Description</td>
      <td>Type</td>
      <td>Values</td>
      <td>HERO11 Black Mini</td>
      <td>HERO11 Black</td>
      <td>HERO10 Black</td>
      <td>HERO9 Black</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Internal battery present</td>
      <td>Is the system's internal battery present?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>2</td>
      <td>Internal battery level</td>
      <td>Rough approximation of internal battery level in bars</td>
      <td>integer</td>
      <td>0: Zero<br />1: One<br />2: Two<br />3: Three<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>6</td>
      <td>System hot</td>
      <td>Is the system currently overheating?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>8</td>
      <td>System busy</td>
      <td>Is the camera busy?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>9</td>
      <td>Quick capture active</td>
      <td>Is Quick Capture feature enabled?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>10</td>
      <td>Encoding active</td>
      <td>Is the system encoding right now?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>11</td>
      <td>Lcd lock active</td>
      <td>Is LCD lock active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>13</td>
      <td>Video progress counter</td>
      <td>When encoding video, this is the duration (seconds) of the video so far; 0 otherwise</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>17</td>
      <td>Enable</td>
      <td>Are Wireless Connections enabled?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>19</td>
      <td>State</td>
      <td>The pairing state of the camera</td>
      <td>integer</td>
      <td>0: Never Started<br />1: Started<br />2: Aborted<br />3: Cancelled<br />4: Completed<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>20</td>
      <td>Type</td>
      <td>The last type of pairing that the camera was engaged in</td>
      <td>integer</td>
      <td>0: Not Pairing<br />1: Pairing App<br />2: Pairing Remote Control<br />3: Pairing Bluetooth Device<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>21</td>
      <td>Pair time</td>
      <td>Time (milliseconds) since boot of last successful pairing complete action</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>22</td>
      <td>State</td>
      <td>State of current scan for WiFi Access Points. Appears to only change for CAH-related scans</td>
      <td>integer</td>
      <td>0: Never started<br />1: Started<br />2: Aborted<br />3: Canceled<br />4: Completed<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>23</td>
      <td>Scan time msec</td>
      <td>The time, in milliseconds since boot that the WiFi Access Point scan completed</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>24</td>
      <td>Provision status</td>
      <td>WiFi AP provisioning state</td>
      <td>integer</td>
      <td>0: Never started<br />1: Started<br />2: Aborted<br />3: Canceled<br />4: Completed<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>26</td>
      <td>Remote control version</td>
      <td>Wireless remote control version</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>27</td>
      <td>Remote control connected</td>
      <td>Is a wireless remote control connected?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>28</td>
      <td>Pairing</td>
      <td>Wireless Pairing State</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>29</td>
      <td>Wlan ssid</td>
      <td>Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int</td>
      <td>string</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>30</td>
      <td>Ap ssid</td>
      <td>Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int</td>
      <td>string</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>31</td>
      <td>App count</td>
      <td>The number of wireless devices connected to the camera</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>32</td>
      <td>Enable</td>
      <td>Is Preview Stream enabled?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>33</td>
      <td>Sd status</td>
      <td>Primary Storage Status</td>
      <td>integer</td>
      <td>-1: Unknown<br />0: OK<br />1: SD Card Full<br />2: SD Card Removed<br />3: SD Card Format Error<br />4: SD Card Busy<br />8: SD Card Swapped<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>34</td>
      <td>Remaining photos</td>
      <td>How many photos can be taken before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>35</td>
      <td>Remaining video time</td>
      <td>How many minutes of video can be captured with current settings before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>36</td>
      <td>Num group photos</td>
      <td>How many group photos can be taken with current settings before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>37</td>
      <td>Num group videos</td>
      <td>Total number of group videos on sdcard</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>38</td>
      <td>Num total photos</td>
      <td>Total number of photos on sdcard</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>39</td>
      <td>Num total videos</td>
      <td>Total number of videos on sdcard</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>41</td>
      <td>Ota status</td>
      <td>The current status of Over The Air (OTA) update</td>
      <td>integer</td>
      <td>0: Idle<br />1: Downloading<br />2: Verifying<br />3: Download Failed<br />4: Verify Failed<br />5: Ready<br />6: GoPro App: Downloading<br />7: GoPro App: Verifying<br />8: GoPro App: Download Failed<br />9: GoPro App: Verify Failed<br />10: GoPro App: Ready<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>42</td>
      <td>Download cancel request pending</td>
      <td>Is there a pending request to cancel a firmware update download?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>45</td>
      <td>Camera locate active</td>
      <td>Is locate camera feature active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>49</td>
      <td>Multi shot count down</td>
      <td>The current timelapse interval countdown value (e.g. 5...4...3...2...1...)</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>54</td>
      <td>Remaining space</td>
      <td>Remaining space on the sdcard in Kilobytes</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>55</td>
      <td>Supported</td>
      <td>Is preview stream supported in current recording/mode/secondary-stream?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>56</td>
      <td>Wifi bars</td>
      <td>WiFi signal strength in bars</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>58</td>
      <td>Num hilights</td>
      <td>The number of hilights in encoding video (set to 0 when encoding stops)</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>59</td>
      <td>Last hilight time msec</td>
      <td>Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>60</td>
      <td>Next poll msec</td>
      <td>The min time between camera status updates (msec). Do not poll for status more often than this</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>64</td>
      <td>Remaining timelapse time</td>
      <td>How many min of Timelapse video can be captured with current settings before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>65</td>
      <td>Exposure select type</td>
      <td>Liveview Exposure Select Mode</td>
      <td>integer</td>
      <td>0: Disabled<br />1: Auto<br />2: ISO Lock<br />3: Hemisphere<br /></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>66</td>
      <td>Exposure select x</td>
      <td>Liveview Exposure Select: y-coordinate (percent)</td>
      <td>percent</td>
      <td>0-100</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>67</td>
      <td>Exposure select y</td>
      <td>Liveview Exposure Select: y-coordinate (percent)</td>
      <td>percent</td>
      <td>0-100</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>68</td>
      <td>Gps status</td>
      <td>Does the camera currently have a GPS lock?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>69</td>
      <td>Ap state</td>
      <td>Is the WiFi radio enabled?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>70</td>
      <td>Internal battery percentage</td>
      <td>Internal battery level (percent)</td>
      <td>percent</td>
      <td>0-100</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>74</td>
      <td>Acc mic status</td>
      <td>Microphone Accesstory status</td>
      <td>integer</td>
      <td>0: Microphone mod not connected<br />1: Microphone mod connected<br />2: Microphone mod connected and microphone plugged into Microphone mod<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>75</td>
      <td>Digital zoom</td>
      <td>Digital Zoom level (percent)</td>
      <td>percent</td>
      <td>0-100</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>76</td>
      <td>Wireless band</td>
      <td>Wireless Band</td>
      <td>integer</td>
      <td>0: 2.4 GHz<br />1: 5 GHz<br />2: Max<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>77</td>
      <td>Digital zoom active</td>
      <td>Is Digital Zoom feature available?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>78</td>
      <td>Mobile friendly video</td>
      <td>Are current video settings mobile friendly? (related to video compression and frame rate)</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>79</td>
      <td>First time use</td>
      <td>Is the camera currently in First Time Use (FTU) UI flow?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>81</td>
      <td>Band 5ghz avail</td>
      <td>Is 5GHz wireless band available?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>82</td>
      <td>System ready</td>
      <td>Is the system ready to accept commands?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>83</td>
      <td>Batt okay for ota</td>
      <td>Is the internal battery charged sufficiently to start Over The Air (OTA) update?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>85</td>
      <td>Video low temp alert</td>
      <td>Is the camera getting too cold to continue recording?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>86</td>
      <td>Actual orientation</td>
      <td>The rotational orientation of the camera</td>
      <td>integer</td>
      <td>0: 0 degrees (upright)<br />1: 180 degrees (upside down)<br />2: 90 degrees (laying on right side)<br />3: 270 degrees (laying on left side)<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>88</td>
      <td>Zoom while encoding</td>
      <td>Is this camera capable of zooming while encoding (static value based on model, not settings)</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>89</td>
      <td>Current mode</td>
      <td>Current flatmode ID</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>93</td>
      <td>Active video presets</td>
      <td>Current Video Preset (ID)</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>94</td>
      <td>Active photo presets</td>
      <td>Current Photo Preset (ID)</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>95</td>
      <td>Active timelapse presets</td>
      <td>Current Timelapse Preset (ID)</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>96</td>
      <td>Active presets group</td>
      <td>Current Preset Group (ID)</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>97</td>
      <td>Active preset</td>
      <td>Current Preset (ID)</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>98</td>
      <td>Preset modified</td>
      <td>Preset Modified Status, which contains an event ID and a preset (group) ID</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>99</td>
      <td>Remaining live bursts</td>
      <td>How many Live Bursts can be captured before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>100</td>
      <td>Num total live bursts</td>
      <td>Total number of Live Bursts on sdcard</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>101</td>
      <td>Capture delay active</td>
      <td>Is Capture Delay currently active (i.e. counting down)?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>102</td>
      <td>Media mod mic status</td>
      <td>Media mod State</td>
      <td>integer</td>
      <td>0: Media mod microphone removed<br />2: Media mod microphone only<br />3: Media mod microphone with external microphone<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>103</td>
      <td>Timewarp speed ramp active</td>
      <td>Time Warp Speed</td>
      <td>integer</td>
      <td>0: 15x<br />1: 30x<br />2: 60x<br />3: 150x<br />4: 300x<br />5: 900x<br />6: 1800x<br />7: 2x<br />8: 5x<br />9: 10x<br />10: Auto<br />11: 1x (realtime)<br />12: 1/2x (slow-motion)<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>104</td>
      <td>Linux core active</td>
      <td>Is the system's Linux core active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>105</td>
      <td>Camera lens type</td>
      <td>Camera lens type (reflects changes to setting 162)</td>
      <td>integer</td>
      <td>0: Default<br />1: Max Lens<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>106</td>
      <td>Video hindsight capture active</td>
      <td>Is Video Hindsight Capture Active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>107</td>
      <td>Scheduled preset</td>
      <td>Scheduled Capture Preset ID</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>108</td>
      <td>Scheduled enabled</td>
      <td>Is Scheduled Capture set?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>110</td>
      <td>Media mod status</td>
      <td>Media Mode Status (bitmasked)</td>
      <td>integer</td>
      <td>0: 000 = Selfie mod: 0, HDMI: 0, Media Mod Connected: False<br />1: 001 = Selfie mod: 0, HDMI: 0, Media Mod Connected: True<br />2: 010 = Selfie mod: 0, HDMI: 1, Media Mod Connected: False<br />3: 011 = Selfie mod: 0, HDMI: 1, Media Mod Connected: True<br />4: 100 = Selfie mod: 1, HDMI: 0, Media Mod Connected: False<br />5: 101 = Selfie mod: 1, HDMI: 0, Media Mod Connected: True<br />6: 110 = Selfie mod: 1, HDMI: 1, Media Mod Connected: False<br />7: 111 = Selfie mod: 1, HDMI: 1, Media Mod Connected: True<br /></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>111</td>
      <td>Sd rating check error</td>
      <td>Does sdcard meet specified minimum write speed?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr>
      <td>112</td>
      <td>Sd write speed error</td>
      <td>Number of sdcard write speed errors since device booted</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr>
      <td>113</td>
      <td>Turbo transfer</td>
      <td>Is Turbo Transfer active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>114</td>
      <td>Camera control status</td>
      <td>Camera control status ID</td>
      <td>integer</td>
      <td>0: Camera Idle: No one is attempting to change camera settings<br />1: Camera Control: Camera is in a menu or changing settings. To intervene, app must request control<br />2: Camera External Control: An outside entity (app) has control and is in a menu or modifying settings<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr>
      <td>115</td>
      <td>Usb connected</td>
      <td>Is the camera connected to a PC via USB?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr>
      <td>116</td>
      <td>Allow control over usb</td>
      <td>Camera control over USB state</td>
      <td>integer</td>
      <td>0: Disabled<br />1: Enabled<br /></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.30.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr>
      <td>117</td>
      <td>Total sd space kb</td>
      <td>Total SD card capacity in kilobytes</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
  </tbody>
</table>


## Preset Status Format
<p>
Preset Status is returned as JSON, whose content is the serialization of the <a href="https://developers.google.com/protocol-buffers">protobuf</a> message:
<a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/preset_status.proto">NotifyPresetStatus</a>.
Using Google protobuf APIs, the JSON can be converted back into a programmatic object in the user's language of choice.
</p>


# Features


## Presets
<p>
The camera organizes modes of operation into presets.
A preset is a logical wrapper around a specific camera mode, title, icon, and a set of settings that enhance different styles of capturing media.
</p>

<p>
Depending on the camera's state, different collections of presets will be available for immediate loading and use.
Below is a table of settings that affect the current preset collection and thereby which presets can be loaded:
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>ID</td>
      <td>Setting</td>
    </tr>
    <tr>
      <td>162</td>
      <td>Max Lens</td>
    </tr>
    <tr>
      <td>173</td>
      <td>Video Performance Mode</td>
    </tr>
    <tr>
      <td>175</td>
      <td>Controls</td>
    </tr>
    <tr>
      <td>177</td>
      <td>Enable Night Photo</td>
    </tr>
    <tr>
      <td>180</td>
      <td>Video Mode</td>
    </tr>
  </tbody>
</table>

<p>
To determine which presets are available for immediate use, get <b>Preset Status</b>.
</p>

### Preset Status
<p>
All cameras support basic query and subscription mechanics that allow the user to:
</p>

<ul>
<li>Get hierarchical data describing the Preset Groups, Presets, and Settings that are available in the camera's current state</li>

</ul>

<p>
Preset Status should not be confused with camera status:
<ul>
<li>Preset Status contains information about current preset groups and presets</li>
<li>Camera status contains numerous statuses about current settings and camera system state</li>
</ul>
</p>

#### Preset Groups
<p>
Each Preset Group contains an ID, whether additional presets can be added, and an array of existing Presets.
</p>

#### Presets
<p>
Each Preset contains information about its ID, associated core mode, title, icon, whether it's a user-defined preset,
whether the preset has been modified from its factory-default state (for factory-default presets only) and an array of 
Settings associated with the Preset.
</p>

<p><i>
Important Note: The Preset ID is required to load a Preset via the <b>Presets: Load</b> command.
</i></p>


## Global Behaviors
<p>
In order to prevent undefined behavior between the camera and a connected app, simultaneous use of the camera and a
connected app is discouraged.
</p>

<p>
Best practice for synchronizing user/app control is to use the <b>Set Camera Control Status</b> command and
corresponding <i>Camera Control Status</i> (CCS) camera statuses in alignment with the finite state machine below:
</p>

```plantuml!


' Define states
IDLE: Control Status: Idle
CAMERA_CONTROL: Control Status: Camera Control
EXTERNAL_CONTROL: Control Status: External Control

' Define transitions
[*]              ->      IDLE

IDLE             ->      IDLE: App sets CCS: Idle
IDLE             -up->   CAMERA_CONTROL: User interacts with camera
IDLE             -down-> EXTERNAL_CONTROL: App sets CCS: External Control

CAMERA_CONTROL   ->      CAMERA_CONTROL: User interacts with camera
CAMERA_CONTROL   -down-> IDLE: User returns camera to idle screen\nApp sets CCS: Idle

EXTERNAL_CONTROL ->    EXTERNAL_CONTROL: App sets CCS: External Control
EXTERNAL_CONTROL -up-> IDLE: App sets CCS: Idle\nUser interacts with camera
EXTERNAL_CONTROL -up-> CAMERA_CONTROL: User interacts with camera




```

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Control Status</td>
      <td>ID</td>
    </tr>
    <tr>
      <td>IDLE</td>
      <td>0</td>
    </tr>
    <tr>
      <td>CONTROL</td>
      <td>1</td>
    </tr>
    <tr>
      <td>EXTERNAL_CONTROL</td>
      <td>2</td>
    </tr>
  </tbody>
</table>

### Set Camera Control Status
<p>
This command is used to tell the camera that the app (i.e. External Control) wishes to claim control of the camera.
This causes the camera to immediately exit any contextual menus and return to the idle screen.
Any interaction with the camera's physical buttons will cause the camera to reclaim control and update control status accordingly.
If the user returns the camera UI to the idle screen, the camera updates control status to Idle.
</p>

<p>
Note:
<ul>
<li>The entity currently claiming control of the camera is advertised in camera status 114</li>
<li>Information about whether the camera is in a contextual menu or not is advertised in camera status 63.</li>
</ul>
</p>


## OTA Update

<p>
The Over The Air (OTA) update feature allows the user to update the camera's firmware via HTTP connection.
</p>

<p>
Firmware update files can be obtained from GoPro's <a href="https://gopro.com/en/us/update">update page</a> or programmatically using the
<a href="https://api.gopro.com/firmware/v2/catalog">firmware catalog</a>.
</p>

### OTA Update Flow
<p>
The OTA update process involves uploading chunks (or all) of a file along with its corresponding SHA1 hash,
marking the file complete and then telling the camera to begin the update process.
For specific command examples, see <b>/gp/gpSoftUpdate</b> in 
<a href="#commands-quick-reference">Commands Quick Reference</a>.
</p>

<p>
Note: Near the end of the firmware update process, in order to complete, the camera will need to reboot 1-2 times.
This will cause any existing HTTP connections to be lost.
</p>
```plantuml!


Actor Client
participant Camera

note across: Obtain UPDATE.zip from update page or firmware catalog
note across: Calculate SHA1_HASH for UPDATE.zip
Client  -> Camera: HTTP/GET: /gp/gpSoftUpdate?request=delete
note right: Delete any old/cached data
Client <-- Camera: HTTP/200 (OK)
note right
JSON {
    "status":0,
    "message":"OK",
    "sha1":"",
    "bytes_complete":0,
    "complete":false
}
end note

Client  -> Camera: HTTP/GET: /gp/gpSoftUpdate?request=showui
note right: Display update OSD on camera UI
Client <-- Camera: HTTP/200 (OK)
note right
JSON: {
    "status":0,
    "message":"OK",
    "sha1":"",
    "bytes_complete":0,
    "complete":false
}
end note

loop read CHUNK of UPDATE.zip, starting at OFFSET
Client  -> Camera: HTTP/POST: /gp/gpSoftUpdate
note right: Content-Type: multipart/form-data\ndata={"sha1": "SHA1_HASH", "offset": OFFSET, file: @CHUNK}

Client <-- Camera: HTTP/200 (OK)
note right
JSON: {
    "status": 0,
    "message": "OK",
    "sha1": "SHA1_HASH",
    "bytes_complete": (total uploaded bytes),
    "complete": false
}
	end note
end

Client  -> Camera: HTTP/POST: /gp/gpSoftUpdate
note right: Content-Type: multipart/form-data\ndata={"sha1": "SHA1_HASH", "complete": true}

Client <-- Camera: HTTP/200 (OK)
note right
JSON: {
    "status":0,
    "message":"OK",
    "sha1":"SHA1_HASH",
    "bytes_complete":(size of UPDATE.zip),
    "complete":true
}
end note

Client  -> Camera: HTTP/GET: /gp/gpSoftUpdate?request=start
note right: Start updating firmware
Client <-- Camera: HTTP/200 (OK)
note right
JSON: {
    "status":0,
    "message":"OK",
    "sha1":"SHA1_HASH",
    "bytes_complete":(size of UPDATE.zip),
    "complete":true
}
end note

loop while camera updates firmware
Client  -> Camera: HTTP/GET: /gp/gpSoftUpdate?request=progress
note right
JSON: {
    "status":11,
    "message":"Firmware update in progress"
}
end note
end

note across: WiFi connection lost
note across: Camera displays OSD "Update Complete", reboots 1-2 times




```

### OTA Update Status Codes
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>ID</td>
      <td>Status</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Ok</td>
      <td>No errors occurred</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Unknown Request</td>
      <td>Server did not recognize the request</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Bad Params</td>
      <td>Parameter values not recognized</td>
    </tr>
    <tr>
      <td>3</td>
      <td>SHA1 Send Mismatch</td>
      <td>SHA1 for chunk did not match SHA1 of previous chunk(s)</td>
    </tr>
    <tr>
      <td>4</td>
      <td>SHA1 Calculates Mismatch</td>
      <td>Calculated SHA1 did not match user-specified SHA1</td>
    </tr>
    <tr>
      <td>5</td>
      <td>HTTP Boundary Error</td>
      <td>HTTP Post malformed</td>
    </tr>
    <tr>
      <td>6</td>
      <td>HTTP Post Error</td>
      <td>Unexpected HTTP/POST Content Type</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Server Busy</td>
      <td>HTTP server is busy</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Offset Mismatch</td>
      <td>Tried to upload chunk with offset that did not align with previous chunk</td>
    </tr>
    <tr>
      <td>9</td>
      <td>Bad Post Data</td>
      <td>Server failed to parse POST data</td>
    </tr>
    <tr>
      <td>10</td>
      <td>File Incomplete</td>
      <td>Tried to start update before server finished validating .zip file</td>
    </tr>
    <tr>
      <td>11</td>
      <td>Update in Progress</td>
      <td>Firmware update in progress</td>
    </tr>
    <tr>
      <td>12</td>
      <td>Insufficient Space</td>
      <td>Insufficient space on the sdcard to hold (decompressed) update file</td>
    </tr>
  </tbody>
</table>


## Webcam

<p>
The webcam feature enables developers who are interested in writing custom drivers to make the camera broadcast its
video preview with a limited set of resolution and field of view options.
</p>

<p>
While active, the webcam feature runs a UDP client that sends raw Transport Stream data to the connected client on port 8554.
To test basic functionality, connect the camera to your system, start the webcam, and use an application such as VLC to
start a network stream on udp://@0.0.0.0:8554.
</p>

<p>
For readers interested in using a GoPro camera as a webcam with preexisting tools, please see <a href="https://community.gopro.com/s/article/GoPro-Webcam?language=en_US">How to use GoPro as a Webcam</a>.
</p>

### Webcam Finite State Machine
```plantuml!


' Define states
PREREQUISITE: Wired USB Control disabled
OFF:          Webcam disabled
IDLE:         Webcam ready
HPP:          High power preview
LPP:          Low power preview

' Actions:
'   Connect camera to system via USB
'   Start
'   Preview
'   Stop
'   Exit

' Define transitions
[*]          --> PREREQUISITE

PREREQUISITE --> OFF

OFF          --> IDLE: Connect USB

IDLE         --> IDLE: Stop\nExit
IDLE         --> HPP:  Start
IDLE         --> LPP:  Preview

HPP          --> HPP:  Start
HPP          --> LPP:  Preview
HPP          --> IDLE: Stop\nExit

LPP          --> LPP:  Preview
LPP          --> HPP:  Start
LPP          --> IDLE: Stop\nExit




```

### Webcam Commands
<p>
Note: Prior to issuing webcam commands, Wired USB Control must be disabled.
For details about how to send this and webcam commands, see <a href="#commands-quick-reference">Commands Quick Reference</a>.
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Command</td>
      <td>Connections</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>Webcam: Start</td>
      <td>USB</td>
      <td>Enters webcam mode, uses default resolution and last-used fov, starts high-res stream to the IP address of caller</td>
    </tr>
    <tr>
      <td>Webcam: Start (with args)</td>
      <td>USB</td>
      <td>Enters webcam mode, uses specified resolution and/or fov, starts streaming to the IP address of caller</td>
    </tr>
    <tr>
      <td>Webcam: Preview</td>
      <td>USB</td>
      <td>Enters webcam mode, sets stream resolution and bitrate, starts low-res stream to the IP address of caller.<br />Can set Webcam Digital Lenses and Digital Zoom levels while streaming</td>
    </tr>
    <tr>
      <td>Webcam: Stop</td>
      <td>USB</td>
      <td>Stops the webcam stream</td>
    </tr>
    <tr>
      <td>Webcam: Exit</td>
      <td>USB</td>
      <td>Stops the webcam stream and exits webcam mode</td>
    </tr>
    <tr>
      <td>Webcam: Status</td>
      <td>USB</td>
      <td>Returns the current state of the webcam endpoint, including status and error codes (see tables below)</td>
    </tr>
    <tr>
      <td>Webcam: Version</td>
      <td>USB</td>
      <td>Provides version information about webcam implementation in JSON format</td>
    </tr>
  </tbody>
</table>

### Status Codes
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Status</td>
      <td>Code</td>
    </tr>
    <tr>
      <td>OFF</td>
      <td>0</td>
    </tr>
    <tr>
      <td>IDLE</td>
      <td>1</td>
    </tr>
    <tr>
      <td>HIGH_POWER_PREVIEW</td>
      <td>2</td>
    </tr>
    <tr>
      <td>LOW_POWER_PREVIEW</td>
      <td>3</td>
    </tr>
  </tbody>
</table>

### Error Codes
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Status</td>
      <td>Code</td>
    </tr>
    <tr>
      <td>NONE</td>
      <td>0</td>
    </tr>
    <tr>
      <td>SET_PRESET</td>
      <td>1</td>
    </tr>
    <tr>
      <td>SET_WINDOW_SIZE</td>
      <td>2</td>
    </tr>
    <tr>
      <td>EXEC_STREAM</td>
      <td>3</td>
    </tr>
    <tr>
      <td>SHUTTER</td>
      <td>4</td>
    </tr>
    <tr>
      <td>COM_TIMEOUT</td>
      <td>5</td>
    </tr>
    <tr>
      <td>INVALID_PARAM</td>
      <td>6</td>
    </tr>
    <tr>
      <td>UNAVAILABLE</td>
      <td>7</td>
    </tr>
    <tr>
      <td>EXIT</td>
      <td>8</td>
    </tr>
  </tbody>
</table>

### Webcam Settings

<p>
Aside from basic settings such as Resolution and FOV, the camera may support other settings such as Hypersmooth.
In order to change these settings independently, the webcam must be in <b>IDLE</b> state.
</p>

<p>
Note: There is a <a href="https://gopro.github.io/OpenGoPro/faq#known-issues">known issue</a> on some cameras in which the webcam state will be wrongly reported as IDLE after a new USB connection.
The best workaround for this is to call <b>Webcam: Start</b> followed by the <b>Webcam: Stop</b> after connecting USB in order to attain the true IDLE state.
</p>

#### Resolutions
<p>
Note: If resolution is not set, 1080p will be used by default
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>ID</td>
      <td>Resolution</td>
      <td>HERO11 Black Mini</td>
      <td>HERO11 Black</td>
      <td>HERO10 Black</td>
      <td>HERO9 Black</td>
    </tr>
    <tr>
      <td>4</td>
      <td>480</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>7</td>
      <td>720</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>12</td>
      <td>1080</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
  </tbody>
</table>

#### Digital Lenses / FOV
<p>
Note: If fov is not set, camera will default to the last-set fov or Wide if fov has never been set.
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>ID</td>
      <td>FOV</td>
      <td>HERO11 Black Mini</td>
      <td>HERO11 Black</td>
      <td>HERO10 Black</td>
      <td>HERO9 Black</td>
    </tr>
    <tr>
      <td>0</td>
      <td>WIDE</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>2</td>
      <td>NARROW</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>3</td>
      <td>SUPERVIEW</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr>
      <td>4</td>
      <td>LINEAR</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
  </tbody>
</table>

# Limitations

## HERO11 Black Mini
<ul>
<li>The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings</li>
<li>HTTP command arguments must be given in the order outlined in <a href="#commands-quick-reference">Commands Quick Reference</a></li>
</ul>
## HERO11 Black
<ul>
<li>The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings</li>
<li>HTTP command arguments must be given in the order outlined in <a href="#commands-quick-reference">Commands Quick Reference</a></li>
</ul>
## HERO10 Black
<ul>
<li>The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings</li>
<li>HTTP command arguments must be given in the order outlined in <a href="#commands-quick-reference">Commands Quick Reference</a></li>
</ul>
## HERO9 Black
<ul>
<li>The HTTP server is not available while the camera is encoding, which means shutter controls are not supported over WiFi. This limitation can be overcome by using  <a href="https://learn.adafruit.com/introduction-to-bluetooth-low-energy">Bluetooth Low Energy</a> for command and control and HTTP/REST for querying media content such as media list, media info, preview stream, etc.</li>
<li>USB command and control is not supported on HERO9 Black.</li>
<li>HTTP command arguments must be given in the order outlined in <a href="#commands-quick-reference">Commands Quick Reference</a></li>
</ul>

## General

<ul>
<li>Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera. It is recommended to send a keep-alive at least once every 120 seconds.</li>
<li>In general, querying the value for a setting that is not associated with the current preset/core mode results in an undefined value. For example, the user should not try to query the current Photo Digital Lenses (FOV) value while in Standard preset (Video mode).</li>
</ul>
