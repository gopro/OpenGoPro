---
lesson: 1
permalink: '/tutorials/bash/bluez'
---

# BlueZ Bash Tutorial

This document will provide a walk-through tutorial to use [BlueZ](http://www.bluez.org/) to interact with the
[Open GoPro Interface](https://github.com/gopro/OpenGoPro).
It is ok not to have read the interface documentation first as we will describe it as needed here.
After completing this tutorial, you will need to reference it for future development.

# Requirements

## Hardware

1. A platform that is [supported by Bluez](http://www.bluez.org/about/)
1. A GoPro camera that is [supported by Open GoPro]({% link specs/ble.md %}#supported-cameras)

## Software

1. BlueZ must be installed. Follow the steps [here](https://www.maketecheasier.com/setup-bluetooth-in-linux/)

Test that installation was successful with:

```console
$ bluetoothctl --version
bluetoothctl: 5.58
```

# Basic BLE Tutorial

This tutorial will walk through a process of connecting to the GoPro via Bluetooth Low Energy
(BLE) and taking a picture / video.

First, invoke the bluetooth control tool from BlueZ with:

```console
$ bluetoothctl
Agent registered
[CHG] Controller FC:44:82:DD:5A:3F Pairable: yes
[bluetooth]#
```

## Advertise

Now, we need to ensure the camera is discoverable (i.e. it is advertising).
Ensure that the Camera is powered on, then select
Connections --> Connect Device --> Quik App

The screen should appear as such:

{% include figure image_path="/assets/images/tutorials/quik.png" alt="Quik" size="50%" caption="Camera is discoverable." %}

{% note %}
This step may vary slightly by camera
{% endnote %}

## Scan

{% tabs scan %}
{% tab scan Input %}

Next, we must find the GoPro Camera from BlueZ. Scan for devices via:

```console
[bluetooth]# scan on
```

As BlueZ discovers devices, it will display them to the console.

Click the output tab to see the output.

{% endtab %}
{% tab scan Output %}

```console
[bluetooth]# scan on
Discovery started
[CHG] Controller FC:44:82:DD:5A:3F Discovering: yes
[NEW] Device 6E:0A:B0:76:36:49 6E-0A-B0-76-36-49
[NEW] Device DF:34:ED:D1:DA:E8 GoPro 0456
[NEW] Device 26:A2:8C:82:74:6E 26-A2-8C-82-74-6E
[CHG] Device F8:A2:6D:4C:5D:E0 RSSI: -60
```

Among other devices, you should see `GoPro XXXX` where XXXX is the last four digits of
your camera's serial number. Take note of the address to the left of this string (**DF:34:ED:D1:DA:E8**
in the example above). This is how the camera will be identified via `bluetoothctl`.

{% endtab %}
{% endtabs %}

## Connect

{% tabs Connect %}
{% tab Connect Input %}

Now that we know the address to connect to, the next step is to establish a BLE connection
to the camera as such:

```console
[bluetooth]# connect DF:34:ED:D1:DA:E8
```

Click the output tab to see the output.

{% endtab %}
{% tab Connect Output %}

When the connection is successfully established, the list of services and characteristics
will be displayed as such:

We will make use of these attributes later on.

```console
[CHG] Device DF:34:ED:D1:DA:E8 Connected: yes
Connection successful
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0001
        00001801-0000-1000-8000-00805f9b34fb
        Generic Attribute Profile
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service000b
        00001804-0000-1000-8000-00805f9b34fb
        Tx Power
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service000b/char000c
        00002a07-0000-1000-8000-00805f9b34fb
        Tx Power Level
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service000e
        0000180f-0000-1000-8000-00805f9b34fb
        Battery Service
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service000e/char000f
        00002a19-0000-1000-8000-00805f9b34fb
        Battery Level
[NEW] Descriptor (Handle 0xea04)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service000e/char000f/desc0011
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012
        0000180a-0000-1000-8000-00805f9b34fb
        Device Information
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char0013
        00002a29-0000-1000-8000-00805f9b34fb
        Manufacturer Name String
[NEW] Characteristic (Handle 0xea8d)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char0015
        00002a24-0000-1000-8000-00805f9b34fb
        Model Number String
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char0017
        00002a25-0000-1000-8000-00805f9b34fb
        Serial Number String
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char0019
        00002a27-0000-1000-8000-00805f9b34fb
        Hardware Revision String
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char001b
        00002a26-0000-1000-8000-00805f9b34fb
        Firmware Revision String
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char001d
        00002a28-0000-1000-8000-00805f9b34fb
        Software Revision String
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char001f
        00002a23-0000-1000-8000-00805f9b34fb
        System ID
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char0021
        00002a2a-0000-1000-8000-00805f9b34fb
        IEEE 11073-20601 Regulatory Cert. Data List
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0012/char0023
        00002a50-0000-1000-8000-00805f9b34fb
        PnP ID
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0025
        b5f90001-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0025/char0026
        b5f90002-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0025/char0028
        b5f90003-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0025/char002a
        b5f90004-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0025/char002c
        b5f90005-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x32a4)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0025/char002c/desc002e
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0025/char002f
        b5f90006-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031
        0000fea6-0000-1000-8000-00805f9b34fb
        GoPro, Inc.
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0032
        b5f90072-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0034
        b5f90073-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x4174)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0034/desc0036
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0037
        b5f90074-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0039
        b5f90075-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x4b84)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0039/desc003b
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char003c
        b5f90076-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char003e
        b5f90077-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x5494)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char003e/desc0040
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0041
        b5f90078-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0043
        b5f90079-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x5da4)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031/char0043/desc0045
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0046
        b5f90090-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0046/char0047
        b5f90091-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0046/char0049
        b5f90092-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x6984)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0046/char0049/desc004b
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Primary Service (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service004c
        b5f90080-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service004c/char004d
        b5f90081-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x7274)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service004c/char004d/desc004f
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service004c/char0050
        b5f90082-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service004c/char0052
        b5f90083-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x8104)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service004c/char0052/desc0054
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Characteristic (Handle 0xe461)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service004c/char0055
        b5f90084-aa8d-11e3-9046-0002a5d5c51b
        Vendor specific
[NEW] Descriptor (Handle 0x8724)
        /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service004c/char0055/desc0057
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: 00001800-0000-1000-8000-00805f9b34fb
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: 00001801-0000-1000-8000-00805f9b34fb
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: 00001804-0000-1000-8000-00805f9b34fb
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: 0000180a-0000-1000-8000-00805f9b34fb
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: 0000180f-0000-1000-8000-00805f9b34fb
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: 0000fea6-0000-1000-8000-00805f9b34fb
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: b5f90001-aa8d-11e3-9046-0002a5d5c51b
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: b5f90080-aa8d-11e3-9046-0002a5d5c51b
[CHG] Device DF:34:ED:D1:DA:E8 UUIDs: b5f90090-aa8d-11e3-9046-0002a5d5c51b
[CHG] Device DF:34:ED:D1:DA:E8 ServicesResolved: yes
[CHG] Device DF:34:ED:D1:DA:E8 Appearance: 0x0080
[CHG] Device DF:34:ED:D1:DA:E8 Icon: computer
[NEW] Device 6C:4A:85:45:04:D4 6C-4A-85-45-04-D4
[GoPro 0456]#
```

{% endtab %}
{% endtabs %}

## Pair

The GoPro has encryption-protected characteristics which require us to pair before
writing to. Now that you are connected (the prompt should now show `GoPro XXXX` instead of
`bluetooth`), do:

```console
[GoPro 0456]# pair
Attempting to pair with DF:34:ED:D1:DA:E8
[CHG] Device DF:34:ED:D1:DA:E8 Paired: yes
Pairing successful
```

Once paired, the camera should beep and display "Connection Successful". Also,
the device should show up when querying `bluetoothctl` for paired devices:

```console
[GoPro 0456]# paired-devices
Device DF:34:ED:D1:DA:E8 GoPro 0456
```

{% tip %}
It is now no longer necessary to pair on subsequent connections.
{% endtip %}

## Enable Notifications

{% tabs notifications %}
{% tab notifications Enter Gatt Menu %}

As specified in the [Open GoPro Bluetooth API]({% link specs/ble.md %}#sending-and-receiving-messages), we must enable notifications for a given characteristic
to receive responses from it. First, let's enter the `gatt` submenu:

```console
[GoPro 0456]# menu gatt
Menu gatt:
Available commands:
-------------------
list-attributes [dev/local]                       List attributes
select-attribute <attribute/UUID>                 Select attribute
attribute-info [attribute/UUID]                   Select attribute
read [offset]                                     Read attribute value
write <data=xx xx ...> [offset] [type]            Write attribute value
acquire-write                                     Acquire Write file descriptor
release-write                                     Release Write file descriptor
acquire-notify                                    Acquire Notify file descriptor
release-notify                                    Release Notify file descriptor
notify <on/off>                                   Notify attribute value
clone [dev/attribute/UUID]                        Clone a device or attribute
register-application [UUID ...]                   Register profile to connect
unregister-application                            Unregister profile
register-service <UUID> [handle]                  Register application service.
unregister-service <UUID/object>                  Unregister application service
register-includes <UUID> [handle]                 Register as Included service in.
unregister-includes <Service-UUID><Inc-UUID>      Unregister Included service.
register-characteristic <UUID> <Flags=read,write,notify...> [handle] Register application characteristic
unregister-characteristic <UUID/object>           Unregister application characteristic
register-descriptor <UUID> <Flags=read,write...> [handle] Register application descriptor
unregister-descriptor <UUID/object>               Unregister application descriptor
back                                              Return to main menu
version                                           Display version
quit                                              Quit program
exit                                              Quit program
help                                              Display help about this program
export                                            Print environment variables
```

Go the the next tab to enable notifications

{% endtab %}
{% tab notifications Enable Notifications %}

Now, we need to enable notifications for the relevant characteristic.
In this demo, we will only be setting the shutter. This command is sent on the "Command Request"
characteristic and it's responses are received as notifications on the "Command Response"
characteristic. So we only care about the "Command Response"
characteristic which [has UUID]({% link specs/ble.md %}#services-and-characteristics)
`b5f90073-aa8d-11e3-9046-0002a5d5c51b`.

> You can see this UUID listed above when the connection was formed. All attributes can also be found again from bluetoothctl with `list-attributes`

To enable notifications, select the attribute then enable notifications:

```console
[GoPro 0456]# select-attribute b5f90073-aa8d-11e3-9046-0002a5d5c51b
[GoPro 0456:/service0031/char0034]# acquire-notify
[CHG] Attribute /org/bluez/hci0/dev_CA_D7_FF_49_B1_27/service0031/char0034 NotifyAcquired: yes
AcquireNotify success: fd 7 MTU 335
```

Since we are acquiring (using the BlueZ terminology as in the command) notifications, this means that we will
be alerted of responses when the characteristic is notified.

{% endtab %}
{% endtabs %}

**Quiz time! 📚 ✏️**

{% quiz
    question="How are responses to the Command Request characteristic received over BLE?"
    option="A:::As write responses to the Command Request characteristic"
    option="B:::As notifications of the Command Response characteristic"
    option="C:::There is no response since this characteristic is Write-without-Response"
    option="D:::They must be polled by reading the Command Response characteristic"
    correct="B"
    info="All GoPro commands follow the same behavior: a command is first sent on a request characteristic.
    The response is then notified on the response characteristic (assuming notifications are enabled)."
%}

{% quiz
    question="How often is it necessary to pair?"
    option="A:::Pairing must occur every time to ensure safe BLE communication"
    option="B:::We never need to pair as the GoPro does not require it to communicate"
    option="C:::Pairing only needs to occur once as BlueZ will automatically re-use the shared keys for future connections"
    correct="C"
    info="Pairing is only needed once (assuming neither side deletes the keys). If the
    GoPro deletes the keys (via Connections->Reset Connections or a factory reset), the devices will need to re-pair."
%}

## Sending Commands

Now that we are are connected, paired, and have enabled notifications, we can send commands.
The command we will be sending is [Set Shutter]({% link specs/ble.md %}#commands-quick-reference), which at byte level is:

| Command         |        Bytes        |
| --------------- | :-----------------: |
| Set Shutter Off | 0x03 0x01 0x01 0x00 |
| Set Shutter On  | 0x03 0x01 0x01 0x01 |

First, we need to choose the attribute to write to which is the "Command Request" characteristic
with UUID `b5f90072-aa8d-11e3-9046-0002a5d5c51b`. This is done via `select-attribute`:

```console
[GoPro 0456:/service0031/char0034]# select-attribute b5f90072-aa8d-11e3-9046-0002a5d5c51b
[GoPro 0456:/service0031/char0032]# attribute-info
Characteristic - Vendor specific
        UUID: b5f90072-aa8d-11e3-9046-0002a5d5c51b
        Service: /org/bluez/hci0/dev_DF_34_ED_D1_DA_E8/service0031
        Flags: write
```

{% success %}
As a bonus, you can then call "attribute-info" to verify that this characteristic is writeable.
{% endsuccess %}

### Send Commands

{% tabs shutter %}
{% tab shutter Set Shutter On %}

Now, let's write the bytes to turn the shutter on and start encoding!

```console
[GoPro 0456:/service0031/char0032]# write "0x03 0x01 0x01 0x01"
Attempting to write /org/bluez/hci0/dev_CA_D7_FF_49_B1_27/service0031/char0032
[CHG] /org/bluez/hci0/dev_CA_D7_FF_49_B1_27/service0031/char0034 Notification:
  02 01 00
```

You should hear the camera beep and it will either take a picture or start recording
depending on what mode it is in.

Also note that we have received the "Command Status" notification response from the
Command Response characteristic since we acquired it's notifications in [Enable Notifications]

If you are recording a video, go to the next tab to set the shutter off.

{% endtab %}
{% tab shutter Set Shutter Off %}

We can now set the shutter off:

```console
[GoPro 0456:/service0031/char0032]# write "0x03 0x01 0x01 0x00"
Attempting to write /org/bluez/hci0/dev_CA_D7_FF_49_B1_27/service0031/char0032
[CHG] /org/bluez/hci0/dev_CA_D7_FF_49_B1_27/service0031/char0034 Notification:
  02 01 00
```

{% endtab %}
{% endtabs %}

### Good Job!

{% success %}
Congratulations 🤙
{% endsuccess %}

You can now send any of the other BLE commands detailed in the Open GoPro documentation in
a similar manner.

# Troubleshooting

## GoPro Stops Advertising

Sometimes the GoPro will stop advertising. A quick fix at this point is to power cycle the camera
by pulling and then re-inserting the battery.

## Complete System Reset

BLE is a fickle beast. If at any point it is impossible to discover or connect to the camera,
perform the following.

1. Reset the camera by choosing Connections --> Reset Connections
2. Power cycle the bluetooth adapter:

    ```console
    [bluetooth]# power off
    Changing power off succeeded
    [CHG] Controller FC:44:82:DD:5A:3F Powered: no
    [CHG] Controller FC:44:82:DD:5A:3F Discovering: no
    [CHG] Controller FC:44:82:DD:5A:3F Class: 0x00000000
    [bluetooth]# power on
    [CHG] Controller FC:44:82:DD:5A:3F Class: 0x002c010c
    Changing power on succeeded
    [CHG] Controller FC:44:82:DD:5A:3F Powered: yes
    ```

3. Remove the GoPro from the paired devices:

    ```console
    [bluetooth]# paired-devices
    Device DF:34:ED:D1:DA:E8 GoPro 0456
    [bluetooth]# remove DF:34:ED:D1:DA:E8
    ```

4. Restart the procedure detailed above

## Logs

It is also possible to get some bluetooth system logs.

To enable debug information and view HCI Trace information from the Bluetooth Monitor:

```console
sudo sed -i 's/bluetoothd/bluetoothd \-d/g' /lib/systemd/system/bluetooth.service
sudo btmon
```

To view the DBus log (i.e. to see BlueZ messages):

```console
sudo dbus-monitor --system
```

You can search this for "bluez" but not every relevant Bluetooth message will include it.
