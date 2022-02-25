from pendulum import now, parse

import logging
import json

# Setup logging 
logging.basicConfig(
  format='[%(asctime)s.%(msecs)s:%(name)s:%(thread)d]' +
         ' %(levelname)s - %(message)s',
  level=logging.INFO
)

def json_serializer(data):
    return lambda x: json.dumps(x).encode("utf-8")

def json_desializer(data):
    return lambda m: json.loads(m.decode('utf-8'))

def stopwatch(seconds: int) -> int:
    """A simple stopwatch.

    Args:
        seconds (int): The amount of seconds to be counted.

    Returns:
        int: The time remaining to finish the stopwatch.
    """
    time_remainder = now().second % seconds

    return (seconds - time_remainder) if (time_remainder > 0) else 0

def next_time_to_predict(dataframe):
    """
        This function receives a dataframe in descendent order, with
        the last time with read values in the first position and returns
        a datetime object representing the next time that read values
        will be collected.
    """
    timestamp = dataframe.iloc[0][0]
    last_time_read = parse(timestamp)

    return last_time_read.add(seconds=30)

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}