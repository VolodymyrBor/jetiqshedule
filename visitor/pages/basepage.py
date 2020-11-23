import time
from typing import Union

from selenium.webdriver import Chrome, Firefox, Safari

from ..webdrivers import get_chrome


class BasePage:

    def __init__(self, url: str,
                 browser: Union[Chrome, Firefox, Safari] = None,
                 wait: float = 30):

        self.url = url
        self.browser = browser or get_chrome()
        self.browser.implicitly_wait(wait)

    def open(self):
        self.browser.get(self.url)

    @staticmethod
    def wait(time_: float):
        time.sleep(time_)

    def close(self):
        self.browser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
