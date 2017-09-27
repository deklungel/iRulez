import logging

log_prefix = "iRulez"
log_initialized = False


# Init main logger
def init_logger():
    logger = logging.getLogger(log_prefix)
    logger.info('Dummy starting')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(" %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    global log_initialized
    log_initialized = True


def get_logger(name: str):
    if not log_initialized:
        init_logger()
    return logging.getLogger(log_prefix + "." + name)

