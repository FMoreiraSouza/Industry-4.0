from kafka import KafkaConsumer
from modules.enums import kafkaSetup
from modules.utils import logging
from json import loads
from interfaces.observer import *
from interfaces.strategy import *

class ConcreteSubject(Subject):

    def __init__(self):
        self._state = "State: No message"
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        logging.info("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, consumer) -> None:
        self._state = "With message."
        logging.info("State: %s", self._state)
        logging.info("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self, consumer)

    def data_pre_processing_logic(self) -> None:

        logging.info("%s", self._state)
        
        consumer = KafkaConsumer(
            bootstrap_servers=[kafkaSetup.BROKER],
            enable_auto_commit=kafkaSetup.OFFSET_COMMIT,
            group_id=kafkaSetup.GROUP_ID,
            client_id=kafkaSetup.CLIENT_ID,
            auto_offset_reset=kafkaSetup.OFFSET_RESET,
            value_deserializer=lambda m: loads(m.decode('utf-8'))
        )

        consumer.subscribe([kafkaSetup.TOPIC_TAGS])

        logging.info("Receiving data")

        logging.info("Subscribe on kafka cluster %s", kafkaSetup.BROKER)
        self.notify(consumer)
