import logging


class ExternalClass:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.warn("init")

    def external_function(self):
        self.logger.debug("function")
