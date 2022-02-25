import traceback
from typing import List, Tuple

import OpenOPC

from modules.utils import log, terminate

""" 
It is responsible to manage connection with OPC system.
"""
class Connector:
    def __init__(self, max_conn_attempt: int = 5):
        """Initialize the class.

        Args:
            max_conn_attempt (int, optional): The maximum number of connection attempts. Defaults to 5.
        """
        self.max_conn_attempt = max_conn_attempt

    def connect(self, opc_client: OpenOPC.client, server: str) -> None:
        """ 
          This method try no connect opc_client to a server a max_conn_attempt of times. 
          If somthing goes wrong, a error message will be  in logs.
        """
        for attempt in range(1, (self.max_conn_attempt + 1)):
            try:
                log('info', f'Attempt {attempt} of {self.max_conn_attempt} to connect to the {server} server.')

                opc_client.connect(server)
            except Exception:
                log('error', f'Failed to connect to {server} server.', traceback.format_exc())
            else:
                log('info', f'Connect to {server}.')
                break

        return None

    def connect_all(self, collector_list: List[Tuple[str, OpenOPC.client]]) -> None:
        """Connect to all servers.

        Args:
            collector_list (List[Tuple[str, OpenOPC.client]]): A list of tuples of collectors.
        """
        if not collector_list:
            terminate("The list of collectors is empty.")

        for server, client in collector_list:
            self.connect(client, server)
