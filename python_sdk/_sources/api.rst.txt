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

.. autoclass:: open_gopro.api.ble_settings.BleSettings
   :show-inheritance:

.. autoclass:: open_gopro.api.ble_statuses.BleStatuses
   :show-inheritance:

.. autoclass:: open_gopro.api.http_commands.HttpCommands
   :show-inheritance:

.. autoclass:: open_gopro.api.http_settings.HttpSettings
   :show-inheritance:

Abstracted Features
-------------------

.. automodule:: open_gopro.features.cohn_feature

.. automodule:: open_gopro.features.access_point_feature

Base Types
----------

.. automodule:: open_gopro.domain.types

GoPro Enum
^^^^^^^^^^

.. autoclass:: open_gopro.domain.enum.GoProEnum

.. autoclass:: open_gopro.domain.enum.GoProIntEnum

BLE Setting
^^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.BleSettingFacade
   :parts: 1

.. autoclass:: open_gopro.api.builders.BleSettingFacade
   :exclude-members: get_name, get_capabilities_names

BLE Status
^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.BleStatusFacade
   :parts: 1

.. autoclass:: open_gopro.api.builders.BleStatusFacade

HTTP Setting
^^^^^^^^^^^^

.. inheritance-diagram:: open_gopro.api.builders.HttpSetting
   :parts: 1

.. autoclass:: open_gopro.api.builders.HttpSetting

Method Protocols
^^^^^^^^^^^^^^^^

.. autoclass:: open_gopro.api.builders.BuilderProtocol

Message Bases
^^^^^^^^^^^^^

These are the base types that are used to implement version-specific API's. These are published for reference
but the end user should never need to use these directly.

.. autoclass:: open_gopro.domain.communicator_interface.Message
   :show-inheritance:

.. autoclass:: open_gopro.domain.communicator_interface.HttpMessage
   :show-inheritance:

.. autoclass:: open_gopro.domain.communicator_interface.BleMessage
   :show-inheritance:

.. autoclass:: open_gopro.domain.communicator_interface.Messages
   :show-inheritance:

.. autoclass:: open_gopro.domain.communicator_interface.BleMessages
   :show-inheritance:

.. autoclass:: open_gopro.domain.communicator_interface.HttpMessages
   :show-inheritance:

.. autoclass:: open_gopro.domain.communicator_interface.MessageRules

Observables
^^^^^^^^^^^

.. automodule:: open_gopro.domain.observable
   :show-inheritance:

.. autoclass:: open_gopro.domain.gopro_observable.GoproObserverDistinctInitial
   :show-inheritance:

.. autoclass:: open_gopro.domain.gopro_observable.GoProObservable
   :show-inheritance:
   :inherited-members:

Responses
=========

Generic common response container:

This can be imported via:

.. code-block:: python

   from open_gopro import GoProResp

.. autoclass:: open_gopro.models.response.GoProResp

Data Models
-----------

These are the various models that are returned in responses, used in commands, etc. They can be imported with:

.. code-block:: python

   from open_gopro import models

.. autopydantic_model:: open_gopro.models.media_list.MediaPath

.. autopydantic_model:: open_gopro.models.media_list.MediaMetadata

.. autopydantic_model:: open_gopro.models.media_list.PhotoMetadata
   :show-inheritance:

.. autopydantic_model:: open_gopro.models.media_list.VideoMetadata
   :show-inheritance:

.. autopydantic_model:: open_gopro.models.media_list.MediaItem

.. autopydantic_model:: open_gopro.models.media_list.GroupedMediaItem
   :show-inheritance:

.. autopydantic_model:: open_gopro.models.media_list.MediaFileSystem

.. autopydantic_model:: open_gopro.models.media_list.MediaList

.. autopydantic_model:: open_gopro.models.general.TzDstDateTime

.. autopydantic_model:: open_gopro.models.general.CameraInfo

.. autopydantic_model:: open_gopro.models.general.WebcamResponse

.. autopydantic_model:: open_gopro.models.general.SupportedOption

.. autopydantic_model:: open_gopro.models.general.CohnInfo

.. autoclass:: open_gopro.models.general.ScheduledCapture

Constants
=========

These can be imported as:

.. code-block:: python

   from open_gopro import constants

.. automodule:: open_gopro.models.constants
   :undoc-members:
   :exclude-members: CmdType, GoProEnumMeta, GoProFlagEnum, ProducerType, ResponseType, enum_factory

.. automodule:: open_gopro.models.constants.constants
   :undoc-members:

.. automodule:: open_gopro.models.constants.settings
   :undoc-members:

.. automodule:: open_gopro.models.constants.statuses
   :undoc-members:

Exceptions
==========

.. automodule:: open_gopro.domain.exceptions
   :undoc-members:

Common Interface
================

.. automodule:: open_gopro.domain.parser_interface

.. autoclass:: open_gopro.gopro_base.GoProBase

.. autoclass:: open_gopro.domain.communicator_interface.GoProBle

.. autoclass:: open_gopro.domain.communicator_interface.GoProHttp

.. autoclass:: open_gopro.domain.communicator_interface.GoProWifi

.. autoclass:: open_gopro.domain.communicator_interface.GoProWiredInterface

.. autoclass:: open_gopro.domain.communicator_interface.GoProWirelessInterface

.. autoclass:: open_gopro.domain.communicator_interface.BaseGoProCommunicator


BLE Interface
=============

.. automodule:: open_gopro.network.ble.controller

.. automodule:: open_gopro.network.ble.client

BLEServices
-----------

.. automodule:: open_gopro.network.ble.services

WiFi Interface
==============

.. automodule:: open_gopro.network.wifi.controller

.. automodule:: open_gopro.network.wifi.client
