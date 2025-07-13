from pydantic import BaseModel


class QEPestData(BaseModel):
    qe_h: float
    qe_i: float
    qe_f: float
