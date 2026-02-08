from __future__ import annotations

import argparse
import logging
from typing import Sequence

from pythonQEPest.core.qepest_meta import QEPestMeta
from pythonQEPest.helpers.get_num_of_cols import get_num_of_cols
from pythonQEPest.helpers.get_values_from_line import get_values_from_line


logger = logging.getLogger(__name__)


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
                            logger.error(er)
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
                            )
                        else:
                            er = f"Error: Line {index} does not have seven elements."
                            logger.error(er)
                            self.qepest.noError = False
                if self.qepest.noError:
                    logger.info("Computation completed")
                else:
                    logger.warning("Finished with errors")

        except FileNotFoundError as e:
            self.qepest.noError = False
            logger.error("Error: can't find : %s", self.qepest.input_file)
            logger.exception(e)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pythonqepest",
        description="Compute QEPest scores from a tab-separated input file.",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="data.txt",
        help="Path to input tab-separated file with QEPest descriptors (default: data.txt).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    from dotenv import load_dotenv

    from pythonQEPest.core.qepest import QEPest
    from pythonQEPest.logger import init_logger

    args = build_parser().parse_args(argv)

    load_dotenv()
    init_logger()

    cli = CLI(qepest=QEPest(dirname=args.input))
    cli.read_file_and_compute_params()
    return 0 if cli.qepest and cli.qepest.noError else 1
