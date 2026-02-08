from typing import Optional
from pydantic import BaseModel

from .QEPestData import QEPestData


class QEPestOutput(BaseModel):
    data: QEPestData
    name: Optional[str] = ""

    def to_array(self) -> list:
        return [
            self.name,
            self.data.qe_h,
            self.data.qe_i,
            self.data.qe_f
        ]
