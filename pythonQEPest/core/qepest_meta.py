import os
from abc import abstractmethod, ABC

from pydantic import BaseModel

from pythonQEPest.dto import QEPestInput, QEPestOutput


class QEPestMeta(ABC):
    def __init__(self, *args, **kwargs):
        self.qex: BaseModel | None = None

        self.col_number: int = 7
        self.dir: str = os.getcwd()

        if len(args) == 0 and len(kwargs) == 0:
            self.initialize_coefficients()
            self.initialize_normalisers()

        if len(kwargs):
            if "coefficients" in kwargs:
                self.initialize_coefficients(kwargs["coefficients"])
            if "normalisers" in kwargs:
                self.initialize_normalisers(kwargs["normalisers"])

    @abstractmethod
    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        pass

    @abstractmethod
    def get_qex_values(self, d: list[float]) -> None:
        pass

    @abstractmethod
    def initialize_coefficients(self, coefficients=None) -> "dict":
        if coefficients is None:
            from pythonQEPest.config.qepest_default import qepest_default

            coefficients = qepest_default
        return coefficients

    @abstractmethod
    def initialize_normalisers(self, normalisers=None) -> "dict":
        if normalisers is None:
            from pythonQEPest.config.normalise import normalise_default

            normalisers = normalise_default
        return normalisers
