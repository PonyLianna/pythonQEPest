from pydantic import RootModel


class QEPestData(RootModel[dict[str, float]]):
    def __getattr__(self, name: str) -> float:
        return self.root.get(name, 0.0)

    def __setattr__(self, name: str, value: float) -> None:
        if name == "root":
            super().__setattr__(name, value)
        else:
            self.root[name] = value
