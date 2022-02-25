from interfaces.observer import *
from interfaces.observable import *
from managers.ai_procedure import *
import logging


class RunProcedure(Observer):
    def update(self, subject: Subject, consumer) -> None:
        for msg in consumer:
            logging.info("Reacting to message")
            ai_procedure()