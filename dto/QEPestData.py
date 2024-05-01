from pydantic import BaseModel


class QEPestData (BaseModel):
    qeh: float
    qei: float
    qef: float
