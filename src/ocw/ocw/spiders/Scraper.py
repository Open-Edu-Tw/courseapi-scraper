import logging
from functools import wraps
import sys

from loguru import logger
import scrapy


def init_logger(name, save_dir=None):
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    stream_handler = None
    for handler in logging.getLogger().handlers:
        if "StreamHandler" in str(handler):
            stream_handler = handler
    if stream_handler:
        logging.getLogger().removeHandler(stream_handler)

    intercept_handler = InterceptHandler()
    logging.getLogger().addHandler(intercept_handler)

    logger.configure(handlers=[{"sink": sys.stderr,}])
    logging.basicConfig(handlers=[intercept_handler], level=0)


    if save_dir:
        if save_dir[-1] != "/":
            save_dir += "/"
        logger.add(f"{save_dir}log/{name}.log", level="DEBUG", retention="2 months", rotation="1 day", enqueue=True)
        logger.add(f"{save_dir}log/{name}.error.log", level="ERROR", retention="2 months", rotation="1 day", enqueue=True)

    return logger


class Scraper(scrapy.Spider):
    @classmethod
    def get_element_handler(cls, default_return_value=""):
        def _get_element_handler(method):
            @wraps(method)
            def wrapper(*args, **kwargs):
                try:
                    result = method(*args, **kwargs)
                    return result
                except (IndexError, KeyError, TypeError, AttributeError) as e:  # cannot get element
                    args[0].logger.debug(f"{method.__name__} fails. No such element. {e}")
                    return default_return_value
                except Exception as e:
                    args[0].logger.exception("")
                    return default_return_value
            return wrapper
        return _get_element_handler
    
class OCWScraper(Scraper):
    mandatory_columns = ["name", "url"]
