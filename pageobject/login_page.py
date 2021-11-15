from selenium.webdriver.common.by import By
from config_parser import ConfigParser
from pageobject.base_page import BasePage
from enum import Enum
import allure

config = ConfigParser()


class CssLoginAdminPage(Enum):
    USERNAME_ADMIN = (By.CSS_SELECTOR, '[name="username"]')
    PASSWORD_ADMIN = (By.CSS_SELECTOR, '[name="password"]')
    LOGIN_BUTTON_ADMIN = (By.CSS_SELECTOR, ".btn.btn-primary")


class LoginAdminPage(BasePage):
    ADMIN_PAGE = f'http://{config.IP_DOCKER}:7070/admin/'

    def navigate(self):
        with allure.step('Открываем экран '):
            self.open_page_by_url(self.ADMIN_PAGE)

    def login_admin(self):
        with allure.step('Логин на страницу'):
            self.clear_and_send_keys(self.is_visible(CssLoginAdminPage.USERNAME_ADMIN), config.LOGIN)
            self.clear_and_send_keys(self.is_visible(CssLoginAdminPage.PASSWORD_ADMIN), config.PASSWORD)
            self.click_locator(CssLoginAdminPage.LOGIN_BUTTON_ADMIN)
