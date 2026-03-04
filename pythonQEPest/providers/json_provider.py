import json
from pathlib import Path

from pythonQEPest.config.config_provider import ConfigProvider
from pythonQEPest.config.qepest_config import QEPestConfig, PestTypeConfig


class JSONConfigProvider(ConfigProvider):
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> QEPestConfig:
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)

        pest_types = []
        for pest_name, pest_data in data.items():
            coefficients = [tuple(coef) for coef in pest_data["coefficients"]]
            normaliser = tuple(pest_data["normaliser"])
            pest_types.append(
                PestTypeConfig(
                    name=pest_name,
                    coefficients=coefficients,
                    normaliser=normaliser,
                )
            )

        return QEPestConfig(pest_types=pest_types)
