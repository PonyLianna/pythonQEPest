from typing import Optional, List

from pydantic import BaseModel

from pythonQEPest.dto.coefficients import QEPestCoefficient


class QEPestCoefficientList(BaseModel):
    name: Optional[str]
    named_coefficients: List[QEPestCoefficient]

    # TODO: Done all the cases and make some sort of docs here, pls
    def __init__(self, *args, **kwargs):
        if args:
            named_coeff = args[0]
            if len(named_coeff) == 1:
                pass
            elif len(named_coeff) > 1:
                if isinstance(named_coeff, dict):
                    lst = [QEPestCoefficient({i: z}) for i, z in named_coeff.items()]
                    super().__init__(name="generic", named_coefficients=lst)

        elif kwargs:
            super().__init__(**kwargs)
        else:
            raise ValueError(
                "No name and coefficients provided. Please provide either a "
                + "name and coefficients tuple or keyword arguments."
            )
