import logging
from logging.handlers import RotatingFileHandler

LEVEL = logging.DEBUG

log_format = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=LEVEL, format=log_format)
rotation_handler = RotatingFileHandler(
    "jamwatch.log", maxBytes=1024 * 1024, backupCount=5
)
rotation_handler.setLevel(LEVEL)
rotation_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger(__name__)
logger.addHandler(rotation_handler)
