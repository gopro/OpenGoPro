from kmp_proto_manipulator.grammar.kotlin_proto import kotlin_object, scope

scope.set_parse_action(lambda toks: "public")
kotlin_object.set_parse_action(lambda toks: " ".join(toks))


def test_parse_enum(enum_as_text: str):
    transformed = kotlin_object.transform_string(enum_as_text)
    print(transformed)


def test_parse_sealed_class(sealed_class_as_text: str):
    transformed = kotlin_object.transform_string(sealed_class_as_text)
    print(transformed)


def test_parse_file(file_as_text: str):
    transformed = kotlin_object.transform_string(file_as_text)
    print(transformed)
