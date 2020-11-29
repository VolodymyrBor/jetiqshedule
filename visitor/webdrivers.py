from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .drivers import CHROMEDRIVER_PATH


def get_chrome(load: bool = True, headless: bool = True) -> webdriver.Chrome:
    """
    Create a chrome webdriver
    :return: chrome browser
    """
    cap = DesiredCapabilities().CHROME
    if not load:
        cap['pageLoadStrategy'] = 'none'

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    chrome = webdriver.Chrome(
        desired_capabilities=cap,
        executable_path=CHROMEDRIVER_PATH,
        options=options,
    )

    return chrome
