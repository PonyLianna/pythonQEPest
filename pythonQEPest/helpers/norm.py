def norm_h(d, descr):
    max_val = (69.5849922, 94.4228257, 120.4572352, 228.1589796, 89.7012502, 276.9634213)[int(descr)]
    return d / max_val if max_val != 0 else 0.0


def norm_i(d, descr):
    max_val = (78.2919965, 71.2829691, 133.9224801, 331.170104, 70.5540709, 193.0023343)[int(descr)]
    return d / max_val if max_val != 0 else 0.0


def norm_f(d, descr):
    max_val = (53.3719946, 52.773116, 73.7976536, 144.9887053, 41.4385926, 102.3024319)[int(descr)]
    return d / max_val if max_val != 0 else 0.0
