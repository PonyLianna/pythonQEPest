from pathlib import Path
from pythonQEPest.providers.json_provider import JSONConfigProvider


class TestChangeConfigs:
    def test_load_raw_json(self):
        data = {
            "herb": {
                "coefficients": [
                    [10.0, 20.0, 30.0, 40.0],
                    [15.0, 25.0, 35.0, 45.0],
                    [12.0, 22.0, 32.0, 42.0],
                    [18.0, 28.0, 38.0, 48.0],
                    [11.0, 21.0, 31.0, 41.0],
                    [14.0, 24.0, 34.0, 44.0],
                ],
                "normaliser": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
            },
            "insect": {
                "coefficients": [
                    [5.0, 10.0, 15.0, 20.0],
                    [25.0, 30.0, 35.0, 40.0],
                    [45.0, 50.0, 55.0, 60.0],
                    [65.0, 70.0, 75.0, 80.0],
                    [85.0, 90.0, 95.0, 100.0],
                    [105.0, 110.0, 115.0, 120.0],
                ],
                "normaliser": [200.0, 200.0, 200.0, 200.0, 200.0, 200.0],
            },
        }

        config = JSONConfigProvider().load_raw_json(data)

        assert config is not None
        pest_names = config.get_pest_names()
        assert "herb" in pest_names
        assert "insect" in pest_names
        assert len(pest_names) == 2

        herb_coeffs = config.get_coefficients("herb")
        assert len(herb_coeffs) == 6
        assert herb_coeffs[0] == (10.0, 20.0, 30.0, 40.0)

        herb_norm = config.get_normaliser("herb")
        assert herb_norm == (100.0, 100.0, 100.0, 100.0, 100.0, 100.0)

        insect_norm = config.get_normaliser("insect")
        assert insect_norm == (200.0, 200.0, 200.0, 200.0, 200.0, 200.0)

    def test_load_from_file(self):
        config_path = Path(__file__).parent / "test_config.json"

        config = JSONConfigProvider().load(config_path)

        assert config is not None
        pest_names = config.get_pest_names()
        assert "herb" in pest_names
        assert len(pest_names) == 1

        herb_coeffs = config.get_coefficients("herb")
        assert len(herb_coeffs) == 6

        herb_norm = config.get_normaliser("herb")
        assert herb_norm == (100.0, 100.0, 100.0, 100.0, 100.0, 100.0)
