import os
import logging


logging.basicConfig(level=logging.INFO)
LOG_FMT = '[%(levelname)s] %(module)s :: %(message)s'


def create_logger(name, level=logging.INFO):
    l = logging.getLogger(name)
    log_filepath = os.path.join(os.getcwd(), '.data', 'calculator.log')
    if not os.path.exists(os.path.dirname(log_filepath)):
        os.makedirs(os.path.dirname(log_filepath), exist_ok=True)
    file_handler = logging.FileHandler(log_filepath)
    l.addHandler(file_handler)
    for h in l.handlers:
        h.setFormatter(logging.Formatter(LOG_FMT))
    l.setLevel(level)
    return l
