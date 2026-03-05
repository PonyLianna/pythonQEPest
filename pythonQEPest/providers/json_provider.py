import json
from pathlib import Path

from pythonQEPest.config.config_provider import ConfigProvider
from pythonQEPest.config.qepest_config import QEPestConfig, PestTypeConfig


class JSONConfigProvider(ConfigProvider):
    def load(self, path: str | Path) -> QEPestConfig:
        path = Path(path)

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        return self.load_raw_json(data)

    def load_raw_json(self, data):
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
