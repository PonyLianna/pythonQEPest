from abc import ABC, abstractmethod

from pythonQEPest.core.qepest import QEPest


class QEPestMeta(ABC):
    def __init__(self, root):
        self.root = root
        self.root.title("PythonQEPest")

        self.qepest = QEPest()

        self.build_gui()

    @abstractmethod
    def build_gui(self):
        pass
