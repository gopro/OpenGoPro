"""Kotlin File Parser / Transformer."""

from pyparsing import ParseResults

from kmp_proto_manipulator.entities.config import Config
from kmp_proto_manipulator.grammar.kotlin_proto import kotlin_object


class KotlinTransformer:
    """Kotlin File Transformer.

    Args:
        config (Config): config file to use for transforming.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        kotlin_object.set_parse_action(self._manipulate_scope)
        self._transformer = kotlin_object

    def _manipulate_scope(self, toks: ParseResults) -> str:
        """Pyparsing adapter to set an objects scope from the config file.

        Args:
            toks (ParseResults): parsing tokens

        Returns:
            str: object with potentially modified scope
        """
        if spec := self.config.root.get(toks.name):
            scope = spec.scope
        else:
            scope = toks.scope
        return " ".join([scope, *toks[1:]])

    def transform(self, kotlin: str) -> str:
        """Perform all manipulations to transform a kotlin file.

        Args:
            kotlin (str): kotlin file as text

        Returns:
            str: transformed kotlin file
        """
        return self._transformer.transform_string(kotlin)
