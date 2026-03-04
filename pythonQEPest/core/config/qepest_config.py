from typing import Optional

from pydantic import BaseModel

from pythonQEPest.core.config.dto import PestTypeConfig


class QEPestConfig(BaseModel):
    name: Optional[str] = "HerbInsectFung"
    pest_types: list[PestTypeConfig]

    def get_pest_names(self) -> list[str]:
        return [pest.name for pest in self.pest_types]

    def get_coefficients(
        self, pest_name: str
    ) -> list[tuple[float, float, float, float]]:
        for pest in self.pest_types:
            if pest.name == pest_name:
                return pest.coefficients.as_set()

        raise ValueError(f"Pest type '{pest_name}' not found")

    def get_normaliser(
        self, pest_name: str
    ) -> tuple[float, float, float, float, float, float]:
        for pest in self.pest_types:
            if pest.name == pest_name:
                return pest.normaliser

        raise ValueError(f"Pest type '{pest_name}' not found")
