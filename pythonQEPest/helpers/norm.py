def norm(arr: list | tuple, d: int | float, descr: int) -> float:
    if descr > len(arr):
        raise KeyError(f"Out of array. {descr} > {len(arr)}")

    max_val = arr[int(descr)]
    return d / max_val if max_val != 0 else 0.0


def norm_h(d: int | float, descr: int) -> float:
    return norm(
        (69.5849922, 94.4228257, 120.4572352, 228.1589796, 89.7012502, 276.9634213),
        d,
        descr,
    )


def norm_i(d: int | float, descr: int) -> float:
    return norm(
        (78.2919965, 71.2829691, 133.9224801, 331.170104, 70.5540709, 193.0023343),
        d,
        descr,
    )


def norm_f(d: int | float, descr: int) -> float:
    return norm(
        (53.3719946, 52.773116, 73.7976536, 144.9887053, 41.4385926, 102.3024319),
        d,
        descr,
    )
