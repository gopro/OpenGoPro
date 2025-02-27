from kmp_proto_manipulator.entities.config import Config
from kmp_proto_manipulator.grammar.kotlin_proto import kotlin_object


class KotlinTransformer:
    def __init__(self, config: Config) -> None:
        self.config = config
        kotlin_object.set_parse_action(self._manipulate_scope)
        self._transformer = kotlin_object

    def _manipulate_scope(self, toks) -> str:
        print(f"REMOVE ME {toks.name}")
        if spec := self.config.root.get(toks.name):
            print(f"using scope {spec.scope}")
            scope = spec.scope
        else:
            print(f"using default scope {toks.scope}")
            scope = toks.scope
        return " ".join([scope, *toks[1:]])

    def transform(self, kotlin: str) -> str:
        return self._transformer.transform_string(kotlin)
