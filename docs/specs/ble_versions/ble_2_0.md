---
title: 'Bluetooth Low Energy (BLE) Specification v2.0'
permalink: /ble_2_0
classes: spec
redirect_from:
    - /ble
---


# About This Page

<p>
This page describes the format, capabilities, and use of <a href="https://learn.adafruit.com/introduction-to-bluetooth-low-energy">Bluetooth Low Energy (BLE)</a> as it pertains to communicating with GoPro cameras.
Messages are sent using either <a href="https://en.wikipedia.org/wiki/Type-length-value">TLV</a> or <a href="https://developers.google.com/protocol-buffers">Protobuf</a> format.
</p>


# General

<p>
Communicating with a GoPro camera via Bluetooth Low Energy involves writing to Bluetooth characteristics and, typically,
waiting for a response notification from a corresponding characteristic.
The camera organizes its Generic Attribute Profile (GATT) table by broad features: AP control, control & query, etc.
</p>

<p>
Note: All byte ordering is in Big Endian unless otherwise noted.
</p>


## Supported Cameras

<p>
Below is a table of cameras that support GoPro's public BLE API:
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
      <td>Read / Indicate</td>
    </tr>
    <tr>
      <td rowspan="2">GP-0090</td>
      <td rowspan="2">GoPro Camera Management</td>
      <td>GP-0091</td>
      <td>Network Management Command</td>
      <td>Write</td>
    </tr>
    <tr>
      <td>GP-0092</td>
      <td>Network Management Response</td>
      <td>Notify</td>
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
The Bluetooth Low Energy protocol limits messages to 20 bytes per packet.
To accommodate this limitation, GoPro cameras use the packet header format below.
All lengths are in bytes.
</p>

<p>
Messages sent to and received from the camera are expected to be packetized and sent in 20 byte chunks.
Messages received from the camera will always use the header with the smallest possible message length.
For example, a three byte response will use the 5-bit General header, not the 13-bit or 16-bit Extended headers.
</p>

<p>
Messages sent to the camera can use either the 5-bit General header or the 13-bit Extended header.
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
        <td colspan="3" style="background-color: rgb(198,210,229);"></td>
        <td colspan="4">Counter (4-bit)</td>
        <td colspan="16" style="background-color: rgb(198,210,229);"></td>
    </tr>
  </tbody>
</table>

<p>
Note: Continuation packet counters start at 0x0 and reset after 0xF.
</p>

### Example: Packetizing a 5-bit General Message
<p>
<b>Message Length:</b> 17 bytes
</p>
<p>
<b>Message:</b> 01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Packet</td>
      <td>Type</td>
      <td>Byte(s)</td>
      <td>Description</td>
    </tr>
    <tr>
      <td rowspan="2">1</td>
      <td>Header</td>
      <td>11</td>
      <td>(0) start packet<br/>(00) 5-bit General message<br/>(10001) message length: 17</td>
    </tr>
    <tr>
      <td>Payload</td>
      <td>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11</td>
      <td>Message</td>
    </tr>
  </tbody>
</table>

### Example: Packetizing a 13-bit Extended Message
<p>
<b>Message Length:</b> 50 bytes
</p>
<p>
<b>Message:</b> 01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:14:15:16:17:18:19:1A:1B:1C:1D:1E:1F:20:21:22:23:24:25:26:27:28:29:2A:2B:2C:2D:2E:2F:30:31:32
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Packet</td>
      <td>Type</td>
      <td>Byte(s)</td>
      <td>Description</td>
    </tr>
    <tr>
      <td rowspan="2">1</td>
      <td>Header</td>
      <td>20:32</td>
      <td>(0) start packet<br/>(01) 13-bit Extended message<br/>(0000000110010) message length: 50</td>
    </tr>
    <tr>
      <td>Payload</td>
      <td>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12</td>
      <td>Message (chunk 1 of 3)</td>
    </tr>
    <tr>
      <td rowspan="2">2</td>
      <td>Header</td>
      <td>80</td>
      <td>(0) continuation packet<br/>(000) ignored<br/>(0000) counter: 0</td>
    </tr>
    <tr>
      <td>Payload</td>
      <td>13:14:15:16:17:18:19:1A:1B:1C:1D:1E:1F:20:21:22:23:24:25</td>
      <td>Message (chunk 2 of 3)</td>
    </tr>
    <tr>
      <td rowspan="2">3</td>
      <td>Header</td>
      <td>81</td>
      <td>(0) continuation packet<br/>(000) ignored<br/>(0001) counter: 1</td>
    </tr>
    <tr>
      <td>Payload</td>
      <td>26:27:28:29:2A:2B:2C:2D:2E:2F:30:31:32</td>
      <td>Message (chunk 3 of 3)</td>
    </tr>
  </tbody>
</table>

### Example: Depacketizing a Mutli-Packet Message
<p>
<b>Packets Received:</b> 5
</p>
<p>
Once the packet headers are identified and removed from each packet, the complete response message can be assembled by concatenating the remaining packet data in the order it was received.
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Packet</td>
      <td>Byte(s)</td>
      <td>Header</td>
    </tr>
    <tr>
      <td>1</td>
      <td><b>20:57</b>:01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12</td>
      <td>20:57<br/>(0) start packet<br/>(01) 13-bit Extended message<br/>(0000001010111) message length: 87</td>
    </tr>
    <tr>
      <td>2</td>
      <td><b>80</b>:13:14:15:16:17:18:19:1A:1B:1C:1D:1E:1F:20:21:22:23:24:25</td>
      <td>80<br/>(1) continuation packet<br/>(000) ignored<br/>(0000) counter: 0</td>
    </tr>
    <tr>
      <td>3</td>
      <td><b>81</b>:26:27:28:29:2A:2B:2C:2D:2E:2F:30:31:32:33:34:35:36:37:38</td>
      <td>81<br/>(1) continuation packet<br/>(000) ignored<br/>(0001) counter: 1</td>
    </tr>
    <tr>
      <td>4</td>
      <td><b>82</b>:39:3A:3B:3C:3D:3E:3F:40:41:42:43:44:45:46:47:48:49:4A:4B</td>
      <td>82<br/>(1) continuation packet<br/>(000) ignored<br/>(0010) counter: 2</td>
    </tr>
    <tr>
      <td>5</td>
      <td><b>83</b>:4C:4D:4E:4F:50:51:52:53:54:55:56:57</td>
      <td>83<br/>(1) continuation packet<br/>(000) ignored<br/>(0011) counter: 3</td>
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
To pair with the camera, use the UI to put it into <a href="https://community.gopro.com/s/article/GoPro-Quik-How-To-Pair-Your-Camera?language=en_US">pairing mode</a>, connect via BLE and then initiate pairing.
The camera will whitelist the client so subsequent connections do not require pairing.
</p>

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
Depending on the camera's state, it may not be ready to accept specific commands.
This ready state is dependent on the <b>System Busy</b> and the <b>Encoding Active</b> status flags. For example:
</p>

<ul>
<li>System Busy flag is set while loading presets, changing settings, formatting sdcard, ...</li>
<li>Encoding Active flag is set while capturing photo/video media</li>
</ul>

