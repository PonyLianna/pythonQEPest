from pythonQEPest.config.config_provider import ConfigProvider
from pythonQEPest.config.qepest_config import QEPestConfig, PestTypeConfig
from pythonQEPest.core.qepest import QEPest
from pythonQEPest.dto import PestTypeCoefficient
from pythonQEPest.dto import QEPestInput


def random_coefficients() -> list:
    return [
        (53.506563385007496, 222.26815379980897, 14.19499523870596, 272.5424991172166),
        (46.00715643037571, 350.16089820262516, 208.06156087128122, 492.8206056952804),
        (138.64460966233446, 241.53026279945124, 377.8993212072419, 174.0669648564985),
        (180.6998401258752, 323.1726892417753, 485.14617786028015, 443.1012676802161),
        (215.3285314998089, 361.68177460255873, 342.7354563068766, 192.3337134546996),
        (125.13208437424792, 48.40447428920039, 440.66537907336544, 38.00801457055535),
    ]


def random_normaliser() -> tuple:
    return (
        259.82936625344365,
        269.23065237533837,
        73.92347759714227,
        328.30992675910346,
        457.99577359338286,
        388.29035194219455,
    )


COEFFICIENTS = [
    (10.0, 20.0, 30.0, 40.0),
    (15.0, 25.0, 35.0, 45.0),
    (12.0, 22.0, 32.0, 42.0),
    (18.0, 28.0, 38.0, 48.0),
    (11.0, 21.0, 31.0, 41.0),
    (14.0, 24.0, 34.0, 44.0),
]

NORMALISERS = (100.0, 100.0, 100.0, 100.0, 100.0, 100.0)


class SinglePestProvider(ConfigProvider):
    def __init__(self, coeffs, normalisers):
        # (100.0, 100.0, 100.0, 100.0, 100.0, 100.0)
        self.coeffs = coeffs
        self.normalisers = normalisers

    def load(self) -> QEPestConfig:
        return QEPestConfig(
            pest_types=[
                PestTypeConfig(
                    name="custom",
                    coefficients=PestTypeCoefficient.model_validate(self.coeffs),
                    normaliser=self.normalisers,
                )
            ]
        )


class CustomTestConfigProvider(ConfigProvider):
    def __init__(self):
        self._config = self._build_config()

    def _build_config(self) -> QEPestConfig:
        pest_types = []
        for pest_name in ["herb", "insect", "fung"]:
            pest_types.append(
                PestTypeConfig(
                    name=pest_name,
                    coefficients=PestTypeCoefficient.model_validate(
                        random_coefficients()
                    ),
                    normaliser=random_normaliser(),
                )
            )
        return QEPestConfig(pest_types=pest_types)

    def load(self) -> QEPestConfig:
        return self._config


class TestCustomConfig:
    def make_input(self, name="test", mw=120.5, logp=3.1, hba=2, hbd=1, rb=4, ar=1):
        return QEPestInput(
            name=name,
            mol_weight=mw,
            log_p=logp,
            hbond_acceptors=hba,
            hbond_donors=hbd,
            rotatable_bonds=rb,
            aromatic_rings=ar,
        )

    def test_custom_config_produces_different_results(self):
        qepest_default = QEPest()
        qepest_custom = QEPest(provider=CustomTestConfigProvider())

        inp = self.make_input("mol1", 240.2127, 3.2392, 5, 1, 4, 1)

        result_default = qepest_default.compute_params(inp)

        assert result_default.to_array() == ["mol1", 0.8511, 0.5339, 0.6224]

        result_custom = qepest_custom.compute_params(inp)

        assert result_custom.to_array() == ["mol1", 1.2516, 1.2516, 1.2516]

        assert result_default.data.qe_herb != result_custom.data.qe_herb
        assert result_default.data.qe_insect != result_custom.data.qe_insect
        assert result_default.data.qe_fung != result_custom.data.qe_fung

    def test_custom_config_same_seed_produces_consistent_results(self):
        provider1 = CustomTestConfigProvider()
        provider2 = CustomTestConfigProvider()

        qepest1 = QEPest(provider=provider1)
        qepest2 = QEPest(provider=provider2)

        inp = self.make_input("test", 200.0, 2.5, 3, 2, 5, 1)

        result1 = qepest1.compute_params(inp)
        result2 = qepest2.compute_params(inp)

        assert result1.data.qe_herb == result2.data.qe_herb
        assert result1.data.qe_insect == result2.data.qe_insect
        assert result1.data.qe_fung == result2.data.qe_fung

    def test_custom_config_with_single_pest_type(self):
        qepest = QEPest(
            provider=SinglePestProvider(coeffs=COEFFICIENTS, normalisers=NORMALISERS)
        )
        inp = self.make_input("test", 100.0, 1.0, 1, 1, 1, 1)

        result = qepest.compute_params(inp)

        assert hasattr(result.data, "qe_custom")
        assert qepest.get_names() == ["custom"]

    def test_change_configs(self):
        qepest_default = QEPest()

        inp = self.make_input("mol1", 240.2127, 3.2392, 5, 1, 4, 1)

        result_default = qepest_default.compute_params(inp)

        assert result_default.to_array() == ["mol1", 0.8511, 0.5339, 0.6224]

        qepest_default.initialise_config(CustomTestConfigProvider())

        results_after_changing = qepest_default.compute_params(inp)

        assert results_after_changing.to_array() == ["mol1", 1.2516, 1.2516, 1.2516]

        assert result_default.data.qe_herb != results_after_changing.data.qe_herb
        assert result_default.data.qe_insect != results_after_changing.data.qe_insect
        assert result_default.data.qe_fung != results_after_changing.data.qe_fung

    def test_change_configs_aggressively(self):
        qepest_default = QEPest()

        inp = self.make_input("mol1", 240.2127, 3.2392, 5, 1, 4, 1)

        result_default = qepest_default.compute_params(inp)

        assert result_default.to_array() == ["mol1", 0.8511, 0.5339, 0.6224]

        assert result_default.data.qe_fung == 0.6224
        assert result_default.data.qe_insect == 0.5339
        assert result_default.data.qe_herb == 0.8511

        qepest_default.initialise_config(
            SinglePestProvider(coeffs=COEFFICIENTS, normalisers=NORMALISERS)
        )

        result_aggressive = qepest_default.compute_params(inp)

        assert result_aggressive.to_array() == ["mol1", 0.5199]
        assert result_aggressive.data.qe_custom == 0.5199
