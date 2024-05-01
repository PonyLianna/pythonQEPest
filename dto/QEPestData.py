from pydantic import BaseModel


class QEPestData (BaseModel):
    qeh: str
    qei: str
    qef: str
