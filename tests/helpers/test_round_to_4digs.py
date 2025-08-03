from pythonQEPest.helpers.round_to_4digs import round_to_4digs


class TestRoundToFourDigs:
    def test_round_basic(self):
        assert round_to_4digs(1.23456) == 1.2346
        assert round_to_4digs(1.23454) == 1.2345

    def test_round_int(self):
        assert round_to_4digs(42) == 42.0
        assert round_to_4digs(0) == 0.0

    def test_round_negative(self):
        assert round_to_4digs(-1.98765) == -1.9876

    def test_round_exact(self):
        assert round_to_4digs(3.1415) == 3.1415
        assert round_to_4digs(3.1415926) == 3.1416

    def test_round_small(self):
        assert round_to_4digs(0.00009) == 0.0001
        assert round_to_4digs(0.00005) == 0.0001
        assert round_to_4digs(0.0001) == 0.0001
