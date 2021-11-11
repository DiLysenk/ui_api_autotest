from .base_page import BasePage
from config_parser import ConfigParser
from selenium.webdriver.common.by import By
from enum import Enum

config = ConfigParser()

class CssMainPage(Enum):
    CURRENCY = (By.CSS_SELECTOR, '.btn.btn-link.dropdown-toggle')
    CABINET = (By.CSS_SELECTOR, '.hidden-xs.hidden-sm.hidden-md')



class MainPage(BasePage):
    OpenCArt = f'http://{config.IP_DOCKER}:7070'
    POUND_STERLING = "£ Pound Sterling"

    def change_currency(self):
        self.click_locator(CssMainPage.CURRENCY)
        self.click_element(self.is_visible_by_text(self.POUND_STERLING))

    def forward_to_register(self):
        self.click_locator(CssMainPage.CABINET)
        self.click_element(self.is_visible_by_text('Регистрация'))


