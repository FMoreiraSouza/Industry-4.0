from abc import ABC, abstractmethod
from typing import List
class Strategy(ABC):
    @abstractmethod
    def getBeforeProcess(self, data: List):
        pass