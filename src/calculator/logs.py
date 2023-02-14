# logs.py does what you expect...create loggers.
import os
import logging


# logging.basicConfig(level=logging.INFO)
LOG_FMT = '[%(levelname)s] %(module)s :: %(message)s'


def create_logger(name, level=logging.INFO, console=True):
    '''Create a simple logger with a file handler and optional console handler.

    Args:
        name: Name of the logger.
        level: Level to set the logger.
        console: Whether or not to add a StreamHandler to the logger.

    Returns:
        logging.Logger
    '''
    l = logging.getLogger(name)

    # Create a log file in the current working directory, should be
    # wherever the client/server are launched from.
    print(os.getcwd())
    log_filepath = os.path.join(os.getcwd(), '.data', 'calculator.log')
    if not os.path.exists(os.path.dirname(log_filepath)):
        os.makedirs(os.path.dirname(log_filepath), exist_ok=True)

    # Create a log handler for the file.
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(level)
    l.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        l.addHandler(console_handler)

    # Set log format so its consistent everywhere all at once.
    for h in l.handlers:
        h.setFormatter(logging.Formatter(LOG_FMT))

    l.setLevel(level)

    return l
