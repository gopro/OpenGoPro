from kmp_proto_manipulator.entities.config import Config
from kmp_proto_manipulator.grammar.kotlin_proto import scope, kotlin_object


class KotlinTransformer:
    def __init__(self, config: Config) -> None:
        self.config = config
        scope.set_parse_action(self._modify_scope)
        kotlin_object.set_parse_action(lambda toks: " ".join(toks))
        self._transformer = kotlin_object

    def _modify_scope(self, toks) -> str:
        return "cheese"

    def transform(self, kotlin: str) -> str:
        return self._transformer.transform_string(kotlin)
