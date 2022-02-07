from selenium.webdriver.common.by import By
from config import settings as cfg
from component.base_page import BasePage
from enum import Enum
import allure


class CssLoginAdminPage(Enum):
    USERNAME_ADMIN = (By.CSS_SELECTOR, '[name="username"]')
    PASSWORD_ADMIN = (By.CSS_SELECTOR, '[name="password"]')
    LOGIN_BUTTON_ADMIN = (By.CSS_SELECTOR, ".btn.btn-primary")


class LoginAdminPage(BasePage):
    ADMIN_PAGE = f'http://{cfg.url.ip_docker}:7070/admin/'

    loc = CssLoginAdminPage

    def navigate(self):
        with allure.step('Открываем экран '):
            self.open_url(self.ADMIN_PAGE)

    def login_admin(self):
        with allure.step('Логинимся на страницу'):
            self.fill_input(self.loc.USERNAME_ADMIN, cfg.user.username)
            self.fill_input(self.loc.PASSWORD_ADMIN, cfg.user.password)
            self.click(self.loc.LOGIN_BUTTON_ADMIN)
