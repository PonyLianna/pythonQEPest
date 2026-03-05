from abc import ABC, abstractmethod

from pythonQEPest.config.qepest_config import QEPestConfig


class ConfigProvider(ABC):
    @abstractmethod
    def load(self) -> QEPestConfig:
        pass
