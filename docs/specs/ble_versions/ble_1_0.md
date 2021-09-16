---
title: 'Bluetooth Low Energy (BLE) Specification v1.0'
permalink: /ble_1_0
classes: spec
---


# About This Page

<p>This page describes the format, capabilities, and use of <a href="https://learn.adafruit.com/introduction-to-bluetooth-low-energy/introduction">Bluetooth Low Energy (BLE)</a> as it pertains to communicating with GoPro cameras. Messages are sent using either <a href="https://en.wikipedia.org/wiki/Type-length-value">TLV</a> or <a href="https://developers.google.com/protocol-buffers">Protobuf</a> format.</p>


# General

<p>
Communicating with a GoPro camera via Bluetooth Low Energy involves writing to Bluetooth characteristics and, typically,
waiting for a response notification from a corresponding characteristic.

The camera organizes its Generic Attribute Profile (GATT) table by broad features: AP control, network management, 
control & query, etc.
</p>


## Supported Cameras

<p>
Below is a table of cameras that support GoPro's public BLE API:
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>ID</td>
      <td>Model</td>
      <td>Marketing Name</td>
      <td>Minimal Firmware Version</td>
    </tr>
    <tr>
      <td>55</td>
      <td>HD9.01</td>
      <td>HERO9 Black</td>
      <td><a href="https://gopro.com/en/us/update/hero9-black">v1.60</a></td>
    </tr>
  </tbody>
</table>


## Services and Characteristics

<p>
Note: GP-XXXX is shorthand for GoPro's 128-bit UUIDs: <b>b5f9xxxx-aa8d-11e3-9046-0002a5d5c51b</b>
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Service UUID</td>
      <td>Service</td>
      <td>Characteristic UUID</td>
      <td>Description</td>
      <td>Permissions</td>
    </tr>
    <tr>
      <td rowspan="4">GP-0001</td>
      <td rowspan="4">GoPro WiFi Access Point</td>
      <td>GP-0002</td>
      <td>WiFi AP SSID</td>
      <td>Read / Write</td>
    </tr>
    <tr>
      <td>GP-0003</td>
      <td>WiFi AP Password</td>
      <td>Read / Write</td>
    </tr>
    <tr>
      <td>GP-0004</td>
      <td>WiFi AP Power</td>
      <td>Write</td>
    </tr>
    <tr>
      <td>GP-0005</td>
      <td>WiFi AP State</td>
      <td>Read / Notify</td>
    </tr>
    <tr>
      <td rowspan="6">FEA6</td>
      <td rowspan="6">Control & Query</td>
      <td>GP-0072</td>
      <td>Command</td>
      <td>Write</td>
    </tr>
    <tr>
      <td>GP-0073</td>
      <td>Command Response</td>
      <td>Notify</td>
    </tr>
    <tr>
      <td>GP-0074</td>
      <td>Settings</td>
      <td>Write</td>
    </tr>
    <tr>
      <td>GP-0075</td>
      <td>Settings Response</td>
      <td>Notify</td>
    </tr>
    <tr>
      <td>GP-0076</td>
      <td>Query</td>
      <td>Write</td>
    </tr>
    <tr>
      <td>GP-0077</td>
      <td>Query Response</td>
      <td>Notify</td>
    </tr>
  </tbody>
</table>


## Packet Headers

<p>
The Bluetooth Low Energy protocol limits messages to 20 Bytes per packet.
To accommodate this limitation, the packet header rules below are used.
All lengths are in bytes.
The packet count starts at 0 for the first continuation packet.
</p>

### Packet Header Format

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
        <td colspan="8">Byte 1</td>
        <td colspan="8">Byte 2 (optional)</td>
        <td colspan="8">Byte 3 (optional)</td>
    </tr>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
        <td>7</td>
        <td>6</td>
        <td>5</td>
        <td>4</td>
        <td>3</td>
        <td>2</td>
        <td>1</td>
        <td>0</td>
        <td>7</td>
        <td>6</td>
        <td>5</td>
        <td>4</td>
        <td>3</td>
        <td>2</td>
        <td>1</td>
        <td>0</td>
        <td>7</td>
        <td>6</td>
        <td>5</td>
        <td>4</td>
        <td>3</td>
        <td>2</td>
        <td>1</td>
        <td>0</td>
    </tr>
    <tr>
        <td>0: Start</td>
        <td colspan="2">00: General</td>
        <td colspan="5">Message Length: 5 bits</td>
        <td colspan="16" style="background-color: rgb(198,210,229);"></td>
    </tr>
    <tr>
        <td>0: Start</td>
        <td colspan="2">01: Extended (13-bit)</td>
        <td colspan="13">Message Length: 13 bits</td>
        <td colspan="8" style="background-color: rgb(198,210,229);"></td>
    </tr>
    <tr>
        <td>0: Start</td>
        <td colspan="2">10: Extended (16-bit)</td>
        <td colspan="5" style="background-color: rgb(198,210,229);"></td>
        <td colspan="16">Message Length: 16 bits</td>
    </tr>
    <tr>
        <td>0: Start</td>
        <td colspan="2">11: Reserved</td>
        <td colspan="21" style="background-color: rgb(198,210,229);"></td>
    </tr>
    <tr>
        <td>1: Continuation</td>
        <td colspan="24" style="background-color: rgb(198,210,229);"></td>
    </tr>
  </tbody>
</table>


## Discovery, Connection and Pairing

### Advertisements
<p>
The camera will send BLE advertisements while it is ON and for the first 8 hours after the camera is put to sleep.
During this time, the camera is discoverable and can be connected to.
If the camera is in sleep mode, connecting to it will cause the camera to wake and boot up.
</p>

