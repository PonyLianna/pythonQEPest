def get_values_from_line(lst: list | tuple | set) -> list[float]:
    return [float(x) for x in lst[1:]]
