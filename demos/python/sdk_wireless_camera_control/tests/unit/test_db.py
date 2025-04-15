from re import L

import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from open_gopro.db import CohnDb
from open_gopro.models.general import CohnInfo


@pytest.fixture(scope="module")
def cohn_db():
    tiny_db = TinyDB(storage=MemoryStorage)
    yield CohnDb(tiny_db)


def test_search_fails(cohn_db: CohnDb):
    # GIVEN
    camera = "1234"

    # WHEN
    credentials = cohn_db.search_credentials(camera)

    # THEN
    assert credentials is None


def test_add_camera(cohn_db: CohnDb):
    # GIVEN
    camera = "1234"
    credentials = CohnInfo(ip_address="ip_address", password="password", username="user", certificate="cert")

    # WHEN
    cohn_db.insert_or_update_credentials(camera, credentials)
    retrieved_credentials = cohn_db.search_credentials(camera)

    # THEN
    assert credentials == retrieved_credentials


def test_update_camera_doesnt_take_empty_fields(cohn_db: CohnDb):
    # GIVEN
    camera = "1234"
    credentials = CohnInfo(ip_address="", password="new password", username="", certificate="new cert")

    # WHEN
    cohn_db.insert_or_update_credentials(camera, credentials)
    retrieved_credentials = cohn_db.search_credentials(camera)

    # THEN
    assert retrieved_credentials == CohnInfo(
        ip_address="ip_address", password="new password", username="user", certificate="new cert"
    )


def test_delete_camera(cohn_db: CohnDb):
    # GIVEN
    camera = "1234"

    # WHEN
    credentials = cohn_db.delete_credentials(camera)
    retrieved_credentials = cohn_db.search_credentials(camera)

    # THEN
    assert retrieved_credentials is None
