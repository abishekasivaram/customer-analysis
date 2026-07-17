import logging
import os
from pathlib import Path

# Make sure root logs dir exists
os.makedirs("logs", exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    log_path = Path(log_file)
    os.makedirs(log_path.parent, exist_ok=True)
    
    handler = logging.FileHandler(log_path)
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

proc_logger = setup_logger('processing', 'logs/processing.log')
perf_logger = setup_logger('performance', 'logs/performance.log')
err_logger = setup_logger('error', 'logs/error.log')

# --- Phase 3 Loggers ---
bus_logger = setup_logger('business_logger', 'logs/business/business.log')
dash_logger = setup_logger('dashboard_logger', 'logs/business/dashboard.log')
api_logger = setup_logger('api_logger', 'logs/api/api.log')

# --- Phase 4 Loggers ---
adv_logger = setup_logger('advisor_logger', 'logs/advisor/advisor.log')
rec_logger = setup_logger('recommendation_logger', 'logs/advisor/recommendation.log')
rule_logger = setup_logger('rule_engine_logger', 'logs/advisor/rule_engine.log')
val_logger = setup_logger('validation_logger', 'logs/advisor/validation.log')
adv_perf_logger = setup_logger('advisor_perf_logger', 'logs/advisor/performance.log')
adv_err_logger = setup_logger('advisor_error_logger', 'logs/advisor/errors.log')
