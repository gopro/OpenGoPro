:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

Usage
*****

This section will describe some high level information of how to use the Open GoPro module. For more detailed
information, see the :ref:`Interfaces<API Reference>` section. For just running the demos, see the
:ref:`QuickStart<QuickStart Guide>` section.

Overview
========

There are two top-level interfaces to communicate with a GoPro camera:

    - :class:`~open_gopro.gopro_wired.WiredGoPro` to communicate with the GoPro via USB HTTP
    - :class:`~open_gopro.gopro_wireless.WirelessGoPro` to communicate with the GoPro via BLE and optionally WiFi HTTP

An individual instance of one of the above classes corresponds to a (potentially not yet) connected GoPro
camera resource. The general procedure to communicate with the GoPro is:

1. Identify and :ref:`open<Opening>` the connection to the target GoPro
2. :ref:`Send Messages<Sending Messages>` and :ref:`Receive Responses<Handling Responses>` via BLE / HTTP
3. Gracefully :ref:`close<Closing>` the connection with the GoPro

.. tip:: There is a lot of logging throughout the Open GoPro package. See
    :ref:`troubleshooting <troubleshooting>` for more info.

Opening
=======

Before communicating with a camera, the camera resource must be "opened". This can be done either with or without
the context manager. See the below sections for opening information specific to Wired / Wireless.

Wireless Opening
----------------

The Wireless GoPro client can be opened either with the context manager:

.. code-block:: python

    from open_gopro import WirelessGoPro

    with WirelessGoPro() as gopro:
        print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
        # Send some messages now

\...or without the context manager:

.. code-block:: python

    from open_gopro import WirelessGoPro

    gopro = WirelessGoPro()
    gopro.open()
    print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
    # Send some messages now

In either case, the following will have occurred before the camera is ready to communicate:

#. scan for camera
#. connect to camera via BLE
#. enable notifications
#. pair (if needed)
#. discover characteristics
#. initialize (register for internal status notifications)
#. discover Open GoPro version
#. connect via WiFi (unless specified not to via argument)

.. note:: While a BLE connection is always needed, the WiFi connection is optional. To configure this (and other
    instance arguments) see the API Reference for :class:`~open_gopro.gopro_wireless.WirelessGoPro`

Wired Opening
-------------

The Wired GoPro client can be opened either with the context manager:

.. code-block:: python

    from open_gopro import WiredGoPro

    with WiredGoPro() as gopro:
        print("Yay! I'm connected via USB, opened, and ready to send / get data now!")
        # Send some messages now

\...or without the context manager:

.. code-block:: python

    from open_gopro import WiredGoPro

    gopro = WiredGoPro()
    gopro.open()
    print("Yay! I'm connected via USB, opened, and ready to send / get data now!")
    # Send some messages now

If an identifier is not passed to the `WiredGoPro`, the mDNS server will be queried during opening to search
for a connected GoPro.

Common Opening
--------------

The GoPro's state can be checked via several properties. All of the following will return True after a
successful opening:

-  :meth:`~open_gopro.gopro_base.GoProBase.is_ble_connected`
-  :meth:`~open_gopro.gopro_base.GoProBase.is_http_connected`
-  :meth:`~open_gopro.gopro_base.GoProBase.is_open`

API Version
^^^^^^^^^^^

One of the steps during the opening sequence is to query the camera's Open GoPro API version. This SDK only
supports Open GoPro API Version 2.0 so will raise an `InvalidOpenGoProVersion` if the connected camera is
using anything else.

The version string can be accessed via the :meth:`~open_gopro.gopro_base.GoProBase.version` property.

Camera Readiness
^^^^^^^^^^^^^^^^

A message can not be sent to the camera if it is not ready where "ready" is defined as not encoding and not
busy. These two states are managed automatically by the `WirelessGoPro` instance such that a call to any
message will block until the camera is ready. It is possible to check these from the application via:

- :meth:`~open_gopro.gopro_base.GoProBase.is_encoding`
- :meth:`~open_gopro.gopro_base.GoProBase.is_busy`

For example,

.. code-block:: python

    with GoPro() as gopro:
        # A naive check for it to be ready
        while gopro.is_encoding or gopro.is_ready:
            pass

To reiterate...it is not needed or recommended to worry about this as the internal state is managed automatically
by the `WirelessGoPro` instance.

