from selenium.common.exceptions import NoSuchElementException

from .basepage import BasePage
from ..locators import SubjectLocators


class SubjectPage(BasePage):

    def open_meeting(self):
        resources = self.browser.find_elements(*SubjectLocators.RESOURCES)
        for r in resources:
            try:
                r.find_element(*SubjectLocators.URL_TYPE)
            except NoSuchElementException:
                continue

            resource_name = r.find_element(*SubjectLocators.RESOURCE_NAME)
            resource_name.click()
            break
