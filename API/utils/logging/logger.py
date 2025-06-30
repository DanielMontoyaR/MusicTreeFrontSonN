import logging
from logging.handlers import RotatingFileHandler
import os

def configurar_logger(nombre="api_logger", archivo_log="logs/api_errors.log"):
    os.makedirs(os.path.dirname(archivo_log), exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(archivo_log, maxBytes=10240, backupCount=5)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]"
        )
        handler.setFormatter(formatter)
        handler.setLevel(logging.ERROR)
        logger.addHandler(handler)

    return logger
