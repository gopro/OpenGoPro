from tinydb import Query, TinyDB

from open_gopro.models.general import CohnInfo


class CohnDb:
    def __init__(self, db: TinyDB) -> None:
        self._db = db

    def insert_or_update_credentials(self, camera_id: str, cohn: CohnInfo) -> None:
        if credentials := self.search_credentials(camera_id):
            credentials = credentials + cohn
            self._db.update({"serial": camera_id, "credentials": dict(credentials)})
        else:
            self._db.insert({"serial": camera_id, "credentials": dict(cohn)})

    def search_credentials(self, camera_id: str) -> CohnInfo | None:
        asdict = self._db.search(Query().serial == camera_id)
        if asdict:
            return CohnInfo(**asdict[0]["credentials"])
        else:
            return None

    def delete_credentials(self, camera_id: str) -> None:
        self._db.remove(Query().serial == camera_id)
