from .basepage import BasePage
from ..locators import CabinetLocators


class CabinetPage(BasePage):

    def go_to_material(self):
        material = self.browser.find_element(*CabinetLocators.MATERIAL)
        material.click()
