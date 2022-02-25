from interfaces.observer import *
from interfaces.strategy import *


class RunProcessor(Observer):

    def __init__(self, strategy: Strategy):
        self._strategy = strategy
        
    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy):
        self._strategy = strategy

    def update(self, subject: Subject, consumer) -> None:
        self._strategy.getBeforeProcess(consumer)