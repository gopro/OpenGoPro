:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

================
QuickStart Guide
================

.. warning:: This section assumes you have successfully :ref:`installed<Installation>` the package.

Open GoPro installs with several demos to demonstrate BLE and Wi-Fi. The source code for these examples
can be found on `Github <https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control/open_gopro/demos>`_
or locally in `$INSTALL/open_gopro/demos` where $INSTALL can be found with:

.. code-block:: console

    $ pip show open-gopro

Note that the GUI demos will only be available if OpenGoPro was installed with the additional GUI option.
See the  :ref:`installation<Installation>` steps for more informatoin.

Command Line Interface (CLI) Demos
==================================

All of the CLI demos have command-line help via the `--help` parameter. All demos will log to the console as well
as write a more detailed log to a file (this file can be set with the `--log` parameter). The detailed log
is very helpful for diagnosing BLE / WiFi inconsistencies.

Photo Demo
----------

The `photo` demo will discover a GoPro camera, connect to it, take a photo, and then download the
photo to your local machine. It defaults to connecting to a wireless camera but can connect to a wired camera
by setting the `wired` option. To run, do:

.. code-block:: console

    $ gopro-photo

For more information, do:

.. code-block:: console

    $ gopro-photo --help
    usage: gopro-photo [-h] [--output OUTPUT] [--wired] [--log LOG] [--identifier IDENTIFIER] [--wifi_interface WIFI_INTERFACE] [--password]

    Connect to a GoPro camera, take a photo, then download it.

    options:
    -h, --help            show this help message and exit
    --output OUTPUT       Where to write the photo to. If not set, write to 'photo.jpg'
    --wired               Set to use wired (USB) instead of wireless (BLE / WIFI) interface
    --log LOG             Location to store detailed log
    --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first
                            discovered GoPro will be connected to
    --wifi_interface WIFI_INTERFACE
                            System Wifi Interface. If not set, first discovered interface will be used.
    --password            Set to read sudo password from stdin. If not set, you will be prompted for password if needed

Video Demo
----------

The video demo will discover a GoPro camera, connect to it, take a video for a given amount of time, and then
download the photo to your local machine.  It defaults to connecting to a wireless camera but can connect to a
wired camera by setting the `wired` option.To run and capture a 2 second video, do:

.. code-block:: console

    $ gopro-video 2

For more information, do:

.. code-block:: console

    $ gopro-video --help
    usage: gopro-video [-h] [-o OUTPUT] [--wired] [--log LOG] [--identifier IDENTIFIER] [--wifi_interface WIFI_INTERFACE] [--password]
                    record_time

    Connect to a GoPro camera, take a video, then download it.

    positional arguments:
    record_time           How long to record for

    options:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                            Where to write the video to. If not set, write to 'video.mp4'
    --wired               Set to use wired (USB) instead of wireless (BLE / WIFI) interface
    --log LOG             Location to store detailed log
    --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first
                            discovered GoPro will be connected to
    --wifi_interface WIFI_INTERFACE
                            System Wifi Interface. If not set, first discovered interface will be used.
    --password            Set to read sudo password from stdin. If not set, you will be prompted for password if needed

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


Graphical User Interface (GUI) Demos
====================================

Wired Webcam Demo
-----------------

The `webcam` demo will configure a GoPro (identified via serial number) as a webcam, start the webcam, and use
`OpenCV <https://pypi.org/project/opencv-python/>`_  to start a viewer to display the stream.

.. code-block:: console

    $ gopro-webcam

For more information, do:

.. code-block:: console

    $ gopro-webcam --help
    usage: gopro-webcam [-h] [-i IDENTIFIER] [-l LOG]

    Setup and view a GoPro webcam.

    options:
    -h, --help            show this help message and exit
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 3 digits of GoPro serial number, which is the last 3 digits of the default camera SSID. If not specified, first
                            GoPro discovered via mDNS will be used
    -l LOG, --log LOG     Location to store detailed log

Livestream Demo
---------------

The `livestream` demo will connect via BLE to the camera, connect the camera to a Wifi AP, configure / start
livestream, then use `OpenCV <https://pypi.org/project/opencv-python/>`_  to start a viewer to display the stream.

.. code-block:: console

    $ gopro-webcam

For more information, do:

.. code-block:: console

    $ gopro-livestream --help
    usage: gopro-livestream [-h] [--min_bit MIN_BIT] [--max_bit MAX_BIT] [--start_bit START_BIT] [--resolution {4,7,12}] [--fov {0,4,3}]
                            [--log LOG] [--identifier IDENTIFIER]
                            ssid password url

    Connect to the GoPro via BLE only, configure then start a Livestream, then display it with CV2.

    positional arguments:
    ssid                  WiFi SSID to connect to.
    password              Password of WiFi SSID.
    url                   RTMP server URL to stream to.

    options:
    -h, --help            show this help message and exit
    --min_bit MIN_BIT     Minimum bitrate.
    --max_bit MAX_BIT     Maximum bitrate.
    --start_bit START_BIT
                            Starting bitrate.
    --resolution {4,7,12}
                            Resolution.
    --fov {0,4,3}         Field of View.
    --log LOG             Location to store detailed log
    --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first
                            discovered GoPro will be connected to
