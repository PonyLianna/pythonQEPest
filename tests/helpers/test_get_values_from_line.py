import pytest

from pythonQEPest.helpers.get_values_from_line import get_values_from_line


class TestGetValuesFromLine:
    basic_list = ["id", "1.1", "2.2", "3.3"]
    basic_list_result = [1.1, 2.2, 3.3]

    basic_tuple = ("id", "5", "6.6")
    basic_tuple_result = [5.0, 6.6]

    def test_basic_list(self):
        assert get_values_from_line(self.basic_list) == self.basic_list_result

    def test_basic_tuple(self):
        assert get_values_from_line(self.basic_tuple) == self.basic_tuple_result

    def test_empty(self):
        assert get_values_from_line([]) == []
        assert get_values_from_line(()) == []

    def test_only_one_elem(self):
        assert get_values_from_line(["id"]) == []

    def test_non_numeric(self):
        with pytest.raises(ValueError):
            get_values_from_line(["id", "foo", "bar"])

    def test_numeric_strings(self):
        lst = ["id", "10", "11.5", "-2.2", "0"]
        assert get_values_from_line(lst) == [10.0, 11.5, -2.2, 0.0]
