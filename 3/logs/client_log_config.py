import logging


# logging.basicConfig(
#     filename="app_client.log",
#     # filemode='',
#     format='%(levelname)-10s %(asctime)s %(name)s %(message)s',
#     # datefmt='',
#     level=logging.INFO,
#     # stream='',
# )


logger = logging.getLogger("client")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/app_client.log", encoding='utf8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


if __name__ == "__main__":
    logging.debug("This is a debug message")
    logging.info("Informational message")
    logging.error("An error has happened!")
    logging.critical("An critical_error!")
