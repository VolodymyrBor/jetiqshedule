import time
from typing import Union

from selenium.webdriver import Chrome, Firefox, Safari

import logger
from ..webdrivers import get_chrome


class BasePage:
    """
    Base class for any page.
    """
    def __init__(self, url: str,
                 browser: Union[Chrome, Firefox, Safari] = None,
                 wait: float = 30):
        self.url = url
        self.logger = logger.get_logger(f'{type(self).__name__}')
        self.browser = browser or get_chrome()
        self.browser.implicitly_wait(wait)

        if not browser:
            self.logger.info('Browser was created.')

    def open(self):
        """
        Open page.
        """
        self.logger.debug(f'Opening page: {self.url}')
        self.browser.get(self.url)

    def wait(self, time_: float):
        """
        Wait some time.
        :param time_: time in seconds.
        """
        self.logger.debug(f'Waiting on {time_}s...')
        time.sleep(time_)

    def close(self):
        """
        Close browser.
        """
        self.logger.info('Closing browser.')
        self.browser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
