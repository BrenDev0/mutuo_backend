import os
import logging


def configure_logger():
    level = os.getenv("LOGGER_LEVEL", logging.INFO)

    logging.basicConfig(
        level=int(level),
        format="%(levelname)s - %(name)s - %(message)s"
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.debug("!!!!! LOGGER LEVEL SET TO DEBUG !!!!!")