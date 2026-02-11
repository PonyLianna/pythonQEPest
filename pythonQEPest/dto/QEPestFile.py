from typing import Optional

from pydantic import BaseModel


class QEPestFile(BaseModel):
    input_file: Optional[str] = None
    output_file: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.input_file is None:
            self.input_file = "data.txt"

        if self.output_file is None:
            self.output_file = f"{self.input_file}.out"
