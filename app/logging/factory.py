import logging


def logger_factory():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('logs/app.log', encoding='utf-8')
    formatter = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(pathname)s]')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
