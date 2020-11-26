from .basepage import BasePage

from ..locators import LoginLocators


class MainPage(BasePage):

    def go_to_login(self):
        self.logger.debug('Find login page.')
        login_button = self.browser.find_element(*LoginLocators.LOGIN_LINK)
        login_button.click()
