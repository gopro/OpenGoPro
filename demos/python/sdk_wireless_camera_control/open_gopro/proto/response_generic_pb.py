# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: response_generic.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


class EnumResultGeneric(betterproto.Enum):
    RESULT_UNKNOWN = 0
    RESULT_SUCCESS = 1
    RESULT_ILL_FORMED = 2
    RESULT_NOT_SUPPORTED = 3
    RESULT_ARGUMENT_OUT_OF_BOUNDS = 4
    RESULT_ARGUMENT_INVALID = 5


@dataclass
class ResponseGeneric(betterproto.Message):
    result: "EnumResultGeneric" = betterproto.enum_field(1)
