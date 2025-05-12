"""Helper methods for modifying SSL / requests configuration."""

import ssl
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
def create_less_strict_requests_session() -> requests.Session:
    """Create a requests session with less strict SSL verification for GoPro cameras

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
    context = ssl.create_default_context()

    # Remove the new strict verification flags
    context.verify_flags &= ~ssl.VERIFY_X509_PARTIAL_CHAIN
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT

    # Create a session and mount our custom adapter
    session = requests.Session()
    adapter = CustomSSLAdapter(ssl_context=context)
    session.mount("https://", adapter)

    return session
