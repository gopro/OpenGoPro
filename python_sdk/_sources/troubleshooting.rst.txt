:github_url: https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control

===============
Troubleshooting
===============

This section will provide some information on how to debug the Open GoPro package.

Logging
-------

There is a lot of logging sprinkled throughout using the standard Python logging module.

Furthermore, there is a help function in `util.py` that will enable logging with some default modules / levels.
All of the demos use this and here is an example:

.. code-block:: python

    from pathlib import Path

    from open_gopro import WirelessGoPro
    from open_gopro.util import setup_logging

    logger = setup_logging(__name__, Path("my_log.log"))

    async with WirelessGoPro() as gopro:
        logger.info("I'm logged!")

There are several other logging-related functions that extend and / or offer finer logging control.

Here is a guide for the levels:

===================  =======================
    Logging Level      Module use
===================  =======================
logging.TRACE        Custom logging level with even more information then debug. You should not need this.
logging.DEBUG        Maximum amount of information. Byte level tx / rx.
logging.INFO         String-level tx / rx. This is very readable.
logging.WARNING      Things that shouldn't have happened but won't break anything
logging.ERROR        This is bad and unrecoverable.
logging.CRITICAL     Not used.
===================  =======================


Bluetooth Characteristics
-------------------------

There is a utility in the GoPro class to dump the discovered BLE characteristics to a
CSV file. This can be done as such:

.. code-block:: python

    from open_gopro import WirelessGoPro

    with WirelessGoPro() as gopro:
        gopro._ble.gatt_db.dump_to_csv()
