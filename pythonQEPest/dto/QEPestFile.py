from enum import Enum
from typing import Optional

from pydantic import BaseModel, model_validator


class QEPestFormat(Enum):
    TXT = "txt"
    JSON = "json"


class QEPestFile(BaseModel):
    input_file: Optional[str] = None
    output_file: Optional[str] = None
    format: Optional[QEPestFormat] = QEPestFormat.TXT
    smiles: Optional[bool] = False

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def set_defaults(self):
        if self.input_file is None:
            self.input_file = "data.txt"

        if self.format is None:
            self.format = QEPestFormat.TXT

        formatted_output = self.input_file.replace(".txt", "").replace(".json", "")
        if self.format == QEPestFormat.JSON:
            self.output_file = f"{formatted_output}.out.json"
        else:
            self.output_file = f"{formatted_output}.out.txt"

        return self
