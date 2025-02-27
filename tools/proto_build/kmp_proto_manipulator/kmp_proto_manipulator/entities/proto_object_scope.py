import enum


class ProtoObjectScope(enum.StrEnum):
    PUBLIC = ""
    INTERNAL = "internal"
    PRIVATE = "private"
