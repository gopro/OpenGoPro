# kotlin_transformer.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 27 22:11:09 UTC 2025

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
        return " ".join([toks[0], "\n", scope, *toks[2:]])

    def transform(self, kotlin: str) -> str:
        """Perform all manipulations to transform a kotlin file.

        Args:
            kotlin (str): kotlin file as text

        Returns:
            str: transformed kotlin file
        """
        return self._transformer.transform_string(kotlin)
