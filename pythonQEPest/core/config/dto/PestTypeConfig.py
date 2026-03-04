from pydantic import BaseModel
from pythonQEPest.core.config.dto import PestTypeCoefficient


class PestTypeConfig(BaseModel):
    name: str
    coefficients: PestTypeCoefficient
    normaliser: tuple[float, float, float, float, float, float]
