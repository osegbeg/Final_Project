# movie_listing_app/logging_config.py

import logging
import logging.handlers

# Papertrail connection settings
PAPERTRAIL_HOST = "logs5.papertrailapp.com"
PAPERTRAIL_PORT = 45759

def configure_logging():
    logger = logging.getLogger()

    # Set the logging level
    logger.setLevel(logging.INFO)

    # Create a SysLogHandler for Papertrail
    handler = logging.handlers.SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # Adding logs to console as well
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


configure_logging()
