from .base_page import BasePage
from selenium.webdriver.common.by import By


class RegisterPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, '[placeholder="First Name"]')
    LAST_NAME = (By.CSS_SELECTOR, '[placeholder="Last Name"]')
    EMAIL = (By.CSS_SELECTOR, '[placeholder="E-Mail"]')
    TELEPHONE = (By.CSS_SELECTOR, '[placeholder="Telephone"]')
    PASSWORD = (By.CSS_SELECTOR, '[placeholder="Password"]')
    PASSWORD_CONFIRM = (By.CSS_SELECTOR, '[placeholder="Password Confirm"]')
    CHECK_BOX_AGREE = (By.CSS_SELECTOR, '[name="agree"]')
    CONTINUE = (By.CSS_SELECTOR, '[value="Continue"]')
    URL_REGISTER = 'http://172.17.0.1:7070/index.php?route=account/register'


    def fill_form(self, name, email):
        self.enter_keys(self.verify_element_visible(self.FIRST_NAME), name)
        self.enter_keys(self.verify_element_visible(self.LAST_NAME), name)
        self.enter_keys(self.verify_element_visible(self.EMAIL), email)
        self.enter_keys(self.verify_element_visible(self.TELEPHONE), "123456789")
        self.enter_keys(self.verify_element_visible(self.PASSWORD), "123456")
        self.enter_keys(self.verify_element_visible(self.PASSWORD_CONFIRM), "123456")
        return self

    def agree_policy(self):
        self.click_element(self.verify_element_clickable(self.CHECK_BOX_AGREE))
        return self

    def click_continue(self):
        self.click_element(self.verify_element_visible(self.CONTINUE))
