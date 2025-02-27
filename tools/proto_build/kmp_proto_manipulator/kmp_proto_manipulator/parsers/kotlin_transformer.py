from kmp_proto_manipulator.entities.config import Config
from kmp_proto_manipulator.grammar.kotlin_proto import scope, kotlin_object, object_name


class KotlinTransformer:
    def __init__(self, config: Config) -> None:
        self.config = config
        kotlin_object.set_parse_action(self._manipulate_scope)
        self._transformer = kotlin_object

    def _manipulate_scope(self, toks) -> str:
        if spec := self.config.root.get(toks.name):
            scope = spec.scope
        else:
            scope = toks["scope"]
        return " ".join([scope, *toks[1:]])

    def transform(self, kotlin: str) -> str:
        return self._transformer.transform_string(kotlin)
