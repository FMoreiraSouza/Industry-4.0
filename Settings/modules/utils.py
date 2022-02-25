from pendulum import now

from configs.log import logger


def log(log_type: str, message: str, details: str = None) -> None:
    """Issue a log.

    Args:
        log_type (str): The log type, it can be: info, debug, warning, error and critical.
        message (str): The message.
        details (str, optional): Extra details. Defaults to None.
    """
    logger_method = getattr(logger, log_type.lower())

    logger_method(message)

    if details is not None:
        logger_method(details)


def terminate(reason: str) -> None:
    """Terminate a script and issue a log.

    Args:
        reason (str): The reason the script had to end.
    """
    log('critical', 'Houston, we have a problem.', reason)
    exit(1)


def stopwatch(seconds: int) -> int:
    """A simple stopwatch.

    Args:
        seconds (int): The amount of seconds to be counted.

    Returns:
        int: The time remaining to finish the stopwatch.
    """
    time_remainder = now().second % seconds

    return (seconds - time_remainder) if (time_remainder > 0) else 0
