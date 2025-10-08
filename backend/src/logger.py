import logging


def setup_logger(log_level: str) -> None:
    """Configure the root logger with a standardized format.

    Args:
        log_level: The logging level to use (e.g., 'INFO', 'DEBUG', 'WARNING').

    Example:
        >>> setup_logger('INFO')
    """
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=log_level,
    )
