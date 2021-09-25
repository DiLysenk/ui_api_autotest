from selenium.webdriver.common.by import By
from config_parser import ConfigParser
from pageobject.base_page import BasePage
from enum import Enum

config = ConfigParser()


class CssLoginAdminPage(Enum):
    USERNAME_ADMIN = (By.CSS_SELECTOR, '[name="username"]')
    PASSWORD_ADMIN = (By.CSS_SELECTOR, '[name="password"]')
    LOGIN_BUTTON_ADMIN = (By.CSS_SELECTOR, ".btn.btn-primary")


class LoginAdminPage(BasePage):
    ADMIN_PAGE = 'http://172.17.0.1:7070/admin/'

    def login_admin(self):
        self.clear_and_send_keys(self.is_visible(CssLoginAdminPage.USERNAME_ADMIN), config.LOGIN)
        self.clear_and_send_keys(self.is_visible(CssLoginAdminPage.PASSWORD_ADMIN), config.PASSWORD)
        self.click_locator(CssLoginAdminPage.LOGIN_BUTTON_ADMIN)
