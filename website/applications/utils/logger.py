import logging
import logging.handlers
import traceback

from website.config import Config


class Logger:
    def __init__(self, **kwargs):
        """
        This class creates a logger instance, with RotatingFileHandler.
        """
        try:
            name = kwargs.get("name", __name__)
            filepath = kwargs.get("logfile", Config.LOGFILE)
            log_level = kwargs.get("log_level", logging.DEBUG)
            self.logger = logging.getLogger(name)
            rf_handler = logging.handlers.RotatingFileHandler(
                filename=filepath, maxBytes=5 * 1024 * 1024, backupCount=5)
            fmt = logging.Formatter('[%(asctime)s:%(name)s - %(levelname)s'
                                    '- %(funcName)s ]- %(message)s')
            rf_handler.setFormatter(fmt)
            self.logger.addHandler(rf_handler)
            self.logger.setLevel(log_level)
        except Exception as e:
            traceback.print_exc()
            raise Exception(e)
