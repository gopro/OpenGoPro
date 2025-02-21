
import sys
_b = (((sys.version_info[0] < 3) and (lambda x: x)) or (lambda x: x.encode('latin1')))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='request_get_preset_status.proto', package='open_gopro', syntax='proto2', serialized_options=None, serialized_pb=_b('\n\x1frequest_get_preset_status.proto\x12\nopen_gopro"¦\x01\n\x16RequestGetPresetStatus\x12D\n\x16register_preset_status\x18\x01 \x03(\x0e2$.open_gopro.EnumRegisterPresetStatus\x12F\n\x18unregister_preset_status\x18\x02 \x03(\x0e2$.open_gopro.EnumRegisterPresetStatus*l\n\x18EnumRegisterPresetStatus\x12!\n\x1dREGISTER_PRESET_STATUS_PRESET\x10\x01\x12-\n)REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY\x10\x02'))
_ENUMREGISTERPRESETSTATUS = _descriptor.EnumDescriptor(name='EnumRegisterPresetStatus', full_name='open_gopro.EnumRegisterPresetStatus', filename=None, file=DESCRIPTOR, values=[_descriptor.EnumValueDescriptor(name='REGISTER_PRESET_STATUS_PRESET', index=0, number=1, serialized_options=None, type=None), _descriptor.EnumValueDescriptor(name='REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY', index=1, number=2, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=216, serialized_end=324)
_sym_db.RegisterEnumDescriptor(_ENUMREGISTERPRESETSTATUS)
EnumRegisterPresetStatus = enum_type_wrapper.EnumTypeWrapper(_ENUMREGISTERPRESETSTATUS)
REGISTER_PRESET_STATUS_PRESET = 1
REGISTER_PRESET_STATUS_PRESET_GROUP_ARRAY = 2
_REQUESTGETPRESETSTATUS = _descriptor.Descriptor(name='RequestGetPresetStatus', full_name='open_gopro.RequestGetPresetStatus', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='register_preset_status', full_name='open_gopro.RequestGetPresetStatus.register_preset_status', index=0, number=1, type=14, cpp_type=8, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR), _descriptor.FieldDescriptor(name='unregister_preset_status', full_name='open_gopro.RequestGetPresetStatus.unregister_preset_status', index=1, number=2, type=14, cpp_type=8, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=48, serialized_end=214)
_REQUESTGETPRESETSTATUS.fields_by_name['register_preset_status'].enum_type = _ENUMREGISTERPRESETSTATUS
_REQUESTGETPRESETSTATUS.fields_by_name['unregister_preset_status'].enum_type = _ENUMREGISTERPRESETSTATUS
DESCRIPTOR.message_types_by_name['RequestGetPresetStatus'] = _REQUESTGETPRESETSTATUS
DESCRIPTOR.enum_types_by_name['EnumRegisterPresetStatus'] = _ENUMREGISTERPRESETSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
RequestGetPresetStatus = _reflection.GeneratedProtocolMessageType('RequestGetPresetStatus', (_message.Message,), dict(DESCRIPTOR=_REQUESTGETPRESETSTATUS, __module__='request_get_preset_status_pb2'))
_sym_db.RegisterMessage(RequestGetPresetStatus)
