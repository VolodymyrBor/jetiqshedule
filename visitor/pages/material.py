from typing import Iterable, List

from .basepage import BasePage
from ..locators import MaterialLocators
from lesson_schedule.shemes import Subject


class MaterialPage(BasePage):

    def get_subjects_urls(self, subjects: Iterable[Subject]) -> List[str]:
        all_rows = self.browser.find_elements(*MaterialLocators.SUBJECT_ROW)
        subjects = {(s.name, s.teacher) for s in subjects}
        subjects_urls = []
        for subject in all_rows:
            name: str = subject.find_element(*MaterialLocators.SUBJECT_NAME).text
            teacher: str = subject.find_element(*MaterialLocators.SUBJECT_TEACHER).text
            if (name.strip('.'), teacher.strip()) in subjects:
                url = subject.find_element(*MaterialLocators.SUBJECT_NAME).get_attribute('href')
                subjects_urls.append(url)

        return subjects_urls