### Pairing
<p>
In order to communicate with a GoPro camera via BLE, a client must first be paired with the camera.
The pairing procedure must be done once for each new client.
If the camera is factory reset, all clients will need to pair again.
To pair with the camera, use the UI to put it into pairing mode, connect via BLE and then initiate pairing.
The camera will whitelist the client so subsequent connections do not require pairing.
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Camera</td>
      <td>To Enter Pairing Mode</td>
    </tr>
    <tr>
      <td>HERO9 Black</td>
      <td>Swipe down, swipe left >> Connections >> Connect Device >> GoPro App</td>
    </tr>
  </tbody>
</table>

### Steps
<p>
Discovery of and connection to the GoPro camera can be done as follows:
</p>

<ol>
  <li>Put the camera into pairing mode</li>
  <li>Scan to discover peripherals (which can be narrowed by limiting to peripherals that advertise service FEA6)</li>
  <li>Connect to the peripheral</li>
  <li>Finish pairing with the peripheral</li>
  <li>Discover all advertised services and characteristics</li>
  <li>Subscribe to notifications from all characteristics that have the notify flag set</li>
</ol>



## Sending and Receiving Messages

<p>
In order to enable two-way communication with a GoPro camera, clients must connect to the camera and subscribe to characteristics that have the notify flag set.
Messages are sent to the camera by writing to a write-enabled UUID and then waiting for a notification from the corresponding response UUID.
Response notifications indicate whether the message was valid and will be (asynchronously) processed.
For example, to send a camera control command, a client should write to GP-0072 and then wait for a response notification from GP-0073.
</p>

<p>
Depending on the camera's state, it may not be ready to accept some commands.
This ready state is dependent on the <b>System Busy</b> and the <b>Encoding Active</b> status flags. For example:
</p>

<ul>
<li>System Busy flag is set while loading presets, changing settings, formatting sdcard, ...</li>
<li>Encoding Active flag is set while capturing photo/video media</li>
</ul>

<p>
If the system is not ready, it should reject an incoming command; however, best practice is to always wait for the
System Busy and Encode Active flags to go down before sending messages other than get status/setting queries.
</p>


## Keep Alive
<p>
Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min).
The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera, as below.
It is recommended to send a keep-alive at least once every 120 seconds.
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>UUID</td>
      <td>Write</td>
      <td>Response UUID</td>
      <td>Response</td>
    </tr>
    <tr>
      <td>GP-0074</td>
      <td>03:5B:01:42</td>
      <td>GP-0075</td>
      <td>02:5B:00</td>
    </tr>
  </tbody>
</table>


## Turbo Transfer
<p>
Some cameras support Turbo Transfer mode, which allows media to be downloaded over WiFi more rapidly.
This special mode should only be used during media offload.
It is recommended that the user check for and--if necessary--disable Turbo Transfer on connect.
For details on which cameras are supported and how to enable and disable Turbo Transfer, see
<a href="#OpenGoPro-BluetoothLowEnergyAPI-ProtobufCommands">Protobuf Commands</a>.
</p>

## Limitations

### HERO9 Black
<ul>
<li>The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings</li>
</ul>

### General

<ul>
<li>Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera. It is recommended to send a keep-alive at least once every 120 seconds.</li>
</ul>


# TLV

<p>
GoPro's BLE protocol comes in two flavors: TLV (Type Length Value) and Protobuf.
This section describes TLV style messaging.
</p>


## Commands

<p>
The table below contains command IDs supported by Open GoPro.
Command messages are sent to GP-0072 and responses/notifications are received on GP-0073.
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Command ID</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>0x01</td>
      <td>Set shutter</td>
    </tr>
    <tr>
      <td>0x05</td>
      <td>Sleep</td>
    </tr>
    <tr>
      <td>0x17</td>
      <td>AP Control</td>
    </tr>
    <tr>
      <td>0x3C</td>
      <td>Get Hardware Info</td>
    </tr>
    <tr>
      <td>0x3E</td>
      <td>Presets: Load Group</td>
    </tr>
    <tr>
      <td>0x40</td>
      <td>Presets: Load</td>
    </tr>
    <tr>
      <td>0x50</td>
      <td>Analytics</td>
    </tr>
    <tr>
      <td>0x51</td>
      <td>Open GoPro</td>
    </tr>
  </tbody>
</table>

### Command Format
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Header/Length</td>
      <td>Command ID</td>
      <td>Parameter Length</td>
      <td>Parameter Value</td>
    </tr>
    <tr>
      <td>1-2 bytes</td>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>Variable length</td>
    </tr>
  </tbody>
</table>

### Command Response
<p>
The GoPro camera sends responses to most commands received, indicating whether the command was valid and will be 
processed or not.
</p>

<p>
Unless indicated otherwise in the Quick Reference table below, command responses use the format below.
</p>

#### Command Response Format
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Header/Length</td>
      <td>Command ID</td>
      <td>Response Code</td>
      <td>Response</td>
    </tr>
    <tr>
      <td>1-2 bytes</td>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>Variable length</td>
    </tr>
  </tbody>
</table>

#### Command Response Error Codes
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Error Code</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>0</td>
      <td>Success</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Error</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Invalid Parameter</td>
    </tr>
    <tr>
      <td>3..255</td>
      <td>Reserved</td>
    </tr>
  </tbody>
</table>

