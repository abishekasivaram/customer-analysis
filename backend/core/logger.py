import logging
import os
from backend.core.config import OUTPUTS_DIR

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(OUTPUTS_DIR / "logs" / log_file)
    handler.setFormatter(formatter)
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)
    return logger

proc_logger = setup_logger('processing', 'processing.log')
perf_logger = setup_logger('performance', 'performance.log')
err_logger = setup_logger('error', 'error.log')
bus_logger = setup_logger('business', 'business.log')
dash_logger = setup_logger('dashboard', 'dashboard.log')
api_logger = setup_logger('api', 'api.log')
