# requests_session.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

"""Helper methods for modifying SSL / requests configuration."""

import ssl
from pathlib import Path
from typing import Any

import requests
from requests.adapters import (
    DEFAULT_POOL_TIMEOUT,
    DEFAULT_POOLBLOCK,
    DEFAULT_POOLSIZE,
    DEFAULT_RETRIES,
    HTTPAdapter,
)


# In Python >= 3.13 , ssl.create_default_context() sets ssl.VERIFY_X509_PARTIAL_CHAIN and ssl.VERIFY_X509_STRICT as
# default flags. We need to remove these flags to allow GoPro cameras to work with the requests library.
def create_less_strict_requests_session(cert: Path) -> requests.Session:
    """Create a requests session with less strict SSL verification for GoPro cameras

    Args:
        cert(Path): Path to the CA certificate file to use for SSL verification

    Returns:
        requests.Session: A requests session with a custom SSL context
    """

    class CustomSSLAdapter(HTTPAdapter):
        """HTTPAdapter that allows customizing the SSL context"""

        def __init__(self, ssl_context: ssl.SSLContext, **kwargs: Any) -> None:
            self.ssl_context = ssl_context
            super().__init__(**kwargs)

        def init_poolmanager(self, *args: Any, **kwargs: Any) -> Any:
            """Initialize the pool manager with our custom SSL context"""
            if self.ssl_context:
                kwargs["ssl_context"] = self.ssl_context
            return super().init_poolmanager(*args, **kwargs)

    # Create a custom SSL context with the strict flags removed
    context = ssl.create_default_context(cafile=cert)

    # Remove the new strict verification flags
    context.verify_flags &= ~ssl.VERIFY_X509_PARTIAL_CHAIN
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT

    # Create a session and mount our custom adapter
    session = requests.Session()
    adapter = CustomSSLAdapter(ssl_context=context)
    session.mount("https://", adapter)

    return session
