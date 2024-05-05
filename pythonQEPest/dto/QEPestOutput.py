from pydantic import BaseModel

from .QEPestData import QEPestData


class QEPestOutput(BaseModel):
    data: QEPestData
    name: str = ""
