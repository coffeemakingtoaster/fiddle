import logging


class LogFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    green = "\x1b[32;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey,
        logging.INFO: green,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red,
    }

    def format(self, record):
        return (
            self.FORMATS.get(record.levelno, self.grey)
            + super().format(record)
            + self.reset
        )


def init_logging():
    logging.basicConfig(
        # format="%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s",
        # datefmt="%m-%d %H:%M",
        level=logging.DEBUG,
    )
    console = logging.StreamHandler()
    # set a format which is simpler for console use
    formatter = LogFormatter("%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s")
    # tell the handler to use this format
    console.setFormatter(formatter)
    # set to be the only logger
    # This is likely not the cleanest way to do this as this would also overwrite file handlers
    logging.getLogger("").handlers = [console]
