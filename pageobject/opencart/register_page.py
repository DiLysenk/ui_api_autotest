import allure

from component.base_page import BasePage
from selenium.webdriver.common.by import By
from enum import Enum
from config import settings as cfg


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
    URL_REGISTER = f'http://{cfg.url.ip_docker}:7070/index.php?route=account/register'

    def fill_form(self, name, email):
        with allure.step('fill forms in fields'):
            self.fill_input(CssRegisterPage.FIRST_NAME, name)
            self.fill_input(CssRegisterPage.LAST_NAME, name)
            self.fill_input(CssRegisterPage.EMAIL, email)
            self.fill_input(CssRegisterPage.TELEPHONE, "123456789")
            self.fill_input(CssRegisterPage.PASSWORD, "123456")
            self.fill_input(CssRegisterPage.PASSWORD_CONFIRM, "123456")
            return self

    def agree_policy(self):
        with allure.step('click in registration'):
            self.click(CssRegisterPage.CHECK_BOX_AGREE)
            return self

    def click_continue(self):
        with allure.step('click in continue'):
            self.click(CssRegisterPage.CONTINUE)
