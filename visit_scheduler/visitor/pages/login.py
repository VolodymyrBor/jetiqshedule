from .basepage import BasePage
from ..locators import LoginLocators


class LoginPage(BasePage):

    def login(self, username: str, password: str):
        """
        Login user in login page of jetiq.
        """
        self.logger.debug(f'Login {username}')

        login_input = self.browser.find_element(*LoginLocators.LOGIN_NAME)
        password_input = self.browser.find_element(*LoginLocators.PASSWORD)

        login_input.send_keys(username)
        self.wait(2)

        password_input.send_keys(password)
        self.wait(2)

        send = self.browser.find_element(*LoginLocators.ENTER_BUTTON)
        send.click()
