import random

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from sources import USER_AGENTS_FILE
from .drivers import CHROMEDRIVER_PATH

def get_user_agent() -> str:
    user_agents = USER_AGENTS_FILE.read_text().splitlines()
    return random.choice(user_agents)


def get_chrome(load: bool = True) -> webdriver.Chrome:
    """
    Create a chrome webdriver
    :return: chrome browser
    """
    cap = DesiredCapabilities().CHROME
    if not load:
        cap['pageLoadStrategy'] = 'none'

    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-agent={get_user_agent()}')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    chrome = webdriver.Chrome(
        desired_capabilities=cap,
        executable_path=CHROMEDRIVER_PATH,
    )

    return chrome
