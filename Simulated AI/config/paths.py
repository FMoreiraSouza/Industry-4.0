"""
Path Config.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR.joinpath('.env')
