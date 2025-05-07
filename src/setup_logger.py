import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
from flask import Flask

app = Flask(__name__)

# User-defined log destination: 'file', 'stdout', or 'both'
LOG_DESTINATION = 'both'
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logger():
    logger = logging.getLogger("FlaskApp")
    logger.setLevel(logging.DEBUG)

    os.makedirs(LOG_DIR, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')

    # Stdout handler
    if LOG_DESTINATION in ['stdout', 'both']:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    # Rotating File Handler (Logs rotate after reaching 1 MB)
    if LOG_DESTINATION in ['file', 'both']:
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=7)  # Rotates logs after reaching 1 MB
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Timed Rotating File Handler (Logs rotate after reaching 1 MB after a certain time interval)
        # if LOG_DESTINATION == 'both':
        #     timed_file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight', interval=1, backupCount=7)
        #     timed_file_handler.setFormatter(formatter)
        #     logger.addHandler(timed_file_handler)


    return logger
