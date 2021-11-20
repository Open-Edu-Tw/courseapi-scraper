from abc import ABC
from functools import wraps

import scrapy


class Scraper(scrapy.Spider, ABC):
    @classmethod
    def get_element_handler(cls, default_return_value=""):
        def _get_element_handler(method):
            @wraps(method)
            def wrapper(*args, **kwargs):
                try:
                    result = method(*args, **kwargs)
                    return result or default_return_value
                except (IndexError, KeyError, TypeError, AttributeError) as e:  # cannot get element
                    args[0].logger.debug(f"{method.__name__} fails. No such a element. {e}")
                    return default_return_value
                except Exception as e:
                    args[0].logger.exception("")
                    return default_return_value

            return wrapper

        return _get_element_handler


class OCWScraper(Scraper, ABC):
    pass
