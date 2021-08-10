:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

================
QuickStart Guide
================

.. warning:: This section assumes you have successfully :ref:`installed<Installation>` the package.


Open GoPro installs with several command line demos to demonstrate BLE and Wi-Fi. The source code for these example
can be found in `$INSTALL/demos` where $INSTALL can be found with:

.. code-block:: console

    $ pip show open-gopro

All of the demos have command-line help via the `--help` parameter. They also all log to the console as well
as write a more detailed log to a file (this file can be set with the `--log` parameter).

A Special Consideration for BlueZ
---------------------------------

The Bleak BLE controller does not currently support autonomous pairing for the BlueZ backend. So if you are using
BlueZ (i.e. Ubuntu, RaspberryPi, etc.), you need to first pair the camera from the command line as shown in the
`BlueZ tutorial <https://gopro.github.io/OpenGoPro/tutorials/bash/bluez>`_. There is work to add this feature
and progress can be tracked on the `Github Issue <https://github.com/gopro/OpenGoPro/issues/29>`_

Photo Demo
----------

The photo demo will discover a GoPro camera, connect to it, take a photo, and then download the
photo to your local machine.

.. code-block:: console

    $ gopro-photo

For more information, do:

.. code-block:: console

    $ gopro-photo --help
    usage: gopro-photo [-h] [-i IDENTIFIER] [-l LOG] [-o OUTPUT]

    Connect to a GoPro camera, take a photo, then download it.

    optional arguments:
    -h, --help            show this help message and exit
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered
                            GoPro will be connected to
    -l LOG, --log LOG     Location to store detailed log
    -o OUTPUT, --output OUTPUT
                            Where to write the photo to. If not set, write to 'photo.jpg'

Video Demo
----------

The video demo will discover a GoPro camera, connect to it, take a video for a given amount of time, and then download the
photo to your local machine.

.. code-block:: console

    $ gopro-video 2

For more information, do:

.. code-block:: console

    $ gopro-video --help
    usage: gopro-video [-h] [-i IDENTIFIER] [-l LOG] [-o OUTPUT] record_time

    Connect to a GoPro camera, take a video, then download it.

    positional arguments:
      record_time           How long to record for

    optional arguments:
      -h, --help            show this help message and exit
      -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered
                            GoPro will be connected to
      -l LOG, --log LOG     Location to store detailed log
      -o OUTPUT, --output OUTPUT
                            Where to write the video to. If not set, write to 'video.jpg'

Battery Demo
------------

The video demo will discover a GoPro camera, connect to it, take a video for a given amount of time, and then download the
photo to your local machine.

.. code-block:: console

    $ gopro-video 2

For more information, do:

.. code-block:: console

    $ gopro-video --help
    usage: gopro-video [-h] [-i IDENTIFIER] [-l LOG] [-o OUTPUT] record_time

    Connect to a GoPro camera, take a video, then download it.

    positional arguments:
        record_time           How long to record for

    optional arguments:
        -h, --help            show this help message and exit
        -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered
                            GoPro will be connected to
        -l LOG, --log LOG     Location to store detailed log
        -o OUTPUT, --output OUTPUT
                            Where to write the video to. If not set, write to 'video.jpg'

Video Demo
----------

The video demo will discover a GoPro camera, connect to it, take a video for a given amount of time, and then download the
photo to your local machine.

.. code-block:: console

    $ gopro-video 2

For more information, do:

.. code-block:: console

    $ gopro-video --help
    usage: gopro-video [-h] [-i IDENTIFIER] [-l LOG] [-o OUTPUT] record_time

    Connect to a GoPro camera, take a video, then download it.

    positional arguments:
      record_time           How long to record for

    optional arguments:
      -h, --help            show this help message and exit
      -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered
                            GoPro will be connected to
      -l LOG, --log LOG     Location to store detailed log
      -o OUTPUT, --output OUTPUT
                            Where to write the video to. If not set, write to 'video.jpg'

Stream Demo
-----------

The stream demo will discover a GoPro camera, connect to it, enable the preview stream, and then attempt to
launch VLC to view the stream. It will attempt to automatically discover VLC if it is not passed a location
for the VLC executable.

.. code-block:: console

    $ gopro-stream

For more information, do:

.. code-block:: console

    $ gopro-stream --help
    usage: gopro-stream [-h] [-i IDENTIFIER] [-l LOG] [-v VLC]

    Connect to a GoPro camera, enable the preview stream, then open VLC to view it.

    optional arguments:
    -h, --help            show this help message and exit
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered
                            GoPro will be connected to
    -l LOG, --log LOG     Location to store detailed log
    -v VLC, --vlc VLC     VLC location. If not set, the location will attempt to be automatically
                            discovered.

Big Demo
--------

This is a superset of the above demos as well as other functionality as shown below. It might not be
very useful to run this as a demo but the source code can be helpful for showing examples of various
behavior.

To run the demo;

.. code-block:: console

    $ gopro-demo

For more information, do:

.. code-block:: console

    $ gopro-demo --help
    usage: gopro-demo [-h] [-i IDENTIFIER] [-l LOG] [-v VLC]

    Connect to a GoPro camera via BLE and Wifi and do some things.

    optional arguments:
    -h, --help            show this help message and exit
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered
                            GoPro will be connected to
    -l LOG, --log LOG     Location to store detailed log
    -v VLC, --vlc VLC     VLC location. If not set, the location will attempt to be automatically
                            discovered.

The demo will perform the following, logging to the console as it goes as well as writing a
more detailed log to a file (this file can be set with the --log parameter):

#. Scan for advertising BLE Devices, displaying any it finds. Note it is possible to specify a device connect to via the --identifier CLI parameter.
#. Connect to the first GoPro BLE Device it finds (if not passed an identifier)
#. Read the Wifi SSID and password via BLE, then enable the WiFi access point
#. Connect to the camera Wifi
#. Dump the discovered BLE characteristics to a .csv file
#. Disable the shutter and Turbo mode
#. Get all statuses and settings
#. Get and print some statuses, settings, and capabilities individually
#. Register to receive push notifications of some statuses, settings, amnd capabilities
#. Take a picture
#. Take a video
#. Get the media list
#. Find a picture from the media list and download it
#. Find a video from the media list and download it
#. Get the media info for a video and a picture
#. Get GPMF data for a picture
#. Get the screen-nail of a video
#. Get telemetry data for a video
#. Get the thumbnail of a picture
#. Get the preset status
#. Cycle through resolutions, getting async notifications for push notifications that we registered for previously
#. Enable the live stream.
#. Attempt to open VLC to view the live stream. This should work if you installed VLC to the default location.
#. Sleep until a keyboard interrupt is received, then exit