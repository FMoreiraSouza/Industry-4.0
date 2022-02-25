from __future__ import annotations
from abc import ABC, abstractmethod
from .observable import *

class Observer(ABC):

    @abstractmethod
    def update(self, subject: Subject):
        pass