import math

from pythonQEPest.helpers.check_nan import check_nan


class TestCheckNAN:
    lst_good = [0.0, 0.1, 0.2]
    lst_bad = [math.nan, float('nan'), 0.0]
    lst_bad_result = [0.0, 0.0, 0.0]
    lst_strange = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, -45.43, math.nan, float("inf")]
    lst_strange_result = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, -45.43, 0.0, float("inf")]

    def test_check_nan(self):
        result = check_nan(self.lst_good)
        assert result == self.lst_good

    def test_check_nan_bad(self):
        result = check_nan(self.lst_bad)
        assert result == self.lst_bad_result

    def test_check_nan_strange(self):
        result = check_nan(self.lst_strange)
        assert result == self.lst_strange_result