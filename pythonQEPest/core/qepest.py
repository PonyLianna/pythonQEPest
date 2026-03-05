import logging
import math
from typing import Optional

from pythonQEPest.config import ConfigProvider
from pythonQEPest.core.qepest_meta import QEPestMeta
from pythonQEPest.config.qepest_config import QEPestConfig
from pythonQEPest.dto import QEPestData

from pythonQEPest.dto.QEPestInput import QEPestInput
from pythonQEPest.dto.QEPestOutput import QEPestOutput
from pythonQEPest.dto.normalisation.Normaliser import Normaliser
from pythonQEPest.helpers.check_nan import check_nan
from pythonQEPest.helpers.compute_df import compute_df
from pythonQEPest.helpers.get_values_from_line import get_values_from_line
from pythonQEPest.helpers.round_to_4digs import round_to_4digs
from pythonQEPest.providers import DefaultConfigProvider

logger = logging.getLogger(__name__)


class QEPest(QEPestMeta):
    def __init__(self, provider: Optional[ConfigProvider] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config: QEPestConfig
        self.normalisers: dict[str, Normaliser] = {}
        self.qex: QEPestData = QEPestData({})

        logger.debug("QEPest initialization")

        self.initialise_config(provider)

        logger.debug("QEPest initialization successful")

    def initialise_config(self, provider: Optional[ConfigProvider] = None):
        logger.debug("Config initialisation")
        if provider is None:
            logger.debug("Config is empty. Loading default one.")
            provider = DefaultConfigProvider()

        self.config = provider.load()
        logger.debug(f"Config {self.config} loaded")

        for pest in self.config.pest_types:
            self.normalisers[pest.name] = Normaliser(pest.normaliser)

    def _log_compute_df(
        self, func, index: int, lst: list[float], data_lst: list
    ) -> float:
        df_result = compute_df(lst[index], *data_lst[index])
        return math.log(func(df_result, index))

    def get_names(self) -> list[str]:
        return self.config.get_pest_names()

    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        self.get_qex_values(
            get_values_from_line(list(data_input.model_dump().values()))
        )
        return QEPestOutput(data=self.qex, name=data_input.name)

    def get_qex_values(self, d: list[float]) -> QEPestData:
        names = self.get_names()

        if len(names) == 0:
            raise ValueError(
                "No pest types configured. " "Please provide a valid configuration."
            )

        qe_values = dict.fromkeys(names, 0.0)

        d_num = len(d)
        for i in range(d_num):
            for name in names:
                coeffs = self.config.get_coefficients(name)
                normaliser = self.normalisers[name]
                qe_values[name] += self._log_compute_df(
                    func=normaliser.norm,
                    index=i,
                    lst=d,
                    data_lst=coeffs,
                )

        result = [round_to_4digs(math.exp(qe_values[name] / d_num)) for name in names]

        result = check_nan(result)

        self.qex = QEPestData(
            {f"qe_{name}": result[idx] for idx, name in enumerate(names)}
        )

        return self.qex


if __name__ == "__main__":
    qepest = QEPest()
    qepest.get_qex_values([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
