import math

from pythonQEPest.core.qepest_meta import QEPestMeta
from pythonQEPest.dto.QEPestData import QEPestData
from pythonQEPest.dto.QEPestInput import QEPestInput
from pythonQEPest.dto.QEPestOutput import QEPestOutput
from pythonQEPest.helpers.check_nan import check_nan
from pythonQEPest.helpers.compute_df import compute_df
from pythonQEPest.helpers.norm import norm_h, norm_f, norm_i
from pythonQEPest.helpers.round_to_4digs import round_to_4digs
from pythonQEPest.helpers.get_values_from_line import get_values_from_line


class QEPest(QEPestMeta):
    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        self.get_qex_values(get_values_from_line(list(data_input.dict().values())))
        return QEPestOutput(data=self.qex, name=data_input.name)

    def get_qex_values(self, d) -> None:
        def log_compute_df(func, index, lst, data_lst) -> float:
            df_result = compute_df(lst[index], *data_lst[index])
            return math.log(func(df_result, index))

        qe_h = 0.0
        qe_i = 0.0
        qe_f = 0.0

        d_num = len(d)
        for i in range(d_num):
            qe_h += log_compute_df(func=norm_h, index=i, lst=d, data_lst=self.herb)
            qe_i += log_compute_df(func=norm_i, index=i, lst=d, data_lst=self.insect)
            qe_f += log_compute_df(func=norm_f, index=i, lst=d, data_lst=self.fung)

        q = [
            round_to_4digs(math.exp(qe_h / d_num)),
            round_to_4digs(math.exp(qe_i / d_num)),
            round_to_4digs(math.exp(qe_f / d_num)),
        ]

        result = check_nan(q)
        self.qex = QEPestData(qe_h=result[0], qe_i=result[1], qe_f=result[2])

    def initialize_coefficients(self) -> None:
        coefficients = {
            'herb': [
                (70.77, 283.0, 84.97, -1.185),  # mwH
                (93.81, 3.077, 1.434, 0.6164),  # logpH
                (117.6, 2.409, 1.567, 7.155),  # hbaH
                (233.4, 0.4535, -1.48, 4.47),  # hbdH
                (84.7, 4.758, -2.423, 5.437),  # rbH
                (301.8, 1.101, 0.8869, -22.81)  # arRCH
            ],
            'insect': [
                (76.38, 298.3, 83.64, 1.912),  # mwI
                (74.27, 4.555, -2.193, -2.987),  # logpI
                (139.4, 1.363, 1.283, 0.5341),  # hbaI
                (670.6, -1.163, 0.7856, 0.7951),  # hbdI
                (65.49, 6.219, -2.448, 5.318),  # rbI
                (287.5, 0.305, 1.554, -88.64)  # arRCI
            ],
            'fung': [
                (51.03, 314.2, -56.31, 2.342),  # mwF
                (50.73, 3.674, -1.238, 2.067),  # logpF
                (73.79, 1.841, 1.326, 0.5158),  # hbaF
                (164.7, -0.9762, -2.027, 1.384),  # hbdF
                (40.91, 1.822, 2.582, 0.6235),  # rbF
                (134.4, 0.8383, 1.347, -31.17)  # arRCF
            ]
        }

        for category, data in coefficients.items():
            getattr(self, category).extend(data)
