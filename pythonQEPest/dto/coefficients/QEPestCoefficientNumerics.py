from pydantic import BaseModel

CoefficientTuple = tuple[float, float, float, float]


class QEPestCoefficientNumerics(BaseModel):
    mw: CoefficientTuple
    logp: CoefficientTuple
    hba: CoefficientTuple
    hbd: CoefficientTuple
    rb: CoefficientTuple
    ar: CoefficientTuple

    def __init__(self, *args, **kwargs):
        if args:
            # In case of [[1,2,3,4],[1,2,3,4],[1,2,3,4]]
            # I don't want it to be a pain to init D:
            if len(args) != 1:
                raise ValueError(
                    f"Expected a single list of coefficients, got {len(args)}"
                )

            coefficients = args[0]
            if len(coefficients) != 6:
                raise ValueError(
                    "Expected list with structure [[1,2,3,4,5,6], ",
                    "[1,2,3,4,5,6], [1,...] ...] got ",
                    f"{len(coefficients)} and {coefficients}",
                )

            coefficients_mapped = {
                field: coefficients[i]
                for i, field in enumerate(["mw", "logp", "hba", "hbd", "rb", "ar"])
            }
            super().__init__(**coefficients_mapped)

        elif kwargs:
            super().__init__(**kwargs)

        else:
            raise ValueError(
                "No coefficients provided. Please provide either a ",
                "list of coefficient tuples or keyword arguments.",
            )
