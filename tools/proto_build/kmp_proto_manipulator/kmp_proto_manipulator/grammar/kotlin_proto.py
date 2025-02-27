"""Grammar to parse a kotlin file generated from protobuf."""

from pyparsing import Literal, Opt, Word, alphanums

INTERNAL = Literal("internal")
PRIVATE = Literal("private")
PUBLIC = Literal("public")
scope = (INTERNAL | PRIVATE | PUBLIC)("scope")

OBJECT_MARKER = Literal("sealed class")

object_name = Word(init_chars=alphanums)("name")

kotlin_object = Opt(scope) + OBJECT_MARKER + object_name
