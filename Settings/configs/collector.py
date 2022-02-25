"""
Collector Configs.

The collector must not be configured directly here,
the settings related to it must be performed in the config.yaml file.
"""
from configs import collector_configs

max_connect_attempts = collector_configs.get('max_connect_attempts', 5)
max_reading_attempts = collector_configs.get('max_reading_attempts', 3)
max_interval_reading = collector_configs.get('max_interval_reading', 30)
