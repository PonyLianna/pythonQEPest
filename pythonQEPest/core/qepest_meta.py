import os
from abc import abstractmethod, ABC

from pythonQEPest.dto import QEPestInput, QEPestOutput, QEPestData


class QEPestMeta(ABC):
    def __init__(self, *args, **kwargs):
        self.qex: QEPestData | None = None

        self.herb: list[float] = []
        self.insect: list[float] = []
        self.fung: list[float] = []

        self.col_number: int = 7
        self.dir: str = os.getcwd()

        self.initialize_coefficients()
        self.initialize_normalisers()

    @abstractmethod
    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        pass

    @abstractmethod
    def get_qex_values(self, d) -> None:
        pass

    @abstractmethod
    def initialize_coefficients(self, coefficients=None) -> None:
        if coefficients is None:
            from pythonQEPest.config.qepest import qepest_default

            coefficients = qepest_default
        return coefficients

    @abstractmethod
    def initialize_normalisers(self, normalisers=None) -> None:
        if normalisers is None:
            from pythonQEPest.config.normalise import normalise_default

            normalisers = normalise_default
        return normalisers
