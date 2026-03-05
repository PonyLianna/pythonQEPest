import logging
import json

from pythonQEPest.core import QEPestMeta
from pythonQEPest.dto import QEPestFile, QEPestInput
from pythonQEPest.dto.QEPestFile import QEPestFormat
from pythonQEPest.helpers.get_values_from_line import get_values_from_line
from pythonQEPest.helpers.get_num_of_cols import get_num_of_cols

logger = logging.getLogger(__name__)


class QEPestFileService:

    def __init__(self, qepest: QEPestMeta, qepest_file: QEPestFile):
        self.qepest = qepest
        self.qepest_file = qepest_file
        self.error = False

    def _write_txt_line(self, line: str, file) -> None:
        splitted_line = line.split("\t")[0]
        qex_headers = " ".join(self.qepest.qex.model_dump().keys())
        qex_values = " ".join(str(x) for x in self.qepest.qex.model_dump().values())

        file.write(f"Name {qex_headers.upper()}\n")
        file.write(f"{splitted_line} {qex_values}\n")

    def _write_json_line(self, line: str, file) -> None:
        splitted_line = line.split("\t")[0]
        data = {"name": splitted_line, **self.qepest.qex.model_dump()}
        file.write(json.dumps(data) + "\n")

    def _process_smiles_line(self, smiles: str, index: int) -> None:
        qepest_input = QEPestInput.from_smiles(smiles, name=f"mol_{index}")
        if qepest_input.mol_weight == 0.0:
            raise RuntimeError(
                "RDKit is not installed. Install it with: pip install rdkit"
            )
        d_values = get_values_from_line(list(qepest_input.model_dump().values()))
        self.qepest.get_qex_values(d_values)

    def _write_smiles_txt_line(self, index: int, file) -> None:
        name = f"mol_{index}"
        qex_headers = " ".join(self.qepest.qex.model_dump().keys())
        qex_values = " ".join(str(x) for x in self.qepest.qex.model_dump().values())
        file.write(f"Name {qex_headers.upper()}\n")
        file.write(f"{name} {qex_values}\n")

    def _write_smiles_json_line(self, index: int, file) -> None:
        name = f"mol_{index}"
        data = {"name": name, **self.qepest.qex.model_dump()}
        file.write(json.dumps(data) + "\n")

    def read_file_and_compute_params(self) -> None:
        if self.qepest_file.smiles:
            self._read_smiles_file()
        else:
            self._read_descriptor_file()

    def _read_smiles_file(self) -> None:
        try:
            with open(self.qepest_file.input_file, "r") as f:
                lines = f.readlines()

            with open(self.qepest_file.output_file, "w") as wr:
                for index, line in enumerate(lines):
                    smiles = line.strip()
                    if not smiles:
                        continue

                    try:
                        self._process_smiles_line(smiles, index)
                    except RuntimeError as e:
                        logger.error(str(e))
                        self.error = True
                        break

                    if self.qepest_file.format == QEPestFormat.TXT:
                        self._write_smiles_txt_line(index, wr)
                    else:
                        self._write_smiles_json_line(index, wr)

            if not self.error:
                logger.info("Computation completed")
            else:
                logger.warning("Finished with errors")

        except FileNotFoundError:
            self.error = True
            logger.error(f"Error: can't find: {self.qepest_file.input_file}")

    def _read_descriptor_file(self) -> None:
        try:
            with open(self.qepest_file.input_file, "r") as f:
                lines = f.readlines()

            with open(self.qepest_file.output_file, "w") as wr:
                for index, line in enumerate(lines):
                    if get_num_of_cols(line) != self.qepest.col_number:
                        logger.error(
                            f"Error: Line {index} does not have the "
                            "expected number of columns."
                        )
                        self.error = True
                        break

                    if index == 0:
                        continue

                    d_values = get_values_from_line(line.split("\t"))
                    self.qepest.get_qex_values(d_values)

                    if self.qepest_file.format == QEPestFormat.TXT:
                        self._write_txt_line(line, wr)
                    else:
                        self._write_json_line(line, wr)

            if not self.error:
                logger.info("Computation completed")
            else:
                logger.warning("Finished with errors")

        except FileNotFoundError:
            self.error = True
            logger.error(f"Error: can't find: {self.qepest_file.input_file}")
