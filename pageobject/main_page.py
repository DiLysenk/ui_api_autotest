import allure

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
    TABLETS = ''

    def __repr__(self):
        return ''

    def navigate(self):
        with allure.step(f'переход на страницу {self.OpenCArt}'):
            self.open_page_by_url(self.OpenCArt)

    def change_currency(self):
        with allure.step('изменить валюту'):
            self.click(CssMainPage.CURRENCY)
            self.click_element(self.is_visible_by_text(self.POUND_STERLING))

    def forward_to_register(self):
        with allure.step('перейти к регистрации'):
            self.click(CssMainPage.CABINET)
            self.click_element(self.is_visible_by_text('Регистрация'))


    def choose_sort_by(self, value):
        with allure.step(f'выбрать сортировку {value}'):
            self.is_visible_by_text('Tablets').click()
            self.choose(value)

