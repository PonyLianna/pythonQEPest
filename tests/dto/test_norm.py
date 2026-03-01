import pytest

from pythonQEPest.dto.normalisation.Normaliser import Normaliser

# from pythonQEPest.helpers.norm import norm_i, norm_h, norm, norm_f


class TestNorm:
    def test_norm_basic(self):
        arr = [10, 20, 30]
        d = 20

        normaliser = Normaliser(arr)

        assert normaliser.norm(d, 1) == 1.0
        assert normaliser.norm(d, 2) == 20 / 30
        assert normaliser.norm(d, 0) == 2.0

    def test_norm_zero_div(self):
        arr = [10, 0, 30]
        d = 5

        normaliser = Normaliser(arr)

        assert normaliser.norm(d, 1) == 0.0

    def test_norm_out_of_range(self):
        arr = [1, 2, 3]

        normaliser = Normaliser(arr)
        with pytest.raises(KeyError):
            normaliser.norm(2, 5)

    def test_norm_negative_descr(self):
        arr = [1, 2, 3]

        normaliser = Normaliser(arr)

        assert normaliser.norm(2, -1) == 2 / 3

    def test_norm_h(self):
        from pythonQEPest.config import normalise_default

        normaliser = Normaliser(normalise_default["herb"])

        assert normaliser.norm(69.5849922, 0) == 1.0
        assert normaliser.norm(0, 2) == 0.0
        assert pytest.approx(normaliser.norm(60, 1), rel=1e-6) == 60 / 94.4228257

    def test_norm_i(self):
        from pythonQEPest.config import normalise_default

        normaliser = Normaliser(normalise_default["insect"])

        assert normaliser.norm(78.2919965, 0) == 1.0
        assert normaliser.norm(0, 3) == 0.0
        assert pytest.approx(normaliser.norm(66, 1), rel=1e-6) == 66 / 71.2829691

    def test_norm_f(self):
        from pythonQEPest.config import normalise_default

        normaliser = Normaliser(normalise_default["fung"])

        assert normaliser.norm(53.3719946, 0) == 1.0
        assert normaliser.norm(0, 5) == 0.0
        assert pytest.approx(normaliser.norm(70, 2), rel=1e-6) == 70 / 73.7976536

    def test_norm_invalid_descr_type(self):
        arr = [1, 2, 3]

        normaliser = Normaliser(arr)

        with pytest.raises(TypeError):
            normaliser.norm(1, "not_an_int")
