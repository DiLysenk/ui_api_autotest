import allure
from pageobject.base_page import BasePage
from config import settings as cfg
from selenium.webdriver.common.by import By
from enum import Enum


class CssMainPage(Enum):
    CURRENCY = (By.CSS_SELECTOR, '.btn.btn-link.dropdown-toggle')
    CABINET = (By.CSS_SELECTOR, '.hidden-xs.hidden-sm.hidden-md')


class MainPage(BasePage):
    OpenCArt = f'http://{cfg.url.ip_docker}:7070'
    POUND_STERLING = "£ Pound Sterling"
    TABLETS = ''

    def __repr__(self):
        return ''

    def navigate(self):
        with allure.step(f'переход на страницу {self.OpenCArt}'):
            self.navigate_to(self.OpenCArt)

    def change_currency(self):
        with allure.step('изменить валюту'):
            self.click(CssMainPage.CURRENCY)
            self.find_by_text(self.POUND_STERLING).click()

    def forward_to_register(self):
        with allure.step('перейти к регистрации'):
            self.click(CssMainPage.CABINET)
            self.find_by_text('Регистрация').click()

    def choose_sort_by(self, value):
        with allure.step(f'выбрать сортировку {value}'):
            self.find_by_text('Tablets').click()
