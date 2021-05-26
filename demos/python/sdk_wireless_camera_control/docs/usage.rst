:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

Usage
*****

This section will describe some high level information of how to use the Open GoPro module. For more detailed
information, see the :ref:`Interfaces<Interfaces>` section. For just running the demo, see the
:ref:`QuickStart Guide<QuickStart Guide>` section.

Overview
========

The top level interface is the :ref:`GoPro <GoPro>` class.

Once a `GoPro` instance is :ref:`connected and initialized<Connecting>`, it can be interacted with via:

- Performing synchronous :ref:`data operations<Synchronous Data Operations>` to send a command and receive a GoPro Response
- Registering for :ref:`push notifications<Asynchronous Push Notifications>` and getting these after they are enqueued

.. note:: There is a lot of logging throughout the Open GoPro package. See :ref:`troubleshooting <troubleshooting>` for more info.

Connecting
==========

A GoPro instance can be initialized with or without an "identifier" where the identifier is the last
4 digits of the GoPro name. The name can be found from the camera via Preferences-->About-->Camera Info-->Camera Name.
If no identifier is passed, the first discovered GoPro BLE device will be connected to.

If the context manager is used for initialization, this entire connection sequence can will be performed before returning the
constructed `GoPro` instance:

#. scan
#. connect via BLE
#. enable notifications
#. pair (if needed)
#. discover characteristics
#. initialize (register for internal status notifications)
#. connect via WiFi

.. code-block:: python

    from open_gopro import GoPro

    with GoPro() as gopro:
        print("Yay! I'm connected via BLE, Wifi, initialized, and ready to send / get data now!")
        gopro.ble_command.set_shutter(params.Shutter.OFF)

This can also be accomplished without the context manager using the `start` method as such:

.. code-block:: python

    from open_gopro import GoPro

    gopro = GoProBle()
    gopro.start()
    print("Yay! I'm connected via BLE, Wifi, initialized, and ready to send / get data now!")
    gopro.ble_command.set_shutter(params.Shutter.OFF)

Initialized
-----------

After either of the above sequences, the `GoPro` instance will be "Connected" and "Initialized". There are properties
to check any of these values:

.. code-block:: python

    print(gopro.is_ble_connected)
    print(gopro.is_wifi_connected)
    print(gopro.is_initialized)

It is required that the device is initialized before any data can be sent.

Synchronous Data Operations
===========================

This section refers to sending commands, getting settings / statuses, and setting settings. In all cases here,
the method will block until a response is received.

The structure is very similar for both BLE and Wifi as each interface is accessed from a `GoPro` attribute that
is a delegate of the relevant type of command:

For BLE:

- command: :attr:`open_gopro.gopro.GoPro.ble_command` of type :class:`open_gopro.ble_commands.BleCommands`
- setting: :attr:`open_gopro.gopro.GoPro.ble_setting` of type :class:`open_gopro.ble_commands.BleSettings`
- status: :attr:`open_gopro.gopro.GoPro.ble_status` of type :class:`open_gopro.ble_commands.BleStatuses`

For WiFI:

- command: :attr:`open_gopro.gopro.GoPro.wifi_command` of type :class:`open_gopro.wifi_commands.WifiCommands`
- setting: :attr:`open_gopro.gopro.GoPro.wifi_setting` of type :class:`open_gopro.wifi_commands.WifiSettings`

There are two patterns here which are described below.

Commands
--------

Commands are instance methods of a Commands class instance (:class:`open_gopro.ble_commands.BleCommands` or
:class:`open_gopro.wifi_commands.WifiCommands`), thus they can be called directly:

.. code-block:: python

    with GoPro() as gopro:
        gorpo.ble_command.set_third_party_client_info()
        gorpo.ble_command.set_shutter(params.Shutter.OFF)
        gorpo.wifi_command.get_camera_state()
        gorpo.wifi_command.set_preset(params.Preset.PHOTO)

Settings and Statuses
---------------------

Each setting or status is an instance of a Status or Setting class that contains multiple methods.

BLE Status
^^^^^^^^^^

For BLE status (:class:`open_gopro.ble_commands.Status`), these methods are:

- get_value()
- register_value_update()
- unregister_value_update()

So, to interact with the encoding_active status:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_status.encoding_active.get_value()
        gopro.ble_status.encoding_active.register_value_update()

BLE Settings
^^^^^^^^^^^^

For BLE settings (:class:`open_gopro.ble_commands.Setting`), these methods are:

- get_capabilities_values()
- get_value()
- register_capability_update()
- register_value_update()
- set()
- unregister_capability_update()
- unregister_value_update()

So, to interact with the resolution setting:

.. code-block:: python

    with GoPro() as gopro:
        gopro.ble_setting.resolution.get_value()
        gopro.ble_setting.resolution.get_capabilities_values()
        gopro.ble_setting.resolution.register_value_update()
        gopro.ble_setting.resolution.register_capability_update()
        gopro.ble_setting.resolution.set(params.Resolution.RES_1080)

WiFi Settings
^^^^^^^^^^^^^

For WiFi settings (:class:`open_gopro.wifi_commands.Setting`), WiFi can only individually "set" a setting. So,
to interact with the resolution setting:

.. code-block:: python

    with GoPro() as gopro:
        gopro.wifi_setting.resolution.set(params.Resolution.RES_1080)
        gopro.wifi_setting.resolution.set(params.Resolution.RES_1440)

It can get values of all settings (with all statuses) at once as described below.