<p>
If the system is not ready, it should reject an incoming command; however, best practice is to always wait for the
System Busy and Encode Active flags to be unset before sending messages other than get status/setting queries.
</p>


## Parsing Responses
<p>
In order to communicate fully with the camera, the user will need to be able to parse response and event notifications in TLV or Protobuf format as needed.
</p>

<p>
TLV and Protobuf responses have very different formats.
Parsing TLV data requires a parser to be written locally.
Parsing Protobuf data can be done using code generated from <a href="#protobuf-commands">Protobuf files</a> linked in this document.
Typically, the camera will send TLV responses/events for commands sent in TLV format and Protobuf responses/events for commands sent in Protobuf format.
</p>

<p>
The pseudocode and flowcharts below refer to the following tables:
</p>

<ul>
<li><a href="#protobuf-ids">Protobuf IDs Table</a></li>
<li><a href="#protobuf-commands">Protobuf Commands Table</a></li>
<li><a href="#command-response-format">Command Response Format</a></li>
<li><a href="#settings-response-format">Settings Response Format</a></li>
<li><a href="#query-response-format">Query Response Format</a></li>
</ul> 


### Pseudocode
<p>
Below is pseudocode describing how to determine whether a respose is TLV or Protobuf and then parse it appropriately.
</p>

```
Camera sends response R (array of bytes) from UUID U (string) with payload P (array of bytes)
// Is it a Protobuf response?
for each row in the Protobuf IDs table {
    F (int) = Feature ID
    A (array of int) = Action IDs
    if P[0] == F and P[1] in A {
        R is a protobuf message
        Match Feature ID P[0] and Action ID P[1] to a Response message in the Protobuf Commands Table
        Use matched Response message to parse payload into useful data structure
        Exit
    }
}
// Nope. It is a TLV response
if U == GP-0072 (Command) {
    Parse using Command Response Format table
}
else if U == GP-0074 (Settings) {
    Parse using Settings Response Format table
}
else if U == GP-0076 (Query) {
    Parse using Query Response Format table
}
Exit
```

### Flowchart
<p>
Below is a flowchart describing how to determine whether a respose is TLV or Protobuf and then parse it appropriately.
</p>

```plantuml!


' Note: The weird whitespace is used to make the text look better on the image

start

:Receive response R;
:Extract payload P;

if (\nP[0] == Feature ID from row N of Protobuf IDs Table\nAND\nP[1] in Action IDs list from row N of Protobuf IDs Table\n) then (yes)
    :R is a protobuf message;
else (no)
    :R is a TLV message;
endif

switch (Response R)
case ( TLV message)
   switch (Response UUID)
   case ( GP-0072\n (Control))
      :R is a Command response;
   case (   GP-0074\n   (Settings))
      :R is a Settings response;
   case ( GP-0076\n (Query))
      :R is a Query response;
   endswitch
   :Parse accordingly;
case ( Protobuf message)
   :Feature ID = P[0]\nAction ID = P[1];
   :Use: Protobuf Commands Table;
   :Parse using appropriate protobuf message;
endswitch

:Knowledge!;
stop




```


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

## Limitations

### HERO11 Black Mini
<ul>
<li>The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings</li>
</ul>
### HERO11 Black
<ul>
<li>The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings</li>
</ul>
### HERO10 Black
<ul>
<li>The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings</li>
</ul>
### HERO9 Black
<ul>
<li>The camera will reject requests to change settings while encoding; for example, if Hindsight feature is active, the user cannot change settings</li>
</ul>

### General

<ul>
<li>Unless changed by the user, GoPro cameras will automatically power off after some time (e.g. 5min, 15min, 30min). The Auto Power Down watchdog timer can be reset by sending periodic keep-alive messages to the camera. It is recommended to send a keep-alive at least once every 120 seconds.</li>
<li>In general, querying the value for a setting that is not associated with the current preset/core mode results in an undefined value. For example, the user should not try to query the current Photo Digital Lenses (FOV) value while in Standard preset (Video mode).</li>
</ul>


# Type Length Value

<p>
GoPro's BLE protocol comes in two flavors: TLV (Type Length Value) and Protobuf.
This section describes TLV style messaging.
</p>

<p>
Note: All TLV messages (payloads) must be packetized and wrapped with <a href="https://gopro.github.io/OpenGoPro/ble_2_0#packet-headers">Packet Headers</a> as outlined in this document.
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
      <td>0x0D</td>
      <td>Set Date/Time</td>
    </tr>
    <tr>
      <td>0x0E</td>
      <td>Get Date/Time</td>
    </tr>
    <tr>
      <td>0x0F</td>
      <td>Set Local Date/Time</td>
    </tr>
    <tr>
      <td>0x10</td>
      <td>Get Local Date/Time</td>
    </tr>
    <tr>
      <td>0x15</td>
      <td>Set Livestream Mode</td>
    </tr>
    <tr>
      <td>0x17</td>
      <td>AP Control</td>
    </tr>
    <tr>
      <td>0x18</td>
      <td>Media: HiLight Moment</td>
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
Below is a table of commands that can be sent to the camera and how to send them.<br />
* Indicates that item is experimental<br />
<span style="color:green">✔</span> Indicates support for all Open GoPro firmware versions.<br />
<span style="color:red">❌</span> Indicates a lack of support for all Open GoPro firmware versions.<br />
>= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ
</p>
 
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>ID</td>
      <td>Command</td>
      <td>Description</td>
      <td>Request</td>
      <td>Response</td>
      <td>HERO11 Black Mini</td>
      <td>HERO11 Black</td>
      <td>HERO10 Black</td>
      <td>HERO9 Black</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x01</td>
      <td>Set shutter</td>
      <td>Shutter: off</td>
      <td>03:01:01:00</td>
      <td>02:01:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x01</td>
      <td>Set shutter</td>
      <td>Shutter: on</td>
      <td>03:01:01:01</td>
      <td>02:01:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x05</td>
      <td>Sleep</td>
      <td>Put camera to sleep</td>
      <td>01:05</td>
      <td>02:05:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x0D</td>
      <td>Set Date/Time</td>
      <td>Set date/time to 2023-01-31 03:04:05</td>
      <td>09:0D:07:07:E7:01:1F:03:04:05</td>
      <td>02:0D:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x0E</td>
      <td>Get Date/Time</td>
      <td>Get date/time</td>
      <td>01:0E</td>
      <td>Complex</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x0F</td>
      <td>Set Local Date/Time</td>
      <td>Set local date/time to: 2023-01-31 03:04:05 (utc-02:00) (dst: on)</td>
      <td>0C:0F:0A:07:E7:01:1F:03:04:05:FF:88:01</td>
      <td>02:0F:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x10</td>
      <td>Get Local Date/Time</td>
      <td>Get local date/time</td>
      <td>01:10</td>
      <td>Complex</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x15</td>
      <td>Set Livestream Mode</td>
      <td>Set live stream mode: url: xxx, encode: true, window size: windowsize.size_720, cert: none</td>
      <td>20:15:F1:79:0A:03:78:78:78:10:01:18:07:38:7B:40:95:06:48:C8:80:03:50:00</td>
      <td>02:15:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x17</td>
      <td>AP Control</td>
      <td>Ap mode: off</td>
      <td>03:17:01:00</td>
      <td>02:17:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x17</td>
      <td>AP Control</td>
      <td>Ap mode: on</td>
      <td>03:17:01:01</td>
      <td>02:17:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x18</td>
      <td>Media: HiLight Moment</td>
      <td>Hilight moment during encoding</td>
      <td>01:18</td>
      <td>02:18:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x3C</td>
      <td>Get Hardware Info</td>
      <td>Get camera hardware info</td>
      <td>01:3C</td>
      <td>Complex</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x3E</td>
      <td>Presets: Load Group</td>
      <td>Video</td>
      <td>04:3E:02:03:E8</td>
      <td>02:3E:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x3E</td>
      <td>Presets: Load Group</td>
      <td>Photo</td>
      <td>04:3E:02:03:E9</td>
      <td>02:3E:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x3E</td>
      <td>Presets: Load Group</td>
      <td>Timelapse</td>
      <td>04:3E:02:03:EA</td>
      <td>02:3E:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x40</td>
      <td>Presets: Load</td>
      <td>Example <a href="#presets">preset id</a>: 0x1234ABCD</td>
      <td>06:40:04:12:34:AB:CD</td>
      <td>02:40:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x50</td>
      <td>Analytics</td>
      <td>Set third party client</td>
      <td>01:50</td>
      <td>02:50:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x51</td>
      <td>Open GoPro</td>
      <td>Get version</td>
      <td>01:51</td>
      <td>Complex</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
  </tbody>
