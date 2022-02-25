import traceback
from time import sleep

import OpenOPC
import pywintypes
from pendulum import now

from configs.collector import max_connect_attempts, max_reading_attempts, max_interval_reading
from modules.connector import Connector
from modules.dispatcher import dispatcher
from modules.enums import TagsDataFrame
from modules.tags import Tags
from modules.utils import terminate, stopwatch, log

pywintypes.datetime = pywintypes.TimeType


def collector():
    #All system tags and their properties.
    tags = Tags()
    #Create a connector object to connect opc_client to opc_servers.
    connector = Connector(max_connect_attempts)

    if tags.empty():
        terminate('No tags found.')

    # Create an list of collectors.
    # tags.get[TagsDataFrame.SERVER_COLUMN].unique() => This code discovers the servers to connect.
    # (server, OpenOPC.client()) for server => This code create a tuple for each opc_client and opc_server.
    collector_list = [(server, OpenOPC.client()) for server in tags.get[TagsDataFrame.SERVER_COLUMN].unique()]

    # Connect the opc_client to all servers using the previous list.
    connector.connect_all(collector_list)

    """
    This is necessary because opc module doesn't work with thread schedule. 
    The solution is to see if the time arrived and trigger the collection.
    """
    while True:
        # To check if it's time to collect data
        if stopwatch(max_interval_reading) == 0:
            # Capture actual time.
            timestamp = now()

            # Update tags.
            tags.update()

            # Create an empty list of raw values.
            raw_values = []

            # For each pair client and server try to read values.
            for server, opc_client in collector_list:
                """
                Try to read until max_reading_attempts. If this limit is reached,
                the collection will not be done int this period and new max_reading_attempts 
                will be tried in the next.
                """
                for attempt in range(1, (max_reading_attempts + 1)):
                    try:
                        log('info', f'Attempt {attempt} of {max_reading_attempts} to read data from {server}.')

                        # Pick all tags by server name.
                        tag_id_list = tags.where(TagsDataFrame.SERVER_COLUMN, server).pick(TagsDataFrame.ID_COLUMN)

                        # Update raw_values with the tags' value collected.
                        raw_values.extend(opc_client.read(tag_id_list))
                    except Exception:
                        log('error', f'Error reading data from {server} server.', traceback.format_exc())
                        # Close connection
                        opc_client.close()
                        # Reconnect
                        connector.connect(opc_client, server)
                    else:
                        # The code sleeps between attemps or collections.
                        sleep((1 / len(collector_list)))
                        break

            # Send the values obtained to dispatcher persist them.
            if raw_values:
                dispatcher(raw_values=raw_values, timestamp=timestamp)
