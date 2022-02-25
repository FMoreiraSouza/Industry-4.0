import traceback
from typing import Any, List, Tuple
from database.models.tags_values import TagsValuesModel
from pendulum import DateTime
from modules.enums import TagsDataFrame
from modules.tags import Tags
from modules.utils import log
from kafka import KafkaProducer
from modules.Serializer import json_serializer
from datetime import datetime
import pandas as pd


def dispatcher(raw_values: List[Tuple[str, Any, str, str]], timestamp: DateTime) -> None:
    """Data dispatcher for Kafka.

    Args:
        raw_values (List[Tuple[str, Any, str, str]]): A list with values read from the OpenOPC.
        timestamp (DateTime): An instance of DateTime.
    """
    if not raw_values:
        log('error', 'The dispatcher cannot handle an empty reading list.')
        return None

    # Create a producer
    producer = KafkaProducer(bootstrap_servers=['15.228.235.67:9092'], value_serializer=json_serializer)

    # Create tag object
    tags = Tags()

    # Map row by row, assigning each read value to its proper tag.
    values = tags.get['values'] = tags.get[TagsDataFrame.ID_COLUMN] \
        .map({tag: value for tag, value, status, date in raw_values})

    count = 0 # Assistant Accountant
    keyValue = {} # Key concatenation object with value

    # Concatenate each value to its proper tag
    for tag_id in tags.get[TagsDataFrame.NAME_COLUMN]:
        keyValue[tag_id] = values[count]
        count = count + 1

    timestamp = timestamp.in_timezone('UTC')
    #print(timestamp)
    #timestamp = timestamp / 1000
    #timestamp = datetime.fromtimestamp(int(timestamp))


    #Building the values for send on Broker
    tag_values = TagsValuesModel()
    #timestamp = timestamp / 1000
    tag_values.timestamp = timestamp.to_datetime_string()
    tag_values.read = keyValue
    tag_values.predicted = {}

    #Panda = pd.DataFrame(tag_values)
    #print(tag_values.to_json())

    #Send values in a topic with serialization data and defining a key for each
    producer.send("raw_values", tag_values.to_json())

    #, key = tag_values.
    #timestamp.to_datetime_string().encode('utf-8')

    log('info', 'Saving read values on broker')