</table>


### Complex Command Inputs

#### Set Local Date/Time
<p>
The timezone is a two byte UTC offset in minutes and must be sent in <a href="https://en.wikipedia.org/wiki/Two%27s_complement">Two's Complement</a> form.
</p>




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
      <td>Response length</td>
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
      <td>00:00:00:37</td>
      <td>Model ID</td>
    </tr>
    <tr>
      <td>0B</td>
      <td>Length of model id</td>
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
Given the response <i>06:51:00:01:01:01:00</i>, the Open GoPro version would be vXX.YY.
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

#### Get Date/Time
<p>
Given the response <i>0B:0E:00:08:07:E5:01:02:03:04:05:06</i>, the date/time would be 2022-01-02 03:04:05 (Saturday).
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Response Byte(s)</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>0B</td>
      <td>Packet length</td>
    </tr>
    <tr>
      <td>0E</td>
      <td>Command ID</td>
    </tr>
    <tr>
      <td>00</td>
      <td>Status (OK)</td>
    </tr>
    <tr>
      <td>08</td>
      <td>Date length (bytes)</td>
    </tr>
    <tr>
      <td>07:E6</td>
      <td>Year</td>
    </tr>
    <tr>
      <td>01</td>
      <td>Month</td>
    </tr>
    <tr>
      <td>02</td>
      <td>Day</td>
    </tr>
    <tr>
      <td>03</td>
      <td>Hour</td>
    </tr>
    <tr>
      <td>04</td>
      <td>Minute</td>
    </tr>
    <tr>
      <td>05</td>
      <td>Second</td>
    </tr>
    <tr>
      <td>06</td>
      <td>Day of the week (Sun=0, Sat=6)</td>
    </tr>
  </tbody>
</table>

