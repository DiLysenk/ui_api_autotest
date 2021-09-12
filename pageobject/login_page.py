from selenium.webdriver.common.by import By
from config_parser import ConfigParser
from .base_page import BasePage

config = ConfigParser()


class LoginAdminPage(BasePage):
    USERNAME_ADMIN = (By.CSS_SELECTOR, '[name="username"]')
    PASSWORD_ADMIN = (By.CSS_SELECTOR, '[name="password"]')
    LOGIN_BUTTON_ADMIN = (By.CSS_SELECTOR, ".btn.btn-primary")
    ADMIN_PAGE = 'http://172.17.0.1:7070/admin/'

    def login_admin(self):
        self.enter_keys(self.verify_element_visible(self.USERNAME_ADMIN), config.LOGIN)
        self.enter_keys(self.verify_element_visible(self.PASSWORD_ADMIN), config.PASSWORD)
        self.click_element(self.verify_element_clickable(self.LOGIN_BUTTON_ADMIN))
