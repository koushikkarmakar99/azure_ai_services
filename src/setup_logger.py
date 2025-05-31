import sys, os
from loguru import logger
from flask import Flask

app = Flask(__name__)

# User-defined log destination: 'file', 'stdout', or 'both'
# LOG_DIR = "logs"
# LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logger():
    logger.remove()  # Remove the default logger
    logger.add(sys.stdout, 
        level="DEBUG", 
        format="[{time:YYYY-MM-DD HH:mm:ss}] | {level} | {name}:{line} | {message}", 
        colorize=True
    )  # Log to standard output

    return logger