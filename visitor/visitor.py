from typing import Iterable

from . import pages
from .locators import URLS
from .webdrivers import get_chrome
from lesson_schedule.schemes import Subject


class Visitor:
    """
    Goes to subject's pages and go to meet.
    """

    def __init__(self, subjects: Iterable[Subject], username: str, password: str):
        self.password = password
        self.username = username
        self.subjects = tuple(subjects)

    def run(self):
        browser = get_chrome(load=False)

        mainpage = pages.MainPage(url=URLS.LOGIN_URL, browser=browser)
        mainpage.open()
        mainpage.go_to_login()

        login_page = pages.LoginPage(browser=browser,
                                     url=mainpage.browser.current_url)

        login_page.login(username=self.username,
                         password=self.password)

        login_page.wait(1)

        material_page = pages.MaterialPage(browser=browser, url=URLS.MATERIAL_URL)
        material_page.open()
        subjects_urls = material_page.get_subjects_urls(self.subjects)
        for url in subjects_urls:
            subject_page = pages.SubjectPage(browser=browser, url=url, wait=1)
            subject_page.open()
            subject_page.open_meeting()
            subject_page.wait(2)

        browser.close()
