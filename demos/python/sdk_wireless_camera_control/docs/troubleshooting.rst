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
    import logging

    from open_gopro import GoPro
    from open_gopro.util import setup_logging

    logger = logging.getLogger(__name__)

    logger = setup_logging(logger, Path("my_log.log"))

    with GoPro() as gopro:
        logger.info("I'm logged!")

Here is a guide for the levels:

===================  =======================
    Logging Level      Module use
===================  =======================
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

    from open_gopro import GoPro

    with GoPro() as gopro:
        gopro._ble.services_as_csv()
