from enum import Enum

class State(Enum):
    """State Enum.
    """
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class kafkaSetup:
    """
    Values for kafka config
    """
    BROKER          = "127.0.0.1:9092"
    TOPIC_TAGS      = "raw_values"
    TOPIC_TARGET    = "notifier"
    GROUP_ID        = "processor"
    CLIENT_ID       = "processor-client"
    OFFSET_RESET    = "earliest"
    OFFSET_COMMIT   = True