# bases.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Base classes shared throughout models"""

from pydantic import BaseModel

from open_gopro.util import pretty_print, scrub


class CustomBaseModel(BaseModel):
    """Additional functionality added to Pydantic BaseModel"""

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(getattr(self, f) for f in self.__fields__.keys()))

    def __str__(self) -> str:
        d = dict(self)
        scrub(d, bad_values=[None])
        return pretty_print(d)
