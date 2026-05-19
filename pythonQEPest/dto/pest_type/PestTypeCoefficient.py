from typing import Any

from pydantic import BaseModel, model_validator


class PestTypeCoefficient(BaseModel):
    mwH: tuple[float, float, float, float]
    logpH: tuple[float, float, float, float]
    hbaH: tuple[float, float, float, float]
    hbdH: tuple[float, float, float, float]
    rbH: tuple[float, float, float, float]
    arRCH: tuple[float, float, float, float]

    @model_validator(mode="before")
    @classmethod
    def accept_positional(cls, data: Any):
        if isinstance(data, dict):
            return data

        if isinstance(data, (list, tuple)):
            if len(data) != 6:
                raise ValueError("Expected 6 items: mwH, logpH, hbaH, hbdH, rbH, arRCH")

            keys = ("mwH", "logpH", "hbaH", "hbdH", "rbH", "arRCH")
            return dict(zip(keys, data, strict=True))

        raise TypeError("Expected a dict or a 6-item tuple/list")

    def as_set(self):
        return [self.mwH, self.logpH, self.hbaH, self.hbdH, self.rbH, self.arRCH]
