import logging
from pathlib import Path


# logging set up 
LOGS_DIR = Path('../logs/')
LOG_CRITICAL = Path(LOGS_DIR/'critical_errors.log')
LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
LOG_DEBUG = Path(LOGS_DIR/'debug.log')


# logging parameters set up and create logger
def logger_setup(name):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # create file handler which logs even debug messages
    log_handler_file = logging.FileHandler(f'{LOGS_DIR}/{name}.log', 'a')
    log_handler_file.setLevel(logging.DEBUG)
    
    # create console handler
    log_handler_console = logging.StreamHandler()
    log_handler_console.setLevel(logging.ERROR)
    
    # create formatter and add it to the handlers
    formatter = logging.Formatter(LOG_FORMATTER)
    log_handler_file.setFormatter(formatter)
    log_handler_console.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(log_handler_file)
    logger.addHandler(log_handler_console)
    
    return logger         