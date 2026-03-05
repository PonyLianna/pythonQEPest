from typing import Optional

from pydantic import BaseModel
from pythonQEPest.dto.QEPestData import QEPestData


class QEPestOutput(BaseModel):
    data: QEPestData
    name: Optional[str] = ""

    def to_array(self) -> list:
        values = list(self.data.root.values())
        return [self.name] + values
