from dataclasses import dataclass
from .proto_object_scope import ProtoObjectScope


class ProtoObject:
    scope: ProtoObjectScope
    remainder: str