### Commands Quick Reference
<p>
Below is a table of commands that can be sent to the camera and how to send them.
</p>
 
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>ID</td>
      <td>Command</td>
      <td>Description</td>
      <td>Request</td>
      <td>Response</td>
      <td>HERO9 Black</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x01</td>
      <td>Set shutter</td>
      <td>Shutter: on</td>
      <td>03:01:01:01</td>
      <td>02:01:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x01</td>
      <td>Set shutter</td>
      <td>Shutter: off</td>
      <td>03:01:01:00</td>
      <td>02:01:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x05</td>
      <td>Sleep</td>
      <td>Put camera to sleep</td>
      <td>01:05</td>
      <td>02:05:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x17</td>
      <td>AP Control</td>
      <td>WiFi AP: on</td>
      <td>03:17:01:01</td>
      <td>02:17:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x17</td>
      <td>AP Control</td>
      <td>WiFi AP: off</td>
      <td>03:17:01:00</td>
      <td>02:17:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x3C</td>
      <td>Get Hardware Info</td>
      <td>Get camera hardware info</td>
      <td>01:3C</td>
      <td>Complex</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x3E</td>
      <td>Presets: Load Group</td>
      <td>Video</td>
      <td>04:3E:02:03:E8</td>
      <td>02:3E:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x3E</td>
      <td>Presets: Load Group</td>
      <td>Photo</td>
      <td>04:3E:02:03:E9</td>
      <td>02:3E:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x3E</td>
      <td>Presets: Load Group</td>
      <td>Timelapse</td>
      <td>04:3E:02:03:EA</td>
      <td>02:3E:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Activity</td>
      <td>06:40:04:00:00:00:01</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Burst Photo</td>
      <td>06:40:04:00:01:00:02</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Cinematic</td>
      <td>06:40:04:00:00:00:02</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Live Burst</td>
      <td>06:40:04:00:01:00:01</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Night Photo</td>
      <td>06:40:04:00:01:00:03</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Night Lapse</td>
      <td>06:40:04:00:02:00:02</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Photo</td>
      <td>06:40:04:00:01:00:00</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Slo-Mo</td>
      <td>06:40:04:00:00:00:03</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Standard</td>
      <td>06:40:04:00:00:00:00</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Time Lapse</td>
      <td>06:40:04:00:02:00:01</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Time Warp</td>
      <td>06:40:04:00:02:00:00</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Max Photo</td>
      <td>06:40:04:00:04:00:00</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Max Timewarp</td>
      <td>06:40:04:00:05:00:00</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Max Video</td>
      <td>06:40:04:00:03:00:00</td>
      <td>02:40:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x50</td>
      <td>Analytics</td>
      <td>Set third party client</td>
      <td>01:50</td>
      <td>02:50:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x51</td>
      <td>Open GoPro</td>
      <td>Get version</td>
      <td>01:51</td>
      <td>Complex</td>
      <td>Y</td>
    </tr>
  </tbody>
</table>


### Complex Command Responses

<p>
Below are clarifications for complex camera responses
</p>

#### Get Hardware Info
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Response Packet</td>
      <td>Response Byte(s)</td>
      <td>Description</td>
    </tr>
    <tr>
      <td rowspan="7">1</td>
      <td>20</td>
      <td>Start packet</td>
    </tr>
    <tr>
      <td>51</td>
      <td>Packet length</td>
    </tr>
    <tr>
      <td>3C:00</td>
      <td>Command 3C sent successfully</td>
    </tr>
    <tr>
      <td>04</td>
      <td>Length of model number</td>
    </tr>
    <tr>
      <td>00:00:00:13</td>
      <td>Model number</td>
    </tr>
    <tr>
      <td>0B</td>
      <td>Length of model name</td>
    </tr>
    <tr>
      <td>48:45:52:4F:58:20:42:6C:61:63</td>
      <td>"HEROX Blac"</td>
    </tr>
    <tr>
      <td rowspan="6">2</td>
      <td>80</td>
      <td>Continuation packet</td>
    </tr>
    <tr>
      <td>6B</td>
      <td>"k"</td>
    </tr>
    <tr>
      <td>04</td>
      <td>Length of board type</td>
    </tr>
    <tr>
      <td>30:78:30:35</td>
      <td>"0x05"</td>
    </tr>
    <tr>
      <td>0F</td>
      <td>Length of firmware version</td>
    </tr>
    <tr>
      <td>48:44:58:2E:58:58:2E:58:58:2E:58:58</td>
      <td>"HDX.XX.XX.XX"</td>
    </tr>
    <tr>
      <td rowspan="5">3</td>
      <td>81</td>
      <td>Continuation packet (1)</td>
    </tr>
    <tr>
      <td>2E:58:58</td>
      <td>".XX"</td>
    </tr>
    <tr>
      <td>0E</td>
      <td>Length of serial number</td>
    </tr>
    <tr>
      <td>58:58:58:58:58:58:58:58:58:58:58:58:58:58</td>
      <td>"XXXXXXXXXXXXXX"</td>
    </tr>
    <tr>
      <td>0A</td>
      <td>Length of AP SSID</td>
    </tr>
    <tr>
      <td rowspan="4">4</td>
      <td>82</td>
      <td>Continuation packet (2)</td>
    </tr>
    <tr>
      <td>47:50:32:34:35:30:58:58:58:58</td>
      <td>"GP2450XXXX"</td>
    </tr>
    <tr>
      <td>0C</td>
      <td>AP MAC Address length</td>
    </tr>
    <tr>
      <td>58:58:58:58:58:58:58:58</td>
      <td>"XXXXXXXX"</td>
    </tr>
    <tr>
      <td rowspan="2">5</td>
      <td>83</td>
      <td>Continuation packet (3)</td>
    </tr>
    <tr>
      <td>58:58:58:58</td>
      <td>"XXXX"</td>
    </tr>
  </tbody>
</table>

