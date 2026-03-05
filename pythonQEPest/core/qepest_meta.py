import os
from abc import abstractmethod, ABC

from pydantic import BaseModel

from pythonQEPest.dto import QEPestInput, QEPestOutput


class QEPestMeta(ABC):
    def __init__(self, *args, **kwargs):
        self.qex: BaseModel | None = None

        self.col_number: int = 7
        self.dir: str = os.getcwd()

    @abstractmethod
    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        pass

    @abstractmethod
    def get_qex_values(self, d: list[float]) -> None:
        pass

    @abstractmethod
    def _log_compute_df(
        self, func, index: int, lst: list[float], data_lst: list
    ) -> float:
        pass
