from typing import Union


def get_values_from_line(lst: Union[list, tuple, set]) -> list[float]:
    return [float(x) for x in lst[1:]]