Sending Messages
================

Once a `WirelessGoPro` or `WiredGoPro` instance has been :ref:`opened<opening>`, it is now possible to send
messages to the camera (provided that the camera is :ref:`ready<camera readiness>`).  Messages are accessed
by transport protocol where the superset of message groups are:

.. list-table::
   :widths: 50 50 50 50
   :header-rows: 1

   * - Message Group
     - WiredGoPro
     - WirelessGoPro (WiFi Enabled)
     - WirelessGoPro (WiFi Disabled)
   * - :meth:`~open_gopro.gopro_base.GoProBase.http_command`
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
   * - :meth:`~open_gopro.gopro_base.GoProBase.http_setting`
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
     - |:x:|
   * - :meth:`~open_gopro.gopro_base.GoProBase.ble_command`
     - |:x:|
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
   * - :meth:`~open_gopro.gopro_base.GoProBase.ble_setting`
     - |:x:|
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|
   * - :meth:`~open_gopro.gopro_base.GoProBase.ble_status`
     - |:x:|
     - |:heavy_check_mark:|
     - |:heavy_check_mark:|

In the case where a given group of messages is not supported, a `NotImplementedError` will be returned when
the relevant property is accessed.

All messages are communicated via one of two strategies:

- Performing synchronous :ref:`data operations<Synchronous Data Operations>` to send a message and receive a GoPro Response
- Registering for :ref:`asynchronous push notifications<Asynchronous Push Notifications>` and getting these after they are enqueued

Both of these patterns will be expanded upon below. But first, a note on selecting parameters for use with messages...

Selecting Parameters
--------------------

Whenever a parameter is required for a message, it will be type-hinted in the method definition as either a standard Python type
or an Enum from the :ref:`Params<parameters>` module.

Here is a full example for clarity:

.. code-block:: python

    from open_gopro import WirelessGoPro, Params

    with WirelessGoPro() as gopro:
        gopro.ble_command.set_shutter(Params.Toggle.ENABLE)

.. tip:: The message signature can also be found from the API Reference. For example, here is the documentation
    of the above message: :meth:`~open_gopro.api.ble_commands.BleCommands.set_shutter`


Synchronous Data Operations
---------------------------

.. note:: Unless explicitly specified in the :ref:`Asynchronous<Asynchronous Push Notifications>` section,
    all messages are synchronous messages.

This section refers to sending commands, getting settings / statuses, and setting settings. In all cases here,
the method will block until a :ref:`response<handling responses>` is received.

Commands
^^^^^^^^

Commands are callable instance attributes of a Messages class instance
(i.e. :class:`~open_gopro.api.ble_commands.BleCommands` or
:class:`~open_gopro.api.http_commands.HttpCommands`), thus they can be called directly:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_command.set_shutter(Params.Toggle.ENABLE)
        gopro.http_command.set_shutter(Params.Toggle.DISABLE)

Statuses
^^^^^^^^

Statuses are instances of a BleStatus(:class:`~open_gopro.api.builders.BleStatus`). They can be read
synchronously using their `get_value` method as such:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_status.encoding_active.get_value()
        gopro.ble_status.int_batt_per.get_value()

It is also possible to read all statuses at once via:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_command.get_camera_statuses()

.. note::
    HTTP can not access individual statuses. Instead it can use
    :meth:`~open_gopro.api.http_commands.HttpCommands.get_camera_state`
    to retrieve all of them (as well as all of the settings) at once

Settings
^^^^^^^^

Settings are instances of a BleSetting(:class:`~open_gopro.api.builders.BleSetting`)
or HttpSetting(:class:`~open_gopro.api.builders.HttpSetting`). They can be interacted synchronously in several
ways.

Their values can be read (via BLE only) using the `get_value` method as such:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_setting.resolution.get_value()
        gopro.ble_setting.video_field_of_view.get_value()

It is also possible to read all settings at once via:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_command.get_camera_settings()

.. note::
    HTTP can not access individual settings. Instead it can use
    :meth:`~open_gopro.api.http_commands.HttpCommands.get_camera_state`
    to retrieve all of them (as well as all of the statuses) at once.

Depending on the camera's current state, settings will have differing capabilities. It is possible to query
the current capabilities for a given setting (via BLE only) using the `get_capabilities_values` method as such:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_setting.resolution.get_capabilities_values()

