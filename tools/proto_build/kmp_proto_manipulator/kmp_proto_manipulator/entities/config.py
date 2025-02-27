import enum

from pydantic import BaseModel, RootModel


class ProtoObjectScope(enum.StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"


class ProtoObjectConfig(BaseModel):
    scope: ProtoObjectScope


class Config(RootModel):
    root: dict[str, ProtoObjectConfig]
