"""Entities used to store config file information."""

import enum

from pydantic import BaseModel, RootModel


class ProtoObjectScope(enum.StrEnum):
    """Target scope defined in config file."""

    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"


class ProtoObjectConfig(BaseModel):
    """Per-kotlin-object specification of manipulations."""

    scope: ProtoObjectScope


class Config(RootModel):
    """Complete config file definition."""

    root: dict[str, ProtoObjectConfig]
