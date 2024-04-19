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

.. tip:: There is a lot of useful logging throughout the Open GoPro package. See
    :ref:`troubleshooting <troubleshooting>` for more info.

Asyncio
=======

This package is `asyncio <https://docs.python.org/3/library/asyncio.html>`_-based which means that its awaitable
methods need to be called from an async coroutine. For the code snippets throughout this documentation, assume that this
is accomplished in the same manner as the demo scripts provided:

.. code-block:: python

    import asyncio

    async def main() -> None:
        # Put our code here

    if __name__ == "__main__":
        asyncio.run(main())

Opening
=======

Before communicating with a camera, the camera resource must be "opened". This can be done either with or without
the context manager. See the below sections for opening information specific to Wired / Wireless.

Wireless Opening
----------------

The Wireless GoPro client can be opened either with the context manager:

.. code-block:: python

    from open_gopro import WirelessGoPro

    async with WirelessGoPro() as gopro:
        print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
        # Send some messages now

\...or without the context manager:

.. code-block:: python

    from open_gopro import WirelessGoPro

    gopro = WirelessGoPro()
    await gopro.open()
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

    async with WiredGoPro() as gopro:
        print("Yay! I'm connected via USB, opened, and ready to send / get data now!")
        # Send some messages now

\...or without the context manager:

.. code-block:: python

    from open_gopro import WiredGoPro

    gopro = WiredGoPro()
    await gopro.open()
    print("Yay! I'm connected via USB, opened, and ready to send / get data now!")
    # Send some messages now

If, as above,  an identifier is not passed to the `WiredGoPro`, the mDNS server will be queried during opening to search
for a connected GoPro.

Common Opening
--------------

The GoPro's state can be checked via several properties.

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
message will block until the camera is ready. They are combined into the following ready state:

- :meth:`~open_gopro.gopro_base.GoProBase.is_ready`

For example,

.. code-block:: python

    async with WirelessGoPro() as gopro:
        # A naive check for it to be ready
        while not await gopro.is_ready:
            pass

To reiterate...it is not needed or recommended to worry about this as the internal state is managed automatically
by the `WirelessGoPro` instance. Just know that most commands will be (asynchronously) blocked until the camera is ready.

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
     - ✔️
     - ✔️
     - ❌
   * - :meth:`~open_gopro.gopro_base.GoProBase.http_setting`
     - ✔️
     - ✔️
     - ❌
   * - :meth:`~open_gopro.gopro_base.GoProBase.ble_command`
     - ❌
     - ✔️
     - ✔️
   * - :meth:`~open_gopro.gopro_base.GoProBase.ble_setting`
     - ❌
     - ✔️
     - ✔️
   * - :meth:`~open_gopro.gopro_base.GoProBase.ble_status`
     - ❌
     - ✔️
     - ✔️

In the case where a given group of messages is not supported, a `NotImplementedError` will be returned when
the relevant property is accessed.

All messages are communicated via one of two strategies:

- Performing synchronous :ref:`data operations<Synchronous Data Operations>` to send a message and receive a GoPro Response
- Registering for :ref:`asynchronous push notifications<Asynchronous Push Notifications>` and getting these after they are enqueued

.. note:: For the remainder of this document, the term (a)synchronous is in the context of communication with the camera.
    Do not confuse this with `asyncio`: all operations from the user's perspective are awaitable.

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
the method will await until a :ref:`response<handling responses>` is received.

Commands
^^^^^^^^

Commands are callable instance attributes of a Messages class instance
(i.e. :class:`~open_gopro.api.ble_commands.BleCommands` or
:class:`~open_gopro.api.http_commands.HttpCommands`), thus they can be called directly:

.. code-block:: python

    async with WirelessGoPro() as gopro:
        await gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        await gopro.http_command.set_shutter(shutter=Params.Toggle.DISABLE)

.. warning:: Most commands specifically require `keyword-only arguments <https://peps.python.org/pep-3102/>`_. You can
    not optionally use positional arguments in such cases as this will affect functionality.

Statuses
^^^^^^^^

Statuses are instances of a BleStatus(:class:`~open_gopro.api.builders.BleStatusFacade`). They can be read
synchronously using their `get_value` method as such:

.. code-block:: python

    async with WirelessGoPro() as gopro:
        is_encoding = await gopro.ble_status.encoding_active.get_value()
        battery = await gopro.ble_status.int_batt_per.get_value()

It is also possible to read all statuses at once via:

.. code-block:: python

    async with WirelessGoPro() as gopro:
        statuses = await gopro.ble_command.get_camera_statuses()

.. note::
    HTTP can not access individual statuses. Instead it can use
    :meth:`~open_gopro.api.http_commands.HttpCommands.get_camera_state`
    to retrieve all of them (as well as all of the settings) at once

Settings
^^^^^^^^

Settings are instances of a BleSetting(:class:`~open_gopro.api.builders.BleSettingFacade`)
or HttpSetting(:class:`~open_gopro.api.builders.HttpSetting`). They can be interacted synchronously in several
ways.

Their values can be read (via BLE only) using the `get_value` method as such:

.. code-block:: python

    async with WirelessGoPro() as gopro:
        resolution = await gopro.ble_setting.resolution.get_value()
        fov = await gopro.ble_setting.video_field_of_view.get_value()

It is also possible to read all settings at once via:

.. code-block:: python

    async with WirelessGoPro() as gopro:
        settings = await gopro.ble_command.get_camera_settings()

.. note::
    HTTP can not access individual settings. Instead it can use
    :meth:`~open_gopro.api.http_commands.HttpCommands.get_camera_state`
    to retrieve all of them (as well as all of the statuses) at once.

Depending on the camera's current state, settings will have differing capabilities. It is possible to query
the current capabilities for a given setting (via BLE only) using the `get_capabilities_values` method as such:

