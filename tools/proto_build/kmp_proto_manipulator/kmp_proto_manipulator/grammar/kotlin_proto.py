# kotlin_proto.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 27 22:11:09 UTC 2025

"""Grammar to parse a kotlin file generated from protobuf."""

from pyparsing import Literal, Opt, Word, alphanums

PB_DECORATOR = Literal("@pbandk.Export")

INTERNAL = Literal("internal")
PRIVATE = Literal("private")
PUBLIC = Literal("public")
scope = (INTERNAL | PRIVATE | PUBLIC)("scope")

SEALED = Literal("sealed")
DATA = Literal("data")
class_type = (SEALED | DATA)("class_type")

CLASS = class_type + Literal("class")

object_name = Word(init_chars=alphanums)("name")

kotlin_object = PB_DECORATOR + Opt(scope) + CLASS + object_name
