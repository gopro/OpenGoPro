# test_db.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

from re import L

import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from open_gopro.database.cohn_db import CohnDb
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
    cohn_db.delete_credentials(camera)
    retrieved_credentials = cohn_db.search_credentials(camera)

    # THEN
    assert retrieved_credentials is None


def main():
    from pathlib import Path

    partial1 = CohnInfo(ip_address="", username="user1", password="password", certificate="cert")
    complete1 = CohnInfo(ip_address="ip_address", username="user1", password="password", certificate="cert")

    partial2 = CohnInfo(ip_address="", username="", password="password", certificate="")
    complete2 = CohnInfo(ip_address="ip_address", username="user2", password="password", certificate="cert")

    db = CohnDb(TinyDB(Path("temp_db.json"), indent=4))
    db.insert_or_update_credentials("one", partial1)
    db.insert_or_update_credentials("one", complete1)
    db.insert_or_update_credentials("two", partial2)
    db.insert_or_update_credentials("two", complete2)


if __name__ == "__main__":
    main()
