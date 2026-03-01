class TestQEPestNormalisation:
    def test_qepest_default_coefficients(self):
        from pythonQEPest.config.normalise import normalise_default

        assert "fung" in normalise_default
        assert "herb" in normalise_default
        assert "insect" in normalise_default

        normalise = {
            "herb": (
                69.5849922,
                94.4228257,
                120.4572352,
                228.1589796,
                89.7012502,
                276.9634213,
            ),
            "insect": (
                78.2919965,
                71.2829691,
                133.9224801,
                331.170104,
                70.5540709,
                193.0023343,
            ),
            "fung": (
                53.3719946,
                52.773116,
                73.7976536,
                144.9887053,
                41.4385926,
                102.3024319,
            ),
        }

        assert normalise_default == normalise
