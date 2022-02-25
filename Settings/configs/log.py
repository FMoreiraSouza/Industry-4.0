"""
Log System Config.
"""

from loguru import logger
from pendulum import today

from configs import project_root

log_file = project_root \
    .joinpath('logs') \
    .joinpath("{}.{}".format(today().to_date_string(), 'log'))

logger.add(
    log_file,
    format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
    level='DEBUG',
    retention='1 week',
    backtrace=True,
    diagnose=True,
    enqueue=True
)
