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

    def __init__(self, username: str, password: str):
        self.password = password
        self.username = username
        self.logger = logger.get_logger('Visitor')

    def run(self, subjects: Iterable[Subject]):
        subjects = tuple(subjects)
        browser = get_chrome(load=False)
        self.logger.info(f'Start visiting of {len(subjects)} subjects.')
        try:
            self._visit_subjects(subjects, browser)
        finally:
            browser.close()
        self.logger.info(f'Finished {len(subjects)} subjects.')

    def _visit_subjects(self, subjects: Iterable[Subject], browser):
        mainpage = pages.MainPage(url=URLS.LOGIN_URL, browser=browser)
        mainpage.open()
        mainpage.go_to_login()
        mainpage.wait(2)
        login_page = pages.LoginPage(browser=browser,
                                     url=mainpage.browser.current_url)

        login_page.login(username=self.username,
                         password=self.password)

        login_page.wait(2)

        material_page = pages.MaterialPage(browser=browser, url=URLS.MATERIAL_URL)
        material_page.open()
        subjects_urls = material_page.get_subjects_urls(subjects)
        self.logger.debug('Visiting subjects...')
        for url, subject in zip(subjects_urls, subjects):
            subject_page = pages.SubjectPage(browser=browser, url=url, wait=1)
            subject_page.open()
            subject_page.wait(1)
            subject_page.open_meeting(subject)
            subject_page.wait(2)
