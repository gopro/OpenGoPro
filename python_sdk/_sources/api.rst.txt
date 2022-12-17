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

There are two top-level GoPro client interfaces - Wireless and Wired:

Wireless
--------

.. code-block:: python

    from open_gopro import WirelessGoPro

.. inheritance-diagram:: open_gopro.gopro_wireless.WirelessGoPro
   :parts: 1

.. autoclass:: open_gopro.gopro_wireless.WirelessGoPro
   :inherited-members:

Wired
-----

.. code-block:: python

    from open_gopro import WiredGoPro

.. inheritance-diagram:: open_gopro.gopro_wired.WiredGoPro
   :parts: 1

.. autoclass:: open_gopro.gopro_wired.WiredGoPro
   :inherited-members:

Open GoPro API
==============

These are both the base types that are used to implement the API (BLE Setting, Ble Status, etc.) and the
version-specific API's themselves.

These should not be imported directly and instead should be accessed using the relevant properties (`ble_command`,
`wifi_setting`, etc.) of a GoPro(:class:`open_gopro.gopro_base.GoProBase`) instance.

.. autoclass:: open_gopro.api.ble_commands.BleCommands
   :show-inheritance:

.. autoclass:: open_gopro.api.ble_commands.BleSettings
   :show-inheritance:

.. autoclass:: open_gopro.api.ble_commands.BleStatuses
   :show-inheritance:

.. autoclass:: open_gopro.api.http_commands.HttpCommands
   :show-inheritance:

.. autoclass:: open_gopro.api.http_commands.HttpSettings
   :show-inheritance:

Base Types
----------

BLE Setting
^^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.BleSetting
   :parts: 1

.. autoclass:: open_gopro.api.builders.BleSetting
   :exclude-members: get_name, get_capabilities_names

BLE Status
^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.BleStatus
   :parts: 1

.. autoclass:: open_gopro.api.builders.BleStatus

HTTP Setting
^^^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.HttpSetting
   :parts: 1

.. autoclass:: open_gopro.api.builders.HttpSetting

Message Bases
^^^^^^^^^^^^^

These are the base types that are used to implement version-specific API's. These are published for reference
but the end user should never need to use these directly.

.. autoclass:: open_gopro.interface.Message
   :show-inheritance:

.. autoclass:: open_gopro.interface.HttpMessage
   :show-inheritance:

.. autoclass:: open_gopro.interface.BleMessage
   :show-inheritance:

.. autoclass:: open_gopro.interface.Messages
   :show-inheritance:

.. autoclass:: open_gopro.interface.BleMessages
   :show-inheritance:

.. autoclass:: open_gopro.interface.HttpMessages
   :show-inheritance:

.. autoclass:: open_gopro.interface.MessageRules

.. autoclass:: open_gopro.interface.RuleSignature

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

.. autoclass:: open_gopro.gopro_base.GoProBase

.. autoclass:: open_gopro.interface.GoProBle

.. autoclass:: open_gopro.interface.GoProHttp

.. autoclass:: open_gopro.interface.GoProWifi

.. autoclass:: open_gopro.interface.GoProWiredInterface

.. autoclass:: open_gopro.interface.GoProWirelessInterface


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