#### Get Local Date/Time (with Timezone and DST)
<p>
Given the response <i>0D:10:00:0A:07:E6:01:02:03:04:05:FE:20:01</i>, the date/time would be 2022-01-02 03:04:05-0800 (DST: ON).
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Response Byte(s)</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>0D</td>
      <td>Packet length</td>
    </tr>
    <tr>
      <td>10</td>
      <td>Command ID</td>
    </tr>
    <tr>
      <td>00</td>
      <td>Status (OK)</td>
    </tr>
    <tr>
      <td>0A</td>
      <td>Date length (bytes)</td>
    </tr>
    <tr>
      <td>07:E6</td>
      <td>Year</td>
    </tr>
    <tr>
      <td>01</td>
      <td>Month</td>
    </tr>
    <tr>
      <td>02</td>
      <td>Day</td>
    </tr>
    <tr>
      <td>03</td>
      <td>Hour</td>
    </tr>
    <tr>
      <td>04</td>
      <td>Minute</td>
    </tr>
    <tr>
      <td>05</td>
      <td>Second</td>
    </tr>
    <tr>
      <td>FE:20</td>
      <td>UTC offset in minutes (<a href='https://en.wikipedia.org/wiki/Two%27s_complement'>Two's Complement</a>)</td>
    </tr>
    <tr>
      <td>01</td>
      <td>DST: ON</td>
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
All settings are sent to UUID GP-0074. All values are hexadecimal and length are in bytes.<br />
* Indicates that item is experimental<br />
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
      <td>Request</td>
      <td>Response</td>
      <td>HERO11 Black Mini</td>
      <td>HERO11 Black</td>
      <td>HERO10 Black</td>
      <td>HERO9 Black</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 4k (id: 1)</td>
      <td>03:02:01:01</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 2.7k (id: 4)</td>
      <td>03:02:01:04</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 2.7k 4:3 (id: 6)</td>
      <td>03:02:01:06</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 1440 (id: 7)</td>
      <td>03:02:01:07</td>
      <td>02:02:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 1080 (id: 9)</td>
      <td>03:02:01:09</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 4k 4:3 (id: 18)</td>
      <td>03:02:01:12</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5k (id: 24)</td>
      <td>03:02:01:18</td>
      <td>02:02:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5k 4:3 (id: 25)</td>
      <td>03:02:01:19</td>
      <td>02:02:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5.3k 8:7 (id: 26)</td>
      <td>03:02:01:1A</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5.3k 4:3 (id: 27)</td>
      <td>03:02:01:1B</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 4k 8:7 (id: 28)</td>
      <td>03:02:01:1C</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>2</td>
      <td>Resolution</td>
      <td>Set video resolution (id: 2) to 5.3k (id: 100)</td>
      <td>03:02:01:64</td>
      <td>02:02:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 240 (id: 0)</td>
      <td>03:03:01:00</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 120 (id: 1)</td>
      <td>03:03:01:01</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 100 (id: 2)</td>
      <td>03:03:01:02</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 60 (id: 5)</td>
      <td>03:03:01:05</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 50 (id: 6)</td>
      <td>03:03:01:06</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 30 (id: 8)</td>
      <td>03:03:01:08</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 25 (id: 9)</td>
      <td>03:03:01:09</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 24 (id: 10)</td>
      <td>03:03:01:0A</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>3</td>
      <td>Frames Per Second</td>
      <td>Set video fps (id: 3) to 200 (id: 13)</td>
      <td>03:03:01:0D</td>
      <td>02:03:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to never (id: 0)</td>
      <td>03:3B:01:00</td>
      <td>01:3B:00</td>
      <td>\&gt;= v02.10.00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 1 min (id: 1)</td>
      <td>03:3B:01:01</td>
      <td>01:3B:00</td>
      <td>\&gt;= v02.10.00</td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 5 min (id: 4)</td>
      <td>03:3B:01:04</td>
      <td>01:3B:00</td>
      <td>\&gt;= v02.10.00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 15 min (id: 6)</td>
      <td>03:3B:01:06</td>
      <td>01:3B:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 30 min (id: 7)</td>
      <td>03:3B:01:07</td>
      <td>01:3B:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 8 seconds (id: 11)</td>
      <td>03:3B:01:0B</td>
      <td>01:3B:00</td>
      <td>\&gt;= v02.10.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>59</td>
      <td>Auto Power Down</td>
      <td>Set auto power down (id: 59) to 30 seconds (id: 12)</td>
      <td>03:3B:01:0C</td>
      <td>01:3B:00</td>
      <td>\&gt;= v02.10.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to wide (id: 0)</td>
      <td>03:79:01:00</td>
      <td>02:79:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to narrow (id: 2)</td>
      <td>03:79:01:02</td>
      <td>02:79:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to superview (id: 3)</td>
      <td>03:79:01:03</td>
      <td>02:79:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to linear (id: 4)</td>
      <td>03:79:01:04</td>
      <td>02:79:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to max superview (id: 7)</td>
      <td>03:79:01:07</td>
      <td>02:79:00</td>
      <td>\&gt;= v02.00.00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to linear + horizon leveling (id: 8)</td>
      <td>03:79:01:08</td>
      <td>02:79:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to hyperview (id: 9)</td>
      <td>03:79:01:09</td>
      <td>02:79:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>121</td>
      <td>Video Digital Lenses</td>
      <td>Set video digital lenses (id: 121) to linear + horizon lock (id: 10)</td>
      <td>03:79:01:0A</td>
      <td>02:79:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>122</td>
      <td>Photo Digital Lenses</td>
      <td>Set photo digital lenses (id: 122) to narrow (id: 19)</td>
      <td>03:7A:01:13</td>
      <td>02:7A:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>122</td>
      <td>Photo Digital Lenses</td>
      <td>Set photo digital lenses (id: 122) to max superview (id: 100)</td>
      <td>03:7A:01:64</td>
      <td>02:7A:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>122</td>
      <td>Photo Digital Lenses</td>
      <td>Set photo digital lenses (id: 122) to wide (id: 101)</td>
      <td>03:7A:01:65</td>
      <td>02:7A:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>122</td>
      <td>Photo Digital Lenses</td>
      <td>Set photo digital lenses (id: 122) to linear (id: 102)</td>
      <td>03:7A:01:66</td>
      <td>02:7A:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>123</td>
      <td>Time Lapse Digital Lenses</td>
      <td>Set time lapse digital lenses (id: 123) to narrow (id: 19)</td>
      <td>03:7B:01:13</td>
      <td>02:7B:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>123</td>
      <td>Time Lapse Digital Lenses</td>
      <td>Set time lapse digital lenses (id: 123) to max superview (id: 100)</td>
      <td>03:7B:01:64</td>
      <td>02:7B:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>123</td>
      <td>Time Lapse Digital Lenses</td>
      <td>Set time lapse digital lenses (id: 123) to wide (id: 101)</td>
      <td>03:7B:01:65</td>
      <td>02:7B:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>123</td>
      <td>Time Lapse Digital Lenses</td>
      <td>Set time lapse digital lenses (id: 123) to linear (id: 102)</td>
      <td>03:7B:01:66</td>
      <td>02:7B:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>128</td>
      <td>Media Format</td>
      <td>Set media format (id: 128) to time lapse video (id: 13)</td>
      <td>03:80:01:0D</td>
      <td>02:80:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>128</td>
      <td>Media Format</td>
      <td>Set media format (id: 128) to time lapse photo (id: 20)</td>
      <td>03:80:01:14</td>
      <td>02:80:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>128</td>
      <td>Media Format</td>
      <td>Set media format (id: 128) to night lapse photo (id: 21)</td>
      <td>03:80:01:15</td>
      <td>02:80:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>128</td>
      <td>Media Format</td>
      <td>Set media format (id: 128) to night lapse video (id: 26)</td>
      <td>03:80:01:1A</td>
      <td>02:80:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>134</td>
      <td>Anti-Flicker</td>
      <td>Set setup anti flicker (id: 134) to 60hz (id: 2)</td>
      <td>03:86:01:02</td>
      <td>02:86:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>134</td>
      <td>Anti-Flicker</td>
      <td>Set setup anti flicker (id: 134) to 50hz (id: 3)</td>
      <td>03:86:01:03</td>
      <td>02:86:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to off (id: 0)</td>
      <td>03:87:01:00</td>
      <td>02:87:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to on (id: 1)</td>
      <td>03:87:01:01</td>
      <td>02:87:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to high (id: 2)</td>
      <td>03:87:01:02</td>
      <td>02:87:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to boost (id: 3)</td>
      <td>03:87:01:03</td>
      <td>02:87:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to auto boost (id: 4)</td>
      <td>03:87:01:04</td>
      <td>02:87:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>135</td>
      <td>Hypersmooth</td>
      <td>Set video hypersmooth (id: 135) to standard (id: 100)</td>
      <td>03:87:01:64</td>
      <td>02:87:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>150</td>
      <td>Horizon Leveling</td>
      <td>Set video horizon levelling (id: 150) to off (id: 0)</td>
      <td>03:96:01:00</td>
      <td>02:96:00</td>
      <td>\&gt;= v02.00.00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>150</td>
      <td>Horizon Leveling</td>
      <td>Set video horizon levelling (id: 150) to on (id: 1)</td>
      <td>03:96:01:01</td>
      <td>02:96:00</td>
      <td>\&gt;= v02.00.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>150</td>
      <td>Horizon Leveling</td>
      <td>Set video horizon levelling (id: 150) to locked (id: 2)</td>
      <td>03:96:01:02</td>
      <td>02:96:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>151</td>
      <td>Horizon Leveling</td>
      <td>Set photo horizon levelling (id: 151) to off (id: 0)</td>
      <td>03:97:01:00</td>
      <td>02:97:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>151</td>
      <td>Horizon Leveling</td>
      <td>Set photo horizon levelling (id: 151) to locked (id: 2)</td>
      <td>03:97:01:02</td>
      <td>02:97:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>162</td>
      <td>Max Lens</td>
      <td>Set max lens (id: 162) to off (id: 0)</td>
      <td>03:A2:01:00</td>
      <td>02:A2:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.20.00</td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>162</td>
      <td>Max Lens</td>
      <td>Set max lens (id: 162) to on (id: 1)</td>
      <td>03:A2:01:01</td>
      <td>02:A2:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.20.00</td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>167</td>
      <td>Hindsight*</td>
      <td>Set hindsight (id: 167) to 15 seconds (id: 2)</td>
      <td>03:A7:01:02</td>
      <td>02:A7:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>167</td>
      <td>Hindsight*</td>
      <td>Set hindsight (id: 167) to 30 seconds (id: 3)</td>
      <td>03:A7:01:03</td>
      <td>02:A7:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>167</td>
      <td>Hindsight*</td>
      <td>Set hindsight (id: 167) to off (id: 4)</td>
      <td>03:A7:01:04</td>
      <td>02:A7:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>173</td>
      <td>Video Performance Mode</td>
      <td>Set video performance mode (id: 173) to maximum video performance (id: 0)</td>
      <td>03:AD:01:00</td>
      <td>02:AD:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v01.16.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>173</td>
      <td>Video Performance Mode</td>
      <td>Set video performance mode (id: 173) to extended battery (id: 1)</td>
      <td>03:AD:01:01</td>
      <td>02:AD:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v01.16.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>173</td>
      <td>Video Performance Mode</td>
      <td>Set video performance mode (id: 173) to tripod / stationary video (id: 2)</td>
      <td>03:AD:01:02</td>
      <td>02:AD:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v01.16.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>175</td>
      <td>Controls</td>
      <td>Set controls (id: 175) to easy (id: 0)</td>
      <td>03:AF:01:00</td>
      <td>02:AF:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>175</td>
      <td>Controls</td>
      <td>Set controls (id: 175) to pro (id: 1)</td>
      <td>03:AF:01:01</td>
      <td>02:AF:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (id: 0)</td>
      <td>03:B0:01:00</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (id: 1)</td>
      <td>03:B0:01:01</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (id: 2)</td>
      <td>03:B0:01:02</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (low light) (id: 3)</td>
      <td>03:B0:01:03</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (ext. batt) (id: 4)</td>
      <td>03:B0:01:04</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (ext. batt) (id: 5)</td>
      <td>03:B0:01:05</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (ext. batt, low light) (id: 6)</td>
      <td>03:B0:01:06</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (50hz) (id: 7)</td>
      <td>03:B0:01:07</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (50hz) (id: 8)</td>
      <td>03:B0:01:08</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (50hz) (id: 9)</td>
      <td>03:B0:01:09</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (low light, 50hz) (id: 10)</td>
      <td>03:B0:01:0A</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (ext. batt, 50hz) (id: 11)</td>
      <td>03:B0:01:0B</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (ext. batt, 50hz) (id: 12)</td>
      <td>03:B0:01:0C</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (ext. batt, low light, 50hz) (id: 13)</td>
      <td>03:B0:01:0D</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (ext. batt) (id: 14)</td>
      <td>03:B0:01:0E</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (ext. batt, 50hz) (id: 15)</td>
      <td>03:B0:01:0F</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (long. batt) (id: 16)</td>
      <td>03:B0:01:10</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (long. batt) (id: 17)</td>
      <td>03:B0:01:11</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (long. batt) (id: 18)</td>
      <td>03:B0:01:12</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (long. batt, low light) (id: 19)</td>
      <td>03:B0:01:13</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 8x ultra slo-mo (long. batt, 50hz) (id: 20)</td>
      <td>03:B0:01:14</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (long. batt, 50hz) (id: 21)</td>
      <td>03:B0:01:15</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (long. batt, 50hz) (id: 22)</td>
      <td>03:B0:01:16</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 1x (long. batt, low light, 50hz) (id: 23)</td>
      <td>03:B0:01:17</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (4k) (id: 24)</td>
      <td>03:B0:01:18</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (2.7k) (id: 25)</td>
      <td>03:B0:01:19</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 2x slo-mo (4k, 50hz) (id: 26)</td>
      <td>03:B0:01:1A</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>176</td>
      <td>Speed</td>
      <td>Set speed (id: 176) to 4x super slo-mo (2.7k, 50hz) (id: 27)</td>
      <td>03:B0:01:1B</td>
      <td>02:B0:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>177</td>
      <td>Enable Night Photo</td>
      <td>Set enable night photo (id: 177) to off (id: 0)</td>
      <td>03:B1:01:00</td>
      <td>02:B1:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>177</td>
      <td>Enable Night Photo</td>
      <td>Set enable night photo (id: 177) to on (id: 1)</td>
      <td>03:B1:01:01</td>
      <td>02:B1:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>178</td>
      <td>Wireless Band</td>
      <td>Set wireless band (id: 178) to 2.4ghz (id: 0)</td>
      <td>03:B2:01:00</td>
      <td>02:B2:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>178</td>
      <td>Wireless Band</td>
      <td>Set wireless band (id: 178) to 5ghz (id: 1)</td>
      <td>03:B2:01:01</td>
      <td>02:B2:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>179</td>
      <td>Trail Length</td>
      <td>Set trail length (id: 179) to short (id: 1)</td>
      <td>03:B3:01:01</td>
      <td>02:B3:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>179</td>
      <td>Trail Length</td>
      <td>Set trail length (id: 179) to long (id: 2)</td>
      <td>03:B3:01:02</td>
      <td>02:B3:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>179</td>
      <td>Trail Length</td>
      <td>Set trail length (id: 179) to max (id: 3)</td>
      <td>03:B3:01:03</td>
      <td>02:B3:00</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>180</td>
      <td>Video Mode</td>
      <td>Set video mode (id: 180) to highest quality (id: 0)</td>
      <td>03:B4:01:00</td>
      <td>02:B4:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>180</td>
      <td>Video Mode</td>
      <td>Set video mode (id: 180) to extended battery (id: 1)</td>
      <td>03:B4:01:01</td>
      <td>02:B4:00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>180</td>
      <td>Video Mode</td>
      <td>Set video mode (id: 180) to extended battery (green icon) (id: 101)</td>
      <td>03:B4:01:65</td>
      <td>02:B4:00</td>
      <td><span style="color:red">❌</span></td>
      <td>\&gt;= v02.01.00</td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>180</td>
      <td>Video Mode</td>
      <td>Set video mode (id: 180) to longest battery (green icon) (id: 102)</td>
      <td>03:B4:01:66</td>
      <td>02:B4:00</td>
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
      <td rowspan="20"><a href="https://github.com/gopro/OpenGoPro/blob/main/docs/specs/capabilities.xlsx">capabilities.xlsx</a><br /><a href="https://github.com/gopro/OpenGoPro/blob/main/docs/specs/capabilities.json">capabilities.json</a></td>
      <td rowspan="5">HERO11 Black Mini</td>
      <td>v02.30.00</td>
    </tr>
    <tr>
      <td>v02.20.00</td>
    </tr>
    <tr>
      <td>v02.10.00</td>
    </tr>
    <tr>
      <td>v02.00.00</td>
    </tr>
    <tr>
      <td>v01.10.00</td>
    </tr>
    <tr>
      <td rowspan="5">HERO11 Black</td>
      <td>v02.10.00</td>
    </tr>
    <tr>
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


## Query
<p>
The camera provides two basic types of state information: Camera status and settings.
Camera status info includes information such as the current preset/mode, whether the system is busy or encoding, remaining sdcard space, etc.
Settings info gives the currently selected option for each setting; for example, this includes the current video resolution, frame rate, digital lens (FOV), etc.
</p>

<p>
Queries are sent to to GP-0076 and responses are received on GP-0077.
</p>

### Query Command Format
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Header/Length</td>
      <td>Query ID</td>
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
Note: omitting <i>:xx:...</i> from any (un)register command will result in being (un)registered for all associated values.
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
      <td>Get setting value(s)</td>
      <td>nn:12:xx:...</td>
      <td>nn -> message length<br/>xx -> setting ID</td>
    </tr>
    <tr>
      <td>0x12</td>
      <td>Get all setting values</td>
      <td>01:12</td>
      <td></td>
    </tr>
    <tr>
      <td>0x13</td>
      <td>Get status value(s)</td>
      <td>nn:13:xx:...</td>
      <td>nn -> message length<br/>xx -> status ID</td>
    </tr>
    <tr>
      <td>0x13</td>
      <td>Get all status values</td>
      <td>01:13</td>
      <td></td>
    </tr>
    <tr>
      <td>0x32</td>
      <td>Get available option IDs for setting(s)</td>
      <td>nn:32:xx:...</td>
      <td>nn -> message length<br/>xx -> setting ID</td>
    </tr>
    <tr>
      <td>0x32</td>
      <td>Get available option IDs for all settings</td>
      <td>01:32</td>
      <td></td>
    </tr>
    <tr>
      <td>0x52</td>
      <td>Register for setting(s) value updates</td>
      <td>nn:52:xx:...</td>
      <td>nn -> message length<br/>xx -> setting ID</td>
    </tr>
    <tr>
      <td>0x53</td>
      <td>Register for status value updates</td>
      <td>nn:53:xx:...</td>
      <td>nn -> message length<br/>xx -> status ID</td>
    </tr>
    <tr>
      <td>0x62</td>
      <td>Register for available option updates for setting(s)</td>
      <td>nn:62:xx:...</td>
      <td>nn -> message length<br/>xx -> setting ID</td>
    </tr>
    <tr>
      <td>0x72</td>
      <td>Unregister for setting updates</td>
      <td>nn:72:xx:...</td>
      <td>nn -> message length<br/>xx -> setting ID</td>
    </tr>
    <tr>
      <td>0x73</td>
      <td>Unregister for status updates</td>
      <td>nn:73:xx:...</td>
      <td>nn -> message length<br/>xx -> status ID</td>
    </tr>
    <tr>
      <td>0x82</td>
      <td>Unregister for available option updates for setting(s)</td>
      <td>nn:82:xx:...</td>
      <td>nn -> message length<br/>xx -> setting ID</td>
    </tr>
    <tr>
      <td>0x92</td>
      <td>Async notification when setting changes</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>0x93</td>
      <td>Async notification when status changes</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>0xA2</td>
      <td>Async notification when available option(s) changed</td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

### Query Response Format
<p>
There are two types of response notifications:
</p>

<ul>
<li><b>Type 1</b>: Notfication sent in direct response to a get-value or register command</li>
<li><b>Type 2</b>: Notification sent in response to data changing (must be registered to receive)</li>
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
      <td>1-2 bytes</td>
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
When receiving a query response that contains information about more than one setting/status
the <b>Status ID</b>, <b>Status Value Length</b>, and <b>Status Value</b> fields become collectively repeatable.
</p>

<p>
Example:
</p>

<p>
<code>
[MESSAGE LENGTH]:[QUERY ID]:[COMMAND STATUS]:[ID1]:[LENGTH1]:[VALUE1]:[ID2]:[LENGTH2]:[VALUE2]:...
</code>
</p>

#### Query ID in Notifications
<p>
In order to discern between a <b>Type 1</b> and a <b>Type 2</b> response, the camera changes the <b>Query ID</b> for <b>Type 2</b>:
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Query</td>
      <td>Query ID in Command</td>
      <td>Query ID in Notification</td>
    </tr>
    <tr>
      <td>Register for setting(s) value updates	</td>
      <td>0x52</td>
      <td>0x92</td>
    </tr>
    <tr>
      <td>Register for status value updates	</td>
      <td>0x53</td>
      <td>0x93</td>
    </tr>
    <tr>
      <td>Register for available option updates for setting(s)</td>
      <td>0x62</td>
      <td>0xA2</td>
    </tr>
  </tbody>
</table>

### Status IDs
<p>
Below is a table of supported status IDs.<br />
* Indicates that item is experimental<br />
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
      <td>Is the camera in AP Mode?</td>
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
      <td>Total SD card capacity in Kilobytes</td>
      <td>integer</td>
      <td>*</td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:red">❌</span></td>
      <td><span style="color:red">❌</span></td>
    </tr>
  </tbody>
</table>


# Protobuf

<p>
In order to maximize BLE bandwidth, some messages and their corresponding notifications utilize
<a href="https://developers.google.com/protocol-buffers">Google Protobuf (Protocol Buffers)</a>.
</p>

<p>
Open GoPro currently uses <a href="https://developers.google.com/protocol-buffers/docs/reference/proto2-spec">Protocol Buffers Version 2</a>.
</p>

<p>
Note: All Protobuf messages (i.e. payloads, which are serialized protobuf objects) must be packetized and wrapped with <a href="https://gopro.github.io/OpenGoPro/ble_2_0#packet-headers">Packet Headers</a> as outlined in this document.
</p>


## Protobuf Message Format

<p>
Protobuf communications with the camera differ from TLV-style communications.
Rather than having a Type, Length, and Value, GoPro protobuf messages utilize the following:
<ol>
<li>Feature ID: Indicates command type (e.g. command, setting, query)</li>
<li>Action ID: Specific camera action; value indicates whether message was sent or an (aync) notification was received</li>
<li>Value: Serialized protobuf object</li>
</ol>
</p>

### Requests Sent
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

### Notifications Received
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Message Length</td>
      <td>Feature ID</td>
      <td>Response Action ID</td>
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

<p>
See <a href="#parsing-responses">Parsing Responses</a> for details on how to detect and parse a protobuf response.
</p>

## Protobuf IDs
<p>
Below is a table that links Protobuf Feature/Action IDs together with the UUIDs to write to and Response UUIDs to read notifications from.
For additional details, see <a href="#services-and-characteristics">Services and Characteristics</a>.
</p>
<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Feature</td>
      <td>Feature ID</td>
      <td>Action IDs</td>
      <td>UUID</td>
      <td>Response UUID</td>
    </tr>
    <tr>
      <td>Network Management</td>
      <td>0x02</td>
      <td>0x02, 0x03, 0x04, 0x05, 0x0B, 0x0C, 0x82, 0x83, 0x84, 0x85</td>
      <td>GP-0091</td>
      <td>GP-0092</td>
    </tr>
    <tr>
      <td>Command</td>
      <td>0xF1</td>
      <td>0x69, 0x6B, 0x78, 0x79, 0xE9, 0xEB, 0xF8, 0xF9</td>
      <td>GP-0072</td>
      <td>GP-0073</td>
    </tr>
    <tr>
      <td>Query</td>
      <td>0xF5</td>
      <td>0x72, 0x74, 0xF2, 0xF3, 0xF4, 0xF5</td>
      <td>GP-0076</td>
      <td>GP-0077</td>
    </tr>
  </tbody>
</table>


## Protobuf Commands
<p>
Below is a table of protobuf commands that can be sent to the camera and their expected response.<br />
* Indicates that item is experimental<br />
<span style="color:green">✔</span> Indicates support for all Open GoPro firmware versions.<br />
<span style="color:red">❌</span> Indicates a lack of support for all Open GoPro firmware versions.<br />
>= vXX.YY.ZZ indicates support for firmware versions equal to or newer than vXX.YY.ZZ
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Feature ID</td>
      <td>Action ID</td>
      <td>Response Action ID</td>
      <td>Description</td>
      <td>Request</td>
      <td>Response</td>
      <td>HERO11 Black Mini</td>
      <td>HERO11 Black</td>
      <td>HERO10 Black</td>
      <td>HERO9 Black</td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td rowspan="7">0x02</td>
      <td>0x02</td>
      <td>0x82</td>
      <td>Start scan</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">RequestStartScan</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">ResponseStartScanning</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td></td>
      <td>0x0B</td>
      <td>Async status update</td>
      <td></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">NotifStartScanning</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x03</td>
      <td>0x83</td>
      <td>Get ap entries</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">RequestGetApEntries</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">ResponseGetApEntries</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x04</td>
      <td>0x84</td>
      <td>Connect</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">RequestConnect</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">ResponseConnect</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td></td>
      <td>0x0C</td>
      <td>Async status update</td>
      <td></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">ResponseConnect</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x05</td>
      <td>0x85</td>
      <td>Connect new</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">RequestConnectNew</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">ResponseConnectNew</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td></td>
      <td>0x0C</td>
      <td>Async status update</td>
      <td></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">NotifProvisioningState</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td rowspan="4">0xF1</td>
      <td>0x69</td>
      <td>0xE9</td>
      <td>Request set camera control status</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/set_camera_control_status.proto">RequestSetCameraControlStatus</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/response_generic.proto">ResponseGeneric</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td>\&gt;= v01.20.00</td>
      <td><span style="color:red">❌</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x6B</td>
      <td>0xEB</td>
      <td>Request set turbo active</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/turbo_transfer.proto">RequestSetTurboActive</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/response_generic.proto">ResponseGeneric</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x78</td>
      <td>0xF8</td>
      <td>Request release network</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">RequestReleaseNetwork</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">ResponseGeneric</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(245,249,255);">
      <td>0x79</td>
      <td>0xF9</td>
      <td>Request set live stream</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/live_streaming.proto">RequestSetLiveStreamMode</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/response_generic.proto">ResponseGeneric</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td rowspan="4">0xF5</td>
      <td>0x72</td>
      <td>0xF2</td>
      <td>Request get preset status</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/request_get_preset_status.proto">RequestGetPresetStatus</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/preset_status.proto">NotifyPresetStatus</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td></td>
      <td>0xF3</td>
      <td>Async status update</td>
      <td></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/preset_status.proto">NotifyPresetStatus</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td>0x74</td>
      <td>0xF4</td>
      <td>Request get live stream status</td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/live_streaming.proto">RequestGetLiveStreamStatus</a></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/live_streaming.proto">NotifyLiveStreamStatus</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
    <tr style="background-color: rgb(222,235,255);">
      <td></td>
      <td>0xF5</td>
      <td>Async status update</td>
      <td></td>
      <td><a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/live_streaming.proto">NotifyLiveStreamStatus</a></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
      <td><span style="color:green">✔</span></td>
    </tr>
  </tbody>
</table>


# Features

<p>
Below are details about Open GoPro features.
</p>


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
<li>(Un)register to be notified when a Preset is modified (e.g. resolution changes from 1080p to 4K) or a Preset Group is modified (e.g. presets are reordered/created/deleted)</li>
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

<p>
For details on which cameras are supported and how to get Preset Status, see <a href="#protobuf-commands">Protobuf Commands</a>.
</p>


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

<p>
For details on which cameras are supported and how to set Camera Control Status, see
<a href="#protobuf-commands">Protobuf Commands</a>.
</p>


## Interface with Access Points
<p>
The camera supports connecting to access points in <a href="https://en.wikipedia.org/wiki/Station_(networking)">Station Mode (STA)</a>.
This is necessary for features such as Live Streaming, where the camera needs an Internet connection.
While in this mode, HTTP command and control of the camera is not available on some cameras.
</p>

### Scanning for Access Points
<p>
In order to scan for Access Points, use the flow below.
See <a href="#protobuf-commands">Protobuf Commands</a> for command details.
</p>
```plantuml!


actor Central
participant "GP-0091" as GP0091
participant "GP-0092" as GP0092

Central  -> GP0091 : RequestStartScan
Central <-- GP0092 : ResponseStartScanning
note right
scanning_state: EnumScanning.SCANNING_STARTED
end note

loop until scanning_state == EnumScanning.SCANNING_SUCCESS
    Central <-- GP0092 : NotifStartScanning
end loop
note right
Indicates scan is complete
Save scan_id, total_entries
end note

Central  -> GP0091 : RequestGetApEntries
note right
Use scan_id, total_entries
end note
Central <-- GP0092 : ResponseGetApEntries
note right: Each ScanEntry contains SSID, signal strength, freq



```

### Scan Results
<p>
The <a href="#protobuf-commands">ResponseGetApEntries</a> message contains information about each discovered device.
This information includes the success of the scan, the scan id used in the original request, and a ScanEntry message, whose definition is nested inside ResponseGetApEntries.
</p>

<p>
A ScanEntry includes information about a discovered device including its SSID, relative signal strength, signal frequency,
and a bitmasked scan_entry_flags value whose individual bits are defined by <a href="https://github.com/gopro/OpenGoPro/blob/main/protobuf/network_management.proto">EnumScanEntryFlags</a>.
</p>

<p>
Note: When scan_entry_flags contains <b>SCAN_FLAG_CONFIGURED</b>, it is an indication that this network has already been provisioned.
</p>

### Connect to a New Access Point
<p>
To provision and connect the camera to a new Access Point, use <a href="#protobuf-commands">RequestConnectNew</a>.
</p>
<p>
Note: This should only be done once to provision the AP; subsequent connections should use <a href="#protobuf-commands">RequestConnect</a>. 
</p>
```plantuml!


actor Central
participant "GP-0091" as GP0091
participant "GP-0092" as GP0092

note over Central, GP0091: Scan for Access Points
Central  -> GP0091  : RequestConnectNew
Central <-- GP0092  : ResponseConnectNew
note right: provisioning_state: EnumProvisioning.PROVISIONING_STARTED

loop until provisioning_state == EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP
    Central <-- GP0092  : NotifProvisionState
end loop




```

### Connect to a Provisioned Access Point
<p>
To connect the camera to a provisioned Access Point, scan for Access Points and connect using <a href="#protobuf-commands">RequestConnect</a>:
</p>
```plantuml!


actor Central
participant "GP-0091" as GP0091
participant "GP-0092" as GP0092

note over Central, GP0091: Scan for Access Points
Central  -> GP0091  : RequestConnect
Central <-- GP0092  : ResponseConnect
note right: provisioning_state: EnumProvisioning.PROVISIONING_STARTED

loop until provisioning_state == EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP
    Central <-- GP0092  : NotifProvisionState
end loop




```

### Disconnect from an Access Point
<p>
To disconnect from a connected Access Point and return the camera to AP mode, use <a href="#protobuf-commands">RequestReleaseNetwork</a>.
</p>
```plantuml!


actor Central
participant "GP-0091" as GP0091
participant "GP-0092" as GP0092

note across: Scan for Access Points
note across: Connect to a New/Provisioned Access Point\n(Camera: STA Mode)
Central  -> GP0091  : RequestReleaseNetwork
Central <-- GP0092  : ResponseGeneric
note right: (Camera: AP Mode)




```


## Turbo Transfer
<p>
Some cameras support Turbo Transfer mode, which allows media to be downloaded over WiFi more rapidly.
This is done by temporarily modifying low-level settings in the OS to prioritize WiFi offload speeds.
</p>

<p>
When Turbo Transfer is active, theh camera displays an OSD indicating that media is being transferred in order to 
prevent the user from inadvertently changing settings or capturing media.
</p>

<p>
Turbo Transfer should only be used during media offload.
It is recommended that the user check for and--if necessary--disable Turbo Transfer on connect.
Developers can query whether the camera is currently in Turbo Transfer Mode from camera status 113.
</p>

<p>
Note:
<ul>
<li>Pressing MODE/POWER or Shutter buttons on the camera will deactivate Turbo Transfer feature.</li>
<li>Some cameras are already optimized for WiFi transfer and do not gain additional speed from this feature.</li>
</ul>
</p>

<p>
For details on which cameras are supported and how to enable and disable Turbo Transfer, see
<a href="#protobuf-commands">Protobuf Commands</a>.
</p>


## Live Streaming
<p>
The camera supports the ability to stream to social media platforms such as Twitch, YouTube, and Facebook or any other
site that accepts RTMP URLs. For additional details about getting started with RTMP, see
<a href="https://gopro.com/en/us/news/how-to-live-stream-on-gopro">How to Stream</a>.
</p>

### Overview
<p>
Live streaming with camera is accomplished as follows:
</p>

<ol>
<li>Put the camera into <b>Station Mode</b> and connect it to an access point (see <a href="#interface-with-access-points">Interface With Access Points</a>)</li>
<li>Set the <b>Live Stream Mode</b></li>
<li>Poll for <b>Live Stream Status</b> until the camera indicates it is ready</li>
<li>Set any desired settings (e.g. Hypersmooth)</li>
<li>Set the shutter to begin live streaming</li>
<li>Unset the shutter to stop live streaming</li>
</ol>

### Live Streaming Sequence
```plantuml!


actor Central
participant "GP-0091" as GP0091
participant "GP-0092" as GP0092
participant "GP-0072" as GP0072
participant "GP-0073" as GP0073
participant "GP-0074" as GP0074
participant "GP-0075" as GP0075
participant "GP-0076" as GP0076
participant "GP-0077" as GP0077

note over Central, GP0091: Set Live Stream Mode
Central  -> GP0072 : RequestSetLiveStreamMode
Central <-- GP0073 : ResponseGeneric

note over Central, GP0092: Poll Live Stream Status until ready
loop until LIVE_STREAM_STATE_READY
Central  -> GP0076 : RequestGetLiveStreamStatus
Central <-- GP0077 : NotifyLiveStreamStatus
end loop

note over Central, GP0091 : Set desired settings
loop until Desired camera state attained
Central  -> GP0074 : Set setting
Central <-- GP0075 : Response
end loop

note over Central, GP0091: Start live streaming!
Central  -> GP0072 : Set shutter
Central <-- GP0073 : response
note over Central, GP0091: Stop live streaming
Central  -> GP0072 : Unset shutter
Central <-- GP0073 : response




```

### Set Live Stream Mode
<p>
Setting the live stream mode is accomplished by sending a <b>RequestSetLiveStreamMode</b> command.
</p>

<p>
Command and enum details are available in <a href="#protobuf-commands">Protobuf Comands</a>.
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Parameter</td>
      <td>Type</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>url</td>
      <td>string</td>
      <td>RTMP url used to stream. Set to empty string to invalidate/cancel stream</td>
    </tr>
    <tr>
      <td>encode</td>
      <td>bool</td>
      <td>Whether to encode video to sdcard while streaming or not</td>
    </tr>
    <tr>
      <td>window_size</td>
      <td>EnumWindowSize</td>
      <td>Streaming video resolution</td>
    </tr>
    <tr>
      <td>cert</td>
      <td>string</td>
      <td>Certificate from a trusted root for streaming services that use encryption</td>
    </tr>
    <tr>
      <td>minimum_bitrate</td>
      <td>int32</td>
      <td>Desired minimum streaming bitrate (min possible: 800)</td>
    </tr>
    <tr>
      <td>maximum_bitrate</td>
      <td>int32</td>
      <td>Desired maximum streaming bitrate (max possible: 8000)</td>
    </tr>
    <tr>
      <td>starting_bitrate</td>
      <td>int32</td>
      <td>Initial streaming bitrate (honored if 800 <= value <= 8000)</td>
    </tr>
    <tr>
      <td>lens</td>
      <td>EnumLens</td>
      <td>Streaming Field of View</td>
    </tr>
  </tbody>
</table>

### Get Live Stream Status
<p>
Current status of the live stream is obtained by sending a <b>RequestGetLiveStreamStatus</b> command to the camera.
This command serves two purposes:
<ul>
<li>Get current state of the live stream</li> 
<li>(Un)register to be notified when live stream state changes</li>
</ul>
</p>

<p>
Responses and notifications come as a <b>NotifyLiveStreamStatus</b> message with properties outlined in the table below.
</p>

<p>
Command and enum details are available in <a href="#protobuf-commands">Protobuf Comands</a>.
</p>

<table border="1">
  <tbody>
    <tr style="background-color: rgb(0,0,0); color: rgb(255,255,255);">
      <td>Parameter</td>
      <td>Type</td>
      <td>Description</td>
    </tr>
    <tr>
      <td>live_stream_status</td>
      <td>EnumLiveStreamStatus</td>
      <td>Basic streaming state (idle, ready, streaming, failed, etc)</td>
    </tr>
    <tr>
      <td>live_stream_error</td>
      <td>EnumLiveStreamError</td>
      <td>Error codes for specific streaming errors</td>
    </tr>
    <tr>
      <td>live_stream_encode</td>
      <td>bool</td>
      <td>Whether camera is encoding video to sdcard while encoding or not</td>
    </tr>
    <tr>
      <td>live_stream_bitrate</td>
      <td>int32</td>
      <td>Current streaming bitrate (Kbps)</td>
    </tr>
    <tr>
      <td>live_stream_window_size_supported_array</td>
      <td>EnumWindowSize</td>
      <td>Defines supported streaming resolutions</td>
    </tr>
    <tr>
      <td>live_stream_encode_supported</td>
      <td>bool</td>
      <td>Does this camera support encoding while streaming?</td>
    </tr>
    <tr>
      <td>live_stream_max_lens_unsupported</td>
      <td>bool</td>
      <td>Does camera lack support for streaming with Max Lens feature?</td>
    </tr>
    <tr>
      <td>live_stream_minimum_stream_bitrate</td>
      <td>int32</td>
      <td>Minimum possible bitrate (static) (Kbps)</td>
    </tr>
    <tr>
      <td>live_stream_maximum_stream_bitrate</td>
      <td>int32</td>
      <td>Maximum possible bitrate (static) (Kbps)</td>
    </tr>
    <tr>
      <td>live_stream_lens_supported</td>
      <td>bool</td>
      <td>Does camera support multiple streaming FOVs?</td>
    </tr>
    <tr>
      <td>live_stream_lens_supported_array</td>
      <td>EnumLens</td>
      <td>Defines supported Field of View values</td>
    </tr>
  </tbody>
</table>
