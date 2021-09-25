from .base_page import BasePage
from selenium.webdriver.common.by import By
from enum import Enum


class CssRegisterPage(Enum):
    FIRST_NAME = (By.CSS_SELECTOR, '[placeholder="First Name"]')
    LAST_NAME = (By.CSS_SELECTOR, '[placeholder="Last Name"]')
    EMAIL = (By.CSS_SELECTOR, '[placeholder="E-Mail"]')
    TELEPHONE = (By.CSS_SELECTOR, '[placeholder="Telephone"]')
    PASSWORD = (By.CSS_SELECTOR, '[placeholder="Password"]')
    PASSWORD_CONFIRM = (By.CSS_SELECTOR, '[placeholder="Password Confirm"]')
    CHECK_BOX_AGREE = (By.CSS_SELECTOR, '[name="agree"]')
    CONTINUE = (By.CSS_SELECTOR, '[value="Continue"]')


class RegisterPage(BasePage):
    URL_REGISTER = 'http://172.17.0.1:7070/index.php?route=account/register'

    def fill_form(self, name, email):
        self.clear_and_send_keys(self.is_visible(CssRegisterPage.FIRST_NAME), name)
        self.clear_and_send_keys(self.is_visible(CssRegisterPage.LAST_NAME), name)
        self.clear_and_send_keys(self.is_visible(CssRegisterPage.EMAIL), email)
        self.clear_and_send_keys(self.is_visible(CssRegisterPage.TELEPHONE), "123456789")
        self.clear_and_send_keys(self.is_visible(CssRegisterPage.PASSWORD), "123456")
        self.clear_and_send_keys(self.is_visible(CssRegisterPage.PASSWORD_CONFIRM), "123456")
        return self

    def agree_policy(self):
        self.click_locator(CssRegisterPage.CHECK_BOX_AGREE)
        return self

    def click_continue(self):
        self.click_locator(CssRegisterPage.CONTINUE)
