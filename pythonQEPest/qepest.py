import math
import os

from pythonQEPest.dto.QEPestData import QEPestData
from pythonQEPest.dto.QEPestInput import QEPestInput
from pythonQEPest.dto.QEPestOutput import QEPestOutput
from pythonQEPest.helpers.check_nan import check_nan
from pythonQEPest.helpers.get_num_of_cols import get_num_of_cols
from pythonQEPest.helpers.get_values_from_line import get_values_from_line


class QEPest:
    def __init__(self, dirname="data.txt"):
        self.qex: QEPestData | None = None

        self.herb: list[float] = []
        self.insect: list[float] = []
        self.fung: list[float] = []

        self.col_number: int = 7
        self.dir: str = os.getcwd()

        self.initialize_coefficients()

        self.input_file = os.path.join(self.dir, dirname)

        self.noError = True

        self.qex: QEPestData
        self.dir = None

    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        self.get_qex_values(get_values_from_line(list(data_input.dict().values())))
        return QEPestOutput(data=self.qex, name=data_input.name)

    def read_file_and_compute_params(self):
        try:
            with open(self.input_file, "r") as file:
                lines = file.readlines()

            with open(f"{self.input_file}.out", "w") as wr:
                for index, line in enumerate(lines):
                    if index == 0:
                        if get_num_of_cols(line) != self.col_number:
                            er = f"Error: Line {index} does not have seven elements."
                            print(er)
                            self.noError = False
                            break
                        wr.write("Name QEH QEI QEF\n")
                    else:
                        if get_num_of_cols(line) == self.col_number:
                            dValues = get_values_from_line(line.split("\t"))
                            self.get_qex_values(dValues)
                            splitted_line = line.split('\t')[0]
                            wr.write(
                                f"{splitted_line} {self.qex.qeh} {self.qex.qei} {self.qex.qef}{chr(10)}"  #chr(10) = \n
                            )
                        else:
                            er = f"Error: Line {index} does not have seven elements."
                            print(er)
                            self.noError = False
                if self.noError:
                    print("Computation completed")
                else:
                    print("Finished with errors")

        except FileNotFoundError as e:
            self.noError = False
            print(f"Error: can't find : {input}")
            print(e)

    def get_qex_values(self, d):
        def log_compute_df(func, index, lst, data_lst) -> float:
            df_result = self.compute_df(lst[index], *data_lst[index])
            return math.log(func(df_result, index))

        qeH = 0.0
        qeI = 0.0
        qeF = 0.0

        d_num = len(d)
        for i in range(d_num):
            qeH += log_compute_df(func=self.norm_h, index=i, lst=d, data_lst=self.herb)
            qeI += log_compute_df(func=self.norm_i, index=i, lst=d, data_lst=self.insect)
            qeF += log_compute_df(func=self.norm_f, index=i, lst=d, data_lst=self.fung)

        q = [
            self.round_to_4digs(math.exp(qeH / d_num)),
            self.round_to_4digs(math.exp(qeI / d_num)),
            self.round_to_4digs(math.exp(qeF / d_num)),
        ]

        result = check_nan(q)
        self.qex = QEPestData(qeh=result[0], qei=result[1], qef=result[2])

    def round_to_4digs(self, q):
        return float("{:.4f}".format(q))

    def compute_df(self, x, a, b, c, o):
        return a * math.exp(-1.0 * math.exp(-1.0 * ((x - b) / c)) - (x - b) / c + 1.0) + o

    def norm_h(self, d, descr):
        max_val = (69.5849922, 94.4228257, 120.4572352, 228.1589796, 89.7012502, 276.9634213)[int(descr)]
        return d / max_val if max_val != 0 else 0.0

    def norm_i(self, d, descr):
        max_val = (78.2919965, 71.2829691, 133.9224801, 331.170104, 70.5540709, 193.0023343)[int(descr)]
        return d / max_val if max_val != 0 else 0.0

    def norm_f(self, d, descr):
        max_val = (53.3719946, 52.773116, 73.7976536, 144.9887053, 41.4385926, 102.3024319)[int(descr)]
        return d / max_val if max_val != 0 else 0.0

    def initialize_coefficients(self):
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


if __name__ == "__main__":
    qepest = QEPest()
    qepest.read_file_and_compute_params()
