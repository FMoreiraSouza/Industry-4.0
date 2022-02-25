"""
Database Config.
"""
import sys
from os import getenv
from mongoengine import connect
from pymongo import MongoClient

class db_client:
    __connection = None

    @classmethod
    def connect(cls) -> MongoClient:
        """Connect to MongoDB.

        Args:
            db_host (str): The database host address.
            db_port (int): The database port.
            db_user (str): The database user.
            db_pass (str): The database pass.

        Returns:
            DBClient: An instance of DBClient.
        """

        try:
            if not cls.__connection:
                cls.__connection = connect(host="mongodb+srv://fmoreira12:persistirdados@cluster1.rcyev.mongodb.net/pythia?retryWrites=true&w=majority")
            return cls.__connection
        except Exception as err:
            sys.exit(1)