Settings' values can be set (via either BLE or WiFI) using the `set` method as such:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_setting.resolution.set(Params.Resolution.RES_4K)
        gopro.http_setting.fps.set(Params.FPS.FPS_30)

Asynchronous Push Notifications
-------------------------------

This section describes how to register for and handle asynchronous push notifications. This is only relevant for BLE.

It is possible to enable push notifications for any of the following:

- setting values via :meth:`~open_gopro.api.builders.BleSetting.register_value_update`
- setting capabilities via :meth:`~open_gopro.api.builders.BleSetting.register_capability_update`
- status values via :meth:`~open_gopro.api.builders.BleStatus.register_value_update`

Firstly, the desired settings / id must be registered for.

Once registered, the camera will send a push notification when the relevant setting / status changes. These
responses are added to an internal queue of the `GoProBase` instance and can be retrieved via
:meth:`~open_gopro.gopro_wireless.WirelessGoPro.get_notification`.

It is possible to stop receiving notifications by issuing the relevant unregister command, i.e.:

- setting values via :meth:`~open_gopro.api.builders.BleSetting.unregister_value_update`
- setting capabilities via :meth:`~open_gopro.api.builders.BleSetting.unregister_capability_update`
- status values via :meth:`~open_gopro.api.builders.BleStatus.unregister_value_update`

Here is an example of registering for and receiving FOV updates:

.. code-block:: python

    from open_gopro import WirelessGoPro
    from open_gopro.constants import SettingId

    with WirelessGoPro() as gopro:
        current_fov = gopro.ble_setting.video_field_of_view.register_value_update().flatten
        print(f"Current FOV is {current_fov}")
        # Get updates until we get a FOV update
        while True:
            update = gopro.get_notification() # Block until update is received
            if SettingId.VIDEO_FOV in update:
                print(f"New resolution is {update[SettingId.VIDEO_FOV]}")
                break
        # We don't care about FOV anymore so let's stop receiving notifications
        gopro.ble_setting.video_field_of_view.unregister_value_update()

.. note:: The `register_XXX_update` methods will return the current value / capabilities. That is why we are
    printing the current value in the example above.

.. tip:: It is probably desirable to have a separate thread to retrieve these updates as the demo examples do.

It is also possible to register / unregister for **all** settings, statuses, and / or capabilities
via one API call using the following commands:

- register for all setting notifications via :meth:`~open_gopro.api.ble_commands.BleCommands.register_for_all_settings`
- register for all status notifications via :meth:`~open_gopro.api.ble_commands.BleCommands.register_for_all_statuses`
- register for all capability notifications via :meth:`~open_gopro.api.ble_commands.BleCommands.register_for_all_capabilities`
- unregister for all setting notifications via :meth:`~open_gopro.api.ble_commands.BleCommands.unregister_for_all_settings`
- unregister for all status notifications via :meth:`~open_gopro.api.ble_commands.BleCommands.unregister_for_all_statuses`
- unregister for all capability notifications via :meth:`~open_gopro.api.ble_commands.BleCommands.unregister_for_all_capabilities`

Handling Responses
==================

Unless otherwise stated, all commands, settings, and status operations return a `GoProResp`
(:class:`~open_gopro.responses.GoProResp`) which is a container around a JSON serializable dict with some helper
functions.

Response Structure
------------------

A `GoProResp` has 3 relevant attributes for the end user:

- | :meth:`~open_gopro.responses.GoProResp.identifier`: identifier of the completed operation.
  | This will vary based on what type the response is and will also contain the most specific identification information.

    - UUID if a direct BLE characteristic read
    - CmdId if an Open GoPro BLE Operation
    - endpoint string if a Wifi HTTP operation
- :meth:`~open_gopro.responses.GoProResp.status`: the status returned from the camera
- :meth:`~open_gopro.responses.GoProResp.data`: JSON serializable dict containing the responded data

Besides the `identifier` attribute which always contains the most specific identification information, there are properties
to attempt to access other identification information. If the property is not valid for the given response,
it will return `None`.

- :meth:`~open_gopro.responses.GoProResp.cmd`. Relevant for any BLE operation.
- :meth:`~open_gopro.responses.GoProResp.uuid`. Relevant for any BLE operation.
- :meth:`~open_gopro.responses.GoProResp.endpoint`. Relevant for any Wifi operation.

