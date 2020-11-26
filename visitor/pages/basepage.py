import time
from typing import Union

from selenium.webdriver import Chrome, Firefox, Safari

import logger
from ..webdrivers import get_chrome


class BasePage:

    def __init__(self, url: str,
                 browser: Union[Chrome, Firefox, Safari] = None,
                 wait: float = 30):

        self.url = url
        self.logger.info('Browser initializing.')
        self.browser = browser or get_chrome()
        self.browser.implicitly_wait(wait)
        self.logger = logger.get_logger(f'{type(self).__name__}')

    def open(self):
        self.logger.info(f'Opening page: {self.url}')
        self.browser.get(self.url)

    def wait(self, time_: float):
        self.logger.debug(f'Wait on {time_}s...')
        time.sleep(time_)

    def close(self):
        self.logger.info('Closing browser.')
        self.browser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