WiFi Status
^^^^^^^^^^^

WiFi can not acess individual statuses. Instead it can use the :meth:`open_gopro.wifi_commands.WifiCommands.get_camera_state`
command to retrieve all of them (as well as all of the settings) at once:

.. code-block:: python

    gopro.state = wifi_command.get_camera_state()

The response is a JSON dict. See :ref:`handling responses<Handling Responses>` for more information on how to handle this.

Asynchronous Push Notifications
===============================

This section describes how to handle asynchronous push notifications. This is only relevant for BLE.

It is possible to enable push notificaitons for any of the following:

- setting values
- setting capabilities
- status values

Firstly, the response to a register command for any of the above will include the current value / capabilities.

Then once registered, the camera will send a push notification when the relevant setting / status changes. These
responses are added to an internal `GoPro` instance queue and can be retrieved from the client via
:meth:`open_gopro.gopro.get_update`. Here is an example of registering for FOV updates:

.. code-block:: python

    with GoPro() as gopro:
        current_fov = gopro.ble_setting.video_field_of_view.register_value_update().flatten
        print(f"Current FOV is {current_fov}")
        # Get updates until we get a FOV update
        while True:
            update = gopro.get_update()
            if SettingId.VIDEO_FOV in update:
                print(f"New resolution is {update[SettingId.VIDEO_FOV]}")
                break

.. note:: It is probably desirable to have a separate thread to retrieve these updates as the demo example is doing.

Selecting Parameters
====================

Whenever a parameter is required, it will be type-hinted in the method definition to either a basic Python type
or an Enum in :ref:`Params <Parameters>`

All of these enums can be accessed by importing params:

.. code-block:: python

    from open_gopro import params

Any decent editor should make this easy to use without referencing the documentation. For example, if I am
trying to turn off the shutter, I can see that I need to pass in a `Shutter` param.

.. image:: _static/shows_param_type.png
    :width: 80%

I can then type in the `Shutter` param type and see the options:

.. image:: _static/valid_params.png
    :width: 60%

Handling Responses
==================

Unless otherwise stated, all commands, settings, and status operations return a GoProResp
which is basically a JSON serializable dict with some helper functions.

The `Open GoPro Documentation <https://github.com/gopro/OpenGoPro>`_ should be referenced in regards to how to access the JSON.

Response Structure
------------------

It has 3 relevant attributes for the end user:

- id: identifier of the completed operation. This will vary based on what type the response is.
    - UUID if a direct BLE characteristic read
    - CmdId if an Open GoPro BLE Operation
    - string if a Wifi HTTP operation
- status: the status returned from the camera
- data: JSON serializable dict

Besides the `id` attribute, there are properties to attempt to access specific identification information. If
the property is not valid for the given response, it will return `None`.

- command: :meth:`open_gopro.responses.GoProResp.cmd`
- uuid: :meth:`open_gopro.responses.GoProResp.uuid`
- endpoint: :meth:`open_gopro.responses.GoProResp.endpoint`

There is also a property to check that the `status` is Success:

- is_ok: :meth:`open_gopro.responses.GoProResp.is_ok`

The response object can be serialized to a JSON string with the default Python str() function. Note that the id and
status attributes are appended to the JSON. For example,

.. code-block:: console

    >>> response = ble_setting.resolution.get_value()
    >>> print(response.status)
    ErrorCode.SUCCESS
    >>> print(response.is_ok)
    True
    >>> print(response.id)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.cmd)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.uuid)
    UUID.CQ_QUERY_RESP
    >>> print(response.data)
    {
        "status": "SUCCESS",
        "id": "UUID.CQ_QUERY_RESP::QueryCmdId.GET_SETTING_VAL",
        "SettingId.RESOLUTION": [
            "RES_1080"
        ]
    }

Data Access
-----------

The data is stored in the `data` attribute but can also be accessed via dict access on the instance
since `__getitem__` has been overloaded. For example:

.. code-block:: console

    >>> print(response.data[SettingId.RESOLUTION])
    RES_5k

could also be done as:

.. code-block:: console

    >>> print(response[SettingId.RESOLUTION])
    RES_5k

Similarly, `__contains__` and `__iter__` have also been overloaded to operate on the `data` attribute:

.. code-block:: console

    >>> print(SettingId.RESOLUTION in response.data)

Value Flattening
----------------

For short responses, it is rather unwieldy to access the JSON dict. Therefore, you can attempt to use the
`flatten` property (:meth:`open_gopro.responses.GoProResp.flatten`) to attempt to flatten the data:

.. code-block:: console

    print(ble_setting.resolution.get_value().flatten)
    RES_5k
    print(", ".join(ble_setting.resolution.get_capabilities_values().flatten))
    RES_4k, RES_2_7k, RES_2_7k_4_3, RES_1440, RES_1080, RES_4k_4_3, RES_5k

If the response data is anything other than a single value or a list, it can't be flattened and so the entire
data structure will be returned.

This works well when getting a single value (from a get status / value) or a list of values (from a get
capabilities). This won't work for many cases.

For complex JSON structures, you will need to read through the
`Open GoPro API Documentation  <https://github.com/gopro/OpenGoPro/tree/main/docs/wifi>`_ for
parsing it. There may be some future work to turn these (at least the media list) into nice Python classes. But
for now, it will look ugly like this:

.. code-block:: python

    # Get list of media
    gopro.media_list = wifi_command.get_media_list().data["media"][0]["fs"]