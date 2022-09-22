"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file

Defines the structure of protobuf message for enabling and disabling Turbo Transfer feature
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class RequestSetTurboActive(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ACTIVE_FIELD_NUMBER: builtins.int
    active: builtins.bool

    def __init__(self, *, active: builtins.bool | None = ...) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["active", b"active"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["active", b"active"]) -> None: ...

global___RequestSetTurboActive = RequestSetTurboActive