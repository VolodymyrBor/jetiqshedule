import random

from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from sources import USER_AGENTS_FILE
from .drivers import CHROMEDRIVER_PATH

def get_user_agent() -> str:
    user_agents = USER_AGENTS_FILE.read_text().splitlines()
    return random.choice(user_agents)


def get_chrome(load: bool = True, proxy: str = None) -> webdriver.Chrome:
    """
    Create a chrome webdriver
    :return: chrome browser
    """
    cap = DesiredCapabilities().CHROME
    if not load:
        cap['pageLoadStrategy'] = 'none'

    seleniumwire_options = {
        'verify_ssl': False,  # Don't verify self-signed cert
    }

    if proxy:
        seleniumwire_options['proxy'] = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
            'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
        }

    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-agent={get_user_agent()}')

    chrome = webdriver.Chrome(
        desired_capabilities=cap,
        executable_path=CHROMEDRIVER_PATH,
        seleniumwire_options=seleniumwire_options
    )

    return chrome
