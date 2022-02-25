"""
Config Init.
"""

from pathlib import Path

from configloader import ConfigLoader

project_root = Path(__file__).parent.parent

config_file = project_root.joinpath('config.yaml')

config = ConfigLoader()
config.update_from_yaml_file(config_file)

# Default config vars.
db_configs = config.get('databases', [])
