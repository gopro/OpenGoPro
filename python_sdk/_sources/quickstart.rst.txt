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

A Special Consideration for BlueZ
---------------------------------

The Bleak BLE controller does not currently support autonomous pairing for the BlueZ backend. So if you are using
BlueZ (i.e. Ubuntu, RaspberryPi, etc.), you need to first pair the camera from the command line as shown in the
`BlueZ tutorial <https://gopro.github.io/OpenGoPro/tutorials/bash/bluez>`_. There is work to add this feature
and progress can be tracked on the `Github Issue <https://github.com/gopro/OpenGoPro/issues/29>`_

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

GUI Stream Demos
----------------

There are two small GUI to demonstrate live streaming and preview streaming. They can be invoked, respspectively,
as:

.. code-block:: console

    $ gopro-live-stream

and...

.. code-block:: console

    $ gopro-preview-stream

These GUI's will allow the user to enter stream parameters, connect to the first discovered camera, then start
the relevant streaming and display the video using `OpenCV <https://pypi.org/project/opencv-python/>`_

.. warning::
    For the livestream demo, it is assumed that the user has a url of a running RTMP server that they want to
    live stream to. If not, there is a script to use Docker to start a local server at $INSTALL/tools/start_rtmp_server.sh.
    Of course this assumes that Docker is installed and on the path.

WiFi Demo
-----------

The `wifi` demo will discover a GoPro camera, connect to it, enable the camera'a WiFi AP, and then connect
to it via WiFi. This is useful if you want to send HTTP commands to it from some external source such as curl.

Note that this demo will run, thus maintaining the WiFi connection, until exited via keyboard interrupt.

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
