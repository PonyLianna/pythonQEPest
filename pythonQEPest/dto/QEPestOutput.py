from typing import Optional

from pydantic import BaseModel


class QEPestOutput(BaseModel):
    data: BaseModel
    name: Optional[str] = ""

    def to_array(self) -> list:
        return [self.name] + list(self.data.model_dump().values())
