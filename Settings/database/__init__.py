"""
Database Init.
"""

from mongoengine import connect, DEFAULT_CONNECTION_NAME

from configs import db_configs
from modules.utils import terminate

db_connections = {}

if db_configs is None:
    terminate('There are no databases configured!')

for index, db_config in enumerate(db_configs):
    db_name = db_config.get('db_name')

    alias = DEFAULT_CONNECTION_NAME if (index == 0) else db_name

    db_connections.update({db_name: alias})

    connect(
        db=db_name,
        alias=alias,
        host=db_config.get('db_host'),
        port=db_config.get('db_port'),
        username=db_config.get('db_user'),
        password=db_config.get('db_pass'),
        authentication_source='admin'
    )
