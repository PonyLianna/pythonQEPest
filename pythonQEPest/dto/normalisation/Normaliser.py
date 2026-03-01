from typing import Union


class Normaliser:
    def __init__(self, arr: Union[tuple, list]):
        # if len(arr) != 6:
        #     raise ValueError(f"Array must be exact length of 6. Given: {len(arr)}")

        self.arr = arr

    def norm(self, d: Union[int, float], descr: int) -> float:
        if descr > len(self.arr):
            raise KeyError(f"Out of array. {descr} > {len(self.arr)}")

        max_val = self.arr[int(descr)]
        return d / max_val if max_val != 0 else 0.0