#### Open GoPro Version
<p>
Given the response <i>06:51:00:01:01:01:00</i>, the Open GoPro version is v1.0.
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Response Byte(s)</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>06</td>
      <td>Packet length</td>
    </tr>
    <tr>
      <td>51</td>
      <td>Command ID</td>
    </tr>
    <tr>
      <td>00</td>
      <td>Status (OK)</td>
    </tr>
    <tr>
      <td>01</td>
      <td>Length of major version</td>
    </tr>
    <tr>
      <td>01</td>
      <td>Major version: 1</td>
    </tr>
    <tr>
      <td>01</td>
      <td>Length of minor version</td>
    </tr>
    <tr>
      <td>00</td>
      <td>Minor version: 0</td>
    </tr>
  </tbody>
</table>


## Settings
<p>
GoPro settings can be configured using the GP-Settings (GP-0074) UUID. Setting status is returned on GP-Settings-Status
(GP-0075) UUID.
</p>

### Settings Request Format
<p>
This will configure a setting on the camera. Only one setting may be sent on a packet
(GATT notify or write-no-response), although multiple packets may be sent back-to-back.
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Request Length</td>
      <td>Setting ID</td>
      <td>Setting Value Length</td>
      <td>Setting Value</td>
    </tr>
    <tr>
      <td>1-2 bytes</td>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>(variable length)</td>
    </tr>
  </tbody>
</table>

### Settings Response Format
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Response Length</td>
      <td>Setting ID</td>
      <td>Response Code</td>
    </tr>
    <tr>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>1 byte</td>
    </tr>
  </tbody>
</table>

### Settings Quick Reference
<p>
All settings are sent to UUID GP-0074. All values are hexadecimal and length are in bytes.
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Setting ID</td>
      <td>Setting</td>
      <td>Option</td>
      <td>Request</td>
      <td>Response</td>
      <td>HERO9 Black</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 4k (value: 1)</td>
      <td>03:02:01:01</td>
      <td>02:02:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 2.7k (value: 4)</td>
      <td>03:02:01:04</td>
      <td>02:02:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 2.7k 4:3 (value: 6)</td>
      <td>03:02:01:06</td>
      <td>02:02:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 1440 (value: 7)</td>
      <td>03:02:01:07</td>
      <td>02:02:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 1080 (value: 9)</td>
      <td>03:02:01:09</td>
      <td>02:02:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 4k 4:3 (value: 18)</td>
      <td>03:02:01:12</td>
      <td>02:02:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5k (value: 24)</td>
      <td>03:02:01:18</td>
      <td>02:02:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 240 (value: 0)</td>
      <td>03:03:01:00</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 120 (value: 1)</td>
      <td>03:03:01:01</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 100 (value: 2)</td>
      <td>03:03:01:02</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 60 (value: 5)</td>
      <td>03:03:01:05</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 50 (value: 6)</td>
      <td>03:03:01:06</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 30 (value: 8)</td>
      <td>03:03:01:08</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 25 (value: 9)</td>
      <td>03:03:01:09</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 24 (value: 10)</td>
      <td>03:03:01:0A</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 200 (value: 13)</td>
      <td>03:03:01:0D</td>
      <td>02:03:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Off</td>
      <td>Set setup auto power down (id: 59) to never (value: 0)</td>
      <td>03:3B:01:00</td>
      <td>01:3B:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Off</td>
      <td>Set setup auto power down (id: 59) to 5 min (value: 4)</td>
      <td>03:3B:01:04</td>
      <td>01:3B:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Off</td>
      <td>Set setup auto power down (id: 59) to 15 min (value: 6)</td>
      <td>03:3B:01:06</td>
      <td>01:3B:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Off</td>
      <td>Set setup auto power down (id: 59) to 30 min (value: 7)</td>
      <td>03:3B:01:07</td>
      <td>01:3B:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Lens</td>
      <td>Set video digital lenses (id: 121) to wide (value: 0)</td>
      <td>03:79:01:00</td>
      <td>02:79:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Lens</td>
      <td>Set video digital lenses (id: 121) to narrow (value: 6)</td>
      <td>03:79:01:06</td>
      <td>02:79:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Lens</td>
      <td>Set video digital lenses (id: 121) to superview (value: 3)</td>
      <td>03:79:01:03</td>
      <td>02:79:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Lens</td>
      <td>Set video digital lenses (id: 121) to linear (value: 4)</td>
      <td>03:79:01:04</td>
      <td>02:79:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Lens</td>
      <td>Set video digital lenses (id: 121) to max superview (value: 7)</td>
      <td>03:79:01:07</td>
      <td>02:79:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Lens</td>
      <td>Set video digital lenses (id: 121) to linear + horizon leveling (value: 8)</td>
      <td>03:79:01:08</td>
      <td>02:79:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>122</td>
      <td>Lens</td>
      <td>Set photo digital lenses (id: 122) to narrow (value: 24)</td>
      <td>03:7A:01:18</td>
      <td>02:7A:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>122</td>
      <td>Lens</td>
      <td>Set photo digital lenses (id: 122) to max superview (value: 25)</td>
      <td>03:7A:01:19</td>
      <td>02:7A:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>122</td>
      <td>Lens</td>
      <td>Set photo digital lenses (id: 122) to wide (value: 22)</td>
      <td>03:7A:01:16</td>
      <td>02:7A:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>122</td>
      <td>Lens</td>
      <td>Set photo digital lenses (id: 122) to linear (value: 23)</td>
      <td>03:7A:01:17</td>
      <td>02:7A:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>123</td>
      <td>Lens</td>
      <td>Set multi shot digital lenses (id: 123) to narrow (value: 24)</td>
      <td>03:7B:01:18</td>
      <td>02:7B:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>123</td>
      <td>Lens</td>
      <td>Set multi shot digital lenses (id: 123) to wide (value: 22)</td>
      <td>03:7B:01:16</td>
      <td>02:7B:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>123</td>
      <td>Lens</td>
      <td>Set multi shot digital lenses (id: 123) to linear (value: 23)</td>
      <td>03:7B:01:17</td>
      <td>02:7B:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>162</td>
      <td>Max Lens Mod Enable</td>
      <td>Set mods max lens enable (id: 162) to off (value: 0)</td>
      <td>03:A2:01:00</td>
      <td>02:A2:00</td>
      <td>Y</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>162</td>
      <td>Max Lens Mod Enable</td>
      <td>Set mods max lens enable (id: 162) to on (value: 1)</td>
      <td>03:A2:01:01</td>
      <td>02:A2:00</td>
      <td>Y</td>
    </tr>
  </tbody>
