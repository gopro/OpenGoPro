# enum.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Custom enum definition"""

from __future__ import annotations

from enum import Enum, EnumMeta, IntEnum
from typing import Any, Iterator, Protocol, TypeVar, no_type_check

T = TypeVar("T")


class ProtobufDescriptor(Protocol):
    """Protocol definition for Protobuf enum descriptor used to generate GoPro enums from protobufs"""

    @property
    def name(self) -> str:
        """Human readable name of protobuf enum

        # noqa: DAR202

        Returns:
            str: enum name
        """

    @property
    def values_by_name(self) -> dict:
        """Get the enum values by name

        # noqa: DAR202

        Returns:
            dict: Dict of enum values mapped by name
        """

    @property
    def values_by_number(self) -> dict:
        """Get the enum values by number

        # noqa: DAR202

        Returns:
            dict: dict of enum numbers mapped by number
        """


class GoProEnumMeta(EnumMeta):
    """Modify enum metaclass to build GoPro specific enums"""

    _is_proto = False
    _iter_skip_names = ("NOT_APPLICABLE", "DESCRIPTOR")

    @no_type_check
    def __new__(mcs, name, bases, classdict, **kwargs) -> GoProEnumMeta:  # noqa
        is_proto = "__is_proto__" in classdict
        classdict["_ignore_"] = "__is_proto__"
        classdict["__doc__"] = ""  # Don't use useless "An enumeration" docstring
        e = super().__new__(mcs, name, bases, classdict, **kwargs)
        setattr(e, "_is_proto", is_proto)
        return e

    @no_type_check
    def __contains__(cls: type[Any], obj: object) -> bool:
        if isinstance(obj, Enum):
            return super().__contains__(obj)
        if isinstance(obj, int):
            return obj in [x.value for x in cls._member_map_.values()]
        if isinstance(obj, str):
            return obj.lower() in [x.name.lower() for x in cls._member_map_.values()]
        raise TypeError(
            f"unsupported operand type(s) for 'in': {type(obj).__qualname__} and {cls.__class__.__qualname__}"
        )

    def __iter__(cls: type[T]) -> Iterator[T]:
        """Do not return enum values whose name is in the _iter_skip_names list

        Returns:
            Iterator[T]: enum iterator
        """
        return iter([x[1] for x in cls._member_map_.items() if x[0] not in GoProEnumMeta._iter_skip_names])  # type: ignore


class GoProIntEnum(IntEnum, metaclass=GoProEnumMeta):
    """GoPro specific integer enum to be used for all settings, statuses, and parameters

    The names NOT_APPLICABLE and DESCRIPTOR are special as they will not be returned as part of the enum iterator
    """

    def __eq__(self, other: object) -> bool:
        if type(self)._is_proto:
            if isinstance(other, int):
                return self.value == other
            if isinstance(other, str):
                return self.name == other
            if isinstance(other, Enum):
                return self.value == other.value
            raise TypeError(f"Unexpected case: proto enum can only be str or int, not {type(other)}")
        return super(IntEnum, self).__eq__(other)

    def __hash__(self) -> Any:
        return hash(self.name + str(self.value))

    def __str__(self) -> str:
        return super(IntEnum, self).__str__()


class GoProEnum(Enum, metaclass=GoProEnumMeta):
    """GoPro specific enum to be used for all settings, statuses, and parameters

    The names NOT_APPLICABLE and DESCRIPTOR are special as they will not be returned as part of the enum iterator
    """

    def __eq__(self, other: object) -> bool:
        if type(self)._is_proto:
            if isinstance(other, int):
                return self.value == other
            if isinstance(other, str):
                return self.name == other
            if isinstance(other, Enum):
                return self.value == other.value
            raise TypeError(f"Unexpected case: proto enum can only be str or int, not {type(other)}")
        return super().__eq__(other)

    def __hash__(self) -> Any:
        return hash(self.name + str(self.value))


def enum_factory(proto_enum: ProtobufDescriptor) -> type[GoProIntEnum]:
    """Dynamically build a GoProEnum from a protobuf enum

    Args:
        proto_enum (ProtobufDescriptor): input protobuf enum descriptor

    Returns:
        GoProEnum: generated GoProEnum
    """
    keys = proto_enum.values_by_name.keys()
    values = list(proto_enum.values_by_number.keys())
    # This has somehow changed between protobuf versions
    if isinstance(proto_enum.values_by_number, dict):
        values.reverse()
    return GoProIntEnum(  # type: ignore # pylint: disable=too-many-function-args
        proto_enum.name,  # type: ignore
        {
            **dict(zip(keys, values)),
            "__is_proto__": True,
        },
    )
