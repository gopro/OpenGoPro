from dataclasses import dataclass
from .proto_object_scope import ProtoObjectScope


@dataclass(frozen=True)
class ProtoObjectConfig:
    scope: ProtoObjectScope


@dataclass(frozen=True)
class Config:
    objects: dict[str, ProtoObjectConfig]
