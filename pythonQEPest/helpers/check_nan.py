import math


def check_nan(d) -> list[float]:
    for i in range(len(d)):
        if math.isnan(d[i]):
            d[i] = 0.0
    return d