</table>


### Camera Capabilities
Below are tables detailing supported features for Open GoPro cameras.

#### HERO9 Black
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Resolution</td>
      <td>Anti-Flicker</td>
      <td>Frames Per Second</td>
      <td>Lens</td>
    </tr>
    <tr>
      <td rowspan="48">1080</td>
      <td rowspan="24">50Hz</td>
      <td rowspan="5">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="5">25</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="5">50</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="5">100</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">200</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="24">60Hz</td>
      <td rowspan="5">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="5">30</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="5">60</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="5">120</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">240</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="32">1440</td>
      <td rowspan="16">50Hz</td>
      <td rowspan="4">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">25</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">50</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">100</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="16">60Hz</td>
      <td rowspan="4">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">30</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">60</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">120</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="18">2.7K</td>
      <td rowspan="9">50Hz</td>
      <td rowspan="5">50</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">100</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="9">60Hz</td>
      <td rowspan="5">60</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">120</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="8">2.7K 4:3</td>
      <td rowspan="4">50Hz</td>
      <td rowspan="4">50</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">60Hz</td>
      <td rowspan="4">60</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="28">4K</td>
      <td rowspan="14">50Hz</td>
      <td rowspan="5">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="5">25</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">50</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="14">60Hz</td>
      <td rowspan="5">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="5">30</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Superview</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">60</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="16">4K 4:3</td>
      <td rowspan="8">50Hz</td>
      <td rowspan="4">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">25</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="8">60Hz</td>
      <td rowspan="4">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">30</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="16">5K</td>
      <td rowspan="8">50Hz</td>
      <td rowspan="4">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">25</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="8">60Hz</td>
      <td rowspan="4">24</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
    <tr>
      <td rowspan="4">30</td>
      <td>Wide</td>
    </tr>
    <tr>
      <td>Linear</td>
    </tr>
    <tr>
      <td>Narrow</td>
    </tr>
    <tr>
      <td>Linear + Horizon Leveling</td>
    </tr>
  </tbody>
</table>


## Query
<p>
The camera provides two basic types of state information: Camera status and settings.
Camera status info includes information such as the current preset/mode, whether the system is encoding, remaining
sdcard space, the date, etc.
Settings info gives the currently selected option for each setting;
for example, this includes the current video resolution, frame rate, digital lens (FOV), etc.
</p>

<p>
Queries are sent to to GP-0076 and responses are received on GP-0077. All packets sent and received are in Big Endian.
</p>

### Query Format
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Header/Length</td>
      <td>Query Command ID</td>
      <td>Array of IDs</td>
    </tr>
    <tr>
      <td>1-2 bytes</td>
      <td>1 byte</td>
      <td>Variable Length</td>
    </tr>
  </tbody>
</table>

### Query Commands
<p>
All query commands are sent to GP-0076. Responses are received on GP-0077.
</p>
<p>
Note: omitting <i>:xx:...</i> from (un)register query commands will result in being (un)registered for all possible
updates
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Query ID</td>
      <td>Query</td>
      <td>Request</td>
      <td>Notes</td>
    </tr>
    <tr>
      <td>0x12</td>
      <td>Get setting value</td>
      <td>02:12:xx</td>
      <td>xx -> Setting ID</td>
    </tr>
    <tr>
      <td>0x12</td>
      <td>Get all setting values</td>
      <td>01:12</td>
      <td></td>
    </tr>
    <tr>
      <td>0x13</td>
      <td>Get status value</td>
      <td>02:13:xx</td>
      <td>xx -> status code</td>
    </tr>
    <tr>
      <td>0x13</td>
      <td>Get all status values</td>
      <td>01:13</td>
      <td></td>
    </tr>
    <tr>
      <td>0x52</td>
      <td>Register for setting updates</td>
      <td>nn:52:xx:...</td>
      <td>nn -> message length<br/>xx -> setting id</td>
    </tr>
    <tr>
      <td>0x53</td>
      <td>Register for status updates</td>
      <td>nn:53:xx:...</td>
      <td>nn -> message length<br/>xx -> status code</td>
    </tr>
    <tr>
      <td>0x72</td>
      <td>Unregister for setting updates</td>
      <td>nn:72:xx:...</td>
      <td>nn -> message length<br/>xx -> setting id</td>
    </tr>
    <tr>
      <td>0x73</td>
      <td>Unregister for status updates</td>
      <td>nn:73:xx:...</td>
      <td>nn -> message length<br/>xx -> status code</td>
    </tr>
  </tbody>
</table>

### Query Response Format
<p>
Query responses are pushed asynchronously in the following scenarios:
</p>

