from kafka import KafkaConsumer
from models.tags_values import TagsValuesModel
from modules.enums import kafkaSetup
from modules.eventProcess import EventProcess
from json import loads
from interfaces.strategy import *
from modules.publish_kafka import publish_kafka
from modules.utils import logging
from database.connection import db_client
from modules.utils import logging

class Processor(Strategy):

  def __init__(self) -> None:
      self.db_client = db_client.connect()

  def getBeforeProcess(self, consumer)-> None:
    for msg in consumer:
      logging.info("Consuming event on topic %s, partition %s and offset %s", kafkaSetup.TOPIC_TAGS, msg.partition, msg.offset)
      tags = msg.value
      try:
        roller1 = tags["read"]["RD1_PV_VRM01_POSITION_ROLLER_1"]
        roller2 = tags["read"]["RD1_PV_VRM01_POSITION_ROLLER_2"]
        on_off  = tags["read"]["RD1_MD_VRM01_ON_OFF"]
        tags_json = tags
      except:
        tags_json = loads(tags)
        roller1 = tags_json["read"]["RD1_PV_VRM01_POSITION_ROLLER_1"]
        roller2 = tags_json["read"]["RD1_PV_VRM01_POSITION_ROLLER_2"]
        on_off  = tags_json["read"]["RD1_MD_VRM01_ON_OFF"]

      del tags_json["read"]["RD1_PV_VRM01_POSITION_ROLLER_1"]
      del tags_json["read"]["RD1_PV_VRM01_POSITION_ROLLER_2"]

      #Instanciando os processamentos
      event_process = EventProcess(tags_json)
      avg = event_process.processor_avg(roller1, roller2, on_off)
      event_process = event_process.add_avg_json(tags_json, avg)

      #Consulta do banco
      query_result = TagsValuesModel.objects(timestamp=event_process['timestamp'])
      tags_values = query_result.first()

      #Salvando no Mongo
      if tags_values == None:
          tags_values = TagsValuesModel()
          tags_values.timestamp = event_process['timestamp']
          tags_values.read = event_process['read']
          tags_values.predicted = {}
          tags_values.save()
          logging.info('Saving read values on database')

      else:
          tags_values.read = event_process['read']
          tags_values.save()
          logging.info('Saving read values on database')

      #Publicando aviso no Kafka
      publish_kafka({'Alert': 'Has new value'})

