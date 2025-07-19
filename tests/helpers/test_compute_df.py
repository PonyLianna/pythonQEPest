import math

import pytest

from pythonQEPest.helpers.compute_df import compute_df


class TestComputeDF:
    def test_compute_df_basic(self):
        x, a, b, c, o = 1.0, 2.0, 3.0, 4.0, 5.0
        result = compute_df(x, a, b, c, o)
        assert isinstance(result, float)

    def test_compute_df_shift(self):
        x, a, b, c, o = 10, 2, 10, 3, 7
        result = compute_df(x, a, b, c, o)
        assert isinstance(result, float)
        assert result > o

    def test_compute_df_o(self):
        val1 = compute_df(1, 2, 3, 4, 0)
        val2 = compute_df(1, 2, 3, 4, 100)
        assert math.isclose(val2 - val1, 100, abs_tol=1e-6)

    def test_compute_df_extremes(self):
        assert isinstance(compute_df(1e10, 2, 3, 4, 5), float)
        with pytest.raises(OverflowError):
            compute_df(-1e10, 2, 3, 4, 5)