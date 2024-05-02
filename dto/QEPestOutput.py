from pydantic import BaseModel
from dto.QEPestData import QEPestData


class QEPestOutput(BaseModel):
    data: QEPestData
    name: str = ""