.. code-block:: python

    async with WirelessGoPro() as gopro:
        capabilities = await gopro.ble_setting.resolution.get_capabilities_values()

Settings' values can be set (via either BLE or WiFI) using the `set` method as such:

.. code-block:: python

    async with WirelessGoPro() as gopro:
        await gopro.ble_setting.resolution.set(Params.Resolution.RES_4K)
        await gopro.http_setting.fps.set(Params.FPS.FPS_30)

Asynchronous Push Notifications
-------------------------------

This section describes how to register for and handle asynchronous push notifications. This is only relevant for BLE.

It is possible to enable push notifications for any of the following:

- setting values via :meth:`~open_gopro.api.builders.BleSettingFacade.register_value_update`
- setting capabilities via :meth:`~open_gopro.api.builders.BleSettingFacade.register_capability_update`
- status values via :meth:`~open_gopro.api.builders.BleStatusFacade.register_value_update`

Firstly, the desired settings / ID must be registered for and given a callback to handle received notifications.

:meth:`~open_gopro.communicator_interface.BaseGoProCommunicator.register_update`.

Once registered, the camera will send a push notification when the relevant setting / status changes. These
responses will then be sent to the registered callback for handling.

It is possible to stop receiving notifications by issuing the relevant unregister command, i.e.:

- setting values via :meth:`~open_gopro.api.builders.BleSettingFacade.unregister_value_update`
- setting capabilities via :meth:`~open_gopro.api.builders.BleSettingFacade.unregister_capability_update`
- status values via :meth:`~open_gopro.api.builders.BleStatusFacade.unregister_value_update`

Here is an example of registering for and receiving FOV updates:

.. code-block:: python

    async def process_battery_notifications(update: types.UpdateType, value: int) -> None:
        if update == constants.StatusId.INT_BATT_PER:
            ...
        elif update == constants.StatusId.BATT_LEVEL:
            ...

    async with WirelessGoPro() as gopro:
        await gopro.ble_status.int_batt_per.register_value_update(process_battery_notifications)
        await gopro.ble_status.batt_level.register_value_update(process_battery_notifications)

.. note:: The `register_XXX_update` methods also return the current value / capabilities.

.. warning:: The coupling of command ID to command is not obvious. This is a temporary solution and will be improved upon
    in a future release.

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
(:class:`~open_gopro.models.response.GoProResp`) which is a container around a JSON serializable dict with some helper
functions.

Response Structure
------------------

A `GoProResp` has the following relevant attributes / properties for the end user:

- | :meth:`~open_gopro.models.response.GoProResp.identifier`: identifier of the completed operation.
  | This will vary based on what type the response is and will also contain the most specific identification information.

    - UUID if a direct BLE characteristic read
    - CmdId if an Open GoPro BLE Operation
    - endpoint string if a Wifi HTTP operation
- :meth:`~open_gopro.models.response.GoProResp.protocol`: the communication protocol where the response was received
- :meth:`~open_gopro.models.response.GoProResp.status`: the status returned from the camera
- :meth:`~open_gopro.models.response.GoProResp.data`: JSON serializable dict containing the responded data
- :meth:`~open_gopro.models.response.GoProResp.ok`: Is this a successful response?

The response object can be serialized to a JSON string with the default Python `str()` function. Note that
the `identifier` and `status` attributes are appended to the JSON.

For example, first let's connect, send a command, and then store the response:

.. code-block:: console

    >>> gopro = WirelessGoPro()
    >>> await gopro.open()
    >>> response = await (gopro.ble_setting.resolution).get_value()
    >>> print(response)

Now let's print the response (as JSON):

.. code-block:: console

    >>> print(response)
    {
        "id" : "QueryCmdId.GET_SETTING_VAL",
        "status" : "ErrorCode.SUCCESS",
        "protocol" : "Protocol.BLE",
        "data" : {
            "SettingId.RESOLUTION" : "Resolution.RES_4K_16_9",
        },
    }

Now let's inspect the responses various attributes / properties:

.. code-block:: console

    >>> print(response.status)
    ErrorCode.SUCCESS
    >>> print(response.ok)
    True
    >>> print(response.identifier)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.protocol)
    Protocol.BLE

Data Access
-----------

The response data is stored in the `data` attribute (:meth:`~open_gopro.models.response.GoProResp.data`) and its type
is specified via the Generic type specified in the corresponding command signature where the response is defined.

For example, consider :meth:`~open_gopro.api.ble_commands.BleCommands.get_hardware_info`. It's signature is:

.. code-block:: python

    async def get_hardware_info(self) -> GoProResp[CameraInfo]:
        ...

Therefore, its response's `data` property is of type :meth:`~open_gopro.models.general.CameraInfo`. Continuing the
example from above:


.. code-block:: console

    >>> gopro = WirelessGoPro(enable_wifi=False)
    >>> await gopro.open()
    >>> response = await gopro.ble_command.get_hardware_info()
    >>> print(response.data)
    {
        "model_number" : "62",
        "model_name" : "HERO12 Black",
        "firmware_version" : "H23.01.01.09.67",
        "serial_number" : "C3501324500702",
        "ap_mac_addr" : "2674f7f66104",
        "ap_ssid" : "GP24500702",
    }

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
    await gopro.open()
    print("Yay! I'm connected via BLE, Wifi, opened, and ready to send / get data now!")
    # When we're done...
    await gopro.close()
    # The camera resource is closed now!!

The `close` method will handle gracefully disconnecting BLE and Wifi.

.. warning::
    If the resource is not closed correctly, it is possible that your OS will maintain the BLE connection after
    the program exits. This will cause reconnection problems as your OS will not discover devices it is
    already connected to.