from pydantic import RootModel, model_validator


class QEPestData(RootModel[dict[str, float]]):
    @model_validator(mode="before")
    @classmethod
    def handle_input(cls, data):
        if data is None:
            return {}
        if isinstance(data, dict):
            return data
        return data

    def __getattr__(self, name: str) -> float:
        return self.root.get(name, 0.0)

    def __setattr__(self, name: str, value: float) -> None:
        if name == "root":
            super().__setattr__(name, value)
        else:
            self.root[name] = value
