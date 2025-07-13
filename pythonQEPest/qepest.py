import math
import os

from pythonQEPest.dto.QEPestData import QEPestData
from pythonQEPest.dto.QEPestInput import QEPestInput
from pythonQEPest.dto.QEPestOutput import QEPestOutput
from pythonQEPest.helpers.check_nan import check_nan
from pythonQEPest.helpers.get_num_of_cols import get_num_of_cols
from pythonQEPest.helpers.get_values_from_line import get_values_from_line


class QEPestWithoutInterface:
    def __init__(self, dirname="data.txt"):
        self.qex = None
        self.herb = []
        self.insect = []
        self.fung = []

        self.col_number = 7
        self.dir = os.getcwd()

        self.initialize_coefficients()

        self.input_file = os.path.join(self.dir, dirname)

        self.noError = True

        self.qex: QEPestData
        self.dir = None

    def compute_params(self, data_input: QEPestInput) -> QEPestOutput:
        self.get_QEX_values(get_values_from_line(list(data_input.dict().values())))
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
                            self.get_QEX_values(dValues)
                            splitted_line = line.split('\t')[0]
                            wr.write(
                                f"{splitted_line} {self.qex.qeh} {self.qex.qei} {self.qex.qef}{chr(10)}" #chr(10) = \n
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

    def get_QEX_values(self, d):
        qeH = 0.0
        qeI = 0.0
        qeF = 0.0

        d_num = len(d)
        for i in range(len(d)):
            qeH += math.log(
                self.norm_h(
                    self.compute_df(
                        d[i],
                        self.herb[i][0],
                        self.herb[i][1],
                        self.herb[i][2],
                        self.herb[i][3],
                    ),
                    i,
                )
            )
            qeI += math.log(
                self.norm_i(
                    self.compute_df(
                        d[i],
                        self.insect[i][0],
                        self.insect[i][1],
                        self.insect[i][2],
                        self.insect[i][3],
                    ),
                    i,
                )
            )
            qeF += math.log(
                self.norm_f(
                    self.compute_df(
                        d[i],
                        self.fung[i][0],
                        self.fung[i][1],
                        self.fung[i][2],
                        self.fung[i][3],
                    ),
                    i,
                )
            )
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
        return (
            a * math.exp(-1.0 * math.exp(-1.0 * ((x - b) / c)) - (x - b) / c + 1.0) + o
        )

    def norm_h(self, d, descr):
        max_val = 0.0
        match descr + 1:
            case 1:
                max_val = 69.5849922
            case 2:
                max_val = 94.4228257
            case 3:
                max_val = 120.4572352
            case 4:
                max_val = 228.1589796
            case 5:
                max_val = 89.7012502
            case 6:
                max_val = 276.9634213

        return d / max_val if max_val != 0 else 0.0

    def norm_i(self, d, descr):
        max_val = 0.0
        match descr + 1:
            case 1:
                max_val = 78.2919965
            case 2:
                max_val = 71.2829691
            case 3:
                max_val = 133.9224801
            case 4:
                max_val = 331.170104
            case 5:
                max_val = 70.5540709
            case 6:
                max_val = 193.0023343

        return d / max_val if max_val != 0 else 0.0

    def norm_f(self, d, descr):
        max_val = 0.0
        match descr + 1:
            case 1:
                max_val = 53.3719946
            case 2:
                max_val = 52.773116
            case 3:
                max_val = 73.7976536
            case 4:
                max_val = 144.9887053
            case 5:
                max_val = 41.4385926
            case 6:
                max_val = 102.3024319
        return d / max_val if max_val != 0 else 0.0

    def initialize_coefficients(self):
        mwH = [70.77, 283.0, 84.97, -1.185]
        logpH = [93.81, 3.077, 1.434, 0.6164]
        hbaH = [117.6, 2.409, 1.567, 7.155]
        hbdH = [233.4, 0.4535, -1.48, 4.47]
        rbH = [84.7, 4.758, -2.423, 5.437]
        arRCH = [301.8, 1.101, 0.8869, -22.81]
        self.herb.extend([mwH, logpH, hbaH, hbdH, rbH, arRCH])

        mwI = [76.38, 298.3, 83.64, 1.912]
        logpI = [74.27, 4.555, -2.193, -2.987]
        hbaI = [139.4, 1.363, 1.283, 0.5341]
        hbdI = [670.6, -1.163, 0.7856, 0.7951]
        rbI = [65.49, 6.219, -2.448, 5.318]
        arRCI = [287.5, 0.305, 1.554, -88.64]
        self.insect.extend([mwI, logpI, hbaI, hbdI, rbI, arRCI])

        mwF = [51.03, 314.2, -56.31, 2.342]
        logpF = [50.73, 3.674, -1.238, 2.067]
        hbaF = [73.79, 1.841, 1.326, 0.5158]
        hbdF = [164.7, -0.9762, -2.027, 1.384]
        rbF = [40.91, 1.822, 2.582, 0.6235]
        arRCF = [134.4, 0.8383, 1.347, -31.17]
        self.fung.extend([mwF, logpF, hbaF, hbdF, rbF, arRCF])


if __name__ == "__main__":
    qepest = QEPest()
    qepest.read_file_and_compute_params()
