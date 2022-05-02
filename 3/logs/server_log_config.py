import logging
import logging.handlers

logger = logging.getLogger("server")
logger.setLevel(logging.DEBUG)
fh = logging.handlers.TimedRotatingFileHandler("logs/app_server.log", encoding='utf8', interval=1, when='D')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


if __name__ == "__main__":
    logging.debug("This is a debug message")
    logging.info("Informational message")
    logging.error("An error has happened!")
    logging.critical("An critical_error!")
