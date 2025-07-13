from pythonQEPest.core.qepest_meta import QEPestMeta
from pythonQEPest.helpers.get_num_of_cols import get_num_of_cols
from pythonQEPest.helpers.get_values_from_line import get_values_from_line


class CLI:
    qepest: QEPestMeta | None = None

    def __init__(self, qepest: QEPestMeta):
        self.qepest = qepest

    def read_file_and_compute_params(self):
        try:
            with open(self.qepest.input_file, "r") as file:
                lines = file.readlines()

            with open(f"{self.qepest.input_file}.out", "w") as wr:
                for index, line in enumerate(lines):
                    if index == 0:
                        if get_num_of_cols(line) != self.qepest.col_number:
                            er = f"Error: Line {index} does not have seven elements."
                            print(er)
                            self.qepest.noError = False
                            break
                        wr.write("Name QEH QEI QEF\n")
                    else:
                        if get_num_of_cols(line) == self.qepest.col_number:
                            d_values = get_values_from_line(line.split("\t"))
                            self.qepest.get_qex_values(d_values)
                            splitted_line = line.split('\t')[0]
                            wr.write(
                                f"{splitted_line} {self.qepest.qex.qe_h} {self.qepest.qex.qe_i} {self.qepest.qex.qe_f}{chr(10)}"
                                #chr(10) = \n
                            )
                        else:
                            er = f"Error: Line {index} does not have seven elements."
                            print(er)
                            self.qepest.noError = False
                if self.qepest.noError:
                    print("Computation completed")
                else:
                    print("Finished with errors")

        except FileNotFoundError as e:
            self.qepest.noError = False
            print(f"Error: can't find : {input}")
            print(e)
