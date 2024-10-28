import logging
from external.external import ExternalClass
from logger.logger import init_logging


def main():
    logger = logging.getLogger(__name__)
    logger.info("starting")
    a = ExternalClass()
    a.external_function()
    logger.error("finished")


if __name__ == "__main__":
    init_logging()
    main()
