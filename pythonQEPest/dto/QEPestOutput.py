from typing import Optional

from pydantic import BaseModel
from pythonQEPest.dto.QEPestData import QEPestData


class QEPestOutput(BaseModel):
    data: QEPestData
    name: Optional[str] = ""

    def to_array(self) -> list:
        return [self.name] + list(self.data.model_dump().values())
