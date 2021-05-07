===============
Troubleshooting
===============

This section will provide some information on how to debug the Open GoPro package.

Logging
-------

There is a lot of logging sprinkled throughout using the standard Python logging module.

Without getting too deep into the logging module, here is an example of activating logging on a per module
basis:

.. code-block:: python

    from open_gopro import GoPro
    import logging

    logger = logging.getLogger(__name__)

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)

    # Enable / disable logging in modules
    for module in ["gopro", "ble_commands", "wifi_commands", "responses"]:
        l = logging.getLogger(f"open_gopro.{module}")
        l.setLevel(logging.DEBUG)
        l.addHandler(stream_handler)

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

There is a utility in the GoProBLE class to dump the discovered BLE characteristics to a
CSV file. This can be done as such:

.. code-block:: python

    from open_gopro import GoPro

    with GoPro() as gopro:
        gopro.services_as_csv()