<ul>
<li>The user queries for current status/settings</li>
<li>The user registers for settings/status updates</li>
<li>The user is registered to receive updates for a status/setting and the value changes</li>
</ul>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Message Length</td>
      <td>Query ID</td>
      <td>Command Status</td>
      <td>Status ID</td>
      <td>Status Value Length</td>
      <td>Status Value</td>
    </tr>
    <tr>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>1-255 bytes</td>
    </tr>
  </tbody>
</table>

#### Multi-Value Responses
<p>
When querying for or receiving a push notifications about more than one setting/status,
the Status ID, Status Value Length, and Status Value fields become collectively repeatable.
</p>

<p>
Example:
</p>

<p>
<code>
[MESSAGE LENGTH]:[QUERY ID]:[COMMAND STATUS]:[ID1]:[LENGTH1]:[VALUE1]:[ID2]:[LENGTH2]:[VALUE2]:...
</code>
</p>

#### Push Notification Responses
<p>
The Query ID for settings/status push notifications replaces the upper 4 bits with <code>1001</code> (nine).
</p>
<p>
For example, if the original query comand ID was 0x52, the query ID of the push notification will be 0x92.
</p>

### Status Codes
<p>
Below is a table of all possible camera status codes.
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Status ID</td>
      <td>Name</td>
      <td>Description</td>
      <td>Type</td>
      <td>Values</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Internal battery present</td>
      <td>Is the system's internal battery present?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>2</td>
      <td>Internal battery level</td>
      <td>Rough approximation of internal battery level in bars</td>
      <td>integer</td>
      <td>0: Zero<br />1: One<br />2: Two<br />3: Three<br /></td>
    </tr>
    <tr>
      <td>3</td>
      <td>External battery present</td>
      <td>Is an external battery connected?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>4</td>
      <td>External battery level</td>
      <td>External battery power level in percent</td>
      <td>percent</td>
      <td>0-100</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Unused</td>
      <td>Unused</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <td>6</td>
      <td>System hot</td>
      <td>Is the system currently overheating?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>7</td>
      <td>Unused</td>
      <td>Unused</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <td>8</td>
      <td>System busy</td>
      <td>Is the camera busy?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>9</td>
      <td>Quick capture active</td>
      <td>Is Quick Capture feature enabled?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>10</td>
      <td>Encoding active</td>
      <td>Is the system encoding right now?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>11</td>
      <td>Lcd lock active</td>
      <td>Is LCD lock active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>12</td>
      <td>Unused</td>
      <td>Unused</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <td>13</td>
      <td>Video progress counter</td>
      <td>When encoding video, this is the duration (seconds) of the video so far; 0 otherwise</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>17</td>
      <td>Enable</td>
      <td>Are Wireless Connections enabled?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>18</td>
      <td>Unused</td>
      <td>Unused</td>
      <td></td>
      <td>*</td>
    </tr>
    <tr>
      <td>19</td>
      <td>State</td>
      <td>The pairing state of the camera</td>
      <td>integer</td>
      <td>0: Success<br />1: In Progress<br />2: Failed<br />3: Stopped<br /></td>
    </tr>
    <tr>
      <td>20</td>
      <td>Type</td>
      <td>The last type of pairing that the camera was engaged in</td>
      <td>integer</td>
      <td>0: Not Pairing<br />1: Pairing App<br />2: Pairing Remote Control<br />3: Pairing Bluetooth Device<br /></td>
    </tr>
    <tr>
      <td>21</td>
      <td>Pair time</td>
      <td>Time (milliseconds) since boot of last successful pairing complete action</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>22</td>
      <td>State</td>
      <td>State of current scan for WiFi Access Points. Appears to only change for CAH-related scans</td>
      <td>integer</td>
      <td>0: Never started<br />1: Started<br />2: Aborted<br />3: Canceled<br />4: Completed<br /></td>
    </tr>
    <tr>
      <td>23</td>
      <td>Scan time msec</td>
      <td>The time, in milliseconds since boot that the WiFi Access Point scan completed</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>24</td>
      <td>Provision status</td>
      <td>WiFi AP provisioning state</td>
      <td>integer</td>
      <td>0: Never started<br />1: Started<br />2: Aborted<br />3: Canceled<br />4: Completed<br /></td>
    </tr>
    <tr>
      <td>25</td>
      <td>Unused</td>
      <td>Unused</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <td>26</td>
      <td>Remote control version</td>
      <td>Wireless remote control version</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>27</td>
      <td>Remote control connected</td>
      <td>Is a wireless remote control connected?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>28</td>
      <td>Pairing</td>
      <td>Wireless Pairing State</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>29</td>
      <td>Wlan ssid</td>
      <td>Provisioned WIFI AP SSID. On BLE connection, value is big-endian byte-encoded int</td>
      <td>string</td>
      <td>*</td>
    </tr>
    <tr>
      <td>30</td>
      <td>Ap ssid</td>
      <td>Camera's WIFI SSID. On BLE connection, value is big-endian byte-encoded int</td>
      <td>string</td>
      <td>*</td>
    </tr>
    <tr>
      <td>31</td>
      <td>App count</td>
      <td>The number of wireless devices connected to the camera</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>32</td>
      <td>Enable</td>
      <td>Is Preview Stream enabled?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>33</td>
      <td>Sd status</td>
      <td>Primary Storage Status</td>
      <td>integer</td>
      <td>-1: Unknown<br />0: OK<br />1: SD Card Full<br />2: SD Card Removed<br />3: SD Card Format Error<br />4: SD Card Busy<br />8: SD Card Swapped<br /></td>
    </tr>
    <tr>
      <td>34</td>
      <td>Remaining photos</td>
      <td>How many photos can be taken before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>35</td>
      <td>Remaining video time</td>
      <td>How many minutes of video can be captured with current settings before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>36</td>
      <td>Num group photos</td>
      <td>How many group photos can be taken with current settings before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>37</td>
      <td>Num group videos</td>
      <td>Total number of group videos on sdcard</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>38</td>
      <td>Num total photos</td>
      <td>Total number of photos on sdcard</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>39</td>
      <td>Num total videos</td>
      <td>Total number of videos on sdcard</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>40</td>
      <td>Date time</td>
      <td>Current date/time (format: %YY%MM%DD%HH%MM%SS, all values in hex)</td>
      <td>string</td>
      <td>*</td>
    </tr>
    <tr>
      <td>41</td>
      <td>Ota status</td>
      <td>The current status of Over The Air (OTA) update</td>
      <td>integer</td>
      <td>0: Idle<br />1: Downloading<br />2: Verifying<br />3: Download Failed<br />4: Verify Failed<br />5: Ready<br />6: GoPro App: Downloading<br />7: GoPro App: Verifying<br />8: GoPro App: Download Failed<br />9: GoPro App: Verify Failed<br />10: GoPro App: Ready<br /></td>
    </tr>
    <tr>
      <td>42</td>
      <td>Download cancel request pending</td>
      <td>Is there a pending request to cancel a firmware update download?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>45</td>
      <td>Camera locate active</td>
      <td>Is locate camera feature active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>49</td>
      <td>Multi shot count down</td>
      <td>The current timelapse interval countdown value (e.g. 5...4...3...2...1...)</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>50</td>
      <td>Unused</td>
      <td>Unused</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <td>51</td>
      <td>Unused</td>
      <td>Unused</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <td>52</td>
      <td>Unused</td>
      <td>Unused</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <td>53</td>
      <td>Unused</td>
      <td>Unused</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <td>54</td>
      <td>Remaining space</td>
      <td>Remaining space on the sdcard in Kilobytes</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>55</td>
      <td>Supported</td>
      <td>Is preview stream supported in current recording/flatmode/secondary-stream?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>56</td>
      <td>Wifi bars</td>
      <td>WiFi signal strength in bars</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>57</td>
      <td>Current time msec</td>
      <td>System time in milliseconds since system was booted</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>58</td>
      <td>Num hilights</td>
      <td>The number of hilights in encoding video (set to 0 when encoding stops)</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>59</td>
      <td>Last hilight time msec</td>
      <td>Time since boot (msec) of most recent hilight in encoding video (set to 0 when encoding stops)</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>60</td>
      <td>Next poll msec</td>
      <td>The min time between camera status updates (msec). Do not poll for status more often than this</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>63</td>
      <td>In contextual menu</td>
      <td>Is the camera currently in a contextual menu (e.g. Preferences)?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>64</td>
      <td>Remaining timelapse time</td>
      <td>How many min of Timelapse video can be captured with current settings before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>65</td>
      <td>Exposure select type</td>
      <td>Liveview Exposure Select Mode</td>
      <td>integer</td>
      <td>0: Disabled<br />1: Auto<br />2: ISO Lock<br />3: Hemisphere<br /></td>
    </tr>
    <tr>
      <td>66</td>
      <td>Exposure select x</td>
      <td>Liveview Exposure Select: y-coordinate (percent)</td>
      <td>percent</td>
      <td>0-100</td>
    </tr>
    <tr>
      <td>67</td>
      <td>Exposure select y</td>
      <td>Liveview Exposure Select: y-coordinate (percent)</td>
      <td>percent</td>
      <td>0-100</td>
    </tr>
    <tr>
      <td>68</td>
      <td>Gps status</td>
      <td>Does the camera currently have a GPS lock?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>69</td>
      <td>Ap state</td>
      <td>Is the WiFi radio enabled?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>70</td>
      <td>Internal battery percentage</td>
      <td>Internal battery level (percent)</td>
      <td>percent</td>
      <td>0-100</td>
    </tr>
    <tr>
      <td>74</td>
      <td>Acc mic status</td>
      <td>Microphone Accesstory status</td>
      <td>integer</td>
      <td>0: Microphone mod not connected<br />1: Microphone mod connected<br />2: Microphone mod connected and microphone plugged into Microphone mod<br /></td>
    </tr>
    <tr>
      <td>75</td>
      <td>Digital zoom</td>
      <td>Digital Zoom level (percent)</td>
      <td>percent</td>
      <td>0-100</td>
    </tr>
    <tr>
      <td>76</td>
      <td>Wireless band</td>
      <td>Wireless Band</td>
      <td>integer</td>
      <td>0: 2.4 GHz<br />1: 5 GHz<br />2: Max<br /></td>
    </tr>
    <tr>
      <td>77</td>
      <td>Digital zoom active</td>
      <td>Is Digital Zoom feature available?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>78</td>
      <td>Mobile friendly video</td>
      <td>Are current video settings mobile friendly? (related to video compression and frame rate)</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>79</td>
      <td>First time use</td>
      <td>Is the camera currently in First Time Use (FTU) UI flow?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>81</td>
      <td>Band 5ghz avail</td>
      <td>Is 5GHz wireless band available?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>82</td>
      <td>System ready</td>
      <td>Is the system ready to accept commands?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>83</td>
      <td>Batt okay for ota</td>
      <td>Is the internal battery charged sufficiently to start Over The Air (OTA) update?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>85</td>
      <td>Video low temp alert</td>
      <td>Is the camera getting too cold to continue recording?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>86</td>
      <td>Actual orientation</td>
      <td>The rotational orientation of the camera</td>
      <td>integer</td>
      <td>0: 0 degrees (upright)<br />1: 180 degrees (upside down)<br />2: 90 degrees (laying on right side)<br />3: 270 degrees (laying on left side)<br /></td>
    </tr>
    <tr>
      <td>87</td>
      <td>Thermal mitigation mode</td>
      <td>Can camera use high resolution/fps (based on temperature)? (HERO7 Silver/White only)</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>88</td>
      <td>Zoom while encoding</td>
      <td>Is this camera capable of zooming while encoding (static value based on model, not settings)</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>89</td>
      <td>Current mode</td>
      <td>Current flatmode ID</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>91</td>
      <td>Logs ready</td>
      <td>Are system logs ready to be downloaded?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>92</td>
      <td>Timewarp 1x active</td>
      <td>Is Timewarp 1x active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>93</td>
      <td>Active video presets</td>
      <td>Current Video Preset (ID)</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>94</td>
      <td>Active photo presets</td>
      <td>Current Photo Preset (ID)</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>95</td>
      <td>Active timelapse presets</td>
      <td>Current Timelapse Preset (ID)</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>96</td>
      <td>Active presets group</td>
      <td>Current Preset Group (ID)</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>97</td>
      <td>Active preset</td>
      <td>Current Preset (ID)</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>98</td>
      <td>Preset modified</td>
      <td>Preset Modified Status, which contains an event ID and a preset (group) ID</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>99</td>
      <td>Remaining live bursts</td>
      <td>How many Live Bursts can be captured before sdcard is full</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>100</td>
      <td>Num total live bursts</td>
      <td>Total number of Live Bursts on sdcard</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>101</td>
      <td>Capture delay active</td>
      <td>Is Capture Delay currently active (i.e. counting down)?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>102</td>
      <td>Media mod mic status</td>
      <td>Media mod State</td>
      <td>integer</td>
      <td>0: Media mod microphone removed<br />2: Media mod microphone only<br />3: Media mod microphone with external microphone<br /></td>
    </tr>
    <tr>
      <td>103</td>
      <td>Timewarp speed ramp active</td>
      <td>Time Warp Speed</td>
      <td>integer</td>
      <td>0: 15x<br />1: 30x<br />2: 60x<br />3: 150x<br />4: 300x<br />5: 900x<br />6: 1800x<br />7: 2x<br />8: 5x<br />9: 10x<br />10: Auto<br />11: 1x (realtime)<br />12: 1/2x (slow-motion)<br /></td>
    </tr>
    <tr>
      <td>104</td>
      <td>Linux core active</td>
      <td>Is the system's Linux core active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>105</td>
      <td>Camera lens type</td>
      <td>Camera lens type (reflects changes to setting 162)</td>
      <td>integer</td>
      <td>0: Default<br />1: Max Lens<br /></td>
    </tr>
    <tr>
      <td>106</td>
      <td>Video hindsight capture active</td>
      <td>Is Video Hindsight Capture Active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>107</td>
      <td>Scheduled preset</td>
      <td>Scheduled Capture Preset ID</td>
      <td>integer</td>
      <td>*</td>
    </tr>
    <tr>
      <td>108</td>
      <td>Scheduled enabled</td>
      <td>Is Scheduled Capture set?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>109</td>
      <td>Creating preset</td>
      <td>Is the camera in the process of creating a custom preset?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
    <tr>
      <td>110</td>
      <td>Media mod status</td>
      <td>Media Mode Status (bitmasked)</td>
      <td>integer</td>
      <td>0: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: False<br />1: Display (selfie) mod: 0, HDMI: 0, Media Mod Connected: True<br />2: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: False<br />3: Display (selfie) mod: 0, HDMI: 1, Media Mod Connected: True<br />4: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: False<br />5: Display (selfie) mod: 1, HDMI: 0, Media Mod Connected: True<br />6: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: False<br />7: Display (selfie) mod: 1, HDMI: 1, Media Mod Connected: True<br /></td>
    </tr>
    <tr>
      <td>113</td>
      <td>Turbo transfer</td>
      <td>Is Turbo Transfer active?</td>
      <td>boolean</td>
      <td>0: False<br />1: True<br /></td>
    </tr>
  </tbody>
