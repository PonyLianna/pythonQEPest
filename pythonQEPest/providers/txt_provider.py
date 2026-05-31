from pathlib import Path

from pythonQEPest.config.config_provider import ConfigProvider
from pythonQEPest.config.qepest_config import QEPestConfig, PestTypeConfig


class TXTConfigProvider(ConfigProvider):
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> QEPestConfig:
        with open(self.path, encoding="utf-8") as f:
            lines = f.readlines()

        pest_types_dict: dict[str, dict] = {}
        current_pest = None

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                current_pest = line[1:-1]
                pest_types_dict[current_pest] = {"coefficients": [], "normaliser": []}
            elif current_pest and "=" in line:
                key, value = line.split("=", 1)
                if key.strip() == "coefficients":
                    parts = [float(x.strip()) for x in value.strip().split(",")]
                    for i in range(0, len(parts), 4):
                        pest_types_dict[current_pest]["coefficients"].append(
                            tuple(parts[i : i + 4])
                        )
                elif key.strip() == "normaliser":
                    parts = [float(x.strip()) for x in value.strip().split(",")]
                    pest_types_dict[current_pest]["normaliser"] = tuple(parts)

        pest_types = []
        for pest_name, pest_data in pest_types_dict.items():
            pest_types.append(
                PestTypeConfig(
                    name=pest_name,
                    coefficients=pest_data["coefficients"],
                    normaliser=tuple(pest_data["normaliser"]),
                )
            )

        return QEPestConfig(pest_types=pest_types)
