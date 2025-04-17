from tinydb import Query, TinyDB

import logging

from open_gopro.models.general import CohnInfo

logger = logging.getLogger(__name__)


class CohnDb:
    def __init__(self, db: TinyDB) -> None:
        self._db = db

    def insert_or_update_credentials(self, camera_id: str, cohn: CohnInfo) -> None:
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
        asdict = self._db.search(Query().serial == camera_id)
        if asdict:
            return CohnInfo(**asdict[0]["credentials"])
        else:
            return None

    def delete_credentials(self, camera_id: str) -> None:
        self._db.remove(Query().serial == camera_id)
