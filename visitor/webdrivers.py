from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .drivers import CHROMEDRIVER_PATH


def get_chrome(load: bool = True) -> webdriver.Chrome:
    """
    Create a chrome webdriver
    :return: chrome browser
    """
    cap = DesiredCapabilities().CHROME
    if not load:
        cap['pageLoadStrategy'] = 'none'

    chrome = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, desired_capabilities=cap)

    return chrome
