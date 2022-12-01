:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

API Reference
*************

This section is a reference for the Open GoPro Python Package API. The BLE / Wifi API's that
this package implements can be found in the Open GoPro documentation linked from :ref:`package summary<Summary>`

.. note::
   Not everything is exposed here. This section should only consist of the interface
   information that a user (not a developer) of the Open GoPro module should care about.

For a higher-level summary / usage, see the :ref:`usage<Usage>` section

.. warning::
   This documentation is not a substitute for the Open GoPro BLE and WiFi
   `specifications <https://gopro.github.io/OpenGoPro/>`_. That is, this interface shows how to use the various
   commands but is not an exhaustive source of information for what each command does. The Open GoPro specs
   should be used simultaneously with this document for development.

GoPro Client
============

There are the top-level GoPro client interfaces.

Wireless
--------

.. code-block:: python

    from open_gopro import WirelessGoPro

.. inheritance-diagram:: open_gopro.gopro.WirelessGoPro

.. autoclass:: open_gopro.gopro.WirelessGoPro

Wired
-----

.. code-block:: python

    from open_gopro import WiredGoPro

.. inheritance-diagram:: open_gopro.gopro.WiredGoPro

.. autoclass:: open_gopro.gopro.WiredGoPro

Open GoPro API
==============

These are both the base types that are used to implement the API (BLE Setting, Ble Status, etc.) and the
version-specific API's themselves.

These should not be imported directly and instead should be accessed using the relevant properties (`ble_command`,
`wifi_setting`, etc.) of a GoPro(:class:`open_gopro.gopro.WirelessGoPro`) instance.

Base Types
----------

These are the base types that are used to implement version-specific API's.

BLE Setting
^^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.BleSetting

.. autoclass:: open_gopro.api.builders.BleSetting
   :exclude-members: get_name, get_capabilities_names

BLE Status
^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.BleStatus

.. autoclass:: open_gopro.api.builders.BleStatus

HTTP Setting
^^^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.HttpSetting

.. autoclass:: open_gopro.api.builders.HttpSetting

BLE Commands
------------

.. inheritance-diagram:: open_gopro.api.ble_commands.BleCommands

.. autoclass:: open_gopro.api.ble_commands.BleCommands

BLE Settings
------------

.. inheritance-diagram:: open_gopro.api.ble_commands.BleSettings

.. autoclass:: open_gopro.api.ble_commands.BleSettings

BLE Statuses
------------

.. autoclass:: open_gopro.api.ble_commands.BleStatuses

HTTP Commands
-------------

.. autoclass:: open_gopro.api.http_commands.HttpCommands

HTTP Settings
-------------

.. autoclass:: open_gopro.api.http_commands.HttpSettings

Parameters
----------

All of these parameters can be accessed via:

.. code-block:: python

   from open_gopro import Params

.. automodule:: open_gopro.api.params
   :undoc-members:


Responses
=========

This can be imported via:

.. code-block:: python

   from open_gopro import GoProResp

.. autoclass:: open_gopro.responses.GoProResp


Constants
=========

These can be imported as:

.. code-block:: python

   from open_gopro import constants


.. automodule:: open_gopro.constants
   :undoc-members:
   :exclude-members: CmdType, GoProEnumMeta, GoProFlagEnum, ProducerType, ResponseType, enum_factory

Exceptions
==========

.. automodule:: open_gopro.exceptions
   :undoc-members:

Common Interface
================

.. autoclass:: open_gopro.gopro.GoProBase

.. automodule:: open_gopro.interface


BLE Interface
=============

.. automodule:: open_gopro.ble.controller

.. automodule:: open_gopro.ble.client

BLEServices
-----------

.. automodule:: open_gopro.ble.services

WiFi Interface
==============

.. automodule:: open_gopro.wifi.controller

.. automodule:: open_gopro.wifi.client
