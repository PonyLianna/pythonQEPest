import math


def compute_df(x, a, b, c, o) -> float:
    return a * math.exp(-1.0 * math.exp(-1.0 * ((x - b) / c)) - (x - b) / c + 1.0) + o
