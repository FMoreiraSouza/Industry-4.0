from enum import Enum


class State(Enum):
    """State Enum.
    """
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class TagsDataFrame:
    """Tags DataFrame Enum.
    """
    ID_COLUMN = 'tag_id'
    NAME_COLUMN = 'tag_name'
    SERVER_COLUMN = 'server'
    DB_ALIAS_COLUMN = 'db_alias'
