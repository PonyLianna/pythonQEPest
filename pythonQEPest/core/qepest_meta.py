import os
from abc import abstractmethod, ABC

from pythonQEPest.dto import QEPestInput, QEPestOutput, QEPestData


class QEPestMeta(ABC):
    def __init__(self):
        self.qex: QEPestData | None = None

        self.herb: list[float] = []
        self.insect: list[float] = []
        self.fung: list[float] = []

        self.col_number: int = 7
        self.dir: str = os.getcwd()

        self.initialize_coefficients()

        self.noError: bool = True

    @abstractmethod
    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        pass

    @abstractmethod
    def get_qex_values(self, d) -> None:
        pass

    @abstractmethod
    def initialize_coefficients(self) -> None:
        pass
