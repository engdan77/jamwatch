import logging
from logging.handlers import RotatingFileHandler

log_format = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
rotation_handler = RotatingFileHandler('jamwatch.log', maxBytes=1024*1024, backupCount=5)
rotation_handler.setLevel(logging.INFO)
rotation_handler.setFormatter(
    logging.Formatter(log_format)
)
logger = logging.getLogger(__name__)
logger.addHandler(rotation_handler)
