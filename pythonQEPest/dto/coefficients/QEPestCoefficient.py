from pydantic import BaseModel

from pythonQEPest.dto.coefficients import QEPestCoefficientNumerics


class QEPestCoefficient(BaseModel):
    name: str
    coefficients: QEPestCoefficientNumerics

    def __init__(self, *args, **kwargs):
        if args:
            if len(args) != 1:
                raise ValueError(f"Expected len(args) == 1, got {len(args)}")

            # In case of {"test": [[1,2,3,4],[1,2,3,4],[1,2,3,4]}
            if len(args[0]) == 1:
                must_be_dict = args[0]
                if isinstance(must_be_dict, dict):
                    key = list(must_be_dict.keys())[0]
                    coefficients = QEPestCoefficientNumerics(must_be_dict[key])
                    super().__init__(name=key, coefficients=coefficients)

            # In case of ["test", [[1,2,3,4],[1,2,3,4],[1,2,3,4]]
            elif len(args[0]) == 2:
                arr = args[0]
                if (
                    isinstance(arr, tuple)
                    or isinstance(arr, set)
                    or isinstance(arr, list)
                ):
                    name = arr[0]
                    coefficients = QEPestCoefficientNumerics(arr[1])
                    super().__init__(name=name, coefficients=coefficients)

        elif kwargs:
            super().__init__(**kwargs)
        else:
            raise ValueError(
                "No name and coefficients provided. Please provide either a "
                + "name and coefficients tuple or keyword arguments."
            )


if __name__ == "__main__":
    # Example usage
    coefficients = QEPestCoefficient(
        mw=[0.1, 0.2, 0.3, 0.4],
        logp=[0.1, 0.2, 0.3, 0.4],
        hba=[0.1, 0.2, 0.3, 0.4],
        hbd=[0.1, 0.2, 0.3, 0.4],
        rb=[0.1, 0.2, 0.3, 0.4],
        ar=[0.1, 0.2, 0.3, 0.4],
    )
    print(coefficients)

    coefficients_alternative = QEPestCoefficient([[0.1, 0.2, 0.3, 0.4] * 6])
    print(coefficients_alternative)
