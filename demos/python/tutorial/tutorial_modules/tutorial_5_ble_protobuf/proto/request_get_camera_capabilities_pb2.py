"""Generated protocol buffer code."""

from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()
from . import response_generic_pb2 as response__generic__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n%request_get_camera_capabilities.proto\x12\nopen_gopro\x1a\x16response_generic.proto"\x1e\n\x1cRequestGetCameraCapabilities"\x9a\x01\n\x1dResponseGetCameraCapabilities\x12-\n\x06result\x18\x01 \x02(\x0e2\x1d.open_gopro.EnumResultGeneric\x12\x16\n\x0eschema_version\x18\x02 \x02(\t\x122\n\x08protocol\x18\x03 \x01(\x0b2 .open_gopro.ProtocolCapabilities"9\n\x14ProtocolCapabilities\x12!\n\x12supports_2byte_ids\x18\x01 \x01(\x08:\x05false'
)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "request_get_camera_capabilities_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _REQUESTGETCAMERACAPABILITIES._serialized_start = 77
    _REQUESTGETCAMERACAPABILITIES._serialized_end = 107
    _RESPONSEGETCAMERACAPABILITIES._serialized_start = 110
    _RESPONSEGETCAMERACAPABILITIES._serialized_end = 264
    _PROTOCOLCAPABILITIES._serialized_start = 266
    _PROTOCOLCAPABILITIES._serialized_end = 323
