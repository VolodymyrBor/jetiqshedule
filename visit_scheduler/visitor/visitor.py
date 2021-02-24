from typing import Iterable

from shared import logger
from . import pages
from .locators import URLS
from .webdrivers import get_chrome
from lesson_schedule.schemes import Subject


class VisitorError(Exception):
    pass


class Visitor:
    """
    Goes to subject's pages and and open meet.
    """

    def __init__(self, username: str, password: str, headless: bool = False):
        self.headless = headless
        self.password = password
        self.username = username
        self.logger = logger.get_logger('Visitor')

    def run(self, subjects: Iterable[Subject]):
        """
        Run visits for subjects.
        :param subjects: subjects that will be visited.
        """
        subjects = tuple(subjects)
        browser = get_chrome(load=False, headless=self.headless)
        self.logger.info(f'Start visiting of {len(subjects)} subjects.')
        try:
            self._visit_subjects(subjects, browser)
        finally:
            browser.close()
        self.logger.info(f'Finished {len(subjects)} subjects.')

    def _visit_subjects(self, subjects: Iterable[Subject], browser):
        subjects = tuple(subjects)
        mainpage = pages.MainPage(url=URLS.LOGIN_URL, browser=browser)
        mainpage.open()
        mainpage.go_to_login()
        mainpage.wait(2)
        login_url = mainpage.browser.current_url
        login_page = pages.LoginPage(browser=browser,
                                     url=mainpage.browser.current_url)

        login_page.login(username=self.username,
                         password=self.password)

        login_page.wait(2)
        if login_url in login_page.browser.current_url:
            err_msg = f'Bad username or password for {self.username}'
            raise VisitorError(err_msg)

        material_page = pages.MaterialPage(browser=browser, url=URLS.MATERIAL_URL)
        material_page.open()
        subjects_urls = material_page.get_subjects_urls(subjects)

        if len(subjects_urls) != len(subjects):
            subjects_names = ', '.join(repr(s.name) for s in subjects)
            raise VisitorError(f'Subjects [{subjects_names}] were not found')

        self.logger.debug('Visiting subjects...')
        for url, subject in zip(subjects_urls, subjects):
            subject_page = pages.SubjectPage(browser=browser, url=url, wait=1)
            subject_page.open()
            subject_page.wait(1)
            subject_page.open_meeting(subject)
            subject_page.wait(2)
