import pytest

from pythonQEPest.helpers.norm import norm_i, norm_h, norm, norm_f


class TestNorm:
    def test_norm_basic(self):
        arr = [10, 20, 30]
        d = 20

        assert norm(arr, d, 1) == 1.0
        assert norm(arr, d, 2) == 20 / 30
        assert norm(arr, d, 0) == 2.0

    def test_norm_zero_div(self):
        arr = [10, 0, 30]
        d = 5
        assert norm(arr, d, 1) == 0.0

    def test_norm_out_of_range(self):
        arr = [1, 2, 3]
        with pytest.raises(KeyError):
            norm(arr, 2, 5)

    def test_norm_negative_descr(self):
        arr = [1, 2, 3]
        assert norm(arr, 2, -1) == 2 / 3

    def test_norm_h(self):
        assert norm_h(69.5849922, 0) == 1.0
        assert norm_h(0, 2) == 0.0
        assert pytest.approx(norm_h(60, 1), rel=1e-6) == 60 / 94.4228257

    def test_norm_i(self):
        assert norm_i(78.2919965, 0) == 1.0
        assert norm_i(0, 3) == 0.0
        assert pytest.approx(norm_i(66, 1), rel=1e-6) == 66 / 71.2829691

    def test_norm_f(self):
        assert norm_f(53.3719946, 0) == 1.0
        assert norm_f(0, 5) == 0.0
        assert pytest.approx(norm_f(70, 2), rel=1e-6) == 70 / 73.7976536

    def test_norm_invalid_descr_type(self):
        arr = [1, 2, 3]
        with pytest.raises(TypeError):
            norm(arr, 1, "not_an_int")
