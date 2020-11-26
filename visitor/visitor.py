from typing import Iterable

import logger
from . import pages
from .locators import URLS
from .webdrivers import get_chrome
from lesson_schedule.schemes import Subject


class Visitor:
    """
    Goes to subject's pages and go to meet.
    """

    def __init__(self, username: str, password: str, proxy: str = None):
        self.proxy = proxy
        self.password = password
        self.username = username
        self.logger = logger.get_logger('Visitor')

    def run(self, subjects: Iterable[Subject]):
        subjects = tuple(subjects)
        browser = get_chrome(load=False, proxy=self.proxy)
        try:
            self._visit_subjects(subjects, browser)
        finally:
            browser.close()
        self.logger.info('Finished.')

    def _visit_subjects(self, subjects: Iterable[Subject], browser):
        mainpage = pages.MainPage(url=URLS.LOGIN_URL, browser=browser)
        self.logger.info('Open main page.')
        mainpage.open()
        self.logger.info('Go to login page.')
        mainpage.go_to_login()

        login_page = pages.LoginPage(browser=browser,
                                     url=mainpage.browser.current_url)

        self.logger.info('Login user.')
        login_page.login(username=self.username,
                         password=self.password)

        login_page.wait(1)

        material_page = pages.MaterialPage(browser=browser, url=URLS.MATERIAL_URL)
        self.logger.info('Go to material')
        material_page.open()
        subjects_urls = material_page.get_subjects_urls(subjects)
        self.logger.info('Visiting subjects...')
        for url, subject in zip(subjects_urls, subjects):
            subject_page = pages.SubjectPage(browser=browser, url=url, wait=1)
            subject_page.open()
            subject_page.wait(1)
            subject_page.open_meeting(subject)
            subject_page.wait(2)
