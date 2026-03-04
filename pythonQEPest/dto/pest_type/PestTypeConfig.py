from pydantic import BaseModel

from pythonQEPest.dto.pest_type.PestTypeCoefficient import PestTypeCoefficient


class PestTypeConfig(BaseModel):
    name: str
    coefficients: PestTypeCoefficient
    normaliser: tuple[float, float, float, float, float, float]
