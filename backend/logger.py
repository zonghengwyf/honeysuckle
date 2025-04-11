import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name="uvicorn.error", log_file="webapi.log"):
    log_dir = '/var/logs/'
    os.makedirs(log_dir, exist_ok=True)  # 创建日志目录

    log_path = os.path.join(log_dir, log_file)

    handler = RotatingFileHandler(log_path, maxBytes=10 * 1024 * 1024, backupCount=10)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


logger = setup_logger()