</table>


# Protobuf

<p>
In order to maximize BLE bandwidth, some complex messages are sent using
<a href="https://developers.google.com/protocol-buffers">Google Protobuf (Protocol Buffers)</a>.
</p>


## Protobuf Message Format

<p>
Protobuf communications with the camera differ from TLV-style communications.
Rather than having a Type, Length, and Value,
protobuf messages sent to a GoPro device have a Command Type (called a Feature),
a Sub-command Type (called an Action)
and a Value (serialization of a protobuf object).
</p>

<p>
Note: For commands that do not require any protobuf inputs, Value would be empty (0 bytes).
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Message Length</td>
      <td>Feature ID</td>
      <td>Action ID</td>
      <td>Protobuf Bytestream</td>
    </tr>
    <tr>
      <td>1-2 bytes</td>
      <td>1 byte</td>
      <td>1 byte</td>
      <td>Variable Length</td>
    </tr>
  </tbody>
</table>


## Protobuf Commands
Open GoPro supports the following protobuf commands:

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Feature ID</td>
      <td>Action ID</td>
      <td>Description</td>
      <td>Request</td>
      <td>Response</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0xF1</td>
      <td>0x6B</td>
      <td>Request set turbo active</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/turbo_transfer.proto">RequestSetTurboActive</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/response_generic.proto">ResponseGeneric</a></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0xF5</td>
      <td>0x72</td>
      <td>Request get preset status</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/request_get_preset_status.proto">RequestGetPresetStatus</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/preset_status.proto">NotifyPresetStatus</a></td>
    </tr>
  </tbody>
</table>
