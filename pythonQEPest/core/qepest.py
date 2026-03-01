import logging
import math
from typing import Optional

from pydantic import create_model, BaseModel

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
        super().__init__(*args, **kwargs)

    def _log_compute_df(self, func, index, lst, data_lst) -> float:
        df_result = compute_df(lst[index], *data_lst[index])
        return math.log(func(df_result, index))

    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        self.get_qex_values(
            get_values_from_line(list(data_input.model_dump().values()))
        )
        return QEPestOutput(data=self.qex, name=data_input.name)

    def get_qex_values(self, d) -> BaseModel:
        names = [n.split("_")[1] for n in dir(self) if n.startswith("coefficient_")]

        # Coefficients names = ("coefficients_fung, coefficient_herb...)
        coefficients_names = [n for n in dir(self) if n.startswith("coefficient_")]
        if len(coefficients_names) == 0:
            raise ValueError(
                "No coefficient_ keys, needs to call "
                + "initialize_coefficient and workable config to work"
            )

        # coefficients = [{i: getattr(self, i)} for i in coefficients_names]

        # Splitting by _ to get (fung, herb, etc...) to form qe_fung, qe_herb...
        # qe_lst = []
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

        fields = {f"qe_{name}": (float, 0.0) for name in names}
        dynamic_model = create_model("QEPestData", **fields)
        self.qex = dynamic_model(
            **{f"qe_{names[idx]}": name for idx, name in enumerate(result)}
        )

        return self.qex

    # TODO: Coefficients must be in other class
    def initialize_coefficients(self, coefficients: Optional = None) -> None:
        coefficients = super().initialize_coefficients()

        for category, data in coefficients.items():
            setattr(self, f"coefficient_{category}", data)

    # TODO: Same with Normalisers
    def initialize_normalisers(self, normalisers: Optional = None) -> None:
        normalisers = super().initialize_normalisers()

        for category, data in normalisers.items():
            setattr(self, f"normaliser_{category}", Normaliser(data))


if __name__ == "__main__":
    qepest = QEPest()
    qepest.initialize_coefficients()
    qepest.initialize_normalisers()
    qepest.get_qex_values(1)
    print(1)
