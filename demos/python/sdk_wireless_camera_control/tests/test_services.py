# test_services.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:35 AM

import pytest
from typing import List, Dict

from open_gopro.constants import UUID
from open_gopro.services import Descriptor, Characteristic, Service, AttributeTable


@pytest.fixture()
def descriptor():
    yield Descriptor(0xABCD, bytes([1, 2, 3, 4]))


@pytest.fixture()
def characteristic(descriptor):
    d = [descriptor, descriptor]
    yield Characteristic(
        0xABCD, UUID.CQ_QUERY, ["readable", "writeable"], "test_characteristic", bytes([1, 2, 3, 4]), d
    )


@pytest.fixture()
def service(characteristic):
    c = {"test_char1": characteristic, "test_char2": characteristic}
    yield Service(UUID.S_CONTROL_QUERY, "test_service", c)


def test_descriptor(descriptor):
    print(str(descriptor))
    assert True


def test_characteristic(characteristic):
    print(str(characteristic))
    assert True


def test_service(service):
    print(str(service))
    assert True


def test_attribute_table(service):
    s = {UUID.S_CONTROL_QUERY: service, UUID.S_CAMERA_MANAGEMENT: service}
    a = AttributeTable(s)
    assert len(a.services) == 2
    assert len(a.services[UUID.S_CONTROL_QUERY].chars) == 2


def test_handle2uuid(service):
    a = AttributeTable({UUID.S_CONTROL_QUERY: service, UUID.S_CAMERA_MANAGEMENT: service})
    assert a.handle2uuid(0xABCD) is UUID.CQ_QUERY
