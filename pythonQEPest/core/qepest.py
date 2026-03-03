import logging
import math
from typing import List

from pydantic import BaseModel
from pythonQEPest.dto import QEPestData

from pythonQEPest.core.qepest_meta import QEPestMeta
from pythonQEPest.dto.QEPestInput import QEPestInput
from pythonQEPest.dto.QEPestOutput import QEPestOutput
from pythonQEPest.dto.normalisation.Normaliser import Normaliser
from pythonQEPest.helpers.check_nan import check_nan
from pythonQEPest.helpers.compute_df import compute_df
from pythonQEPest.helpers.get_values_from_line import get_values_from_line
from pythonQEPest.helpers.round_to_4digs import round_to_4digs

logger = logging.getLogger(__name__)


class QEPest(QEPestMeta):

    def __init__(self, *args, **kwargs):
        self.coefficients_names = None
        self.names = None

        logger.debug("QEPest initialisation")

        logger.info(f"QEPest args: {args}")
        logger.info(f"QEPest kwargs: {kwargs}")

        super().__init__(*args, **kwargs)

        logger.debug("QEPest initialisation successful")

    def _log_compute_df(self, func, index, lst, data_lst) -> float:
        df_result = compute_df(lst[index], *data_lst[index])
        return math.log(func(df_result, index))

    def get_names(self) -> List[str]:
        self.names = [
            n.split("_")[1] for n in dir(self) if n.startswith("coefficient_")
        ]
        return self.names

    def get_coefficients_names(self) -> List[str]:
        self.coefficients_names = [f"coefficient_{name}" for name in self.names]
        return self.coefficients_names

    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        self.get_qex_values(
            get_values_from_line(list(data_input.model_dump().values()))
        )
        return QEPestOutput(data=self.qex, name=data_input.name)

    def get_qex_values(self, d: list[float]) -> BaseModel:
        names = self.get_names()

        # Coefficients names = ("coefficients_fung, coefficient_herb...)
        coefficients_names = self.get_coefficients_names()

        if len(coefficients_names) == 0:
            raise ValueError(
                "No coefficient_ keys, needs to call "
                + "initialize_coefficient and workable config to work"
            )

        for z in names:
            name = f"qe_{z}"
            setattr(self, name, 0.0)

        d_num = len(d)
        for i in range(d_num):
            for name in names:
                self.__dict__[f"qe_{name}"] += self._log_compute_df(
                    func=self.__dict__[f"normaliser_{name}"].norm,
                    index=i,
                    lst=d,
                    data_lst=self.__dict__[f"coefficient_{name}"],
                )

        q = [
            round_to_4digs(math.exp(self.__dict__[f"qe_{name}"] / d_num))
            for name in names
        ]

        result = check_nan(q)

        self.qex = QEPestData(
            **{f"qe_{names[idx]}": name for idx, name in enumerate(result)}
        )

        return self.qex

    # TODO: Coefficients must be in other class.
    # TODO: Ability to provide whatever we want is a good thingy
    def initialize_coefficients(self, coefficients: "dict | None" = None) -> "dict":
        logger.debug("QEPest coefficients initialisation")
        coefficients = super().initialize_coefficients()

        logger.debug("QEPest coefficients initialisation successful")
        for category, data in coefficients.items():
            setattr(self, f"coefficient_{category}", data)

        logger.info(f"QEPest coefficients initialisation with {coefficients.items()}")

        return coefficients

    # TODO: Same with Normalisers
    def initialize_normalisers(self, normalisers: "dict | None" = None) -> "dict":
        logger.debug("QEPest normalisers initialisation")
        normalisers = super().initialize_normalisers()

        logger.debug("QEPest normalisers initialisation successful")

        for category, data in normalisers.items():
            setattr(self, f"normaliser_{category}", Normaliser(data))

        logger.info(f"QEPest normalisers initialisation with {normalisers.items()}")

        return normalisers


if __name__ == "__main__":
    qepest = QEPest()
    qepest.get_qex_values(1)
