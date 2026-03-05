from pythonQEPest.config.config_provider import ConfigProvider
from pythonQEPest.config.qepest_config import QEPestConfig, PestTypeConfig
from pythonQEPest.dto import PestTypeCoefficient


class DefaultConfigProvider(ConfigProvider):
    def load(self) -> QEPestConfig:
        from pythonQEPest.config.qepest_default import qepest_default
        from pythonQEPest.config.normalise import normalise_default

        pest_types = []
        for pest_name in qepest_default.keys():
            pest_types.append(
                PestTypeConfig(
                    name=pest_name,
                    coefficients=PestTypeCoefficient.model_validate(
                        qepest_default[pest_name]
                    ),
                    normaliser=normalise_default[pest_name],
                )
            )

        return QEPestConfig(pest_types=pest_types)
