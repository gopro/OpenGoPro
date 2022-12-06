:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

================
QuickStart Guide
================

.. warning:: This section assumes you have successfully :ref:`installed<Installation>` the package.


Open GoPro installs with several command line demos to demonstrate BLE and Wi-Fi. The source code for these example
can be found on `Github <https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control/open_gopro/demos>`_
or locally in `$INSTALL/open_gopro/demos` where $INSTALL can be found with:

.. code-block:: console

    $ pip show open-gopro

All of the CLI demos have command-line help via the `--help` parameter. All demos will log to the console as well
as write a more detailed log to a file (this file can be set with the `--log` parameter). The detailed log
is very helpful for diagnosing BLE / WiFi inconsistencies.

Photo Demo
----------

The `photo` demo will discover a GoPro camera, connect to it, take a photo, and then download the
photo to your local machine. To run, do:

.. code-block:: console

    $ gopro-photo

For more information, do:

.. code-block:: console

    $ gopro-photo --help
    usage: gopro-photo [-h] [-o OUTPUT] [-l LOG] [-i IDENTIFIER] [-w WIFI_INTERFACE] [-p]

    Connect to a GoPro camera, take a photo, then download it.

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                            Where to write the photo to. If not set, write to 'photo.jpg'
    -l LOG, --log LOG     Location to store detailed log
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the
                            default camera SSID. If not used, first discovered GoPro will be
                            connected to
    -w WIFI_INTERFACE, --wifi_interface WIFI_INTERFACE
                            System Wifi Interface. If not set, first discovered interface will be
                            used.
    -p, --password        Set to read sudo password from stdin. If not set, you will be prompted
                            for password if needed

Video Demo
----------

The video demo will discover a GoPro camera, connect to it, take a video for a given amount of time, and then
download the photo to your local machine. To run and capture a 2 second video, do:

.. code-block:: console

    $ gopro-video 2

For more information, do:

.. code-block:: console

    $ gopro-video --help
    usage: gopro-video [-h] [-o OUTPUT] [-l LOG] [-i IDENTIFIER] [-w WIFI_INTERFACE] [-p] record_time

    Connect to a GoPro camera, take a video, then download it.

    positional arguments:
    record_time           How long to record for

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                            Where to write the video to. If not set, write to 'video.mp4'
    -l LOG, --log LOG     Location to store detailed log
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the
                            default camera SSID. If not used, first discovered GoPro will be
                            connected to
    -w WIFI_INTERFACE, --wifi_interface WIFI_INTERFACE
                            System Wifi Interface. If not set, first discovered interface will be
                            used.
    -p, --password        Set to read sudo password from stdin. If not set, you will be prompted
                            for password if needed

Wired Webcam Demo
-----------------

The `webcam` demo will configure a GoPro (identified via serial number) as a webcam, start the webcam, and use
`OpenCV <https://pypi.org/project/opencv-python/>`_  to start a viewer to display the stream.

.. code-block:: console

    $ gopro-webcam

For more information, do:

.. code-block:: console

    usage: gopro-webcam [-h] [-l LOG] identifier

    Setup and view a GoPro webcam.

    positional arguments:
    identifier         Last 3 digits of GoPro serial number, which is the last 3 digits of the default camera SSID.

    options:
    -h, --help         show this help message and exit
    -l LOG, --log LOG  Location to store detailed log

Wireless Stream Demos
---------------------

The livestream and preview stream demos have been merged into the below GUI

API GUI Demo
-------------

.. warning::
    This is a work in progress and some complex responses are not yet easily viewed.

This is a GUI which allows the user to connect a camera and send any command, view status / setting
updates, view a video stream, and log sent / received messages. It can be started with:

.. code-block:: console

    $ gopro-gui

This will launch a camera chooser screen where the user can either manually enter a camera to connect to
or automatically connect to the first found camera. Once connected, the GUI will appear. Usages is as follows:

- Choose a command from the Command Pallette on the left

  - Note that besides supporting all of the commands from the Open GoPro API, there is also a "Compound" commands
    section which contains commands that combine API functionality. One of these, for example, is Livestream
    which will connect Wifi, configure and start livestreaming.
- Once chosen, enter the desired parameters in the entry form at the top middle
- In the same entry form, click the button to send the command
- The sent command and received response will be logged in the log in the bottom middle as well as any
  asynchronously received messages.
- Any log messages with a down arrow can be expanded to view their details
- Any received statuses, settings, and setting capabilities will be updated in the pane at the top right.

  - The most recently received updates will be highlighted in blue
- A network stream can be started using the video pane in the bottom right. This will automatically get started
  after sending the Livestream command

WiFi Demo
-----------

The `wifi` demo will discover a GoPro camera, connect to it, enable the camera'a WiFi AP, and then connect
to it via WiFi. This is useful if you want to send HTTP commands to it from some external source such as curl.

Note that this demo will run, thus maintaining the WiFi connection, until exited by pressing enter.

.. code-block:: console

    $ gopro-wifi

For more information, do:

.. code-block:: console

    $ gopro-wif --help
    usage: gopro-wifi [-h] [-l LOG] [-i IDENTIFIER] [-w WIFI_INTERFACE] [-p]

    Connect to a GoPro camera's Wifi Access Point.

    optional arguments:
    -h, --help            show this help message and exit
    -l LOG, --log LOG     Location to store detailed log
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the
                            default camera SSID. If not used, first discovered GoPro will be
                            connected to
    -w WIFI_INTERFACE, --wifi_interface WIFI_INTERFACE
                            System Wifi Interface. If not set, first discovered interface will be
                            used.
    -p, --password        Set to read sudo password from stdin. If not set, you will be prompted
                            for password if needed

Battery Demo
------------

This demo will continuously read the battery level (either via polling or registering fro notifications as
configured per the command line argument) and write
the results to a .csv file. To run, do:

.. code-block:: console

    $ gopro-log-battery

For more information, do:

.. code-block:: console

    $ gopro-log-battery --help
    usage: gopro-log-battery [-h] [-p POLL] [-l LOG] [-i IDENTIFIER]

    Connect to the GoPro via BLE only and continuously read the battery (either by polling or
    notifications).

    optional arguments:
    -h, --help            show this help message and exit
    -p POLL, --poll POLL  Set to poll the battery at a given interval. If not set, battery level
                            will be notified instead. Defaults to notifications.
    -l LOG, --log LOG     Location to store detailed log
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the
                            default camera SSID. If not used, first discovered GoPro will be
                            connected to
