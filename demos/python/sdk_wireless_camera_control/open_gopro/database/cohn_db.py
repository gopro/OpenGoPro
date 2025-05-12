# cohn_db.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

"""Database abstractions"""

import logging

from tinydb import Query, TinyDB

from open_gopro.models.general import CohnInfo

logger = logging.getLogger(__name__)


class CohnDb:
    """COHN Database

    Args:
        db (TinyDB): TinyDB storage to use
    """

    def __init__(self, db: TinyDB) -> None:
        self._db = db

    def insert_or_update_credentials(self, camera_id: str, cohn: CohnInfo) -> None:
        """Insert or update a (potentially incomplete) Cohn Credential

        When updating, empty fields on the passed in credentials will be ignored

        Args:
            camera_id (str): camera key to insert / update
            cohn (CohnInfo): credentials to insert / update
        """
        if credentials := self.search_credentials(camera_id):
            credentials = credentials + cohn
            logger.debug(f"Updating existing COHN db entry {camera_id} ==> {credentials}")
            self._db.update(
                fields={"serial": camera_id, "credentials": dict(credentials)},
                cond=Query().serial == camera_id,
            )
        else:
            logger.debug(f"Adding new COHN db entry {camera_id} ==> {credentials}")
            self._db.insert({"serial": camera_id, "credentials": dict(cohn)})

    def search_credentials(self, camera_id: str) -> CohnInfo | None:
        """Find credentials for a given camera identifier

        Args:
            camera_id (str): Camera identifier to search for

        Returns:
            CohnInfo | None: Credentials if found, otherwise None
        """
        asdict = self._db.search(Query().serial == camera_id)
        if asdict:
            return CohnInfo(**asdict[0]["credentials"])
        return None

    def delete_credentials(self, camera_id: str) -> None:
        """Delete credentials for a given camera identifier

        Args:
            camera_id (str): Camera identifier to use
        """
        self._db.remove(Query().serial == camera_id)
