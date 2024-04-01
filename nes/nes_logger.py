""""
This module contains the logger setup function for the NES project.
"""
import logging
from rich.logging import RichHandler

def setup_logger(logger_name: str) -> logging.Logger:
    """
    Set up a logger with the specified name.

    Args:
        logger_name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger object.

    """
    FORMAT = "%(filename)s:%(lineno)d [%(levelname)s] %(message)s"
    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)

    logging.Logger.addHandler(log, logging.FileHandler("nes.log", mode="a"))
    logging.Logger.addHandler(log, RichHandler(level="DEBUG"))
    for h in log.handlers:
        h.setFormatter(logging.Formatter(FORMAT))
    return log