# test_enums.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Aug 16 22:48:50 UTC 2023

# Note: This may seem trivial but there were some major changes around this in Python 3.11

import enum

from open_gopro import proto
from open_gopro.enum import GoProIntEnum, enum_factory


class EnumTest(GoProIntEnum):
    RESULT_SUCCESS = 1
    TWO = 2
    NOT_APPLICABLE = 3
    DESCRIPTOR = 4
    FIVE = 5


class NormalEnum(enum.Enum):
    TWO = 2


def test_str():
    assert EnumTest.TWO.name == "TWO"
    assert EnumTest.TWO.value == 2
    assert str(EnumTest.TWO) == "EnumTest.TWO"


def test_equal():
    assert EnumTest.TWO == 2
    assert not EnumTest.TWO == "TWO"
    assert not EnumTest.TWO == NormalEnum.TWO
    assert EnumTest.TWO == EnumTest.TWO


def test_proto_enum_equal():
    proto_enum = enum_factory(proto.EnumResultGeneric.DESCRIPTOR)
    assert proto_enum.RESULT_SUCCESS == 1
    assert proto_enum.RESULT_SUCCESS == EnumTest.RESULT_SUCCESS
    assert proto_enum.RESULT_SUCCESS == "RESULT_SUCCESS"


def test_special_values():
    assert EnumTest.FIVE in list(EnumTest)
    assert EnumTest.FIVE in EnumTest
    assert EnumTest.NOT_APPLICABLE not in list(EnumTest)
    assert EnumTest.DESCRIPTOR not in list(EnumTest)
