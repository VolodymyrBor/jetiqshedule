from selenium.webdriver.common.by import By


class URLS:
    """
    JetIQ pages urls
    """
    LOGIN_URL = "https://iq.vntu.edu.ua/"
    MATERIAL_URL = "https://iq.vntu.edu.ua/method/subj2.php"


class LoginLocators:
    """
    Locators for login page
    """
    LOGIN_LINK = (By.CSS_SELECTOR, "#s5_pos_top_row1_2 > div > div >"
                                   " div > div > div.s5_outer > div > div.icon_text > a")
    LOGIN_NAME = (By.CSS_SELECTOR, "#lnm")
    PASSWORD = (By.CSS_SELECTOR, "#pas")
    ENTER_BUTTON = (By.CSS_SELECTOR, "input[type=submit]")


class CabinetLocators:
    """
    Locators for student's cabinet page
    """
    MATERIAL = (By.CSS_SELECTOR, 'li:nth-child(2) > div > ul > li:nth-child(1) > a')


class MaterialLocators:
    """
    Locators for material page
    """
    SUBJECT_ROW = (By.CSS_SELECTOR, 'tbody > tr')
    SUBJECT_NAME = (By.CSS_SELECTOR, 'td:nth-child(2) > a')
    SUBJECT_TEACHER = (By.CSS_SELECTOR, 'td:nth-child(3) > a')


class SubjectLocators:
    """
    Locators for a subject page
    """
    RESOURCES = (By.CSS_SELECTOR, 'tbody > tr')
    RESOURCE_TYPE = (By.CSS_SELECTOR, 'td:nth-child(4)')
    RESOURCE_NAME = (By.CSS_SELECTOR, 'td:nth-child(2) > a')
    URL_TYPE = (By.CSS_SELECTOR, "[title='url']")
