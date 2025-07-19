from pythonQEPest.helpers.get_num_of_cols import get_num_of_cols


class TestGetNumOfCols:
    def test_single_column(self):
        assert get_num_of_cols("hello") == 1

    def test_two_columns(self):
        assert get_num_of_cols("foo\tbar") == 2

    def test_multiple_columns(self):
        assert get_num_of_cols("a\tb\tc\t1\t2\t3") == 6

    def test_empty_string(self):
        assert get_num_of_cols("") == 1

    def test_trailing_tab(self):
        assert get_num_of_cols("foo\tbar\t") == 3

    def test_leading_tab(self):
        assert get_num_of_cols("\tfoo\tbar") == 3

    def test_multiple_tabs(self):
        assert get_num_of_cols("\t\t") == 3
        assert get_num_of_cols("a\t\tb") == 3