There is also a property to check that the `status` is Success:

- :meth:`~open_gopro.responses.GoProResp.is_ok`

The response object can be serialized to a JSON string with the default Python `str()` function. Note that
the `identifier` and `status` attributes are appended to the JSON.

For example, first let's connect, send a command, and then store the response:

.. code-block:: console

    >>> from open_gopro import WirelessGoPro
    >>> gopro = WirelessGoPro()
    >>> gopro.open()
    >>> response = gopro.ble_setting.resolution.get_value()

Now let's print the response (as JSON):

.. code-block:: console

    >>> print(response)
    {
        "status": "SUCCESS",
        "identifier": "UUID.CQ_QUERY_RESP::QueryCmdId.GET_SETTING_VAL",
        "SettingId.RESOLUTION": "RES_5_3_K"
    }

Now let's inspect the responses various attributes / properties:

.. code-block:: console

    >>> print(response.status)
    ErrorCode.SUCCESS
    >>> print(response.is_ok)
    True
    >>> print(response.identifier)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.cmd)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.uuid)
    UUID.CQ_QUERY_RESP


Data Access
-----------

The response data is stored in the `data` attribute (:meth:`~open_gopro.responses.GoProResp.data`) but can also
be accessed via dict access on the instance since `__getitem__` has been overridden. For example, the must
succinct way to access the current resolution from the response is:

.. code-block:: console

    >>> print(response[SettingId.RESOLUTION])
    RES_5_3_K

However, it is also possible to this as:

.. code-block:: console

    >>> print(response.data[SettingId.RESOLUTION])
    RES_5_3_K

Similarly, `__contains__`, `__keys__`, `__values__`, and `__items__` and `__iter__` have also been overridden to operate on the `data` attribute:

.. code-block:: console

    >>> SettingId.RESOLUTION in response
    True
    >>> [str(x) for x in response]
    ['SettingId.RESOLUTION']

.. note:: The `Open GoPro Documentation <https://gopro.github.io/OpenGoPro/>`_ should be referenced in regards
    to how to access the JSON for each response.

Value Flattening
----------------

For short responses, it is rather unwieldy to access the JSON dict as described above. Therefore, you can attempt to use the
`flatten` property (:meth:`~open_gopro.responses.GoProResp.flatten`) to flatten the data:

Continuing with our example above, where previously we accessed the responded resolution as:

.. code-block:: console

    >>> print(response[SettingId.RESOLUTION])
    RES_5_3_K

We can also do it as:

.. code-block:: console

    >>> print(response.flatten)
    RES_5_3_K

For example, we can get and print all resolution capabilities on one line via:

    >>> print(", ".join(gopro.ble_setting.resolution.get_capabilities_values().flatten))
    RES_4K, RES_2_7K, RES_2_7K_4_3, RES_1080, RES_4K_4_3, RES_5_K_4_3, RES_5_3_K

If the response data is anything other than a single value or a list, it can't be flattened and so the entire
data structure will be returned.

Flattening works well when getting a single value (from a get status / value) or a list of values (from a get
capabilities). This won't work for many cases.

For complex JSON structures, you will need to read through the
`Open GoPro API Documentation  <https://github.com/gopro/OpenGoPro/tree/main/docs/wifi>`_ for
parsing it. There will be some future work to turn these (at least the media list) into nice Python classes. But
for now, it will look ugly like this:

.. code-block:: python

    # Get list of media
    gopro.media_list = http_command.get_media_list().data["media"][0]["fs"]

Closing
=======

It is important to close the camera resource when you are done with it. This can be done in two ways. If the context
manager was used, it will automatically be closed when exiting, i.e.:

.. code-block:: python

    with WirelessGoPro() as gopro:
        # Do some things.
        pass
        # Then when finished...
    # The camera resource is closed now!!

Otherwise, you will need to manually call the `close` method, i.e.:

.. code-block:: python

    gopro = WirelessGoPro()
    gopro.open()
    print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
    # When we're done...
    gopro.close()
    # The camera resource is closed now!!

The `close` method will handle gracefully disconnecting BLE and Wifi.

.. warning::
    If the resource is not closed correctly, it is possible that your OS will maintain the BLE connection after
    the program exits. This will cause reconnection problems as your OS will not discover devices it is
    already connected to.